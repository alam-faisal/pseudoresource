import numpy as np
from tqdm import tqdm

def rmps_purity(num_sites, k_copies, chi, func, distrib='isometric',
                samples=5000, local_dim=2, param=1.0, quiet=True):
    """ generates samples and then computes purity; meant for interactive use """
    avg_purity = 0.0
    r = tqdm(range(samples)) if not quiet else range(samples)
    for _ in r:  
        rmps_a = func(num_sites, chi, local_dim, distrib=distrib, param=param)
        rmps_b = func(num_sites, chi, local_dim, distrib=distrib, param=param)           
        avg_purity += np.abs(rmps_a.overlap(rmps_b))**(2*k_copies)
    
    avg_purity /= samples
    return avg_purity

def trace_samples(num_sites, chi, context, func, distrib='isometric', param=1.0, scaled=False): 
    if context.resume:
        samples, step = context.run_state['samples'], context.run_state['step']
        context.log(f"Resuming with {step} samples.")
    else:
        samples, step = [], 0
        context.log("Starting new sampling run.")

    for i in tqdm(range(step, context.max_iter)):
        rmps_a = func(num_sites, chi, local_dim=2, distrib=distrib, param=param)
        rmps_b = func(num_sites, chi, local_dim=2, distrib=distrib, param=param)
        trace = np.abs(rmps_a.overlap(rmps_b, scaled=scaled))
        samples.append(trace)

        run_state = {'step': i + 1, 'samples': samples}
        if context.step_update(run_state):
            break

    return samples

def samples_to_purity(samples, k_copies): 
    """ turns samples to purity """
    return np.sum(np.array(samples)**(2*k_copies)) / len(samples)