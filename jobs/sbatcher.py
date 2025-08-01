import os

yaml_files = [
    "cjob06_17_00", "cjob06_17_01", "cjob06_17_02", "cjob06_17_03",
    "cjob06_17_04", "cjob06_17_05", "cjob06_17_06", 
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(CURRENT_DIR, "configs")
run_experiment = os.path.join(CURRENT_DIR, "run_experiment_parallel.py")

def submit_sbatch(job_name, command, yaml_file):
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
        f.write("conda activate ~/envs/qaravan-env\n")
        f.write(command + "\n")

    os.system(f"sbatch {sbatch_file}")
    print(f"Submitted job '{job_name}' using YAML: {yaml_file}")

for yaml_file in yaml_files:
    yaml_filename = f"{yaml_file}.yml"
    job_name = yaml_file
    yaml_path = os.path.join(CONFIG_DIR, yaml_filename)
    command = f"python {run_experiment} {yaml_path}"
    submit_sbatch(job_name, command, yaml_filename)