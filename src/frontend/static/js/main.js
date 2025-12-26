/**
 * ML Inference Dashboard - Main Application Logic
 */

// DOM element references
const elements = {
    // Header / Experiment info
    experimentName: document.getElementById('experiment_name'),
    experimentSubtitle: document.getElementById('experiment_subtitle'),
    badgeBackend: document.getElementById('badge_backend'),
    badgeDevice: document.getElementById('badge_device'),

    // Status
    status: document.getElementById('status'),

    // Main metrics
    queryCount: document.getElementById('query_count'),
    latencyMs: document.getElementById('instant_latency_ms'),
    queueWaitMs: document.getElementById('queue_wait_ms'),
    tokenizeMs: document.getElementById('tokenize_ms'),
    inferenceMs: document.getElementById('inference_ms'),
    throughputQps: document.getElementById('throughput_qps'),

    // Padding analysis
    paddingPct: document.getElementById('padding_pct'),
    maxSeqLen: document.getElementById('max_seq_len'),
    avgSeqLen: document.getElementById('avg_seq_len'),
    queueWaitP95: document.getElementById('queue_wait_p95'),

    // Stage percentages
    pctTokenize: document.getElementById('pct_tokenize'),
    pctQueueWait: document.getElementById('pct_queue_wait'),
    pctInference: document.getElementById('pct_inference'),
    pctOther: document.getElementById('pct_other'),

    // Stage bar segments
    barTokenize: document.getElementById('bar_tokenize'),
    barQueueWait: document.getElementById('bar_queue_wait'),
    barInference: document.getElementById('bar_inference'),
    barOther: document.getElementById('bar_other'),

    // P95 stats
    tokenizeP95: document.getElementById('tokenize_p95'),
    queueWaitP95Breakdown: document.getElementById('queue_wait_p95_breakdown'),
    inferenceP95: document.getElementById('inference_p95'),
    totalP95: document.getElementById('total_p95'),

    // Chart live values
    latencyLive: document.getElementById('latency_live'),
    throughputLive: document.getElementById('throughput_live'),
    queueLive: document.getElementById('queue_live'),
    tokenizeLive: document.getElementById('tokenize_live'),
    inferenceLive: document.getElementById('inference_live'),
    cpuLive: document.getElementById('cpu_live'),
    gpuLive: document.getElementById('gpu_live'),
    queriesLive: document.getElementById('queries_live'),
    paddingLive: document.getElementById('padding_live'),
    utilizationLive: document.getElementById('utilization_live'),

    // Instance metrics section
    instanceSectionTitle: document.getElementById('instance_section_title'),
    instanceMetrics: document.getElementById('instance_metrics'),

    // Per-worker stats section
    workerStatsTitle: document.getElementById('worker_stats_title'),
    workerStatsSection: document.getElementById('worker_stats_section')
};

// Format number with fixed decimals
function fmt(value, decimals = 1) {
    return (value || 0).toFixed(decimals);
}

// Update experiment info in header
function updateExperimentInfo(data) {
    const name = data.experiment_name || 'ML Inference Dashboard';
    const description = data.experiment_description || 'Real-time Stage Breakdown';
    const backend = data.backend_type || 'pytorch';
    const device = data.device || 'cpu';

    if (elements.experimentName) {
        elements.experimentName.textContent = name || 'ML Inference Dashboard';
    }
    if (elements.experimentSubtitle) {
        elements.experimentSubtitle.textContent = description || 'Real-time Stage Breakdown';
    }
    if (elements.badgeBackend) {
        elements.badgeBackend.textContent = backend.toUpperCase();
    }
    if (elements.badgeDevice) {
        elements.badgeDevice.textContent = device.toUpperCase();
    }
}

// Update status badge
function updateStatus(isRunning) {
    if (isRunning) {
        elements.status.textContent = 'Running';
        elements.status.className = 'status running';
    } else {
        elements.status.textContent = 'Idle';
        elements.status.className = 'status idle';
    }
}

