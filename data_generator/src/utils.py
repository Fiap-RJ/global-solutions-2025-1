# data_generator/src/utils.py


def calculate_heat_index(
    temp_celsius: float, relative_humidity_percent: float
) -> float:
    """Calcula o Índice de Calor (Heat Index) usando a fórmula da NOAA."""
    temp_fahrenheit = (temp_celsius * 9 / 5) + 32
    rh = relative_humidity_percent

    hi_fahrenheit = (
        -42.379
        + (2.04901523 * temp_fahrenheit)
        + (10.14333127 * rh)
        - (0.22475541 * temp_fahrenheit * rh)
        - (0.00683783 * temp_fahrenheit**2)
        - (0.05481717 * rh**2)
        + (0.00122874 * temp_fahrenheit**2 * rh)
        + (0.00085282 * temp_fahrenheit * rh**2)
        - (0.00000199 * temp_fahrenheit**2 * rh**2)
    )

    if rh < 13 and (80 <= temp_fahrenheit <= 112):
        adjustment = ((13 - rh) / 4) * (((17 - abs(temp_fahrenheit - 95)) / 17) ** 0.5)
        hi_fahrenheit -= adjustment

    if rh > 85 and (80 <= temp_fahrenheit <= 87):
        adjustment = ((rh - 85) / 10) * ((87 - temp_fahrenheit) / 5)
        hi_fahrenheit += adjustment

    if hi_fahrenheit < 80:
        hi_fahrenheit = temp_fahrenheit

    return (hi_fahrenheit - 32) * 5 / 9


def assign_risk_label(heat_index_celsius: float) -> int:
    """Atribui um rótulo de risco com base no IC."""
    if heat_index_celsius <= 36:
        return 0
    elif heat_index_celsius <= 40:
        return 1
    elif heat_index_celsius <= 44:
        return 2
    else:
        return 3
