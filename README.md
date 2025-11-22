# AutomationIntake

This project is a web application for intaking automation ideas. The application, developed in Python using Flask, allows users to describe a process they'd like to automate. It then uses Google's Gemini API to ask clarifying questions and provide an initial automation assessment.

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

3. Set up your environment variables.

Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

4. Run the intake UI in debug mode.

```bash
flask --app app.main run --debug
```

The UI provides a conversation-style intake experience. You can describe a process, answer clarifying questions from the assistant, and receive a lightweight automation assessment once enough detail has been collected.