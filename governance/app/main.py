"""
WM GenAI Models Governance — FastAPI Application

Serves:
  1. Governance API: model registry, evaluations, compliance, monitoring
  2. Model Demo API: live endpoints for each of the 5 GenAI models
  3. Frontend: Next.js static build
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from governance.app.registry import (
    get_governance_summary,
    get_model_by_id,
    get_model_registry,
)

app = FastAPI(
    title="WM GenAI Models Governance",
    description="5 Production GenAI Models + Governance System for WM Risk Model Control",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ───────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "service": "wm-genai-models-governance"}


# ── Governance API ───────────────────────────────────────────
@app.get("/api/governance/summary")
async def governance_summary():
    """Dashboard summary of all governed models."""
    return get_governance_summary()


@app.get("/api/governance/models")
async def list_models():
    """List all governed models."""
    return [m.model_dump() for m in get_model_registry()]


@app.get("/api/governance/models/{model_id}")
async def get_model(model_id: str):
    """Get details for a specific model."""
    model = get_model_by_id(model_id)
    if model is None:
        return {"error": "Model not found"}
    return model.model_dump()


@app.get("/api/governance/compliance")
async def compliance_matrix():
    """Compliance mapping for all models."""
    models = get_model_registry()
    return {
        "models": [
            {
                "id": m.id,
                "name": m.name,
                "risk_rating": m.risk_rating.value,
                "compliance": m.compliance.model_dump(),
            }
            for m in models
        ],
        "frameworks": ["SR 11-7", "NIST AI 600-1", "OWASP LLM 2025", "OWASP Agentic 2026", "FINRA"],
    }


@app.get("/api/governance/evaluations")
async def list_evaluations():
    """All evaluation results across all models."""
    models = get_model_registry()
    results = []
    for m in models:
        for e in m.eval_results:
            results.append({
                "model_id": m.id,
                "model_name": m.name,
                **e.model_dump(),
            })
    return results


@app.get("/api/governance/findings")
async def list_findings():
    """Findings summary across all models."""
    models = get_model_registry()
    return [
        {
            "model_id": m.id,
            "model_name": m.name,
            "open_findings": m.open_findings,
            "total_findings": m.total_findings,
            "risk_rating": m.risk_rating.value,
        }
        for m in models
    ]


# ── Model Demo API (live, input-aware endpoints) ─────────────


@app.post("/api/models/document-intelligence/extract")
async def demo_document_extract(body: dict):
    """Extract structured data from financial document text (rule-based demo)."""
    import re

    text = body.get("text", "")
    if not text:
        return {"error": "Provide 'text' field with financial document text"}

    # Rule-based extraction from the actual input text
    fund_name = None
    ticker = None
    expense_ratio = None
    aum = None
    returns = {}
    holdings = []
    risk_level = "medium"
    asset_class = "equity"

    # Extract fund name: look for common patterns
    name_match = re.search(r"(?:The\s+)?([A-Z][A-Za-z\s&]+(?:Fund|Trust|ETF|Portfolio))", text)
    if name_match:
        fund_name = name_match.group(1).strip()

    # Extract ticker
    ticker_match = re.search(r"\(([A-Z]{3,5}X?)\)", text)
    if ticker_match:
        ticker = ticker_match.group(1)

    # Extract expense ratio
    er_match = re.search(r"expense ratio[:\s]+of\s+([\d.]+)%", text, re.IGNORECASE)
    if er_match:
        expense_ratio = float(er_match.group(1))

    # Extract AUM
    aum_match = re.search(r"AUM[:\s]+(?:is\s+)?\$([\d.]+)\s*(billion|million|B|M)", text, re.IGNORECASE)
    if aum_match:
        val = float(aum_match.group(1))
        unit = aum_match.group(2).lower()
        aum = val * 1000 if unit.startswith("b") else val

    # Extract returns
    for period, pattern in [
        ("1_year", r"1-year return[:\s]+(?:is\s+)?([\d.]+)%"),
        ("ytd", r"YTD[:\s]+(?:return\s+)?(?:is\s+)?([\d.]+)%"),
        ("3_year", r"3-year[:\s]+(?:annualized\s+)?(?:return\s+)?([\d.]+)%"),
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            returns[period] = float(m.group(1))

    # Extract holdings
    for hm in re.finditer(r"([A-Z]{2,5})\s*\(([\d.]+)%\)", text):
        holdings.append({"ticker": hm.group(1), "weight_pct": float(hm.group(2))})

    # Determine asset class from keywords
    text_lower = text.lower()
    if "bond" in text_lower or "fixed income" in text_lower:
        asset_class = "fixed_income"
    elif "alternative" in text_lower or "hedge" in text_lower:
        asset_class = "alternatives"
    elif "money market" in text_lower:
        asset_class = "money_market"

    # Determine risk level
    if "aggressive" in text_lower or "high risk" in text_lower:
        risk_level = "high"
    elif "conservative" in text_lower or "low risk" in text_lower:
        risk_level = "low"
    elif any(h.get("weight_pct", 0) > 10 for h in holdings):
        risk_level = "high"

    # Confidence based on how many fields we extracted
    fields_found = sum(1 for x in [fund_name, ticker, expense_ratio, aum] if x is not None)
    confidence = min(1.0, (fields_found + len(returns) + len(holdings)) / 8)

    return {
        "model": "WM Document Intelligence v1.0.0",
        "mode": "rule_based_extraction",
        "input_length": len(text),
        "extraction": {
            "fund_name": fund_name or "Not detected",
            "ticker": ticker,
            "asset_class": asset_class,
            "risk_level": risk_level,
            "expense_ratio_pct": expense_ratio,
            "aum_millions": aum,
            "returns": returns if returns else None,
            "top_holdings": holdings if holdings else None,
            "confidence_score": round(confidence, 2),
        },
        "note": "Rule-based extraction. Set OPENAI_API_KEY for full LLM structured output with 50+ fields.",
    }


@app.post("/api/models/meeting-summarizer/summarize")
async def demo_meeting_summarize(body: dict):
    """Summarize meeting transcript (rule-based demo)."""
    import re

    transcript = body.get("transcript", "")
    if not transcript:
        return {"error": "Provide 'transcript' field"}

    lines = [l.strip() for l in transcript.strip().split("\n") if l.strip()]
    speakers = set()
    topics = []
    action_keywords = []
    compliance_flags = []

    for line in lines:
        # Extract speakers
        speaker_match = re.match(r"^([\w\s]+):", line)
        if speaker_match:
            speakers.add(speaker_match.group(1).strip())

        line_lower = line.lower()

        # Detect topics
        topic_patterns = {
            "portfolio review": r"portfolio|allocation|equity|bond|fixed income",
            "risk discussion": r"risk|volatility|concern|worried|drawdown",
            "retirement planning": r"retire|retirement|401k|ira|pension|social security",
            "estate planning": r"estate|trust|529|education|inheritance",
            "tax planning": r"tax|roth|conversion|deduction|capital gain",
            "insurance": r"insurance|annuit|life insurance|long.term care",
        }
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, line_lower) and topic not in topics:
                topics.append(topic)

        # Detect action items
        if any(kw in line_lower for kw in ["recommend", "should", "let's", "i'll", "we could", "set up", "open", "send"]):
            action_keywords.append(line[:120])

        # Compliance flags
        if any(kw in line_lower for kw in ["guaranteed", "risk-free", "can't lose", "promise"]):
            compliance_flags.append({"flag": "promissory_language", "evidence": line[:100]})
        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", line):
            compliance_flags.append({"flag": "pii_detected", "evidence": "SSN pattern found"})

    # Build summary from detected topics
    summary_parts = []
    if topics:
        summary_parts.append(f"Meeting covered: {', '.join(topics)}.")
    summary_parts.append(f"{len(speakers)} participants identified. {len(action_keywords)} action items detected.")

    return {
        "model": "Client Meeting Summarizer v1.3.0",
        "mode": "rule_based_analysis",
        "input_lines": len(lines),
        "analysis": {
            "summary": " ".join(summary_parts),
            "participants": sorted(speakers),
            "topics_discussed": topics,
            "action_items": [{"description": a, "owner": "advisor"} for a in action_keywords[:5]],
            "compliance_flags": compliance_flags,
            "pii_detected": bool(any(f["flag"] == "pii_detected" for f in compliance_flags)),
            "confidence_score": round(min(1.0, len(topics) / 3), 2),
        },
        "note": "Rule-based analysis. Set OPENAI_API_KEY for full LLM summarization with structured output.",
    }


@app.post("/api/models/portfolio-risk-narrator/generate")
async def demo_risk_narrative(body: dict):
    """Generate risk commentary from portfolio data (rule-based demo)."""
    import json

    raw = body.get("portfolio", "")
    if not raw:
        return {"error": "Provide 'portfolio' field with JSON data"}

    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in 'portfolio' field"}

    total_value = data.get("total_value", 0)
    ytd = data.get("ytd_return_pct", 0)
    vol = data.get("volatility_pct", 0)
    sharpe = data.get("sharpe_ratio", 0)
    client = data.get("client_name", "Client")

    # Generate narrative from the actual data
    commentary = []
    commentary.append(f"Portfolio for {client} with total value ${total_value:,.0f}.")

    if ytd > 0:
        commentary.append(f"Year-to-date return of {ytd}% indicates positive performance.")
    else:
        commentary.append(f"Year-to-date return of {ytd}% — portfolio is underperforming.")

    if vol > 15:
        commentary.append(f"Annualized volatility of {vol}% is above the moderate threshold — risk monitoring warranted.")
    elif vol > 0:
        commentary.append(f"Annualized volatility of {vol}% is within acceptable range.")

    if sharpe > 1:
        commentary.append(f"Sharpe ratio of {sharpe} indicates efficient risk-adjusted returns.")
    elif sharpe > 0:
        commentary.append(f"Sharpe ratio of {sharpe} is below optimal — review return drivers.")

    return {
        "model": "Portfolio Risk Narrator v1.0.0",
        "mode": "rule_based_narrative",
        "input_fields": len(data),
        "narrative": {
            "executive_summary": " ".join(commentary),
            "data_points_used": list(data.keys()),
            "risk_flags": [f"High volatility ({vol}%)" for v in [vol] if v > 15],
            "confidence_score": round(min(1.0, len(data) / 8), 2),
        },
        "note": "Rule-based narrative. Set OPENAI_API_KEY for full LLM commentary with fact-checking.",
    }


@app.post("/api/models/regulatory-change-detector/analyze")
async def demo_regulatory_analyze(body: dict):
    """Analyze regulatory document for WM impact (rule-based demo)."""
    import re

    text = body.get("text", "")
    if not text:
        return {"error": "Provide 'text' field with regulatory document text"}

    text_lower = text.lower()

    # Detect regulator
    regulator = "Unknown"
    for reg, pattern in [("SEC", r"\bSEC\b"), ("FINRA", r"\bFINRA\b"), ("OCC", r"\bOCC\b"), ("CFPB", r"\bCFPB\b"), ("Federal Reserve", r"\bFed\b|\bFederal Reserve\b")]:
        if re.search(pattern, text):
            regulator = reg
            break

    # Detect impact areas
    areas = []
    area_patterns = {
        "Advisory Communications": r"communication|advertising|marketing|correspondence",
        "Compliance": r"compliance|supervision|oversight|control",
        "Technology": r"technology|system|AI|GenAI|model|algorithm",
        "Risk Management": r"risk|model risk|validation|testing",
        "Client Services": r"client|customer|investor|account",
        "Trading": r"trading|execution|order|best execution",
    }
    for area, pattern in area_patterns.items():
        if re.search(pattern, text_lower):
            areas.append(area)

    # Detect urgency
    impact = "medium"
    if any(w in text_lower for w in ["immediately", "effective immediately", "emergency", "urgent"]):
        impact = "critical"
    elif any(w in text_lower for w in ["must", "required", "shall", "mandatory"]):
        impact = "high"
    elif any(w in text_lower for w in ["recommended", "guidance", "best practice"]):
        impact = "medium"

    # GenAI implications
    genai_implications = None
    if any(w in text_lower for w in ["genai", "generative ai", "artificial intelligence", "llm", "large language model"]):
        genai_implications = "This regulation directly impacts GenAI use cases. All governed models should be reviewed for compliance."

    return {
        "model": "Regulatory Change Detector v1.0.0",
        "mode": "rule_based_analysis",
        "input_length": len(text),
        "analysis": {
            "regulator": regulator,
            "impact_level": impact,
            "affected_areas": areas if areas else ["General"],
            "genai_implications": genai_implications,
            "key_requirements": [s.strip() + "." for s in text.split(".") if any(w in s.lower() for w in ["must", "shall", "required"]) and len(s.strip()) > 20][:5],
            "confidence_score": round(min(1.0, (len(areas) + (1 if genai_implications else 0)) / 4), 2),
        },
        "note": "Rule-based analysis. Set OPENAI_API_KEY for full LLM impact assessment.",
    }


@app.post("/api/models/compliance-checker/check")
async def demo_compliance_check(body: dict):
    """Screen communication for compliance violations (fully functional, no API key needed)."""
    import re

    text = body.get("text", "")
    if not text:
        return {"error": "Provide 'text' field with draft communication text"}

    text_lower = text.lower()
    violations = []

    # Promissory language
    for pattern, word in [
        (r"\bguarantee[ds]?\b", "guaranteed"), (r"\brisk[\s-]?free\b", "risk-free"),
        (r"\bcan'?t lose\b", "can't lose"), (r"\bwill definitely\b", "will definitely"),
        (r"\bsure thing\b", "sure thing"), (r"\bno risk\b", "no risk"),
        (r"\bassured returns?\b", "assured returns"),
    ]:
        if re.search(pattern, text_lower):
            match = re.search(pattern, text_lower)
            context = text[max(0, match.start() - 30):match.end() + 30]
            violations.append({
                "type": "promissory_language",
                "severity": "high",
                "description": f"Promissory language: '{word}'",
                "evidence": context.strip(),
                "regulation": "FINRA Rule 2210(d)(1)(B)",
                "fix": f"Remove '{word}' and add risk disclaimers",
            })

    # Performance without disclaimer
    has_performance = bool(re.search(r"\d+\.?\d*%\s*(return|performance|gain|yield|annual)", text_lower))
    has_disclaimer = any(p in text_lower for p in ["past performance", "no guarantee", "may lose value", "not indicative"])
    if has_performance and not has_disclaimer:
        violations.append({
            "type": "missing_disclosure",
            "severity": "high",
            "description": "Performance data cited without required disclaimer",
            "evidence": "Performance percentage found without 'past performance' disclaimer",
            "regulation": "SEC Marketing Rule 206(4)-1",
            "fix": "Add: 'Past performance is not indicative of future results. Investments may lose value.'",
        })

    # PII detection
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", text):
        violations.append({
            "type": "pii_in_external",
            "severity": "high",
            "description": "Social Security Number detected in communication",
            "evidence": "[SSN REDACTED]",
            "regulation": "Reg S-P",
            "fix": "Remove all SSN references",
        })

    # Unbalanced presentation (all positive, no risk)
    positive_words = len(re.findall(r"\b(great|excellent|outstanding|superior|best|top|outperform)\b", text_lower))
    risk_words = len(re.findall(r"\b(risk|loss|decline|volatility|uncertainty|downturn)\b", text_lower))
    if positive_words >= 3 and risk_words == 0:
        violations.append({
            "type": "unbalanced_presentation",
            "severity": "medium",
            "description": f"Unbalanced: {positive_words} positive terms, 0 risk acknowledgements",
            "evidence": "Communication is entirely positive without risk discussion",
            "regulation": "FINRA Rule 2210(d)(1)(A) - Fair and Balanced",
            "fix": "Add balanced discussion of risks and potential downsides",
        })

    # Decision logic
    high_count = sum(1 for v in violations if v["severity"] == "high")
    if high_count >= 2:
        decision = "rejected"
    elif high_count == 1 or len(violations) >= 2:
        decision = "requires_changes"
    elif len(violations) == 0:
        decision = "approved"
    else:
        decision = "requires_changes"

    return {
        "model": "Compliance Checker v1.0.0",
        "mode": "fully_functional",
        "input_length": len(text),
        "decision": decision,
        "violations_count": len(violations),
        "violations": violations,
        "risk_score": round(min(1.0, len(violations) * 0.2 + high_count * 0.3), 2),
        "required_disclosures": (
            ["Past performance is not indicative of future results. Investments may lose value."]
            if has_performance and not has_disclaimer else []
        ),
    }
