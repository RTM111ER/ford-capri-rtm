"""
Verify that the real Harpaz family anchors, applied to the 123 equations,
produce 123 closures.

Usage:
    python core/verify_real.py   (from repo root)

Output:
    Total equations: 123
    Closures for real Harpaz family: 123 / 123
    Percentage: 100.0%
"""

import os
import sys
# Make this script runnable from anywhere — add its own directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rtm_equations import EQUATIONS

# Real Harpaz anchors
HARPAZ = {
    "surname":      292,
    "first_self":   320,
    "full_self":    612,
    "father":       543,
    "father_first": 251,
    "brother1":     426,
    "brother1_first": 134,
    "brother2":     738,
    "brother2_first": 446,
    "wife":          56,
    "wife_married": 348,
    "apartment":     58,
    "core":         116,
    "birth_year":  1982,
    "measurement_year": 2026,
    "father_birth":1949,
    "father_age":    76,
    "self_age":      44,
}

FIXED_INPUTS = {
    "ford_capri":   680,
    "ford":         290,
    "capri":        390,
    "plate_a":      637,
    "plate_b":      177,
    "plate_digits": [6, 3, 7, 1, 7, 7],
    "prod_count_rounded":  1900000,
    "prod_count_precise":  1886647,
    "prod_gematria":       1912,
    "prod_precise_gematria": 4343,
    "prod_start":          1968,
    "prod_end":            1986,
    "designer_short":       660,
    "designer_full":       1148,
    "designer_birth":      1935,
    "hebrew_date_882":      882,
    "date_digit_4528":     4528,
}

# Extended value targets (structural closures — spelled Hebrew phrases)
EXTENDED_TARGET_VALUES = {
    "word_eight_401": 401,
    "word_11": 11,
    "hebrew_year_786": 786,
    "question_eran_age_729": 729,
    "gap_return_5": 5,
    "word_thirty_686": 686,
    "eran_age_phrase_1266": 1266,
    "eran_digit_1373": 1373,
    "eleven_fem_1494": 1494,
    "eleven_masc_1098": 1098,
    "amir_age_phrase_1028": 1028,
    "one_one_818": 818,
    "designer_short_660": 660,
    "word_sixty_60": 60,
    "word_22": 22,
    "ford_290": 290,
    "ford_capri_680": 680,
    "capri_390": 390,
    "word_50": 50,
    "word_forty_three_909": 909,
    "prod_gematria_1912": 1912,
    "prod_end_1986": 1986,
    "prod_start_1968": 1968,
    "val_1896": 1896,
    "val_1451": 1451,
    "word_31_digit_1045": 1045,
    "double_sync_62": 62,
    "word_66": 66,
}


def check(eq_func, target_key, target_value, A, I):
    """Check if equation closes to the target."""
    try:
        result, _ = eq_func(A, I)
        # If target is an anchor key
        if target_key in A:
            return result == A[target_key]
        # If target is an extended target
        if target_key in EXTENDED_TARGET_VALUES:
            return result == EXTENDED_TARGET_VALUES[target_key]
        return result == target_value
    except Exception as e:
        print(f"  ERROR in {eq_func.__name__}: {e}")
        return False


closed = 0
failed = []
for item in EQUATIONS:
    finding, label, func, target_key, target_val = item
    if check(func, target_key, target_val, HARPAZ, FIXED_INPUTS):
        closed += 1
    else:
        try:
            result, _ = func(HARPAZ, FIXED_INPUTS)
        except Exception as e:
            result = f"ERROR: {e}"
        failed.append((label, target_key, target_val, result))

print(f"Total equations: {len(EQUATIONS)}")
print(f"Closures for real Harpaz family: {closed} / {len(EQUATIONS)}")
print(f"Percentage: {100*closed/len(EQUATIONS):.1f}%")
print()

if failed:
    print(f"FAILURES ({len(failed)}):")
    for label, tkey, tval, result in failed:
        print(f"  {label}: expected {tkey}={tval}, got {result}")
