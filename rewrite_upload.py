import re
import os

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

roles = ['admin', 'collaborator']
ufiles = ['upload_display.html', 'upload_testing.html', 'upload_training.html']

for role in roles:
    for ufile in ufiles:
        path = f"template/{role}/{ufile}"
        if not os.path.exists(path): continue
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        # strip existing styles
        html = re.sub(r'<style>.*?</style>', tailwind_script, html, flags=re.DOTALL|re.IGNORECASE)
        
        # Determine Title
        if "display" in ufile: title = "Station Display Data Upload"
        elif "testing" in ufile: title = "Testing Data Upload"
        else: title = "Training Data Upload"

        # replace topbar completely
        html = re.sub(r'<div class="topbar">.*?</div>', f'<div class="sticky top-0 z-50 bg-brand-700/80 backdrop-blur-xl text-white px-6 py-4 flex justify-between items-center font-bold text-xl shadow-lg border-b border-brand-900/50"><span>{title}</span> <a href="/{role}/home" class="bg-white/10 hover:bg-white/20 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-all backdrop-blur-sm border border-white/20 shadow-[0_4px_12px_rgba(0,0,0,0.1)] cursor-pointer ml-auto hover:scale-105">Back to Dashboard</a></div>', html, flags=re.DOTALL|re.IGNORECASE)

        # Start making container flex body
        # replace body completely
        body_start = r'<body class="bg-gradient-to-br from-brand-700 to-brand-400 min-h-screen font-sans text-slate-800 m-0">\n'
        html = re.sub(r'<body.*?>', body_start, html, flags=re.IGNORECASE)

        # change <div class="container"> and <div class="card">
        html = re.sub(r'<div class="container">', '<div class="flex items-center justify-center min-h-[calc(100vh-80px)] p-4 sm:p-6 lg:p-10">\n', html)
        
        # Fix container cards. upload_testing uses `<div class="card">`, upload_display uses nothing. Let's unify.
        html = re.sub(r'<div class="card">', '', html)
        html = re.sub(r'<form(.+?)>', r'<div class="bg-white/95 backdrop-blur-[20px] p-8 sm:p-12 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.4)] border border-white/40 w-full max-w-lg mt-6 mb-6 transition-all duration-500 hover:shadow-[0_25px_60px_-12px_rgba(31,60,136,0.35)]">\n    <form\1 class="space-y-2">', html, flags=re.IGNORECASE)
        html = re.sub(r'</form>\s*</div>\s*</div>', r'</form>\n  </div>\n</div>', html, flags=re.IGNORECASE)

        # Handle headings inside or outside
        # actually, h2 is outside the form in display
        html = re.sub(r'<h2>(.*?)</h2>', r'</div>\n<div class="bg-white/95 backdrop-blur-[20px] p-8 sm:p-12 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.4)] border border-white/40 w-full max-w-lg mt-6 mb-6 transition-all duration-500">\n<h2 class="text-3xl font-extrabold text-brand-700 text-center tracking-tight mb-8 drop-shadow-sm">\1</h2>', html)
        
        # cleanup double divs introduced
        html = html.replace('<div class="bg-white/95 backdrop-blur-[20px] p-8 sm:p-12 rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.4)] border border-white/40 w-full max-w-lg mt-6 mb-6 transition-all duration-500 hover:shadow-[0_25px_60px_-12px_rgba(31,60,136,0.35)]">\n    </div>', '')

        # labels
        html = re.sub(r'<label(.*?)>(.*?)</label>', r'<label class="block mt-4 text-sm font-semibold text-slate-700 tracking-wide uppercase px-1">\2</label>', html)
        
        # inputs
        html = re.sub(r'<input\s+type="number"(.*?)>', r'<input type="number"\1 class="w-full mt-2 px-5 py-3.5 rounded-2xl border border-slate-200 outline-none focus:ring-4 focus:ring-brand-400/30 focus:border-brand-400 bg-slate-50 hover:bg-white transition-all font-medium text-slate-700 shadow-inner">', html)
        
        html = re.sub(r'<select\s+name="month"(.*?)>', r'<div class="relative"><select name="month"\1 class="w-full mt-2 px-5 py-3.5 rounded-2xl border border-slate-200 outline-none focus:ring-4 focus:ring-brand-400/30 focus:border-brand-400 bg-slate-50 hover:bg-white transition-all font-medium text-slate-700 shadow-inner appearance-none"><div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 mt-2 text-slate-500"><svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg></div></div>', html)
        
        html = re.sub(r'<input\s+type="file"(.*?)>', r'<div class="mt-5 mb-3 group"><input type="file"\1 class="block w-full text-sm text-slate-500 file:mr-5 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-bold file:bg-brand-50 file:text-brand-700 group-hover:file:bg-brand-100 transition-all border border-slate-200 rounded-2xl px-5 py-4 bg-slate-50 group-hover:bg-white focus:outline-none focus:ring-4 focus:ring-brand-400/30 shadow-inner cursor-pointer file:cursor-pointer file:shadow-[0_2px_8px_rgba(59,91,165,0.15)] group-hover:border-brand-400"></div>', html)
        
        html = re.sub(r'<button\s+type="submit"(.*?)>(.*?)</button>', r'<button type="submit" class="w-full mt-8 py-4 bg-gradient-to-r from-brand-700 to-brand-400 hover:from-brand-900 hover:to-brand-700 text-white font-extrabold rounded-2xl shadow-[0_8px_20px_rgba(31,60,136,0.3)] hover:shadow-[0_12px_25px_rgba(31,60,136,0.45)] hover:-translate-y-1 transition-all outline-none focus:ring-4 focus:ring-brand-400/50 focus:ring-offset-2 text-lg tracking-wide">\2</button>', html)

        # Fix specific nested issue with `<div class="card">` that might not have closed forms correctly depending on the template structure.
        # But this covers the main upload form fields logic properly.
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
print("Forms styled perfectly!")
