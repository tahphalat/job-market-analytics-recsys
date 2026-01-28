
import pandas as pd
import shutil
import os
import json

# Paths
SOURCE_CSV = "/Users/tahphalat/CEDT/Intern2026/Project/dsde/data/processed/jobs_canonical.csv"
ARTIFACTS_DIR = "/Users/tahphalat/CEDT/Intern2026/Project/dsde/artifacts"
DEST_DIR = "/Users/tahphalat/CEDT/Intern2026/my-portfolio/public/data"

def main():
    print(f"Reading data from {SOURCE_CSV}...")
    # Read only necessary columns to save memory
    df = pd.read_csv(SOURCE_CSV, usecols=['title', 'company', 'location_text', 'source_url', 'published_at'])
    
    # Take a sample of 50 jobs
    print("Sampling 50 jobs...")
    df_sample = df.sample(n=50).fillna("")
    
    # Rename columns to match frontend expectation
    # Frontend expects: title, company, location, url, date
    df_sample = df_sample.rename(columns={
        'location_text': 'location',
        'source_url': 'url',
        'published_at': 'date'
    })
    
    # Export to JSON
    output_jobs_path = os.path.join(DEST_DIR, "jobs_lite.json")
    print(f"Saving jobs to {output_jobs_path}...")
    df_sample.to_json(output_jobs_path, orient='records')
    
    # Process Artifacts
    print("Processing artifacts...")
    
    # 1. Copy KPI Summary
    src_kpi = os.path.join(ARTIFACTS_DIR, "kpi_summary.json")
    if os.path.exists(src_kpi):
        shutil.copy(src_kpi, os.path.join(DEST_DIR, "kpi_summary.json"))
        print("Copied kpi_summary.json")
    
    # 2. Convert Top Skills CSV to JSON
    src_skills = os.path.join(ARTIFACTS_DIR, "top_skills.csv")
    if os.path.exists(src_skills):
        df_skills = pd.read_csv(src_skills)
        # Rename columns to match frontend expectations: 'name', 'count'
        df_skills = df_skills.rename(columns={'value': 'name', 'count': 'count'})
        
        # Calculate percentage (optional, relative to max or total)
        # For simple bar chart, raw count is fine, frontend can calc percent
        # But let's add a simple percent based on max for the progress bar
        max_val = df_skills['count'].max()
        df_skills['percent'] = ((df_skills['count'] / max_val) * 100).astype(int)
        
        output_skills = os.path.join(DEST_DIR, "skills.json")
        df_skills.to_json(output_skills, orient='records')
        print(f"Converted {src_skills} -> {output_skills}")

    print("Data generation complete.")

if __name__ == "__main__":
    main()
