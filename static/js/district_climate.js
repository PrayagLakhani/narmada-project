// Load districts

const API_BASE = "https://narmada-project.onrender.com";

fetch(`${API_BASE}/api/admin-districts`)
.then(res => res.json())
.then(data => {
  const dropdown = document.getElementById("districtDropdown");
  dropdown.innerHTML = '<option value="">-- Select District --</option>';

  data.forEach(d => {
    const option = document.createElement("option");
    option.value = d;
    option.text = d;
    dropdown.appendChild(option);
  });
});


function calculate() {
  const district = document.getElementById("districtDropdown").value;
  const resultDiv = document.getElementById("result");
  const status = document.getElementById("status");

  if (!district) {
    alert("Please select a district");
    return;
  }

  status.innerText = "Calculating...";

  fetch(`${API_BASE}/api/admin-mean?district=${encodeURIComponent(district)}`)
  .then(res => res.json())
  .then(data => {

    if (data.error) {
      resultDiv.innerHTML = `<p style="color:red">${data.error}</p>`;
      status.innerText = "Failed";
      return;
    }

    if (!data.output || !String(data.output).trim()) {
      resultDiv.innerHTML = `<p style="color:red">No parameter mean data found for ${district}.</p>`;
      status.innerText = "No data";
      return;
    }

    const formattedOutput = String(data.output)
      .replace(/Mean Precipitation/g, "<b>Mean Precipitation</b>")
      .replace(/Mean Temperature/g, "<b>Mean Temperature</b>")
      .replace(/Mean Streamflow/g, "<b>Mean Streamflow</b>")
      .replace(/Mean Water Level/g, "<b>Mean Water Level</b>")
      .replace(/\n/g, "<br>");

    resultDiv.innerHTML = `
      <div class="result-card">
        <h3>${district}</h3>
        <div class="row">
  ${formattedOutput}
</div>
      </div>
    `;

    status.innerText = "Done";

  })
  .catch(() => {
    resultDiv.innerHTML = `<p style="color:red">Failed to fetch parameter mean climate data.</p>`;
    status.innerText = "Failed";
  });
}