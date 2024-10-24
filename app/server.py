# -*- coding: utf-8 -*-
"""
Authors: Chris Hay, Mihai Criveti
Description: FastAPI Server, loads applications dynamically
"""

import logging
import os
import sys
from importlib import import_module
from pathlib import Path
from typing import Awaitable, Callable, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


# Set up logging
# ANSI escape sequences for colors
class ColorFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34;1m"
    reset = "\x1b[0m"
    # Format string defined before usage
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.grey + self.format_str + self.reset)  # Default format
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Set up logging with custom formatter
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
log = logging.getLogger(__name__)

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# List of directories to skip
SKIP_ROUTE_DIRECTORIES_LIST = {
    "__pycache__",
    ".pytest_cache",
    ".tox",
    ".ruff_cache",
    ".pyre",
    ".mypy_cache",
    ".pytype",
}

# Load dotenv
load_dotenv()

# Define default auth tokens and read from env if defined
DEFAULT_AUTH_TOKENS = ["dev-only-token"]
auth_tokens_env: Optional[str] = os.getenv("ICA_AUTH_TOKENS")

if auth_tokens_env:
    AUTH_TOKENS: List[str] = auth_tokens_env.split(",")
else:
    AUTH_TOKENS = DEFAULT_AUTH_TOKENS
    log.warning("No ICA_AUTH_TOKENS provided in environment; using default tokens.")

# Set up FastAPI application
app = FastAPI(
    title="IBM Consulting Assistants Integrations Host",
    version="1.0",
    description="Hosts integrations",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the 'public' directory if it doesn't exist
public_dir = Path("public")
if not public_dir.exists():
    public_dir.mkdir(parents=True)
    log.info(f"Created 'public' directory at {public_dir.resolve()}")

# Serve static files from 'public' directory
app.mount("/public", StaticFiles(directory="public"), name="public")
log.info("Mounted 'public' directory as static files at /public")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class AuthTokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware for checking auth tokens.

    Checks for the presence of a valid authorization token in the request headers.
    Requests to the '/public' and '/health' paths are allowed without an Integrations-API-Key header.

    Args:
        app (FastAPI): The FastAPI application instance.

    Methods:
        dispatch(request: Request, call_next: Callable) -> Response:
            Checks for a valid authorization token in the request headers unless
            the request is targeting the '/public' path or the '/health' path.

    Example:
        >>> from fastapi.testclient import TestClient
        >>> client = TestClient(app)
        >>> response = client.get("/some_route", headers={"Integrations-API-Key": "default_token_1"})
        >>> response.status_code
        200
        >>> response = client.get("/public/README.md")  # No Integrations-API-Key header required
        >>> response.status_code
        200
        >>> response = client.get("/health")  # No Integrations-API-Key header required
        >>> response.status_code
        200
        >>> response = client.get("/some_route", headers={"Integrations-API-Key": "invalid_token"})
        >>> response.status_code
        401
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Skip auth check for the '/public' and '/health' paths
        #        if request.url.path.startswith(("/public", "/health", "/favicon.ico", "/docs", "/openapi.json")):
        # if request.url.path.startswith(("/public", "/health", "/favicon.ico")):
        if request.url.path.startswith(
            (
                "/public",
                "/health",
                "/system/file_upload/retrievers/get_upload_url/invoke",
                "/system/file_upload/upload",
                "/system/file_upload/download",
                "/system/file_upload/list",
                "system/file_upload/delete",
                "/file_upload_ui",
                "/static",
                "/docs",
                "/openapi.json"
            )
        ):
            log.debug(f"Skipping auth check for path: {request.url.path}")
            return await call_next(request)

        # Allow CORS preflight requests
        if request.method == "OPTIONS":
            return await call_next(request)

        auth_token = request.headers.get("Integrations-API-Key")
        if auth_token not in AUTH_TOKENS:
            log.warning(f"Unauthorized access attempt with token: {auth_token}")
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
        response = await call_next(request)
        return response


# Add the AuthTokenMiddleware to the FastAPI app
app.add_middleware(AuthTokenMiddleware)
log.debug("Added AuthTokenMiddleware to FastAPI app")


def register_routes_from_folder(folder: Path) -> None:
    """
    Register routes from a specified folder.

    Args:
        folder (Path): The directory containing route modules.

    Returns:
        None

    Example:
        >>> from pathlib import Path
        >>> register_routes_from_folder(Path("app/routes"))
    """
    log.info(f"Checking routes in directory: {folder}")
    module_base = "dev.app.routes" if "dev/app/routes" in str(folder) else "app.routes"
    log.info(f"Module base: {module_base}")

    for route_folder in folder.iterdir():
        if route_folder.is_dir() and route_folder.name not in SKIP_ROUTE_DIRECTORIES_LIST:
            router_file_name = f"{route_folder.name}_router"  # Load route from the <folder_name>_router.py
            module_name = f"{module_base}.{route_folder.name}.{router_file_name}"
            try:
                route_module = import_module(module_name)
                log.info(f"Successfully loaded module: {ColorFormatter.blue}{module_name}{ColorFormatter.reset}")
            except ModuleNotFoundError as e:
                log.error(f"Failed to load module: {module_name}. Error: {e}")
                continue
            if hasattr(route_module, "add_custom_routes"):
                route_module.add_custom_routes(app)
                log.debug(f"* Registered custom routes from: {module_name}")


# Register standard routes
routes_folder = project_root / "app" / "routes"
register_routes_from_folder(routes_folder)

# Register development routes if the environment variable is set
if os.getenv("ICA_DEV_ROUTES") == "1":
    dev_routes_folder = project_root / "dev" / "app" / "routes"
    log.info(f"*** Registering DEV routes from {dev_routes_folder} ***")
    register_routes_from_folder(dev_routes_folder)
