import os
import re

target_dir = r"c:\MY PROJECTS\ZUNO STRANDS AGENT (UPDATED)\Strands-Agents-for-Insurance"

# Regex to match numeric step comments like:
# # 1. Something
# # Step 1: Something
pattern = re.compile(r"^\s*#\s*(?:\d+\.|Step\s*\d+:)\s*.*", flags=re.IGNORECASE)

for root, dirs, files in os.walk(target_dir):
    for filename in files:
        if filename.endswith(".py"):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            changed = False
            for line in lines:
                if pattern.match(line):
                    changed = True
                    continue
                new_lines.append(line)

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"Stripped comments from {filepath}")
