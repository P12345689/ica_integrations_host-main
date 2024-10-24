import autogen
import os
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

os.environ["AUTOGEN_USE_DOCKER"] = "False"
os.environ["TOKENIZERS_PARALLELISM"] = "False"


class DemystifierTeam:
    DEMYSTIFIER_SYSTEM_MESSAGE = """You are a helpful AI assistant. Solve tasks using your coding and language skills 
                        demystifying and documenting code and pseudocode for a project. Your documentation will be forwarded 
                        and reviewed by DocReviewer. In case your documentation is incomplete and needs to be fixed, you 
                        will receive feedback from DocReviewer. You will need to update documentation based on that feedback. 
                        Maybe this process of rewriting the documentation will happen a few times until the DocReviewer can't 
                        find any more issues. Never say "TERMINATE"
                        """
    DOCREVIEWER_SYSTEM_MESSAGE = """You are a helpful AI reviewer assistant. After the Demystifier documents code or
                        pseudocode, it  is passed to you. Your primary role is to ensure the documentation quality and 
                        correctness. You are responsible for documentation review and writing feedback report on what needs 
                        to be rewritten. Don't fix or rewrite the documentation yourself, just provide the feedback report 
                        back to the Demystifier. Iterate until Demystifier writes documentation that doesn't have issues. 
                        You decide that the documentation is successful or not.  Once the documentation is perfect forward 
                        it to DocOptimizer. Never say "TERMINATE"
                        """

    DOCOPTIMIZER_SYSTEM_MESSAGE = """You will receive code documentation from the DocReviewer agent, but in case the 
                        documentation needs to be updated, you send the feedback to the Demystifier. You decide when the documentation is 
                        good enough and can't be optimized further. Don't ask anyone for permission, just proceed with your actions. 
                        Once you decide that the documentation is good enough, output the final documentation in a format that is easy for a human to review, 
                        and then forward the final documentation to the chat manager and say "TERMINATE"
                        """

    DEFAULT_DEMYSTIFIER_TEMPERATURE = 0.2
    DEFAULT_DOCREVIEWER_TEMPERATURE = 0.8
    DEFAULT_DOCOPTIMIZER_TEMPERATURE = 0.6

    DEFAULT_TIMEOUT = 180
    DEFAULT_MAX_ROUND = 10
    DEFAULT_MAXTOKENS = 3000

    def execute(
        self,
        config_list,
        user_prompt,
        demystifier_config_list: Optional[Any] = None,
        docreviewer_config_list: Optional[Any] = None,
        docoptimizer_config_list: Optional[Any] = None,
        demystifier_temperature: Optional[float] = DEFAULT_DEMYSTIFIER_TEMPERATURE,
        docreviewer_temperature: Optional[float] = DEFAULT_DOCREVIEWER_TEMPERATURE,
        docoptimizer_temperature: Optional[float] = DEFAULT_DOCOPTIMIZER_TEMPERATURE,
        max_tokens: Optional[int] = None,
        max_round: Optional[int] = None,
        system_message: Optional[dict] = None,
    ):
        self.config_list = config_list
        self.user_prompt=user_prompt
        self.demystifier_config_list = demystifier_config_list or config_list
        self.docreviewer_config_list = docreviewer_config_list or config_list
        self.docoptimizer_config_list = docoptimizer_config_list or config_list

        self.demystifier_temperature = demystifier_temperature
        self.docreviewer_temperature = docreviewer_temperature
        self.docoptimizer_temperature = docoptimizer_temperature

        #set system message, fallback to default
        if system_message is not None:
            if system_message['DEMYSTIFIER_SYSTEM_MESSAGE'] is not None:
                self.DEMYSTIFIER_SYSTEM_MESSAGE = system_message['DEMYSTIFIER_SYSTEM_MESSAGE'].strip()
            logger.info(f"DEMYSTIFIER_SYSTEM_MESSAGE is set to {self.DEMYSTIFIER_SYSTEM_MESSAGE}")
            
            if system_message['DOCREVIEWER_SYSTEM_MESSAGE'] is not None:
                self.DOCREVIEWER_SYSTEM_MESSAGE = system_message['DOCREVIEWER_SYSTEM_MESSAGE'].strip()
            logger.info(f"DOCREVIEWER_SYSTEM_MESSAGE is set to {self.DOCREVIEWER_SYSTEM_MESSAGE}")

            if system_message['DOCOPTIMIZER_SYSTEM_MESSAGE'] is not None:
                self.DOCOPTIMIZER_SYSTEM_MESSAGE = system_message['DOCOPTIMIZER_SYSTEM_MESSAGE'].strip()
            logger.info(f"DOCOPTIMIZER_SYSTEM_MESSAGE is set to {self.DOCOPTIMIZER_SYSTEM_MESSAGE}")



        Demystifier = autogen.AssistantAgent(
            name="demystifier",
            llm_config={
                "config_list": self.demystifier_config_list,
                "cache_seed": False,  # change the cache_seed for different trials
                "temperature": demystifier_temperature or self.demystifier_temperature,
                "timeout": self.DEFAULT_TIMEOUT,
                "max_tokens": max_tokens or self.DEFAULT_MAXTOKENS,
            },
            system_message=self.DEMYSTIFIER_SYSTEM_MESSAGE,
            human_input_mode="NEVER",
        )
        logger.debug(
            f"{Demystifier.name} system_message is {Demystifier.system_message} "
        )

        DocReviewer = autogen.AssistantAgent(
            name="DocReviewer",
            llm_config={
                "config_list": self.docreviewer_config_list,
                "cache_seed": False,  # change the cache_seed for different trials
                "temperature": self.docreviewer_temperature,
                "timeout": self.DEFAULT_TIMEOUT,
            },
            system_message=self.DOCREVIEWER_SYSTEM_MESSAGE,
            human_input_mode="NEVER",
        )
        logger.debug(
            f"{DocReviewer.name} system_message is {DocReviewer.system_message} "
        )

        DocOptimizer = autogen.AssistantAgent(
            name="DocOptimizer",
            llm_config={
                "config_list": self.docoptimizer_config_list,
                "cache_seed": False,  # change the cache_seed for different trials
                "temperature": self.docoptimizer_temperature,
                "timeout": self.DEFAULT_TIMEOUT,
            },
            system_message=self.DOCOPTIMIZER_SYSTEM_MESSAGE,
            human_input_mode="NEVER",
        )
        logger.debug(
            f"{DocOptimizer.name} system_message is {DocOptimizer.system_message} "
        )

        groupchat = autogen.GroupChat(
            agents=[Demystifier, DocReviewer, DocOptimizer],
            messages=[],
            max_round=max_round or self.DEFAULT_MAX_ROUND,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": self.config_list},
        )

        initializer = autogen.UserProxyAgent(
            name="Initializer",
            code_execution_config=False,
        )

        chat_result = initializer.initiate_chat(manager, message=self.user_prompt)

        return groupchat.messages
