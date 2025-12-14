
'use client';

import { useState } from 'react';
import { DemoProfile, DemoRecsByProfile } from '../../../../src/lib/artifacts/types';
import { Card } from '../../../../components/Card';
import { SectionTitle } from '../../../../components/SectionTitle';

export function RecommendationEngine({ 
    recs, 
    profiles 
}: { 
    recs: DemoRecsByProfile; 
    profiles: DemoProfile[];
}) {
    // Default to first profile if available
    const initialProfile = profiles[0]?.name || Object.keys(recs)[0] || '';
    const [selectedProfile, setSelectedProfile] = useState(initialProfile);

    const activeRecs = recs[selectedProfile] || [];
    const activeProfileData = profiles.find(p => p.name === selectedProfile);

    return (
        <Card>
            <SectionTitle 
                eyebrow="Explainable AI" 
                title="Recommendation Engine" 
                subtitle="Smart job matching based on semantic skills similarity." 
            />

            <div className="mt-8 grid lg:grid-cols-[300px_1fr] gap-8">
                {/* Sidebar / Persona Selector */}
                <div className="space-y-6">
                    <div className="p-4 rounded-xl border border-white/5 bg-ink/40">
                        <label className="text-xs font-mono text-mist/50 uppercase tracking-wider mb-2 block">Select Persona</label>
                        <select 
                            value={selectedProfile}
                            onChange={(e) => setSelectedProfile(e.target.value)}
                            className="w-full bg-surface border border-white/10 rounded-lg p-2 text-sm text-primary focus:ring-accent/50"
                        >
                            {profiles.length > 0 ? (
                                profiles.map(p => <option key={p.name} value={p.name}>{p.name}</option>)
                            ) : (
                                Object.keys(recs).map(k => <option key={k} value={k}>{k}</option>)
                            )}
                        </select>
                         
                         {activeProfileData && (
                            <div className="mt-4 pt-4 border-t border-white/5">
                                <p className="text-xs text-secondary leading-relaxed italic">
                                    &quot;{activeProfileData.profile}&quot;
                                </p>
                            </div>
                         )}
                    </div>
                    
                    <div className="p-4 rounded-xl bg-accent/5 border border-accent/10">
                         <h4 className="text-accent text-sm font-semibold mb-2">How it works</h4>
                         <ul className="text-xs text-mist/70 space-y-2 list-disc pl-4">
                             <li>TF-IDF Vectorization of job descriptions.</li>
                             <li>User profile keyword extraction.</li>
                             <li>Cosine Similarity scoring.</li>
                             <li>Explanation generation based on intersecting terms.</li>
                         </ul>
                    </div>
                </div>

                {/* Results List */}
                <div className="space-y-4">
                     <h3 className="text-sm font-semibold text-mist/90 mb-2">Recommended Jobs ({activeRecs.length})</h3>
                     {activeRecs.length === 0 ? (
                        <div className="text-center py-8 text-mist/50">No recommendations available.</div>
                     ) : (
                        activeRecs.slice(0, 5).map((rec, i) => (
                            <div key={rec.job_id} className="group relative p-4 rounded-xl border border-white/5 bg-surface/30 hover:bg-surface/50 transition-all">
                                <div className="flex justify-between items-start gap-4">
                                     <div>
                                        <h4 className="font-semibold text-primary group-hover:text-highlight transition-colors mb-1">{rec.title}</h4>
                                        <div className="text-xs text-mist/60">{rec.company}</div>
                                     </div>
                                     <div className="flex flex-col items-end">
                                         <div className="text-lg font-bold text-highlight font-mono">
                                            {(rec.score * 100).toFixed(0)}%
                                        </div>
                                         <div className="text-[10px] text-mist/40 uppercase">Match</div>
                                     </div>
                                </div>
                                
                                <div className="mt-3">
                                    <div className="text-xs text-mist/50 mb-1">Why this job?</div>
                                    <div className="flex flex-wrap gap-2">
                                        {rec.reasons.slice(0, 4).map((reason, idx) => (
                                            <span key={idx} className="inline-flex items-center gap-1.5 px-2 py-1 rounded bg-highlight/10 border border-highlight/20 text-xs text-highlight/80">
                                                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                                                {reason}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                {rec.source_url && (
                                     <a href={rec.source_url} target="_blank" rel="noreferrer" className="absolute inset-0 z-10" aria-label="View job" />
                                )}
                            </div>
                        ))
                     )}
                </div>
            </div>
        </Card>
    );
}
