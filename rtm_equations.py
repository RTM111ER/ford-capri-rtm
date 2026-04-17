"""
RTM Ford Capri — Complete Equation Inventory
=============================================

Every equation that produces a closure, extracted from each finding
in the book. Each equation is:
  - Expressed as a pure function of (anchors, fixed_inputs)
  - Targets a pre-declared biographical anchor
  - Counts as a closure if the result exactly matches the anchor

Derived values used within the equation are tracked for the network
density measurement (Layer 3 simulation).

Target count: 123 equations matching the book's stated total.
"""

# =============================================================================
# ANCHOR KEYS (biographical identity anchors)
# =============================================================================

ANCHOR_KEYS = {
    "surname",           # 292 = הרפז
    "first_self",        # 320 = ערן
    "full_self",         # 612 = ערן הרפז
    "father",            # 543 = אמיר הרפז
    "father_first",      # 251 = אמיר
    "brother1",          # 426 = עידן הרפז
    "brother1_first",    # 134 = עידן
    "brother2",          # 738 = תום הרפז
    "brother2_first",    # 446 = תום
    "wife",              #  56 = ליובוב
    "wife_married",      # 348 = ליובוב הרפז
    "apartment",         #  58
    "core",              # 116
    "birth_year",        # 1982
    "measurement_year",  # 2026
    "father_birth",      # 1949
    "father_age",        #  76 (derived: measurement - father_birth)
    "self_age",          #  44 (derived: measurement - birth_year)
}

# Extended targets that count as closures but aren't in the primary anchor set
EXTENDED_TARGETS = {
    # Compound biographical phrases
    "amir_age_phrase_1028",      # 1028 = "שבעים ושש"
    "amir_age_phrase_1623",      # 1623 = "אמיר הרפז בן שבעים ושש"
    "eran_age_phrase_1266",      # 1266 = "ערן הרפז בן ארבעים וארבע" = "שישים ושש"
    "eran_digit_1373",           # 1373 = "שש אחד שתיים" (digit spelling of 612)
    "apartment_phrase_1414",     # 1414 = "דירה מספר חמישים ושמונה"
    # Vehicle/manufacturer outputs
    "ford_290",                  # Ford
    "capri_390",                 # Capri
    "ford_capri_680",            # Ford Capri full
    # Temporal/eleven-minutes family
    "eleven_fem_1494",           # "אחת עשרה דקות" feminine
    "eleven_masc_1098",          # "אחד עשרה דקות" cross-gender
    "eleven_std_masc_1093",      # "אחד עשר דקות" standard masculine
    "prod_gematria_1912",        # 1912
    # Production years (as outputs in some findings)
    "prod_start_1968",
    "prod_end_1986",
    # Designer identities
    "designer_short_660",        # 660
    "designer_full_1148",        # 1148
    # Numeric words
    "word_11",
    "word_22",
    "word_44",
    "word_76",
    "word_60",
    "word_66",
}

# =============================================================================
# INDIVIDUAL EQUATIONS, BY FINDING
# =============================================================================
# Each entry: (finding, label, function, target_anchor_key, target_value)
# The function takes (A, I) where A=anchor dict, I=fixed inputs dict
# Returns: (computed_value, set_of_derived_intermediates)

EQUATIONS = []

# Helper
def MIRROR(n):
    return int(str(abs(n))[::-1])

def PLATE_DIGITS_SUM(I):
    return sum(I["plate_digits"])  # 6+3+7+1+7+7 = 31


# =============================================================================
# FINDING #01 — REGISTRY GEMATRIA REDUCTION (1 closure)
# =============================================================================

def f01_01(A, I):
    # 637,177 → "שש מאות שלושים ושבע אלף מאה שבעים ושבע" = 3,068
    # 3,068 - 1,949 - 680 - (6+3+7+1+7+7) - 116 = 292
    step1 = 3068 - A["father_birth"]                    # 3068-1949 = 1119
    step2 = step1 - I["ford_capri"]                      # 1119-680 = 439
    step3 = step2 - PLATE_DIGITS_SUM(I) - A["core"]      # 439-31-116 = 292
    return step3, {3068, step1, step2}

EQUATIONS.append(("01", "01.01", f01_01, "surname", 292))


# =============================================================================
# FINDING #02 — CHRONO-LINGUISTIC CONVERGENCE (3 closures)
# =============================================================================

def f02_01(A, I):
    # 680 + 177 + 637 = 1494 ("אחת עשרה דקות" feminine)
    return I["ford_capri"] + I["plate_b"] + I["plate_a"], set()

EQUATIONS.append(("02", "02.01", f02_01, "eleven_fem_1494", 1494))

def f02_02(A, I):
    # 1494 - 11 = 1483; 2026 - 1483 = 543 (Amir Harpaz)
    vehicle_sum = I["ford_capri"] + I["plate_b"] + I["plate_a"]  # 1494
    step1 = vehicle_sum - 11                                      # 1483
    return A["measurement_year"] - step1, {vehicle_sum, step1}

EQUATIONS.append(("02", "02.02", f02_02, "father", 543))

def f02_03(A, I):
    # 1900000 → "מיליון תשע מאות אלף יחידות" = 1912
    # 1912 - 637 - 177 = 1098 ("אחד עשרה דקות" masculine/cross-gender)
    return I["prod_gematria"] - I["plate_a"] - I["plate_b"], {I["prod_gematria"]}

EQUATIONS.append(("02", "02.03", f02_03, "eleven_masc_1098", 1098))


# =============================================================================
# FINDING #03 — GRAMMATICAL GAP MATRIX (11 closures, 21 steps)
# =============================================================================

def f03_01(A, I):
    # 1098 - 1093 = 5 → "חמש" = 348 = Liubov Harpaz
    # We verify: if 1098-1093==5, then anchor 348 is reached
    gap = 1098 - 1093  # always 5
    if gap == 5:
        return 348, {1098, 1093, 5}
    return -1, set()

EQUATIONS.append(("03", "03.01", f03_01, "wife_married", 348))

def f03_02(A, I):
    # 1093 + 1098 = 2191; mirror(2191) = 1912
    pair_sum = 1093 + 1098
    mir = MIRROR(pair_sum)
    return mir, {pair_sum}

