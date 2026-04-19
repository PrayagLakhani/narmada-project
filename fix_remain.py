import os, re
files = ['template/collaborator/home.html', 'template/admin/upload_testing.html', 'template/admin/upload_training.html', 'template/collaborator/upload_testing.html', 'template/collaborator/upload_training.html']

for fpath in files:
    if not os.path.exists(fpath): continue
        
    with open(fpath, 'r', encoding='utf-8') as f: html = f.read()

    if 'home.html' in fpath:
        role = 'admin' if 'admin' in fpath else 'collaborator'
        role_t = role.title()
        
        new_body = f"""<body class="bg-gradient-to-br from-brand-700 to-brand-400 min-h-screen font-sans text-slate-800 m-0">

  <div class="sticky top-0 z-50 bg-brand-700/80 backdrop-blur-xl text-white px-6 py-4 flex justify-between items-center font-bold text-xl shadow-lg border-b border-brand-900/50" onclick="toggleMenu()">
    <div class="flex items-center gap-3 cursor-pointer">
      <div class="text-2xl font-bold cursor-pointer">&#9776;</div>
      <span class="text-xl font-bold">{role_t} Dashboard</span>
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
      <a href="/{role}/display" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300" style="text-decoration:none;">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Enter Display Page</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Open the analytics and map visualization dashboard.</span>
      </a>
      <a href="/{role}/upload/display" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300" style="text-decoration:none;">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Upload Display Data</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Push current display datasets for immediate viewing.</span>
      </a>
      <a href="/{role}/upload/training" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300" style="text-decoration:none;">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Upload Training Data</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Submit training datasets for model preparation.</span>
      </a>
      <a href="/{role}/upload/testing" class="group block p-8 rounded-3xl border border-white/60 bg-white/95 backdrop-blur-xl shadow-xl hover:shadow-2xl hover:scale-[1.02] transition-all duration-300" style="text-decoration:none;">
        <span class="block text-xl font-bold text-brand-700 mb-2 group-hover:text-brand-400 transition-colors">Upload Testing Data</span>
        <span class="block text-slate-500 leading-relaxed text-sm">Send testing batches to validate model outcomes.</span>
      </a>
    </div>
  </div>
</body>"""
        html = re.sub(r'<body.*?>.*?</body>', new_body, html, flags=re.DOTALL|re.IGNORECASE)

    else:
        role = 'admin' if 'admin' in fpath else 'collaborator'
        if "display" in fpath: title_top = "Station Display Data Upload" if role == 'admin' else "GIS Layer Upload"
        elif "testing" in fpath: title_top = "Testing Data Upload"
        else: title_top = "Training Data Upload"
        
        html = re.sub(r'<body.*?>', '<body class="bg-gradient-to-br from-brand-700 to-brand-400 min-h-screen font-sans text-slate-800 m-0">', html, flags=re.IGNORECASE)
        html = re.sub(r'<div class="topbar">.*?</div>', f'<div class="sticky top-0 z-50 bg-brand-700/80 backdrop-blur-xl text-white px-6 py-4 flex justify-between items-center font-bold text-xl shadow-lg border-b border-brand-900/50"><span>{title_top}</span> <a href="/{role}/home" class="bg-white/10 hover:bg-white/20 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all backdrop-blur-sm border border-white/20 shadow-sm cursor-pointer ml-auto hover:scale-105" style="text-decoration: none;">Back to Dashboard</a></div>\n<div class="flex items-center justify-center min-h-[calc(100vh-80px)] p-4 sm:p-6 lg:p-10">', html, flags=re.DOTALL|re.IGNORECASE)
        
        html = html.replace('<div class="container">', '')
        html = html.replace('<div class="card">', '')
        
        html = re.sub(r'<form(.+?)>', r'<form\1 class="bg-white/95 backdrop-blur-xl p-8 sm:p-12 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.4)] border border-white/40 w-full max-w-2xl mt-6 mb-6 transition-all duration-500 hover:shadow-[0_25px_60px_-12px_rgba(31,60,136,0.35)] space-y-3">', html, flags=re.IGNORECASE)
        
        html = re.sub(r'</form>\s*</div>\s*</div>', '</form>\n</div>', html, flags=re.IGNORECASE)
        html = re.sub(r'</form>\s*</div>', '</form>\n</div>', html, flags=re.IGNORECASE)
        
        html = re.sub(r'<h2>(.*?)</h2>', r'<h2 class="text-3xl font-extrabold text-brand-700 text-center tracking-tight mb-8">\1</h2>', html, flags=re.IGNORECASE)
        html = re.sub(r'<h4>(.*?)</h4>', r'<h4 class="text-xl font-bold text-brand-700 border-b-2 border-slate-100 pb-2 mb-4 mt-8">\1</h4>', html, flags=re.IGNORECASE)
        html = re.sub(r'<label(.*?)>(.*?)</label>', r'<label\1 class="block mt-4 text-sm font-semibold text-slate-700 tracking-wide px-1">\2</label>', html, flags=re.IGNORECASE|re.DOTALL)
        html = re.sub(r'<input\s+type="file"(.*?)>', r'<input type="file"\1 class="block w-full text-sm text-slate-500 file:mr-5 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-all border border-slate-200 rounded-2xl px-5 py-3.5 bg-slate-50 hover:bg-white focus:outline-none shadow-inner cursor-pointer mt-2">', html, flags=re.IGNORECASE)
        html = re.sub(r'<input\s+type="number"(.*?)>', r'<input type="number"\1 class="w-full mt-2 px-5 py-3.5 rounded-2xl border border-slate-200 outline-none focus:ring-4 focus:ring-brand-400/30 focus:border-brand-400 bg-slate-50 hover:bg-white transition-all font-medium text-slate-700 shadow-inner">', html, flags=re.IGNORECASE)
        html = re.sub(r'<button\s+type="submit"(.*?)>(.*?)</button>', r'<button type="submit"\1 class="w-full mt-8 py-4 bg-gradient-to-r from-brand-700 to-brand-400 hover:from-brand-900 hover:to-brand-700 text-white font-extrabold rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all outline-none focus:ring-4 focus:ring-brand-400/50 text-lg">\2</button>', html, flags=re.IGNORECASE)
        html = re.sub(r'<p\s+id="status"(.*?)</p>', r'<p id="status" class="mt-6 font-semibold text-center text-lg"\1></p>', html, flags=re.IGNORECASE)

    with open(fpath, 'w', encoding='utf-8') as f: f.write(html)
print("Forms fully styled!")