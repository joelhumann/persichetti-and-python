import math

def ratio_to_cents(ratio: float) -> float:
    return 1200 * math.log2(ratio)

def cents_to_ratio(cents: float) -> float:
    return 2 ** (cents / 1200)