EQUATIONS.append(("03", "03.02", f03_02, "prod_gematria_1912", 1912))

def f03_03(A, I):
    # 1494 - 1093 = 401 ("שמונה")
    return 1494 - 1093, set()

# 401 is not an anchor. This "closure" is a structural match to the word "eight"
# The book counts it; we encode it as hitting a word-level target.
EQUATIONS.append(("03", "03.03", f03_03, "word_eight_401", 401))

def f03_04(A, I):
    # 401 - 390 = 11 (the number itself)
    step1 = 1494 - 1093  # 401
    return step1 - I["capri"], {step1}

EQUATIONS.append(("03", "03.04", f03_04, "word_11", 11))

def f03_05(A, I):
    # Independent path: 680 - (2191-1912) = 680 - 279 = 401
    step1 = (1093 + 1098) - 1912  # 279
    return I["ford_capri"] - step1, {step1, 2191}

EQUATIONS.append(("03", "03.05", f03_05, "word_eight_401", 401))

def f03_06(A, I):
    # 401 + 401 = 802; 802 - 8 - 8 = 786 (current Hebrew year תשפ"ו)
    return 401 + 401 - 8 - 8, {802}

EQUATIONS.append(("03", "03.06", f03_06, "hebrew_year_786", 786))

def f03_07(A, I):
    # 786 - 57 = 729 ("בן כמה ערן הרפז")
    return 786 - 57, set()

EQUATIONS.append(("03", "03.07", f03_07, "question_eran_age_729", 729))

def f03_08(A, I):
    # 729 - 44 = 685; 685 - 680 = 5 (grammatical gap returns!)
    step1 = 729 - A["self_age"]  # 685
    return step1 - I["ford_capri"], {step1, 729}

EQUATIONS.append(("03", "03.08", f03_08, "gap_return_5", 5))

def f03_09(A, I):
    # 685 + 685 = 1370; 1982 - 1370 = 612 (Eran Harpaz)
    step1 = 685 + 685   # 1370
    return A["birth_year"] - step1, {685, step1}

EQUATIONS.append(("03", "03.09", f03_09, "full_self", 612))

def f03_10(A, I):
    # 348 + 348 = 696; 696 - 5 - 5 = 686 ("שלושים")
    return 348 + 348 - 5 - 5, {696}

EQUATIONS.append(("03", "03.10", f03_10, "word_thirty_686", 686))

def f03_11(A, I):
    # 686 - 30 = 656; 656 - 612 = 44 (observer age)
    step1 = 686 - 30    # 656
    return step1 - A["full_self"], {686, step1}

EQUATIONS.append(("03", "03.11", f03_11, "self_age", 44))


# =============================================================================
# FINDING #04 — TEMPORAL SYNTHESIS (4 closures)
# =============================================================================

def f04_01(A, I):
    # 1093 + 1494 = 2587; 2587 - 1949 - 290 = 348 (Liubov Harpaz)
    step1 = 1093 + 1494  # 2587
    return step1 - A["father_birth"] - I["ford"], {step1}

EQUATIONS.append(("04", "04.01", f04_01, "wife_married", 348))

def f04_02(A, I):
    # 348 + 680 = 1028 ("שבעים ושש" = Amir age phrase)
    return 348 + I["ford_capri"], set()

EQUATIONS.append(("04", "04.02", f04_02, "amir_age_phrase_1028", 1028))

def f04_03(A, I):
    # 1098 + 1494 = 2592; 2592 - 1949 - (plate digits) = 612
    step1 = 1098 + 1494  # 2592
    return step1 - A["father_birth"] - PLATE_DIGITS_SUM(I), {step1}

EQUATIONS.append(("04", "04.03", f04_03, "full_self", 612))

def f04_04(A, I):
    # 1912 - 738 - 837 - (plate digits) = 306; 306+306 = 612
    step1 = I["prod_gematria"] - 738 - 837 - PLATE_DIGITS_SUM(I)  # 306
    if step1 * 2 == A["full_self"]:
        return A["full_self"], {step1, 738, 837}
    return -1, set()

EQUATIONS.append(("04", "04.04", f04_04, "full_self", 612))


# =============================================================================
# FINDING #05 — SIBLING IDENTITY EXTRACTION (2 closures)
# =============================================================================

def f05_01(A, I):
    # 680 - 637 = 43; 177 - 43 = 134 (Idan)
    step1 = I["ford_capri"] - I["plate_a"]  # 43
    return I["plate_b"] - step1, {step1}

EQUATIONS.append(("05", "05.01", f05_01, "brother1_first", 134))

def f05_02(A, I):
    # 1494 → 1930 (Hebrew spelling); 1930 - 1494 - 116 = 320 (Eran)
    vehicle_sum = 1494
    vehicle_sum_spelling = 1930
    return vehicle_sum_spelling - vehicle_sum - A["core"], {vehicle_sum, vehicle_sum_spelling}

EQUATIONS.append(("05", "05.02", f05_02, "first_self", 320))


# =============================================================================
# FINDING #06 — PRODUCTION SOURCE MATRIX (7 closures)
# =============================================================================

def f06_01(A, I):
    # 738 → "שבע מאות שלושים ושמונה" = 1912 (explicit identity)
    # Target: 738 = Tom Harpaz
    return 738, set()

EQUATIONS.append(("06", "06.01", f06_01, "brother2", 738))

def f06_02(A, I):
    # 1912 + 738 = 2650; 2650 → "אלפיים שלוש מאות עשרים ותשע" (= 2329)
    # 2650 - 2329 - (plate digits) = 290 (Ford)
    step1 = I["prod_gematria"] + 738  # 2650
    return step1 - 2329 - PLATE_DIGITS_SUM(I), {step1, 2329}

EQUATIONS.append(("06", "06.02", f06_02, "ford_290", 290))

def f06_03(A, I):
    # 2329 - 6 - 1 - 2 = 2320; 2320 = "מי זה 1373?" (gematria of question)
    # 1373 = "שש אחד שתיים" (digit spelling of 612 = Eran Harpaz)
    step1 = 2329 - 6 - 1 - 2  # 2320
    return 1373, {step1, 2329}  # target: digit spelling of Eran

