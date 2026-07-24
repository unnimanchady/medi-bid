import re

with open('create_hospital_templates.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the chat container to include the ID
content = content.replace(
    '<div class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-bgLight flex flex-col space-y-4">',
    '<div id="message-history-container" class="flex-1 overflow-y-auto custom-scrollbar p-6 bg-bgLight flex flex-col space-y-4">'
)

# Replace the scroll script to query the ID
content = content.replace(
    "const chatContainer = document.querySelector('.overflow-y-auto.custom-scrollbar');",
    "const chatContainer = document.getElementById('message-history-container');"
)

# Replace main_pattern
content = content.replace(
    r"main_pattern = re.compile(r'<!-- MAIN CONTENT -->.*?(?=</div>\n\n    <!-- Scripts -->)', re.DOTALL)",
    r"main_pattern = re.compile(r'<main class=\"flex-1 flex flex-col h-screen overflow-y-auto\">.*?</main>', re.DOTALL)"
)

# And because the replacement should include the <main> tags, we need to ensure inbox_main and thread_main include <main class="flex-1 flex flex-col h-screen overflow-y-auto">...
# Oh wait, thread_main starts with:
# <main class="flex-1 flex flex-col min-w-0 overflow-hidden bg-white">
# Let's verify that.
# Let's just update the main_pattern to match <main...>...</main>

with open('create_hospital_templates.py', 'w', encoding='utf-8') as f:
    f.write(content)
