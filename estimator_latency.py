
def estimate_latency(model, hardware):
    bit_precision = hardware.bit_precision
    bit_rate = hardware.bit_rate * 1e9  # Convert to bits/sec
    d_model = model.d_model
    dff = model.dff
    seq_len = model.d_sequence
    num_layers = model.N_layers
    num_heads = model.H_model

    latency_breakdown = {}

    # Basic formula: latency = bits / bit_rate
    def latency(bits): return bits / bit_rate

    # QKV Projection (3x)
    qkv_bits = 3 * seq_len * d_model * bit_precision
    latency_breakdown["QKV_proj"] = latency(qkv_bits)

    # Attention: dot products between Q and K + Softmax + V multiplication
    attn_bits = 2 * seq_len * d_model * bit_precision
    latency_breakdown["Attention"] = latency(attn_bits)

    # Softmax (approx)
    latency_breakdown["Softmax"] = latency(seq_len * bit_precision)

    # MHA output projection
    mha_bits = seq_len * d_model * bit_precision
    latency_breakdown["MHA_proj"] = latency(mha_bits)

    # Feedforward (2 layers): d_model → dff → d_model
    ff1_bits = seq_len * d_model * dff * bit_precision
    ff2_bits = seq_len * dff * d_model * bit_precision
    latency_breakdown["FFN_1"] = latency(ff1_bits)
    latency_breakdown["FFN_2"] = latency(ff2_bits)

    # Aggregate per-layer latency
    total_per_layer = sum(latency_breakdown.values())
    total_latency = num_layers * total_per_layer
    latency_breakdown["Total_Latency"] = total_latency

    return latency_breakdown
