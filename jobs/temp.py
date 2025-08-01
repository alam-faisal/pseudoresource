import os
import pickle
import re
import math

# Pattern to match filenames like open_5_32.pickle
pattern = re.compile(r"open_(\d+)_(\d+)\.pickle")

# Loop over all files in the current directory
for filename in os.listdir('.'):
    match = pattern.match(filename)
    if match:
        n = int(match.group(1))
        chi = int(match.group(2))
        
        # Open the pickle file
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        
        # Check if 'samples' exists and is a list
        if 'samples' in data and isinstance(data['samples'], list):
            samples = data['samples']
            
            if len(samples) < 1e6:
                print(f"File: {filename} -> n={n}, chi={chi} (samples: {len(samples)})")
            
            # Multiply each sample by 2^(n/2)
            scale_factor = 2 ** (n / 2)
            new_samples = [s * scale_factor for s in samples]
            
            # Update and save back
            data['samples'] = new_samples
            with open(filename, 'wb') as f:
                pickle.dump(data, f)