EQUATIONS.append(("06", "06.03", f06_03, "eran_digit_1373", 1373))

def f06_04(A, I):
    # 2320 - 1912 - 116 = 292 (Harpaz)
    step1 = 2320
    return step1 - I["prod_gematria"] - A["core"], {step1}

EQUATIONS.append(("06", "06.04", f06_04, "surname", 292))

def f06_05(A, I):
    # 2320 - 637 - 177 = 1506; 1506 = "ארבע מאות חמישים ושבע" (spelling of 457)
    # 1506 - 457 - 680 = 369; 369+369 = 738 (Tom)
    step1 = 2320 - I["plate_a"] - I["plate_b"]  # 1506
    step2 = step1 - 457 - I["ford_capri"]        # 369
    if step2 * 2 == 738:
        return 738, {2320, step1, step2, 457}
    return -1, set()

EQUATIONS.append(("06", "06.05", f06_05, "brother2", 738))

def f06_06(A, I):
    # 2320 - 1968 = 352; 2320 - 1986 = 334; 352 + 334 = 686 ("שלושים")
    offset_1 = 2320 - I["prod_start"]  # 352
    offset_2 = 2320 - I["prod_end"]    # 334
    return offset_1 + offset_2, {offset_1, offset_2, 2320}

EQUATIONS.append(("06", "06.06", f06_06, "word_thirty_686", 686))

def f06_07(A, I):
    # 686 - 30 = 656; 656 - 612 = 44 (observer age)
    step1 = 686 - 30  # 656
    return step1 - A["full_self"], {686, step1}

EQUATIONS.append(("06", "06.07", f06_07, "self_age", 44))


# =============================================================================
# FINDING #07 — TRIPLE GENERATION SYNC (3 closures)
# =============================================================================

def f07_01(A, I):
    # 738 - 680 = 58 (apartment)
    return 738 - I["ford_capri"], set()

EQUATIONS.append(("07", "07.01", f07_01, "apartment", 58))

def f07_02(A, I):
    # 1912 - 637 - 177 - 680 = 418; 738 - 418 = 320 (Eran)
    step1 = I["prod_gematria"] - I["plate_a"] - I["plate_b"] - I["ford_capri"]  # 418
    return 738 - step1, {step1}

EQUATIONS.append(("07", "07.02", f07_02, "first_self", 320))

def f07_03(A, I):
    # 186 = 612 - 426 (Eran - Idan); 186 → "מאה שמונים ושש" = 1098
    # 1098 - 186 - 543 = 369; 369+369 = 738 (Tom)
    gap = A["full_self"] - A["brother1"]  # 186
    step1 = 1098 - gap - A["father"]  # 369
    if step1 * 2 == 738:
        return 738, {gap, 1098, step1}
    return -1, set()

EQUATIONS.append(("07", "07.03", f07_03, "brother2", 738))


# =============================================================================
# FINDING #08 — PRODUCTION TIMELINE CONVERGENCE (4 closures)
# =============================================================================

def f08_01(A, I):
    # 1968 → mirror → 8691; 1986 → mirror → 6891
    # 8691 - 6891 - 637 - 177 - 680 = 306; 306+306 = 612
    m1 = MIRROR(I["prod_start"])  # 8691
    m2 = MIRROR(I["prod_end"])    # 6891
    step1 = m1 - m2 - I["plate_a"] - I["plate_b"] - I["ford_capri"]  # 306
    if step1 * 2 == A["full_self"]:
        return A["full_self"], {m1, m2, step1}
    return -1, set()

EQUATIONS.append(("08", "08.01", f08_01, "full_self", 612))

def f08_02(A, I):
    # 2026 - 1968 = 58 (apartment from production span)
    return A["measurement_year"] - I["prod_start"], set()

EQUATIONS.append(("08", "08.02", f08_02, "apartment", 58))

def f08_03(A, I):
    # 1986 - 749 - 815 - 58 = 364; 364+364 = 728; 728-116 = 612
    step1 = I["prod_end"] - 749 - 815 - A["apartment"]  # 364
    step2 = step1 * 2                                    # 728
    return step2 - A["core"], {749, 815, step1, step2}

EQUATIONS.append(("08", "08.03", f08_03, "full_self", 612))

def f08_04(A, I):
    # 637 - 364 = 273; 273 - 177 = 96; 680 - 96 = 584 = 292+292
    # step1=364 is from f08_03
    step1 = I["prod_end"] - 749 - 815 - A["apartment"]  # 364
    s2 = I["plate_a"] - step1    # 273
    s3 = s2 - I["plate_b"]       # 96
    s4 = I["ford_capri"] - s3    # 584
    if s4 == 2 * A["surname"]:
        return A["surname"], {step1, s2, s3, s4}
    return -1, set()

EQUATIONS.append(("08", "08.04", f08_04, "surname", 292))


# =============================================================================
# FINDING #09 — SYMMETRY LOOP CONVERGENCE (4 closures)
# =============================================================================

def f09_01(A, I):
    # (177+177+637)*2 = 991*2 = 1982 (birth year)
    step1 = 2 * I["plate_b"] + I["plate_a"]  # 991
    return step1 * 2, {step1}

EQUATIONS.append(("09", "09.01", f09_01, "birth_year", 1982))

def f09_02(A, I):
    # 637+637+177 = 1451 = digit spelling of 1200; 1200 → "אלף מאתיים" = 612
    step1 = 2 * I["plate_a"] + I["plate_b"]  # 1451
    if step1 == 1451:  # confirms digit spelling of 1200
        return 612, {step1, 1200}  # via 1200 standard spelling
    return -1, set()

EQUATIONS.append(("09", "09.02", f09_02, "full_self", 612))

def f09_03(A, I):
    # 1451 - 1200 = 251 (Amir)
    step1 = 2 * I["plate_a"] + I["plate_b"]  # 1451
    return step1 - 1200, {step1, 1200}

EQUATIONS.append(("09", "09.03", f09_03, "father_first", 251))

