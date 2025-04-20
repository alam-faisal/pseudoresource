import os
from itertools import product
import numpy as np

# ========== User Inputs ========== #
n_list = np.arange(4, 100, 2)
chi_list = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
run_types = ['periodic']

resume = False 
param = 1.0
# ================================= #

param_grid = list(product(n_list, chi_list, run_types))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
run_experiment = os.path.join(CURRENT_DIR, "run_experiment.py")

def chicoma_sbatch(job_name, command):
    sbatch_file = f"{job_name}.sbatch"
    log_file = f"{job_name}"

    with open(sbatch_file, "w") as f:
        f.write("#!/bin/bash -l\n")
        f.write(f"#SBATCH --job-name={job_name}\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --exclusive\n")
        f.write("#SBATCH --time=16:00:00\n")
        f.write("#SBATCH --no-requeue\n")
        f.write("#SBATCH -A t26_qams\n")
        f.write(f"#SBATCH --output={log_file}.out\n")
        f.write(f"#SBATCH --error={log_file}.err\n")
        f.write("conda activate qaravan-env\n")
        f.write(command + "\n")

    os.system(f"sbatch {sbatch_file}")

for num_sites, chi, run_type in param_grid:
    job_name = f"{run_type}_{num_sites}_{chi}"
    command = f"python {run_experiment} {num_sites} {chi} {run_type} {param} {int(resume)}"
    chicoma_sbatch(job_name, command)
    print(f"Sbatch job '{job_name}' submitted.")
