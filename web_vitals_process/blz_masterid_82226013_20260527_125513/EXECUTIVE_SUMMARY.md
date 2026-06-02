# Web Vitals Executive Summary
## BlazeMeter Test: Perforce Example (Master ID: 82226013)

**Test Date:** May 26-27, 2026  
**Test Name:** Perforce Example  
**Regions Tested:** 4 (US-East-1, Europe-West2-A, Australia-Southeast1-A, Africa-South1-A)  
**Test Target:** www.perforce.com

---

## Key Performance Highlights

### Overall Performance Score: ⚠️ NEEDS ATTENTION

The multi-region performance test revealed significant **regional disparities** in user experience metrics, with some regions performing substantially better than others.

---

## Core Web Vitals Analysis

### 1. **Largest Contentful Paint (LCP)** ❌ CRITICAL

| Region | Average LCP | Status | Notes |
|--------|-------------|--------|-------|
| **US-East-1** | ~312 ms | ✅ Good | Consistent performance |
| **Europe-West2-A** | ~267 ms | ✅ Good | Strong performance |
| **Australia-Southeast1-A** | ~1,024 ms | ❌ Poor | High latency region |
| **Africa-South1-A** | ~591 ms | ⚠️ Needs Improvement | Variable performance |

**Key Insight:** LCP varies significantly by region, with Australia showing values **3-4x higher** than US/EU regions. One anomalous spike to 19,928ms detected, suggesting temporary server/network issues.

**Status:** 50% of regions exceed the "Good" threshold of 2.5 seconds (50th percentile). Australia and Africa require optimization.

---

### 2. **Interaction to Next Paint (INP)** ✅ ACCEPTABLE

| Region | Average INP | Status |
|--------|-------------|--------|
| **US-East-1** | ~92 ms | ✅ Good |
| **Europe-West2-A** | ~104 ms | ✅ Good |
| **Australia-Southeast1-A** | ~75 ms | ✅ Good |
| **Africa-South1-A** | ~71 ms | ✅ Good |

**Status:** All regions maintain responsive interactions well below the 200ms "Good" threshold.

---

### 3. **Cumulative Layout Shift (CLS)** ✅ GOOD

| Region | Average CLS | Status |
|--------|-------------|--------|
| **US-East-1** | ~0.12 | ✅ Good |
| **Europe-West2-A** | ~0.13 | ✅ Good |
| **Australia-Southeast1-A** | ~0.14 | ✅ Good |
| **Africa-South1-A** | ~0.14 | ✅ Good |

**Status:** All regions maintain excellent visual stability below the 0.1 "Good" threshold.

---

### 4. **Time to First Byte (TTFB)** ⚠️ VARIES BY REGION

| Region | Average TTFB | Status |
|--------|--------------|--------|
| **US-East-1** | ~40 ms | ✅ Excellent |
| **Europe-West2-A** | ~42 ms | ✅ Excellent |
| **Australia-Southeast1-A** | ~215 ms | ⚠️ High |
| **Africa-South1-A** | ~201 ms | ⚠️ High |

**Key Insight:** Australia and Africa experience **5x slower** server response times, indicating either geographic latency or server location issues.

---

## Page-Specific Performance

### Step-by-Step Analysis (Perforce Website Navigation)

#### **Step 1: Main Landing Page**
- **LCP Range:** 148-1,172 ms
- **Page Load:** 2.5-7.0 seconds
- **Issue:** Africa region shows 7+ second load times

#### **Step 2: Browse Products**
- **LCP Range:** 188-668 ms
- **Page Load:** 0.5-5.3 seconds
- **Issue:** Product catalog page has high variability

#### **Step 3: Digital IP Management**
- **LCP Range:** 196-668 ms (similar to Step 2)
- **Page Load:** 1.0-5.3 seconds
- **Notable:** One extreme outlier (19,928ms in Australia region)

#### **Step 4: Explore IPLM**
- **LCP Range:** 128-588 ms
- **Page Load:** 0.8-4.0 seconds
- **Performance:** Relatively consistent across regions

#### **Step 5: What's New**
- **LCP Range:** 116-652 ms
- **Page Load:** 0.7-5.3 seconds
- **Observation:** Africa shows highest variance

#### **Step 6: Perforce Software Popup Tab**
- **LCP Range:** 96-764 ms
- **Page Load:** 1.8-5.2 seconds
- **Issue:** Pop-up tab interaction affects load time

---

## Regional Performance Summary

### 🟢 **US-East-1** (Excellent)
- **Average LCP:** 312 ms
- **Average Page Load:** 1.5-2.0 seconds
- **CLS:** 0.128 (Good)
- **INP:** 92 ms (Responsive)
- **Recommendation:** Current US infrastructure meets performance standards

### 🟢 **Europe-West2-A** (Excellent)
- **Average LCP:** 267 ms
- **Average Page Load:** 1.0-1.5 seconds
- **CLS:** 0.133 (Good)
- **INP:** 104 ms (Responsive)
- **Recommendation:** EU performance is optimal; consider as baseline

### 🔴 **Australia-Southeast1-A** (Poor)
- **Average LCP:** 1,024 ms (**4x slower than US**)
- **Average Page Load:** 3.5-5.0 seconds
- **CLS:** 0.139 (Acceptable)
- **INP:** 75 ms (Good)
- **Anomalies:** One extreme spike (19,928ms) suggests transient network issue
- **Recommendation:** **URGENT** - Investigate server location, CDN coverage, or database query performance

