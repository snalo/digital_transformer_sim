
import os
import json
import pandas as pd
from model_parser import load_models
from hw_profile import HardwareProfile

from estimator_latency import estimate_latency
from estimator_energy import estimate_energy
from estimator_area import estimate_area

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

# Run simulations using ASTRA-style estimators
results = []
for model in models:
    for hw in hardware_profiles:
        latency = estimate_latency(model, hw)
        energy = estimate_energy(model, hw)
        area = estimate_area(hw)

        results.append({
            "Model": model.name,
            "Hardware": hw.name,
            "Latency (s)": latency["Total_Latency"],
            "Energy (J)": energy["Total_Energy"],
            "Area (mm^2)": area["Total_Area"],
            "Latency Breakdown": latency,
            "Energy Breakdown": energy,
            "Area Breakdown": area
        })

# Save results
df = pd.DataFrame(results)
df.to_csv("simulation_results_new.csv", index=False)
print("Simulation complete. Results saved to simulation_results.csv")
