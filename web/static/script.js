async function toggleGenerator() {
    const generatorStatus = document.getElementById('generatorStatus');
    const isRunning = generatorStatus.classList.contains('active');
    const endpoint = isRunning ? 'stop' : 'start';

    try {
        const response = await fetch(`/generator/${endpoint}`, { method: 'POST' });
        if (response.ok) {
            if (isRunning) {
                generatorStatus.textContent = 'Generator is sleeping';
                generatorStatus.classList.remove('active');
                generatorStatus.classList.add('sleeping');
                document.getElementById('generatorToggle').textContent = 'Start generator';
            } else {
                generatorStatus.textContent = 'Generator is active';
                generatorStatus.classList.remove('sleeping');
                generatorStatus.classList.add('active');
                document.getElementById('generatorToggle').textContent = 'Stop generator';
            }
        }
    } catch (error) {
        alert('Ошибка соединения с сервером');
    }
}

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

function showModal(graphData) {
    document.getElementById('modalGraph').innerHTML = graphData;
    document.getElementById('graphModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('graphModal').style.display = 'none';
}

function validateTimestampInput(input) {
    const timestampRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$/;
    return timestampRegex.test(input);
}

async function fetchGraph() {
    const unit = document.getElementById("unit").value;
    const parameter = document.getElementById("parameter").value;
    const startTime = document.getElementById("start_time").value.replace(' ', 'T');
    const endTime = document.getElementById("end_time").value.replace(' ', 'T');

    if (!validateTimestampInput(startTime) || !validateTimestampInput(endTime)) {
        alert("Неверный формат даты и времени. Используйте формат YYYY-MM-DDTHH:MM:SS");
        return;
    }

    try {
        const response = await fetch(`/plot/${unit}/${parameter}?start_time=${startTime}&end_time=${endTime}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail);
        }
        const svgContent = await response.text();
        showModal(svgContent);
    } catch (error) {
        alert(`Ошибка: ${error.message}`);
        console.error('Console error! Error fetching graph:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#start_time", {
        enableTime: true,
        enableSeconds: true,
        time_24hr: true,
        dateFormat: "Y-m-d H:i:S",
        seconds: true
    });

    flatpickr("#end_time", {
        enableTime: true,
        enableSeconds: true,
        time_24hr: true,
        dateFormat: "Y-m-d H:i:S",
        seconds: true
    });
});

document.getElementById("unit").addEventListener("change", loadParameters);
window.onload = loadUnits;