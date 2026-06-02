#!/usr/bin/env python3
"""
Generate HTML report from extracted Web Vitals CSV files.
Aggregates metrics from multiple sessions/locations and creates a comprehensive report.
"""

import os
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from statistics import mean, stdev
from typing import Dict, List, Tuple
import base64


class WebVitalsReportGenerator:
    """Generate HTML reports from Web Vitals CSV data."""

    TEMPLATE_DIR = Path(__file__).resolve().parent.parent / 'html_report_templates'
    BASIC_TEMPLATE_FILE     = TEMPLATE_DIR / 'basic-web-vitals-report.html'
    DETAILED_TEMPLATE_FILE  = TEMPLATE_DIR / 'detailed-web-vitals-report.html'
    EXECUTIVE_TEMPLATE_FILE = TEMPLATE_DIR / 'executive-web-vitals-report.html'

    # Good / Poor thresholds for core metrics (values are inclusive)
    WEB_VITALS_THRESHOLDS = {
        'LCP_ms':  {'good': 2500,  'poor': 4000},
        'INP_ms':  {'good': 200,   'poor': 500},
        'CLS':     {'good': 0.1,   'poor': 0.25},
        'TTFB_ms': {'good': 800,   'poor': 1800},
        'FCP_ms':  {'good': 1800,  'poor': 3000},
    }
    
    # Web Vitals field definitions
    NUMERIC_FIELDS = {
        'LCP_ms': 'Largest Contentful Paint (ms)',
        'INP_ms': 'Interaction to Next Paint (ms)',
        'CLS': 'Cumulative Layout Shift',
        'TTFB_ms': 'Time To First Byte (ms)',
        'FCP_ms': 'First Contentful Paint (ms)',
        'TTI_ms': 'Time To Interactive (ms)',
        'TBT_ms': 'Total Blocking Time (ms)',
        'documentCompleteTime_ms': 'Document Complete Time (ms)',
        'pageLoadTime_ms': 'Page Load Time (ms)',
        'requestCount': 'Request Count',
        'totalPageSizeMB': 'Total Page Size (MB)',
        'dnsLookupTime_ms': 'DNS Lookup Time (ms)',
        'FPS': 'Frames Per Second'
    }
    
    def __init__(
        self,
        execution_dir: str,
        account_id: int = None,
        workspace_id: int = None,
        project_id: int = None,
        test_case_id: int = None,
        master_id: int = None,
        report_style: str = 'detailed',
    ):
        """Initialize report generator with execution directory and optional IDs."""
        self.execution_dir = Path(execution_dir)
        self.account_id = account_id
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.test_case_id = test_case_id
        self.master_id = master_id
        self.report_style = report_style
        self.metadata = self._load_metadata()
        self.csv_files = self._find_csv_files()
        self.aggregated_data = self._aggregate_csv_data()
    
    def _load_metadata(self) -> Dict:
        """Load execution metadata from JSON file."""
        metadata_file = self.execution_dir / 'execution-metadata.json'
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _find_csv_files(self) -> Dict[str, List[str]]:
        """Find all web-vitals-report-*.csv files organized by location."""
        csv_files = {}
        for location_dir in self.execution_dir.glob('*/'):
            if location_dir.is_dir() and location_dir.name != 'execution-metadata.json':
                location = location_dir.name
                # Look for both naming patterns: web-vitals-report-*.csv and *_web-vitals-report.csv
                csv_list = list(location_dir.glob('*web-vitals-report.csv'))
                if not csv_list:
                    csv_list = list(location_dir.glob('web-vitals-report-*.csv'))
                if csv_list:
                    csv_files[location] = csv_list
        return csv_files
    
    def _aggregate_csv_data(self) -> Dict:
        """Parse and aggregate data from all CSV files."""
        aggregated = {
            'by_location': {},
            'by_step': {},
            'all_rows': []
        }
        
        for location, csv_files in self.csv_files.items():
            aggregated['by_location'][location] = {
                'sessions': [],
                'metrics': {}
            }
            
            for csv_file in csv_files:
                session_data = self._parse_csv(csv_file)
                aggregated['by_location'][location]['sessions'].append({
                    'file': csv_file.name,
                    'rows': session_data
                })
                aggregated['all_rows'].extend(session_data)
        
        # Aggregate by step name
        for row in aggregated['all_rows']:
            step = row.get('stepName', 'Unknown')
            if step not in aggregated['by_step']:
                aggregated['by_step'][step] = []
            aggregated['by_step'][step].append(row)
        
        return aggregated
    
    def _parse_csv(self, csv_file: Path) -> List[Dict]:
        """Parse a web-vitals-report CSV file."""
        rows = []
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert numeric fields
                    for field in self.NUMERIC_FIELDS:
                        if field in row:
                            # Handle N/A and empty values
                            if row[field] in ('', 'N/A', None):
                                row[field] = None
                            else:
                                try:
                                    row[field] = float(row[field])
                                except ValueError:
                                    row[field] = None
                    rows.append(row)
        except Exception as e:
            print(f"Error parsing {csv_file}: {e}")
        return rows
    
    def _calculate_stats(self, values: List[float]) -> Dict:
        """Calculate statistics for a list of numeric values."""
        values = [v for v in values if v is not None]
        if not values:
            return {'min': None, 'max': None, 'mean': None, 'stdev': None}
        
        stats = {
            'min': min(values),
            'max': max(values),
            'mean': mean(values),
            'count': len(values)
        }
        if len(values) > 1:
            stats['stdev'] = stdev(values)
        return stats

    def _slugify(self, value: str) -> str:
        """Convert a string into a filesystem-friendly slug."""
        if not value:
            return 'unknown'

        slug = re.sub(r'\s+', '-', value.strip())
        slug = re.sub(r'[^A-Za-z0-9._-]', '', slug)
        return slug or 'unknown'

    @staticmethod
    def _location_to_region(location: str) -> str:
        """Convert a cloud region location string to a short display name.

        Examples:
          europe-west2-a      -> Europe
          australia-southeast1-a -> Australia
          africa-south1-a     -> Africa
          us-east-1           -> US
          asia-east1-a        -> Asia
          northamerica-northeast1-a -> North America
          southamerica-east1  -> South America
        """
        _prefix_map = {
            'us':            'US',
            'europe':        'Europe',
            'australia':     'Australia',
            'africa':        'Africa',
            'asia':          'Asia',
            'northamerica':  'North America',
            'southamerica':  'South America',
            'me':            'Middle East',
        }
        prefix = location.split('-')[0].lower()
        return _prefix_map.get(prefix, prefix.capitalize())

    def _load_basic_template(self) -> str:
        """Load the basic report template and substitute dynamic placeholders."""
        if not self.BASIC_TEMPLATE_FILE.exists():
            raise FileNotFoundError(f'Basic template not found: {self.BASIC_TEMPLATE_FILE}')

        locations = list(self.aggregated_data['by_location'].keys())
        # Convert raw location strings to human-readable region names (deduplicated, ordered).
        seen = {}
        for loc in locations:
            region = self._location_to_region(loc)
            if region not in seen:
                seen[region] = True
        regions_list = ', '.join(seen.keys()) if seen else 'N/A'
        regions_title = regions_list

        html = self.BASIC_TEMPLATE_FILE.read_text(encoding='utf-8')
        html = html.replace('{{REGIONS_TITLE}}', regions_title)
        html = html.replace('{{REGIONS_LIST}}', regions_list)
        return html
    
    def _load_detailed_template(self) -> str:
        """Load the detailed report template and substitute dynamic section tokens."""
        if not self.DETAILED_TEMPLATE_FILE.exists():
            raise FileNotFoundError(f'Detailed template not found: {self.DETAILED_TEMPLATE_FILE}')

        html = self.DETAILED_TEMPLATE_FILE.read_text(encoding='utf-8')
        html = html.replace('{{MASTER_ID}}',          str(self.metadata.get('testMasterId', 'N/A')))
        html = html.replace('{{HEADER_SECTION}}',     self._generate_header())
        html = html.replace('{{SUMMARY_SECTION}}',    self._generate_summary())
        html = html.replace('{{BY_LOCATION_SECTION}}',self._generate_by_location())
        html = html.replace('{{BY_STEP_SECTION}}',    self._generate_by_step())
        html = html.replace('{{RAW_DATA_SECTION}}',   self._generate_raw_data())
        return html

    # ─────────────────────────── Executive report ────────────────────────────

    def _classify_rating(self, field: str, value) -> str:
        """Return 'good', 'needs_improvement', or 'poor' for a metric value."""
        thresh = self.WEB_VITALS_THRESHOLDS.get(field)
        if thresh is None or value is None:
            return 'unknown'
        if value <= thresh['good']:
            return 'good'
        if value <= thresh['poor']:
            return 'needs_improvement'
        return 'poor'

    def _build_executive_chart_data(self) -> dict:
        """Compute all chart datasets for the executive report."""
        rows = self.aggregated_data['all_rows']

        # ── Donut data: Good / NI / Poor counts for LCP, INP, CLS ──────────
        donut_data = {}
        for field in ('LCP_ms', 'INP_ms', 'CLS'):
            counts = [0, 0, 0]   # [good, needs_improvement, poor]
            for row in rows:
                v = row.get(field)
                if v is not None:
                    r = self._classify_rating(field, v)
                    if r == 'good':             counts[0] += 1
                    elif r == 'needs_improvement': counts[1] += 1
                    else:                       counts[2] += 1
            donut_data[field] = counts

        # ── Regional averages: LCP, FCP, TTFB, Page Load ────────────────────
        region_labels, reg_lcp, reg_fcp, reg_ttfb, reg_page_load = [], [], [], [], []
        for loc, data in self.aggregated_data['by_location'].items():
            loc_rows = [r for s in data['sessions'] for r in s['rows']]
            region_labels.append(self._location_to_region(loc))

            def _avg(field):
                vals = [r[field] for r in loc_rows if r.get(field) is not None]
                return round(mean(vals), 1) if vals else 0

            reg_lcp.append(_avg('LCP_ms'))
            reg_fcp.append(_avg('FCP_ms'))
            reg_ttfb.append(_avg('TTFB_ms'))
            reg_page_load.append(_avg('pageLoadTime_ms'))

        # ── Step averages: Page Load + LCP (sorted by page load desc) ────────
        step_tuples = []
        for step, step_rows in self.aggregated_data['by_step'].items():
            pl_vals  = [r['pageLoadTime_ms'] for r in step_rows if r.get('pageLoadTime_ms') is not None]
            lcp_vals = [r['LCP_ms']          for r in step_rows if r.get('LCP_ms')          is not None]
            step_tuples.append((
                round(mean(pl_vals)  if pl_vals  else 0, 1),
                step,
                round(mean(lcp_vals) if lcp_vals else 0, 1),
            ))
        step_tuples.sort(reverse=True)
        step_labels    = [t[1] for t in step_tuples]
        step_page_load = [t[0] for t in step_tuples]
        step_lcp       = [t[2] for t in step_tuples]

        # ── KPI averages + ratings ────────────────────────────────────────────
        kpi = {}
        for field in ('LCP_ms', 'INP_ms', 'CLS', 'TTFB_ms', 'FCP_ms'):
            vals = [r[field] for r in rows if r.get(field) is not None]
            avg  = round(mean(vals), 3) if vals else None
            kpi[field] = {'avg': avg, 'rating': self._classify_rating(field, avg)}

        # ── Radar: normalised 0-100 score per region (higher = better) ───────
        radar_fields = ['LCP_ms', 'INP_ms', 'CLS', 'TTFB_ms', 'pageLoadTime_ms']
        radar_labels = ['LCP', 'INP', 'CLS', 'TTFB', 'Page Load']
        radar_poor   = [4000,  500,   0.25,  1800,   5000]     # "poor" anchor
        palette = ['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']
        radar_datasets = []
        for i, (loc, data) in enumerate(self.aggregated_data['by_location'].items()):
            loc_rows = [r for s in data['sessions'] for r in s['rows']]
            scores = []
            for field, poor_thresh in zip(radar_fields, radar_poor):
                vals = [r[field] for r in loc_rows if r.get(field) is not None]
                avg  = mean(vals) if vals else poor_thresh
                scores.append(max(0, round(100 * (1 - avg / poor_thresh), 1)))
            color = palette[i % len(palette)]
            radar_datasets.append({
                'label': self._location_to_region(loc),
                'data': scores,
                'borderColor': color,
                'backgroundColor': color + '28',
                'pointBackgroundColor': color,
                'pointRadius': 4,
                'borderWidth': 2,
            })

        return {
            'lcp_donut': donut_data['LCP_ms'],
            'inp_donut': donut_data['INP_ms'],
            'cls_donut': donut_data['CLS'],
            'regional':  {
                'labels':   region_labels,
                'lcp':      reg_lcp,
                'fcp':      reg_fcp,
                'ttfb':     reg_ttfb,
                'pageLoad': reg_page_load,
            },
            'steps': {
                'labels':      step_labels,
                'avgPageLoad': step_page_load,
                'avgLCP':      step_lcp,
            },
            'radar': {'labels': radar_labels, 'datasets': radar_datasets},
            'kpi':   kpi,
        }

    def _generate_executive_header(self) -> str:
        """Compact horizontal hierarchy bar for the executive report."""
        meta = self.metadata
        locations = list(self.aggregated_data['by_location'].keys())
        loc_chips = ''.join(f'<span class="loc-chip">{loc}</span>' for loc in locations)
        fields = [
            ('Account',   meta.get('accountName',   'N/A')),
            ('Workspace', meta.get('workspaceName',  'N/A')),
            ('Project',   meta.get('projectName',    'N/A')),
            ('Test',      meta.get('testCaseName',   'N/A')),
            ('Master',    meta.get('testMasterName', 'N/A')),
        ]
        badges = ''
        for i, (lbl, val) in enumerate(fields):
            if i > 0:
                badges += '<span class="hier-sep">›</span>'
            badges += f'<div class="hier-badge"><span class="lbl">{lbl}</span><span class="val">{val}</span></div>'
        badges += '<span class="hier-sep">›</span>'
        badges += f'<div class="hier-badge"><span class="lbl">Regions</span><div class="loc-list">{loc_chips}</div></div>'
        return f'<div class="hierarchy-bar">{badges}</div>'

    def _generate_kpi_scorecard(self, chart_data: dict) -> str:
        """Render KPI scorecard cards with rating badges."""
        kpi = chart_data['kpi']
        rating_cfg = {
            'good':             ('good',    '✓ Good'),
            'needs_improvement':('warning', '⚠ Needs Improvement'),
            'poor':             ('poor',    '✗ Poor'),
            'unknown':          ('unknown', '— N/A'),
        }
        fields = [
            ('LCP_ms',  'LCP',  'ms'),
            ('INP_ms',  'INP',  'ms'),
            ('CLS',     'CLS',  ''),
            ('TTFB_ms', 'TTFB', 'ms'),
            ('FCP_ms',  'FCP',  'ms'),
        ]
        cards = ''
        for field, label, unit in fields:
            d = kpi.get(field, {'avg': None, 'rating': 'unknown'})
            css, badge_text = rating_cfg.get(d['rating'], rating_cfg['unknown'])
            val = f"{d['avg']:.1f}" if d['avg'] is not None else 'N/A'
            cards += (
                f'<div class="kpi-card kpi-{css}">'
                f'<div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{val}<span class="kpi-unit">{unit}</span></div>'
                f'<div class="kpi-badge badge-{css}">{badge_text}</div>'
                f'</div>'
            )
        total_steps = len(self.aggregated_data['all_rows'])
        n_regions   = len(self.aggregated_data['by_location'])
        cards += (
            f'<div class="kpi-card kpi-neutral">'
            f'<div class="kpi-label">Steps Measured</div>'
            f'<div class="kpi-value">{total_steps}</div>'
            f'<div class="kpi-badge badge-neutral">{n_regions} Regions</div>'
            f'</div>'
        )
        return f'<div class="kpi-grid">{cards}</div>'

    def _generate_executive_summary_table(self, chart_data: dict) -> str:
        """Regional summary table with per-metric averages and LCP rating badge."""
        rating_cfg = {
            'good':             ('badge-good',    '✓ Good'),
            'needs_improvement':('badge-warning', '⚠ NI'),
            'poor':             ('badge-poor',    '✗ Poor'),
            'unknown':          ('badge-unknown', '—'),
        }
        regional = chart_data['regional']
        kpi_per_region = []
        for i, (loc, data) in enumerate(self.aggregated_data['by_location'].items()):
            loc_rows = [r for s in data['sessions'] for r in s['rows']]
            def _avg(f):
                v = [r[f] for r in loc_rows if r.get(f) is not None]
                return round(mean(v), 2) if v else None
            lcp_avg = _avg('LCP_ms')
            kpi_per_region.append({
                'region':    regional['labels'][i],
                'lcp':       lcp_avg,
                'inp':       _avg('INP_ms'),
                'cls':       _avg('CLS'),
                'ttfb':      _avg('TTFB_ms'),
                'page_load': _avg('pageLoadTime_ms'),
                'rating':    self._classify_rating('LCP_ms', lcp_avg),
            })

        rows_html = ''
        for r in kpi_per_region:
            css, badge_text = rating_cfg.get(r['rating'], rating_cfg['unknown'])
            def _fmt(v, decimals=1):
                return f'{v:.{decimals}f}' if v is not None else 'N/A'
            rows_html += (
                f'<tr>'
                f'<td><strong>{r["region"]}</strong></td>'
                f'<td>{_fmt(r["lcp"])} <span class="badge-tbl {css}">{badge_text}</span></td>'
                f'<td>{_fmt(r["inp"])}</td>'
                f'<td>{_fmt(r["cls"], 3)}</td>'
                f'<td>{_fmt(r["ttfb"])}</td>'
                f'<td>{_fmt(r["page_load"])}</td>'
                f'</tr>'
            )

        return (
            f'<div class="card">'
            f'<div class="card-title">Regional Summary</div>'
            f'<table><thead><tr>'
            f'<th>Region</th><th>LCP (ms)</th><th>INP (ms)</th>'
            f'<th>CLS</th><th>TTFB (ms)</th><th>Page Load (ms)</th>'
            f'</tr></thead><tbody>{rows_html}</tbody></table>'
            f'</div>'
        )

    def _load_executive_template(self) -> str:
        """Load executive template and inject all dynamic tokens."""
        if not self.EXECUTIVE_TEMPLATE_FILE.exists():
            raise FileNotFoundError(f'Executive template not found: {self.EXECUTIVE_TEMPLATE_FILE}')

        chart_data = self._build_executive_chart_data()

        html = self.EXECUTIVE_TEMPLATE_FILE.read_text(encoding='utf-8')
        html = html.replace('{{MASTER_ID}}',        str(self.metadata.get('testMasterId', 'N/A')))
        html = html.replace('{{TEST_MASTER_NAME}}', self.metadata.get('testMasterName', 'N/A'))
        html = html.replace('{{GENERATED_AT}}',     datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))
        html = html.replace('{{HEADER_SECTION}}',   self._generate_executive_header())
        html = html.replace('{{KPI_SCORECARD}}',    self._generate_kpi_scorecard(chart_data))
        html = html.replace('{{SUMMARY_TABLE}}',    self._generate_executive_summary_table(chart_data))
        html = html.replace('{{CHART_DATA_JSON}}',  json.dumps(chart_data, ensure_ascii=False))
        return html

    def generate_html(self) -> str:
        """Generate comprehensive HTML report."""
        if self.report_style == 'basic':
            return self._load_basic_template()
        if self.report_style == 'detailed':
            return self._load_detailed_template()
        if self.report_style == 'executive':
            return self._load_executive_template()

        # Fallback (executive / future styles) — inline skeleton
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Vitals Report - {self.metadata.get('testMasterId', 'N/A')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .header h1 {{ color: #667eea; margin-bottom: 10px; }}
        .hierarchy {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .hierarchy-item {{
            background: #f5f7fa;
            padding: 12px;
            border-radius: 4px;
            border-left: 4px solid #667eea;
        }}
        .hierarchy-item label {{ font-weight: bold; color: #667eea; display: block; font-size: 0.85em; }}
        .hierarchy-item value {{ display: block; color: #333; margin-top: 5px; }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{ color: #667eea; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-card .label {{ font-size: 0.9em; opacity: 0.9; }}
        .metric-card .value {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
        .metric-card .unit {{ font-size: 0.8em; opacity: 0.8; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{ background: #f9f9f9; }}
        .chart-container {{
            position: relative;
            height: 300px;
            margin-bottom: 20px;
        }}
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            border-bottom: 1px solid #ddd;
        }}
        .tab-btn {{
            padding: 10px 20px;
            background: none;
            border: none;
            cursor: pointer;
            color: #667eea;
            font-weight: 600;
            border-bottom: 3px solid transparent;
        }}
        .tab-btn.active {{
            border-bottom-color: #667eea;
        }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .stats-table {{
            font-size: 0.9em;
        }}
        .stats-table td {{
            padding: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {self._generate_header()}
        {self._generate_summary()}
        {self._generate_by_location()}
        {self._generate_by_step()}
        {self._generate_raw_data()}
    </div>
</body>
</html>
"""
        return html
    
    def _generate_header(self) -> str:
        """Generate header section with BlazeMeter hierarchy."""
        meta = self.metadata
        account_name = meta.get('accountName', 'N/A')
        workspace_name = meta.get('workspaceName', 'N/A')
        project_name = meta.get('projectName', 'N/A')
        test_name = meta.get('testCaseName', 'N/A')
        master_name = meta.get('testMasterName', 'N/A')
        locations = ''.join(
            f'<div>{location}</div>' for location in self.aggregated_data['by_location'].keys()
        ) or 'N/A'
        
        return f"""
        <div class="header">
            <h1>Web Vitals Performance Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <div class="hierarchy">
                <div class="hierarchy-item">
                    <label>Account</label>
                    <value>{account_name}</value>
                </div>
                <div class="hierarchy-item">
                    <label>Workspace</label>
                    <value>{workspace_name}</value>
                </div>
                <div class="hierarchy-item">
                    <label>Project</label>
                    <value>{project_name}</value>
                </div>
                <div class="hierarchy-item">
                    <label>Test Case</label>
                    <value>{test_name}</value>
                </div>
                <div class="hierarchy-item">
                    <label>Master</label>
                    <value>{master_name}</value>
                </div>
                <div class="hierarchy-item">
                    <label>Locations</label>
                    <value>{locations}</value>
                </div>
            </div>
        </div>
"""
    
    def _generate_summary(self) -> str:
        """Generate summary statistics."""
        if not self.aggregated_data['all_rows']:
            return '<div class="section"><p>No data available</p></div>'
        
        metrics_html = '<div class="metrics-grid">'
        
        # Calculate summary stats for key metrics
        for field in ['LCP_ms', 'INP_ms', 'CLS', 'TTFB_ms', 'FCP_ms', 'pageLoadTime_ms']:
            values = [row.get(field) for row in self.aggregated_data['all_rows']]
            stats = self._calculate_stats(values)
            
            if stats['mean'] is not None:
                metrics_html += f"""
                <div class="metric-card">
                    <div class="label">{self.NUMERIC_FIELDS.get(field, field)}</div>
                    <div class="value">{stats['mean']:.1f}</div>
                    <div class="unit">Avg | Min: {stats['min']:.1f} | Max: {stats['max']:.1f}</div>
                </div>
                """
        
        metrics_html += '</div>'
        
        return f"""
        <div class="section">
            <h2>Executive Summary</h2>
            {metrics_html}
            <p><strong>Total Steps Measured:</strong> {len(self.aggregated_data['all_rows'])}</p>
            <p><strong>Locations:</strong> {', '.join(self.aggregated_data['by_location'].keys())}</p>
        </div>
        """
    
    def _generate_by_location(self) -> str:
        """Generate section with metrics by location."""
        if not self.aggregated_data['by_location']:
            return ''
        
        html = '<div class="section"><h2>Performance by Location</h2>'
        
        for location, data in self.aggregated_data['by_location'].items():
            html += f'<h3>{location}</h3>'
            html += f'<p><strong>Sessions:</strong> {len(data["sessions"])}</p>'
            
            # Create stats table
            html += '<table class="stats-table"><thead><tr>'
            html += '<th>Metric</th><th>Min</th><th>Max</th><th>Mean</th><th>StdDev</th>'
            html += '</tr></thead><tbody>'
            
            for field in ['LCP_ms', 'INP_ms', 'CLS', 'TTFB_ms', 'FCP_ms', 'pageLoadTime_ms']:
                values = []
                for session in data['sessions']:
                    for row in session['rows']:
                        if row.get(field) is not None:
                            values.append(row[field])
                
                stats = self._calculate_stats(values)
                html += f'<tr><td>{self.NUMERIC_FIELDS.get(field, field)}</td>'
                min_val = f'{stats["min"]:.1f}' if stats["min"] is not None else 'N/A'
                max_val = f'{stats["max"]:.1f}' if stats["max"] is not None else 'N/A'
                mean_val = f'{stats["mean"]:.1f}' if stats["mean"] is not None else 'N/A'
                stdev_val = f'{stats.get("stdev"):.1f}' if stats.get("stdev") is not None else 'N/A'
                html += f'<td>{min_val}</td>'
                html += f'<td>{max_val}</td>'
                html += f'<td>{mean_val}</td>'
                html += f'<td>{stdev_val}</td>'
                html += '</tr>'
            
            html += '</tbody></table>'
        
        html += '</div>'
        return html
    
    def _generate_by_step(self) -> str:
        """Generate section with metrics by test step."""
        if not self.aggregated_data['by_step']:
            return ''
        
        html = '<div class="section"><h2>Performance by Test Step</h2>'
        html += '<table><thead><tr>'
        html += '<th>Step Name</th><th>URL</th><th>LCP (ms)</th><th>INP (ms)</th><th>CLS</th><th>Page Load (ms)</th>'
        html += '</tr></thead><tbody>'
        
        for step, rows in sorted(self.aggregated_data['by_step'].items()):
            if rows:
                first_row = rows[0]
                html += '<tr>'
                html += f'<td>{step}</td>'
                html += f'<td>{first_row.get("url", "N/A")}</td>'
                
                # Calculate averages for this step
                lcp_values = [r.get('LCP_ms') for r in rows if r.get('LCP_ms') is not None]
                inp_values = [r.get('INP_ms') for r in rows if r.get('INP_ms') is not None]
                cls_values = [r.get('CLS') for r in rows if r.get('CLS') is not None]
                pload_values = [r.get('pageLoadTime_ms') for r in rows if r.get('pageLoadTime_ms') is not None]
                
                lcp_str = f'{mean(lcp_values):.1f}' if lcp_values else 'N/A'
                inp_str = f'{mean(inp_values):.1f}' if inp_values else 'N/A'
                cls_str = f'{mean(cls_values):.3f}' if cls_values else 'N/A'
                pload_str = f'{mean(pload_values):.1f}' if pload_values else 'N/A'
                
                html += f'<td>{lcp_str}</td>'
                html += f'<td>{inp_str}</td>'
                html += f'<td>{cls_str}</td>'
                html += f'<td>{pload_str}</td>'
                html += '</tr>'
        
        html += '</tbody></table></div>'
        return html
    
    def _generate_raw_data(self) -> str:
        """Generate section with raw data table."""
        if not self.aggregated_data['all_rows']:
            return ''
        
        html = '<div class="section"><h2>Raw Data</h2>'
        html += '<table><thead><tr>'
        html += '<th>Timestamp</th><th>Test Name</th><th>Step Name</th><th>URL</th>'
        for field in ['LCP_ms', 'INP_ms', 'CLS', 'TTFB_ms', 'pageLoadTime_ms', 'FPS']:
            html += f'<th>{self.NUMERIC_FIELDS.get(field, field)}</th>'
        html += '</tr></thead><tbody>'
        
        for row in self.aggregated_data['all_rows'][:100]:  # Limit to first 100 rows
            html += '<tr>'
            html += f'<td>{row.get("timestamp", "N/A")}</td>'
            html += f'<td>{row.get("testName", "N/A")}</td>'
            html += f'<td>{row.get("stepName", "N/A")}</td>'
            html += f'<td>{row.get("url", "N/A")}</td>'
            for field in ['LCP_ms', 'INP_ms', 'CLS', 'TTFB_ms', 'pageLoadTime_ms', 'FPS']:
                value = row.get(field, 'N/A')
                html += f'<td>{value if isinstance(value, str) else f"{value:.2f}" if value is not None else "N/A"}</td>'
            html += '</tr>'
        
        html += '</tbody></table>'
        if len(self.aggregated_data['all_rows']) > 100:
            html += f'<p><em>Showing 100 of {len(self.aggregated_data["all_rows"])} rows</em></p>'
        html += '</div>'
        
        return html
    
    def save_report(self, output_file: str = None) -> str:
        """Save HTML report to file."""
        if output_file is None:
            master_id = self.metadata.get('testMasterId', 'unknown')
            master_name = self.metadata.get('testMasterName', 'unknown')
            master_slug = self._slugify(master_name)
            report_style_slug = self._slugify(self.report_style)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.execution_dir / f'web-vitals-{report_style_slug}-report-{master_slug}-{master_id}-{timestamp}.html'
        else:
            output_file = Path(output_file)
        
        html_content = self.generate_html()
        output_file.write_text(html_content, encoding='utf-8')
        return str(output_file)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_web_vitals_report.py <execution_directory> [--report-style basic|detailed|executive]")
        print("Example: python generate_web_vitals_report.py web_vitals_process/blz_masterid_82173056_20260527_143022 --report-style executive")
        sys.exit(1)

    exec_dir = sys.argv[1]
    report_style = 'detailed'

    if len(sys.argv) >= 4 and sys.argv[2] == '--report-style':
        report_style = sys.argv[3]

    if report_style not in {'basic', 'detailed', 'executive'}:
        print(f"Error: Unsupported report style: {report_style}")
        sys.exit(1)

    if not Path(exec_dir).exists():
        print(f"Error: Directory not found: {exec_dir}")
        sys.exit(1)

    generator = WebVitalsReportGenerator(exec_dir, report_style=report_style)
    report_file = generator.save_report()
    print(f"Report generated: {report_file}")
