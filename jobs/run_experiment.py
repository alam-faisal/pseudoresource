import os
import sys
import yaml

# Set up current and root directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(ROOT_DIR)

# Define data directory and ensure it exists
DATA_DIR = os.path.join(CURRENT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

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

        # Save checkpoint file in data/ subdirectory
        checkpoint_file = os.path.join(DATA_DIR, f"{job_name}.pickle")

        context = RunContext(max_iter=max_iter, 
                             progress_interval=progress_interval,
                             checkpoint_interval=checkpoint_interval,
                             checkpoint_file=checkpoint_file, 
                             resume=resume, 
                             convergence_check=False)

        context.log(f"Running {run_type} with num_sites={num_sites}, chi={chi}, param={param}.")

        if run_type == 'periodic':
            trace_samples(num_sites, chi, context, func=periodic_rmps, scaled=True)
        elif run_type == 'open':
            trace_samples(num_sites, chi, context, func=open_rmps_even, scaled=True)
        elif run_type == 'ti':
            trace_samples(num_sites, chi, context, func=ti_rmps, scaled=True)
        elif run_type == 'uniform': 
            trace_samples(num_sites, chi, context, func=open_rmps_even, distrib='uniform', param=param, scaled=True)
        else:
            raise ValueError("Invalid run type. Choose from: periodic, open, ti, uniform.")

if __name__ == "__main__":
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--yaml', type=str, default=None)
    parser.add_argument('--chi', type=int)
    parser.add_argument('--num-sites', type=int)
    parser.add_argument('--run-type', type=str, choices=['periodic', 'open', 'ti', 'uniform'])
    parser.add_argument('--param', type=float, default=1.0)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--max-iter', type=int, default=int(1e6))
    parser.add_argument('--progress-interval', type=int, default=int(1e3))
    parser.add_argument('--checkpoint-interval', type=int, default=int(1e3))

    args = parser.parse_args()

    start = time.time()

    if args.yaml:
        with open(args.yaml, "r") as f:
            data = yaml.safe_load(f)
        experiments = data['experiments']
        param = data.get('param', 1.0)
        resume = data.get('resume', False)
        max_iter = data.get('max_iter', 1000000)
    else:
        if None in (args.chi, args.num_sites, args.run_type):
            parser.error("chi, num-sites, and run-type must be provided if --yaml is not used.")
        experiments = [{
            "chi": args.chi,
            "num_sites": args.num_sites,
            "run_type": args.run_type
        }]
        param = args.param
        resume = args.resume

    main(experiments, param, resume, args.max_iter, args.progress_interval, args.checkpoint_interval)

    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")