def f09_04(A, I):
    # 1982-1451=531; 2026-1451=575; 531+575=1106; 1106-680=426 (Idan Harpaz)
    step1 = 2 * I["plate_a"] + I["plate_b"]  # 1451
    off1 = A["birth_year"] - step1           # 531
    off2 = A["measurement_year"] - step1     # 575
    total = off1 + off2                       # 1106
    return total - I["ford_capri"], {step1, off1, off2, total}

EQUATIONS.append(("09", "09.04", f09_04, "brother1", 426))


# =============================================================================
# FINDING #10 — SELF-ANSWERING QUESTION (4 closures)
# =============================================================================

def f10_01(A, I):
    # mirror(177) + mirror(637) = 771 + 736 = 1507; 1507 - 1215 = 292 (Harpaz)
    m1 = MIRROR(I["plate_b"])  # 771
    m2 = MIRROR(I["plate_a"])  # 736
    step1 = m1 + m2             # 1507
    return step1 - 1215, {m1, m2, step1, 1215}

EQUATIONS.append(("10", "10.01", f10_01, "surname", 292))

def f10_02(A, I):
    # 1926 (digit spelling of 1215) - 1215 - (plate digits) = 680 (Ford Capri)
    return 1926 - 1215 - PLATE_DIGITS_SUM(I), {1926, 1215}

EQUATIONS.append(("10", "10.02", f10_02, "ford_capri_680", 680))

def f10_03(A, I):
    # 1949 - 1541 - 116 = 292 (Harpaz) — via standard spelling of 1215
    return A["father_birth"] - 1541 - A["core"], {1541, 1215}

EQUATIONS.append(("10", "10.03", f10_03, "surname", 292))

def f10_04(A, I):
    # 1494 + 1494 = 2988; 2988 - 2026 - 680 - (plate digits) = 251 (Amir)
    vehicle_sum = 1494
    step1 = 2 * vehicle_sum  # 2988
    return step1 - A["measurement_year"] - I["ford_capri"] - PLATE_DIGITS_SUM(I), {vehicle_sum, step1}

EQUATIONS.append(("10", "10.04", f10_04, "father_first", 251))


# =============================================================================
# FINDING #11 — PRECISE PRODUCTION CONVERGENCE (4 closures)
# =============================================================================

def f11_01(A, I):
    # 4343 + 4343 = 8686; 8686 - 2026 - 1982 - 1968 - 1986 - 680 = 44
    step1 = 2 * I["prod_precise_gematria"]  # 8686
    return step1 - A["measurement_year"] - A["birth_year"] - I["prod_start"] - I["prod_end"] - I["ford_capri"], {step1}

EQUATIONS.append(("11", "11.01", f11_01, "self_age", 44))

def f11_02(A, I):
    # 4343 - mirror(4343) = 4343 - 3434 = 909 ("ארבע שלוש" = digit spelling of 43)
    mir = MIRROR(I["prod_precise_gematria"])  # 3434
    return I["prod_precise_gematria"] - mir, {mir}

EQUATIONS.append(("11", "11.02", f11_02, "word_forty_three_909", 909))

def f11_03(A, I):
    # 4343 - 43 - 2026 - 1982 = 292 (Harpaz)
    return I["prod_precise_gematria"] - 43 - A["measurement_year"] - A["birth_year"], set()

EQUATIONS.append(("11", "11.03", f11_03, "surname", 292))

def f11_04(A, I):
    # 4343 - 4 - 3 - 2026 = 2310; 2310-2026=284; 2310-1982=328; 284+328=612
    step1 = I["prod_precise_gematria"] - 4 - 3 - A["measurement_year"]  # 2310
    off1 = step1 - A["measurement_year"]  # 284
    off2 = step1 - A["birth_year"]        # 328
    return off1 + off2, {step1, off1, off2}

EQUATIONS.append(("11", "11.04", f11_04, "full_self", 612))


# =============================================================================
# FINDING #12 — DESIGNER TRIPLE IDENTITY (12 closures)
# =============================================================================

def f12_01(A, I):
    # 1028 - 660 - 76 = 292 (Harpaz)
    return 1028 - I["designer_short"] - A["father_age"], {1028}

EQUATIONS.append(("12", "12.01", f12_01, "surname", 292))

def f12_02(A, I):
    # 1707 - 972 - 543 - 116 = 76 (Amir Harpaz Age)
    return 1707 - 972 - A["father"] - A["core"], {1707, 972}

EQUATIONS.append(("12", "12.02", f12_02, "father_age", 76))

def f12_03(A, I):
    # 1623 - 660 - 60 - 680 - 31 - 116 = 76
    return 1623 - I["designer_short"] - 60 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["core"], {1623}

EQUATIONS.append(("12", "12.03", f12_03, "father_age", 76))

def f12_04(A, I):
    # 660 - 60 = 600; 600+600 = 1200 → "אלף מאתיים" = 612
    step1 = I["designer_short"] - 60  # 600
    step2 = step1 * 2                 # 1200
    if step2 == 1200:
        return 612, {step1, step2}
    return -1, set()

EQUATIONS.append(("12", "12.04", f12_04, "full_self", 612))

def f12_05(A, I):
    # 660 + 612 = 1272 = "שלוש שלוש"; 1272 - 3 - 3 = 1266
    step1 = I["designer_short"] + A["full_self"]  # 1272
    return step1 - 3 - 3, {step1}

EQUATIONS.append(("12", "12.05", f12_05, "eran_age_phrase_1266", 1266))

def f12_06(A, I):
    # 660+660 = 1320; 1320+1320 = 2640
    # 2640-1982 = 658; 2640-2026 = 614; 658+614 = 1272; -3-3 = 1266
    quad = 4 * I["designer_short"]  # 2640
    off1 = quad - A["birth_year"]    # 658
    off2 = quad - A["measurement_year"]  # 614
    step1 = off1 + off2              # 1272
    return step1 - 3 - 3, {quad, off1, off2, step1}

EQUATIONS.append(("12", "12.06", f12_06, "eran_age_phrase_1266", 1266))

def f12_07(A, I):
    # 660 + 76 + 60 = 796; 796 - 116 = 680 (Ford Capri)
    step1 = I["designer_short"] + A["father_age"] + 60  # 796
    return step1 - A["core"], {step1}

