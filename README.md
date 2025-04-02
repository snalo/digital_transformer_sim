# digital_transformer_sim
Transformer Model Sim

# PIDCOP Transformer Analysis

This project evaluates Transformer models against PIDCOP hardware constraints by estimating their latency, energy consumption, and area utilization. It provides tools to parse configurations, run estimations, and visualize results.

---

## Overview

The analysis pipeline includes:

- Parsing transformer model specs and hardware profiles
- Estimating hardware-related metrics (latency, energy, area)
- Outputting and visualizing results

---

## Project Structure

```
pidcop_transformer_analysis/
│
├── configs/
│   ├── model_configurations.json     # Transformer model specifications
│   └── hardware_pidcop.json          # PIDCOP hardware configuration
│
├── core/
│   ├── model_parser.py               # Parses and loads transformer configs
│   ├── hw_profile.py                 # Handles hardware profiles
│   └── estimator.py                  # Latency, energy, and area estimations
│
├── results/
│   └── pidcop_estimates.csv          # Estimated metrics for each model
│
├── visualizations/
│   └── plot_results.py               # Visualization scripts (charts, graphs)
│
├── main.py                           # Main entry point for analysis
└── README.md                         # Project overview and usage instructions
```

---

## Requirements

- Python 3.8+
- pandas
- matplotlib (optional, for visualizations)
- json

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How It Works

1. **Configurations**:  
   Add model and hardware specs to the `configs/` folder.

2. **Run Analysis**:  
   Use the main script to process configurations:

   ```bash
   python main.py
   ```

3. **Output**:  
   Results are saved to `results/pidcop_estimates.csv`.

4. **Visualizations** *(optional)*:  
   Generate plots by running:

   ```bash
   python visualizations/plot_results.py
   ```

---

## Sample Output

- Latency per transformer model
- Estimated energy use (Joules)
- Area estimates based on hardware constraints

---

##  Contribution

Pull requests and issues are welcome! Please ensure code is tested and documented.

---

## License

MIT License
