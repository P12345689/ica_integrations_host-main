# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request

# langchain import


def add_custom_routes(app: FastAPI):
    @app.post("/geministt/invoke")
    async def geministt(request: Request):
        # # get the model and prompt
        # model = ChatConsultingAssistants(model="Granite 13B V2.1")
        # prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

        # # get the data
        # data = await request.json()
        # topic = data["input"]

        # # execute the search
        # llm_chain = LLMChain(llm=model, prompt=prompt)
        # formatted_result = llm_chain.run(topic=topic)

        # return the result
        response = {
            "status": "success",
            "invocationId": "",
            "response": [{"message": "Not implemented", "type": "text"}],  # formatted_result,
        }

        return response
