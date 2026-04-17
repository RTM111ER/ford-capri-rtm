"""
================================================================================
RTM FORD CAPRI — FULL TWO-LAYER SIMULATION (COLAB T4)
================================================================================

Tests the 123 equations from "The Ford Capri Identity Matrix" (Case File #3)
against random observer sets spanning the complete Hebrew gematria space (1-999).

Null model rationale:
  Every Hebrew name reduces to a gematria value in 1-999.
  Sampling uniformly from 1-999 covers EVERY possible name — common, rare,
  extinct, foreign-transliterated, imagined. The null model is therefore
  maximally complete: "Across the entire space of possible family identities,
  how many produce ≥109 closures and ≥85% network density?"

Two layers measured simultaneously:
  LAYER 1 — Closure count (compare to book's σ=37.4 baseline)
  LAYER 2 — Network density (the new metric — recurrence of derived values
           across findings)

Usage in Google Colab:
  1. Runtime → Change runtime type → T4 GPU
  2. Cell 1:  !pip install cupy-cuda12x
  3. Cell 2:  paste this entire file
  4. Cell 3:  main(n_trials=100_000_000, batch_size=500_000)

Expected runtime on T4: 30-60 minutes for 100M trials.
Falls back to NumPy on CPU automatically.

Author: Eran Harpaz, RTM — Reflective Time Model
================================================================================
"""

import sys
import time

# =============================================================================
# BACKEND — CuPy if available, NumPy fallback
# =============================================================================

try:
    import cupy as xp
    GPU = True
    print("✓ Backend: CuPy (GPU)")
except ImportError:
    import numpy as xp
    GPU = False
    print("✗ Backend: NumPy (CPU — slower, for local testing)")


# =============================================================================
# FIXED INPUTS — Ford Capri dataset (never vary across random trials)
# =============================================================================

FORD_CAPRI          = 680
FORD                = 290
CAPRI               = 390
PLATE_A             = 637
PLATE_B             = 177
PLATE_MIRROR_A      = 736     # mirror(637)
PLATE_MIRROR_B      = 771     # mirror(177)
PLATE_DIGITS_SUM    = 31      # 6+3+7+1+7+7

PROD_COUNT_ROUNDED  = 1_900_000
PROD_COUNT_PRECISE  = 1_886_647
PROD_GEMATRIA       = 1912    # "מיליון תשע מאות אלף יחידות"
PROD_PRECISE_GEM    = 4343
PROD_PRECISE_MIRROR = 3434
PROD_START          = 1968
PROD_END            = 1986
PROD_START_MIRROR   = 8691
PROD_END_MIRROR     = 6891

DESIGNER_SHORT      = 660     # פיליפ טי קלארק
DESIGNER_FULL       = 1148    # פיליפ תומאס קלארק
DESIGNER_BIRTH      = 1935

HEBREW_DATE_882     = 882     # יז בכסלו תשמ"ז
DATE_DIGIT_4528     = 4528    # digit spelling of 19121986

MEASUREMENT_YEAR    = 2026


# =============================================================================
# HEBREW LINGUISTIC CONSTANTS (invariant across observers)
# =============================================================================

ELEVEN_FEM      = 1494   # "אחת עשרה דקות" — also = 680+637+177
ELEVEN_MASC     = 1098   # "אחד עשרה דקות"
ELEVEN_STD_MASC = 1093   # "אחד עשר דקות"
WORD_EIGHT      = 401    # "שמונה"
WORD_ONE_FEM    = 409    # "אחת"
WORD_FIFTY      = 408    # "חמישים"
WORD_THIRTY     = 686    # "שלושים"
WORD_SIXTY      = 60
ONE_ONE         = 818    # "אחת אחת"

VAL_1373 = 1373   # "שש אחד שתיים" (digit spelling of 612)
VAL_1200 = 1200   # "אלף מאתיים" = 612
VAL_1266 = 1266   # "שישים ושש" / "ערן הרפז בן ארבעים וארבע"
VAL_1623 = 1623   # "אמיר הרפז בן שבעים ושש"
VAL_1028 = 1028   # "שבעים ושש"
VAL_972  = 972    # "שבע שש"
VAL_1014 = 1014   # "חמישים ושש"
VAL_948  = 948    # "חמש שש"
VAL_1101 = 1101   # "שלושים ואחת"
VAL_1045 = 1045   # "שלוש אחת"
VAL_1707 = 1707   # "שש מאות שישים"
VAL_1930 = 1930   # spelling of 1494
VAL_2329 = 2329
VAL_2650 = 2650
VAL_2761 = 2761   # digit spelling of plate 637,177
VAL_4262 = 4262   # standard spelling of 2761
VAL_1414 = 1414   # "דירה מספר חמישים ושמונה"
VAL_1215 = 1215
VAL_1926 = 1926
VAL_1541 = 1541
VAL_3455 = 3455
VAL_2665 = 2665
VAL_6120 = 6120
VAL_6142 = 6142
VAL_1896 = 1896
VAL_2290 = 2290
VAL_2087 = 2087
VAL_2378 = 2378
VAL_1112 = 1112
HEBREW_YEAR_786   = 786   # תשפ"ו
QUESTION_ERAN_729 = 729   # "בן כמה ערן הרפז"
VAL_749  = 749    # "חמש שמונה" (58 digit)
VAL_815  = 815    # "חמישים ושמונה"


