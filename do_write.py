import os

d = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE} - Narmada Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = { theme: { extend: { colors: { brand: { 400: '#3b5ba5', 700: '#1f3c88', 900: '#16306d' } }, fontFamily: { sans: ['Inter', 'sans-serif'] } } } }
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gray-50 flex flex-col min-h-screen font-sans antialiased text-gray-800 relative overflow-hidden">

  <!-- Background decorations (matched to login pages) -->
  <div class="absolute top-0 left-0 w-full h-80 bg-gradient-to-br from-brand-700 to-brand-400 rounded-b-[4rem] shadow-xl z-0"></div>
  <div class="absolute top-10 left-10 w-64 h-64 bg-white opacity-10 mix-blend-overlay rounded-full z-0"></div>
  <div class="absolute top-40 right-20 w-80 h-80 bg-brand-900 opacity-20 mix-blend-overlay rounded-full z-0"></div>

  <!-- Navbar layered over background -->
  <div class="w-full flex justify-between items-center p-6 z-10 relative">
    <h1 class="text-white font-bold text-xl tracking-wide">{ROLE_NAME} Portal</h1>
    <a href="{BACK_LINK}" class="text-white hover:text-gray-200 text-sm font-medium transition-colors flex items-center justify-center gap-1">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
      Back to Dashboard
    </a>
  </div>

  <!-- Main Login-style Form Card -->
  <div class="flex-grow flex items-center justify-center p-4 z-10 relative">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-2xl border border-gray-100 p-8">
      
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-50 text-indigo-700 mb-4 shadow-sm flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 tracking-tight">{TITLE}</h2>
        <p class="text-gray-500 text-sm mt-2">Upload your dataset in CSV format.</p>
      </div>

      <!-- FORM -->
      <form id="uploadForm" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Year</label>
          <input type="number" name="year" class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-brand-700 focus:border-brand-700 text-sm transition-colors bg-white text-gray-900" placeholder="2024" required>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Month</label>
          <div class="relative">
            <select name="month" class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-brand-700 focus:border-brand-700 text-sm transition-colors bg-white text-gray-900 appearance-none" required>
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
            <svg class="absolute right-3 top-3 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">CSV File</label>
          <input type="file" name="file" accept=".csv" class="block w-full text-sm text-gray-500 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-colors" required>
        </div>
        
        <button type="submit" class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-md text-sm font-medium text-white bg-brand-700 hover:bg-brand-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-700 transition-colors mt-2">Upload & Process</button>
      </form>

      <p id="status" class="mt-6 text-sm font-medium text-center"></p>

    </div>
  </div>

<script>
document.getElementById("uploadForm").onsubmit = async (e) => {
    e.preventDefault();

    const status = document.getElementById("status");
    status.innerText = "Uploading...";
    status.style.color = "#6B7280";

    const formData = new FormData(e.target);

    try {
        const res = await fetch("{ENDPOINT}", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.error || "Upload failed");

        status.style.color = "#10B981";
        status.innerText = "✅ Upload successful";
        e.target.reset();

    } catch (err) {
        status.style.color = "#EF4444";
        status.innerText = "❌ " + err.message;
    }
};
</script>
</body>
</html>"""

pages = [
    {
        "file": "template/admin/upload_display.html",
        "title": "Upload Display Data",
        "role_name": "Admin",
        "back_link": "/admin/home",
        "endpoint": "/api/admin-update-stations-display"
    },
    {
        "file": "template/admin/upload_testing.html",
        "title": "Upload Testing Data",
        "role_name": "Admin",
        "back_link": "/admin/home",
        "endpoint": "/api/admin-ingest-testing"
    },
    {
        "file": "template/admin/upload_training.html",
        "title": "Upload Training Data",
        "role_name": "Admin",
        "back_link": "/admin/home",
        "endpoint": "/api/admin-ingest-training"
    },
    {
        "file": "template/collaborator/upload_display.html",
        "title": "Upload Display Data",
        "role_name": "Collaborator",
        "back_link": "/collaborator/home",
        "endpoint": "/api/collaborator-update-stations-display"
    },
    {
        "file": "template/collaborator/upload_testing.html",
        "title": "Upload Testing Data",
        "role_name": "Collaborator",
        "back_link": "/collaborator/home",
        "endpoint": "/api/collaborator-ingest-testing"
    },
    {
        "file": "template/collaborator/upload_training.html",
        "title": "Upload Training Data",
        "role_name": "Collaborator",
        "back_link": "/collaborator/home",
        "endpoint": "/api/collaborator-ingest-training"
    }
]

base = os.path.dirname(os.path.abspath(__file__))
for p in pages:
    fpath = os.path.join(base, p["file"])
    with open(fpath, "w", encoding="utf-8") as f:
        c = d.replace("{TITLE}", p["title"])
        c = c.replace("{ROLE_NAME}", p["role_name"])
        c = c.replace("{BACK_LINK}", p["back_link"])
        c = c.replace("{ENDPOINT}", p["endpoint"])
        f.write(c)

print("done writing pages natively!")