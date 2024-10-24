# -*- coding: utf-8 -*-
"""
Authors: Mihai Criveti
Description: Configuration module for wikipedia integration
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    # Wikipedia API configuration
    wiki_api_url: str = "https://en.wikipedia.org/w/api.php"
    wiki_page_url: str = "https://en.wikipedia.org/wiki/"

    # libica config
    ica_model_id: str = "Llama3.1 70b Instruct"
    search_llm_prompt: str = "Compile the following search results into a detailed response, outputting markdown.\n\n"
    legal_notice: str = f"NOTICE: this content was summarized using a large language model: {ica_model_id}"

    class Config:
        env_file = ".icasearch.env"
        env_file_encoding = "utf-8"


settings = Settings()
