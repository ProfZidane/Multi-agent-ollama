from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from tools.search import search_eng
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Literal
from langchain_experimental.llms.ollama_functions import OllamaFunctions


llm = ChatOllama(model="mistral")

def problem_solver_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    prompt = """
    You are a problem solver. Your task is to solve the following issue or perform the task described:
    {input}
    Provide a step-by-step solution or explanation for your answer.
    """
    input_text = state["messages"][-1].content
    messages = [{"role": "system", "content": prompt.format(input=input_text)}]
    
    response = llm.invoke(messages)
    
    return Command(
        update={
            "messages": [
                HumanMessage(content=response["messages"][-1].content, name="solver")
            ]
        },
        goto="supervisor",
    )
