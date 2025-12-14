
'use client';

import { useState, useEffect, useRef } from 'react';
import { Card } from '../../../../components/Card';
import { SectionTitle } from '../../../../components/SectionTitle';

type Log = {
    id: number;
    timestamp: string;
    message: string;
    type: 'info' | 'success'; 
};

export function RealTimeMonitor() {
    const [isSimulating, setIsSimulating] = useState(false);
    const [logs, setLogs] = useState<Log[]>([]);
    const [eventsProcessed, setEventsProcessed] = useState(0);
    const logContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const mockJobs = [
            "Senior Data Engineer @ TechFlow",
            "Analytics Engineer @ DataCorp",
            "ML Ops Specialist @ AI Solutions",
            "Data Architect @ FinTech Global",
            "BI Developer @ Retail Giant",
            "Python Developer @ StartupX"
        ];
        let interval: NodeJS.Timeout;

        if (isSimulating) {
            interval = setInterval(() => {
                const now = new Date();
                const timeString = now.toLocaleTimeString('en-US', { hour12: false }) + '.' + now.getMilliseconds().toString().padStart(3, '0');
                const job = mockJobs[Math.floor(Math.random() * mockJobs.length)];
                
                const newLog: Log = {
                    id: Date.now(),
                    timestamp: timeString,
                    message: `Ingested new job posting: ${job}`,
                    type: 'success'
                };

                setLogs(prev => [...prev.slice(-19), newLog]); // Keep last 20
                setEventsProcessed(c => c + 1);

                // Auto-scroll
                if (logContainerRef.current) {
                    logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
                }

            }, 800);
        }

        return () => clearInterval(interval);
    }, [isSimulating]);

    return (
        <Card>
            <SectionTitle 
                eyebrow="Live Operations" 
                title="Real-Time Monitor" 
                subtitle="Simulate streaming ingestion layer (Kafka Consumer)." 
            />

            <div className="mt-8 grid lg:grid-cols-3 gap-8">
                {/* Control Panel */}
                <div className="space-y-6">
                    <div className="p-6 rounded-xl border border-white/5 bg-surface/30 flex flex-col items-center justify-center text-center">
                        <div className={`w-3 h-3 rounded-full mb-4 ${isSimulating ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
                        <h4 className="text-primary font-semibold">
                            Status: {isSimulating ? 'Active' : 'Idle'}
                        </h4>
                        <p className="text-xs text-mist/60 mt-1 mb-6">
                            {isSimulating ? 'Consuming topic: jobs-raw' : 'Consumer stopped'}
                        </p>
                        
                        <button
                            onClick={() => setIsSimulating(!isSimulating)}
                            className={`px-6 py-2 rounded-lg font-medium transition-all ${
                                isSimulating 
                                ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20' 
                                : 'bg-emerald-500 text-black hover:bg-emerald-400 border border-emerald-500'
                            }`}
                        >
                            {isSimulating ? 'Stop Simulation' : 'Start Simulation'}
                        </button>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="p-4 rounded-xl border border-white/5 bg-ink/40 text-center">
                             <div className="text-2xl font-mono font-bold text-white">{eventsProcessed}</div>
                             <div className="text-xs text-mist/50 uppercase tracking-wider mt-1">Events</div>
                        </div>
                        <div className="p-4 rounded-xl border border-white/5 bg-ink/40 text-center">
                             <div className="text-2xl font-mono font-bold text-accent">
                                 {isSimulating ? '1.2' : '0'}
                             </div>
                             <div className="text-xs text-mist/50 uppercase tracking-wider mt-1">Evt/Sec</div>
                        </div>
                    </div>
                </div>

                {/* Console Output */}
                <div className="lg:col-span-2 rounded-xl border border-white/10 bg-[#0c0c0c] overflow-hidden flex flex-col font-mono text-xs">
                    <div className="px-4 py-2 border-b border-white/5 bg-white/5 flex justify-between items-center">
                        <span className="text-mist/60">Console Output</span>
                        <div className="flex gap-1.5">
                            <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 border border-red-500/50"></div>
                            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
                            <div className="w-2.5 h-2.5 rounded-full bg-green-500/20 border border-green-500/50"></div>
                        </div>
                    </div>
                    <div 
                        ref={logContainerRef}
                        className="p-4 space-y-2 h-[300px] overflow-y-auto scrollbar-hide"
                    >
                        {!logs.length && !isSimulating && (
                            <div className="text-mist/30 italic text-center mt-10">Waiting for stream start...</div>
                        )}
                        {logs.map(log => (
                            <div key={log.id} className="flex gap-3">
                                <span className="text-mist/40 shrink-0">[{log.timestamp}]</span>
                                <span className={`${log.type === 'success' ? 'text-emerald-400' : 'text-primary'}`}>
                                    {log.type === 'success' && '✓ '}
                                    {log.message}
                                </span>
                            </div>
                        ))}
                         {isSimulating && (
                            <div className="flex gap-3 animate-pulse">
                                <span className="text-mist/40 shrink-0">...</span>
                                <span className="text-mist/30">Listening for new messages</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </Card>
    );
}
