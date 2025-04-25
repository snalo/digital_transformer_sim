
import json

class HardwareProfile:
    def __init__(self, name, config):
        self.name = name
        self.mul_lanes = config["mul_lanes"]
        self.mul_cols = config["mul_cols"]
        self.bit_precision = config["bit_precision"]
        self.bit_rate = config["bit_rate"]
        self.max_parallel_dotprods = config["max_parallel_dotprods"]

        #self.energy_per_mac = config["energy_per_mac"]["value"]
        self.adc_energy_per_sample = config["adc_energy_per_sample"]["value"]
        self.dac_energy_per_bit = config["dac_energy_per_bit"]["value"]
        self.static_power = config["static_power"]["value"]
        self.dynamic_power = config["dynamic_power"]["value"]

        self.area_per_mul_lane = config["area_per_mul_lane"]["value"]
        self.pca_area = config["pca_area"]["value"]
        self.adc_area = config["adc_area"]["value"]
        self.waveguide_pitch = config["waveguide_pitch"]["value"]

        #self.reuse_factor = config["reuse_factor"]["value"]

def load_hardware_profiles(json_path):
    with open(json_path, 'r') as f:
        hardware_data = json.load(f)
    return [HardwareProfile(name, config) for name, config in hardware_data.items()]
