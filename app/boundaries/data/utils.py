import logging
import os
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

os.environ["NUMEXPR_MAX_THREADS"] = str(os.cpu_count())
DATABASE = "population_statistics"