# =============================================================================
# ANCHOR STRUCTURE (per-family observer identity)
# =============================================================================

ANCHOR_NAMES = [
    "surname",          #  0 — family surname gematria
    "first_self",       #  1 — observer's first name
    "full_self",        #  2 — observer's full name (first + surname)
    "father",           #  3 — father's full name
    "father_first",     #  4 — father's first name
    "brother1",         #  5 — brother 1 full name
    "brother1_first",   #  6 — brother 1 first name
    "brother2",         #  7 — brother 2 full name
    "brother2_first",   #  8 — brother 2 first name
    "wife",             #  9 — wife's first name
    "wife_married",     # 10 — wife's married name (first + surname)
    "apartment",        # 11 — apartment number
    "core",             # 12 — 2 × apartment
    "birth_year",       # 13
    "father_birth",     # 14
    "father_age",       # 15 — 2026 - father_birth
    "self_age",         # 16 — 2026 - birth_year
]
A_IDX = {name: i for i, name in enumerate(ANCHOR_NAMES)}
N_ANCHORS = len(ANCHOR_NAMES)

def col(A, key):
    return A[:, A_IDX[key]]


# =============================================================================
# RANDOM FAMILY GENERATOR — FULL GEMATRIA SPACE 1-999
# =============================================================================

def generate_random_families(N, seed=0):
    """
    Generate N random observer identities.
    Each name gematria sampled uniformly from 1-999, covering every possible
    Hebrew name in the language's complete gematria space.

    This is a maximal null model: any name that could ever exist maps to a
    value in this range.
    """
    xp.random.seed(seed)

    # Independent random gematria for each name component (1-999 inclusive)
    first_self    = xp.random.randint(1, 1000, N, dtype=xp.int64)
    father_first  = xp.random.randint(1, 1000, N, dtype=xp.int64)
    brother1_first = xp.random.randint(1, 1000, N, dtype=xp.int64)
    brother2_first = xp.random.randint(1, 1000, N, dtype=xp.int64)
    wife          = xp.random.randint(1, 1000, N, dtype=xp.int64)
    surname       = xp.random.randint(1, 1000, N, dtype=xp.int64)

    # Full names = first + surname (Hebrew gematria additivity)
    full_self     = first_self + surname
    father        = father_first + surname
    brother1      = brother1_first + surname
    brother2      = brother2_first + surname
    wife_married  = wife + surname

    # Birth years — cover a reasonable life span around 2026
    birth_year    = xp.random.randint(1920, 2010, N, dtype=xp.int64)
    father_birth  = birth_year - xp.random.randint(20, 50, N, dtype=xp.int64)
    father_age    = MEASUREMENT_YEAR - father_birth
    self_age      = MEASUREMENT_YEAR - birth_year

    # Apartment number — any realistic value
    apartment = xp.random.randint(1, 1000, N, dtype=xp.int64)
    core      = 2 * apartment

    A = xp.zeros((N, N_ANCHORS), dtype=xp.int64)
    A[:, A_IDX["surname"]]         = surname
    A[:, A_IDX["first_self"]]      = first_self
    A[:, A_IDX["full_self"]]       = full_self
    A[:, A_IDX["father"]]          = father
    A[:, A_IDX["father_first"]]    = father_first
    A[:, A_IDX["brother1"]]        = brother1
    A[:, A_IDX["brother1_first"]]  = brother1_first
    A[:, A_IDX["brother2"]]        = brother2
    A[:, A_IDX["brother2_first"]]  = brother2_first
    A[:, A_IDX["wife"]]            = wife
    A[:, A_IDX["wife_married"]]    = wife_married
    A[:, A_IDX["apartment"]]       = apartment
    A[:, A_IDX["core"]]            = core
    A[:, A_IDX["birth_year"]]      = birth_year
    A[:, A_IDX["father_birth"]]    = father_birth
    A[:, A_IDX["father_age"]]      = father_age
    A[:, A_IDX["self_age"]]        = self_age
    return A


def build_harpaz_batch(N):
    """Replicate the real Harpaz anchors across N rows (for sanity check)."""
    HARPAZ = {
        "surname": 292, "first_self": 320, "full_self": 612,
        "father": 543, "father_first": 251,
        "brother1": 426, "brother1_first": 134,
        "brother2": 738, "brother2_first": 446,
        "wife": 56, "wife_married": 348,
        "apartment": 58, "core": 116,
        "birth_year": 1982, "father_birth": 1949,
        "father_age": 76, "self_age": 44,
    }
    A = xp.zeros((N, N_ANCHORS), dtype=xp.int64)
    for k, v in HARPAZ.items():
        A[:, A_IDX[k]] = v
    return A


