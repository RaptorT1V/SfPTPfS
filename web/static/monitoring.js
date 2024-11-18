let chart;
let ws;

async function loadUnits() {
    try {
        const response = await fetch("/units");
        const data = await response.json();
        const unitSelect = document.getElementById("unit");
        data.units.forEach(unit => {
            const option = document.createElement("option");
            option.value = unit;
            option.textContent = unit;
            unitSelect.appendChild(option);
        });
        loadParameters();
    } catch (error) {
        console.error("Error loading units:", error);
    }
}

async function loadParameters() {
    const unit = document.getElementById("unit").value;
    try {
        const response = await fetch(`/parameters/${unit}`);
        const data = await response.json();
        const parameterSelect = document.getElementById("parameter");
        parameterSelect.innerHTML = "";
        data.parameters.forEach(param => {
            const option = document.createElement("option");
            option.value = param;
            option.textContent = param;
            parameterSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading parameters:", error);
    }
}

function startRealtimeGraph() {
    if (ws) {
        ws.close();
    }

    const unit = document.getElementById("unit").value;
    const parameter = document.getElementById("parameter").value;
    const ctx = document.getElementById("realtimeChart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: `${unit} - ${parameter}`,
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        }
    });

    ws = new WebSocket(`ws://${window.location.host}/ws/${unit}/${parameter}`);
    ws.onmessage = (event) => {
        const { time, value } = JSON.parse(event.data);

        chart.data.labels.push(time);
        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        chart.update();
    };

    ws.onclose = () => console.log("WebSocket closed");
}

window.onload = loadUnits;
