'use client';
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [logs, setLogs] = useState<any[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/logs')
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setLogs(data);
        } else if (data.error) {
          setErrorMessage(data.error);
        }
      })
      .catch((err) => setErrorMessage(err.message));
  }, []);

  return (
    <main className="p-8 font-sans max-w-6xl mx-auto text-black">
      <h1 className="text-3xl font-bold mb-6">DevSecOps Command Center</h1>

      {errorMessage && (
        <div className="p-4 mb-6 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <strong>Database Notice:</strong> {errorMessage}
        </div>
      )}

      <div className="overflow-x-auto bg-white shadow-md rounded-lg border border-gray-200">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 border-b">
              <th className="p-4">PR #</th>
              <th className="p-4">Agent Decisions</th>
              <th className="p-4">Security Flags</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log: any, i) => (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="p-4 font-mono">{log.pr_number || 'N/A'}</td>
                <td className="p-4">{log.agent_decisions || 'N/A'}</td>
                <td className="p-4 text-red-600 font-semibold">{log.security_flags || 'None'}</td>
              </tr>
            ))}
            {logs.length === 0 && !errorMessage && (
              <tr>
                <td colSpan={3} className="p-4 text-center text-gray-500">
                  No scans recorded yet. Trigger a PR to populate data!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}