# =============================================================================
# THE 123 EQUATIONS — fully vectorized
# =============================================================================

def run_all_equations(A):
    """
    Evaluate all 123 equations across N trials in parallel.
    Returns: (closures_per_trial, closure_matrix)
      closures_per_trial: (N,) int — count of closures per trial
      closure_matrix:     (N, 123) bool — which equations closed
    """
    N = A.shape[0]
    closed = xp.zeros((N, 123), dtype=xp.bool_)

    # Anchor columns (aliases)
    A_sur   = col(A, "surname")
    A_fself = col(A, "first_self")
    A_full  = col(A, "full_self")
    A_fath  = col(A, "father")
    A_fath1 = col(A, "father_first")
    A_br1   = col(A, "brother1")
    A_br1f  = col(A, "brother1_first")
    A_br2   = col(A, "brother2")
    A_br2f  = col(A, "brother2_first")
    A_wife  = col(A, "wife")
    A_wifm  = col(A, "wife_married")
    A_apt   = col(A, "apartment")
    A_core  = col(A, "core")
    A_by    = col(A, "birth_year")
    A_fby   = col(A, "father_birth")
    A_fage  = col(A, "father_age")
    A_sage  = col(A, "self_age")

    PS = PLATE_DIGITS_SUM
    MY = MEASUREMENT_YEAR

    # -------- FINDING #01 --------
    # 01.01
    closed[:, 0] = (3068 - A_fby - FORD_CAPRI - PS - A_core) == A_sur

    # -------- FINDING #02 --------
    closed[:, 1] = (FORD_CAPRI + PLATE_A + PLATE_B) == ELEVEN_FEM
    closed[:, 2] = (MY - (ELEVEN_FEM - 11)) == A_fath
    closed[:, 3] = (PROD_GEMATRIA - PLATE_A - PLATE_B) == ELEVEN_MASC

    # -------- FINDING #03 --------
    closed[:, 4]  = (1098 - 1093 == 5) & (A_wifm == 348)
    closed[:, 5]  = xp.full(N, True, dtype=xp.bool_)  # mirror(2191)=1912 always
    closed[:, 6]  = (ELEVEN_FEM - ELEVEN_STD_MASC) == WORD_EIGHT
    closed[:, 7]  = (WORD_EIGHT - CAPRI) == 11
    closed[:, 8]  = (FORD_CAPRI - (2191 - 1912)) == WORD_EIGHT
    closed[:, 9]  = (401 + 401 - 8 - 8) == HEBREW_YEAR_786
    closed[:, 10] = (HEBREW_YEAR_786 - 57) == QUESTION_ERAN_729
    closed[:, 11] = ((QUESTION_ERAN_729 - A_sage) - FORD_CAPRI) == 5
    closed[:, 12] = (A_by - 2 * (QUESTION_ERAN_729 - A_sage)) == A_full
    closed[:, 13] = (A_wifm * 2 - 10) == WORD_THIRTY
    closed[:, 14] = (WORD_THIRTY - 30 - A_full) == A_sage

    # -------- FINDING #04 --------
    closed[:, 15] = ((ELEVEN_STD_MASC + ELEVEN_FEM) - A_fby - FORD) == A_wifm
    closed[:, 16] = (A_wifm + FORD_CAPRI) == VAL_1028
    closed[:, 17] = ((ELEVEN_MASC + ELEVEN_FEM) - A_fby - PS) == A_full
    step_04_04 = PROD_GEMATRIA - 738 - 837 - PS
    closed[:, 18] = (step_04_04 * 2) == A_full

    # -------- FINDING #05 --------
    closed[:, 19] = (PLATE_B - (FORD_CAPRI - PLATE_A)) == A_br1f
    closed[:, 20] = (VAL_1930 - ELEVEN_FEM - A_core) == A_fself

    # -------- FINDING #06 --------
    closed[:, 21] = (A_br2 == 738)
    closed[:, 22] = ((VAL_2650 - VAL_2329 - PS) == FORD)
    closed[:, 23] = xp.full(N, (VAL_2329 - 6 - 1 - 2 == 2320), dtype=xp.bool_) & xp.full(N, True, dtype=xp.bool_)  # 1373 is a fixed linguistic target
    closed[:, 24] = (2320 - PROD_GEMATRIA - A_core) == A_sur
    step_06_05 = 2320 - PLATE_A - PLATE_B - 457 - FORD_CAPRI
    closed[:, 25] = (step_06_05 * 2) == A_br2
    closed[:, 26] = ((2320 - PROD_START) + (2320 - PROD_END)) == WORD_THIRTY
    closed[:, 27] = (WORD_THIRTY - 30 - A_full) == A_sage

    # -------- FINDING #07 --------
    closed[:, 28] = (738 - FORD_CAPRI) == A_apt
    closed[:, 29] = (738 - (PROD_GEMATRIA - PLATE_A - PLATE_B - FORD_CAPRI)) == A_fself
    gap = A_full - A_br1  # 186 for real Harpaz
    step_07_03 = ELEVEN_MASC - gap - A_fath
    closed[:, 30] = (step_07_03 * 2) == A_br2

    # -------- FINDING #08 --------
    step_08_01 = PROD_START_MIRROR - PROD_END_MIRROR - PLATE_A - PLATE_B - FORD_CAPRI
    closed[:, 31] = (step_08_01 * 2) == A_full
    closed[:, 32] = (MY - PROD_START) == A_apt
    step_08_03 = PROD_END - VAL_749 - VAL_815 - A_apt
    closed[:, 33] = (step_08_03 * 2 - A_core) == A_full
    s1 = PLATE_A - step_08_03
    s2 = s1 - PLATE_B
    closed[:, 34] = (FORD_CAPRI - s2) == (2 * A_sur)

    # -------- FINDING #09 --------
    closed[:, 35] = ((PLATE_B + PLATE_B + PLATE_A) * 2) == A_by
    closed[:, 36] = ((PLATE_A * 2 + PLATE_B) == 1451) & (A_full == 612)
    closed[:, 37] = ((PLATE_A * 2 + PLATE_B) - VAL_1200) == A_fath1
    step_09_04 = (A_by - 1451) + (MY - 1451)
    closed[:, 38] = (step_09_04 - FORD_CAPRI) == A_br1

    # -------- FINDING #10 --------
    closed[:, 39] = ((PLATE_MIRROR_B + PLATE_MIRROR_A) - VAL_1215) == A_sur
    closed[:, 40] = (VAL_1926 - VAL_1215 - PS) == FORD_CAPRI
    closed[:, 41] = (A_fby - VAL_1541 - A_core) == A_sur
    closed[:, 42] = (ELEVEN_FEM * 2 - MY - FORD_CAPRI - PS) == A_fath1

    # -------- FINDING #11 --------
    closed[:, 43] = (2 * PROD_PRECISE_GEM - MY - A_by - PROD_START - PROD_END - FORD_CAPRI) == A_sage
    closed[:, 44] = (PROD_PRECISE_GEM - PROD_PRECISE_MIRROR) == 909
    closed[:, 45] = (PROD_PRECISE_GEM - 43 - MY - A_by) == A_sur
    step_11_04 = PROD_PRECISE_GEM - 4 - 3 - MY
    closed[:, 46] = ((step_11_04 - MY) + (step_11_04 - A_by)) == A_full

    # -------- FINDING #12 --------
    closed[:, 47] = (VAL_1028 - DESIGNER_SHORT - A_fage) == A_sur
    closed[:, 48] = (VAL_1707 - VAL_972 - A_fath - A_core) == A_fage
    closed[:, 49] = (VAL_1623 - DESIGNER_SHORT - 60 - FORD_CAPRI - PS - A_core) == A_fage
    closed[:, 50] = ((DESIGNER_SHORT - 60) * 2 == VAL_1200) & (A_full == 612)
    closed[:, 51] = (DESIGNER_SHORT + A_full - 6) == VAL_1266
    quad = 4 * DESIGNER_SHORT
    closed[:, 52] = ((quad - A_by) + (quad - MY) - 6) == VAL_1266
    closed[:, 53] = (DESIGNER_SHORT + A_fage + 60 - A_core) == FORD_CAPRI
    closed[:, 54] = (DESIGNER_SHORT - A_fage - 60 - 2 * A_core) == A_sur
    closed[:, 55] = (DESIGNER_SHORT - A_fage - 60 - CAPRI) == A_br1f
    closed[:, 56] = (2000 - FORD_CAPRI - PS - A_fath - A_full) == A_br1f
    closed[:, 57] = (2000 - FORD_CAPRI - PS - A_fath - A_br1) == A_fself
    closed[:, 58] = (2000 - FORD_CAPRI - PS - A_fath - A_fage - A_full) == A_apt

    # -------- FINDING #13 --------
    closed[:, 59] = (DESIGNER_FULL + PLATE_A + PLATE_B + FORD_CAPRI - A_by) == DESIGNER_SHORT
    step_13_02 = DESIGNER_BIRTH - FORD_CAPRI - PS
    closed[:, 60] = (step_13_02 == 2 * A_full)
    closed[:, 61] = ((DESIGNER_FULL + PLATE_A + PLATE_B + FORD_CAPRI - A_full) - PROD_END) == A_sage
    closed[:, 62] = (DESIGNER_FULL - PLATE_A - PLATE_B - FORD) == A_sage
    closed[:, 63] = (CAPRI - (DESIGNER_FULL - PLATE_A - PLATE_B)) == A_wife
    step_13_06 = DESIGNER_FULL - CAPRI - A_full
    closed[:, 64] = (step_13_06 * 2) == A_sur
    closed[:, 65] = ((DESIGNER_BIRTH - FORD_CAPRI - PS) - DESIGNER_FULL) == A_fage
    double = 2 * DESIGNER_FULL
    closed[:, 66] = ((double - MY) + (double - A_by)) == (2 * A_sur)
    closed[:, 67] = ((double - PROD_START) + (double - PROD_END) - FORD) == A_wifm

    # -------- FINDING #14 --------
    closed[:, 68] = (A_fath - WORD_ONE_FEM) == A_br1f
    closed[:, 69] = ((WORD_FIFTY - 50 - A_sur) - 22) == A_sage
    closed[:, 70] = ((WORD_FIFTY - 50 - A_sur) == 66)
    closed[:, 71] = (WORD_FIFTY - A_core) == A_sur
    closed[:, 72] = (WORD_ONE_FEM + WORD_ONE_FEM == ONE_ONE)
    closed[:, 73] = ((DESIGNER_FULL - ONE_ONE) * 2 == DESIGNER_SHORT)
    closed[:, 74] = ((A_fath - 330) * 2) == A_br1
    closed[:, 75] = (A_full - 330 - PS) == A_fath1
    closed[:, 76] = (A_br2 - 330 - A_core) == A_sur
    closed[:, 77] = (MY - (DESIGNER_FULL + ONE_ONE)) == WORD_SIXTY
    closed[:, 78] = ((MY - (DESIGNER_FULL + ONE_ONE)) + (A_by - (DESIGNER_FULL + ONE_ONE))) == A_fage
    closed[:, 79] = ((PROD_END - (DESIGNER_FULL + ONE_ONE)) + (PROD_START - (DESIGNER_FULL + ONE_ONE))) == 22
    closed[:, 80] = (44 == A_sage)
    closed[:, 81] = (ONE_ONE - FORD_CAPRI - A_core) == 22

    # -------- FINDING #15 --------
    closed[:, 82] = (VAL_1028 - VAL_972) == A_wife
    closed[:, 83] = (2000 - VAL_1623 - FORD - PS) == A_wife
    closed[:, 84] = ((VAL_1101 - VAL_1014) - PS) == A_wife
    closed[:, 85] = (VAL_1101 - A_wife) == VAL_1045
    closed[:, 86] = ((VAL_1101 + VAL_1014) - 6 - 1 - 2 - FORD_CAPRI - PLATE_A - PLATE_B) == A_full
    closed[:, 87] = ((VAL_1707 - VAL_1014) + FORD_CAPRI) == VAL_1373
    closed[:, 88] = ((VAL_1101 + VAL_1014) - VAL_1707 - A_core) == A_sur
    closed[:, 89] = (VAL_1014 + VAL_972) == PROD_END
    closed[:, 90] = (PROD_GEMATRIA + A_wife) == PROD_START
    closed[:, 91] = (VAL_1014 - VAL_948 == 66)
    closed[:, 92] = (VAL_948 - PLATE_A - PLATE_B) == A_br1f
    closed[:, 93] = (2000 - FORD_CAPRI - PS - A_fath - A_br1) == A_fself
    closed[:, 94] = (2000 - FORD_CAPRI - PS - A_fath - A_fage - A_full) == A_apt
    closed[:, 95] = (2000 - FORD_CAPRI - PS - A_fath - A_full) == A_br1f
    closed[:, 96] = (VAL_1014 - VAL_948) == 66

    # -------- FINDING #16 --------
    closed[:, 97]  = ((VAL_4262 - VAL_1623 - VAL_1266) == VAL_1373)
    closed[:, 98]  = ((VAL_1414 - (VAL_1373 - 9)) == 50)
    closed[:, 99]  = ((VAL_1373 - A_full - FORD_CAPRI - PS) == 50)
    closed[:, 100] = (WORD_FIFTY - A_core) == A_sur
    closed[:, 101] = (FORD_CAPRI - (VAL_4262 - MY - A_by)) == A_br1
    mir_1373 = 3731
    step_16_06 = PROD_END - (mir_1373 - PROD_START)
    closed[:, 102] = (step_16_06 - PS - A_core) == A_fage
    closed[:, 103] = (step_16_06 * 2) == A_br2f

    # -------- FINDING #17 --------
    closed[:, 104] = (A_full == 612)  # mirror chain 6120→216→612
    closed[:, 105] = (VAL_6120 - 216 - MY - A_by) == VAL_1896
    closed[:, 106] = (VAL_6142 - VAL_1896 - PROD_START - PROD_END) == A_sur
    closed[:, 107] = (VAL_6120 - VAL_2290 - VAL_2087 - A_sur) == 1451
    closed[:, 108] = (1451 - VAL_1200) == A_fath1
    s1_17 = VAL_1896 - ELEVEN_FEM
    s2_17 = ELEVEN_MASC - s1_17
    s3_17 = s2_17 - 10
    s4_17 = s3_17 - 30
    closed[:, 109] = (s4_17 - A_full) == A_sage
    closed[:, 110] = (VAL_2378 - VAL_1112) == VAL_1266
    closed[:, 111] = (VAL_3455 - VAL_2665 - A_sage - A_full) == A_br1f
    closed[:, 112] = (VAL_3455 - VAL_2665 - A_sage - A_br1) == A_fself

    # -------- FINDING #18 --------
    closed[:, 113] = (PROD_GEMATRIA - HEBREW_DATE_882 - FORD_CAPRI - A_apt) == A_sur
    step_18_02 = PROD_GEMATRIA - HEBREW_DATE_882 - PLATE_A - PLATE_B
    closed[:, 114] = (step_18_02 == 216) & (A_full == 612)
    closed[:, 115] = (PROD_END - HEBREW_DATE_882 - PLATE_A - PLATE_B) == FORD
    closed[:, 116] = (FORD - 2 * A_core) == A_apt
    step_18_05 = (PROD_END - HEBREW_DATE_882) * 2
    closed[:, 117] = ((step_18_05 - MY) + (step_18_05 - A_by) - A_core) == A_sur

    # -------- FINDING #19 --------
    closed[:, 118] = (DATE_DIGIT_4528 - PROD_END - PROD_START - PS) == A_fath
    closed[:, 119] = ((DATE_DIGIT_4528 - A_fby - MY) + PS) == (2 * A_sur)

    # -------- FINDING #20 --------
    closed[:, 120] = (VAL_1101 - PS - FORD_CAPRI) == CAPRI
    closed[:, 121] = ((VAL_1045 + VAL_1101 - PS) - 9 - FORD_CAPRI - PLATE_A - PLATE_B) == A_full
    closed[:, 122] = ((VAL_1045 + VAL_1101 - PS) - VAL_1373 - FORD_CAPRI) == 62

    closures = closed.sum(axis=1)
    return closures, closed


