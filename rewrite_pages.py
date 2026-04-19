import os
import re

tailwind_script = """<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          brand: {
            400: '#3b5ba5',
            700: '#1f3c88',
            900: '#16306d',
          }
        }
      }
    }
  }
</script>"""

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Admin & Collaborator Home
roles = ['admin', 'collaborator']
for role in roles:
    h_path = f"template/{role}/home.html"
    if os.path.exists(h_path):
        html = read_file(h_path)
        html = re.sub(r'<style>.*?</style>', tailwind_script, html, flags=re.DOTALL)
        role_title = "Admin" if role == 'admin' else "Collaborator"
        
        new_body = f"""<body class="bg-gradient-to-br from-brand-700 to-brand-400 min-h-[100vh] font-sans text-slate-800 m-0">
  <div class="sticky top-0 z-50 bg-white/10 backdrop-blur-md shadow-sm border-b border-white/20 px-6 py-4 flex justify-between items-center text-white" onclick="toggleMenu()">
    <div class="flex items-center gap-3 cursor-pointer">
      <div class="text-2xl font-bold cursor-pointer">&#9776;</div>
      <span class="text-xl font-bold">{role_title} Dashboard</span>
    </div>
    <span class="text-sm font-medium opacity-90 backdrop-blur-sm bg-white/20 px-4 py-1.5 rounded-full border border-white/20 tracking-wide">Control Panel</span>
  </div>

  <div class="absolute top-16 left-6 w-56 bg-white shadow-2xl rounded-2xl z-[1001] overflow-hidden hidden border border-slate-100" id="menu">
    <a href="/" class="block px-5 py-3.5 text-slate-700 hover:bg-brand-700 hover:text-white transition-colors font-medium border-b border-slate-50">Home</a>
    <a href="/{role}/logout" class="block px-5 py-3.5 text-red-500 hover:bg-red-50 transition-colors font-medium">LogOut</a>
  </div>

  <div class="max-w-4xl mx-auto px-4 pt-12 pb-20">
    <div class="text-center mb-10 bg-white/95 backdrop-blur-xl rounded-3xl p-10 shadow-2xl border border-white/40">
      <h2 class="text-3xl font-extrabold text-brand-700 tracking-tight">Choose Action</h2>
      <p class="mt-3 text-slate-500 font-medium text-lg max-w-lg mx-auto">Manage display insights and upload data pipelines from one central place.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <a href="/{role}/display" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Enter Display Page</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Open the analytics and map visualization dashboard.</span>
      </a>
      <a href="/{role}/upload/display" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Upload Display Data</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Push current display datasets for immediate viewing.</span>
      </a>
      <a href="/{role}/upload/training" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Upload Training Data</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Submit training datasets for model preparation.</span>
      </a>
      <a href="/{role}/upload/testing" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Upload Testing Data</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Send testing batches to validate model outcomes.</span>
      </a>
    </div>
  </div>
</body>"""
        html = re.sub(r'<body.*?>.*?</body>', new_body, html, flags=re.DOTALL)
        write_file(h_path, html)

# Upload Files Update
upload_files = ['upload_display.html', 'upload_testing.html', 'upload_training.html']
for role in roles:
    for ufile in upload_files:
        upath = f"template/{role}/{ufile}"
        if os.path.exists(upath):
            html = read_file(upath)
            html = re.sub(r'<style>.*?</style>', tailwind_script, html, flags=re.DOTALL)
            
            # Determine correct Title for Topbar
            if "display" in ufile: top_title = "Station Display Data Upload"
            elif "testing" in ufile: top_title = "Testing Data Upload"
            else: top_title = "Training Data Upload"
            
            html = re.sub(r'<div class="topbar">.*?</div>', f'<div class="sticky top-0 z-50 bg-brand-700 text-white px-6 py-4 flex justify-between items-center font-bold text-lg shadow-md">{top_title} <a href="/{role}/home" class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm text-white transition-colors cursor-pointer ml-auto border border-white/20">Back to Home</a></div>', html, flags=re.DOTALL)
            
            html = re.sub(r'<div class="container">\s*<form(.+?)</form>\s*</div>', lambda m: f'<div class="min-h-screen bg-gradient-to-br from-brand-700 to-brand-400 flex justify-center items-center py-10 px-4"><form{m.group(1)}</form></div>', html, flags=re.DOTALL|re.IGNORECASE)
            html = re.sub(r'<div class="container">\s*<div class="card">\s*(<h2.*?>.*?</h2>)\s*<form(.+?)</form>\s*<p id="status"></p>\s*</div>\s*</div>', lambda m: f'<div class="min-h-screen bg-gradient-to-br from-brand-700 to-brand-400 flex justify-center items-center py-10 px-4"><div class="bg-white px-10 py-10 rounded-2xl shadow-2xl w-full max-w-md">{m.group(1)}<form{m.group(2)}</form><p id="status" class="mt-4 font-semibold text-center"></p></div></div>', html, flags=re.DOTALL|re.IGNORECASE)
            
            # Form tags modification
            html = re.sub(r'<form(.+?)>', r'<form\1 class="bg-white p-10 rounded-2xl shadow-2xl w-full max-w-md">', html)
            html = re.sub(r'<h2>(.*?)</h2>', r'<h2 class="text-3xl font-extrabold text-brand-700 text-center mb-8">\1</h2>', html)
            html = re.sub(r'<label>(.*?)</label>', r'<label class="block mt-4 text-sm font-semibold text-slate-700">\1</label>', html)
            html = re.sub(r'<input\s+type="number"(.*?)>', r'<input type="number"\1 class="w-full mt-2 px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-400 focus:border-brand-400 bg-slate-50 transition-all font-medium">', html)
            html = re.sub(r'<select\s+name="month"(.*?)>', r'<select name="month"\1 class="w-full mt-2 px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-brand-400 focus:border-brand-400 bg-slate-50 transition-all font-medium">', html)
            html = re.sub(r'<input\s+type="file"(.*?)>', r'<input type="file"\1 class="w-full mt-4 mb-4 text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-all border border-slate-200 rounded-xl px-4 py-3 bg-slate-50">', html)
            html = re.sub(r'<button\s+type="submit"(.*?)>(.*?)</button>', r'<button type="submit" class="w-full mt-6 py-3.5 bg-brand-700 hover:bg-brand-900 text-white font-bold rounded-xl shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all outline-none focus:ring-2 focus:ring-brand-400 focus:ring-offset-2">\2</button>', html)
            
            # status paragraph inside form
            html = re.sub(r'<p\s+id="status"\s*></p>', r'<p id="status" class="mt-4 font-semibold text-center"></p>', html)
            
            write_file(upath, html)

print("Pages updated successfully!")
