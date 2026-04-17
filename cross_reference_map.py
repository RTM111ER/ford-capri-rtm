#!/usr/bin/env python3
"""
Systematic cross-reference mapping.

For each finding, extract:
1. All gematria anchors listed
2. All empirical constants listed
3. All intermediate values appearing in STEPS
4. Targets (closures)

Then map every value to every finding it appears in,
and mark its role (SOURCE / INTERMEDIATE / TARGET / ANCHOR).
"""

# Manually extracted from pdftotext output — every value in every finding

findings = {
    "#01": {
        "anchors": {680, 292},  # Ford Capri, Harpaz
        "empirical": {637177, 637, 177, 6, 3, 7, 1, 1949, 116, 31},  # 31=digit sum
        "intermediates": {3068, 1119, 439},
        "targets": {292},  # Harpaz
    },
    "#02": {
        "anchors": {680, 1494, 1098, 543, 1912},  # Ford Capri, Eleven Min fem, masc, Amir Harpaz, prod gematria
        "empirical": {637, 177, 11, 2026, 1900000},
        "intermediates": {1483, 409, 13, 575, 510},  # verification spellings
        "targets": {1494, 543, 1098},  # Eleven Min fem, Amir Harpaz, Eleven Min masc
    },
    "#03": {
        "anchors": {1494, 1098, 1093, 348, 401, 390, 680, 786, 729, 612, 1912},
        "empirical": {5, 8, 11, 31, 44, 57, 1982, 680, 390, 1912, 2026},
        "intermediates": {2191, 401, 279, 802, 786, 729, 685, 1370, 696, 686, 656},
        "targets": {5, 348, 1912, 401, 11, 786, 729, 5, 612, 44},  # multiple
    },
    "#04": {
        "anchors": {612, 1494, 1098, 1093, 348, 290, 680, 1028, 1912},
        "empirical": {1949, 637, 177, 6, 3, 7, 1, 31, 290, 738, 837, 1900000, 1912},
        "intermediates": {2592, 2587, 306, 1912, 738, 837},
        "targets": {348, 1028, 612, 612},
    },
    "#05": {
        "anchors": {680, 134, 320, 1930},
        "empirical": {637, 177, 116, 1494},
        "intermediates": {43, 1494, 1930},
        "targets": {134, 320},
    },
    "#06": {
        "anchors": {738, 612, 292, 290, 680, 1912, 1373, 1506, 2320, 686, 2650},
        "empirical": {1900000, 6, 3, 7, 1, 31, 6, 1, 2, 637, 177, 116, 1968, 1986},
        "intermediates": {1912, 2650, 2329, 2320, 1506, 457, 369, 686, 656, 352, 334},
        "targets": {290, 1373, 292, 738, 44},
    },
    "#07": {
        "anchors": {738, 680, 320, 1098, 612, 426, 543, 1912},
        "empirical": {58, 637, 177, 186},
        "intermediates": {418, 186, 369, 1098, 46, 446, 606},
        "targets": {58, 320, 738},
    },
    "#08": {
        "anchors": {612, 292, 680, 749, 815},
        "empirical": {1968, 1986, 8691, 6891, 637, 177, 58, 116, 2026},
        "intermediates": {306, 364, 728, 273, 96, 584},
        "targets": {612, 58, 612, 584},
    },
    "#09": {
        "anchors": {612, 251, 426, 680, 1451},
        "empirical": {637, 177, 1200, 1982, 2026},
        "intermediates": {991, 1451, 531, 575, 1106},
        "targets": {1982, 612, 251, 426},
    },
    "#10": {
        "anchors": {1215, 292, 680, 1926, 1541, 1494, 251},
        "empirical": {637, 177, 771, 736, 1215, 6, 3, 7, 1, 1949, 116, 2026},
        "intermediates": {1507, 1926, 1541, 2988},
        "targets": {292, 680, 292, 251},
    },
    "#11": {
        "anchors": {4343, 909, 612, 292, 680},
        "empirical": {1886647, 1968, 1986, 1982, 2026, 44, 43, 3434, 4, 3},
        "intermediates": {4343, 8686, 3434, 909, 2310, 284, 328, 273, 636},
        "targets": {44, 909, 292, 612},
    },
    "#12": {
        "anchors": {660, 1028, 972, 1707, 1623, 612, 1272, 1266, 543, 612, 426, 292, 134, 320, 680, 390},
        "empirical": {660, 76, 60, 680, 543, 612, 426, 390, 116, 1982, 2026, 6, 3, 7, 1, 31},
        "intermediates": {600, 1200, 1272, 1320, 2640, 658, 614, 796, 2000},
        "targets": {292, 76, 612, 1266, 680, 292, 134, 134, 320, 58},  # 12 closures
    },
    "#13": {
        "anchors": {1148, 660, 612, 292, 56, 348, 290, 680, 390},
        "empirical": {637, 177, 6, 3, 7, 1, 290, 680, 1935, 1982, 2026, 1968, 1986},
        "intermediates": {2642, 1224, 2030, 334, 146, 2296, 270, 314, 584, 328, 310, 638},
        "targets": {660, 1224, 44, 44, 56, 292, 76, 584, 348},  # 9
    },
    "#14": {
        "anchors": {401, 409, 408, 818, 1266, 1148, 660, 612, 292, 543, 251, 426, 134, 738, 680},
        "empirical": {11, 31, 50, 116, 1968, 1986, 1982, 2026, 76},
        "intermediates": {409, 408, 66, 818, 330, 213, 1966, 60, 16, 20, 2, 22},
        "targets": {409, 134, 408, 66, 44, 1266, 292, 818, 330, 660, 426, 251, 292, 1966, 76, 22, 44, 22},  # 14
    },
    "#15": {
        "anchors": {660, 1028, 972, 1623, 290, 1014, 1101, 1707, 1373, 948, 1266, 1912, 612, 680, 543, 426, 292, 320, 134, 56},
        "empirical": {660, 76, 31, 6, 1, 2, 637, 177, 116, 1968, 1986},
        "intermediates": {2000, 56, 1045, 87, 2115, 693, 1373, 1986, 1968, 66, 1266, 948},
        "targets": {56, 56, 1045, 56, 612, 1373, 292, 1986, 1968, 1266, 134, 320, 58, 134},  # 15
    },
    "#16": {
        "anchors": {2761, 4262, 1623, 1266, 1373, 1364, 1414, 408, 612, 680, 292, 426, 446},
        "empirical": {6, 3, 7, 1, 6, 1, 2, 116, 2026, 1982, 3731, 1968, 1986, 76},
        "intermediates": {2761, 4262, 1373, 1364, 50, 408, 254, 3731, 1763, 223},
        "targets": {1373, 50, 292, 426, 76, 446, 426},  # 7
    },
    "#17": {
        "anchors": {3455, 2665, 1896, 2290, 2087, 1451, 612, 1094, 1098, 696, 686, 1112, 2378, 948, 1266, 612, 292, 251, 426, 134, 320},
        "empirical": {1900000, 1886647, 13353, 216, 2026, 1982, 1968, 1986, 44, 56, 116, 637, 177},
        "intermediates": {13353, 6120, 216, 1896, 6142, 1451, 402, 696, 686, 656, 1112, 790, 1896},
        "targets": {612, 1896, 292, 1451, 612, 251, 1266, 44, 134, 320, 612},  # 9
    },
    "#18": {
        "anchors": {1912, 882, 292, 612, 680, 290, 408},
        "empirical": {19, 12, 1900000, 1986, 637, 177, 58, 116, 216, 1982, 2026},
        "intermediates": {1912, 882, 216, 1104, 2208, 182, 226, 408},
        "targets": {292, 216, 612, 290, 58, 292},  # 5
    },
    "#19": {
        "anchors": {4528, 543, 292},
        "empirical": {19121986, 1986, 1968, 31, 1949, 2026, 6, 3, 7, 1},
        "intermediates": {4528, 31, 553, 584},
        "targets": {543, 584},  # 2
    },
    "#20": {
        "anchors": {1101, 1045, 390, 612, 680, 1373},
        "empirical": {31, 637, 177, 6, 1, 2},
        "intermediates": {2146, 2115, 62},
        "targets": {390, 612, 62},  # 3
    },
}

# Now build reverse index: which findings is each value in?
from collections import defaultdict
value_to_findings = defaultdict(lambda: defaultdict(set))  # value -> {role -> {findings}}

for fname, data in findings.items():
    for role, values in data.items():
        for v in values:
            value_to_findings[v][role].add(fname)

# Find values appearing in 3+ findings (any role)
print("=" * 75)
print("VALUES APPEARING IN 3+ FINDINGS (SYSTEMATIC CROSS-REFERENCE MAP)")
print("=" * 75)

# Count unique findings per value
multi_findings = []
for val, roles in value_to_findings.items():
    all_findings = set()
    for role, fset in roles.items():
        all_findings.update(fset)
    if len(all_findings) >= 3:
        multi_findings.append((val, len(all_findings), all_findings, roles))

multi_findings.sort(key=lambda x: -x[1])

for val, count, all_f, roles in multi_findings:
    print(f"\n  VALUE {val}: appears in {count} findings: {sorted(all_f)}")
    for role, fset in sorted(roles.items()):
        print(f"    {role}: {sorted(fset)}")