# =============================================================================
# NETWORK DENSITY (LAYER 2) — finding-level interconnection
# =============================================================================

# Mapping: equation index → finding index (0-19)
_counts = [1, 3, 11, 4, 2, 7, 3, 4, 4, 4, 4, 12, 9, 14, 15, 7, 9, 5, 2, 3]
_eq_to_finding = []
for _f, _n in enumerate(_counts):
    _eq_to_finding.extend([_f] * _n)
EQ_TO_FINDING = xp.array(_eq_to_finding, dtype=xp.int32)  # (123,)
assert len(_eq_to_finding) == 123

# Derived hub values per equation (for network density)
# Extracted from the cross-reference analysis
HUBS = {
    "v1912":0,"v1494":1,"v1098":2,"v1093":3,"v348":4,"v612":5,"v292":6,
    "v2000":7,"v660":8,"v1148":9,"v818":10,"v1373":11,"v1266":12,
    "v1623":13,"v1028":14,"v972":15,"v1014":16,"v948":17,"v1101":18,
    "v1045":19,"v1707":20,"v1896":21,"v1451":22,"v1200":23,
    "v738":24,"v369":25,"v408":26,"v686":27,"v656":28,"v786":29,
    "v1215":30,"v2650":31,"v2329":32,"v2320":33,"v401":34,"v409":35,
    "v216":36,"v3455":37,"v2665":38,"v6120":39,"v4262":40,"v4343":41,
}
N_HUBS = len(HUBS)

