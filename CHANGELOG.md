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


# Platinum Drivers v4.0 — Changelog

## Baseline
- Built from the v1 branch and retains its v39-derived A7xx configuration and D32S8 workaround revert.
- Uses the same pinned Mesa source commit as v1/v2/v3 (`e4415d24616afbeee528a050b6d70f036057408c`).

## Build-profile changes
- Retains the v1 Mesa release profile: `-Doptimization=3`, `-Db_ndebug=true`, and `b_lto=false`.
- Adds only `-fno-plt` to C and C++ compile flags.
- Deliberately removes the v2/v3 ThinLTO, LTO O3, section-GC and ICF changes after the user reported worse performance with v2.
- CI verifies `-fno-plt` is present in Ninja's generated commands and checks that `-flto` does not appear.

## Hardware and thermal policy
- No GPU register, clock, voltage, governor, fan, GMEM/sysmem, cache-size, UBWC or thermal-throttle changes.
- V4 is an isolated code-generation experiment. `-fno-plt` is not guaranteed to improve every AArch64 workload.

## Validation status
- CI must build both standard and OneUI packages, check the compiler flags, and validate the ZIP and metadata.
- FPS, 1% lows, frame times, visual correctness and sustained temperatures require comparison on a physical Adreno 740 device.
- V1 remains the known-good fallback until v4 demonstrates a repeatable improvement in the same workload.


# Platinum Drivers v5.0 — Changelog

## Mesa base
- Updated from the v1–v4 pinned Mesa revision to upstream Mesa commit `20a455bed795148c07a3adc3eed1e84c5ed4a785` (Mesa 27.0.0 development line).
- Both standard and OneUI packages use the same pinned commit for reproducibility.
- Removed the historical v1-era D32S8 workaround revert and A7xx gen1 preamble override; use current upstream A7xx descriptors.

## Features brought forward from other driver projects
- Added upstream KGSL zero-timeout polling and syncobj-merge assertions from Banners-Turnip's A7xx common build checks. CI fails if either upstream fix is absent.
- Added the Banners-Turnip A7xx per-game SSBO-emulation entries for MIO and UNCHARTED: Legacy of Thieves Collection. These are application-specific compatibility settings rather than global driver changes.
- Adopted the WinNative balanced GMEM-autotuner adjustment: estimated GMEM bandwidth multiplier changes from 11/10 to 10/10. The script requires the exact expected upstream source expression and fails on unknown drift.
- Adopted the idempotent Adreno 740 OneUI UBWC-hint script for the OneUI package.

## Power / thermal decisions
- Retains standard KGSL dynamic power management.
- Does not force `KGSL_PROP_PWR_CONSTRAINT = PWR_MAX`, disable the KGSL governor, alter clocks or voltage, or force GMEM/SYSMEM.
- Does not use ThinLTO, `-fno-plt`, LTO-O3, section GC, or ICF.
- No speculative Adreno register, cache-size, UBWC, shader, GMEM, thermal or fan modifications.

## Validation
- CI validates the Mesa SHA, both upstream KGSL fixes, the V5 autotuner expression, no-LTO build commands, both package archives and metadata.
- FPS, 1% lows, frame-time variance, visual correctness, sustained temperature and battery use remain physical-device measurements. CI success does not prove a performance or battery gain.
