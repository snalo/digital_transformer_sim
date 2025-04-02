
import json

class TransformerModel:
    def __init__(self, name, config):
        self.name = name
        self.N_layers = config["N_layers"]
        self.d_model = config["d_model"]
        self.dff = config["dff"]
        self.H_model = config["H_model"]
        self.d_sequence = config["d_sequence"]
        self.num_tokens = config["num_tokens"]

        self.total_macs = self.estimate_total_macs()

    def estimate_total_macs(self):
        # Estimate MACs for one transformer layer (multi-head attention + FFN)
        attention_macs = 4 * self.d_sequence * self.d_model * self.d_model
        ffn_macs = 2 * self.d_sequence * self.d_model * self.dff
        total_layer_macs = attention_macs + ffn_macs
        return self.N_layers * total_layer_macs

def load_models(json_path):
    with open(json_path, 'r') as f:
        model_data = json.load(f)
    return [TransformerModel(name, config) for name, config in model_data.items()]
