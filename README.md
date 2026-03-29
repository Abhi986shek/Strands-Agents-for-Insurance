# Generic Auto Insurance AI Framework

A fully modular, mock customer support agent for Auto Insurance built with the **Strands SDK** — a state-of-the-art framework for designing AI support agents powered by Claude 3.5 Sonnet. This repository showcases an end-to-end framework where external logic (e.g. quote generation, validation) has been mocked out to provide a seamless boilerplate for anyone building industry-specific chatbots.

## What is Strands?
Strands is a modern conceptual AI Agent framework designed to replace older, clunky configuration consoles. It offers:

- **Code-First Approach**: All agent instructions, state definitions, and LLM constraints are written natively in Python.
- **Direct Tool Calling**: Developers can simply decorate Python functions as `@tool` to expose specific business logic directly to the LLM context.
- **Continuous Async Operations**: Built-in async streaming capabilities allow rapid user-bot dialogue.
- **Superior Developer Experience**: Eradicates the necessity for manual mapping on web consoles.

---

## Technical Features Implemented
- **Automated Workflow Execution**: Enforces a strict, step-by-step pipeline ensuring users verify before moving to the next stage.
- **Mock OTP Verification**: Sample tool design demonstrating identity validation prior to accessing data structures.
- **Policy Tier Engine**: Configurable tiered product listing (Basic Cover, Standard Protection, Premium Shield).
- **Add-On Customization Logic**: Plug-and-play structure for insurance riders like 'Roadside Assistance' or 'Zero Depreciation'.
- **End-to-end Journey**: From initial greeting -> code verification -> quote drafting -> generating mock checkout URLs.
- **Global Config & Context Management**: Stores session references so the bot retains knowledge over extended conversations.

---

## Directory Schema

```
STRANDS-AGENTS-FOR-INSURANCE/
├── insurance_bot/
│   ├── tools/
│   │   ├── __init__.py           # Exposes all tool modules to agent.py
│   │   ├── auth_tools.py         # OTP & user phone number validation
│   │   ├── vehicle_tools.py      # License plate and auto details fetch
│   │   ├── quote_tools.py        # Tier pricing logic and add-on costs
│   │   ├── payment_tools.py      # Policy drafting and checkout URLs
│   │   └── faq_tools.py          # General informational searches
│   ├── agent.py                  # Core LLM prompt and rule definitions
│   ├── app.py                    # REST API Entry Point (Flask)
│   ├── config.py                 # Global environment placeholders
│   ├── routes.py                 # Flask web endpoints configuration
│   └── utils.py                  # Base64 and payload parsers
├── README.md                     # You're reading it
└── requirements.txt              # Dependency specifications
```

---

## Getting Started

### 1. Requirements
- Python 3.9+
- Activated virtual environment for dependency isolation.

### 2. Installations
Run the PIP package installer to pull dependencies such as `flask`, `flask_cors`, and `strands`.
```bash
pip install -r requirements.txt
```

### 3. Execution
Launch the application module internally to spin up a listening web server locally on port 5000:
```bash
python -m insurance_bot.app
```

---

## Extending the Agent
To add new functionalities to the agent:
1. Navigate to `insurance_bot/tools/`.
2. Create your module (e.g. `cancellation_tools.py`).
3. Define native functions wrapped by `@tool`.
4. Import your new tool in `insurance_bot/tools/__init__.py`.
5. Inject the function directly into the `tools` array located inside `create_agent` at `insurance_bot/agent.py`.
6. Add new constraints or steps into the system instructions if necessary to dictate when the LLM should invoke it.

> Note: This provides absolute control over response bounds and reduces LLM hallucination when fetching arbitrary data!

## Contributing & Licensing
This repository is configured as generic portfolio architecture. Contributions to refine the mock layers or add additional example tools are welcome.
