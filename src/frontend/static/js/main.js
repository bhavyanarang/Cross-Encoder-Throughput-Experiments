/**
 * ML Inference Dashboard - Main Application Logic
 */

// DOM element cache for performance
const elCache = {};

// Helper function to safely update DOM elements with caching
function updateEl(id, value, decimals = 1) {
    if (!elCache[id]) {
        elCache[id] = document.getElementById(id);
    }
    const el = elCache[id];
    if (el) {
        if (typeof value === 'number') {
            el.textContent = value.toFixed(decimals);
        } else {
            el.textContent = value || 0;
        }
    }
}

// Format number with fixed decimals (max 2 decimal places)
function fmt(value, decimals = 2) {
    if (typeof value !== 'number') value = 0;
    return value.toFixed(Math.min(decimals, 2));
}

// DOM element references - will be initialized after DOM is ready
let elements = {};

// Initialize DOM element references
function initElements() {
    elements = {
        experimentName: document.getElementById('experiment_name'),
        experimentSubtitle: document.getElementById('experiment_subtitle'),
        badgeBackend: document.getElementById('badge_backend'),
        badgeDevice: document.getElementById('badge_device'),
        status: document.getElementById('status'),
        queryCount: document.getElementById('query_count'),
        latencyMs: document.getElementById('instant_latency_ms'),
        throughputQps: document.getElementById('throughput_qps'),
        tokenizeMs: document.getElementById('tokenize_ms'),
        tokenizerQueueWaitMs: document.getElementById('tokenizer_queue_wait_ms'),
        modelQueueWaitMs: document.getElementById('model_queue_wait_ms'),
        tokenizerQueueSize: document.getElementById('tokenizer_queue_size'),
        modelQueueSize: document.getElementById('model_queue_size'),
        inferenceMs: document.getElementById('inference_ms'),
        overheadMs: document.getElementById('overhead_ms'),
        paddingPct: document.getElementById('padding_pct'),
        maxSeqLen: document.getElementById('max_seq_len'),
        avgSeqLen: document.getElementById('avg_seq_len'),
        pctTokenize: document.getElementById('pct_tokenize'),
        pctTokenizerQueueWait: document.getElementById('pct_tokenizer_queue_wait'),
        pctModelQueueWait: document.getElementById('pct_model_queue_wait'),
        pctQueueWait: document.getElementById('pct_queue_wait'),
        pctInference: document.getElementById('pct_inference'),
        pctOverhead: document.getElementById('pct_overhead'),
        barTokenize: document.getElementById('bar_tokenize'),
        barTokenizerQueueWait: document.getElementById('bar_tokenizer_queue_wait'),
        barModelQueueWait: document.getElementById('bar_model_queue_wait'),
        barInference: document.getElementById('bar_inference'),
        barOverhead: document.getElementById('bar_overhead'),
        tokenizeP95: document.getElementById('tokenize_p95'),
        tokenizerQueueWaitP95Breakdown: document.getElementById('tokenizer_queue_wait_p95_breakdown'),
        modelQueueWaitP95Breakdown: document.getElementById('model_queue_wait_p95_breakdown'),
        inferenceP95: document.getElementById('inference_p95'),
        totalP95: document.getElementById('total_p95'),
        latencyLive: document.getElementById('latency_live'),
        throughputLive: document.getElementById('throughput_live'),
        tokenizeLive: document.getElementById('tokenize_live'),
        tokenizerQueueWaitLive: document.getElementById('tokenizer_queue_wait_live'),
        tokenizerQueueSizeLive: document.getElementById('tokenizer_queue_size_live'),
        tokenizerThroughputLive: document.getElementById('tokenizer_throughput_live'),
        inferenceLive: document.getElementById('inference_live'),
        modelQueueWaitLive: document.getElementById('model_queue_wait_live'),
        modelQueueSizeLive: document.getElementById('model_queue_size_live'),
        overheadLive: document.getElementById('overhead_live'),
        cpuLive: document.getElementById('cpu_live'),
        gpuLive: document.getElementById('gpu_live'),
        queriesLive: document.getElementById('queries_live'),
        paddingLive: document.getElementById('padding_live'),
        utilizationLive: document.getElementById('utilization_live'),
        instanceSectionTitle: document.getElementById('instance_section_title'),
        instanceMetrics: document.getElementById('instance_metrics'),
        workerStatsTitle: document.getElementById('worker_stats_title'),
        workerStatsSection: document.getElementById('worker_stats_section'),
        tokenizerWorkerStatsTitle: document.getElementById('tokenizer_worker_stats_title'),
        tokenizerWorkerStatsSection: document.getElementById('tokenizer_worker_stats_section'),
    };
}

// Update experiment info in header
function updateExperimentInfo(data) {
    const name = data.experiment_name || 'ML Inference Dashboard';
    const description = data.experiment_description || 'Real-time Stage Breakdown';
    const backend = data.backend_type || 'pytorch';
    const device = data.device || 'cpu';

    if (elements.experimentName) elements.experimentName.textContent = name;
    if (elements.experimentSubtitle) elements.experimentSubtitle.textContent = description;
    if (elements.badgeBackend) elements.badgeBackend.textContent = backend.toUpperCase();
    if (elements.badgeDevice) elements.badgeDevice.textContent = device.toUpperCase();
}

