
## Experiment Run: 2025-12-21 02:11:04

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Device:** `mps`

**Quantized:** `False`

**Requests per config:** `500`

| Batch | Conc | Requests | Pairs | Time(s) | Avg(ms) | P50(ms) | P95(ms) | P99(ms) | Avg Throughput | Pairs/s |
|-------|------|----------|-------|---------|---------|---------|---------|---------|----------------|--------|
| 1 | 1 | 500 | 500 | 4.61 | 8.68 | 7.79 | 8.67 | 35.97 | 21.40 req/s | 108.43 |
| 1 | 4 | 500 | 500 | 3.63 | 18.32 | 23.82 | 32.12 | 35.47 | 37.04 req/s | 137.56 |
| 1 | 8 | 500 | 500 | 3.66 | 31.24 | 27.65 | 62.54 | 67.35 | 48.93 req/s | 136.76 |
| 1 | 16 | 500 | 500 | 3.79 | 42.16 | 38.54 | 79.13 | 83.97 | 58.06 req/s | 131.97 |
| 1 | 32 | 500 | 500 | 3.79 | 48.69 | 56.83 | 80.29 | 85.49 | 65.38 req/s | 131.94 |

**Best Throughput:** batch=1, conc=4 → 137.56 pairs/s

**Best Latency:** batch=1, conc=1 → 8.68ms avg

---

## Experiment Run: 2025-12-21 02:17:25

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Device:** `mps`

**Quantized:** `False`

**Requests per config:** `500`

| Batch | Conc | Requests | Pairs | Time(s) | Avg(ms) | P50(ms) | P95(ms) | P99(ms) | Avg Throughput | Pairs/s |
|-------|------|----------|-------|---------|---------|---------|---------|---------|----------------|--------|
| 1 | 1 | 500 | 500 | 4.93 | 9.23 | 7.94 | 12.35 | 36.61 | 20.27 req/s | 101.34 |
| 1 | 4 | 500 | 500 | 3.58 | 18.22 | 23.27 | 29.98 | 40.29 | 35.41 req/s | 139.69 |
| 1 | 8 | 500 | 500 | 3.73 | 31.62 | 26.64 | 62.36 | 67.84 | 46.91 req/s | 134.04 |
| 1 | 16 | 500 | 500 | 3.95 | 43.17 | 46.68 | 82.26 | 95.52 | 55.68 req/s | 126.67 |
| 1 | 32 | 500 | 500 | 3.80 | 49.52 | 58.37 | 82.82 | 100.01 | 62.94 req/s | 131.56 |

**Best Throughput:** batch=1, conc=4 → 139.69 pairs/s

**Best Latency:** batch=1, conc=1 → 9.23ms avg

---
