import os, re
files = ['template/collaborator/home.html', 'template/admin/upload_testing.html', 'template/admin/upload_training.html', 'template/collaborator/upload_display.html', 'template/collaborator/upload_testing.html', 'template/collaborator/upload_training.html']
ts = """<script src="https://cdn.tailwindcss.com"></script>\n<script>\n  tailwind.config = { theme: { extend: { colors: { brand: { 400: '#3b5ba5', 700: '#1f3c88', 900: '#16306d' } } } } }\n</script>"""
for f in files:
    with open(f, 'r', encoding='utf-8') as file: content = file.read()
    content = re.sub(r'<style>.*?</style>', ts, content, flags=re.DOTALL|re.IGNORECASE)
    with open(f, 'w', encoding='utf-8') as file: file.write(content)
print("Done styling")
