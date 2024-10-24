# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_consultingassistants import ChatConsultingAssistants

# langchain import
from app.utilities.request_utilities import api_wrapper


def add_custom_routes(app: FastAPI):
    @app.get("/joke/invoke")
    @app.post("/joke/invoke")
    async def joke_orig(request: Request):
        # this is for backwards compatibility
        # call the original
        return await joke(request)

    @app.get("/experience/joke/retrievers/get_joke/invoke")
    @app.post("/experience/joke/retrievers/get_joke/invoke")
    async def joke(request: Request):
        async def get_joke_response(data):
            # get the query
            topic = data

            # get the model and prompt
            model = ChatConsultingAssistants(model="Granite 13B V2.1")
            prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

            # execute the search
            llm_chain = LLMChain(llm=model, prompt=prompt)
            formatted_result = llm_chain.run(topic=topic)

            # return the result
            return [{"message": formatted_result, "type": "text"}]

        # execute the joke
        return await api_wrapper(get_joke_response, request)
