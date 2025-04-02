
def estimate_latency_energy_area(model, hardware):
    # Total MACs
    total_macs = model.total_macs

    # Latency = total_macs / (bit_rate * max_parallel_dotprods)
    ops_per_sec = hardware.bit_rate * 1e9 * hardware.max_parallel_dotprods
    latency = total_macs / ops_per_sec

    # Energy = MAC energy + DAC + ADC + static
    mac_energy = total_macs * hardware.energy_per_mac
    dac_energy = total_macs * hardware.bit_precision * hardware.dac_energy_per_bit
    adc_energy = model.d_sequence * hardware.adc_energy_per_conv
    static_energy = latency * hardware.static_power
    total_energy = mac_energy + dac_energy + adc_energy + static_energy

    # Area = multiplier + PCA + ADC
    total_mac_units = hardware.mul_lanes * hardware.mul_cols
    area = (hardware.area_per_mul_lane * total_mac_units +
            hardware.pca_area * hardware.mul_cols +
            hardware.adc_area * hardware.mul_cols)

    return {
        "Model": model.name,
        "Hardware": hardware.name,
        "Total MACs": total_macs,
        "Latency (s)": latency,
        "Energy (J)": total_energy,
        "Area (mm^2)": area
    }
