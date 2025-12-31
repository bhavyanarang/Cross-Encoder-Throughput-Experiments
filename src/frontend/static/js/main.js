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
    overheadMs: document.getElementById('overhead_ms'),
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
    pctOverhead: document.getElementById('pct_overhead'),
    pctMpQueueSend: document.getElementById('pct_mp_queue_send'),
    pctMpQueueReceive: document.getElementById('pct_mp_queue_receive'),
    pctGrpcSerialize: document.getElementById('pct_grpc_serialize'),
    pctGrpcDeserialize: document.getElementById('pct_grpc_deserialize'),
    pctScheduler: document.getElementById('pct_scheduler'),
    pctOther: document.getElementById('pct_other'),

    // Stage bar segments
    barTokenize: document.getElementById('bar_tokenize'),
    barQueueWait: document.getElementById('bar_queue_wait'),
    barInference: document.getElementById('bar_inference'),
    barOverhead: document.getElementById('bar_overhead'),
    barMpQueueSend: document.getElementById('bar_mp_queue_send'),
    barMpQueueReceive: document.getElementById('bar_mp_queue_receive'),
    barGrpcSerialize: document.getElementById('bar_grpc_serialize'),
    barGrpcDeserialize: document.getElementById('bar_grpc_deserialize'),
    barScheduler: document.getElementById('bar_scheduler'),
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
    overheadLive: document.getElementById('overhead_live'),
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
    workerStatsSection: document.getElementById('worker_stats_section'),

    // Per-tokenizer-worker stats section
    tokenizerWorkerStatsTitle: document.getElementById('tokenizer_worker_stats_title'),
    tokenizerWorkerStatsSection: document.getElementById('tokenizer_worker_stats_section')
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
    elements.overheadMs.textContent = fmt(data.last_overhead_ms || 0);
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

    // Collect all components with their names and percentages
    const components = [
        { name: 'tokenize', label: 'Tokenization', pct: stagePct.tokenize_pct || 0, element: elements.barTokenize, pctElement: elements.pctTokenize },
        { name: 'queue_wait', label: 'Queue Wait', pct: stagePct.queue_wait_pct || 0, element: elements.barQueueWait, pctElement: elements.pctQueueWait },
        { name: 'inference', label: 'Model Inference', pct: stagePct.inference_pct || 0, element: elements.barInference, pctElement: elements.pctInference },
        { name: 'overhead', label: 'Tokenizer Overhead', pct: stagePct.overhead_pct || 0, element: elements.barOverhead, pctElement: elements.pctOverhead },
        { name: 'mp_queue_send', label: 'MP Queue Send', pct: stagePct.mp_queue_send_pct || 0, element: elements.barMpQueueSend, pctElement: elements.pctMpQueueSend },
        { name: 'mp_queue_receive', label: 'MP Queue Receive', pct: stagePct.mp_queue_receive_pct || 0, element: elements.barMpQueueReceive, pctElement: elements.pctMpQueueReceive },
        { name: 'grpc_serialize', label: 'gRPC Serialize', pct: stagePct.grpc_serialize_pct || 0, element: elements.barGrpcSerialize, pctElement: elements.pctGrpcSerialize },
        { name: 'grpc_deserialize', label: 'gRPC Deserialize', pct: stagePct.grpc_deserialize_pct || 0, element: elements.barGrpcDeserialize, pctElement: elements.pctGrpcDeserialize },
        { name: 'scheduler', label: 'Scheduler', pct: stagePct.scheduler_pct || 0, element: elements.barScheduler, pctElement: elements.pctScheduler },
        { name: 'other', label: 'Other', pct: stagePct.other_pct || 0, element: elements.barOther, pctElement: elements.pctOther },
    ];

    // Calculate total of all percentages
    const totalPct = components.reduce((sum, c) => sum + c.pct, 0);
    
    // If total is 0 or components exist, sort by percentage (descending) and get top 3
    let displayComponents = [];
    if (totalPct > 0) {
        const sorted = components.filter(c => c.pct > 0).sort((a, b) => b.pct - a.pct);
        const top3 = sorted.slice(0, 3);
        const rest = sorted.slice(3);

        // Calculate "Other" as sum of all non-top-3 components
        // If "other" is already in top3, don't add it again
        const otherInTop3 = top3.some(c => c.name === 'other');
        const restComponents = rest.filter(c => c.name !== 'other');
        const otherPct = restComponents.reduce((sum, c) => sum + c.pct, 0) + (otherInTop3 ? 0 : (stagePct.other_pct || 0));

        // Build display components list: top 3 + Other (if > 0 and not already in top3)
        displayComponents = [...top3];
        if (otherPct > 0 && !otherInTop3) {
            displayComponents.push({
                name: 'other',
                label: 'Other',
                pct: otherPct,
                element: elements.barOther,
                pctElement: elements.pctOther
            });
        }
    }

    // Hide all legend items and bar segments first
    const allLegendItems = document.querySelectorAll('.legend-item');
    allLegendItems.forEach(item => item.style.display = 'none');
    components.forEach(c => {
        c.element.style.display = 'none';
        c.pctElement.textContent = '0';
    });

    // If no components to display, we're done
    if (displayComponents.length === 0) {
        return;
    }

    // Normalize display components to ensure they sum to 100%
    const displayTotal = displayComponents.reduce((sum, c) => sum + c.pct, 0);
    const scaleFactor = displayTotal > 0 ? 100 / displayTotal : 1;
    
    // Update bar segments and legend for displayed components
    let cumulative = 0;
    displayComponents.forEach((comp) => {
        // Normalize the percentage to ensure 100% fill
        const normalizedPct = comp.pct * scaleFactor;
        
        // Show bar segment
        comp.element.style.display = 'flex';
        comp.element.style.width = normalizedPct + '%';
        comp.element.style.left = cumulative + '%';
        comp.element.textContent = normalizedPct > 2 ? fmt(normalizedPct, 1) + '%' : '';
        cumulative += normalizedPct;

        // Update percentage text (show original percentage, not normalized)
        comp.pctElement.textContent = fmt(comp.pct, 1);

        // Show legend item using data-component attribute
        const legendItem = document.querySelector(`.legend-item[data-component="${comp.name}"]`);
        if (legendItem) {
            legendItem.style.display = 'flex';
        }
    });
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
    elements.overheadLive.textContent = fmt(data.last_overhead_ms || 0) + ' ms';
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

