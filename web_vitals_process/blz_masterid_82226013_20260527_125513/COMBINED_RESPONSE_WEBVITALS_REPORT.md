# Combined Response + Web Vitals Report

## Scope
- Master ID: 82226013
- Source files: 4 regional CSV files from web vitals process output
- Records analyzed: 248
- Regions: africa-south1-a, australia-southeast1-a, europe-west2-a, us-east-1

Response data is represented by TTFB, TTI, document complete time, and page load time. Web vitals are LCP, INP, and CLS.

## Regional Summary (Response + Web Vitals)
| Region | Samples | LCP avg (ms) | INP avg (ms) | CLS avg | TTFB avg (ms) | TTI avg (ms) | Document Complete avg (ms) | Page Load avg (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| africa-south1-a | 47 | 1,183.5 | 32.5 | 0.1000 | 1,049.5 | 1,363.9 | 5,477.9 | 5,485.3 |
| australia-southeast1-a | 47 | 363.9 | 72.0 | 0.1099 | 41.7 | 709.3 | 3,582.3 | 3,595.8 |
| europe-west2-a | 83 | 265.3 | 87.1 | 0.1134 | 38.4 | 449.7 | 1,550.5 | 1,558.0 |
| us-east-1 | 71 | 287.0 | 120.0 | 0.0991 | 41.8 | 531.1 | 1,895.9 | 1,904.2 |

## Step x Region Combined View
| Region | Step | Samples | LCP avg | LCP p95 | INP avg | CLS avg | TTFB avg | TTFB p95 | Doc Complete avg | Page Load avg | TTI avg |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| africa-south1-a | Browse Products | 8 | 2,803.5 | 19,928.0 | N/A | 0.0828 | 2,616.6 | 19,791.7 | 7,200.2 | 7,201.4 | 2,907.4 |
| africa-south1-a | Digital IP Management | 8 | 2,803.5 | 19,928.0 | 32.0 | 0.0828 | 2,616.6 | 19,791.7 | 7,200.2 | 7,201.4 | 2,907.4 |
| africa-south1-a | Explore IPLM | 8 | 345.5 | 588.0 | N/A | 0.0894 | 167.2 | 311.1 | 4,179.9 | 4,184.1 | 472.5 |
| africa-south1-a | Main Landing Page | 8 | 428.5 | 1,172.0 | 33.0 | 0.2530 | 200.2 | 765.3 | 6,030.2 | 6,048.2 | 950.3 |
| africa-south1-a | Perforce Software Popup Tab | 7 | 292.6 | 452.0 | N/A | 0.0819 | 5.2 | 9.4 | 3,122.1 | 3,141.9 | 409.4 |
| africa-south1-a | What’s New | 8 | 316.0 | 652.0 | N/A | 0.0077 | 169.1 | 383.5 | 4,840.2 | 4,841.5 | 417.2 |
| australia-southeast1-a | Browse Products | 8 | 352.0 | 668.0 | N/A | 0.1216 | 48.5 | 214.5 | 3,670.6 | 3,673.3 | 707.9 |
| australia-southeast1-a | Digital IP Management | 8 | 352.0 | 668.0 | 62.0 | 0.1216 | 48.5 | 214.5 | 3,670.6 | 3,673.3 | 707.9 |
| australia-southeast1-a | Explore IPLM | 8 | 391.0 | 568.0 | N/A | 0.0792 | 50.0 | 217.2 | 2,642.6 | 2,650.0 | 568.4 |
| australia-southeast1-a | Main Landing Page | 8 | 480.0 | 1,064.0 | 82.0 | 0.2530 | 26.5 | 30.5 | 4,032.5 | 4,056.9 | 1,289.8 |
| australia-southeast1-a | Perforce Software Popup Tab | 7 | 289.7 | 764.0 | N/A | 0.0512 | 3.7 | 11.0 | 4,625.9 | 4,671.3 | 543.9 |
| australia-southeast1-a | What’s New | 8 | 309.5 | 616.0 | N/A | 0.0257 | 49.2 | 216.6 | 2,982.1 | 2,984.5 | 417.2 |
| europe-west2-a | Browse Products | 14 | 241.7 | 248.0 | N/A | 0.1136 | 45.3 | 60.3 | 929.4 | 929.8 | 396.5 |
| europe-west2-a | Digital IP Management | 14 | 241.7 | 248.0 | 136.0 | 0.1136 | 45.3 | 60.3 | 929.4 | 929.8 | 396.5 |
| europe-west2-a | Explore IPLM | 14 | 253.7 | 332.0 | N/A | 0.0903 | 42.0 | 45.4 | 990.0 | 992.6 | 345.4 |
| europe-west2-a | Main Landing Page | 14 | 308.6 | 380.0 | 38.3 | 0.2881 | 38.1 | 43.7 | 2,590.9 | 2,612.0 | 782.1 |
| europe-west2-a | Perforce Software Popup Tab | 13 | 316.3 | 488.0 | N/A | 0.0641 | 5.1 | 11.3 | 2,810.6 | 2,830.5 | 483.6 |
| europe-west2-a | What’s New | 14 | 233.4 | 292.0 | N/A | 0.0070 | 42.9 | 48.2 | 1,142.7 | 1,144.0 | 296.3 |
| us-east-1 | Browse Products | 12 | 262.0 | 288.0 | N/A | 0.1043 | 49.1 | 58.4 | 1,194.2 | 1,194.8 | 474.9 |
| us-east-1 | Digital IP Management | 12 | 262.0 | 288.0 | 182.0 | 0.1043 | 49.1 | 58.4 | 1,194.2 | 1,194.8 | 474.9 |
| us-east-1 | Explore IPLM | 12 | 326.3 | 356.0 | N/A | 0.0903 | 45.4 | 64.4 | 1,232.8 | 1,236.3 | 416.9 |
| us-east-1 | Main Landing Page | 12 | 333.0 | 376.0 | 58.0 | 0.2647 | 46.3 | 67.8 | 3,002.4 | 3,021.1 | 953.2 |
| us-east-1 | Perforce Software Popup Tab | 11 | 327.3 | 600.0 | N/A | 0.0096 | 5.0 | 10.5 | 3,407.7 | 3,434.1 | 562.3 |
| us-east-1 | What’s New | 12 | 214.7 | 280.0 | N/A | 0.0138 | 43.6 | 58.7 | 1,470.1 | 1,471.9 | 307.0 |

## Notable Response/Web-Vitals Outliers
| Region | Timestamp | Step | LCP (ms) | TTFB (ms) | Page Load (ms) | URL |
|---|---|---|---:|---:|---:|---|
| africa-south1-a | 2026-05-26T15:31:04.491Z | Browse Products | 19,928.0 | 19,791.7 | 24,479.5 | https://www.perforce.com/products |
| africa-south1-a | 2026-05-26T15:31:05.814Z | Digital IP Management | 19,928.0 | 19,791.7 | 24,479.5 | https://www.perforce.com/products#p-20457 |

## Correlation Notes
- Regions with higher TTFB also trend toward higher page load time and higher LCP.
- INP remains low across regions, indicating interaction responsiveness is not the primary issue.
- CLS is consistently elevated on key navigation steps and should be treated as a UX stability defect.
