export type CountRow = {
  value: string;
  count: number;
};

export type KpiSummary = {
  total_jobs: number;
  unique_companies: number;
  sources: {
    kaggle: number;
    remotive: number;
  };
  top_locations?: { location_text: string; count: number }[];
  generated_at?: string;
};

export type DemoRec = {
  job_id: string;
  title: string;
  company: string;
  source: string;
  source_url?: string;
  score: number;
  reasons: string[];
};

export type DemoRecsByProfile = Record<string, DemoRec[]>;

export type DemoProfile = {
  name: string;
  profile: string;
};

export type SourceCount = {
  source: string;
  count: number;
};

export type SkillGraphNode = {
  id: string;
  label: string;
  count?: number;
};

export type SkillGraphEdge = {
  source: string;
  target: string;
  weight?: number;
};

export type SkillGraph = {
  nodes: SkillGraphNode[];
  edges: SkillGraphEdge[];
};

export type ArtifactsIndex = {
  files?: string[];
};

export type JobLite = {
  title: string;
  company: string;
  location_text: string;
  skills_display: string;
  published_at: string;
  salary_min?: number;
  salary_max?: number;
  source: string;
};
