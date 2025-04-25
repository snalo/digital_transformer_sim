import os
import json
import pandas as pd
from model_parser import load_models
from hw_profile import HardwareProfile

from estimator_latency import estimate_latency
from estimator_energy import estimate_energy
from estimate_area import estimate_area

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
            "Area per MAC (mm^2)": area["Area per MAC (mm^2)"],
            "Total Area (mm^2)": area["Total_Area"],
            "Latency Breakdown": latency,
            "Energy Breakdown": energy,
            "Area Breakdown": area
        })

df = pd.DataFrame(results)

# Generate Hardware Summary
reference_model = models[0]  # Use the first model (Transformer base)

summary_data = []
for filename in os.listdir(profile_dir):
    if filename.endswith(".json"):
        path = os.path.join(profile_dir, filename)
        with open(path, 'r') as f:
            hw_data = json.load(f)
            for hw_name, config in hw_data.items():
                lanes = config.get("mul_lanes", "")
                cols = config.get("mul_cols", "")
                bit_precision = config.get("bit_precision", "")
                max_macs = config.get("max_parallel_dotprods", "")
                static_power = config.get("static_power", {}).get("value", "")
                dynamic_power = config.get("dynamic_power", {}).get("value", "")

                hw_profile = HardwareProfile(hw_name, config)
                area_info = estimate_area(hw_profile)  # From estimator_area
                area_per_mac = area_info["Area per MAC (mm^2)"]

                energy_breakdown = estimate_energy(reference_model, hw_profile)
                mac_energy = energy_breakdown.get("MAC", None)

                d_model = reference_model.d_model
                dff = reference_model.dff
                seq_len = reference_model.d_sequence
                layers = reference_model.N_layers
                macs_per_layer = (
                    3 * seq_len * d_model +
                    2 * seq_len * d_model +
                    seq_len * d_model +
                    2 * seq_len * d_model * dff
                )
                total_macs = macs_per_layer * layers
                if mac_energy:
                    energy_per_mac = mac_energy / total_macs
                else:
                    energy_per_mac = ""

                summary_data.append({
                    "Hardware": hw_name,
                    "Lanes": lanes,
                    "Columns": cols,
                    "Bit Precision": bit_precision,
                    "Max MACs": max_macs,
                    "Area per MAC (mm^2)": area_per_mac,
                    "Static Power (W)": static_power,
                    "Dynamic Power (W)": dynamic_power,
                    "Energy per MAC (J, estimated)": energy_per_mac
                })

summary_df = pd.DataFrame(summary_data)

# === Now Export Both Results to a Single Excel File with Two Sheets ===
output_path = "Simulation_Summary_0425.xlsx"
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name="Simulation")
    summary_df.to_excel(writer, index=False, sheet_name="Hardware Summary")

print(f" Simulation complete. Results exported to '{output_path}' with two sheets.")
