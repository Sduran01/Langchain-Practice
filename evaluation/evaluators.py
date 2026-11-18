"""Evaluators for the dispatch agent.

Each evaluator uses the LangSmith signature
    (inputs, outputs, reference_outputs) -> dict

- inputs:            {"question": ...}                        (dataset example)
- outputs:           {"answer": ..., "tool_calls": [...]}     (from eval.target)
- reference_outputs: {"expected_tool_calls": [...], "expected_facts": {...}}
"""
import json

import config  # Load environment variables
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

JUDGE_MODEL = "openai:gpt-4o-mini"


def _to_json(value) -> str:
    return json.dumps(value, indent=2)


# ---------------------------------------------------------------------------
# 1. Correctness of the final answer (LLM as a judge)
# ---------------------------------------------------------------------------

_correctness_judge = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    feedback_key="correctness",
    model=JUDGE_MODEL,
)


def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """LLM judge: is the final answer factually correct and complete?"""
    # The built-in CORRECTNESS_PROMPT fills {inputs}, {outputs} and
    # {reference_outputs}, so pass the values under those names.
    return _correctness_judge(
        inputs=inputs["question"],
        outputs=outputs["answer"],
        reference_outputs=_to_json(reference_outputs["expected_facts"]),
    )


# ---------------------------------------------------------------------------
# 2. Tool efficiency (LLM as a judge)
# ---------------------------------------------------------------------------
TOOL_EFFICIENCY_PROMPT = """You are grading how efficiently a trucking dispatch assistant used its tools.

Available tools (all are read-only lookups):
- get_driver_availability(driver_id): availability ("busy"/"available") AND the active load IDs
- get_driver_active_loads(driver_id): full details of the driver's active loads
- get_driver_location(driver_id): driver's current location
- get_driver_equipment(driver_id): truck (incl. max cargo payload) and trailer (type, number, length)
- get_load_details(load_id): load status, route, weight, trailer requirement, assigned driver

<question>
{question}
</question>

<tool_calls_made>
{tool_calls}
</tool_calls_made>

<reference_tool_calls>
{expected_tool_calls}
</reference_tool_calls>

The reference is a guide to a reasonable set of calls, not the only acceptable one.
Judge whether the calls made were the minimum needed to answer the question:
- Penalize duplicate calls (same tool with the same arguments).
- Penalize calls whose results are not needed for this question.
- Penalize wrong arguments (e.g. the wrong driver_id) that forced extra calls.
- Do NOT penalize a call that is needed but missing from the reference, and do NOT
  penalize using fewer calls than the reference if the question can still be answered.

Score:
- 1.0: no unnecessary, duplicate or wasted calls
- 0.5: mostly efficient, with one unnecessary or duplicate call
- 0.0: several unnecessary calls, or clearly wasteful tool usage
"""

_tool_efficiency_judge = create_llm_as_judge(
    prompt=TOOL_EFFICIENCY_PROMPT,
    feedback_key="tool_efficiency",
    model=JUDGE_MODEL,
    choices=[0.0, 0.5, 1.0],
)


def tool_efficiency(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """LLM judge: did the agent avoid unnecessary or duplicate tool calls?"""
    return _tool_efficiency_judge(
        question=inputs["question"],
        tool_calls=_to_json(outputs["tool_calls"]),
        expected_tool_calls=_to_json(reference_outputs["expected_tool_calls"]),
    )


# ---------------------------------------------------------------------------
# 3. Required tool calls were made (deterministic check)
# ---------------------------------------------------------------------------
def required_tool_calls(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """Every expected tool call (same name AND same args) must appear in the
    agent's tool calls. Order does not matter and extra calls are allowed
    (extra calls are scored by tool_efficiency instead).
    """
    made = outputs["tool_calls"]
    missing = [
        expected
        for expected in reference_outputs["expected_tool_calls"]
        if expected not in made
    ]

    if missing:
        comment = "Missing required tool calls: " + _to_json(missing)
    else:
        comment = "All required tool calls were made."

    return {
        "key": "required_tool_calls",
        "score": not missing,
        "comment": comment,
    }


# ---------------------------------------------------------------------------
# 4. Tool arguments are correct (deterministic check)
# ---------------------------------------------------------------------------
def tool_arguments(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """Every tool call the agent made must use arguments that appear in the
    expected tool calls, e.g. driver_id 2 for a question about Carlos.

    This checks extra calls too: if the agent also calls
    get_driver_availability(driver_id=2) for a Carlos question, the arguments
    are correct even though that tool isn't in the reference.
    Score = fraction of the agent's tool calls with correct arguments.
    """
    made = outputs["tool_calls"]
    if not made:
        return {
            "key": "tool_arguments",
            "score": 0.0,
            "comment": "The agent made no tool calls.",
        }

    allowed_args = [call["args"] for call in reference_outputs["expected_tool_calls"]]
    wrong = [call for call in made if call["args"] not in allowed_args]

    if wrong:
        comment = (
            "Tool calls with wrong arguments: " + _to_json(wrong)
            + "\nExpected arguments: " + _to_json(allowed_args)
        )
    else:
        comment = "All tool calls used correct arguments."

    return {
        "key": "tool_arguments",
        "score": (len(made) - len(wrong)) / len(made),
        "comment": comment,
    }


evaluators = [correctness, tool_efficiency, required_tool_calls, tool_arguments]
