
def estimate_energy(model, hardware):
    bit_precision = hardware.bit_precision
    d_model = model.d_model
    dff = model.dff
    seq_len = model.d_sequence
    num_layers = model.N_layers

    # Component energy values (in J) from hardware profile
    e_mac = hardware.energy_per_mac
    e_adc = hardware.adc_energy_per_conv
    e_dac = hardware.dac_energy_per_bit
    static_power = hardware.static_power

    # MAC operations per transformer layer
    macs_per_layer = (
        3 * seq_len * d_model +         # QKV
        2 * seq_len * d_model +         # Attention QK + V
        seq_len * d_model +             # MHA projection
        seq_len * d_model * dff * 2     # FFN1 + FFN2
    )
    total_macs = macs_per_layer * num_layers

    # Energy Breakdown
    energy_breakdown = {}
    energy_breakdown["MAC"] = total_macs * e_mac
    energy_breakdown["DAC"] = total_macs * bit_precision * e_dac
    energy_breakdown["ADC"] = seq_len * num_layers * e_adc

    # Estimate latency for static power (simplified)
    bits_total = total_macs * bit_precision
    bit_rate = hardware.bit_rate * 1e9
    est_latency = bits_total / bit_rate
    energy_breakdown["Static"] = est_latency * static_power

    energy_breakdown["Total_Energy"] = sum(energy_breakdown.values())
    return energy_breakdown