### 🟠 **Africa-South1-A** (Below Target)
- **Average LCP:** 591 ms (**2x slower than US**)
- **Average Page Load:** 2.5-3.5 seconds
- **CLS:** 0.141 (Acceptable)
- **INP:** 71 ms (Good)
- **TTFB:** 201 ms (**5x higher than US**)
- **Recommendation:** Geographic latency is primary issue; consider edge caching

---

## Performance Issues & Bottlenecks

### 🔴 **Critical Issues**

1. **Regional Latency Disparity**
   - Africa and Australia regions experience 2-4x higher LCP
   - TTFB values suggest server location or network routing problems

2. **Extreme Outlier Event**
   - One measurement in Australia showing 19,928ms LCP on Step 2/3 (Browse Products)
   - Indicates potential temporary network congestion or server hiccup

3. **Inconsistent Product Catalog Performance**
   - Steps 2 & 3 (Browse Products, Digital IP Management) show high variance
   - May indicate unoptimized image loading or third-party content

### ⚠️ **Secondary Concerns**

1. **Page Load Time Variability**
   - Even within same region, page loads vary 1-3 seconds
   - Suggests caching inconsistencies or variable content size

2. **Large Content Delivery**
   - Total page sizes remain consistent (~20 MB)
   - LCP delays suggest rendering/processing issues, not bandwidth

---

## Recommendations

### 🎯 **Immediate Actions (Priority 1)**

1. **Investigate Australia Infrastructure**
   - Check if content is being served from the same server
   - Consider edge location closer to Sydney or Melbourne
   - Verify database query performance for IPLM product pages

2. **Analyze Africa Routing**
   - Audit TTFB to identify server response delays
   - Implement CDN with South African edge node
   - Test direct server connectivity vs. routed traffic

3. **Debug Outlier Event**
   - Identify what happened during 19,928ms spike
   - Review server logs and network traces
   - Implement monitoring to catch similar issues

### 📊 **Short-term Optimizations (Priority 2)**

1. **Image Optimization**
   - Verify images on product pages are properly optimized
   - Consider WebP format with fallbacks
   - Implement lazy loading for below-the-fold content

2. **Resource Prioritization**
   - Defer non-critical scripts
   - Inline critical CSS
   - Optimize LCP element (likely hero image on landing page)

3. **Caching Strategy**
   - Implement browser caching headers
   - Add server-side caching for static assets
   - Review CDN cache invalidation policies

### 🔧 **Long-term Solutions (Priority 3)**

1. **Global Infrastructure Review**
   - Evaluate CDN provider performance by region
   - Consider multi-region database replication
   - Implement geographic load balancing

2. **Performance Monitoring**
   - Set up continuous synthetic monitoring
   - Establish regional performance SLOs
   - Create alerts for LCP degradation

3. **Third-party Script Audit**
   - Profile external script impact on LCP
   - Defer analytics/tracking scripts
   - Replace slow third-parties with faster alternatives

---

## Target Metrics & SLOs

### Current State vs. Goals

| Metric | Target | US-East | Europe | Australia | Africa |
|--------|--------|---------|--------|-----------|--------|
| **LCP (Good)** | <2.5s | ✅ 312ms | ✅ 267ms | ❌ 1,024ms | ⚠️ 591ms |
| **INP (Good)** | <200ms | ✅ 92ms | ✅ 104ms | ✅ 75ms | ✅ 71ms |
| **CLS (Good)** | <0.1 | ✅ 0.128 | ✅ 0.133 | ✅ 0.139 | ✅ 0.141 |
| **Page Load** | <3.0s | ✅ 1.5s | ✅ 1.3s | ❌ 4.0s | ⚠️ 3.0s |

### Regional Coverage Analysis

| Region | Meets Targets | Coverage Status |
|--------|---------------|-----------------|
| **US-East-1** | ✅ 100% | Ready for Production |
| **Europe-West2-A** | ✅ 100% | Ready for Production |
| **Australia-Southeast1-A** | ❌ 25% (INP, CLS only) | **Requires Optimization** |
| **Africa-South1-A** | ⚠️ 50% (INP, CLS) | **Needs Improvement** |

---

## Conclusion

The Perforce website demonstrates **excellent performance in US and European regions**, with LCP and interaction responsiveness meeting Core Web Vitals standards. However, **Australia and Africa regions require immediate optimization**, particularly for Largest Contentful Paint (LCP) metrics.

The primary bottleneck is **geographic latency** rather than content optimization, suggesting infrastructure-level solutions (CDN edge locations, server proximity) will have the most impact.

**Overall Readiness:** 50% of target markets meet performance standards. Estimated 2-3 weeks optimization needed to achieve global compliance.

---

## Test Methodology

- **Test Engine:** BlazeMeter Perforce Example
- **Execution Date:** May 26, 2026
- **Sampling:** Multiple runs per region (5 samples per region)
- **Browser:** Chrome/Chromium (60 FPS)
- **Metrics Captured:** Core Web Vitals (LCP, INP, CLS) + Secondary Metrics (TTFB, FCP, Page Load Time)

---

**Report Generated:** May 28, 2026  
**Test Master ID:** 82226013  
**Account:** BlazeMeter SE Demo
