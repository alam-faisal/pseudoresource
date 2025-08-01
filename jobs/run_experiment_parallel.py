import os
import sys
import yaml
import multiprocessing

# Set up current and root directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ROOT_DIR)

# Define data directory and ensure it exists
DATA_DIR = os.path.join(CURRENT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

from rmps_purity import trace_samples
from qaravan.tensorQ import periodic_rmps, open_rmps_even, ti_rmps, open_rmps_staggered
from qaravan.core import RunContext

# Worker function to run one experiment
def run_experiment(exp_and_args):
    exp, param, resume, max_iter, progress_interval, checkpoint_interval = exp_and_args

    num_sites = exp['num_sites']
    chi = exp['chi']
    run_type = exp['run_type']
    job_name = f"{run_type}_{num_sites}_{chi}"
    checkpoint_file = os.path.join(DATA_DIR, f"{job_name}.pickle")

    context = RunContext(
        max_iter=int(max_iter),
        progress_interval=progress_interval,
        checkpoint_interval=checkpoint_interval,
        checkpoint_file=checkpoint_file,
        resume=resume,
        convergence_check=False
    )

    context.log(f"Running {run_type} with num_sites={num_sites}, chi={chi}, param={param}.")

    if run_type == 'periodic':
        trace_samples(num_sites, chi, context, func=periodic_rmps, scaled=True)
    elif run_type == 'open':
        trace_samples(num_sites, chi, context, func=open_rmps_staggered, scaled=True)
    elif run_type == 'ti':
        trace_samples(num_sites, chi, context, func=ti_rmps, scaled=True)
    elif run_type == 'uniform':
        trace_samples(num_sites, chi, context, func=periodic_rmps, distrib='uniform', param=param, scaled=True)
    elif run_type == 'gaussian':
        trace_samples(num_sites, chi, context, func=periodic_rmps, distrib='gaussian', param=param, scaled=True)
    else:
        raise ValueError("Invalid run type. Choose from: periodic, open, ti, uniform.")

def main(experiments, param=1.0, resume=False, max_iter=1e6,
         progress_interval=1e3, checkpoint_interval=1e4):

    args = [(exp, param, resume, max_iter, progress_interval, checkpoint_interval) for exp in experiments]

    print(os.cpu_count(), "cores available for parallel processing.")
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.map(run_experiment, args)

if __name__ == "__main__":
    import time 
    start = time.time()
    yaml_path = sys.argv[1]
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    experiments = data['experiments']
    param = data.get('param', 1.0)
    resume = data.get('resume', False)
    max_iter = data.get('max_iter', int(1e6))

    # Optional override
    progress_interval = int(1e4)
    checkpoint_interval = int(1e4)

    main(experiments, param, resume, max_iter, progress_interval, checkpoint_interval)
    end = time.time()
    print(f"Total execution time: {end - start:.2f} seconds")
