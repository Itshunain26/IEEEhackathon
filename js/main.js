async function loadGraph(){

    let res = await fetch("/api/trends");
    let d = await res.json();

    new Chart(document.getElementById("crimeChart"), {
        type: "bar",
        data: {
            labels: d.labels,
            datasets: [{
                label: "Crimes by State",
                data: d.values
            }]
        }
    });
}

async function loadSummary(){

    let r = await fetch("/api/summary");
    let d = await r.json();

    totalStolen.innerText = d.stolen.toLocaleString();
    totalRecovered.innerText = d.recovered.toLocaleString();
    worstArea.innerText = d.area;
    recoveryRate.innerText = d.rate;
}

loadGraph();
loadSummary();