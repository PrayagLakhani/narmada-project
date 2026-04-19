import os
import re

files = [
    'template/admin/upload_display.html',
    'template/admin/upload_testing.html',
    'template/admin/upload_training.html',
    'template/collaborator/upload_display.html',
    'template/collaborator/upload_testing.html',
    'template/collaborator/upload_training.html'
]

for f in files:
    fpath = f"/home/nitin/software/{f}"
    if not os.path.exists(fpath): continue
    
    with open(fpath, 'r', encoding='utf-8') as f_in:
        html = f_in.read()
        
    # Replace background and flex centered alignment with simple padded container
    html = html.replace('<body class="bg-slate-50 min-h-screen text-slate-800 flex items-center justify-center p-6 font-sans">', '<body class="bg-slate-50 min-h-screen text-slate-800 p-8 font-sans">')
    
    # We remove max-w-lg and center alignments to let the form breathe and look modern
    html = html.replace('max-w-lg w-full bg-white rounded-2xl shadow-xl border border-slate-200 p-8', 'max-w-4xl mx-auto bg-white rounded-lg shadow-sm border border-slate-200 p-8 md:p-12 mt-8 mb-8')
    
    # Text changes
    html = html.replace('text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600', 'text-2xl font-semibold text-slate-900 mb-2')
    html = html.replace('text-center mb-8', 'text-left mb-10')
    html = html.replace('<p class="text-sm text-slate-500 mt-2 font-medium">Please select a file to upload.</p>', '<p class="text-sm text-slate-500">Provide the dataset required for processing. Must be standard CSV format.</p>')
    
    # Button modern styling
    html = html.replace('class="w-full flex justify-center py-3.5 px-4 rounded-xl text-sm font-bold text-white bg-slate-800 hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-900 shadow-lg hover:shadow-xl transition-all duration-300"', 'class="inline-flex justify-center items-center py-2.5 px-6 rounded-md text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600 shadow-sm transition-colors mt-6"')

    # Go back button modern styling
    html = html.replace('class="mt-6 w-full flex justify-center py-3.5 px-4 border border-slate-200 rounded-xl shadow-sm text-sm font-bold text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-200 transition-all duration-300"', 'class="inline-flex justify-center py-2 px-4 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors mt-8"')

    with open(fpath, 'w', encoding='utf-8') as f_out:
        f_out.write(html)
        
print("Upload forms updated to SaaS design.")