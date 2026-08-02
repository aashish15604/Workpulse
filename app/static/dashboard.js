async function fetchJSON(url) {
  const res = await fetch(url);
  return res.json();
}

function renderOverviewCards(overview) {
  const cards = [
    { label: "Total Tasks", value: overview.total_tasks },
    { label: "Completed", value: overview.completed },
    { label: "In Progress", value: overview.in_progress },
    { label: "Overdue", value: overview.overdue },
    { label: "Completion Rate", value: `${overview.completion_rate}%` },
  ];
  const container = document.getElementById("overview-cards");
  container.innerHTML = cards
    .map(c => `<div class="card"><div class="label">${c.label}</div><div class="value">${c.value}</div></div>`)
    .join("");
}

function renderEmployeeTable(employeeMetrics) {
  const rows = employeeMetrics.map(e => `
    <tr>
      <td>${e.name}</td>
      <td><span class="status-pill status-${e.status}">${e.status}</span></td>
      <td>${e.total_assigned}</td>
      <td>${e.completed}</td>
      <td>${e.overdue}</td>
      <td>${e.completion_rate}%</td>
    </tr>`).join("");
  document.querySelector("#employeeTable tbody").innerHTML = rows;
}

async function loadDashboard() {
  const overview = await fetchJSON("/api/metrics/overview");
  const employeeMetrics = await fetchJSON("/api/metrics/employees");
  renderOverviewCards(overview);
  renderEmployeeTable(employeeMetrics);
}

loadDashboard();
setInterval(loadDashboard, 15000);