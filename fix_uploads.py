import os

files = [
    '/home/nitin/software/template/admin/upload_display.html',
    '/home/nitin/software/template/admin/upload_testing.html',
    '/home/nitin/software/template/admin/upload_training.html',
    '/home/nitin/software/template/collaborator/upload_display.html',
    '/home/nitin/software/template/collaborator/upload_testing.html',
    '/home/nitin/software/template/collaborator/upload_training.html'
]

for fpath in files:
    if not os.path.exists(fpath):
        print(f"Skipping {fpath} - not found")
        continue
    
    role = 'admin' if 'admin' in fpath else 'collaborator'
    page_type = 'display' if 'display' in fpath else ('testing' if 'testing' in fpath else 'training')
    
    api_endpoint = f"/api/{role}-update-stations-{page_type}" if page_type == 'display' else f"/api/{role}-ingest-{page_type}"
    title_map = {'display': 'Display', 'testing': 'Testing', 'training': 'Training'}
    form_title = f"Upload {title_map[page_type]} Data"
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Data Upload</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{
    theme: {{
      extend: {{
        colors: {{
          brand: {{
            400: '#3b5ba5',
            700: '#1f3c88',
            900: '#16306d',
          }}
        }}
      }}
    }}
  }}
</script>
</head>

<body class="bg-slate-50 min-h-screen font-sans text-slate-800 m-0 flex flex-col">

<!-- Clean Navbar -->
<nav class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <h1 class="text-lg font-bold text-slate-900">Upload {title_map[page_type]} Data</h1>
      <a href="/{role}/home" class="text-slate-600 hover:text-slate-900 font-medium text-sm transition-colors">
        ← Back to Dashboard
      </a>
    </div>
  </div>
</nav>

<!-- Main Content -->
<main class="flex-grow flex items-center justify-center p-6">
  <form id="uploadForm" class="w-full max-w-2xl bg-white rounded-lg shadow-sm border border-slate-200 p-8 md:p-10">
    
    <h2 class="text-2xl font-semibold text-slate-900 mb-2">{form_title}</h2>
    <p class="text-slate-600 text-sm mb-8">Provide the dataset in standard CSV format for processing.</p>

    <div class="space-y-6">
      
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-2">Year</label>
        <input type="number" name="year" required class="w-full px-4 py-2.5 rounded-md border border-slate-300 outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white text-slate-900 placeholder-slate-400 transition-colors" placeholder="2024">
      </div>

      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-2">Month</label>
        <div class="relative">
          <select name="month" required class="w-full px-4 py-2.5 rounded-md border border-slate-300 outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white text-slate-900 appearance-none transition-colors">
            <option value="">Select a month</option>
            <option value="Jan">January</option>
            <option value="Feb">February</option>
            <option value="Mar">March</option>
            <option value="Apr">April</option>
            <option value="May">May</option>
            <option value="Jun">June</option>
            <option value="Jul">July</option>
            <option value="Aug">August</option>
            <option value="Sep">September</option>
            <option value="Oct">October</option>
            <option value="Nov">November</option>
            <option value="Dec">December</option>
          </select>
          <svg class="absolute right-3 top-3 w-4 h-4 text-slate-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </div>
      </div>

      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-2">CSV File</label>
        <input type="file" name="file" accept=".csv" required class="block w-full text-sm text-slate-500 file:mr-3 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-colors">
      </div>

      <button type="submit" class="w-full py-2.5 px-4 rounded-md bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
        Upload & Process
      </button>

    </div>

    <p id="status" class="mt-6 text-sm font-medium text-center"></p>

  </form>
</main>

<script>
document.getElementById("uploadForm").onsubmit = async (e) => {{
    e.preventDefault();

    const status = document.getElementById("status");
    status.innerText = "Uploading...";
    status.style.color = "#6B7280";

    const formData = new FormData(e.target);

    try {{
        const res = await fetch("{api_endpoint}", {{
            method: "POST",
            body: formData
        }});

        const data = await res.json();

        if (!res.ok) throw new Error(data.error);

        status.style.color = "#10B981";
        status.innerText = "✅ Uploaded successfully";

    }} catch (err) {{
        status.style.color = "#EF4444";
        status.innerText = "❌ " + err.message;
    }}
}};

function logout() {{
    localStorage.clear();
    window.location.href = "/login";
}}
</script>

</body>
</html>'''

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

print("All upload pages fixed with flat SaaS design.")
