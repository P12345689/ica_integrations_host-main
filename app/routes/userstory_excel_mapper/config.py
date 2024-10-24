
import os

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME: str = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")

API_KEY = os.environ.get("ICA_AUTH_TOKENS", "dev-only-token")

# Public directory for XLSX files
PUBLIC_DIR: str = "public/xlsx_builder"

# Number of requirements allowed in the input
MAX_REQUIREMENTS = 10

CONFIG_FILE_PATH = "app/routes/userstory_excel_mapper/config.json"

TEMPLATE_DIR: str = "app/routes/userstory_excel_mapper/templates"