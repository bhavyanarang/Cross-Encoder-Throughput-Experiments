/**
 * ML Inference Dashboard - Chart Configuration and Utilities
 */

// Chart color scheme matching GitHub Dark theme
const COLORS = {
    blue: { line: '#58a6ff', fill: 'rgba(88,166,255,0.08)' },
    green: { line: '#3fb950', fill: 'rgba(63,185,80,0.08)' },
    red: { line: '#f85149', fill: 'rgba(248,81,73,0.08)' },
    orange: { line: '#f0883e', fill: 'rgba(240,136,62,0.08)' },
    purple: { line: '#a371f7', fill: 'rgba(163,113,247,0.08)' },
    gray: { line: '#8b949e', fill: 'rgba(139,148,158,0.08)' }
};

// Base chart configuration
function createChartConfig(color) {
    return {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                data: [],
                borderColor: color.line,
                backgroundColor: color.fill,
                fill: true,
                tension: 0.3,
                pointRadius: 0,
                borderWidth: 1.5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 0 },
            interaction: {
                intersect: false,
                mode: 'index'
            },
            scales: {
                x: {
                    display: true,
                    grid: { 
                        color: 'rgba(110,118,129,0.08)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6e7681',
                        font: { size: 9 },
                        maxTicksLimit: 8,
                        callback: function(value, index) {
                            const labels = this.chart.data.labels;
                            if (labels.length > 12) {
                                return index % Math.ceil(labels.length / 8) === 0 ? labels[index] : '';
                            }
                            return labels[index];
                        }
                    }
                },
                y: {
                    display: true,
                    grid: { 
                        color: 'rgba(110,118,129,0.08)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6e7681',
                        font: { size: 9 },
                        maxTicksLimit: 5
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#161b22',
                    titleColor: '#c9d1d9',
                    bodyColor: '#8b949e',
                    borderColor: '#30363d',
                    borderWidth: 1,
                    padding: 8,
                    displayColors: false
                }
            }
        }
    };
}

// Chart instances container
const charts = {};

// Initialize all charts
function initCharts() {
    charts.latency = new Chart(
        document.getElementById('latencyChart'),
        createChartConfig(COLORS.blue)
    );
    charts.throughput = new Chart(
        document.getElementById('throughputChart'),
        createChartConfig(COLORS.blue)
    );
    charts.tokenize = new Chart(
        document.getElementById('tokenizeChart'),
        createChartConfig(COLORS.red)
    );
    charts.inference = new Chart(
        document.getElementById('inferenceChart'),
        createChartConfig(COLORS.green)
    );
    charts.cpu = new Chart(
        document.getElementById('cpuChart'),
        createChartConfig(COLORS.orange)
    );
    charts.gpu = new Chart(
        document.getElementById('gpuChart'),
        createChartConfig(COLORS.purple)
    );
    charts.queries = new Chart(
        document.getElementById('queriesChart'),
        createChartConfig(COLORS.gray)
    );
}

// Update a single chart
function updateChart(chart, labels, data) {
    if (!chart || !data) return;
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update('none');
}

// Update all charts with history data
function updateAllCharts(history) {
    if (!history) return;
    
    const labels = (history.timestamps || []).map(t => t.toFixed(0) + 's');
    
    updateChart(charts.latency, labels, history.latencies);
    updateChart(charts.throughput, labels, history.throughput);
    updateChart(charts.tokenize, labels, history.tokenize_ms);
    updateChart(charts.inference, labels, history.inference_ms);
    updateChart(charts.cpu, labels, history.cpu_percent);
    updateChart(charts.gpu, labels, history.gpu_memory_mb);
    updateChart(charts.queries, labels, history.queries);
}

// Export for use in main.js
window.DashboardCharts = {
    init: initCharts,
    updateAll: updateAllCharts,
    charts: charts
};

