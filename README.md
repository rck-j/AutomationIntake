# AutomationIntake

This project is to create a web application for intaking automation projects. The intake application developed in python will allow users to input a process, clarify the process with assistance from chatgpt, then create mermaid.js diagram of the process, provide a markdown document of the high level process, then provide an analysis of what steps can be taken to automate the process.

## Getting started

1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the intake UI in debug mode.

```bash
flask --app app.main run --debug
```

The current UI provides a conversation-style intake experience. You can describe a process, answer clarifying questions from the assistant, and receive a lightweight automation assessment once enough detail has been collected.