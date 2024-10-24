# -*- coding: utf-8 -*-
import json

from fastapi import FastAPI, Request
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
# langchain import
from langchain_consultingassistants import ChatConsultingAssistants


def add_custom_routes(app: FastAPI):
    @app.post("/summarize_text/invoke")
    async def summarize_text(request: Request):
        # get the model and prompt
        model = ChatConsultingAssistants(model="Granite 13B V2.1")

        # TODO: In the future, pull this from our prompt library
        prompt = ChatPromptTemplate.from_template(
            "Summarize in {number} {summary_type} in a {style} style from the following text: {text}"
        )

        # get the data
        try:
            data = await request.body()
            input_data = json.loads(data.decode("utf-8"), strict=False)
            input = input_data["input"]
            text = input["text"]
            number = input["number"]
            style = input["style"]
            summary_type = input["summary_type"]

            # execute the search
            llm_chain = LLMChain(llm=model, prompt=prompt)
            formatted_result = llm_chain.run(text=text, number=number, style=style, summary_type=summary_type)

        except Exception:
            # handle any other unexpected errors
            formatted_result = "I'm sorry but i couldn't find a response, please try with a different query"

        # return the result
        response = {
            "status": "success",
            "invocationId": "",
            "response": [{"message": formatted_result, "type": "text"}],
        }

        return response
