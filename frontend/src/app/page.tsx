"use client";

const models = [
  { id: "WM-DOC-INT-001", name: "WM Document Intelligence", version: "1.0.0", type: "extraction", risk: "high", status: "certified", passRate: 0.96, findings: 1, desc: "Extracts structured financial data from prospectuses and fund fact sheets using RAG + LLM structured output" },
  { id: "WM-MTG-SUM-001", name: "Client Meeting Summarizer", version: "1.3.0", type: "summarization", risk: "high", status: "monitoring", passRate: 0.95, findings: 2, desc: "Summarizes advisor-client meetings into structured notes, action items, and compliance flags" },
  { id: "WM-RSK-NAR-001", name: "Portfolio Risk Narrator", version: "1.0.0", type: "generation", risk: "medium", status: "certified", passRate: 0.955, findings: 0, desc: "Generates natural-language risk commentary from portfolio analytics with fact-checking" },
  { id: "WM-REG-DET-001", name: "Regulatory Change Detector", version: "1.0.0", type: "analysis", risk: "medium", status: "testing", passRate: 0.933, findings: 1, desc: "Monitors SEC/FINRA/OCC updates and identifies impact on WM operations" },
  { id: "WM-CMP-CHK-001", name: "Compliance Checker", version: "1.0.0", type: "classification", risk: "high", status: "certified", passRate: 0.96, findings: 1, desc: "Pre-send compliance screening for advisor communications (FINRA 2210)" },
];

const riskColors: Record<string, string> = { critical: "bg-red-600 text-white", high: "bg-red-100 text-red-800", medium: "bg-yellow-100 text-yellow-800", low: "bg-green-100 text-green-800" };
const statusColors: Record<string, string> = { certified: "bg-green-100 text-green-800", monitoring: "bg-blue-100 text-blue-800", testing: "bg-purple-100 text-purple-800", draft: "bg-gray-100 text-gray-600" };

export default function Dashboard() {
  const totalModels = models.length;
  const certified = models.filter(m => m.status === "certified" || m.status === "monitoring").length;
  const avgPass = models.reduce((s, m) => s + m.passRate, 0) / totalModels;
  const openFindings = models.reduce((s, m) => s + m.findings, 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Governance Dashboard</h1>
        <p className="text-sm text-gray-500">5 GenAI vendor models under WM Model Control governance</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total Models", value: totalModels, color: "bg-blue-600" },
          { label: "Certified / Monitoring", value: certified, color: "bg-green-600" },
          { label: "Avg Pass Rate", value: `${(avgPass * 100).toFixed(1)}%`, color: "bg-teal-600" },
          { label: "Open Findings", value: openFindings, color: openFindings > 0 ? "bg-red-600" : "bg-green-600" },
        ].map(s => (
          <div key={s.label} className="rounded-xl border bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">{s.label}</p>
            <p className="text-3xl font-bold mt-1">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="space-y-3">
        {models.map(m => (
          <div key={m.id} className="rounded-xl border bg-white p-5 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-semibold">{m.name}</h3>
                  <span className="text-xs text-gray-400">v{m.version}</span>
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${riskColors[m.risk]}`}>{m.risk.toUpperCase()}</span>
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[m.status]}`}>{m.status}</span>
                </div>
                <p className="text-sm text-gray-600">{m.desc}</p>
                <div className="flex items-center gap-4 mt-2">
                  <span className="text-xs text-gray-500">ID: {m.id}</span>
                  <span className="text-xs text-gray-500">Type: {m.type}</span>
                  <span className="text-xs text-gray-500">Findings: {m.findings}</span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold">{(m.passRate * 100).toFixed(1)}%</p>
                <p className="text-xs text-gray-500">Pass Rate</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="rounded-xl border bg-white p-5 shadow-sm">
        <h3 className="font-semibold mb-3">Compliance Frameworks</h3>
        <div className="flex gap-2 flex-wrap">
          {["SR 11-7", "NIST AI 600-1", "OWASP LLM Top 10 2025", "OWASP Agentic Top 10 2026", "FINRA 2210/2111", "ISO 42001"].map(f => (
            <span key={f} className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700">{f}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