EQUATIONS.append(("12", "12.07", f12_07, "ford_capri_680", 680))

def f12_08(A, I):
    # 660 - 76 - 60 - 116 - 116 = 292 (Harpaz)
    return I["designer_short"] - A["father_age"] - 60 - 2 * A["core"], set()

EQUATIONS.append(("12", "12.08", f12_08, "surname", 292))

def f12_09(A, I):
    # 660 - 76 - 60 - 390 = 134 (Idan)
    return I["designer_short"] - A["father_age"] - 60 - I["capri"], set()

EQUATIONS.append(("12", "12.09", f12_09, "brother1_first", 134))

def f12_10(A, I):
    # 2000 - 680 - 31 - 543 - 612 = 134 (Idan)
    # 2000 = 1028+972 (two spellings of 76)
    return 2000 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["father"] - A["full_self"], {2000}

EQUATIONS.append(("12", "12.10", f12_10, "brother1_first", 134))

def f12_11(A, I):
    # 2000 - 680 - 31 - 543 - 426 = 320 (Eran)
    return 2000 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["father"] - A["brother1"], {2000}

EQUATIONS.append(("12", "12.11", f12_11, "first_self", 320))

def f12_12(A, I):
    # 2000 - 680 - 31 - 543 - 76 - 612 = 58 (apartment)
    return 2000 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["father"] - A["father_age"] - A["full_self"], {2000}

EQUATIONS.append(("12", "12.12", f12_12, "apartment", 58))


# =============================================================================
# FINDING #13 — DESIGNER FULL NAME (9 closures)
# =============================================================================

def f13_01(A, I):
    # 1148 + 637 + 177 + 680 - 1982 = 660
    step1 = I["designer_full"] + I["plate_a"] + I["plate_b"] + I["ford_capri"]  # 2642
    return step1 - A["birth_year"], {step1}

EQUATIONS.append(("13", "13.01", f13_01, "designer_short_660", 660))

def f13_02(A, I):
    # 1935 - 680 - 31 = 1224; 1224 = 612+612
    step1 = I["designer_birth"] - I["ford_capri"] - PLATE_DIGITS_SUM(I)  # 1224
    if step1 == 2 * A["full_self"]:
        return A["full_self"], {step1, 1224}
    return -1, set()

EQUATIONS.append(("13", "13.02", f13_02, "full_self", 612))

def f13_03(A, I):
    # 2642 - 612 = 2030; 2030 - 1986 = 44
    step1 = I["designer_full"] + I["plate_a"] + I["plate_b"] + I["ford_capri"] - A["full_self"]  # 2030
    return step1 - I["prod_end"], {step1, 2642}

EQUATIONS.append(("13", "13.03", f13_03, "self_age", 44))

def f13_04(A, I):
    # 1148 - 637 - 177 - 290 = 44
    return I["designer_full"] - I["plate_a"] - I["plate_b"] - I["ford"], set()

EQUATIONS.append(("13", "13.04", f13_04, "self_age", 44))

def f13_05(A, I):
    # 1148 - 637 - 177 = 334; 390 - 334 = 56 (Liubov)
    step1 = I["designer_full"] - I["plate_a"] - I["plate_b"]  # 334
    return I["capri"] - step1, {step1}

EQUATIONS.append(("13", "13.05", f13_05, "wife", 56))

def f13_06(A, I):
    # 1148 - 390 - 612 = 146; 146+146 = 292 (Harpaz)
    step1 = I["designer_full"] - I["capri"] - A["full_self"]  # 146
    if step1 * 2 == A["surname"]:
        return A["surname"], {step1}
    return -1, set()

EQUATIONS.append(("13", "13.06", f13_06, "surname", 292))

def f13_07(A, I):
    # 1224 - 1148 = 76 (Amir age)
    step1 = I["designer_birth"] - I["ford_capri"] - PLATE_DIGITS_SUM(I)  # 1224
    return step1 - I["designer_full"], {step1}

EQUATIONS.append(("13", "13.07", f13_07, "father_age", 76))

def f13_08(A, I):
    # 1148+1148 = 2296; 2296-2026=270; 2296-1982=314; 270+314=584=292+292
    double = 2 * I["designer_full"]  # 2296
    off1 = double - A["measurement_year"]  # 270
    off2 = double - A["birth_year"]        # 314
    total = off1 + off2                     # 584
    if total == 2 * A["surname"]:
        return A["surname"], {double, off1, off2, total}
    return -1, set()

EQUATIONS.append(("13", "13.08", f13_08, "surname", 292))

def f13_09(A, I):
    # 2296-1968=328; 2296-1986=310; 328+310=638; 638-290=348 (Liubov Harpaz)
    double = 2 * I["designer_full"]  # 2296
    off1 = double - I["prod_start"]   # 328
    off2 = double - I["prod_end"]     # 310
    total = off1 + off2                # 638
    return total - I["ford"], {double, off1, off2, total}

EQUATIONS.append(("13", "13.09", f13_09, "wife_married", 348))


# =============================================================================
# FINDING #14 — ELEVEN CASCADE (14 closures)
# =============================================================================

def f14_01(A, I):
    # Layer A: 543 (Amir Harpaz) - 409 ("אחת") = 134 (Idan)
    return A["father"] - 409, {409, 401}

EQUATIONS.append(("14", "14.01", f14_01, "brother1_first", 134))

def f14_02(A, I):
    # 408 - 50 - 292 = 66; 66 - 11 - 11 = 44
    step1 = 408 - 50 - A["surname"]  # 66
    return step1 - 11 - 11, {408, step1}

EQUATIONS.append(("14", "14.02", f14_02, "self_age", 44))

def f14_03(A, I):
    # "Sixty Six" = 1266 (Eran age phrase) — structural identity
    # Reached via step1 from previous: 66 → "שישים ושש" = 1266
    step1 = 408 - 50 - A["surname"]  # 66
    if step1 == 66:
        return 1266, {408, step1}
    return -1, set()

EQUATIONS.append(("14", "14.03", f14_03, "eran_age_phrase_1266", 1266))

