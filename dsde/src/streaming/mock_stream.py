
import time
import random
import pandas as pd
from datetime import datetime

class MockProducer:
    """Simulates a Kafka producer sending new job postings."""
    
    def __init__(self):
        self.tech_stack = ["Python", "SQL", "React", "AWS", "Docker", "Kubernetes", "TypeScript", "Go"]
        
    def generate_job(self):
        """Generates a random job dictionary."""
        return {
            "timestamp": datetime.now().isoformat(),
            "title": f"Senior {random.choice(['Data Engineer', 'Software Engineer', 'Data Scientist'])}",
            "company": f"TechCorp {random.randint(1, 100)}",
            "skills": random.sample(self.tech_stack, k=random.randint(2, 5)),
            "salary": random.randint(80000, 180000)
        }
        
    def stream_jobs(self, count=10, delay=0.5):
        """Yields jobs one by one with a delay."""
        for _ in range(count):
            yield self.generate_job()
            time.sleep(delay)

class MockConsumer:
    """Simulates a Spark/Flink consumer aggregating top skills."""
    
    def __init__(self):
        self.skill_counts = {tech: 0 for tech in ["Python", "SQL", "React", "AWS", "Docker", "Kubernetes", "TypeScript", "Go"]}
        
    def ingest(self, job):
        """Updates internal state based on incoming job."""
        for skill in job["skills"]:
            if skill in self.skill_counts:
                self.skill_counts[skill] += 1
                
    def get_top_skills(self):
        """Returns sorted skills."""
        return sorted(self.skill_counts.items(), key=lambda x: x[1], reverse=True)
