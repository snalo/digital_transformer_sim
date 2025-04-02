
def estimate_area(hardware):
    # Multiply units
    num_mac_units = hardware.mul_lanes * hardware.mul_cols

    # Area contributions from compute + photonic + ADC blocks
    area_breakdown = {}
    area_breakdown["MAC_array"] = num_mac_units * hardware.area_per_mul_lane
    area_breakdown["PCA"] = hardware.mul_cols * hardware.pca_area
    area_breakdown["ADC"] = hardware.mul_cols * hardware.adc_area

    area_breakdown["Total_Area"] = sum(area_breakdown.values())
    return area_breakdown
