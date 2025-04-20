from pathlib import Path

# Define base project path
base_path = Path("./auto_feedback_agent")

# Folder structure
folders = [
    "app",
    "agents",
    "prompts",
    "data",
    "utils",
    "notebooks"
]

# Files to create with basic content
files = {
    "README.md": "# Auto-Feedback Engine for Students Using AI Agents\n",
    "requirements.txt": "openai\nlangchain\nstreamlit\nflask\njinja2\ntiktoken\npandas\nscikit-learn\n",
    "app/main.py": "# Streamlit or Gradio app goes here\n",
    "agents/feedback_agent.py": "# Feedback agent logic goes here\n",
    "agents/rubric_grader.py": "# Optional rubric grading logic\n",
    "prompts/feedback_template.txt": "You are an AI tutor. Evaluate the student's essay and return feedback.\n",
    "prompts/grading_rubric.md": "## Grading Rubric\n- Clarity\n- Structure\n- Grammar\n- Relevance\n",
    "data/sample_essay_1.txt": "This is a sample essay.\n",
    "data/sample_essay_2.txt": "Another example essay.\n",
    "utils/preprocess.py": "# Text preprocessing utils\n",
    "utils/metrics.py": "# Scoring and evaluation utilities\n",
    "notebooks/prompt_experiments.ipynb": ""
}

# Create folders
for folder in folders:
    (base_path / folder).mkdir(parents=True, exist_ok=True)

# Create files
for relative_path, content in files.items():
    file_path = base_path / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)


