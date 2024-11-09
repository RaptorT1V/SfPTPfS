// Загрузка агрегатов
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
    } catch (error) {
        console.error("Error loading units:", error);
    }
}

// Загрузка параметров
async function loadParameters() {
    const unit = document.getElementById("unit").value;
    try {
        const response = await fetch(`/parameters/${unit}`);
        const data = await response.json();
        const parameterSelect = document.getElementById("parameter");

        parameterSelect.innerHTML = "";
        data.parameters.forEach(parameter => {
            const option = document.createElement("option");
            option.value = parameter;
            option.textContent = parameter;
            parameterSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading parameters:", error);
    }
}

async function fetchGraph() {
    const unit = document.getElementById("unit").value;
    const parameter = document.getElementById("parameter").value;
    const startTime = document.getElementById("start_time").value;
    const endTime = document.getElementById("end_time").value;

    try {
        const response = await fetch(`/plot/${unit}/${parameter}?start_time=${startTime}&end_time=${endTime}`);
        if (!response.ok) {
            throw new Error(`Failed to generate plot. Error: ${response.statusText}`);
        }

        const svgContent = await response.text(); // Получаем SVG-код
        document.getElementById("graph").innerHTML = svgContent; // Вставляем SVG прямо в HTML
    } catch (error) {
        console.error('Error fetching graph:', error);
        alert("Error generating graph.");
        document.getElementById("graph").innerHTML = `<p>Error loading graph.</p>`;
    }
}

document.getElementById("unit").addEventListener("change", loadParameters);
window.onload = loadUnits;