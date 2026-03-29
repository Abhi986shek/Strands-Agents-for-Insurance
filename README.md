# AutoGuard Strands Agent
A modular customer support agent for AutoGuard Insurance built with Strands SDK - a code-first framework for building AI agents with Claude 3.5 Sonnet.

## What is Strands?
Strands is a modern SDK that replaces Amazon Bedrock Agents, offering:

- Code-first approach: Define agents, tools, and prompts in Python code
- Direct tool calls: Python functions decorated with @tool instead of action groups
- Streaming support: Built-in async streaming capabilities
- Better developer experience: No console configuration needed

## Features
- Complete motor insurance purchase journey
- OTP verification and secure authentication
- Vehicle registration validation
- Dynamic quote generation with multiple plans
- Add-on selection and IDV customization
- Secure payment link generation
- Session management

Project Structure

```
AUTOGUARD STRANDS AGENT/
├── insurance_bot/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── check_vehicle_registration.py
│   │   ├── create_payment_link.py
│   │   ├── get_available_addons_for_selected_plan.py
│   │   ├── get_available_plans_with_prices.py
│   │   ├── get_idv_values.py
│   │   ├── get_motor_quote.py
│   │   ├── save_motor_quote.py
│   │   ├── send_otp.py
│   │   └── verify_otp.py
│   ├── agent.py
│   ├── app.py
│   ├── config.py
│   ├── routes.py
│   ├── utils.py
│   ├── .env (this is for referance - create your .env file here)
│   └── app.log
└── Myenv
└── requirements.txt
```

# Installation & Setup
## Install dependencies
```
pip install -r requirements.txt
```

# Running the Application
## Run as module 
```
python -m insurance_bot.app
```
