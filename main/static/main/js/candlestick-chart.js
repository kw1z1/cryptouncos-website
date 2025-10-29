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
        
        // Подготовка данных
        const prices = chartData.map(d => [d.open, d.high, d.low, d.close]);
        const timestamps = chartData.map(d => d.timestamp);
        
        // Создаем датасет для свечей
        const candlestickData = {
            labels: timestamps,
            datasets: [{
                label: 'BTC/USD',
                data: prices,
                type: 'candlestick',
                borderColor: 'rgba(230, 0, 122, 0.8)',
                borderWidth: 1,
                color: {
                    up: '#00ff88',
                    down: '#ff4444',
                    unchanged: '#999999'
                }
            }]
        };

        this.chart = new Chart(ctx, {
            type: 'candlestick',
            data: candlestickData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
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
                                const data = context.raw;
                                return [
                                    `Open: $${data[0].toLocaleString()}`,
                                    `High: $${data[1].toLocaleString()}`,
                                    `Low: $${data[2].toLocaleString()}`,
                                    `Close: $${data[3].toLocaleString()}`
                                ];
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
                            color: '#d5d3d3'
                        }
                    },
                    y: {
                        position: 'right',
                        grid: {
                            color: 'rgba(67, 22, 42, 0.5)'
                        },
                        ticks: {
                            color: '#d5d3d3',
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