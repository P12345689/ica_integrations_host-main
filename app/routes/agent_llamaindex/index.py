from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
resp = llm.complete("Who is Paul Graham?")
print(resp)