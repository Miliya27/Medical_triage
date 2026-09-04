import React from 'react';

export default function VitalsMonitor({ vitals, setVitals, onPresetSelect, sensorMode, setSensorMode }) {
    const getSpO2Status = (val) => val < 90 ? 'bg-red-500/20 text-red-400 border-red-500/40 glow-red' : (val < 95 ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40');
    const getHRStatus = (val) => (val > 120 || val < 45) ? 'bg-red-500/20 text-red-400 border-red-500/40 glow-red' : (val > 100 ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40');
    const getBPStatus = (sys) => (sys < 90 || sys > 170) ? 'bg-red-500/20 text-red-400 border-red-500/40 glow-red' : (sys > 140 ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40');

    return (
        <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
                <div className="flex items-center gap-2.5">
                    <span className="text-xl">🫀</span>
                    <h2 className="text-base font-bold text-slate-100">Live Vitals & Sensor Input</h2>
                    <span className={`text-[11px] font-mono font-semibold px-2 py-0.5 rounded-full border ${sensorMode === 'ble' ? 'bg-indigo-500/20 text-indigo-400 border-indigo-500/40 animate-pulse' : 'bg-cyan-500/20 text-cyan-400 border-cyan-500/40'
                        }`}>
                        {sensorMode === 'ble' ? '📡 BLE Pulse Ox Active' : '⚙️ Simulated Vitals'}
                    </span>
                </div>

                {/* Sensor Mode Toggle & Presets */}
                <div className="flex flex-wrap items-center gap-1.5">
                    <button
                        type="button"
                        onClick={() => setSensorMode(sensorMode === 'ble' ? 'simulated' : 'ble')}
                        className="text-xs px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium border border-slate-700 transition-all"
                    >
                        {sensorMode === 'ble' ? 'Switch to Simulator' : 'Connect BLE Sensor'}
                    </button>

                    <span className="text-slate-600 text-xs font-mono">|</span>

                    <span className="text-xs text-slate-400 font-medium">Presets:</span>
                    {['anaphylaxis', 'cardiac', 'sepsis', 'stable'].map((p) => (
                        <button
                            key={p}
                            type="button"
                            onClick={() => onPresetSelect(p)}
                            className="text-xs px-2 py-0.5 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 capitalize border border-slate-700 transition-all"
                        >
                            {p}
                        </button>
                    ))}
                </div>
            </div>

            {/* Vitals Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                {/* SpO2 Card */}
                <div className={`p-3 rounded-xl border bg-slate-900/60 ${getSpO2Status(vitals.spo2)}`}>
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">SpO2</div>
                    <div className="text-2xl font-black font-mono my-0.5">{vitals.spo2}%</div>
                    <div className="text-[10px] font-medium opacity-80">
                        {vitals.spo2 < 90 ? 'CRITICAL HYPOXIA' : (vitals.spo2 < 95 ? 'Mild Hypoxia' : 'Normal Oxygen')}
                    </div>
                </div>

                {/* Heart Rate Card */}
                <div className={`p-3 rounded-xl border bg-slate-900/60 ${getHRStatus(vitals.heart_rate)}`}>
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Heart Rate</div>
                    <div className="text-2xl font-black font-mono my-0.5">{vitals.heart_rate} <span className="text-xs font-normal">bpm</span></div>
                    <div className="text-[10px] font-medium opacity-80">
                        {vitals.heart_rate > 120 ? 'TACHYCARDIA' : (vitals.heart_rate < 50 ? 'BRADYCARDIA' : 'Normal HR')}
                    </div>
                </div>

                {/* Blood Pressure Card */}
                <div className={`p-3 rounded-xl border bg-slate-900/60 ${getBPStatus(vitals.systolic_bp)}`}>
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Blood Pressure</div>
                    <div className="text-xl font-black font-mono my-0.5">{vitals.systolic_bp}/{vitals.diastolic_bp}</div>
                    <div className="text-[10px] font-medium opacity-80">
                        {vitals.systolic_bp < 90 ? 'SHOCK / HYPOTENSION' : (vitals.systolic_bp > 150 ? 'High BP' : 'Normal BP')}
                    </div>
                </div>

                {/* Respiration Rate */}
                <div className="p-3 rounded-xl border border-slate-800 bg-slate-900/60 text-slate-200">
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Resp Rate</div>
                    <div className="text-2xl font-black font-mono my-0.5">{vitals.respiration_rate} <span className="text-xs font-normal">/min</span></div>
                    <div className="text-[10px] text-slate-400 font-medium">
                        {vitals.respiration_rate > 24 ? 'Tachypnea' : 'Normal'}
                    </div>
                </div>

                {/* Temperature */}
                <div className="p-3 rounded-xl border border-slate-800 bg-slate-900/60 text-slate-200">
                    <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Temp</div>
                    <div className="text-2xl font-black font-mono my-0.5">{vitals.temperature}°C</div>
                    <div className="text-[10px] text-slate-400 font-medium">
                        {vitals.temperature > 38.5 ? 'Fever' : 'Afebrile'}
                    </div>
                </div>
            </div>
        </div>
    );
}
