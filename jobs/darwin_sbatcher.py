import os

# =================================== #
DATE_PREFIX = "07_30"
script_name = "run_experiment.py"
# =================================== #

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")
yaml_files = sorted([
    f for f in os.listdir(CONFIG_DIR)
    if f.startswith(f"job{DATE_PREFIX}_") and f.endswith(".yml")
])

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
run_experiment = os.path.join(CURRENT_DIR, script_name) 

def submit_sbatch(job_name, command, yaml_file):
    sbatch_file = f"{job_name}.sbatch"
    log_file = f"{job_name}"

    with open(sbatch_file, "w") as f:
        f.write("#!/bin/bash -l\n")
        f.write(f"#SBATCH --job-name={job_name}\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --ntasks=1\n")
        f.write("#SBATCH --cpus-per-task=128\n")
        f.write("#SBATCH --exclusive\n")
        f.write("#SBATCH --time=2-0:00:00\n")
        f.write("#SBATCH --qos=long")
        f.write("#SBATCH --no-requeue\n")
        f.write(f"#SBATCH --output={log_file}.out\n")
        f.write(f"#SBATCH --error={log_file}.err\n\n")
        f.write("conda activate qaravan-env\n")
        f.write(f"python {command} --yaml {yaml_file}\n")
    os.system(f"sbatch {sbatch_file}")

for yaml_file in yaml_files:
    job_name = os.path.splitext(yaml_file)[0]
    full_yaml_path = os.path.join(CONFIG_DIR, yaml_file)
    submit_sbatch(job_name, run_experiment, full_yaml_path)
