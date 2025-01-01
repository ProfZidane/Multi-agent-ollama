from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState
from langgraph.types import Command
from langchain_ollama import ChatOllama
from langgraph.graph import END
from langchain_experimental.llms.ollama_functions import OllamaFunctions

from pydantic import BaseModel

members = ["researcher", "analyst"]
options = members + ["FINISH"]

# system_prompt = (
#     "You are a supervisor tasked with managing a conversation between the"
#     f" following workers: {members}. Given the following user request,"
#     " respond with the worker to act next. Each worker will perform a"
#     " task and respond with their results and status. When finished,"
#     " respond with FINISH."
# )

system_prompt = (
    "You are a supervisor responsible for assigning tasks to workers. "
    f"The workers are: {members}. "
    "Your task is to read the user's request and decide which worker should handle it. "
    "Provide one of the following responses: "
    "- 'researcher' if the task requires looking up information or performing a search. "
    "- 'analyst' if the task requires solving problems or providing explanations. "
    "When all tasks are complete, respond with 'FINISH'. "
    "Here are examples of tasks and the appropriate responses:"
    "\n1. User request: 'Find information about climate change.' -> Response: researcher."
    "\n2. User request: 'Explain how photosynthesis works.' -> Response: analyst."
    "\n3. User request: 'What's 2+2?' -> Response: analyst."
    "\n4. User request: 'Search for the latest news on AI.' -> Response: researcher."
)



class Router(BaseModel):
    next: Literal["researcher", "analyst", "FINISH"]

    


model = ChatOllama(model="mistral")


def supervisor_node(state: MessagesState) -> Command[Literal["researcher", "analyst", "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]    
    
    response = model.invoke(messages)
    
    if response is None:
        return Command(goto=END)  
    print("-----------------")
    print(response)    
    print("-----------------")

    content = response.content.lower()
    
    for member in members:
        if member in content:
            return Command(goto=member)
    if "FINISH" in content:
        return Command(goto=END)
    return Command(goto=END)  
    
    """ goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto) """