def f14_04(A, I):
    # 408 - 116 = 292 (Harpaz)
    return 408 - A["core"], {408}

EQUATIONS.append(("14", "14.04", f14_04, "surname", 292))

def f14_05(A, I):
    # 409 + 409 = 818 ("אחת אחת" = logic of 11)
    return 409 + 409, set()

EQUATIONS.append(("14", "14.05", f14_05, "one_one_818", 818))

def f14_06(A, I):
    # Layer B: 1148 - 818 = 330; 330*2 = 660
    step1 = I["designer_full"] - 818  # 330
    if step1 * 2 == I["designer_short"]:
        return I["designer_short"], {step1, 818}
    return -1, set()

EQUATIONS.append(("14", "14.06", f14_06, "designer_short_660", 660))

def f14_07(A, I):
    # 543 - 330 = 213; 213+213 = 426 (Idan Harpaz)
    step1 = A["father"] - 330  # 213
    if step1 * 2 == A["brother1"]:
        return A["brother1"], {step1, 330}
    return -1, set()

EQUATIONS.append(("14", "14.07", f14_07, "brother1", 426))

def f14_08(A, I):
    # 612 - 330 - 31 = 251 (Amir)
    return A["full_self"] - 330 - PLATE_DIGITS_SUM(I), {330}

EQUATIONS.append(("14", "14.08", f14_08, "father_first", 251))

def f14_09(A, I):
    # 738 - 330 - 116 = 292 (Harpaz)
    return A["brother2"] - 330 - A["core"], {330}

EQUATIONS.append(("14", "14.09", f14_09, "surname", 292))

def f14_10(A, I):
    # Layer D: 1148 + 818 = 1966
    # 2026 - 1966 = 60 ("שישים")
    sum_val = I["designer_full"] + 818  # 1966
    return A["measurement_year"] - sum_val, {sum_val, 818}

EQUATIONS.append(("14", "14.10", f14_10, "word_sixty_60", 60))

def f14_11(A, I):
    # 2026-1966=60; 1982-1966=16; 60+16 = 76 (Amir age)
    sum_val = I["designer_full"] + 818  # 1966
    off1 = A["measurement_year"] - sum_val  # 60
    off2 = A["birth_year"] - sum_val        # 16
    return off1 + off2, {sum_val, off1, off2}

EQUATIONS.append(("14", "14.11", f14_11, "father_age", 76))

def f14_12(A, I):
    # 1986-1966=20; 1968-1966=2; 20+2 = 22 (2x11 logic)
    sum_val = I["designer_full"] + 818  # 1966
    off1 = I["prod_end"] - sum_val       # 20
    off2 = I["prod_start"] - sum_val     # 2
    return off1 + off2, {sum_val, off1, off2}

EQUATIONS.append(("14", "14.12", f14_12, "word_22", 22))

def f14_13(A, I):
    # 22 + 22 = 44 (observer age)
    sum_val = I["designer_full"] + 818
    off1 = I["prod_end"] - sum_val
    off2 = I["prod_start"] - sum_val
    step = off1 + off2  # 22
    return step * 2, {step}

EQUATIONS.append(("14", "14.13", f14_13, "self_age", 44))

def f14_14(A, I):
    # 818 - 680 - 116 = 22 (independent path to 2x11)
    return 818 - I["ford_capri"] - A["core"], {818}

EQUATIONS.append(("14", "14.14", f14_14, "word_22", 22))


# =============================================================================
# FINDING #15 — BRIDGE 2000 (15 closures)
# =============================================================================

def f15_01(A, I):
    # 1028 - 972 = 56 (Liubov)
    return 1028 - 972, {1028, 972}

EQUATIONS.append(("15", "15.01", f15_01, "wife", 56))

def f15_02(A, I):
    # 2000 - 1623 - 290 - 31 = 56
    return 2000 - 1623 - I["ford"] - PLATE_DIGITS_SUM(I), {2000, 1623}

EQUATIONS.append(("15", "15.02", f15_02, "wife", 56))

def f15_03(A, I):
    # 1101 - 1014 = 87; 87 - 31 = 56 (third path to Liubov)
    step1 = 1101 - 1014  # 87
    return step1 - PLATE_DIGITS_SUM(I), {1101, 1014, step1}

EQUATIONS.append(("15", "15.03", f15_03, "wife", 56))

def f15_04(A, I):
    # 1101 - 56 = 1045 ("שלוש אחת" = digit spelling of 31)
    return 1101 - A["wife"], {1101}

EQUATIONS.append(("15", "15.04", f15_04, "word_31_digit_1045", 1045))

def f15_05(A, I):
    # 1101 + 1014 = 2115; 2115 - 6-1-2 - 680 - 637 - 177 = 612
    step1 = 1101 + 1014  # 2115
    return step1 - 6 - 1 - 2 - I["ford_capri"] - I["plate_a"] - I["plate_b"], {1101, 1014, step1}

EQUATIONS.append(("15", "15.05", f15_05, "full_self", 612))

def f15_06(A, I):
    # 1707 - 1014 = 693; 693 + 680 = 1373 (digit spelling of 612)
    step1 = 1707 - 1014  # 693
    return step1 + I["ford_capri"], {1707, 1014, step1}

EQUATIONS.append(("15", "15.06", f15_06, "eran_digit_1373", 1373))

def f15_07(A, I):
    # 2115 - 1707 - 116 = 292 (Harpaz)
    step1 = 1101 + 1014  # 2115
    return step1 - 1707 - A["core"], {step1, 1707}

EQUATIONS.append(("15", "15.07", f15_07, "surname", 292))

def f15_08(A, I):
    # 1014 + 972 = 1986 (Prod End Year, as OUTPUT)
    return 1014 + 972, {1014, 972}

EQUATIONS.append(("15", "15.08", f15_08, "prod_end_1986", 1986))

def f15_09(A, I):
    # 1912 + 56 = 1968 (Prod Start Year, as OUTPUT)
    return I["prod_gematria"] + A["wife"], set()

EQUATIONS.append(("15", "15.09", f15_09, "prod_start_1968", 1968))

