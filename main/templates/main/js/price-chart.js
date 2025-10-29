// Bitcoin Price Chart with Indicators
class BitcoinPriceChart {
    constructor() {
        this.chart = null;
        this.init();
    }

    init() {
        this.renderChart();
        this.setupEventListeners();
    }

    renderChart() {
        const ctx = document.getElementById('priceChart').getContext('2d');
        
        // Подготовка данных
        const prices = chartData.map(d => d.c);
        const timestamps = chartData.map(d => new Date(d.x));
        
        // Создаем цвет для каждой точки на основе движения цены
        const pointBackgroundColors = prices.map((price, index) => {
            if (index === 0) return '#e6007a';
            return price > prices[index - 1] ? '#00ff88' : '#ff4444';
        });

        const pointBorderColors = prices.map((price, index) => {
            if (index === 0) return '#e6007a';
            return price > prices[index - 1] ? '#00ff88' : '#ff4444';
        });

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: timestamps,
                datasets: [
                    {
                        label: 'BTC Price',
                        data: prices,
                        borderColor: '#e6007a',
                        backgroundColor: 'rgba(230, 0, 122, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: pointBackgroundColors,
                        pointBorderColor: pointBorderColors,
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'SMA 20',
                        data: this.calculateSMA(prices, 20),
                        borderColor: '#00ff88',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        pointRadius: 0,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff',
                            font: {
                                family: 'Space Mono, monospace',
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(13, 2, 8, 0.95)',
                        borderColor: '#e6007a',
                        borderWidth: 1,
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('en-US', {
                                        style: 'currency',
                                        currency: 'USD'
                                    }).format(context.parsed.y);
                                }
                                return label;
                            },
                            title: function(tooltipItems) {
                                const date = new Date(tooltipItems[0].parsed.x);
                                return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            displayFormats: {
                                day: 'MMM d'
                            }
                        },
                        grid: {
                            color: 'rgba(67, 22, 42, 0.5)',
                            borderColor: '#43162a'
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
                            color: 'rgba(67, 22, 42, 0.5)',
                            borderColor: '#43162a'
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

    calculateSMA(data, period) {
        const sma = [];
        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                sma.push(null);
            } else {
                const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                sma.push(sum / period);
            }
        }
        return sma;
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            window.location.reload();
        });

        // Auto-refresh every 30 seconds
        setInterval(() => {
            this.updateChart();
        }, 30000);
    }

    async updateChart() {
        try {
            const response = await fetch(window.location.href);
            const text = await response.text();
            
            // Здесь можно обновить данные графика
            // Для простоты просто перезагружаем страницу
            console.log('Chart data updated');
        } catch (error) {
            console.error('Error updating chart:', error);
        }
    }
}

// Initialize chart when page loads
document.addEventListener('DOMContentLoaded', () => {
    new BitcoinPriceChart();
});