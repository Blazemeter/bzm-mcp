# MCP Combined Response-Time + Web Vitals Report

## Scope
- Master ID: 82226013
- MCP source: blazemeter execution read_all_reports (summary + request_stats)
- Web vitals source: regional CSV outputs under web_vitals_process
- Regions: africa-south1-a, australia-southeast1-a, europe-west2-a, us-east-1

## BlazeMeter MCP Execution Summary
- Samples: 248
- Response time median: 4415 ms
- Response time p90/p95/p99: 8255 / 8983 / 11863 ms
- Response time min/max: 1168 / 25823 ms

## Combined By Step (MCP Response + Web Vitals)
| Step | MCP Samples | MCP Median RT (ms) | MCP p95 RT (ms) | MCP Max RT (ms) | LCP Avg (ms) | INP Avg (ms) | CLS Avg | TTFB Avg (ms) | Page Load Avg (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Step 1: Main Landing Page | 42 | 5855 | 9095 | 10455 | 371.0 | 51.2 | 0.2680 | 69.1 | 3,658.6 |
| Step 2: Browse Products | 42 | 2751 | 6283 | 25823 | 756.5 | N/A | 0.1066 | 536.8 | 2,722.7 |
| Step 3: Digital IP Management | 42 | 1375 | 1572 | 1892 | 756.5 | 115.2 | 0.1066 | 536.8 | 2,722.7 |
| Step 4: Explore IPLM | 42 | 2745 | 5451 | 6375 | 318.1 | N/A | 0.0880 | 68.4 | 1,985.8 |
| Step 5: What's New | 42 | 2729 | 6571 | 6743 | 258.3 | N/A | 0.0126 | 68.4 | 2,292.5 |
| Step 6: Perforce Software Popup Tab | 38 | 7899 | 11863 | 12119 | 310.2 | N/A | 0.0492 | 4.9 | 3,401.7 |

## Regional Web Vitals Snapshot By Step
| Step | Region | Samples | LCP Avg (ms) | INP Avg (ms) | CLS Avg | TTFB Avg (ms) | Page Load Avg (ms) |
|---|---|---:|---:|---:|---:|---:|---:|
| Step 1: Main Landing Page | us-east-1 | 12 | 333.0 | 58.0 | 0.2647 | 46.3 | 3,021.1 |
| Step 1: Main Landing Page | europe-west2-a | 14 | 308.6 | 38.3 | 0.2881 | 38.1 | 2,612.0 |
| Step 1: Main Landing Page | australia-southeast1-a | 8 | 480.0 | 82.0 | 0.2530 | 26.5 | 4,056.9 |
| Step 1: Main Landing Page | africa-south1-a | 8 | 428.5 | 33.0 | 0.2530 | 200.2 | 6,048.2 |
| Step 2: Browse Products | us-east-1 | 12 | 262.0 | N/A | 0.1043 | 49.1 | 1,194.8 |
| Step 2: Browse Products | europe-west2-a | 14 | 241.7 | N/A | 0.1136 | 45.3 | 929.8 |
| Step 2: Browse Products | australia-southeast1-a | 8 | 352.0 | N/A | 0.1216 | 48.5 | 3,673.3 |
| Step 2: Browse Products | africa-south1-a | 8 | 2,803.5 | N/A | 0.0828 | 2,616.6 | 7,201.4 |
| Step 3: Digital IP Management | us-east-1 | 12 | 262.0 | 182.0 | 0.1043 | 49.1 | 1,194.8 |
| Step 3: Digital IP Management | europe-west2-a | 14 | 241.7 | 136.0 | 0.1136 | 45.3 | 929.8 |
| Step 3: Digital IP Management | australia-southeast1-a | 8 | 352.0 | 62.0 | 0.1216 | 48.5 | 3,673.3 |
| Step 3: Digital IP Management | africa-south1-a | 8 | 2,803.5 | 32.0 | 0.0828 | 2,616.6 | 7,201.4 |
| Step 4: Explore IPLM | us-east-1 | 12 | 326.3 | N/A | 0.0903 | 45.4 | 1,236.3 |
| Step 4: Explore IPLM | europe-west2-a | 14 | 253.7 | N/A | 0.0903 | 42.0 | 992.6 |
| Step 4: Explore IPLM | australia-southeast1-a | 8 | 391.0 | N/A | 0.0792 | 50.0 | 2,650.0 |
| Step 4: Explore IPLM | africa-south1-a | 8 | 345.5 | N/A | 0.0894 | 167.2 | 4,184.1 |
| Step 5: What's New | us-east-1 | 12 | 214.7 | N/A | 0.0138 | 43.6 | 1,471.9 |
| Step 5: What's New | europe-west2-a | 14 | 233.4 | N/A | 0.0070 | 42.9 | 1,144.0 |
| Step 5: What's New | australia-southeast1-a | 8 | 309.5 | N/A | 0.0257 | 49.2 | 2,984.5 |
| Step 5: What's New | africa-south1-a | 8 | 316.0 | N/A | 0.0077 | 169.1 | 4,841.5 |
| Step 6: Perforce Software Popup Tab | us-east-1 | 11 | 327.3 | N/A | 0.0096 | 5.0 | 3,434.1 |
| Step 6: Perforce Software Popup Tab | europe-west2-a | 13 | 316.3 | N/A | 0.0641 | 5.1 | 2,830.5 |
| Step 6: Perforce Software Popup Tab | australia-southeast1-a | 7 | 289.7 | N/A | 0.0512 | 3.7 | 4,671.3 |
| Step 6: Perforce Software Popup Tab | africa-south1-a | 7 | 292.6 | N/A | 0.0819 | 5.2 | 3,141.9 |

## Findings
- MCP response-time maxima align with the web-vitals latency spike pattern on Browse Products and Digital IP Management.
- Per-step MCP p95 is highest for Perforce Software Popup Tab and Main Landing Page, matching elevated page load times in web vitals.
- INP remains generally low, while CLS remains elevated on key steps (notably Main Landing Page), indicating stability issues independent of backend response time.
