# Platinum Drivers v1.0 — Changelog

## Base
- Based on the repository's v39 source tag.
- Retains the v39 A7xx device configuration and D32S8 workaround revert.
- The OneUI package retains the existing 8g2 UI glitch patch.

## Build and optimisation changes
- Set Mesa release optimisation level to 3 and NDEBUG explicitly.
- Kept LTO disabled: Mesa's build system explicitly rejects LTO unless an unsupported/broken-build override is enabled, so Platinum does not use that option.
- Explicitly set Mesa's release optimisation level to 3.
- Explicitly enabled NDEBUG for the release build.
- Both packages are built against one pinned Mesa commit per release for reproducibility.

## Stability decisions
- No unverified shader or GPU register changes.
- No forced sysmem/GMEM policy changes.
- No speculative cache-size or UBWC changes.
- No GPU clock, voltage, thermal governor or throttling overrides.

## Validation status
- CI checks both ZIP archives and their metadata.
- Vulkan CTS, visual regression, game compatibility, FPS and sustained-temperature testing still require runs on physical target devices. The selected release optimisation settings are not a guarantee of FPS or temperature improvement.


# Platinum Drivers v2.0 — Changelog

## Baseline
- Based on the same v39-derived A7xx configuration as Platinum v1.0.
- Uses the exact same Mesa source commit as v1.0 (`e4415d24616afbeee528a050b6d70f036057408c`) for a controlled A/B comparison.
- Keeps the standard Adreno 740 TP UBWC hint disabled; the separate OneUI build retains the conditional compatibility toggle.

## Build-performance changes
- Adds Clang `-O3` to C and C++ compilation.
- Adds Clang ThinLTO (`-flto=thin`) to C and C++ compilation and the link step.
- Adds `-fno-plt`, matching the separate A6xx/A7xx performance-build recipe used by Banners-Turnip.
- Leaves Meson's `b_lto` option disabled. ThinLTO is applied via compiler/linker flags, not Meson's rejected LTO option.
- The build script fails if Ninja's generated commands do not contain `-flto=thin`.

## Stability and thermal decisions
- No GPU clock, voltage, governor, fan or thermal-throttle changes.
- No forced GMEM/sysmem selection, cache-size guesses or global UBWC changes.
- No new speculative shader or register patches.
- ThinLTO is intended to reduce driver-side CPU overhead; it does not guarantee higher GPU throughput or unchanged temperature.

## Validation status
- CI must build both variants, verify ThinLTO in generated commands, and validate both package archives and metadata.
- FPS, 1% lows, frame times, rendering correctness and sustained temperatures still require testing on physical Adreno 740 hardware.
- The 5–10% FPS / no-extra-heat goal is unverified until those tests are completed.
