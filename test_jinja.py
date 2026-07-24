from flask import Flask
from jinja2 import Environment, FileSystemLoader
import os

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

failed = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            rel_path = os.path.relpath(os.path.join(root, file), 'templates')
            try:
                env.get_template(rel_path.replace('\\', '/'))
            except Exception as e:
                failed.append((rel_path, str(e)))

if failed:
    print(f"Failed to compile {len(failed)} templates:")
    for f, e in failed:
        print(f"{f}: {e}")
else:
    print("All templates compiled successfully!")
