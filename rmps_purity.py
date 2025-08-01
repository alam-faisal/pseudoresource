import numpy as np
from tqdm import tqdm
from qaravan.tensorQ import one_copy_projector_ti_subspace

def haar_purity(num_sites, k_copies, local_dim=2, ti=False, scaled=False): 
    """ if scaled, returns purity * r**(num_sites*k_copies) where r is the effective local dimension """
    q = one_copy_projector_ti_subspace(local_dim, num_sites) if ti else local_dim**num_sites
    q_norm = q if scaled else 1
    factors = [(q+i)/q_norm for i in range(k_copies)]
    return np.math.factorial(k_copies)/np.prod(factors)

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
        context.log(f"Resuming with {step} samples for chi {chi} and num_sites {num_sites}")
    else:
        samples, step = [], 0
        context.log("Starting new sampling run for chi {chi} and num_sites {num_sites}")

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

def samples_to_purity_with_error(samples, k_copies):
    samples = np.array(samples, dtype=np.float64)
    transformed = samples**(2 * k_copies)
    mean = np.mean(transformed)
    std_err = np.std(transformed, ddof=1) / np.sqrt(len(transformed))
    return mean, std_err