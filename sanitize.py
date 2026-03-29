import os

target_dir = r"c:\MY PROJECTS\ZUNO STRANDS AGENT (UPDATED)\Strands-Agents-for-Insurance"

replacements = [
    ("import insurance_bot.config", "import insurance_bot.config"),
    ("├── insurance_bot/", "├── insurance_bot/"),
    ("python -m insurance_bot.app", "python -m insurance_bot.app")
]

for root, dirs, files in os.walk(target_dir):
    for filename in files:
        if filename.endswith(".py") or filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            for old, new in replacements:
                new_content = new_content.replace(old, new)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
