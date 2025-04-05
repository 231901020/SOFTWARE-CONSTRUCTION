const ctx = document.getElementById('cpuChart').getContext('2d');
const MAX_POINTS = 20;

let datasets = {};
let labels = [];

const cpuChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: []
    },
    options: {
        responsive: true,
        animation: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    generateLabels: (chart) => {
                        return chart.data.datasets.map((ds, i) => {
                            return {
                                text: `${ds.label} (${ds.data[ds.data.length - 1]?.toFixed(1) || 0}%)`,
                                fillStyle: ds.borderColor,
                                strokeStyle: ds.borderColor,
                                lineWidth: 2,
                                index: i
                            };
                        });
                    }
                }
            }
        },
        scales: {
            y: {
                min: 0,
                max: 100,
                title: {
                    display: true,
                    text: "CPU Usage (%)"
                }
            }
        }
    }
});

function getRandomColor() {
    const colors = [
        '#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#2ecc71',
        '#e74c3c', '#3498db', '#9b59b6', '#1abc9c', '#f39c12',
        '#d35400', '#7f8c8d', '#2c3e50', '#8e44ad', '#16a085'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

function updateCPUChart() {
    fetch('/cpu-usage-data')
        .then(res => res.json())
        .then(data => {
            const time = new Date().toLocaleTimeString();
            labels.push(time);
            if (labels.length > MAX_POINTS) labels.shift();

            document.getElementById("cpuPercent").innerText = data.cpu.toFixed(1) + "%";

            data.processes.forEach(proc => {
                const name = proc.name;
                if (!datasets[name]) {
                    datasets[name] = {
                        label: name,
                        data: [],
                        borderColor: getRandomColor(),
                        fill: false,
                        tension: 0.2,
                        pointRadius: 1,
                        pointHoverRadius: 4
                    };
                    cpuChart.data.datasets.push(datasets[name]);
                }

                datasets[name].data.push(proc.cpu);
                if (datasets[name].data.length > MAX_POINTS) {
                    datasets[name].data.shift();
                }
            });

            cpuChart.update();
        });
}

setInterval(updateCPUChart, 1000);
