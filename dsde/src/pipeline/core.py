import time
import logging
from typing import Callable, Any, List
from functools import wraps

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [PIPELINE] - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("Pipeline")

class Task:
    """Represents a single step in the pipeline (similar to an Airflow Operator)."""
    def __init__(self, func: Callable, name: str = None):
        self.func = func
        self.name = name or func.__name__

    def __call__(self, *args, **kwargs):
        logger.info(f"🟢 STARTING Task: {self.name}")
        start_time = time.time()
        try:
            result = self.func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"✅ COMPLETED Task: {self.name} (Duration: {duration:.2f}s)")
            return result
        except Exception as e:
            logger.error(f"❌ FAILED Task: {self.name} - Error: {e}")
            raise e

class Pipeline:
    """Orchestrator that simulates an Airflow DAG."""
    def __init__(self, name: str):
        self.name = name
        self.tasks: List[Task] = []

    def add_task(self, func: Callable, name: str = None):
        """Register a function as a pipeline task."""
        task = Task(func, name)
        self.tasks.append(task)
        return task

    def run(self):
        """Run all registered tasks sequentially."""
        logger.info(f"🚀 STARTING Pipeline: {self.name}")
        overall_start = time.time()
        
        # Note: In a real Airflow DAG, this would be defined by dependencies.
        # Here we just run what was added implementation-wise.
        # This wrapper is mostly for structure in the actual script.
        pass 
        
    @staticmethod
    def task(name: str = None):
        """Decorator to turn a function into a Task execution wrapper."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                t = Task(func, name)
                return t(*args, **kwargs)
            return wrapper
        return decorator
