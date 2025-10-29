// Professional Candlestick Chart with Indicators
class CandlestickChart {
    constructor() {
        this.chart = null;
        this.init();
    }

    init() {
        this.renderChart();
        this.setupEventListeners();
    }

    renderChart() {
        const ctx = document.getElementById('candlestickChart').getContext('2d');
        
        // Подготовка данных для обычного линейного графика (временно)
        const prices = chartData.map(d => d.close);
        const timestamps = chartData.map(d => d.timestamp);
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: timestamps,
                datasets: [{
                    label: 'BTC/USD',
                    data: prices,
                    borderColor: '#e6007a',
                    backgroundColor: 'rgba(230, 0, 122, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff',
                            font: {
                                family: 'Space Mono, monospace'
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(13, 2, 8, 0.9)',
                        borderColor: '#e6007a',
                        borderWidth: 1,
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        callbacks: {
                            label: function(context) {
                                return `Price: $${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        grid: {
                            color: 'rgba(67, 22, 42, 0.5)'
                        },
                        ticks: {
                            color: '#d5d3d3',
                            font: {
                                family: 'Space Mono, monospace'
                            }
                        }
                    },
                    y: {
                        position: 'right',
                        grid: {
                            color: 'rgba(67, 22, 42, 0.5)'
                        },
                        ticks: {
                            color: '#d5d3d3',
                            font: {
                                family: 'Space Mono, monospace'
                            },
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Fullscreen functionality
        document.getElementById('fullscreenBtn').addEventListener('click', () => {
            const chartContainer = document.querySelector('.chart-container');
            chartContainer.classList.toggle('fullscreen');
        });
    }
}

// Initialize chart when page loads
document.addEventListener('DOMContentLoaded', () => {
    new CandlestickChart();
});