// Update status badge
function updateStatus(isRunning) {
    if (!elements.status) return;
    elements.status.textContent = isRunning ? 'Running' : 'Ready';
    elements.status.className = 'status ' + (isRunning ? 'running' : 'idle');
}

// Update stage breakdown bar and percentages
function updateStageBreakdown(data) {
    const stagePct = data.stage_percentages || {};

    const components = [
        { name: 'tokenize', pct: stagePct.tokenize_pct || 0, element: elements.barTokenize, pctElement: elements.pctTokenize },
        { name: 'tokenizer_queue_wait', pct: stagePct.tokenizer_queue_wait_pct || 0, element: elements.barTokenizerQueueWait, pctElement: elements.pctTokenizerQueueWait },
        { name: 'model_queue_wait', pct: stagePct.model_queue_wait_pct || 0, element: elements.barModelQueueWait, pctElement: elements.pctModelQueueWait },
        { name: 'inference', pct: stagePct.inference_pct || 0, element: elements.barInference, pctElement: elements.pctInference },
        { name: 'overhead', pct: stagePct.overhead_pct || 0, element: elements.barOverhead, pctElement: elements.pctOverhead },
    ];

    const totalPct = components.reduce((sum, c) => sum + c.pct, 0);

    if (totalPct === 0) {
        components.forEach(comp => {
            if (comp.element) comp.element.style.width = '0%';
            if (comp.pctElement) comp.pctElement.textContent = '0';
        });
        return;
    }

    components.forEach((comp) => {
        const normalizedPct = (comp.pct / totalPct) * 100;

        if (comp.element) {
            comp.element.style.width = normalizedPct + '%';
        }
        if (comp.pctElement) comp.pctElement.textContent = fmt(comp.pct, 1);
    });
}

// Update P95 statistics
function updateP95Stats(data) {
    const stageBreakdown = data.stage_breakdown || {};
    const tokenizeStats = stageBreakdown.tokenize || {};
    const tokenizerQueueWaitStats = stageBreakdown.tokenizer_queue_wait || {};
    const modelQueueWaitStats = stageBreakdown.model_queue_wait || {};
    const inferenceStats = stageBreakdown.model_inference || {};

    if (elements.tokenizeP95) elements.tokenizeP95.textContent = fmt(tokenizeStats.p95_ms || 0) + ' ms';
    if (elements.tokenizerQueueWaitP95Breakdown) elements.tokenizerQueueWaitP95Breakdown.textContent = fmt(tokenizerQueueWaitStats.p95_ms || 0) + ' ms';
    if (elements.modelQueueWaitP95Breakdown) elements.modelQueueWaitP95Breakdown.textContent = fmt(modelQueueWaitStats.p95_ms || 0) + ' ms';
    if (elements.inferenceP95) elements.inferenceP95.textContent = fmt(inferenceStats.p95_ms || 0) + ' ms';
    if (elements.totalP95) elements.totalP95.textContent = fmt(data.p95_ms || 0) + ' ms';
}

// Update per-worker stats
function updateWorkerStats(data) {
    const workerStats = data.worker_stats || [];

    if (workerStats.length === 0) {
        const section = document.getElementById('worker-section');
        if (section) section.style.display = 'none';
        return;
    }

    const section = document.getElementById('worker-section');
    if (section) section.style.display = 'block';

    const container = document.getElementById('worker_stats_section');
    if (container) {
        const cardsHtml = workerStats.map((ws, i) => `
            <div class="metric-card">
                <div class="metric-label">Worker ${ws.worker_id || i}</div>
                <div class="metric-value">${fmt(ws.avg_ms || 0)}</div>
                <div class="metric-unit">ms latency</div>
                <div class="metric-subtext">${ws.query_count || 0} queries | ${fmt(ws.throughput_qps || 0)} q/s</div>
            </div>
        `).join('');
        container.innerHTML = cardsHtml;
    }
}

// Update per-tokenizer-worker stats
function updateTokenizerWorkerStats(data) {
    const tokenizerWorkerStats = data.tokenizer_worker_stats || [];

    if (tokenizerWorkerStats.length === 0) {
        const section = document.getElementById('tokenizer-worker-section');
        if (section) section.style.display = 'none';
        return;
    }

    const section = document.getElementById('tokenizer-worker-section');
    if (section) section.style.display = 'block';

    const container = document.getElementById('tokenizer_worker_stats_section');
    if (container) {
        const cardsHtml = tokenizerWorkerStats.map((tws, i) => `
            <div class="metric-card">
                <div class="metric-label">Tokenizer ${tws.worker_id || i}</div>
                <div class="metric-value">${fmt(tws.avg_ms || 0)}</div>
                <div class="metric-unit">ms latency</div>
                <div class="metric-subtext">${tws.query_count || 0} queries | ${fmt(tws.throughput_qps || 0)} q/s</div>
            </div>
        `).join('');
        container.innerHTML = cardsHtml;
    }
}

