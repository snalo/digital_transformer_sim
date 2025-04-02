import os
import json
import pandas as pd
from model_parser import load_models
from hw_profile import HardwareProfile
from estimator import estimate_latency_energy_area

# Load transformer models
models = load_models("model_configurations.json")

# Load all hardware profiles from /all_hw_profiles
hardware_profiles = []
profile_dir = "all_hw_profiles"
for filename in os.listdir(profile_dir):
    if filename.endswith(".json"):
        path = os.path.join(profile_dir, filename)
        with open(path, 'r') as f:
            hw_data = json.load(f)
            for hw_name, config in hw_data.items():
                hw_profile = HardwareProfile(hw_name, config)
                hardware_profiles.append(hw_profile)

# Run simulations
results = []
for model in models:
    for hw in hardware_profiles:
        result = estimate_latency_energy_area(model, hw)
        results.append(result)

# Save results
df = pd.DataFrame(results)
df.to_csv("simulation_results.csv", index=False)
print("Simulation complete. Results saved to simulation_results.csv")
