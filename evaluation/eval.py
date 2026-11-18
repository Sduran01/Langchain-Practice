from langsmith import Client
from dispatch_agent.agent import dispatch_agent

def target(inputs: dict) -> dict:
    agent = dispatch_agent()
    response = agent.invoke({"messages":inputs["question"]})
    print(f"target response: {response}")

    # Collect every tool call the agent made, in the same
    # {"name": ..., "args": ...} shape as expected_tool_calls in the dataset
    tool_calls = [
        {"name": tool_call["name"], "args": tool_call["args"]}
        for message in response["messages"]
        for tool_call in getattr(message, "tool_calls", None) or []
    ]

    return {
        "answer": response["messages"][-1].content,
        "tool_calls": tool_calls,
    }
if __name__ == '__main__':
    print(Client)
