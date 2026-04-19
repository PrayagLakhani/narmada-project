import re

files = [
    'template/admin/upload_display.html',
    'template/admin/upload_testing.html',
    'template/admin/upload_training.html',
    'template/collaborator/upload_display.html',
    'template/collaborator/upload_testing.html',
    'template/collaborator/upload_training.html'
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Small manual fix for input[type=file] matching that might not have been fully substituted in the big regex block due to missing/extra classes from last step
    
    # Simple direct string replaces on remaining ugly fields
    html = re.sub(r'class="w-full mt-2 px-5 py-3.5 rounded-2xl border border-slate-200 outline-none focus:ring-4 focus:ring-brand-400/30 focus:border-brand-400 bg-slate-50 hover:bg-white transition-all font-medium text-slate-700 shadow-inner"',
                  'class="w-full px-3 py-2.5 mt-1 rounded-md border border-slate-200 outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 bg-white shadow-sm transition-colors text-sm text-slate-800"', html)
                  
    html = re.sub(r'class="block w-full text-sm text-slate-500 file:mr-5 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-all border border-slate-200 rounded-2xl px-5 py-3.5 bg-slate-50 hover:bg-white focus:outline-none shadow-inner cursor-pointer mt-2"',
                  'class="block w-full text-sm text-slate-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 transition-all border border-slate-200 rounded-md px-2 py-1.5 bg-white outline-none cursor-pointer mt-1"', html)

    html = re.sub(r'class="w-full mt-8 py-4 bg-gradient-to-r from-brand-700 to-brand-400 hover:from-brand-900 hover:to-brand-700 text-white font-extrabold rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all outline-none focus:ring-4 focus:ring-brand-400/50 text-lg"',
                  'class="w-full sm:w-auto px-5 py-2.5 mt-6 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold rounded-md shadow-sm transition-colors outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-900"', html)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Patched remaining element structures")