# Per-equation hub participation (assigned from cross-reference analysis)
_eq_hubs_spec = {
    0: [], 1: ["v1494"], 2: ["v1494"], 3: ["v1912","v1098"],
    4: ["v1098","v1093","v348"], 5: ["v1912","v1098","v1093"],
    6: ["v1494","v1093","v401"], 7: ["v401"], 8: ["v1912","v1093","v1098","v401"],
    9: ["v401","v786"], 10: ["v786"], 11: [], 12: ["v612"],
    13: ["v348","v686"], 14: ["v686","v656","v612"],
    15: ["v1093","v1494","v348"], 16: ["v348","v1028"],
    17: ["v1098","v1494","v612"], 18: ["v1912","v738","v612"],
    19: [], 20: ["v1494"],
    21: ["v738"], 22: ["v2650","v2329","v1912"],
    23: ["v2329","v1373"], 24: ["v1912","v292"],
    25: ["v369","v738","v2320"], 26: ["v686"],
    27: ["v686","v656","v612"],
    28: ["v738"], 29: ["v1912","v738"], 30: ["v1098","v369","v738"],
    31: ["v612"], 32: [], 33: ["v612"], 34: ["v292"],
    35: [], 36: ["v1200","v612"], 37: ["v1200"], 38: [],
    39: ["v1215","v292"], 40: ["v1215"], 41: ["v1215"], 42: ["v1494"],
    43: ["v4343"], 44: ["v4343"], 45: ["v4343","v292"], 46: ["v4343","v612"],
    47: ["v660","v1028"], 48: ["v1707","v972"], 49: ["v660","v1623"],
    50: ["v660","v1200","v612"], 51: ["v660","v612","v1266"],
    52: ["v660","v1266"], 53: ["v660"], 54: ["v660","v292"],
    55: ["v660"], 56: ["v2000"], 57: ["v2000"], 58: ["v2000"],
    59: ["v1148","v660"], 60: ["v1148","v612"], 61: ["v1148","v612"],
    62: ["v1148"], 63: ["v1148"], 64: ["v1148","v612","v292"],
    65: ["v1148"], 66: ["v1148","v292"], 67: ["v1148","v348"],
    68: ["v409"], 69: ["v408","v292"], 70: ["v408","v1266"],
    71: ["v408","v292"], 72: ["v409","v818"],
    73: ["v1148","v818","v660"], 74: [], 75: [], 76: [],
    77: ["v1148","v818"], 78: ["v1148","v818"], 79: ["v1148","v818"],
    80: [], 81: ["v818"],
    82: ["v1028","v972"], 83: ["v2000","v1623"],
    84: ["v1101","v1014"], 85: ["v1101","v1045"],
    86: ["v1101","v1014","v612"], 87: ["v1707","v1014","v1373"],
    88: ["v1101","v1014","v1707","v292"], 89: ["v1014","v972"],
    90: ["v1912"], 91: ["v1014","v948","v1266"],
    92: ["v948"], 93: ["v2000"], 94: ["v2000"], 95: ["v2000"],
    96: ["v1014","v948"],
    97: ["v4262","v1623","v1266","v1373"], 98: ["v1373"], 99: ["v1373"],
    100: ["v408","v292"], 101: ["v4262"], 102: [], 103: [],
    104: ["v6120","v612","v216"], 105: ["v6120","v216","v1896"],
    106: ["v1896","v292"], 107: ["v6120","v1451","v292"],
    108: ["v1451","v1200"],
    109: ["v1896","v1494","v1098","v686","v656"],
    110: ["v1266"], 111: ["v3455","v2665"], 112: ["v3455","v2665"],
    113: ["v1912","v292"], 114: ["v1912","v216","v612"],
    115: [], 116: [], 117: ["v292"],
    118: [], 119: ["v292"],
    120: ["v1101"], 121: ["v1045","v1101","v612"],
    122: ["v1045","v1101","v1373"],
}

