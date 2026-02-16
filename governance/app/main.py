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


# ── Model Demo API (live inference endpoints) ────────────────

@app.post("/api/models/document-intelligence/extract")
async def demo_document_extract(body: dict):
    """Demo: Extract structured data from a document."""
    text = body.get("text", "")
    if not text:
        return {"error": "Provide 'text' field"}

    # Return sample extraction (LLM call requires API key)
    return {
        "model": "WM Document Intelligence v1.0.0",
        "status": "demo_mode",
        "note": "Set OPENAI_API_KEY for live extraction",
        "sample_output": {
            "fund_name": "Morgan Stanley Growth Fund",
            "ticker": "MSGFX",
            "asset_class": "equity",
            "expense_ratio_pct": 0.85,
            "risk_level": "high",
            "confidence_score": 0.92,
        },
    }


@app.post("/api/models/meeting-summarizer/summarize")
async def demo_meeting_summarize(body: dict):
    """Demo: Summarize a meeting transcript."""
    transcript = body.get("transcript", "")
    if not transcript:
        return {"error": "Provide 'transcript' field"}

    return {
        "model": "Client Meeting Summarizer v1.3.0",
        "status": "demo_mode",
        "sample_output": {
            "summary": "Advisor reviewed client's portfolio allocation (60/30/10) and discussed interest rate risk concerns. Recommended reducing bond duration and increasing international equity exposure by 5%. Also discussed opening a 529 plan for client's daughter.",
            "action_items": [
                {"description": "Reduce bond duration from long-term to intermediate", "owner": "advisor", "priority": "high"},
                {"description": "Increase international equity allocation by 5%", "owner": "advisor", "priority": "normal"},
                {"description": "Open 529 education savings plan", "owner": "operations", "priority": "normal"},
            ],
            "compliance_flags": [],
            "confidence_score": 0.95,
        },
    }


@app.post("/api/models/portfolio-risk-narrator/generate")
async def demo_risk_narrative(body: dict):
    """Demo: Generate risk narrative from portfolio data."""
    return {
        "model": "Portfolio Risk Narrator v1.0.0",
        "status": "demo_mode",
        "sample_output": {
            "executive_summary": "The portfolio returned 8.2% YTD, outperforming the S&P 500 benchmark by 120bps. Risk metrics remain within policy limits, though elevated concentration in Technology (32%) warrants monitoring.",
            "risk_assessment": "Portfolio volatility of 14.2% is consistent with the moderate risk profile. The Sharpe ratio of 1.15 indicates efficient risk-adjusted returns. VaR(95%) at 2.8% suggests maximum daily loss of $280K on a $10M portfolio under normal conditions.",
            "confidence_score": 0.93,
        },
    }


@app.post("/api/models/regulatory-change-detector/analyze")
async def demo_regulatory_analyze(body: dict):
    """Demo: Analyze regulatory document for WM impact."""
    return {
        "model": "Regulatory Change Detector v1.0.0",
        "status": "demo_mode",
        "sample_output": {
            "regulation_title": "FINRA Regulatory Notice 26-03: GenAI Supervision Requirements",
            "regulator": "FINRA",
            "impact_level": "high",
            "summary": "FINRA requires firms to implement supervision procedures for GenAI-generated client communications, including pre-use testing, ongoing monitoring, and record retention.",
            "affected_areas": ["Advisory Communications", "Compliance", "Technology"],
            "genai_implications": "All 5 GenAI models must be reviewed for compliance with new supervision requirements. Meeting Summarizer and Compliance Checker are directly affected.",
            "confidence_score": 0.91,
        },
    }


@app.post("/api/models/compliance-checker/check")
async def demo_compliance_check(body: dict):
    """Demo: Screen communication for compliance violations."""
    text = body.get("text", "")
    if not text:
        return {"error": "Provide 'text' field"}

    # Simple rule-based check for demo
    import re
    violations = []
    promissory = re.findall(r"\b(guarantee[ds]?|risk[\s-]?free|can't lose)\b", text.lower())
    for match in promissory:
        violations.append({
            "type": "promissory_language",
            "severity": "high",
            "evidence": match,
            "regulation": "FINRA Rule 2210(d)(1)(B)",
        })

    return {
        "model": "Compliance Checker v1.0.0",
        "decision": "rejected" if violations else "approved",
        "violations": violations,
        "risk_score": min(1.0, len(violations) * 0.3),
    }