// Update per-tokenizer-worker statistics
function updateTokenizerWorkerStats(data) {
    const tokenizerWorkerStats = data.tokenizer_worker_stats || [];

    if (tokenizerWorkerStats.length === 0) {
        elements.tokenizerWorkerStatsTitle.style.display = 'none';
        elements.tokenizerWorkerStatsSection.style.display = 'none';
        return;
    }

    elements.tokenizerWorkerStatsTitle.style.display = 'block';
    elements.tokenizerWorkerStatsSection.style.display = 'grid';

    // Build HTML for tokenizer worker stat cards
    const cardsHtml = tokenizerWorkerStats.map((tws, i) => {
        const color = getInstanceColor(i);
        return `
            <div class="worker-card" style="border-color: ${color}">
                <div class="worker-title">
                    <span class="worker-id" style="color: ${color}">Tokenizer Worker ${tws.worker_id}</span>
                </div>
                <div class="worker-metrics">
                    <div class="worker-metric">
                        <div class="worker-metric-label">Avg Latency</div>
                        <div class="worker-metric-value">${fmt(tws.avg_ms)} ms</div>
                    </div>
                    <div class="worker-metric">
                        <div class="worker-metric-label">P95 Latency</div>
                        <div class="worker-metric-value">${fmt(tws.p95_ms)} ms</div>
                    </div>
                    <div class="worker-metric">
                        <div class="worker-metric-label">Throughput</div>
                        <div class="worker-metric-value">${fmt(tws.throughput_tokens_per_sec)} tokens/s</div>
                    </div>
                    <div class="worker-metric">
                        <div class="worker-metric-label">Requests</div>
                        <div class="worker-metric-value">${tws.request_count}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    elements.tokenizerWorkerStatsSection.innerHTML = cardsHtml;
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
        updateTokenizerWorkerStats(data);

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
