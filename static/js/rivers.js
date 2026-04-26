
const API_BASE = "https://narmada-project.onrender.com";


function loadRiverData() {
  const status = document.getElementById("status");
  const tbody = document.getElementById("riverTableBody");

  status.textContent = "Loading data...";
  tbody.innerHTML = "";

  fetch(`${API_BASE}/api/admin-rivers-per-district`)
    .then(res => res.json())
    .then(data => {
      data.forEach(d => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${d.district}</td>
          <td><span class="badge">${d.river_count}</span></td>
          <td class="river-list">${d.river_names.join(", ")}</td>
        `;

        tbody.appendChild(row);
      });

      status.textContent = "Data loaded successfully";
    })
    .catch(err => {
      console.error(err);
      status.textContent = "Backend not running!";
      alert("Flask backend is not running");
    });
}

  document.addEventListener("DOMContentLoaded", loadRiverData);
