# BlazeMeter web vitals

# Web Vitals

Understand Web Vitals.  Web Vitals are a standardized set of performance metrics created by Google to measure the real-world user experience of a website, encompassing loading speed, visual stability, and interactivity. High scores not only ensure a seamless user experience but are also direct ranking factors in Google Search results. They focus on 3 core metrics.  Largest Content Paint (LCP), Interaction to Next Paint (INP), Cumulative Layout Shift (CLS)

# Core Web Vital Metrics

Understand the 3 core Web Vital metrics and what are good, needs improvements, and poor values for each metric.

Largest Content Paint (LCP) Measures loading performance. It tracks how long it takes for the largest text block or image to render within the visible viewport. This is the time it takes for the largest content element to become fully rendered in the portion of the web page the viewer sees. This metric helps development teams understand how users perceive the page load speed. 
Good: less than or equal to 2.5 seconds
Needs Improvement: between 2.5 and 4.0 seconds
Poor: greater than 4.0 seconds 

Interaction to Next Paint (INP)
INP Measures loading performance. It tracks how long it takes for the largest text block or image to render within the visible viewport. It measures latency of all clicks, taps, and keyboard interactions with the page throughout its lifespan and reports the single metric which all interactions are under. It's a measure of responsiveness and indicates when a page is consistently able to respond quickly to most users. INP replaced First Input Delay (FID) in March 2024.
Good: less than 200 milliseconds
Needs Improvement: between 200-500 milliseconds
Poor: greater than 500 milliseconds 

Cumulative Layout Shift (CLS)
CLP Measures visual stability. It calculates the amount of unexpected shifting of visible page content, such as a banner loading and pushing reading material down.
Good: less than or equal to 0.1 seconds
Needs Improvement: between 0.1 and .25 seconds
Poor: greater than .25 seconds

# Additional Metrics
Time to First Byte (TTFB), Time to Interactive (TTI), Total Blocking Time (TBT), FCP, document complete time, page Load Timein milliseconds, request Count, total page size in megabytes, dns lookup time in milliseconds, Frames per second (FPS)

Time to First Byte (TTFB): The time from the browser's initial request to receiving the first byte of data from the server. It includes DNS lookup, TCP connection, and server processing time.
Benchmark: Good is under 800ms; poor is over 1,800ms.

DNS Lookup Time: The duration required to resolve a domain name (e.g., example.com) into an IP address. High DNS time often indicates issues with the DNS provider or a lack of caching.

Document Complete Time: The point when the browser's onload event fires. This signifies that all static resources (HTML, images, CSS) have finished downloading.

Page Load Time: Often used interchangeably with "Document Complete," it measures the total time from navigation start to the completion of the load event.
Benchmark: Ideally kept under 2 seconds

Time to Interactive (TTI): The time it takes for a page to become fully interactive. A page is TTI when it has displayed useful content and can respond to user input within 50ms.

Total Blocking Time (TBT): The total amount of time between FCP and TTI where the main thread was blocked long enough to prevent input responsiveness.

Frames Per Second (FPS): A measure of visual smoothness during animations, scrolling, or transitions. A consistent 60 FPS is the standard for a fluid user experience. 

Request Count: The total number of individual HTTP requests (for images, scripts, CSS, etc.) required to load the page. Lower counts generally improve speed, especially on mobile.

Total Page Size (Page Weight): The sum of the file sizes of all resources downloaded to render the page, usually measured in Megabytes (MB)

Metric 	    Primary Focus	        Measurement Unit
TTFB	    Server responsiveness	Milliseconds (ms)
FCP         Perceived loading speed	Milliseconds (ms)
TBT/TTI	    Interactivity	        Milliseconds (ms)
Page Size	Data efficiency	        Megabytes (MB)
FPS	        Visual smoothness	    Frames per second
