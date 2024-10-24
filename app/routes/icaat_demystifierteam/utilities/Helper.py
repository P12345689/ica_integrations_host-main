# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, Santhana Krishnan, Thomas Chang, Kasra Amirtahmasebi
Description: Autogen Integration for code spliting
"""

import os
import time
from autogen import config_list_from_json
from typing import Optional
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FOLDER = os.path.join(BASE_DIR, "../config")

class ConfigUtility:
    cache = dict()
    def __init__(self, file_location: Optional[str] = CONFIG_FOLDER):
        self.file_location = file_location

    def get_agent_config(self, agent_name, env_or_file="AGENT_CONFIG"):
        #AGENT_CONFIG_LIST
        config_list = config_list_from_json(
                env_or_file=env_or_file,
                file_location=self.file_location,
                filter_dict={"agent_name": {str(agent_name)}},
            )
        logger.debug(f"AGENT_CONFIG of  router {agent_name} :  {config_list} ")
        return config_list

    def get_skills_list(self, env_or_file):
        skills_list = config_list_from_json(
            env_or_file=env_or_file,
            file_location=self.file_location
        )
        return skills_list


    def get_index_name(self, apikey, env_or_file="INDEXNAME_APIKEY_MAP"):
        config_list = config_list_from_json(
                env_or_file=env_or_file,
                file_location=self.file_location,)
        
        for dict_data in config_list:
            index_name=dict_data["index_name"]
            knowledge_base_url=dict_data["knowledge_base_url"]
            apikeys=dict_data["apikeys"]
            for temp_apikey in apikeys:
                if(temp_apikey==apikey):
                    logger.info(f" apikey: {apikey} ; index_name : {index_name}")
                    return index_name,knowledge_base_url
                
        logger.info(f" apikey : {apikey} : index_name not mapped in configuration file {env_or_file} ")
        return None
    