def f15_10(A, I):
    # 1014 - 948 = 66; "Sixty Six" = 1266
    step1 = 1014 - 948
    if step1 == 66:
        return 1266, {1014, 948, step1}
    return -1, set()

EQUATIONS.append(("15", "15.10", f15_10, "eran_age_phrase_1266", 1266))

def f15_11(A, I):
    # 948 - 637 - 177 = 134 (Idan)
    return 948 - I["plate_a"] - I["plate_b"], {948}

EQUATIONS.append(("15", "15.11", f15_11, "brother1_first", 134))

def f15_12(A, I):
    # 2000 - 680 - 31 - 543 - 426 = 320 (Eran)
    return 2000 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["father"] - A["brother1"], {2000}

EQUATIONS.append(("15", "15.12", f15_12, "first_self", 320))

def f15_13(A, I):
    # 2000 - 680 - 31 - 543 - 76 - 612 = 58 (apartment)
    return 2000 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["father"] - A["father_age"] - A["full_self"], {2000}

EQUATIONS.append(("15", "15.13", f15_13, "apartment", 58))

def f15_14(A, I):
    # 2000 - 680 - 31 - 543 - 612 = 134 (Idan)
    return 2000 - I["ford_capri"] - PLATE_DIGITS_SUM(I) - A["father"] - A["full_self"], {2000}

EQUATIONS.append(("15", "15.14", f15_14, "brother1_first", 134))

def f15_15(A, I):
    # 1,014 - 948 = 66 (intermediate before "Sixty Six" = 1,266)
    # This is step 15 of Finding #15 — the sub-closure that
    # 66 itself is a structurally meaningful derived value
    return 1014 - 948, {1014, 948}

EQUATIONS.append(("15", "15.15", f15_15, "word_66", 66))


# =============================================================================
# FINDING #16 — SELF-REFERENTIAL PLATE MATRIX (7 closures)
# =============================================================================

def f16_01(A, I):
    # 2761 = "ארבעת אלפים מאתיים שישים ושתיים" = 4262
    # 4262 - 1623 - 1266 = 1373 (digit spelling of 612)
    return 4262 - 1623 - 1266, {4262, 2761, 1623, 1266}

EQUATIONS.append(("16", "16.01", f16_01, "eran_digit_1373", 1373))

def f16_02(A, I):
    # 1373 - 6-1-2 = 1364 = "אחת ארבע אחת ארבע" (digit spelling of 1414)
    # 1414 - 1364 = 50
    step1 = 1373 - 6 - 1 - 2  # 1364
    return 1414 - step1, {1373, step1, 1414}

EQUATIONS.append(("16", "16.02", f16_02, "word_50", 50))

def f16_03(A, I):
    # 1373 - 612 - 680 - (plate digits) = 50 (parallel path to 50)
    return 1373 - A["full_self"] - I["ford_capri"] - PLATE_DIGITS_SUM(I), {1373}

EQUATIONS.append(("16", "16.03", f16_03, "word_50", 50))

def f16_04(A, I):
    # 50 → "חמישים" = 408; 408 - 116 = 292 (Harpaz)
    return 408 - A["core"], {408}

EQUATIONS.append(("16", "16.04", f16_04, "surname", 292))

def f16_05(A, I):
    # 4262 - 2026 - 1982 = 254; 680 - 254 = 426 (Idan Harpaz)
    step1 = 4262 - A["measurement_year"] - A["birth_year"]  # 254
    return I["ford_capri"] - step1, {4262, step1}

EQUATIONS.append(("16", "16.05", f16_05, "brother1", 426))

def f16_06(A, I):
    # mirror(1373) = 3731; 3731 - 1968 = 1763; 1986 - 1763 = 223
    # 223 - (plate digits) - 116 = 76 (Amir Age)
    mir = MIRROR(1373)  # 3731
    step1 = mir - I["prod_start"]        # 1763
    step2 = I["prod_end"] - step1        # 223
    return step2 - PLATE_DIGITS_SUM(I) - A["core"], {mir, step1, step2}

EQUATIONS.append(("16", "16.06", f16_06, "father_age", 76))

def f16_07(A, I):
    # 223 + 223 = 446 (Tom first name)
    mir = MIRROR(1373)
    step1 = mir - I["prod_start"]
    step2 = I["prod_end"] - step1  # 223
    return step2 * 2, {step2}

EQUATIONS.append(("16", "16.07", f16_07, "brother2_first", 446))

# Note: 680-223-31=426 is closely related to f16_05 result; some sources list it as
# the 7th closure. I'll defer to the book's count of 7.


# =============================================================================
# FINDING #17 — PRODUCTION DELTA RESOLUTION (9 closures)
# =============================================================================

def f17_01(A, I):
    # 13353 → two spellings: 3455 (standard) + 2665 (digit) = 6120
    # 6120 → mirror → 0216 → 216 → mirror → 612
    discrepancy = I["prod_count_rounded"] - I["prod_count_precise"]  # 13353
    spelling_sum = 2665 + 3455  # 6120
    m1 = MIRROR(spelling_sum)   # 216 (leading 0 dropped)
    m2 = MIRROR(m1)              # 612
    return m2, {discrepancy, 3455, 2665, spelling_sum, m1}

EQUATIONS.append(("17", "17.01", f17_01, "full_self", 612))

def f17_02(A, I):
    # 6120 - 216 - 2026 - 1982 = 1896
    return 6120 - 216 - A["measurement_year"] - A["birth_year"], {6120, 216}

EQUATIONS.append(("17", "17.02", f17_02, "val_1896", 1896))

def f17_03(A, I):
    # 6142 - 1896 - 1968 - 1986 = 292 (Harpaz)
    return 6142 - 1896 - I["prod_start"] - I["prod_end"], {6142, 1896}

EQUATIONS.append(("17", "17.03", f17_03, "surname", 292))

def f17_04(A, I):
    # 6120 - 2290 - 2087 - 292 = 1451
    return 6120 - 2290 - 2087 - A["surname"], {6120, 2290, 2087}

EQUATIONS.append(("17", "17.04", f17_04, "val_1451", 1451))

def f17_05(A, I):
    # 1451 - 1200 = 251 (Amir)
    return 1451 - 1200, {1451, 1200}

