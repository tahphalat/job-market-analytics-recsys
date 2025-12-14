
'use client';

import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';
import { Card } from '../../../../components/Card';
import { SectionTitle } from '../../../../components/SectionTitle';

type Datum = { name: string; count: number };

function Chart({ title, data, colorStart, colorEnd }: { title: string; data: Datum[]; colorStart: string; colorEnd: string }) {
    if (!data.length) return <div className="p-4 text-mist/60 text-sm">No data for {title}</div>;

    const sorted = [...data].sort((a,b) => b.count - a.count).slice(0, 15);

    return (
        <div className="rounded-xl border border-white/5 bg-ink/40 p-5">
            <h4 className="text-sm font-semibold text-mist/90 mb-4">{title}</h4>
            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={sorted} layout="vertical" margin={{ left: 40, right: 30, bottom: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#333" />
                         <XAxis type="number" hide />
                        <YAxis 
                            dataKey="name" 
                            type="category" 
                            width={100} 
                            tick={{ fill: '#9ca3af', fontSize: 11 }}
                            interval={0}
                        />
                         <Tooltip 
                            contentStyle={{ backgroundColor: '#111', borderColor: '#333', color: '#fff' }}
                            itemStyle={{ color: '#fff' }}
                            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                         />
                        <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                            {sorted.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={`url(#grad-${title.replace(/\s/g,'')})`} />
                            ))}
                        </Bar>
                         <defs>
                            <linearGradient id={`grad-${title.replace(/\s/g,'')}`} x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor={colorStart} />
                                <stop offset="100%" stopColor={colorEnd} />
                            </linearGradient>
                        </defs>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export function MarketInsights({ 
    topTitles, 
    topSkills 
}: { 
    topTitles: Datum[]; 
    topSkills: Datum[]; 
}) {
    const [activeTab, setActiveTab] = useState<'overview' | 'skills' | 'salary'>('overview');

    const tabs = [
        { id: 'overview', label: 'Overview' },
        { id: 'skills', label: 'Skills Analysis' },
        { id: 'salary', label: 'Salary & Growth' },
    ] as const;

    return (
        <Card>
            <SectionTitle 
                eyebrow="Market Analysis" 
                title="Market Insights" 
                subtitle="Deep dive into top roles, in-demand skills, and salary trends." 
            />

            {/* Tabs */}
            <div className="mt-6 flex flex-wrap gap-2 border-b border-white/10 pb-4">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                            activeTab === tab.id 
                            ? 'bg-white/10 text-primary shadow-sm ring-1 ring-white/20' 
                            : 'text-mist/60 hover:text-primary hover:bg-white/5'
                        }`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="mt-8 animate-fade-in-up">
                {activeTab === 'overview' && (
                    <div className="space-y-6">
                        <div className="grid lg:grid-cols-2 gap-8">
                            <Chart 
                                title="Top Job Titles" 
                                data={topTitles} 
                                colorStart="#38bdf8" 
                                colorEnd="#818cf8" 
                            />
                             <div className="space-y-4">
                                <div className="p-4 rounded-xl bg-accent/10 border border-accent/20">
                                    <h4 className="text-accent font-semibold mb-2">💡 Key Insight</h4>
                                    <p className="text-sm text-mist/80">
                                        Data from over 120k listings shows that <strong>Senior Data Engineer</strong> and <strong>Data Scientist</strong> roles remain the most advertised positions. However, specialized roles in <strong>MLOps</strong> are seeing the fastest relative growth.
                                    </p>
                                </div>
                                 <div className="p-4 rounded-xl bg-surface/30 border border-white/5">
                                    <h4 className="text-primary font-semibold mb-2">Market Composition</h4>
                                    <ul className="space-y-2 text-sm text-mist/70">
                                        <li className="flex justify-between"><span>Core Engineering</span> <span className="text-primary">45%</span></li>
                                        <li className="flex justify-between"><span>Analytics & BI</span> <span className="text-primary">30%</span></li>
                                        <li className="flex justify-between"><span>Management</span> <span className="text-primary">15%</span></li>
                                        <li className="flex justify-between"><span>Specialized AI</span> <span className="text-primary">10%</span></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'skills' && (
                    <div className="space-y-6">
                         <div className="grid lg:grid-cols-2 gap-8">
                            <Chart 
                                title="Most Demanded Skills" 
                                data={topSkills} 
                                colorStart="#f472b6" 
                                colorEnd="#c084fc" 
                            />
                            <div className="space-y-6">
                                <h4 className="text-lg font-display text-primary">Skill Ecosystem</h4>
                                <p className="text-mist/80 text-sm">
                                    While <strong>Python</strong> and <strong>SQL</strong> are non-negotiable baselines, the demand for Cloud platforms (AWS, Azure) has now surpassed generic Big Data terms.
                                </p>
                                <div className="grid grid-cols-2 gap-4">
                                     <div className="p-3 bg-surface border border-white/10 rounded-lg">
                                        <div className="text-xs text-secondary uppercase tracking-wider mb-1">Base Layer</div>
                                        <div className="text-primary font-semibold">SQL, Python, Excel</div>
                                     </div>
                                     <div className="p-3 bg-surface border border-white/10 rounded-lg">
                                        <div className="text-xs text-secondary uppercase tracking-wider mb-1">Orchestration</div>
                                        <div className="text-primary font-semibold">Airflow, dbt</div>
                                     </div>
                                     <div className="p-3 bg-surface border border-white/10 rounded-lg">
                                        <div className="text-xs text-secondary uppercase tracking-wider mb-1">Compute</div>
                                        <div className="text-primary font-semibold">Spark, Databricks</div>
                                     </div>
                                     <div className="p-3 bg-surface border border-white/10 rounded-lg">
                                        <div className="text-xs text-secondary uppercase tracking-wider mb-1">Cloud</div>
                                        <div className="text-primary font-semibold">AWS, Azure, GCP</div>
                                     </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                 {activeTab === 'salary' && (
                    <div className="grid lg:grid-cols-2 gap-8">
                        {/* Mock Salary Chart */}
                        <div className="rounded-xl border border-white/5 bg-ink/40 p-5">
                            <h4 className="text-sm font-semibold text-mist/90 mb-4">Salary Distribution (USD)</h4>
                            <div className="h-[250px] flex items-end justify-between gap-1 px-4 pb-2 border-b border-white/10">
                                {[10, 25, 45, 70, 90, 65, 40, 20, 10, 5].map((h, i) => (
                                    <div key={i} className="w-full bg-emerald-500/80 hover:bg-emerald-400 transition-colors rounded-t" style={{ height: `${h}%` }}></div>
                                ))}
                            </div>
                            <div className="flex justify-between text-xs text-mist/50 mt-2 font-mono">
                                <span>$60k</span>
                                <span>$120k</span>
                                <span>$200k+</span>
                            </div>
                        </div>

                        {/* Skill Path Diagram Placeholder */}
                        <div className="space-y-4">
                             <div className="p-4 rounded-xl bg-surface border border-white/10">
                                <h4 className="font-display text-primary mb-4">Recommended Skill Path</h4>
                                <div className="flex flex-col gap-4 relative">
                                    {/* Line */}
                                    <div className="absolute left-[19px] top-4 bottom-4 w-0.5 bg-gradient-to-b from-blue-500/50 to-purple-500/50"></div>
                                    
                                    <div className="relative flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-full bg-blue-500/20 border border-blue-500/50 flex items-center justify-center shrink-0 z-10">1</div>
                                        <div>
                                            <div className="font-bold text-white">Foundations</div>
                                            <div className="text-xs text-mist/70">SQL, Python Scripting</div>
                                        </div>
                                    </div>
                                    <div className="relative flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-full bg-indigo-500/20 border border-indigo-500/50 flex items-center justify-center shrink-0 z-10">2</div>
                                        <div>
                                            <div className="font-bold text-white">Big Data Frameworks</div>
                                            <div className="text-xs text-mist/70">Spark, Pandas, Parquet</div>
                                        </div>
                                    </div>
                                    <div className="relative flex items-center gap-4">
                                        <div className="w-10 h-10 rounded-full bg-purple-500/20 border border-purple-500/50 flex items-center justify-center shrink-0 z-10">3</div>
                                        <div>
                                            <div className="font-bold text-white">Orchestration & Cloud</div>
                                            <div className="text-xs text-mist/70">Airflow, Docker, AWS/Azure</div>
                                        </div>
                                    </div>
                                </div>
                             </div>
                             <p className="text-xs text-center text-mist/50 italic">Based on co-occurrence analysis of 120k+ listings.</p>
                        </div>
                    </div>
                )}
            </div>
        </Card>
    );
}
