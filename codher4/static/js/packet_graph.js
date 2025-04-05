const ctx = document.getElementById('graph').getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'TCP',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                fill: false
            },
            {
                label: 'UDP',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                fill: false
            },
            {
                label: 'ICMP',
                data: [],
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 2,
                fill: false
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function updateChart() {
    fetch('/graph-data')
        .then(response => response.json())
        .then(data => {
            const timeLabel = new Date().toLocaleTimeString();

            chart.data.labels.push(timeLabel);
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
            }

            chart.data.datasets[0].data.push(data.TCP);
            chart.data.datasets[1].data.push(data.UDP);
            chart.data.datasets[2].data.push(data.ICMP);

            // Keep data length in sync
            chart.data.datasets.forEach(ds => {
                if (ds.data.length > 20) ds.data.shift();
            });

            chart.update();
        })
        .catch(error => {
            console.error('Error fetching graph data:', error);
        });
}

// Refresh every 2 seconds
setInterval(updateChart, 2000);
