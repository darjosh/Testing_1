import os
from pathlib import Path
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Package name
package_name = "mongodb_connect"

# List of file paths
list_of_files = [
    ".github/workflows/ci.yml",
    ".github/workflows/python-publish.yaml",
    "src/__init__.py",
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/mongo_crud.py",
    "src/database_automation/__init__.py",
    "src/database_automation/data_ingestion.py",
    "src/database_automation/data_transformation.py",
    "src/database_automation/model_trainer.py",
    "src/database_automation/model_evaluation.py",
    "src/utils/__init__.py",
    "src/utils/utils.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/unit/unit.py",
    "tests/integration/__init__.py",
    "tests/integration/int.py",
    "init_setup.sh",
    "requirements.txt",
    "requirements_dev.txt",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "tox.ini",
    "experiments/experiments.ipynb"
]

# Iterate over the list of files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # create an empty file
