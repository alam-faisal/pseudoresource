import os

yaml_files = [
    "job04_28_0.yml", "job04_28_1.yml", "job04_28_2.yml", "job04_28_3.yml", 
    "job04_28_4.yml", "job04_28_5.yml", "job04_28_6.yml", "job04_28_7.yml",
    "job04_28_8.yml",
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
run_experiment = os.path.join(CURRENT_DIR, "run_experiment.py")

def submit_sbatch(job_name, command):
    sbatch_file = f"{job_name}.sbatch"
    log_file = f"{job_name}"

    with open(sbatch_file, "w") as f:
        f.write("#!/bin/bash -l\n")
        f.write(f"#SBATCH --job-name={job_name}\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --exclusive\n")
        f.write("#SBATCH --time=2-0:00:00\n")
        f.write("#SBATCH --no-requeue\n")
        f.write("#SBATCH --qos=long\n")
        f.write(f"#SBATCH --output={log_file}.out\n")
        f.write(f"#SBATCH --error={log_file}.err\n")
        f.write("conda activate qaravan-env\n")
        f.write(command + "\n")

    os.system(f"sbatch {sbatch_file}")
    print(f"Submitted job '{job_name}' using YAML: {yaml_file}")

for yaml_file in yaml_files:
    job_name = os.path.splitext(os.path.basename(yaml_file))[0]
    yaml_path = os.path.join(CURRENT_DIR, yaml_file)
    command = f"python {run_experiment} {yaml_path}"
    submit_sbatch(job_name, command)