// Fetch metrics and update dashboard
async function fetchAndUpdate() {
    try {
        const response = await fetch('/metrics');

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!data) return;

        // Update all UI elements
        updateEl('query_count', data.query_count || 0, 0);
        updateEl('instant_latency_ms', data.instant_latency_ms || data.avg_ms || 0);
        updateEl('throughput_qps', data.throughput_qps || 0);

        const queueSizes = data.queue_sizes || {};
        const stageBreakdown = data.stage_breakdown || {};
        const padding = data.padding_analysis || {};

        updateEl('tokenize_ms', data.last_tokenize_ms || 0);
        updateEl('tokenizer_queue_wait_ms', data.last_tokenizer_queue_wait_ms || 0);
        updateEl('tokenizer_queue_size', queueSizes.tokenizer_queue_size || 0, 0);
        updateEl('inference_ms', data.last_inference_ms || 0);
        updateEl('model_queue_wait_ms', data.last_model_queue_wait_ms || 0);
        updateEl('model_queue_size', queueSizes.model_queue_size || 0, 0);
        updateEl('overhead_ms', data.last_overhead_ms || 0);

        const tokenizerWorkerStats = data.tokenizer_worker_stats || [];
        const tokenizerThroughput = tokenizerWorkerStats.reduce((sum, ws) => sum + (ws.throughput_qps || 0), 0);
        updateEl('tokenizer_throughput_qps', tokenizerThroughput);

        const workerStats = data.worker_stats || [];
        const inferenceThroughput = workerStats.reduce((sum, ws) => sum + (ws.throughput_qps || 0), 0);
        updateEl('inference_throughput_qps', inferenceThroughput);

        updateEl('padding_pct', padding.avg_padding_pct || 0);
        updateEl('max_seq_len', padding.max_seq_length || 0, 0);
        updateEl('avg_seq_len', padding.avg_seq_length || 0);

        // Live values
        updateEl('latency_live', (data.instant_latency_ms || 0).toFixed(1) + ' ms');
        updateEl('throughput_live', (data.throughput_qps || 0).toFixed(1) + ' q/s');
        updateEl('tokenize_live', (data.last_tokenize_ms || 0) + ' ms');
        updateEl('tokenizer_queue_wait_live', (data.last_tokenizer_queue_wait_ms || 0) + ' ms');
        updateEl('tokenizer_queue_size_live', queueSizes.tokenizer_queue_size || 0);
        updateEl('tokenizer_throughput_live', tokenizerThroughput.toFixed(1) + ' q/s');
        updateEl('inference_live', (data.last_inference_ms || 0) + ' ms');
        updateEl('model_queue_wait_live', (data.last_model_queue_wait_ms || 0) + ' ms');
        updateEl('model_queue_size_live', queueSizes.model_queue_size || 0);
        updateEl('inference_throughput_live', inferenceThroughput.toFixed(1) + ' q/s');
        updateEl('overhead_live', (data.last_overhead_ms || 0) + ' ms');
        updateEl('cpu_live', (data.cpu_percent || 0).toFixed(1) + '%');
        updateEl('gpu_live', (data.gpu_memory_mb || 0).toFixed(0) + ' MB');
        updateEl('queries_live', data.query_count || 0);
        updateEl('padding_live', (padding.avg_padding_pct || 0).toFixed(1) + '%');
        updateEl('utilization_live', (data.instance_metrics?.avg_utilization_pct || 0).toFixed(1) + '%');

        updateExperimentInfo(data);
        updateStatus(data.is_running);
        updateStageBreakdown(data);
        updateP95Stats(data);
        updateWorkerStats(data);
        updateTokenizerWorkerStats(data);

        // Update charts
        if (data.history && window.DashboardCharts && window.DashboardCharts.updateAll) {
            window.DashboardCharts.updateAll(data.history);
        }
    } catch (error) {
        const statusEl = document.getElementById('status');
        if (statusEl) {
            statusEl.textContent = 'Disconnected';
            statusEl.className = 'status';
        }
    }
}

// Initialize dashboard
function init() {
    updateScriptStatus('Initializing...', '#00aa00');

    initElements();
    updateScriptStatus('Ready', '#00ff00');

    // Initialize charts
    if (typeof Chart !== 'undefined' && window.DashboardCharts && typeof window.DashboardCharts.init === 'function') {
        try {
            window.DashboardCharts.init();
        } catch (err) {
            updateScriptStatus('Chart Init Failed', '#ff0000');
        }
    }

    // Start fetching
    fetchAndUpdate();
    setInterval(fetchAndUpdate, 500);
}

// Update script status indicator
function updateScriptStatus(message, color = '#00ff00') {
    const statusEl = document.getElementById('script_status');
    if (statusEl) {
        statusEl.textContent = message;
        statusEl.style.background = color;
    }
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    updateScriptStatus('Waiting for DOM...', '#ffaa00');
    document.addEventListener('DOMContentLoaded', () => {
        updateScriptStatus('DOM Ready', '#00aa00');
        setTimeout(init, 100);
    });
} else {
    updateScriptStatus('DOM Ready', '#00aa00');
    setTimeout(init, 100);
}
