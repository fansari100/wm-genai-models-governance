"use client";

const complianceData = [
  { model: "Document Intelligence", sr117: ["Model Definition", "Effective Challenge", "Monitoring"], nist: ["Content Provenance", "Pre-deployment Testing"], owasp: ["LLM01", "LLM09"], finra: ["Logging", "Version tracking"] },
  { model: "Meeting Summarizer", sr117: ["Model Definition", "Effective Challenge", "Governance", "Monitoring"], nist: ["Governance", "Provenance", "Testing", "Disclosure"], owasp: ["LLM01", "LLM06", "LLM09"], finra: ["Logging", "Version tracking", "PII redaction"] },
  { model: "Risk Narrator", sr117: ["Model Definition", "Effective Challenge"], nist: ["Content Provenance", "Testing"], owasp: ["LLM09"], finra: ["Version tracking"] },
  { model: "Regulatory Detector", sr117: ["Model Definition", "Effective Challenge"], nist: ["Governance", "Testing"], owasp: ["LLM01", "LLM09"], finra: [] },
  { model: "Compliance Checker", sr117: ["Model Definition", "Effective Challenge", "Monitoring"], nist: ["Governance", "Testing"], owasp: ["LLM01", "LLM06"], finra: ["FINRA 2210", "FINRA 2111", "Logging"] },
];

export default function CompliancePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Compliance Framework Mapping</h1>
      <p className="text-sm text-gray-500">Every model mapped to SR 11-7, NIST AI 600-1, OWASP LLM Top 10, and FINRA</p>

      <div className="overflow-x-auto rounded-xl border bg-white shadow-sm">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-[#0A1A3A] text-white">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase">Model</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase">SR 11-7 / OCC</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase">NIST AI 600-1</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase">OWASP LLM 2025</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase">FINRA</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {complianceData.map((c, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium">{c.model}</td>
                <td className="px-4 py-3">{c.sr117.map(s => <span key={s} className="inline-block rounded bg-gray-100 px-1.5 py-0.5 text-[10px] mr-1 mb-1">{s}</span>)}</td>
                <td className="px-4 py-3">{c.nist.map(s => <span key={s} className="inline-block rounded bg-blue-50 px-1.5 py-0.5 text-[10px] text-blue-700 mr-1 mb-1">{s}</span>)}</td>
                <td className="px-4 py-3">{c.owasp.map(s => <span key={s} className="inline-block rounded bg-red-50 px-1.5 py-0.5 text-[10px] text-red-700 mr-1 mb-1">{s}</span>)}</td>
                <td className="px-4 py-3">{c.finra.map(s => <span key={s} className="inline-block rounded bg-green-50 px-1.5 py-0.5 text-[10px] text-green-700 mr-1 mb-1">{s}</span>)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
