from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. Define the state of our agent system
class AgentState(TypedDict):
    task: str
    draft: str
    critique: str
    iterations: int

# 2. The Worker: Generates the initial output
def research_agent(state: AgentState):
    print("---RESEARCHER WORKING---")
    return {"draft": f"Fact-checked info about {state['task']}", "iterations": state.get("iterations", 0) + 1}

# 3. The Critic: Checks for hallucinations or errors
def reviewer_agent(state: AgentState):
    print("---REVIEWER CHECKING---")
    if "Fact-checked" in state["draft"] and state["iterations"] > 1:
        return {"critique": "PASSED"}
    return {"critique": "REJECTED: Needs more detail."}

# 4. Logic to decide: Finish or Loop back?
def should_continue(state: AgentState):
    if state["critique"] == "PASSED":
        return END
    return "researcher"

# 5. Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher", research_agent)
workflow.add_node("reviewer", reviewer_agent)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "reviewer")
workflow.add_conditional_edges("reviewer", should_continue)

app = workflow.compile()