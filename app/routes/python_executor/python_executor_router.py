# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Python Code Executor - Securely executes Python code with various safety measures.

This module provides a FastAPI router for securely executing Python code and generating code based on user queries.
It implements various security measures to ensure safe code execution.
"""

import ast
import asyncio
import builtins
import json
import logging
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field
from RestrictedPython import compile_restricted, limited_builtins, safe_builtins, utility_builtins
from RestrictedPython.Guards import guarded_unpack_sequence
from RestrictedPython.PrintCollector import PrintCollector

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables
DEFAULT_TIMEOUT = int(os.getenv("PYTHON_EXECUTOR_DEFAULT_TIMEOUT", "5"))
DEFAULT_MAX_MEMORY = int(os.getenv("PYTHON_EXECUTOR_DEFAULT_MAX_MEMORY", "100"))
MAX_TIMEOUT = int(os.getenv("PYTHON_EXECUTOR_MAX_TIMEOUT", "30"))
MAX_MEMORY = int(os.getenv("PYTHON_EXECUTOR_MAX_MEMORY", "500"))
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Mistral Large")
MAX_INPUT_LENGTH = int(os.getenv("PYTHON_EXECUTOR_MAX_INPUT_LENGTH", "1000"))
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/python_executor/templates"))


class ExecuteInputModel(BaseModel):
    """Model to validate input data for code execution."""

    code: str = Field(..., max_length=MAX_INPUT_LENGTH)


class GenerateInputModel(BaseModel):
    """Model to validate input data for code generation and execution."""

    query: str = Field(..., max_length=MAX_INPUT_LENGTH)


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def sanitize_user_input(input_str: str) -> Optional[str]:
    """
    Sanitize user input to prevent potential security issues.

    This function uses abstract syntax tree (AST) parsing to identify and block:
    1. Imports of any kind
    2. Calls to specific built-in functions
    3. Use of certain attributes that could lead to unsafe operations

    Args:
        input_str (str): The user input to sanitize.

    Returns:
        Optional[str]: The sanitized input if it passes all checks, None otherwise.

    Raises:
        ValueError: If potentially unsafe operations are detected.
    """
    dangerous_builtins = {"eval", "exec", "compile", "__import__"}
    dangerous_attributes = {"__globals__", "__getattribute__", "__class__"}

    class InputAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.errors = []

        def visit_Import(self, node):
            self.errors.append("Imports are not allowed in user input")
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            self.errors.append("Imports are not allowed in user input")
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in dangerous_builtins:
                self.errors.append(f"Unsafe builtin function call detected: {node.func.id}")
            self.generic_visit(node)

        def visit_Attribute(self, node):
            if node.attr in dangerous_attributes:
                self.errors.append(f"Unsafe attribute access detected: {node.attr}")
            self.generic_visit(node)

    try:
        tree = ast.parse(input_str)
        analyzer = InputAnalyzer()
        analyzer.visit(tree)

        if analyzer.errors:
            log.warning(f"Unsafe operations detected in user input: {', '.join(analyzer.errors)}")
            return None

        sanitized_input = input_str.strip()[:MAX_INPUT_LENGTH]
        log.info(f"Sanitized input: {sanitized_input}")
        return sanitized_input
    except SyntaxError:
        # If it's not valid Python syntax, it's probably just a query string, so we'll allow it
        sanitized_input = input_str.strip()[:MAX_INPUT_LENGTH]
        log.info(f"Non-Python input sanitized: {sanitized_input}")
        return sanitized_input


def sanitize_code(code: str) -> str:
    """
    Sanitize the code to prevent potentially dangerous operations.

    This function uses abstract syntax tree (AST) parsing to identify and block:
    1. Imports of specific modules
    2. Calls to specific built-in functions
    3. Use of certain attributes that could lead to unsafe operations

    Args:
        code (str): The Python code to sanitize.

    Returns:
        str: The sanitized code if it passes all checks.

    Raises:
        ValueError: If potentially unsafe operations are detected.
    """
    dangerous_imports = {"os", "sys", "subprocess", "shutil", "socket"}
    dangerous_builtins = {"eval", "exec", "compile", "__import__"}
    dangerous_attributes = {"__globals__", "__getattribute__", "__class__"}

    class CodeAnalyzer(ast.NodeVisitor):
        def __init__(self):
            self.errors = []

        def visit_Import(self, node):
            for alias in node.names:
                if alias.name in dangerous_imports:
                    self.errors.append(f"Unsafe import detected: {alias.name}")
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            if node.module in dangerous_imports:
                self.errors.append(f"Unsafe import detected: {node.module}")
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in dangerous_builtins:
                self.errors.append(f"Unsafe builtin function call detected: {node.func.id}")
            self.generic_visit(node)

        def visit_Attribute(self, node):
            if node.attr in dangerous_attributes:
                self.errors.append(f"Unsafe attribute access detected: {node.attr}")
            self.generic_visit(node)

    try:
        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)

        if analyzer.errors:
            raise ValueError("\n".join(analyzer.errors))

        log.info(f"Code passed security checks: {code}")
        return code
    except SyntaxError as e:
        log.error(f"Syntax error in code: {str(e)}")
        raise ValueError(f"Syntax error in code: {str(e)}")
    except Exception as e:
        log.error(f"Error during code sanitization: {str(e)}")
        raise ValueError(f"Error during code sanitization: {str(e)}")


def _safe_exec(code: str, max_memory: int) -> Any:
    import resource

    resource.setrlimit(resource.RLIMIT_AS, (max_memory * 1024 * 1024, resource.RLIM_INFINITY))

    restricted_globals = {
        "__builtins__": {
            **safe_builtins,
            "sum": builtins.sum,
            "print": builtins.print,
            "range": builtins.range,
            "int": builtins.int,
            "float": builtins.float,
            "str": builtins.str,
            "list": builtins.list,
            "dict": builtins.dict,
            "set": builtins.set,
            "len": builtins.len,
            "max": builtins.max,
            "min": builtins.min,
            "all": builtins.all,
        },
        "_print_": PrintCollector,
        "_getattr_": getattr,
        "_getitem_": lambda obj, key: obj[key],
        "_write_": lambda x: x,
        "_getiter_": iter,
        "_iter_unpack_sequence_": guarded_unpack_sequence,
    }
    restricted_globals.update(utility_builtins)
    restricted_globals.update(limited_builtins)

    local_vars: Dict[str, Any] = {}
    exec(compile_restricted(code, "<string>", "exec"), restricted_globals, local_vars)

    if "result" in local_vars:
        return local_vars["result"]
    elif "printed" in local_vars:
        return local_vars["printed"]
    else:
        return None


async def execute_code_with_timeout(code: str, timeout: int, max_memory: int) -> Tuple[Any, str]:
    """Execute the given Python code securely with a timeout and memory limit."""
    try:
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=1) as executor:
            result = await asyncio.wait_for(
                loop.run_in_executor(executor, _safe_exec, code, max_memory),
                timeout=timeout,
            )
        log.info(f"Code execution result: {result}")
        return result, code
    except asyncio.TimeoutError:
        log.error(f"Execution timed out after {timeout} seconds")
        raise TimeoutError(f"Execution timed out after {timeout} seconds")
    except Exception as e:
        log.error(f"Execution error: {str(e)}")
        raise Exception(f"Execution error: {str(e)}")


async def generate_code_with_llm(query: str) -> Tuple[str, str, str]:
    prompt_template = template_env.get_template("code_generation_prompt.jinja")
    prompt = prompt_template.render(query=query)
    log.info(f"Generated prompt for LLM: {prompt}")
    log.info(f"Using model: {DEFAULT_MODEL}")  # Debug to check model ID

    try:
        client = ICAClient()
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=1) as executor:
            response_future = loop.run_in_executor(
                executor,
                lambda: client.prompt_flow(model_id_or_name=DEFAULT_MODEL, prompt=prompt),
            )
            response = await response_future

        log.info(f"Raw LLM response: {response}")
        response_data = json.loads(response)

        if "code" not in response_data or "explanation" not in response_data:
            raise ValueError("Invalid response format from LLM")

        generated_code = response_data["code"]
        explanation = response_data["explanation"]
        log.info(f"Generated code: {generated_code}")
        log.info(f"Code explanation: {explanation}")

        return generated_code, explanation, ""
    except json.JSONDecodeError:
        error_message = "Failed to parse LLM response as JSON"
        log.error(error_message)
        return "", "", error_message
    except Exception as e:
        error_message = f"Error in code generation: {str(e)}"
        log.error(error_message)
        return "", "", error_message


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/system/python_executor/execute_code/invoke")
    async def execute_python_code(request: Request) -> OutputModel:
        """Handle POST requests to execute Python code securely."""
        invocation_id = str(uuid4())
        log.info(f"Executing code with invocation ID: {invocation_id}")

        try:
            data = await request.json()
            input_data = ExecuteInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"Invalid input: {str(e)}", type="text")],
            )

        sanitized_code = sanitize_user_input(input_data.code)
        if sanitized_code is None:
            log.warning("Potentially unsafe code detected")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[
                    ResponseMessageModel(
                        message="Invalid input: Potentially unsafe code detected",
                        type="text",
                    )
                ],
            )

        try:
            sanitized_code = sanitize_code(sanitized_code)
            result, executed_code = await execute_code_with_timeout(sanitized_code, DEFAULT_TIMEOUT, DEFAULT_MAX_MEMORY)

            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(
                code=executed_code,
                result=result,
                explanation="Code executed successfully.",
            )

            log.info(f"Code execution successful for invocation ID: {invocation_id}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )
        except TimeoutError as e:
            log.error(f"Execution timed out: {str(e)}")
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(
                code=input_data.code,
                result="",
                explanation=f"Execution timed out: {str(e)}",
            )
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )
        except Exception as e:
            log.error(f"Execution error: {str(e)}")
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(
                code=input_data.code,
                result="",
                explanation=f"Execution error: {str(e)}",
            )
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )

    @app.post("/experience/python_executor/generate_and_execute/invoke")
    async def generate_and_execute_python_code(request: Request) -> OutputModel:
        """Handle POST requests to generate and execute Python code securely."""
        invocation_id = str(uuid4())
        log.info(f"Generating and executing code with invocation ID: {invocation_id}")

        try:
            data = await request.json()
            input_data = GenerateInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"Invalid input: {str(e)}", type="text")],
            )

        sanitized_query = sanitize_user_input(input_data.query)
        if sanitized_query is None:
            log.warning("Potentially unsafe query detected")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[
                    ResponseMessageModel(
                        message="Invalid input: Potentially unsafe query detected",
                        type="text",
                    )
                ],
            )

        generated_code = ""
        explanation = ""
        try:
            generated_code, explanation, error_message = await generate_code_with_llm(sanitized_query)
            if error_message:
                log.error(f"Error in code generation: {error_message}")
                response_template = template_env.get_template("response_template.jinja")
                rendered_response = response_template.render(code=generated_code, result="", explanation=error_message)
                return OutputModel(
                    status="success",
                    invocationId=invocation_id,
                    response=[ResponseMessageModel(message=rendered_response, type="text")],
                )

            sanitized_code = sanitize_code(generated_code)
            result, executed_code = await execute_code_with_timeout(sanitized_code, DEFAULT_TIMEOUT, DEFAULT_MAX_MEMORY)

            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(code=executed_code, result=result, explanation=explanation)

            log.info(f"Code generation and execution successful for invocation ID: {invocation_id}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )
        except TimeoutError as e:
            log.error(f"Execution timed out: {str(e)}")
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(
                code=generated_code,
                result="",
                explanation=f"Execution timed out: {str(e)}",
            )
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )
        except MemoryError as e:
            log.error(f"Memory limit exceeded: {str(e)}")
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(
                code=generated_code,
                result="",
                explanation=f"Memory limit exceeded: {str(e)}",
            )
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )
        except Exception as e:
            log.error(f"Execution error: {str(e)}")
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(code=generated_code, result="", explanation=f"Execution error: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response, type="text")],
            )