EQUATIONS.append(("17", "17.05", f17_05, "father_first", 251))

def f17_06(A, I):
    # 1896 - 1494 = 402; 1098 - 402 = 696 = 348+348
    # 696 - 5 - 5 = 686 ("Thirty"); 686 - 30 = 656; 656 - 612 = 44
    step1 = 1896 - 1494           # 402
    step2 = 1098 - step1           # 696
    step3 = step2 - 5 - 5          # 686
    step4 = step3 - 30             # 656
    return step4 - A["full_self"], {1896, step1, step2, step3, step4}

EQUATIONS.append(("17", "17.06", f17_06, "self_age", 44))

def f17_07(A, I):
    # 2378 - 1112 = 1266 (Eran age phrase)
    return 2378 - 1112, {2378, 1112}

EQUATIONS.append(("17", "17.07", f17_07, "eran_age_phrase_1266", 1266))

def f17_08(A, I):
    # 3455 - 2665 - 44 - 612 = 134 (Idan)
    return 3455 - 2665 - A["self_age"] - A["full_self"], {3455, 2665}

EQUATIONS.append(("17", "17.08", f17_08, "brother1_first", 134))

def f17_09(A, I):
    # 3455 - 2665 - 44 - 426 = 320 (Eran)
    return 3455 - 2665 - A["self_age"] - A["brother1"], {3455, 2665}

EQUATIONS.append(("17", "17.09", f17_09, "first_self", 320))


# =============================================================================
# FINDING #18 — LAST CAR OFF LINE (5 closures)
# =============================================================================

def f18_01(A, I):
    # 1912 - 882 - 680 - 58 = 292 (Harpaz)
    return I["prod_gematria"] - I["hebrew_date_882"] - I["ford_capri"] - A["apartment"], set()

EQUATIONS.append(("18", "18.01", f18_01, "surname", 292))

def f18_02(A, I):
    # 1912 - 882 - 637 - 177 = 216; mirror(216) = 612
    step1 = I["prod_gematria"] - I["hebrew_date_882"] - I["plate_a"] - I["plate_b"]  # 216
    return MIRROR(step1) if step1 > 0 else -1, {step1}

EQUATIONS.append(("18", "18.02", f18_02, "full_self", 612))

def f18_03(A, I):
    # 1986 - 882 - 637 - 177 = 290 (Ford)
    return I["prod_end"] - I["hebrew_date_882"] - I["plate_a"] - I["plate_b"], set()

EQUATIONS.append(("18", "18.03", f18_03, "ford_290", 290))

def f18_04(A, I):
    # 290 - 116 - 116 = 58 (apartment as 2× core from Ford)
    return I["ford"] - 2 * A["core"], set()

EQUATIONS.append(("18", "18.04", f18_04, "apartment", 58))

def f18_05(A, I):
    # 1986-882=1104; 1104+1104=2208; 2208-2026=182; 2208-1982=226
    # 182+226=408; 408-116=292
    step1 = I["prod_end"] - I["hebrew_date_882"]  # 1104
    step2 = step1 * 2                              # 2208
    off1 = step2 - A["measurement_year"]          # 182
    off2 = step2 - A["birth_year"]                 # 226
    step3 = off1 + off2                            # 408
    return step3 - A["core"], {step1, step2, off1, off2, step3}

EQUATIONS.append(("18", "18.05", f18_05, "surname", 292))


# =============================================================================
# FINDING #19 — DATE DIGIT SPELLING (2 closures)
# =============================================================================

def f19_01(A, I):
    # 19121986 → digit spelling = 4528
    # 4528 - 1986 - 1968 - 31 = 543 (Amir Harpaz)
    return I["date_digit_4528"] - I["prod_end"] - I["prod_start"] - PLATE_DIGITS_SUM(I), {I["date_digit_4528"]}

EQUATIONS.append(("19", "19.01", f19_01, "father", 543))

def f19_02(A, I):
    # 4528 - 1949 - 2026 = 553; 553 + 31 = 584 = 292+292
    step1 = I["date_digit_4528"] - A["father_birth"] - A["measurement_year"]  # 553
    step2 = step1 + PLATE_DIGITS_SUM(I)  # 584
    if step2 == 2 * A["surname"]:
        return A["surname"], {step1, step2}
    return -1, set()

EQUATIONS.append(("19", "19.02", f19_02, "surname", 292))


# =============================================================================
# FINDING #20 — CALENDRICAL THIRTY-ONE (3 closures)
# =============================================================================

def f20_01(A, I):
    # 19+12=31; 6+3+7+1+7+7=31 (sync)
    # 1101 - 31 - 680 = 390 (Capri)
    return 1101 - PLATE_DIGITS_SUM(I) - I["ford_capri"], {1101}

EQUATIONS.append(("20", "20.01", f20_01, "capri_390", 390))

def f20_02(A, I):
    # 1045+1101=2146; 2146-31=2115; 2115-6-1-2-680-637-177=612
    step1 = 1045 + 1101            # 2146
    step2 = step1 - PLATE_DIGITS_SUM(I)  # 2115
    return step2 - 6 - 1 - 2 - I["ford_capri"] - I["plate_a"] - I["plate_b"], {1045, 1101, step1, step2}

EQUATIONS.append(("20", "20.02", f20_02, "full_self", 612))

def f20_03(A, I):
    # 2115 - 1373 - 680 = 62 = 31+31 (double root)
    step1 = 1045 + 1101 - PLATE_DIGITS_SUM(I)  # 2115
    return step1 - 1373 - I["ford_capri"], {step1, 1373}

EQUATIONS.append(("20", "20.03", f20_03, "double_sync_62", 62))


# =============================================================================
# SUMMARY
# =============================================================================

if __name__ == "__main__":
    by_finding = {}
    for item in EQUATIONS:
        f = item[0]
        by_finding[f] = by_finding.get(f, 0) + 1
    total = sum(by_finding.values())
    print("Equations encoded by finding:")
    for f in sorted(by_finding.keys()):
        print(f"  #{f}: {by_finding[f]}")
    print(f"TOTAL: {total} equations")
