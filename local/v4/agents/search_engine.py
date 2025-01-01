from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from tools.search import search_eng
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Literal
from langchain_experimental.llms.ollama_functions import OllamaFunctions



tavily_tool = search_eng()
llm = ChatOllama(model="mistral")

research_agent = create_react_agent(
    llm, tools=[tavily_tool], state_modifier="You are a researcher. DO NOT do any math."
)

def research_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    result = research_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="researcher")
            ]
        },
        goto="supervisor",
    )