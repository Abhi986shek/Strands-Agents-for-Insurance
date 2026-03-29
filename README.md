# Insurance Bot Agent Framework

A modular, mock customer support agent for Auto Insurance built with Strands SDK - a code-first framework for building AI agents with Claude 3.5 Sonnet.

## What is Strands?
Strands is a modern SDK that offers:

- Code-first approach: Define agents, tools, and prompts in Python code
- Direct tool calls: Python functions decorated with @tool instead of action groups
- Streaming support: Built-in async streaming capabilities
- Better developer experience: No console configuration needed

## Features
- Complete motor insurance purchase journey illustration
- Authentication flow (Mock OTP verification)
- Vehicle registration validation simulation
- Dynamic quote generation with multiple tiers
- Add-on selection and customization options
- Secure payment link generation stub
- Session management

## Project Structure

```
STRANDS-AGENTS-FOR-INSURANCE/
├── insurance_bot/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── auth_tools.py
│   │   ├── vehicle_tools.py
│   │   ├── quote_tools.py
│   │   ├── payment_tools.py
│   │   └── faq_tools.py
│   ├── agent.py
│   ├── app.py
│   ├── config.py
│   ├── routes.py
│   ├── utils.py
│   └── app.log
├── README.md
└── requirements.txt
```

## Installation & Setup
### Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
### Run as module 
```bash
python -m insurance_bot.app
```
