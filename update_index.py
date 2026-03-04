#!/usr/bin/env python3
import json
from datetime import datetime

# Load existing index
with open('reports/index.json', 'r') as f:
    data = json.load(f)

# Define type mappings based on report characteristics
scan_keywords = ['scan', 'candidates', 'analysis', 'theory', 'trade-ideas', 'thesis', 'victims', 'technical-check', 'irl-trade', '13f']
scan_ids = [
    'short-candidates', 'chet-quantum-shorts', 'chet-trade-ideas', 'chet-updated-analysis',
    'ai-victims-trade', 'irl-trade', 'crypto-unwind-theory', 'fnma-fmcc-brief', 
    'fnma-fmcc-exit-analysis', 'quantum-technical-check', 'chartboi-oxy-analysis',
    'q4-13f-analysis', 'sotu-analysis', 'iran-defense-plays', 'put-candidates-analysis'
]

# Add type field to existing reports
for report in data['reports']:
    report_id = report['id'].lower()
    is_scan = any(kw in report_id for kw in scan_ids) or 'scan' in report.get('tags', [])
    report['type'] = 'scan' if is_scan else 'deep-dive'

# New reports to add
new_reports = [
    {
        "id": "q4-13f-analysis-2026-02-25",
        "title": "Q4 2025 13F Analysis: AI & Situational Awareness Thesis",
        "date": "2026-02-25",
        "path": "reports/q4-13f-analysis.md",
        "type": "scan",
        "category": "investment-research",
        "tags": ["13f", "institutional", "ai-infrastructure", "smart-money"],
        "description": "Analysis of Q4 2025 13F filings for institutional positioning in AI names. Top picks: TSM, CEG, GEV, AVGO, VST.",
        "visibility": "public",
        "summary": "Elite hedge funds (Coatue, Tiger Global, Lone Pine) loading AI infrastructure plays. Top conviction: TSM (semiconductor), CEG/VST (nuclear power), GEV (power infrastructure), AVGO (custom AI chips).",
        "author": "Jai Research"
    },
    {
        "id": "sotu-analysis-2026-02-25",
        "title": "State of the Union 2026 - Investment Analysis",
        "date": "2026-02-25",
        "path": "reports/sotu-analysis.md",
        "type": "scan",
        "category": "investment-research",
        "tags": ["macro", "policy", "energy", "defense", "healthcare"],
        "description": "Investment implications from 2026 State of the Union address covering energy, defense, healthcare, and housing policy shifts.",
        "visibility": "public",
        "summary": "Key plays: Energy bullish (drill baby drill), Defense surge ($1.5T budget), Healthcare disruption (direct payments), AI datacenter power requirements, Housing ban on institutional buyers.",
        "author": "Jai Research"
    },
    {
        "id": "iran-defense-plays-2026-03-03",
        "title": "Iran Conflict Defense Plays",
        "date": "2026-03-03",
        "path": "reports/iran-defense-plays.md",
        "type": "scan",
        "category": "investment-research",
        "tags": ["defense", "geopolitical", "drones", "missiles"],
        "description": "Defense stocks positioned for Iran conflict escalation. Comparing KTOS, RTX, LHX, AXON, MPTI.",
        "visibility": "public",
        "summary": "Top picks: KTOS (best upside - counter-drone), RTX (best value), LHX (quality). Skip AXON for Iran play.",
        "author": "Jai Research"
    },
    {
        "id": "put-candidates-analysis-2026-03",
        "title": "Put Candidates Analysis",
        "date": "2026-03-01",
        "path": "reports/put-candidates-analysis.md",
        "type": "scan",
        "category": "investment-research",
        "tags": ["options", "puts", "short-thesis"],
        "description": "Analysis of potential put option candidates based on technical and fundamental factors.",
        "visibility": "public",
        "summary": "Screening for overvalued names with catalyst risk and liquid options markets.",
        "author": "Jai Research"
    },
    {
        "id": "rivn-deep-dive-2026-02",
        "title": "Rivian (RIVN) Deep Dive Research Report",
        "ticker": "RIVN",
        "date": "2026-02-20",
        "path": "reports/rivn-deep-dive.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["ev", "automotive", "growth", "r2-platform"],
        "description": "Comprehensive analysis of Rivian covering R2 platform launch, VW partnership, DOE loan, and production ramp.",
        "visibility": "public",
        "summary": "RIVN at inflection point after first gross profit ($170M Q4). R2 mass-market launch H1 2026. $5.8B VW deal + $6.6B DOE loan fund growth. High execution risk.",
        "rating": "SPECULATIVE",
        "author": "Jai Research"
    },
    {
        "id": "jpm-deep-dive-2026",
        "title": "JPMorgan Chase (JPM) Deep Dive",
        "ticker": "JPM",
        "date": "2026-02-15",
        "path": "reports/jpm-deep-dive.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["banks", "financials", "dividend"],
        "description": "Deep dive on JPMorgan Chase covering banking fundamentals and outlook.",
        "visibility": "public",
        "summary": "Analysis of America's largest bank.",
        "author": "Jai Research"
    },
    {
        "id": "krc-deep-dive-2026",
        "title": "Kilroy Realty (KRC) Deep Dive",
        "ticker": "KRC",
        "date": "2026-02-18",
        "path": "reports/krc-deep-dive.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["reit", "office", "real-estate"],
        "description": "Deep dive on Kilroy Realty office REIT.",
        "visibility": "public",
        "summary": "West Coast office REIT analysis.",
        "author": "Jai Research"
    },
    {
        "id": "HYMC-deep-dive-2026",
        "title": "Hycroft Mining (HYMC) Deep Dive",
        "ticker": "HYMC",
        "date": "2026-02-16",
        "path": "reports/HYMC-deep-dive.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["mining", "gold", "silver", "speculative"],
        "description": "Deep dive on Hycroft Mining gold/silver operations.",
        "visibility": "public",
        "summary": "Speculative mining play analysis.",
        "author": "Jai Research"
    },
    {
        "id": "mpti-deep-dive-2026",
        "title": "M-Tron Industries (MPTI) Deep Dive",
        "ticker": "MPTI",
        "date": "2026-03-02",
        "path": "reports/mpti-deep-dive.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["defense", "frequency-control", "small-cap"],
        "description": "Deep dive on M-Tron Industries frequency control and timing devices.",
        "visibility": "public",
        "summary": "Small-cap defense contractor analysis.",
        "author": "Jai Research"
    },
    {
        "id": "be-short-thesis-2026",
        "title": "Bloom Energy (BE) Short Thesis",
        "ticker": "BE",
        "date": "2026-02-28",
        "path": "reports/be-short-thesis.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["energy", "fuel-cells", "short-thesis"],
        "description": "Short thesis on Bloom Energy covering valuation and competitive concerns.",
        "visibility": "public",
        "summary": "Bear case analysis for Bloom Energy.",
        "rating": "SELL",
        "author": "Jai Research"
    },
    {
        "id": "TAKOF-deep-dive-2026",
        "title": "Drone Delivery Canada (TAKOF) Deep Dive",
        "ticker": "TAKOF",
        "date": "2026-02-22",
        "path": "reports/TAKOF-deep-dive.md",
        "type": "deep-dive",
        "category": "investment-research",
        "tags": ["drones", "delivery", "canada", "speculative"],
        "description": "Deep dive on Drone Delivery Canada operations and outlook.",
        "visibility": "public",
        "summary": "Canadian drone delivery company analysis.",
        "author": "Jai Research"
    }
]

# Add new reports
existing_ids = {r['id'] for r in data['reports']}
for report in new_reports:
    if report['id'] not in existing_ids:
        report['last_updated'] = datetime.now().isoformat() + 'Z'
        data['reports'].append(report)
        print(f"Added: {report['id']}")

# Sort by date descending
data['reports'].sort(key=lambda x: x.get('date', ''), reverse=True)

# Write updated index
with open('reports/index.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nTotal reports: {len(data['reports'])}")
print(f"Deep dives: {sum(1 for r in data['reports'] if r.get('type') == 'deep-dive')}")
print(f"Scans: {sum(1 for r in data['reports'] if r.get('type') == 'scan')}")
