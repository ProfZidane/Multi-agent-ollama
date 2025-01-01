from langchain_ollama import ChatOllama


llm = ChatOllama(model="mistral")

system_prompt = (
    "Your task is to answer the user's question. "
)

test_messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the square root of 42?"},
]

response = llm.invoke(test_messages)
print("Test superviseur :", response)


