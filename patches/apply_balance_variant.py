#!/usr/bin/env python3
"""Apply WinNative's conservative balanced GMEM-autotuner adjustment.

This intentionally does not force GPU clocks, GMEM, or SYSMEM. It changes
only the heuristic's GMEM cost estimate. The exact anchor is required so an
upstream refactor cannot silently produce a nominal V5 build without the tweak.
"""
from pathlib import Path

path = Path("src/freedreno/vulkan/tu_autotune.cc")
source = path.read_text()
old = "gmem_bandwidth = (gmem_bandwidth * 11 + total_draw_call_bandwidth) / 10;"
new = "gmem_bandwidth = (gmem_bandwidth * 10 + total_draw_call_bandwidth) / 10;"

if source.count(old) == 1:
    source = source.replace(old, new, 1)
    path.write_text(source)
    print("V5 balanced autotuner: GMEM estimate multiplier 11 -> 10")
elif source.count(new) == 1:
    print("V5 balanced autotuner: multiplier 10 already applied")
else:
    raise SystemExit(
        "V5 balanced autotuner: expected exactly one upstream 11/10 GMEM "
        "bandwidth expression (or the already-patched 10/10 expression); "
        "refusing to build with an unknown autotuner implementation"
    )

check = path.read_text()
if check.count(new) != 1 or old in check:
    raise SystemExit("V5 balanced autotuner verification failed")
print("V5 balanced autotuner: verified")