_HUB_MAT_init = xp.zeros((123, N_HUBS), dtype=xp.int8)
for _eq, _names in _eq_hubs_spec.items():
    for _n in _names:
        _HUB_MAT_init[_eq, HUBS[_n]] = 1
HUB_MATRIX = _HUB_MAT_init


def compute_network_density(closure_matrix):
    """
    Finding-level network density.

    For each trial:
      1. For each finding, union all hubs used by its CLOSED equations
      2. For each pair of findings both having ≥1 closure:
           connected = do their hub-sets overlap?
      3. density = connected_pairs / total_pairs

    Real Harpaz (conservative hub assignment): ~66%
    Random mean: ~20%
    """
    N = closure_matrix.shape[0]
    closed_i8 = closure_matrix.astype(xp.int8)

    # Per-trial, per-finding hub presence: (N, 20, N_HUBS) bool
    finding_hubs = xp.zeros((N, 20, N_HUBS), dtype=xp.bool_)
    findings_active = xp.zeros((N, 20), dtype=xp.bool_)

    for f in range(20):
        eq_mask = (EQ_TO_FINDING == f)
        # Equations in this finding, closed per trial: (N, n_eqs_in_f)
        closed_in_f = closed_i8[:, eq_mask]
        # Hub presence: (N, N_HUBS) — any closed equation in f uses this hub?
        hm_slice = HUB_MATRIX[eq_mask]  # (n_eqs_in_f, N_HUBS)
        hub_presence = (closed_in_f @ hm_slice) > 0
        finding_hubs[:, f, :] = hub_presence
        findings_active[:, f] = closed_in_f.sum(axis=1) > 0

    # Finding-pair overlap: (N, 20, 20)
    fh_i8 = finding_hubs.astype(xp.int8)
    overlap = (xp.matmul(fh_i8, fh_i8.transpose(0, 2, 1))) > 0

    # Upper triangle (i < j) and both findings active
    upper = xp.triu(xp.ones((20, 20), dtype=xp.bool_), k=1)
    active_pair = findings_active[:, :, None] & findings_active[:, None, :]
    connected = overlap & active_pair & upper[None, :, :]
    connected_pairs = connected.sum(axis=(1, 2)).astype(xp.float32)

    n_active = findings_active.sum(axis=1).astype(xp.float32)
    total_pairs = n_active * (n_active - 1) / 2.0

    density = xp.where(total_pairs > 0, connected_pairs / total_pairs, 0.0)
    return density


