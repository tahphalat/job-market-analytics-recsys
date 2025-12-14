'use client';

import Papa from 'papaparse';
import {
  ArtifactsIndex,
  CountRow,
  DemoRecsByProfile,
  KpiSummary,
  SkillGraph
} from './types';

const ARTIFACT_BASE = '/artifacts';

export class ArtifactMissingError extends Error {
  status?: number;
  constructor(path: string, status?: number) {
    super(`Artifact missing: ${path}`);
    this.name = 'ArtifactMissingError';
    this.status = status;
  }
}

function buildUrl(path: string) {
  if (path.startsWith('http')) return path;
  if (path.startsWith('/artifacts/')) return path;
  if (path.startsWith('/')) return `${ARTIFACT_BASE}${path}`;
  return `${ARTIFACT_BASE}/${path}`;
}

async function ensureOk(res: Response, path: string) {
  if (!res.ok) {
    if (res.status === 404) {
      throw new ArtifactMissingError(path, res.status);
    }
    throw new Error(`Failed to load artifact: ${path} (status ${res.status})`);
  }
}

export async function fetchJson<T>(path: string): Promise<T> {
  const url = buildUrl(path);
  const res = await fetch(url, { cache: 'no-store' });
  await ensureOk(res, path);
  return (await res.json()) as T;
}

export async function fetchCsv(path: string): Promise<Record<string, string>[]> {
  const url = buildUrl(path);
  const res = await fetch(url, { cache: 'no-store' });
  await ensureOk(res, path);
  const text = await res.text();
  const parsed = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true
  });
  if (parsed.errors && parsed.errors.length > 0) {
    throw new Error(`Failed to parse CSV: ${path}`);
  }
  return parsed.data.filter(Boolean);
}

export async function loadKpiSummary() {
  return fetchJson<KpiSummary>('kpi_summary.json');
}

export async function loadTopSkills(): Promise<CountRow[]> {
  const rows = await fetchCsv('top_skills.csv');
  return rows
    .map((row) => ({
      value: row.value,
      count: Number(row.count || 0)
    }))
    .filter((row) => !!row.value);
}

export async function loadTopTitles(): Promise<CountRow[]> {
  const rows = await fetchCsv('top_titles.csv');
  return rows
    .map((row) => ({
      value: row.value,
      count: Number(row.count || 0)
    }))
    .filter((row) => !!row.value);
}

export async function loadDemoRecs(): Promise<DemoRecsByProfile> {
  return fetchJson<DemoRecsByProfile>('demo_recs.json');
}

export async function loadSkillGraph(): Promise<SkillGraph> {
  return fetchJson<SkillGraph>('graphs/skill_graph.json');
}

export async function loadArtifactsIndex(): Promise<ArtifactsIndex> {
  return fetchJson<ArtifactsIndex>('index.json');
}
