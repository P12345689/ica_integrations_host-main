# -*- coding: utf-8 -*-
import json

from fastapi import FastAPI, Request
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
# langchain import
from langchain_consultingassistants import ChatConsultingAssistants


def add_custom_routes(app: FastAPI):
    @app.post("/instagram_post_ideas/invoke")
    async def instagram_post_ideas(request: Request):
        # get the model and prompt
        # model = ChatConsultingAssistants(model="Granite 13B V2.1")
        model = ChatConsultingAssistants(model="Llama3.1 70b Instruct")

        # TODO: In the future, pull this from our prompt library
        prompt = ChatPromptTemplate.from_template(
            "Write {number} Instagram post ideas that ask thought-provoking questions or engage in discussions with my target audience, encouraging meaningful interactions. Context: Target audience — {audience} What I do — {pitch} Engagement and discussions — {topics} Inspiration: {inspiration} Formatting guidelines: {guidelines})"
        )

        # get the data
        try:
            data = await request.body()
            input_data = json.loads(data.decode("utf-8"), strict=False)
            input = input_data["input"]
            pitch = input["pitch"]
            audience = input["audience"]
            number = input["number"]
            topics = input["topics"]
            inspiration = input["inspiration"]
            guidelines = input["guidelines"]

            # execute the search
            llm_chain = LLMChain(llm=model, prompt=prompt)
            formatted_result = llm_chain.run(
                pitch=pitch,
                audience=audience,
                number=number,
                topics=topics,
                inspiration=inspiration,
                guidelines=guidelines,
            )

        except Exception as e:
            # handle any other unexpected errors
            print(e)
            formatted_result = "I'm sorry but i couldn't find a response, please try with a different query"

        # return the result
        response = {
            "status": "success",
            "invocationId": "",
            "response": [{"message": formatted_result, "type": "text"}],
        }

        return response
