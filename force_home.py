import os, re

# Debug tool to forcefully replace home.html
files = ['template/admin/home.html', 'template/collaborator/home.html']

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    role = 'admin' if 'admin' in fpath else 'collaborator'
    role_t = role.title()
        
    # We strip out everything from <body to </body>
    new_body = f"""<body class="bg-slate-50 min-h-screen font-sans text-slate-800 m-0 flex flex-col">

  <!-- Superior Navbar -->
  <nav class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center gap-4">
          <div class="text-slate-800 hover:text-brand-700 font-bold text-2xl tracking-tight cursor-pointer" onclick="toggleMenu()">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </div>
          <span class="text-xl font-extrabold text-slate-800 tracking-tight">{role_t} Dashboard</span>
        </div>
        <div class="flex items-center gap-4">
           <span class="hidden sm:inline bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-md">Control Panel</span>
           <a href="/{role}/logout" class="text-slate-500 hover:text-red-600 text-sm font-semibold transition-colors flex items-center gap-1">
             <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
             Logout
           </a>
        </div>
      </div>
    </div>
  </nav>

  <!-- Flyout Menu Sidebar -->
  <div class="absolute top-16 left-4 w-60 bg-white border border-slate-200 shadow-xl rounded-lg z-[1001] hidden overflow-hidden transition-all" id="menu">
    <a href="/" class="px-5 py-3.5 text-slate-600 hover:bg-slate-50 hover:text-brand-700 font-medium border-b border-slate-100 flex items-center gap-3">
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
        Home Portal
    </a>
    <a href="/{role}/display" class="px-5 py-3.5 text-slate-600 hover:bg-slate-50 hover:text-brand-700 font-medium border-b border-slate-100 flex items-center gap-3">
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
        Go to Map Display
    </a>
    <a href="/{role}/logout" class="px-5 py-3.5 text-red-500 hover:bg-red-50 font-medium flex items-center gap-3">
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        Log Out
    </a>
  </div>

  <!-- Main Content -->
  <main class="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <div class="mb-10 block">
      <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">System Modules</h1>
      <p class="mt-2 text-md text-slate-500 max-w-3xl">Select a workspace module below to view nodes or enter data pipelines.</p>
    </div>

    <!-- Minimalist Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <a href="/{role}/display" style="text-decoration:none;" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-brand-400 hover:shadow-lg transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-brand-50 text-brand-700 rounded-xl group-hover:bg-brand-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-1 group-hover:text-brand-700">Display Page</h3>
            <p class="text-sm text-slate-500 leading-relaxed">View generated data, interactive maps, and final analytics.</p>
        </div>
      </a>

      <a href="/{role}/upload/display" style="text-decoration:none;" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-indigo-400 hover:shadow-lg transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-indigo-50 text-indigo-600 rounded-xl group-hover:bg-indigo-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-1 group-hover:text-indigo-600">Upload Display</h3>
            <p class="text-sm text-slate-500 leading-relaxed">Upload rendered structural set intended for direct GIS integration.</p>
        </div>
      </a>

      <a href="/{role}/upload/training" style="text-decoration:none;" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-teal-400 hover:shadow-lg transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-teal-50 text-teal-600 rounded-xl group-hover:bg-teal-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-1 group-hover:text-teal-600">Upload Training</h3>
            <p class="text-sm text-slate-500 leading-relaxed">System ingestion. Load historical datasets for deep ML training paths.</p>
        </div>
      </a>

      <a href="/{role}/upload/testing" style="text-decoration:none;" class="group bg-white border border-slate-200 rounded-xl p-6 hover:border-sky-400 hover:shadow-lg transition-all flex flex-col items-start gap-4">
        <div class="p-3 bg-sky-50 text-sky-600 rounded-xl group-hover:bg-sky-600 group-hover:text-white transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
        </div>
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-1 group-hover:text-sky-600">Upload Testing</h3>
            <p class="text-sm text-slate-500 leading-relaxed">Provide verification databatches to validate system model accuracy.</p>
        </div>
      </a>

    </div>
  </main>
  
  <script>
    function toggleMenu() {
        const menu = document.getElementById("menu");
        if (menu.classList.contains("hidden")) {
            menu.classList.remove("hidden");
        } else {
            menu.classList.add("hidden");
        }
    }
  </script>
</body>"""
    
    html = re.sub(r'<body.*?>.*?</body\s*>', new_body, html, flags=re.DOTALL|re.IGNORECASE)
    
    # In case there was a script outside the body tag from previous iterations
    html = re.sub(r'<script.*?>\s*function toggleMenu\(\).*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Homepages updated to minimal flat SaaS design.")
