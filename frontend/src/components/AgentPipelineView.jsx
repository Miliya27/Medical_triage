import React from 'react';

export default function AgentPipelineView({ result }) {
    if (!result) return null;

    const { agent1_symptom_analysis: a1, agent2_drug_check: a2, agent3_escalation: a3 } = result;

    const getTierColor = (tier) => {
        if (tier === 'RED') return 'bg-red-500/20 border-red-500 text-red-400 glow-red';
        if (tier === 'YELLOW') return 'bg-yellow-500/20 border-yellow-500 text-yellow-400 glow-yellow';
        return 'bg-emerald-500/20 border-emerald-500 text-emerald-400 glow-green';
    };

    return (
        <div className="space-y-6">
            {/* Top Banner: Final Triage Tier Output from Agent 3 */}
            <div className={`glass-card rounded-2xl p-6 border-2 ${getTierColor(a3?.final_triage_tier)} flex flex-col md:flex-row items-center justify-between gap-6 shadow-2xl`}>
                <div className="flex items-center gap-4">
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-3xl font-black font-mono border ${getTierColor(a3?.final_triage_tier)}`}>
                        {a3?.final_triage_tier}
                    </div>
                    <div>
                        <div className="text-xs uppercase tracking-wider font-bold opacity-80 mb-1">Final Escalation Output (Agent 3)</div>
                        <h2 className="text-2xl font-black">{a3?.tier_display || a3?.final_triage_tier}</h2>
                        <p className="text-sm text-slate-300 mt-1 max-w-xl">{a3?.clinical_summary}</p>
                    </div>
                </div>

                <div className="flex flex-col items-end gap-2 text-right">
                    <div className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-slate-400">Composite Risk Score:</span>
                        <span className="text-xl font-black font-mono bg-slate-900 px-3 py-1 rounded-lg border border-slate-700 text-slate-100">
                            {a3?.composite_score} / 10
                        </span>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-slate-400">Responder Alert Flag:</span>
                        <span className={`text-xs font-bold font-mono px-3 py-1 rounded-lg border uppercase ${a3?.responder_alert_flag ? 'bg-red-500/30 text-red-300 border-red-500 animate-pulse' : 'bg-slate-800 text-slate-400 border-slate-700'
                            }`}>
                            {a3?.responder_alert_flag ? '⚠️ RESPONDER ALERT ACTIVE' : 'STANDBY'}
                        </span>
                    </div>
                </div>
            </div>

            {/* 3-Agent Pipeline Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* Agent 1 Card */}
                <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl flex flex-col justify-between">
                    <div>
                        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                            <div className="flex items-center gap-2">
                                <span className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 flex items-center justify-center font-bold text-xs">
                                    1
                                </span>
                                <h3 className="text-sm font-bold text-slate-100">Symptom Analyzer Agent</h3>
                            </div>
                            <span className="text-[10px] font-mono bg-cyan-950/60 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded">
                                RAG + Ollama
                            </span>
                        </div>

                        {/* Suspected Conditions */}
                        <div className="mb-4">
                            <div className="text-xs font-semibold text-slate-400 mb-1">Suspected Conditions</div>
                            <div className="flex flex-wrap gap-1.5">
                                {a1?.suspected_conditions?.map((c, i) => (
                                    <span key={i} className="text-xs px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-700 text-cyan-300 font-medium">
                                        {c}
                                    </span>
                                ))}
                            </div>
                        </div>

                        {/* Primary Concerns */}
                        {a1?.primary_concerns && (
                            <div className="mb-4">
                                <div className="text-xs font-semibold text-slate-400 mb-1">Primary Clinical Concerns</div>
                                <ul className="text-xs text-slate-300 space-y-1 list-disc pl-4">
                                    {a1.primary_concerns.map((p, i) => (
                                        <li key={i}>{p}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* RAG Protocol Citations */}
                        {a1?.retrieved_protocols && (
                            <div className="mb-4">
                                <div className="text-xs font-semibold text-slate-400 mb-1 flex items-center justify-between">
                                    <span>WHO / First-Aid Protocols (RAG)</span>
                                    <span className="text-[10px] text-cyan-400">Local ChromaDB</span>
                                </div>
                                <div className="space-y-1.5">
                                    {a1.retrieved_protocols.map((p, i) => (
                                        <div key={i} className="p-2 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] flex items-center justify-between">
                                            <span className="font-medium text-slate-200 truncate max-w-[200px]">{p.title}</span>
                                            <span className="text-[10px] font-mono bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">
                                                {p.urgency}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="pt-3 border-t border-slate-800/80 text-[11px] text-slate-400 italic">
                        Rationale: "{a1?.rationale}"
                    </div>
                </div>

                {/* Agent 2 Card */}
                <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl flex flex-col justify-between">
                    <div>
                        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                            <div className="flex items-center gap-2">
                                <span className="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-400 border border-purple-500/40 flex items-center justify-center font-bold text-xs">
                                    2
                                </span>
                                <h3 className="text-sm font-bold text-slate-100">Drug & Interaction Agent</h3>
                            </div>
                            <span className="text-[10px] font-mono bg-purple-950/60 text-purple-400 border border-purple-800 px-2 py-0.5 rounded">
                                OpenFDA Formulary
                            </span>
                        </div>

                        {/* Contraindications Flag */}
                        <div className="mb-4">
                            <div className="text-xs font-semibold text-slate-400 mb-1">Safety Status</div>
                            <div className={`p-2.5 rounded-xl border text-xs font-bold flex items-center gap-2 ${a2?.contraindications_found ? 'bg-red-500/20 border-red-500 text-red-400 glow-red' : 'bg-emerald-500/20 border-emerald-500 text-emerald-400'
                                }`}>
                                <span>{a2?.contraindications_found ? '⚠️ CONTRAINDICATIONS DETECTED' : '✅ NO DIRECT CONTRAINDICATIONS'}</span>
                            </div>
                        </div>

                        {/* Warnings list */}
                        {a2?.warnings && a2.warnings.length > 0 && (
                            <div className="mb-4 space-y-2">
                                <div className="text-xs font-semibold text-slate-400">Formulary Warnings</div>
                                {a2.warnings.map((w, i) => (
                                    <div key={i} className="p-2.5 rounded-xl bg-slate-900 border border-amber-900/60 text-xs">
                                        <div className="font-bold text-amber-400 flex items-center justify-between mb-1">
                                            <span>{w.drug} ({w.type})</span>
                                            <span className="text-[10px] bg-amber-950 px-1.5 py-0.5 rounded border border-amber-800">{w.severity}</span>
                                        </div>
                                        <p className="text-slate-300 text-[11px] leading-relaxed">{w.description}</p>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Safe Alternatives */}
                        {a2?.recommended_alternatives && a2.recommended_alternatives.length > 0 && (
                            <div>
                                <div className="text-xs font-semibold text-slate-400 mb-1">Recommended Safe Alternatives</div>
                                <div className="flex flex-wrap gap-1.5">
                                    {a2.recommended_alternatives.map((alt, i) => (
                                        <span key={i} className="text-[11px] px-2 py-0.5 rounded bg-emerald-950/60 border border-emerald-800 text-emerald-300 font-mono">
                                            {alt}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="pt-3 border-t border-slate-800/80 text-[11px] text-slate-400">
                        {a2?.summary}
                    </div>
                </div>

                {/* Agent 3 Card */}
                <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl flex flex-col justify-between">
                    <div>
                        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                            <div className="flex items-center gap-2">
                                <span className="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/40 flex items-center justify-center font-bold text-xs">
                                    3
                                </span>
                                <h3 className="text-sm font-bold text-slate-100">Escalation & Vitals Agent</h3>
                            </div>
                            <span className="text-[10px] font-mono bg-amber-950/60 text-amber-400 border border-amber-800 px-2 py-0.5 rounded">
                                Risk Engine
                            </span>
                        </div>

                        {/* Vitals Flags */}
                        <div className="mb-4">
                            <div className="text-xs font-semibold text-slate-400 mb-1">Vitals Risk Indicators</div>
                            {a3?.vitals_red_flags && a3.vitals_red_flags.length > 0 ? (
                                <div className="space-y-1">
                                    {a3.vitals_red_flags.map((flag, i) => (
                                        <div key={i} className="px-2.5 py-1 rounded bg-red-950/80 border border-red-800 text-red-300 text-xs font-mono font-bold">
                                            🚩 {flag}
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400 text-xs">
                                    No vital sign red flags detected.
                                </div>
                            )}
                        </div>

                        {/* Recommended Disposition */}
                        <div className="mb-4">
                            <div className="text-xs font-semibold text-slate-400 mb-1">Field Disposition Plan</div>
                            <div className="p-3 rounded-xl bg-slate-900 border border-slate-700 text-xs text-slate-200 font-medium">
                                🎯 {a3?.recommended_disposition}
                            </div>
                        </div>
                    </div>

                    <div className="pt-3 border-t border-slate-800/80 text-[11px] text-slate-400">
                        Escalation score calculated combining Agent 1 + Agent 2 + Vitals.
                    </div>
                </div>

            </div>
        </div>
    );
}
