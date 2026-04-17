#!/usr/bin/env python3
"""
Build the finding-to-finding connection graph.
Two findings share an edge if they share a DERIVED value
(not just input infrastructure).
"""

# Exclude pure input infrastructure
INFRASTRUCTURE = {680, 637, 177, 116, 2026, 1982, 1968, 1986, 31,
                   1, 2, 3, 6, 7, 290, 11, 8, 5, 50, 44, 58, 290, 76,
                   1900000, 1886647, 1935, 1949, 19121986, 19, 12}

# From previous map — rebuild with just meaningful shared values
# Format: finding -> set of meaningful values that appear there
from collections import defaultdict

meaningful_values = {
    "#01": {292, 3068},
    "#02": {1494, 1912, 1098, 543, 409, 575, 510, 1483},
    "#03": {1494, 1098, 1093, 348, 1912, 401, 786, 729, 612, 686, 656, 2191, 802},
    "#04": {1098, 1494, 1093, 348, 1028, 612, 1912, 738, 837, 2592, 2587, 306},
    "#05": {1494, 134, 320, 1930},
    "#06": {1912, 738, 2650, 2329, 2320, 1373, 292, 1506, 369, 686, 656, 612},
    "#07": {738, 1912, 418, 320, 186, 1098, 612, 426, 543, 369, 292, 58},
    "#08": {8691, 6891, 306, 612, 584, 292, 58, 749, 815, 364, 728, 96, 273},
    "#09": {991, 1451, 1200, 612, 251, 426, 1982, 1106, 531, 575},
    "#10": {771, 736, 1215, 292, 1926, 1541, 680, 1494, 2988, 251, 1507},
    "#11": {4343, 3434, 909, 292, 612, 8686, 2310, 284, 328},
    "#12": {660, 1028, 972, 1707, 1623, 1200, 612, 1272, 1266, 2640, 680,
            134, 2000, 320, 58, 292, 76},
    "#13": {1148, 2642, 660, 1224, 612, 56, 292, 76, 2296, 584, 348, 638, 44,
            270, 314, 328, 310, 146, 334},
    "#14": {401, 409, 408, 818, 1266, 1148, 330, 660, 426, 251, 292, 738,
            1966, 76, 22, 44, 66, 213, 134},
    "#15": {1028, 972, 2000, 56, 1623, 1101, 1014, 1045, 2115, 1707, 1373,
            612, 292, 1986, 1968, 1912, 948, 1266, 134, 320, 58, 693, 87, 66},
    "#16": {2761, 4262, 1623, 1266, 1373, 1364, 1414, 50, 408, 292, 254, 426,
            3731, 1763, 223, 446, 76, 612, 680},
    "#17": {13353, 3455, 2665, 6120, 216, 1896, 6142, 2290, 2087, 292, 1451,
            1200, 612, 251, 1494, 1098, 402, 696, 686, 656, 1112, 2378, 1266,
            790, 134, 320, 56, 948, 44, 612},
    "#18": {1912, 882, 216, 612, 292, 290, 58, 1104, 2208, 182, 226, 408},
    "#19": {4528, 543, 584, 292, 553},
    "#20": {1101, 1045, 2146, 2115, 390, 612, 1373, 62},
}

# Filter out pure infrastructure values from each set
clean = {}
for f, vals in meaningful_values.items():
    clean[f] = vals - INFRASTRUCTURE

# Build edges: shared values between pairs of findings
from itertools import combinations
edges = defaultdict(set)  # (f1, f2) -> set of shared values

for f1, f2 in combinations(sorted(clean.keys()), 2):
    shared = clean[f1] & clean[f2]
    if shared:
        edges[(f1, f2)] = shared

# Count connections per finding
connections = defaultdict(set)
for (f1, f2), shared in edges.items():
    connections[f1].add(f2)
    connections[f2].add(f1)

print("=" * 80)
print("FINDING-TO-FINDING CONNECTION GRAPH")
print("=" * 80)
print("Two findings connect if they share a DERIVED value (not input infrastructure)")
print()

print("─" * 80)
print("CONNECTION COUNT PER FINDING")
print("─" * 80)
ranked = sorted(connections.items(), key=lambda kv: -len(kv[1]))
for f, cons in ranked:
    print(f"  {f}: connected to {len(cons)} other findings  →  {sorted(cons)}")

print()
print("─" * 80)
print("STRONGEST PAIRWISE CONNECTIONS (sharing 3+ values)")
print("─" * 80)
strong = sorted(edges.items(), key=lambda kv: -len(kv[1]))
for (f1, f2), shared in strong:
    if len(shared) >= 3:
        print(f"\n  {f1} ↔ {f2} share {len(shared)} values:")
        print(f"    {sorted(shared)}")

print()
print("─" * 80)
print("NETWORK STATISTICS")
print("─" * 80)
total_edges = len(edges)
max_possible = 20 * 19 // 2  # 190
density = total_edges / max_possible
print(f"  Total edges: {total_edges} / {max_possible} possible")
print(f"  Network density: {density:.1%}")
avg_connections = sum(len(c) for c in connections.values()) / len(connections)
print(f"  Average connections per finding: {avg_connections:.1f}")

# Find isolated or near-isolated findings
print()
print("─" * 80)
print("LEAST CONNECTED FINDINGS")
print("─" * 80)
for f, cons in sorted(connections.items(), key=lambda kv: len(kv[1])):
    if len(cons) <= 5:
        print(f"  {f}: {len(cons)} connections → {sorted(cons)}")
