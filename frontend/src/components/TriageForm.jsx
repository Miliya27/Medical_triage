import React, { useState } from 'react';

export default function TriageForm({ onSubmit, loading, onPresetSelect }) {
    const [patientName, setPatientName] = useState('Alex Rivera');
    const [age, setAge] = useState(34);
    const [gender, setGender] = useState('Male');
    const [symptoms, setSymptoms] = useState('Stung by a wasp 15 minutes ago. Patient developed hives across torso, lip swelling, severe wheezing, and lightheadedness.');
    const [allergies, setAllergies] = useState('Penicillin');
    const [currentMedications, setCurrentMedications] = useState('Propranolol');
    const [isListening, setIsListening] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            patient_name: patientName,
            age: parseInt(age) || 30,
            gender: gender,
            symptoms: symptoms,
            allergies: allergies.split(',').map((s) => s.strip ? s.strip() : s.trim()).filter(Boolean),
            current_medications: currentMedications.split(',').map((s) => s.strip ? s.strip() : s.trim()).filter(Boolean)
        });
    };

    const handlePreset = (presetName) => {
        if (presetName === 'anaphylaxis') {
            setSymptoms('Bee sting 10 minutes ago. Rapid lip and facial swelling, widespread urticaria (hives), respiratory stridor, SpO2 dropping.');
            setAllergies('NSAIDs');
            setCurrentMedications('Atenolol');
            onPresetSelect('anaphylaxis');
        } else if (presetName === 'cardiac') {
            setSymptoms('Severe retrosternal crushing chest pain radiating to left jaw and shoulder, diaphoresis, dyspnea.');
            setAllergies('Penicillin');
            setCurrentMedications('Sildenafil 50mg');
            onPresetSelect('cardiac');
        } else if (presetName === 'sepsis') {
            setSymptoms('High fever 39.9°C, rigors, confusion, tachypnea, productive cough with rusty sputum, low BP.');
            setAllergies('Sulfa drugs');
            setCurrentMedications('Metformin');
            onPresetSelect('sepsis');
        } else if (presetName === 'minor') {
            setSymptoms('2cm shallow superficial laceration on left forearm from clean glass edge. Bleeding controlled, full distal sensation.');
            setAllergies('None');
            setCurrentMedications('None');
            onPresetSelect('stable');
        }
    };

    const toggleVoiceInput = () => {
        if (!isListening) {
            setIsListening(true);
            setTimeout(() => {
                setSymptoms((prev) => prev + ' [Voice Transcription]: Patient complaining of severe shortness of breath and chest pressure.');
                setIsListening(false);
            }, 2500);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="glass-card rounded-2xl p-6 border border-slate-800 shadow-xl space-y-5">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2">
                    <span className="text-xl">🩺</span>
                    <h2 className="text-base font-bold text-slate-100">Patient Encounter & Symptom Intake</h2>
                </div>

                {/* Preset Selector */}
                <div className="flex items-center gap-1.5">
                    <span className="text-xs text-slate-400 font-medium hidden sm:inline">Scenarios:</span>
                    <button type="button" onClick={() => handlePreset('anaphylaxis')} className="text-[11px] px-2 py-1 rounded bg-red-950/40 text-red-400 border border-red-800/40 hover:bg-red-900/40 transition">
                        Anaphylaxis
                    </button>
                    <button type="button" onClick={() => handlePreset('cardiac')} className="text-[11px] px-2 py-1 rounded bg-amber-950/40 text-amber-400 border border-amber-800/40 hover:bg-amber-900/40 transition">
                        ACS / Cardiac
                    </button>
                    <button type="button" onClick={() => handlePreset('sepsis')} className="text-[11px] px-2 py-1 rounded bg-yellow-950/40 text-yellow-400 border border-yellow-800/40 hover:bg-yellow-900/40 transition">
                        Sepsis
                    </button>
                    <button type="button" onClick={() => handlePreset('minor')} className="text-[11px] px-2 py-1 rounded bg-emerald-950/40 text-emerald-400 border border-emerald-800/40 hover:bg-emerald-900/40 transition">
                        Minor Trauma
                    </button>
                </div>
            </div>

            {/* Demographics Row */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-1">Patient Name / Identifier</label>
                    <input
                        type="text"
                        value={patientName}
                        onChange={(e) => setPatientName(e.target.value)}
                        required
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                    />
                </div>

                <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-1">Age</label>
                    <input
                        type="number"
                        value={age}
                        onChange={(e) => setAge(e.target.value)}
                        required
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                    />
                </div>

                <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-1">Gender</label>
                    <select
                        value={gender}
                        onChange={(e) => setGender(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                    >
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other / Non-Binary</option>
                    </select>
                </div>
            </div>

            {/* Symptoms Free Text area with Voice Input */}
            <div>
                <div className="flex items-center justify-between mb-1">
                    <label className="block text-xs font-semibold text-slate-400">
                        Presenting Symptoms & Chief Complaint <span className="text-cyan-400">*</span>
                    </label>
                    <button
                        type="button"
                        onClick={toggleVoiceInput}
                        className={`text-xs px-2.5 py-1 rounded-lg border font-medium flex items-center gap-1.5 transition ${isListening
                                ? 'bg-red-500/20 text-red-400 border-red-500/40 animate-pulse'
                                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                            }`}
                    >
                        🎙️ {isListening ? 'Transcribing Voice Input...' : 'Simulate Voice Input'}
                    </button>
                </div>
                <textarea
                    rows={3}
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                    required
                    placeholder="Describe symptoms, onset duration, trigger events, pain intensity..."
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                />
            </div>

            {/* Medical History: Allergies & Meds */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-1">Documented Allergies (Comma separated)</label>
                    <input
                        type="text"
                        value={allergies}
                        onChange={(e) => setAllergies(e.target.value)}
                        placeholder="e.g. Penicillin, NSAIDs, Latex"
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                    />
                </div>

                <div>
                    <label className="block text-xs font-semibold text-slate-400 mb-1">Current Active Medications</label>
                    <input
                        type="text"
                        value={currentMedications}
                        onChange={(e) => setCurrentMedications(e.target.value)}
                        placeholder="e.g. Sildenafil, Warfarin, Propranolol"
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 transition"
                    />
                </div>
            </div>

            {/* Submit Button */}
            <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold py-3 px-6 rounded-xl shadow-lg shadow-cyan-500/20 border border-cyan-300/30 transition-all flex items-center justify-center gap-2 text-sm disabled:opacity-50 cursor-pointer"
            >
                {loading ? (
                    <>
                        <div className="w-5 h-5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                        <span>Executing 3-Agent Pipeline (RAG + Ollama + Drug Check + Escalation)...</span>
                    </>
                ) : (
                    <>
                        <span>⚡ Run 3-Agent Triage Pipeline</span>
                    </>
                )}
            </button>
        </form>
    );
}
