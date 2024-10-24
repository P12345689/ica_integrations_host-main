# -*- coding: utf-8 -*-
"""libica - IBM Consulting Assistants - Extensions API Library."""

__author__ = "Mihai Criveti"
__copyright__ = "Copyright 2024, Mihai Criveti"
__license__ = "MIT"
__version__ = "0.8.0"
__date__ = "2024-04-01"
__email__ = "crmihai1@ie.ibm.com"
__status__ = "Alpha"
__description__ = "IBM Consulting Assistants - Extensions API Library"
__url__ = "https://github.ibm.com/destiny/consulting_assistants_api"
__download_url__ = "https://github.ibm.com/destiny/consulting_assistants_api"
__packages__ = ["libica"]

import logging
import sys

from aimodels.bam import BAMClient
from libica.ica_catalog import ICACatalog
from libica.ica_client import ICAClient
from libica.ica_error import ICAClientError
from libica.ica_settings import Settings

# Setup logging
# """
# Usage in every python file:
#   >>> import logging
#   >>> log = logging.getLogger(__name__)
#   >>> log.info("Hello")
# """
logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(name)s:%(funcName)s(%(lineno)d) -- %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    stream=sys.stderr,
    level=logging.INFO,
)
# TODO: make this a configurable thing via ENV, etc.
# import logging.config
# logging.config.fileConfig('logging.conf')
# Should automatically split debug logs to a separate file
# And always print to both file (separate logs) and stdout + stderr combined
# Don't default to write to file to make it container friendly

__all__ = ["ICAClient", "Settings", "ICAClientError", "ICACatalog", "BAMClient"]
