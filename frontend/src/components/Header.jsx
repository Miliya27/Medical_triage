import React from 'react';

export default function Header({ activeTab, setActiveTab, encounterCount }) {
    return (
        <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-4 py-3">
            <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
                {/* Logo & Title */}
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center glow-cyan">
                        <span className="text-2xl">⚡</span>
                    </div>
                    <div>
                        <h1 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                            Off-Grid Medical Triage System
                            <span className="text-xs bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2.5 py-0.5 rounded-full font-mono">
                                100% OFFLINE
                            </span>
                        </h1>
                        <p className="text-xs text-slate-400">
                            3-Agent Autonomous Pipeline • Local Ollama LLM • ChromaDB RAG • SQLite Storage
                        </p>
                    </div>
                </div>

                {/* Navigation Tabs */}
                <div className="flex items-center gap-2 bg-slate-850 p-1 rounded-xl border border-slate-800">
                    <button
                        onClick={() => setActiveTab('triage')}
                        className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all ${activeTab === 'triage'
                                ? 'bg-cyan-500 text-slate-950 font-bold shadow-lg shadow-cyan-500/20'
                                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                            }`}
                    >
                        📋 Live Triage Pipeline
                    </button>

                    <button
                        onClick={() => setActiveTab('history')}
                        className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${activeTab === 'history'
                                ? 'bg-cyan-500 text-slate-950 font-bold shadow-lg shadow-cyan-500/20'
                                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                            }`}
                    >
                        📂 Patient History
                        {encounterCount > 0 && (
                            <span className="bg-slate-900 text-cyan-400 text-[10px] px-1.5 py-0.2 rounded-full font-mono font-bold">
                                {encounterCount}
                            </span>
                        )}
                    </button>
                </div>
            </div>
        </header>
    );
}
