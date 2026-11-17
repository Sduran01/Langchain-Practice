from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage
import inspect
from pprint import pprint
from langgraph.types import Command, interrupt
import config  # Load environment variables
from dispatch_agent.tools import tools

SYSTEM_PROMPT = """
You are the AI dispatch assistant for DA Transport.

Driver directory:
- John: ID 1
- Carlos: ID 2
- Mike: ID 3
- David: ID 4
- Jose: ID 5

Use the available tools to retrieve driver, load,
location, and equipment information.

Never invent driver availability, load status,
equipment specifications, or company information.

A driver is considered busy if they have at least
one load with status 'assigned' or 'in_transit'.

For equipment compatibility, verify the trailer
type and maximum cargo payload.

Do not assume that equipment compatibility guarantees
future availability or legal load feasibility.
"""


class State(TypedDict):
    messages: Annotated[list, add_messages]

def dispatch_agent():
    # 1. Initialize the model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 2. Bind our dispatch tools
    llm_with_tools = llm.bind_tools(tools)

    # 3. Define the agent node
    def agent_node(state: State):
        response = llm_with_tools.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                *state["messages"]
            ]
        )
        return {"messages": [response]}

    # 4. Build the graph
    builder_graph = StateGraph(State)

    builder_graph.add_node("agent", agent_node)
    builder_graph.add_node("tools", ToolNode(tools))

    # 5. Define graph edges
    builder_graph.add_edge(START, "agent")

    builder_graph.add_conditional_edges(
        "agent",
        tools_condition
    )

    builder_graph.add_edge("tools", "agent")

    # 6. Compile and return the graph
    return builder_graph.compile()

def main():
    agent = dispatch_agent()
    response = agent.invoke({"messages":"Is John available, and what active loads does he have?"})
    for message in response["messages"]:
        message.pretty_print()
if __name__ == '__main__':
    main()