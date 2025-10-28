// Bitcoin Chart with Real-time Data
class BitcoinChart {
    constructor() {
        this.chart = null;
        this.currentTimeframe = 1;
        this.init();
    }

    async init() {
        await this.loadChartData();
        this.setupEventListeners();
        this.startRealTimeUpdates();
    }

    async loadChartData() {
        try {
            // Симуляция реальных данных через CoinGecko API
            const response = await fetch(`https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=${this.currentTimeframe}`);
            const data = await response.json();
            
            this.renderChart(data.prices);
            this.updateStats(data);
        } catch (error) {
            console.error('Error loading chart data:', error);
            // Fallback данные
            this.renderFallbackChart();
        }
    }

    renderChart(prices) {
        const ctx = document.getElementById('bitcoinChart').getContext('2d');
        
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = prices.map(([timestamp]) => {
            const date = new Date(timestamp);
            return this.currentTimeframe === 1 ? 
                date.toLocaleTimeString() : 
                date.toLocaleDateString();
        });

        const data = prices.map(([, price]) => price);

        // Индикатор SMA (Simple Moving Average)
        const sma = this.calculateSMA(data, 20);

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'BTC Price',
                        data: data,
                        borderColor: '#ff00ff',
                        backgroundColor: 'rgba(255, 0, 255, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'SMA (20)',
                        data: sma,
                        borderColor: '#00ff88',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff',
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff'
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#cccccc'
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#cccccc',
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

    updateStats(data) {
        const currentPrice = data.prices[data.prices.length - 1][1];
        const previousPrice = data.prices[0][1];
        const change = ((currentPrice - previousPrice) / previousPrice * 100).toFixed(2);

        document.getElementById('currentPrice').textContent = `$${currentPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        document.getElementById('priceChange').textContent = `${change}%`;
        document.getElementById('priceChange').className = `stat-value ${change >= 0 ? 'positive' : 'negative'}`;
    }

    renderFallbackChart() {
        // Fallback данные если API недоступно
        const fallbackData = {
            prices: Array.from({length: 100}, (_, i) => [
                Date.now() - (100 - i) * 3600000,
                40000 + Math.random() * 5000
            ])
        };
        this.renderChart(fallbackData.prices);
    }

    setupEventListeners() {
        document.querySelectorAll('.timeframe-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.timeframe-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentTimeframe = parseInt(e.target.dataset.timeframe);
                this.loadChartData();
            });
        });
    }

    startRealTimeUpdates() {
        // Обновляем каждые 30 секунд
        setInterval(() => {
            this.loadChartData();
        }, 30000);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new BitcoinChart();
});