// Update main metrics cards
function updateMetrics(data) {
    elements.queryCount.textContent = data.query_count || 0;
    elements.latencyMs.textContent = fmt(data.instant_latency_ms || data.avg_ms);
    elements.queueWaitMs.textContent = fmt(data.last_queue_wait_ms);
    elements.tokenizeMs.textContent = fmt(data.last_tokenize_ms);
    elements.inferenceMs.textContent = fmt(data.last_inference_ms);
    elements.throughputQps.textContent = fmt(data.throughput_qps);

    // Padding analysis
    const padding = data.padding_analysis || {};
    elements.paddingPct.textContent = fmt(padding.last_padding_pct || padding.avg_padding_pct);
    elements.maxSeqLen.textContent = padding.last_max_seq_length || 0;
    elements.avgSeqLen.textContent = fmt(padding.last_avg_seq_length || padding.avg_avg_seq_length);

    // Queue wait P95
    const queueWait = data.queue_wait_analysis || {};
    elements.queueWaitP95.textContent = fmt(queueWait.p95_ms);
}

// Update stage breakdown bar and percentages
function updateStageBreakdown(data) {
    const stagePct = data.stage_percentages || {};
    const pctTokenize = stagePct.tokenize_pct || 0;
    const pctQueueWait = stagePct.queue_wait_pct || 0;
    const pctInference = stagePct.inference_pct || 0;
    const pctOther = stagePct.other_pct || 100;

    // Update percentage text
    elements.pctTokenize.textContent = fmt(pctTokenize, 0);
    elements.pctQueueWait.textContent = fmt(pctQueueWait, 0);
    elements.pctInference.textContent = fmt(pctInference, 0);
    elements.pctOther.textContent = fmt(pctOther, 0);

    // Update bar widths
    elements.barTokenize.style.width = pctTokenize + '%';
    elements.barTokenize.textContent = pctTokenize > 8 ? fmt(pctTokenize, 0) + '%' : '';

    elements.barQueueWait.style.width = pctQueueWait + '%';
    elements.barQueueWait.textContent = pctQueueWait > 8 ? fmt(pctQueueWait, 0) + '%' : '';

    elements.barInference.style.width = pctInference + '%';
    elements.barInference.textContent = pctInference > 8 ? fmt(pctInference, 0) + '%' : '';

    elements.barOther.style.width = pctOther + '%';
    elements.barOther.textContent = pctOther > 8 ? fmt(pctOther, 0) + '%' : '';
}

// Update P95 statistics
function updateP95Stats(data) {
    const stageBreakdown = data.stage_breakdown || {};
    const tokenizeStats = stageBreakdown.tokenize || {};
    const queueWaitStats = stageBreakdown.queue_wait || {};
    const inferenceStats = stageBreakdown.model_inference || {};

    // Safely access p95_ms with fallback to 0 if undefined
    const tokenizeP95 = tokenizeStats.p95_ms !== undefined ? tokenizeStats.p95_ms : 0;
    const queueWaitP95 = queueWaitStats.p95_ms !== undefined ? queueWaitStats.p95_ms : 0;
    const inferenceP95 = inferenceStats.p95_ms !== undefined ? inferenceStats.p95_ms : 0;
    const totalP95 = data.p95_ms !== undefined ? data.p95_ms : 0;

    elements.tokenizeP95.textContent = fmt(tokenizeP95) + ' ms';
    elements.queueWaitP95Breakdown.textContent = fmt(queueWaitP95) + ' ms';
    elements.inferenceP95.textContent = fmt(inferenceP95) + ' ms';
    elements.totalP95.textContent = fmt(totalP95) + ' ms';
}

// Update chart live values
function updateChartValues(data) {
    elements.latencyLive.textContent = fmt(data.instant_latency_ms || data.avg_ms) + ' ms';
    elements.throughputLive.textContent = fmt(data.throughput_qps) + ' q/s';
    elements.queueLive.textContent = fmt(data.last_queue_wait_ms) + ' ms';
    elements.tokenizeLive.textContent = fmt(data.last_tokenize_ms) + ' ms';
    elements.inferenceLive.textContent = fmt(data.last_inference_ms) + ' ms';
    elements.cpuLive.textContent = fmt(data.cpu_percent, 0) + '%';
    elements.gpuLive.textContent = fmt(data.gpu_memory_mb, 0) + ' MB';
    elements.queriesLive.textContent = data.query_count || 0;

    // Padding live value
    const padding = data.padding_analysis || {};
    elements.paddingLive.textContent = fmt(padding.last_padding_pct || padding.avg_padding_pct) + '%';

    // Utilization live value (average across instances)
    const instanceMetrics = data.instance_metrics || {};
    elements.utilizationLive.textContent = fmt(instanceMetrics.avg_utilization_pct || 0) + '%';
}

