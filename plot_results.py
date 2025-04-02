
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_results(csv_file="simulation_results.csv", output_dir="plots"):
    # Load data
    df = pd.read_csv(csv_file)

    # Create output directory if needed
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Plot 1: Latency vs Energy
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Latency (s)", y="Energy (J)", hue="Hardware", style="Model", s=100)
    plt.title("Latency vs Energy Consumption")
    plt.xlabel("Latency (s)")
    plt.ylabel("Energy (J)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/latency_vs_energy.png")

    # Plot 2: Area by Hardware
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Hardware", y="Area (mm^2)", hue="Model")
    plt.title("Area per Model and Hardware")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/area_comparison.png")

    print(f"Plots saved to {output_dir}/")

if __name__ == "__main__":
    plot_results()
