# -*- coding: utf-8 -*-
from langchain_consultingassistants.chat import ChatConsultingAssistants
from langchain_consultingassistants.llms import ConsultingAssistantsLLM

from .chat import ChatConsultingAssistants
from .llms import ConsultingAssistantsLLM

__all__ = ["ConsultingAssistantsLLM", "ChatConsultingAssistants"]
