import os, re

files = [
    'template/admin/home.html',
    'template/collaborator/home.html',
    'template/admin/upload_display.html',
    'template/admin/upload_testing.html',
    'template/admin/upload_training.html',
    'template/collaborator/upload_display.html',
    'template/collaborator/upload_testing.html',
    'template/collaborator/upload_training.html'
]

for fpath in files:
    if not os.path.exists(fpath): continue
        
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Standardize Tailwind script (ensure it exists)
    if 'home.html' in fpath:
        role = 'admin' if 'admin' in fpath else 'collaborator'
        role_t = role.title()
        
        # Sleek, enterprise SaaS dashboard look
        new_body = f"""<body class="bg-slate-50 min-h-screen font-sans text-slate-800 m-0 flex flex-col">

  <!-- Superior Navbar -->
  <nav class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center gap-4">
          <div class="text-brand-700 font-bold text-2xl tracking-tight cursor-pointer" onclick="toggleMenu()">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </div>
          <span class="text-xl font-extrabold text-slate-800 tracking-tight">{role_t} Dashboard</span>
        </div>
        <div class="flex items-center gap-4">
           <span class="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-md">Control Panel</span>
           <a href="/{role}/logout" class="text-slate-500 hover:text-red-500 text-sm font-semibold transition-colors flex items-center gap-1">
             <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
             Logout
           </a>
        </div>
      </div>
    </div>
  </nav>

  <!-- Flyout Menu Sidebar -->
  <div class="absolute top-16 left-4 w-64 bg-white border border-slate-200 shadow-xl rounded-lg z-[1001] hidden overflow-hidden transition-all" id="menu">
    <a href="/" class="block px-5 py-3.5 text-slate-600 hover:bg-slate-50 hover:text-brand-700 font-medium border-b border-slate-100 flex items-center gap-3">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
        Home Portal
    </a>
    <a href="/{role}/logout" class="block px-5 py-3.5 text-red-500 hover:bg-red-50 font-medium flex items-center gap-3">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        Log Out
    </a>
  </div>

  <!-- Main Content -->
  <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <div class="mb-10">
      <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">System Modules</h1>
      <p class="mt-2 text-md text-slate-500 max-w-3xl">Select a workspace module below to process, manage, or view system pipelines and display nodes.</p>
    </div>

    <!-- Minimalist Grid Links -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      
      <a href="/{role}/display" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-brand-400 hover:shadow-md transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-brand-50 text-brand-700 rounded-lg group-hover:bg-brand-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-brand-700">Display Page</h3>
            <p class="text-sm text-slate-500 leading-relaxed">View generated data, interactive maps, and final analytics.</p>
        </div>
      </a>

      <a href="/{role}/upload/display" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-brand-400 hover:shadow-md transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-indigo-50 text-indigo-600 rounded-lg group-hover:bg-indigo-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-indigo-600">Upload Display</h3>
            <p class="text-sm text-slate-500 leading-relaxed">Upload rendered sets intended directly for display integration.</p>
        </div>
      </a>

      <a href="/{role}/upload/training" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-brand-400 hover:shadow-md transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-teal-50 text-teal-600 rounded-lg group-hover:bg-teal-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-teal-600">Upload Training</h3>
            <p class="text-sm text-slate-500 leading-relaxed">System ingestion. Load historical datasets for ML training paths.</p>
        </div>
      </a>

      <a href="/{role}/upload/testing" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-brand-400 hover:shadow-md transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-sky-50 text-sky-600 rounded-lg group-hover:bg-sky-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-sky-600">Upload Testing</h3>
            <p class="text-sm text-slate-500 leading-relaxed">Provide verification data batches to validate model accuracy.</p>
        </div>
      </a>

    </div>
  </main>
</body>"""
        # We also need to strip any old menu toggle scripts since we embedded toggleMenu but didn't redefine it.
        # It was defined inside the file, but we can just use the existing one if it's there. 
        # For home.html we replace the whole body.
        html = re.sub(r'<body.*?>.*?</body>', new_body, html, flags=re.DOTALL|re.IGNORECASE)

    else:
        # It's an upload page (Flat minimalist clean design)
        role = 'admin' if 'admin' in fpath else 'collaborator'
        if "display" in fpath: 
            title_top = "Station Display Data Upload" if role == 'admin' else "GIS Layer Upload"
            desc_text = "Upload static layer maps and raster sets for GIS display processing."
        elif "testing" in fpath: 
            title_top = "Testing Data Upload"
            desc_text = "Upload structural data tests to validate current models securely."
        else: 
            title_top = "Training Data Upload"
            desc_text = "Push raw input batches for continuous pipeline ML training."
        
        # New clean body replacement for uploads
        body_intro = f"""<body class="bg-slate-50 min-h-screen font-sans text-slate-800 m-0 flex flex-col">
    <!-- Navbar -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center gap-3">
                    <span class="text-xl font-bold text-slate-900 tracking-tight">{title_top}</span>
                </div>
                <div class="flex items-center gap-4">
                    <a href="/{role}/home" class="text-sm font-semibold text-slate-500 hover:text-brand-700 transition-colors flex items-center gap-2 px-3 border border-transparent hover:border-slate-200 rounded-md py-1.5 focus:outline-none">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                        Back to Dashboard
                    </a>
                </div>
            </div>
        </div>
    </nav>
    
    <main class="flex-grow w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        <div class="mb-8">
            <p class="text-sm text-slate-500 font-medium tracking-tight mb-2"><a href="/{role}/home" class="hover:text-brand-600 transition-colors">Home</a> <span class="mx-1">/</span> Uploads</p>
            <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">{title_top}</h1>
            <p class="mt-2 text-slate-500 max-w-2xl">{desc_text}</p>
        </div>"""
        
        html = re.sub(r'<body.*?>', body_intro, html, flags=re.IGNORECASE)
        html = re.sub(r'<div class="sticky top-0 z-50.*?</div>\s*<div class="flex items-center justify-center min-h-\[calc\(100vh-80px\)\] p-4 sm:p-6 lg:p-10">', '\n<div class="bg-white border border-slate-200 rounded-xl shadow-sm p-6 md:p-8 w-full">', html, flags=re.DOTALL|re.IGNORECASE)
        
        # In upload_display of collaborator we had an extra <div flex items-center pt-6> for clear btn.
        # We will rip out any previous floating clear button div cleanly.
        html = re.sub(r'<div class="flex items-center justify-center pt-6 pb-1">.*?</div>', '', html, flags=re.DOTALL|re.IGNORECASE)
        
        # Modify the form
        html = re.sub(r'<form(.*?) (class="bg-white/95.*?")>', r'<form\1 class="space-y-5">', html, flags=re.IGNORECASE|re.DOTALL)
        # Some forms didn't capture properly, let's just make it raw
        html = re.sub(r'<form\s+id="uploadForm"[^>]*>', r'<form id="uploadForm" class="space-y-6 max-w-3xl">', html, flags=re.IGNORECASE)
        
        # Fix any remaining container closures at bottom
        html = re.sub(r'</form>\s*</div>\s*</body>', '</form>\n        </div>\n    </main>\n</body>', html, flags=re.IGNORECASE)
        html = re.sub(r'</form>\n</div>(?!\n\s*</main>)', '</form>\n        </div>\n    </main>', html, flags=re.IGNORECASE)
        
        # Form headings -> small section titles
        html = re.sub(r'<h2 class="text-3xl font-extrabold text-brand-700 text-center tracking-tight mb-8">.*?</h2>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<h2 class="text-3xl font-extrabold text-brand-700 text-center tracking-tight mb-2 drop-shadow-sm">.*?</h2>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<h4 class="text-xl font-[a-z]+ text-brand-700 border-b-2 border-slate-[0-9]+ pb-2 mb-4 mt-[0-9]+">(.*?)</h4>', r'<h4 class="text-md uppercase tracking-wider font-bold text-slate-500 border-b border-slate-100 pb-2 mt-10 mb-4">\1</h4>', html, flags=re.IGNORECASE)
        
        # Labels and Form Elements
        html = re.sub(r'<label\s+class="block mt-4 text-sm font-semibold text-slate-[0-9]+ tracking-wide uppercase px-1">(.*?)</label>', r'<label class="block text-sm font-bold text-slate-700 mb-1">\1</label>', html, flags=re.IGNORECASE)
        html = re.sub(r'<label\s+class="block text-sm font-bold text-slate-700 mb-1">(.*?)\s*<input\s+type="file"', r'<label class="block text-sm font-bold text-slate-700 mt-5 mb-1">\1</label><input type="file"', html, flags=re.IGNORECASE)

        # File Inputs
        html = re.sub(r'class="block w-full text-sm text-slate-500 file:mr-5 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-all border border-slate-200 rounded-[a-z0-9]+ px-5 py-3.5 bg-slate-50 hover:bg-white focus:outline-none shadow-[a-z-]+ cursor-pointer mt-2"', 
                      'class="block w-full text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 transition-all border border-slate-200 rounded-lg px-3 py-2 bg-white outline-none cursor-pointer hover:border-slate-300 focus:border-brand-500 focus:ring-1 focus:ring-brand-500"', html, flags=re.IGNORECASE|re.DOTALL)
        
        # Number Inputs
        html = re.sub(r'class="w-full mt-2 px-5 py-3.5 rounded-[a-z0-9]+ border border-slate-200 outline-none focus:ring-4 focus:ring-brand-[a-z0-9/]+ focus:border-brand-[a-z0-9]+ bg-slate-50 hover:bg-white transition-all font-medium text-slate-700 shadow-[a-z-]+"?',
                      'class="w-full px-3 py-2.5 rounded-lg border border-slate-200 outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 bg-white hover:border-slate-300 transition-colors font-medium text-slate-800"', html, flags=re.IGNORECASE|re.DOTALL)

        # Select
        html = re.sub(r'class="w-full mt-2 px-5 py-3.5 rounded-[a-z0-9]+ border border-slate-200 outline-none focus:ring-4 focus:ring-brand-[a-z0-9/]+ focus:border-brand-[a-z0-9]+ bg-slate-50 hover:bg-white transition-all font-medium text-slate-700 shadow-[a-z-]+ appearance-none"?',
                      'class="w-full px-3 py-2.5 rounded-lg border border-slate-200 outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 bg-white hover:border-slate-300 transition-colors font-medium text-slate-800 appearance-none"', html, flags=re.IGNORECASE|re.DOTALL)

        # Submit Buttons (solid dark slate/brand color)
        html = re.sub(r'<button\s+type="submit"\s+class="w-full mt-[0-9]+ py-4 bg-gradient-to-r from-brand-[0-9]+ to-brand-[0-9]+ hover:from-brand-[0-9]+ hover:to-brand-[0-9]+ text-white font-extrabold rounded-[a-z0-9]+ shadow-[a-z]+ hover:shadow-[a-z]+ hover:-translate-y-1 transition-all outline-none focus:ring-4 focus:ring-brand-[0-9a-z/]+ text-lg(?: tracking-wide)?"\s*(id="submitBtn")?>(.*?)</button>',
                      r'<div class="pt-6 border-t border-slate-100 mt-8"><button type="submit" \1 class="w-full sm:w-auto px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-lg shadow-sm transition-colors outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-900 text-base">\2</button></div>', html, flags=re.IGNORECASE|re.DOTALL)
        
        # Clear btn (if exists) -> placed before the main card or inside the card header
        # Instead of placing it weirdly, place it nicely right aligned
        if "onclick=\"confirmClear()\"" in html:
            clear_btn = r'<button class="text-sm bg-white border border-red-200 text-red-600 hover:bg-red-50 font-semibold py-1.5 px-3 rounded-md shadow-sm transition-colors block ml-auto mt-4" onclick="confirmClear()">🗑 Clear Directory</button>'
            html = re.sub(r'<button.*?confirmClear\(\).*?</button>', '', html, flags=re.DOTALL|re.IGNORECASE)
            html = html.replace('</h1>', f'</h1>\n            {clear_btn}')
            
        # Role text & Banners
        html = re.sub(r'<p id="roleText" class="text-center font-medium text-slate-500 mb-6"></p>', r'<p id="roleText" class="text-sm font-medium text-slate-500 mb-4"></p>', html, flags=re.IGNORECASE)
        html = re.sub(r'<div class="text-center font-semibold text-\[13px\] text-brand-700 bg-brand-[0-9/]+ border border-brand-[0-9/]+ rounded-xl padding-3 mb-6 p-4 break-all shadow-[a-z-]+" id="saveBanner"></div>', r'<div class="text-sm font-medium text-amber-800 bg-amber-50 border border-amber-200 rounded-lg mb-6 p-3 break-all hidden" id="saveBanner"></div>', html, flags=re.IGNORECASE)
        
        # Adjust Status and Progress
        html = re.sub(r'<div id="progressWrapper"(.*?)>.*?</div>', r'<div id="progressWrapper" class="w-full bg-slate-100 rounded-md h-2 mt-4 overflow-hidden hidden"><div id="progressBar" class="bg-brand-500 h-2 transition-all duration-300" style="width: 0%"></div></div>', html, flags=re.IGNORECASE|re.DOTALL)
        html = re.sub(r'<p id="status" class="mt-6 font-semibold text-center text-lg text-brand-700 min-h-\[28px\]"></p>', r'<p id="status" class="mt-4 font-semibold text-sm text-slate-700 min-h-[20px]"></p>', html, flags=re.IGNORECASE)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
print("Modern, clean UI applied based on Tailwind")
