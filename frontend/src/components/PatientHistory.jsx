import React from 'react';

export default function PatientHistory({ encounters, onSelectEncounter }) {
    if (!encounters || encounters.length === 0) {
        return (
            <div className="glass-card rounded-2xl p-8 border border-slate-800 text-center text-slate-400 space-y-2">
                <span className="text-3xl">📂</span>
                <h3 className="text-base font-bold text-slate-200">No Patient Encounters Recorded Yet</h3>
                <p className="text-xs">Run a triage pipeline to save encounters locally into SQLite.</p>
            </div>
        );
    }

    return (
        <div className="glass-card rounded-2xl p-6 border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                    <span className="text-xl">📂</span>
                    <h2 className="text-base font-bold text-slate-100">SQLite Patient Encounter Log History</h2>
                </div>
                <span className="text-xs font-mono bg-slate-800 text-slate-300 px-2.5 py-1 rounded-lg border border-slate-700">
                    Total Encounters: {encounters.length}
                </span>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-300">
                    <thead className="bg-slate-900/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
                        <tr>
                            <th className="p-3">ID</th>
                            <th className="p-3">Patient Name</th>
                            <th className="p-3">Age / Gender</th>
                            <th className="p-3">Symptoms</th>
                            <th className="p-3">Final Tier</th>
                            <th className="p-3">Alert</th>
                            <th className="p-3">Timestamp</th>
                            <th className="p-3">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {encounters.map((enc) => (
                            <tr key={enc.id} className="hover:bg-slate-900/50 transition">
                                <td className="p-3 font-mono font-bold text-slate-400">#{enc.id}</td>
                                <td className="p-3 font-bold text-slate-100">{enc.patient_name}</td>
                                <td className="p-3">{enc.age} y/o ({enc.gender})</td>
                                <td className="p-3 max-w-xs truncate">{enc.symptoms}</td>
                                <td className="p-3">
                                    <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold font-mono border ${enc.final_triage_tier === 'RED' ? 'bg-red-500/20 text-red-400 border-red-500/40' :
                                            enc.final_triage_tier === 'YELLOW' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40' :
                                                'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                                        }`}>
                                        {enc.final_triage_tier}
                                    </span>
                                </td>
                                <td className="p-3">
                                    {enc.responder_alert_flag ? (
                                        <span className="text-red-400 font-bold">⚠️ YES</span>
                                    ) : (
                                        <span className="text-slate-500">NO</span>
                                    )}
                                </td>
                                <td className="p-3 font-mono text-[11px] text-slate-400">{enc.created_at?.slice(0, 19).replace('T', ' ')}</td>
                                <td className="p-3">
                                    <button
                                        onClick={() => onSelectEncounter(enc)}
                                        className="px-2.5 py-1 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 hover:bg-cyan-900 transition font-medium"
                                    >
                                        View Details
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
