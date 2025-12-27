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

// Instance charts container (for multi-model)
const instanceCharts = [];

// Instance colors for multi-model charts
const INSTANCE_COLORS = [
    { line: '#58a6ff', fill: 'rgba(88,166,255,0.15)' },   // blue
    { line: '#3fb950', fill: 'rgba(63,185,80,0.15)' },    // green
    { line: '#f0883e', fill: 'rgba(240,136,62,0.15)' },   // orange
    { line: '#a371f7', fill: 'rgba(163,113,247,0.15)' },  // purple
    { line: '#f85149', fill: 'rgba(248,81,73,0.15)' },    // red
    { line: '#56d4dd', fill: 'rgba(86,212,221,0.15)' },   // cyan
    { line: '#db61a2', fill: 'rgba(219,97,162,0.15)' },   // pink
    { line: '#e3b341', fill: 'rgba(227,179,65,0.15)' },   // yellow
];

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
    charts.queue = new Chart(
        document.getElementById('queueChart'),
        createChartConfig(COLORS.orange)
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
        createChartConfig(COLORS.gray)
    );
    charts.gpu = new Chart(
        document.getElementById('gpuChart'),
        createChartConfig(COLORS.purple)
    );
    charts.queries = new Chart(
        document.getElementById('queriesChart'),
        createChartConfig(COLORS.gray)
    );
    charts.padding = new Chart(
        document.getElementById('paddingChart'),
        createChartConfig(COLORS.purple)
    );
    charts.utilization = new Chart(
        document.getElementById('utilizationChart'),
        createChartConfig(COLORS.green)
    );
    charts.overhead = new Chart(
        document.getElementById('overheadChart'),
        createChartConfig(COLORS.orange)
    );
}

// Create multi-line chart config for instance utilization
function createMultiLineChartConfig(instanceNames) {
    const datasets = instanceNames.map((name, i) => ({
        label: name,
        data: [],
        borderColor: INSTANCE_COLORS[i % INSTANCE_COLORS.length].line,
        backgroundColor: INSTANCE_COLORS[i % INSTANCE_COLORS.length].fill,
        fill: false,
        tension: 0.3,
        pointRadius: 0,
        borderWidth: 2
    }));

    return {
        type: 'line',
        data: {
            labels: [],
            datasets: datasets
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
                        maxTicksLimit: 8
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
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: '%',
                        color: '#6e7681',
                        font: { size: 9 }
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#8b949e',
                        boxWidth: 12,
                        padding: 8,
                        font: { size: 10 }
                    }
                },
                tooltip: {
                    backgroundColor: '#161b22',
                    titleColor: '#c9d1d9',
                    bodyColor: '#8b949e',
                    borderColor: '#30363d',
                    borderWidth: 1,
                    padding: 8
                }
            }
        }
    };
}

// Initialize or update instance charts dynamically
function initInstanceCharts(instanceNames) {
    const container = document.getElementById('instance_charts');
    const title = document.getElementById('instance_charts_title');

    if (!instanceNames || instanceNames.length <= 1) {
        container.style.display = 'none';
        title.style.display = 'none';
        return;
    }

    container.style.display = 'grid';
    title.style.display = 'block';

    // Only create charts once
    if (instanceCharts.length === 0) {
        // Create utilization chart for all instances
        container.innerHTML = `
            <div class="chart-container full-width">
                <div class="chart-header">
                    <span class="chart-title">Instance Utilization Over Time</span>
                </div>
                <div class="chart-wrapper" style="height: 180px;">
                    <canvas id="instanceUtilChart"></canvas>
                </div>
            </div>
            <div class="chart-container full-width">
                <div class="chart-header">
                    <span class="chart-title">Instance Idle Time Over Time</span>
                </div>
                <div class="chart-wrapper" style="height: 180px;">
                    <canvas id="instanceIdleChart"></canvas>
                </div>
            </div>
        `;

        // Create multi-line chart for utilization
        instanceCharts.push(new Chart(
            document.getElementById('instanceUtilChart'),
            createMultiLineChartConfig(instanceNames)
        ));

        // Create multi-line chart for idle time
        instanceCharts.push(new Chart(
            document.getElementById('instanceIdleChart'),
            createMultiLineChartConfig(instanceNames)
        ));
    }
}

// Update a single chart
function updateChart(chart, labels, data) {
    if (!chart || !data) return;
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update('none');
}

// Update multi-line chart with per-instance data
function updateMultiLineChart(chart, labels, dataArrays) {
    if (!chart || !dataArrays || dataArrays.length === 0) return;

    chart.data.labels = labels;

    // dataArrays is array of [time1, time2, ...] where each timeN is [inst0, inst1, ...]
    // We need to transpose to [inst0_values, inst1_values, ...]
    const numInstances = chart.data.datasets.length;

    for (let i = 0; i < numInstances; i++) {
        chart.data.datasets[i].data = dataArrays.map(timePoint =>
            timePoint && timePoint[i] !== undefined ? timePoint[i] : 0
        );
    }

    chart.update('none');
}

// Update all charts with history data
function updateAllCharts(history) {
    if (!history) return;

    const labels = (history.timestamps || []).map(t => t.toFixed(0) + 's');

    updateChart(charts.latency, labels, history.latencies);
    updateChart(charts.throughput, labels, history.throughput);
    updateChart(charts.queue, labels, history.queue_wait_ms);
    updateChart(charts.tokenize, labels, history.tokenize_ms);
    updateChart(charts.inference, labels, history.inference_ms);
    updateChart(charts.cpu, labels, history.cpu_percent);
    updateChart(charts.gpu, labels, history.gpu_memory_mb);
    updateChart(charts.queries, labels, history.queries);
    updateChart(charts.padding, labels, history.padding_pct);
    updateChart(charts.utilization, labels, history.gpu_utilization_pct);
    updateChart(charts.overhead, labels, history.overhead_ms || []);

    // Update per-instance charts if available
    if (history.instance_names && history.instance_names.length > 1) {
        initInstanceCharts(history.instance_names);

        if (instanceCharts.length >= 2 && history.instance_utilization) {
            updateMultiLineChart(instanceCharts[0], labels, history.instance_utilization);
            updateMultiLineChart(instanceCharts[1], labels, history.instance_idle);
        }
    }
}

// Export for use in main.js
window.DashboardCharts = {
    init: initCharts,
    updateAll: updateAllCharts,
    charts: charts,
    instanceCharts: instanceCharts,
    initInstanceCharts: initInstanceCharts
};
