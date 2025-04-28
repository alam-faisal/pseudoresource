import os, sys, yaml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ROOT_DIR)

from rmps_purity import trace_samples
from qaravan.tensorQ import periodic_rmps, open_rmps_even, ti_rmps
from qaravan.core import RunContext

def main(experiments, param=1.0, resume=False, max_iter=1e6, 
         progress_interval=1e3, checkpoint_interval=1e4):

    for exp in experiments:
        num_sites = exp['num_sites']
        chi = exp['chi']
        run_type = exp['run_type']
        job_name = f"{run_type}_{num_sites}_{chi}"
        checkpoint_file = os.path.join(CURRENT_DIR, f"{job_name}.pickle")

        context = RunContext(max_iter=max_iter, 
                             progress_interval=progress_interval,
                             checkpoint_interval=checkpoint_interval,
                             checkpoint_file=checkpoint_file, 
                             resume=resume, 
                             convergence_check=False)
        context.log(f"Running {run_type} with num_sites={num_sites}, chi={chi}, param={param}.")

        if run_type == 'periodic':
            trace_samples(num_sites, chi, context, func=periodic_rmps)
        elif run_type == 'open':
            trace_samples(num_sites, chi, context, func=open_rmps_even)
        elif run_type == 'ti':
            trace_samples(num_sites, chi, context, func=ti_rmps)
        elif run_type == 'uniform': 
            trace_samples(num_sites, chi, context, func=open_rmps_even, distrib='uniform', param=param)
        else:
            raise ValueError("Invalid run type. Choose from: periodic, open, ti, uniform.")

if __name__ == "__main__":
    yaml_path = sys.argv[1]
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    experiments = data['experiments']
    param = data.get('param', 1.0)
    resume = data.get('resume', False)

    # Optional override
    max_iter = int(1e6)
    progress_interval = int(1e3)
    checkpoint_interval = int(1e4)

    main(experiments, param, resume, max_iter, progress_interval, checkpoint_interval)