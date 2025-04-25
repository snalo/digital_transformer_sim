import math

def estimate_area(hardware):
    name = hardware.name
    N = hardware.mul_lanes
    M = hardware.mul_cols

    unit_counts = {
        "deap_cnn": 100,
        "holylight": 15,
        "pixel_photonic": 100,
        "pidcop_small": 100,
        "pidcop_large": 100,
        "pidcop_asymmetric": 100
    }
    unit_count = unit_counts.get(name, 100)

    area_per_mac = get_area_per_mac_unit(name, N, M, hardware)
    extra_area = get_extras_area(name, N, M, unit_count, hardware)
    total_area = area_per_mac * unit_count + extra_area

    return {
        "Area per MAC (mm^2)": area_per_mac,
        "Total_Area": total_area
    }


def get_area_per_mac_unit(name, N, M, hardware):
    # Shared constants
    radius = 4.55  # um
    mrr_area = (3.14 * (radius ** 2) * 1e-6)  # mm²
    MZM = 0.0052  # mm² (PIXEL only)
    voltage_adder_area = 0.0005  # mm²
    tir = 3  # arbitrary constant for PIXEL PCA scaling

    pd = hardware.pca_area
    adc = hardware.adc_area
    dac = 0 if name.startswith("pidcop") else 0.0015  # mm² – fixed value

    if name == "holylight":
        return mrr_area * N * M + M * adc + M * pd + (M + 1) * N * dac

    elif name == "deap_cnn":
        return mrr_area * (2 * N * M) + M * adc + M * pd + 2 * N * M * dac

    elif name.startswith("pixel"):
        pca_area = tir * M * 0.007
        return MZM * (16 * N * M) + M * adc + 3 * M * pd + 16 * M * N * dac + voltage_adder_area * M + pca_area

    elif name.startswith("pidcop"):
        return mrr_area * N * M + M * adc + M * pd  # no DAC

    else:
        raise ValueError(f"Unknown hardware type: {name}")


def get_extras_area(name, N, M, unit_count, hardware):
    # External component area (not per MAC)
    splitter = 0.005
    S_A_area = 0.00003
    eDram_area = 0.166
    max_pool_area = 0.00024
    sigmoid = 0.0006
    router = 0.151
    bus = 0.009
    io_interface = 0.0244

    splitter_area = M * splitter
    global_logic_area = math.ceil(unit_count / 4) * (
        S_A_area + eDram_area + sigmoid + router + bus + max_pool_area + io_interface
    )

    return splitter_area + global_logic_area
