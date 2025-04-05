const ctx = document.getElementById("cpuChart").getContext("2d");
let cpuChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "CPU Usage (%)",
            data: [],
            borderColor: "rgb(75, 192, 192)",
            tension: 0.1,
            fill: true,
        }]
    },
    options: {
        responsive: true,
        animation: false,
        scales: {
            y: {
                min: 0,
                max: 100
            }
        }
    }
});

function updateCPUChart() {
    fetch("/cpu-usage-data")
        .then(res => res.json())
        .then(data => {
            const currentTime = new Date().toLocaleTimeString();
            if (cpuChart.data.labels.length > 20) {
                cpuChart.data.labels.shift();
                cpuChart.data.datasets[0].data.shift();
            }
            cpuChart.data.labels.push(currentTime);
            cpuChart.data.datasets[0].data.push(data.cpu);
            document.getElementById("cpuPercent").innerText = data.cpu + "%";
            cpuChart.update();
        });
}

setInterval(updateCPUChart, 1000);
