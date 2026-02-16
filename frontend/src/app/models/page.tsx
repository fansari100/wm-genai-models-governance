"use client";

const models = [
  { id: "WM-DOC-INT-001", name: "WM Document Intelligence", version: "1.0.0", vendor: "WM AI Platform", methodology: "RAG + GPT-5.2 structured output + business rules validation", baseModel: "gpt-5.2", risk: "high", status: "certified", usesRag: true, handlesPii: false, clientFacing: false, dataClass: "confidential", certDate: "2026-01-15", nextRecert: "2026-07-15", owner: "AI Platform Team" },
  { id: "WM-MTG-SUM-001", name: "Client Meeting Summarizer", version: "1.3.0", vendor: "WM Technology", methodology: "GPT-5.2 structured output + Presidio PII + compliance rules + HITL", baseModel: "gpt-5.2", risk: "high", status: "monitoring", usesRag: false, handlesPii: true, clientFacing: true, dataClass: "pii", certDate: "2025-11-01", nextRecert: "2026-05-01", owner: "WM Technology" },
  { id: "WM-RSK-NAR-001", name: "Portfolio Risk Narrator", version: "1.0.0", vendor: "Risk Analytics", methodology: "Data-to-text generation + fact-checking (verifies all numbers against source)", baseModel: "gpt-5.2", risk: "medium", status: "certified", usesRag: false, handlesPii: false, clientFacing: true, dataClass: "confidential", certDate: "2026-02-01", nextRecert: "2026-08-01", owner: "Risk Analytics" },
  { id: "WM-REG-DET-001", name: "Regulatory Change Detector", version: "1.0.0", vendor: "Compliance", methodology: "Semantic embedding + ChromaDB similarity + GPT-5.2 impact analysis", baseModel: "gpt-5.2", risk: "medium", status: "testing", usesRag: true, handlesPii: false, clientFacing: false, dataClass: "internal", certDate: null, nextRecert: null, owner: "Compliance" },
  { id: "WM-CMP-CHK-001", name: "Compliance Checker", version: "1.0.0", vendor: "Compliance", methodology: "GPT-5.2 classification + deterministic rule engine (FINRA 2210/2111)", baseModel: "gpt-5.2", risk: "high", status: "certified", usesRag: false, handlesPii: true, clientFacing: false, dataClass: "confidential", certDate: "2026-02-05", nextRecert: "2026-08-05", owner: "Compliance" },
];

const riskColors: Record<string, string> = { high: "bg-red-100 text-red-800", medium: "bg-yellow-100 text-yellow-800", low: "bg-green-100 text-green-800" };
const statusColors: Record<string, string> = { certified: "bg-green-100 text-green-800", monitoring: "bg-blue-100 text-blue-800", testing: "bg-purple-100 text-purple-800" };

export default function ModelsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Model Inventory</h1>
      <p className="text-sm text-gray-500">Complete registry of all 5 GenAI vendor models under governance</p>

      <div className="space-y-4">
        {models.map(m => (
          <div key={m.id} className="rounded-xl border bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-3">
              <h3 className="font-bold text-lg">{m.name}</h3>
              <span className="text-xs text-gray-400">v{m.version}</span>
              <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${riskColors[m.risk]}`}>{m.risk.toUpperCase()} Risk</span>
              <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${statusColors[m.status]}`}>{m.status}</span>
            </div>
            <p className="text-sm text-gray-600 mb-3"><strong>Methodology:</strong> {m.methodology}</p>
            <div className="grid grid-cols-4 gap-4 text-xs">
              <div><span className="text-gray-500">ID:</span> <span className="font-mono">{m.id}</span></div>
              <div><span className="text-gray-500">Base Model:</span> {m.baseModel}</div>
              <div><span className="text-gray-500">Vendor:</span> {m.vendor}</div>
              <div><span className="text-gray-500">Owner:</span> {m.owner}</div>
              <div><span className="text-gray-500">Data Class:</span> {m.dataClass}</div>
              <div><span className="text-gray-500">Client-Facing:</span> {m.clientFacing ? "Yes" : "No"}</div>
              <div><span className="text-gray-500">Handles PII:</span> {m.handlesPii ? "Yes" : "No"}</div>
              <div><span className="text-gray-500">Uses RAG:</span> {m.usesRag ? "Yes" : "No"}</div>
              <div><span className="text-gray-500">Certified:</span> {m.certDate || "Pending"}</div>
              <div><span className="text-gray-500">Next Recert:</span> {m.nextRecert || "N/A"}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