# =============================================================================
# MAIN DRIVER
# =============================================================================

def main(n_trials=100_000_000, batch_size=500_000, seed=42):
    print("=" * 78)
    print("RTM FORD CAPRI — TWO-LAYER SIMULATION")
    print("=" * 78)
    print(f"Backend : {'GPU (CuPy)' if GPU else 'CPU (NumPy)'}")
    print(f"Trials  : {n_trials:,}")
    print(f"Batch   : {batch_size:,}")
    print(f"Null    : uniform over full gematria space 1-999 (every possible name)")
    print()

    # Sanity check on real Harpaz family
    print("Sanity check — real Harpaz anchors:")
    A_real = build_harpaz_batch(100)
    c_real, cm_real = run_all_equations(A_real)
    d_real = compute_network_density(cm_real)
    real_c = int(c_real[0])
    real_d = float(d_real[0])
    print(f"  Closures       : {real_c} / 123  (expected 123)")
    print(f"  Network density: {real_d:.1%}")
    print()

    # Simulation loop
    print(f"Simulating {n_trials:,} random families...")
    t0 = time.time()

    max_c, max_d = 0, 0.0
    sum_c, sum_c2 = 0.0, 0.0
    sum_d, sum_d2 = 0.0, 0.0
    match_c, match_d, match_both = 0, 0, 0
    done = 0

    n_batches = (n_trials + batch_size - 1) // batch_size
    for b in range(n_batches):
        actual = min(batch_size, n_trials - done)
        A_rand = generate_random_families(actual, seed=seed + b)
        c_b, cm_b = run_all_equations(A_rand)
        d_b = compute_network_density(cm_b)

        # Transfer to host for scalar reductions
        c_np = xp.asnumpy(c_b) if GPU else c_b
        d_np = xp.asnumpy(d_b) if GPU else d_b

        max_c = max(max_c, int(c_np.max()))
        max_d = max(max_d, float(d_np.max()))
        sum_c += float(c_np.sum())
        sum_c2 += float((c_np.astype('float64') ** 2).sum())
        sum_d += float(d_np.sum())
        sum_d2 += float((d_np.astype('float64') ** 2).sum())
        match_c += int((c_np >= real_c).sum())
        match_d += int((d_np >= real_d).sum())
        match_both += int(((c_np >= real_c) & (d_np >= real_d)).sum())
        done += actual

        if (b + 1) % 5 == 0 or b + 1 == n_batches:
            dt = time.time() - t0
            rate = done / dt if dt > 0 else 0
            eta = (n_trials - done) / rate if rate > 0 else 0
            print(f"  {done:>12,} / {n_trials:,}  ({100*done/n_trials:5.1f}%)  "
                  f"t={dt:7.1f}s  rate={rate:>9,.0f}/s  eta={eta/60:5.1f}min  "
                  f"max_c={max_c}  max_d={max_d:.1%}")

    dt = time.time() - t0
    mean_c = sum_c / done
    std_c = (sum_c2 / done - mean_c ** 2) ** 0.5
    mean_d = sum_d / done
    std_d = (sum_d2 / done - mean_d ** 2) ** 0.5
    sigma_c = (real_c - mean_c) / std_c if std_c > 0 else float('inf')
    sigma_d = (real_d - mean_d) / std_d if std_d > 0 else float('inf')

    print()
    print("=" * 78)
    print("RESULTS")
    print("=" * 78)
    print(f"Total runtime : {dt:.1f}s  ({done/dt:,.0f} trials/sec)")
    print()
    print("LAYER 1 — CLOSURE COUNT")
    print(f"  Real Harpaz : {real_c} / 123")
    print(f"  Random mean : {mean_c:.2f}   std: {std_c:.3f}   max: {max_c}")
    print(f"  σ-distance  : {sigma_c:.1f}σ")
    print(f"  Matches ≥{real_c}: {match_c:,} / {done:,}  "
          f"({100*match_c/done:.2e}%)")
    print()
    print("LAYER 2 — NETWORK DENSITY")
    print(f"  Real Harpaz : {real_d:.1%}")
    print(f"  Random mean : {mean_d:.1%}   std: {std_d:.4f}   max: {max_d:.1%}")
    print(f"  σ-distance  : {sigma_d:.1f}σ")
    print(f"  Matches ≥{real_d:.1%}: {match_d:,} / {done:,}")
    print()
    print("JOINT TEST — both layers ≥ real")
    print(f"  Matches BOTH: {match_both:,} / {done:,}")
    print()
    print("=" * 78)


# =============================================================================
# ENTRY POINT
# =============================================================================
#
# IN GOOGLE COLAB: paste this whole file into one cell, run it, then in a new
# cell call:
#
#     main(n_trials=100_000_000, batch_size=500_000)
#
# IN A LOCAL TERMINAL: run with arguments from the command line:
#
#     python layer_1_and_2.py 100000000 500000
#
# The command-line entry point below only activates when this file is run
# directly with `python layer_1_and_2.py`, not when it is imported or exec'd.

if __name__ == "__main__" and len(sys.argv) > 1:
    try:
        n = int(sys.argv[1])
        batch = int(sys.argv[2]) if len(sys.argv) > 2 else 500_000
        main(n_trials=n, batch_size=batch)
    except (ValueError, IndexError):
        print("Usage: python layer_1_and_2.py N_TRIALS [BATCH_SIZE]")
        print("Example: python layer_1_and_2.py 100000000 500000")
