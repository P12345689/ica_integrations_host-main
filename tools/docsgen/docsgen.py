#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: docsgen CLI tool for generating markdown documentation from README.md files

This module provides a command-line interface for generating markdown documentation for integrations
from README.md files using a choice of LLMs and Jinja templates. It also creates a .pages file for MkDocs navigation.
"""

import argparse
import glob
import logging
import os
from typing import List, Union

from langchain_openai import AzureChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms.watsonxllm import WatsonxLLM
from langchain_consultingassistants import ChatConsultingAssistants

from jinja2 import Template
from config import get_model

# Define a Union type if you expect different types of models to be used.
ModelType = Union[AzureChatOpenAI, ChatOpenAI, WatsonxLLM, ChatConsultingAssistants]

# Setup logging
debug_mode = os.getenv('DEBUG') == '1'
logging_level = logging.DEBUG if debug_mode else logging.INFO
logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Default values for templates
DEFAULT_MD_TEMPLATE: str = "templates/md_template.jinja"
DEFAULT_PAGES_TEMPLATE: str = "templates/pages_template.jinja"

def process_readme(content: str, template: Template, model: ModelType, dry_run: bool = False, verbose: bool = False) -> str:
    """Process README content using a Jinja template and potentially enhance it with LLM."""
    rendered_template: str = template.render(content=content)

    if verbose:
        log.debug(f"Rendered template:\n{rendered_template}")

    if dry_run:
        log.debug("Dry run active, returning rendered template without invoking model.")
        return rendered_template
    else:
        messages = [
            ("system", "You are a helpful assistant that enhances documentation."),
            ("human", rendered_template)
        ]
        try:
            response = model.invoke(messages)
            content = response.content if hasattr(response, 'content') else "No content"
            log.debug(f"Model response:\n{content}")
            return content
        except Exception as e:
            log.error(f"Error invoking model: {e}")
            raise

def generate_pages_content(directories: List[str], template: Template, model: ModelType, dry_run: bool = False, verbose: bool = False) -> str:
    """Generate .pages file content using a Jinja template and potentially enhance it with LLM."""
    rendered_template: str = template.render(directories=directories)

    if verbose:
        log.debug(f"Rendered .pages template:\n{rendered_template}")

    if dry_run:
        log.debug("Dry run active, returning rendered template without invoking model.")
        return rendered_template
    else:
        messages = [
            ("system", "You are a helpful assistant that generates navigation for documentation."),
            ("human", rendered_template)
        ]
        try:
            response = model.invoke(messages)
            content = response.content if hasattr(response, 'content') else "No content"
            log.debug(f"Model response for .pages:\n{content}")
            return content
        except Exception as e:
            log.error(f"Error invoking model for .pages content: {e}")
            raise

def docsgen(
    directories: List[str],
    output_dir: str,
    md_template: str = DEFAULT_MD_TEMPLATE,
    pages_template: str = DEFAULT_PAGES_TEMPLATE,
    dry_run: bool = False,
    verbose: bool = False
) -> None:
    """Main function to generate documentation from README files."""
    model = get_model()
    log.info("Model initialized.")

    with open(md_template, 'r') as f:
        md_template_content = Template(f.read())
    with open(pages_template, 'r') as f:
        pages_template_content = Template(f.read())

    processed_dirs: List[str] = []

    for pattern in directories:
        for dir_path in glob.glob(pattern):
            readme_path = os.path.join(dir_path, 'README.md')
            if os.path.exists(readme_path):
                log.info(f"Processing file: {readme_path}")
                with open(readme_path, 'r') as f:
                    content = f.read()

                if verbose:
                    log.debug(f"Preview of README content: {content[:500]}...")

                processed_content = process_readme(content, md_template_content, model, dry_run=dry_run, verbose=verbose)

                if not dry_run:
                    output_file = os.path.join(output_dir, f"{os.path.basename(dir_path)}.md")
                    with open(output_file, 'w') as f:
                        f.write(processed_content)
                    log.info(f"Processed {readme_path} -> {output_file}")
                else:
                    log.debug(f"Dry run completed for {readme_path}")

                processed_dirs.append(os.path.basename(dir_path))
            else:
                log.warning(f"README.md not found in {dir_path}")

    log.info("Generating .pages file")
    pages_content = generate_pages_content(processed_dirs, pages_template_content, model, dry_run=dry_run, verbose=verbose)
    if not dry_run:
        pages_file = os.path.join(output_dir, '.pages')
        with open(pages_file, 'w') as f:
            f.write(pages_content)
        log.info(f"Generated .pages file at {pages_file}")
    else:
        log.debug("Dry run completed for .pages file generation")

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate markdown documentation from README.md files.")
    parser.add_argument('directories', nargs='+', help="Directories or glob patterns containing README.md files")
    parser.add_argument('-o', '--output', required=True, help="Output directory for generated files")
    parser.add_argument('--md-template', default=DEFAULT_MD_TEMPLATE, help="Path to the Jinja template for markdown generation")
    parser.add_argument('--pages-template', default=DEFAULT_PAGES_TEMPLATE, help="Path to the Jinja template for .pages generation")
    parser.add_argument('--dry-run', action='store_true', help="If set, only display the prompts without generating any files")
    parser.add_argument('--verbose', action='store_true', help="If set, display detailed logging information")

    args = parser.parse_args()

    if not args.dry_run:
        os.makedirs(args.output, exist_ok=True)
        log.info(f"Output directory {args.output} created or already exists.")

    docsgen(args.directories, args.output, args.md_template, args.pages_template, dry_run=args.dry_run, verbose=args.verbose)

if __name__ == "__main__":
    main()
