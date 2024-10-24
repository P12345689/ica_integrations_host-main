# -*- coding: utf-8 -*-
"""
Authors: Chris Hay, Mihai Criveti
Description: IBM Consulting Assistants Langchain Extensions API - Python SDK
"""

from typing import Any, Dict

from .llms import ConsultingAssistantsLLM


class ChatConsultingAssistants(ConsultingAssistantsLLM):
    """
    A class to handle chat interactions with consulting assistants.

    This class extends the ConsultingAssistantsLLM and provides a method to
    call the language model with a formatted prompt based on provided parameters.
    """

    def __call__(self, prompt_params: Dict[str, Any], **kwargs) -> str:
        """
        Call the language model with a formatted prompt.

        Args:
            prompt_params (Dict[str, Any]): A dictionary containing parameters
                                            to format the prompt.
            **kwargs: Additional keyword arguments to pass to the underlying
                      _call method.

        Returns:
            str: The response from the language model.
        """
        # Form the prompt using the provided parameters
        formatted_prompt = self.prompt_template.format(**prompt_params)

        # Call the llm with the formatted prompt and return the result
        return super()._call(formatted_prompt, **kwargs)
