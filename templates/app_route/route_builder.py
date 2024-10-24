# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Route builder
"""

import argparse
import logging
import os
import re
import shutil
from tempfile import TemporaryDirectory

from cookiecutter.main import cookiecutter

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

welcome_message = """
Welcome to the IBM Consulting Assistants Integration Builder

🔨 This tool helps you forge new integrations!

For more information, see Developing Integrations: 🧑‍💻
https://pages.github.ibm.com/destiny/consulting_assistants_api/develop/developing_integrations/

Remember to use the naming convention: my_route

All new routes are copied to dev/routes instead of app/route. Once they are ready and pass unit testing,
the process to move them to app/routes can start (includes an architecture and code review).

Remember to start the server with ICA_DEV_ROUTES=1 to enable development routes.
"""


def validate_name(module_name):
    # Validates the module name to contain only alphanumeric characters and underscores
    return re.match(r"^[a-zA-Z0-9_]+$", module_name) is not None


def generate_and_copy_module(template_path, destination_path):
    print(welcome_message)
    logging.info("Starting module generation process...")

    with TemporaryDirectory() as tmp_dir:
        # Generate the module with user input into the temporary directory
        module_path = cookiecutter(template_path, output_dir=tmp_dir)
        module_name = os.path.basename(module_path)

        # Checks if the module name is valid
        if not validate_name(module_name):
            logging.error(
                "Invalid module name. The module name should contain only alphanumeric characters and underscores."
            )
            return

        full_destination_path = os.path.join(destination_path, module_name)

        # Check if the destination path already contains a directory with the same module name
        if os.path.exists(full_destination_path):
            logging.error(f"Module '{module_name}' already exists at {destination_path}.")
            return

        # Copy the generated module to the destination
        try:
            shutil.copytree(module_path, full_destination_path)
            logging.info(f"Module '{module_name}' successfully copied to {destination_path}.")
        except Exception as e:
            logging.error(f"Failed to copy module to {destination_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate and deploy a module from a cookiecutter template.")
    parser.add_argument(
        "--template_path",
        type=str,
        help="Path to the cookiecutter template",
        default="templates/app_route",
    )
    parser.add_argument(
        "--destination_path",
        type=str,
        help="Destination path where the module should be copied",
        default="dev/app/routes/",
    )
    args = parser.parse_args()

    generate_and_copy_module(args.template_path, args.destination_path)


if __name__ == "__main__":
    main()
