"""
feedback_agent.py  –  Generates structured feedback on student essays
using a quantised Mistral‑7B GGUF model via llama.cpp.

How to use:
    export LLAMA_MODEL_PATH=/absolute/path/to/mistral-7b-instruct-v0.2.Q4_K_M.gguf
    python feedback_agent.py
"""

import os
import json
from pathlib import Path
from functools import lru_cache
from typing import Dict
from dotenv import load_dotenv
load_dotenv()   

from llama_cpp import Llama

# ---------------------------------------------------------------------
# Configuration 
# ---------------------------------------------------------------------
DEFAULT_MODEL_PATH = os.getenv(
    "LLAMA_MODEL_PATH",
    "../agents/mistral-7b-instruct-v0.2.Q2_K.gguf"
)
N_THREADS      = int(os.getenv("LLAMA_THREADS", os.cpu_count() or 4))
N_GPU_LAYERS   = int(os.getenv("LLAMA_GPU_LAYERS", "0"))  # >0 on Apple‑Silicon
MAX_NEW_TOKENS = 400
TEMPERATURE    = 0.7
TOP_P          = 0.9
# ---------------------------------------------------------------------


@lru_cache(maxsize=1)
def _load_llm() -> Llama:
    """Load GGUF model once and memoise it."""
    model_path = Path(DEFAULT_MODEL_PATH).expanduser()
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Set LLAMA_MODEL_PATH env or download a GGUF file."
        )
    return Llama(
        model_path=str(model_path),
        n_threads=N_THREADS,
        n_gpu_layers=N_GPU_LAYERS,
        verbose=False
    )


def _build_prompt(essay: str) -> str:
    """Return the full system‑+‑user prompt."""
    return f"""
    You are an AI writing tutor. A student submitted the essay below.

    Tasks:
    1. Provide constructive feedback (clarity, structure, grammar, logic).
    2. Predict a letter grade (A–F).
    3. Suggest a concise, personalised next‑step plan for improvement.

    Essay:
    \"\"\"{essay.strip()}\"\"\"

    Respond **only** with valid JSON:
    {{
    "grade": "<letter>",
    "feedback": "<detailed feedback>",
    "action_plan": "<next steps>"
    }}
    """


def generate_feedback(essay_text: str) -> Dict[str, str]:
    """
    Generate feedback dict using the local LLM.

    Returns:
        {"grade": "...", "feedback": "...", "action_plan": "..."}
    """
    llm = _load_llm()
    prompt = _build_prompt(essay_text)

    raw = llm(
        prompt,
        max_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        stop=["```", "</s>"],
    )
    text = raw["choices"][0]["text"].strip()

    # Best‑effort JSON parse; fall back to raw string
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"grade": "N/A", "feedback": text, "action_plan": ""}


# ---------------------------------------------------------------------
# Demo / CLI test
# ---------------------------------------------------------------------
# if __name__ == "__main__":
#     sample_essay = (
#         "Technology has become an essential part of our lives. While it helps in many ways, "
#         "it also causes people to be distracted, spend too much time on their phones, and have "
#         "less real communication. Balancing the use of technology is important."
#     )
#     result = generate_feedback(sample_essay)
#     print(json.dumps(result, indent=2))
