
'use client';

import { useState, useMemo } from 'react';
import { JobLite } from '../../../../src/lib/artifacts/types';
import { Card } from '../../../../components/Card';
import { SectionTitle } from '../../../../components/SectionTitle';
import { Badge } from '../../../../components/Badge';

export function JobBrowser({ jobs }: { jobs: JobLite[] }) {
    const [search, setSearch] = useState('');
    const [hideIncomplete, setHideIncomplete] = useState(false);
    const [page, setPage] = useState(1);
    const PAGE_SIZE = 20;

    const filteredJobs = useMemo(() => {
        let result = jobs;

        if (hideIncomplete) {
            result = result.filter(j => 
                j.salary_min !== undefined && 
                j.company && 
                j.location_text
            );
        }

        if (search.trim()) {
            const terms = search.toLowerCase().trim().split(/\s+/);
            result = result.filter(j => {
                const text = `${j.title} ${j.company} ${j.skills_display} ${j.location_text}`.toLowerCase();
                return terms.every(term => text.includes(term));
            });
        }

        return result;
    }, [jobs, search, hideIncomplete]);

    const totalPages = Math.ceil(filteredJobs.length / PAGE_SIZE);
    const paginatedJobs = filteredJobs.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

    const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(e.target.value);
        setPage(1); // Reset to first page
    };

    return (
        <Card className="min-h-[600px]">
            <SectionTitle 
                eyebrow="Explore" 
                title="Job Browser" 
                subtitle={`Browse ${filteredJobs.length.toLocaleString()} curated job listings.`} 
            />

            {/* Filter Bar */}
            <div className="mt-6 flex flex-col sm:flex-row gap-4">
                <div className="relative flex-grow">
                    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-mist/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <input 
                        type="text" 
                        placeholder="Search by title, company, skills..." 
                        value={search}
                        onChange={handleSearch}
                        className="w-full bg-ink/50 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-primary placeholder-mist/40 focus:outline-none focus:ring-1 focus:ring-accent/50"
                    />
                </div>
                <div className="flex items-center gap-2">
                    <input 
                        type="checkbox" 
                        id="hideInc" 
                        checked={hideIncomplete}
                        onChange={(e) => setHideIncomplete(e.target.checked)}
                        className="rounded border-white/20 bg-ink/50 text-accent focus:ring-accent/50"
                    />
                    <label htmlFor="hideInc" className="text-sm text-mist/80 cursor-pointer select-none">
                        Hide items missing salary
                    </label>
                </div>
            </div>

            {/* Job List */}
            <div className="mt-6 space-y-3">
                {paginatedJobs.length === 0 ? (
                    <div className="text-center py-12 text-mist/50 border border-dashed border-white/10 rounded-xl">
                        No jobs found matching criteria.
                    </div>
                ) : (
                    paginatedJobs.map((job, i) => (
                        <div key={i} className="group relative p-4 rounded-xl border border-white/5 bg-surface/20 hover:bg-surface/40 hover:border-white/10 transition-all">
                            <div className="flex justify-between items-start gap-4">
                                <div>
                                    <h4 className="font-semibold text-primary group-hover:text-accent transition-colors">
                                        {job.title}
                                    </h4>
                                    <div className="text-sm text-mist/70 mt-1">
                                        {job.company} • {job.location_text}
                                    </div>
                                </div>
                                {(job.salary_min !== undefined) && (
                                     <div className="shrink-0 text-right">
                                        <Badge variant="outline" className="border-emerald-500/20 text-emerald-400 bg-emerald-500/5">
                                            ${job.salary_min.toLocaleString()} - ${job.salary_max?.toLocaleString()}
                                        </Badge>
                                     </div>
                                )}
                            </div>
                            
                            {/* Skills */}
                            <div className="mt-3 flex flex-wrap gap-2">
                                {job.skills_display && job.skills_display.split(',').slice(0, 5).map((skill, idx) => (
                                    <span key={idx} className="text-xs px-2 py-0.5 rounded bg-white/5 text-mist/60 border border-white/5">
                                        {skill.trim()}
                                    </span>
                                ))}
                                {job.skills_display && job.skills_display.split(',').length > 5 && (
                                    <span className="text-xs px-2 py-0.5 text-mist/40">+{job.skills_display.split(',').length - 5} more</span>
                                )}
                            </div>

                            <div className="mt-3 flex justify-between items-end border-t border-white/5 pt-3">
                                <span className="text-xs text-mist/40">
                                    Posted {new Date(job.published_at).toLocaleDateString()} via {job.source}
                                </span>
                                {/* <button className="text-xs text-accent opacity-0 group-hover:opacity-100 transition-opacity">View Details →</button> */}
                            </div>
                        </div>
                    ))
                )}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
                <div className="mt-6 flex justify-center items-center gap-4 text-sm">
                    <button 
                        disabled={page === 1}
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        className="px-3 py-1 rounded hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-transparent"
                    >
                        Previous
                    </button>
                    <span className="text-mist/60">
                        Page <span className="text-primary">{page}</span> of {totalPages}
                    </span>
                    <button 
                         disabled={page === totalPages}
                         onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                         className="px-3 py-1 rounded hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-transparent"
                    >
                        Next
                    </button>
                </div>
            )}
        </Card>
    );
}