// Update per-instance metrics cards
function updateInstanceMetrics(data) {
    const instanceMetrics = data.instance_metrics || {};
    const instances = instanceMetrics.instances || [];

    if (instances.length <= 1) {
        elements.instanceSectionTitle.style.display = 'none';
        elements.instanceMetrics.style.display = 'none';
        return;
    }

    elements.instanceSectionTitle.style.display = 'block';
    elements.instanceMetrics.style.display = 'grid';

    // Build HTML for instance cards
    const cardsHtml = instances.map((inst, i) => {
        const color = getInstanceColor(i);
        const busyClass = inst.is_busy ? 'busy' : 'idle';
        return `
            <div class="metric-card instance-card" style="border-color: ${color}">
                <div class="metric-label">${inst.name}</div>
                <div class="metric-value" style="color: ${color}">${fmt(inst.utilization_pct)}%</div>
                <div class="metric-unit">utilization</div>
                <div class="instance-stats">
                    <span class="stat">${inst.request_count} reqs</span>
                    <span class="stat ${busyClass}">${inst.is_busy ? '⚡ busy' : '💤 idle'}</span>
                </div>
            </div>
        `;
    }).join('');

    elements.instanceMetrics.innerHTML = cardsHtml;
}

// Get color for instance by index
function getInstanceColor(index) {
    const colors = ['#58a6ff', '#3fb950', '#f0883e', '#a371f7', '#f85149', '#56d4dd', '#db61a2', '#e3b341'];
    return colors[index % colors.length];
}

// Update per-worker/per-model statistics
function updateWorkerStats(data) {
    const workerStats = data.worker_stats || [];

    if (workerStats.length === 0) {
        elements.workerStatsTitle.style.display = 'none';
        elements.workerStatsSection.style.display = 'none';
        return;
    }

    elements.workerStatsTitle.style.display = 'block';
    elements.workerStatsSection.style.display = 'grid';

    // Build HTML for worker stat cards
    const cardsHtml = workerStats.map((ws, i) => {
        const color = getInstanceColor(i);
        return `
            <div class="worker-card" style="border-color: ${color}">
                <div class="worker-title">
                    <span class="worker-id" style="color: ${color}">Worker ${ws.worker_id}</span>
                </div>
                <div class="worker-metrics">
                    <div class="worker-metric">
                        <div class="worker-metric-label">Avg Latency</div>
                        <div class="worker-metric-value">${fmt(ws.avg_ms)} ms</div>
                    </div>
                    <div class="worker-metric">
                        <div class="worker-metric-label">P95 Latency</div>
                        <div class="worker-metric-value">${fmt(ws.p95_ms)} ms</div>
                    </div>
                    <div class="worker-metric">
                        <div class="worker-metric-label">Throughput</div>
                        <div class="worker-metric-value">${fmt(ws.throughput_qps)} q/s</div>
                    </div>
                    <div class="worker-metric">
                        <div class="worker-metric-label">Queries</div>
                        <div class="worker-metric-value">${ws.query_count}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    elements.workerStatsSection.innerHTML = cardsHtml;
}

// Fetch metrics and update dashboard
async function fetchAndUpdate() {
    try {
        const response = await fetch('/metrics');
        const data = await response.json();

        updateExperimentInfo(data);
        updateStatus(data.is_running);
        updateMetrics(data);
        updateStageBreakdown(data);
        updateP95Stats(data);
        updateChartValues(data);
        updateInstanceMetrics(data);
        updateWorkerStats(data);

        if (data.history) {
            window.DashboardCharts.updateAll(data.history);
        }
    } catch (error) {
        elements.status.textContent = 'Disconnected';
        elements.status.className = 'status';
        console.error('Failed to fetch metrics:', error);
    }
}

// Initialize dashboard
function init() {
    window.DashboardCharts.init();
    fetchAndUpdate();
    setInterval(fetchAndUpdate, 500);
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
