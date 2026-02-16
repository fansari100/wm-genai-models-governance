"use client";

const evals = [
  { model: "WM Document Intelligence", type: "quality_correctness", tests: 25, passed: 24, rate: 0.96, date: "2026-01-10" },
  { model: "WM Document Intelligence", type: "safety_security", tests: 30, passed: 29, rate: 0.967, date: "2026-01-12" },
  { model: "WM Document Intelligence", type: "rag_groundedness", tests: 20, passed: 19, rate: 0.95, date: "2026-01-11" },
  { model: "Meeting Summarizer", type: "quality_correctness", tests: 30, passed: 28, rate: 0.933, date: "2025-10-20" },
  { model: "Meeting Summarizer", type: "safety_security", tests: 40, passed: 38, rate: 0.95, date: "2025-10-22" },
  { model: "Meeting Summarizer", type: "pii_redaction", tests: 15, passed: 15, rate: 1.0, date: "2025-10-21" },
  { model: "Risk Narrator", type: "quality_correctness", tests: 20, passed: 19, rate: 0.95, date: "2026-01-28" },
  { model: "Risk Narrator", type: "fact_verification", tests: 50, passed: 48, rate: 0.96, date: "2026-01-29" },
  { model: "Regulatory Detector", type: "quality_correctness", tests: 15, passed: 14, rate: 0.933, date: "2026-02-10" },
  { model: "Compliance Checker", type: "quality_correctness", tests: 40, passed: 39, rate: 0.975, date: "2026-02-03" },
  { model: "Compliance Checker", type: "safety_security", tests: 25, passed: 24, rate: 0.96, date: "2026-02-04" },
  { model: "Compliance Checker", type: "false_positive_rate", tests: 30, passed: 28, rate: 0.933, date: "2026-02-04" },
];

const typeColors: Record<string, string> = {
  quality_correctness: "bg-blue-100 text-blue-800",
  safety_security: "bg-red-100 text-red-800",
  rag_groundedness: "bg-green-100 text-green-800",
  pii_redaction: "bg-purple-100 text-purple-800",
  fact_verification: "bg-teal-100 text-teal-800",
  false_positive_rate: "bg-orange-100 text-orange-800",
};

export default function EvaluationsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Evaluation Results</h1>
      <p className="text-sm text-gray-500">{evals.length} evaluation runs across all 5 models</p>

      <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Model</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Type</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Tests</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Passed</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Pass Rate</th>
              <th className="px-4 py-3 text-left text-xs font-medium uppercase text-gray-500">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {evals.map((e, i) => (
              <tr key={i} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium">{e.model}</td>
                <td className="px-4 py-3"><span className={`rounded-full px-2 py-0.5 text-xs font-medium ${typeColors[e.type] || "bg-gray-100 text-gray-800"}`}>{e.type.replace(/_/g, " ")}</span></td>
                <td className="px-4 py-3 text-sm">{e.tests}</td>
                <td className="px-4 py-3 text-sm text-green-700 font-medium">{e.passed}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-20 rounded-full bg-gray-100">
                      <div className={`h-2 rounded-full ${e.rate >= 0.95 ? "bg-green-500" : e.rate >= 0.90 ? "bg-yellow-500" : "bg-red-500"}`} style={{ width: `${e.rate * 100}%` }} />
                    </div>
                    <span className="text-sm font-medium">{(e.rate * 100).toFixed(1)}%</span>
                  </div>
                </td>
                <td className="px-4 py-3 text-sm text-gray-500">{e.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
