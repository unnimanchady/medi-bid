with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\\nif __name__ == "__main__":', '\nif __name__ == "__main__":')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed app.py syntax error")
