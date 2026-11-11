# Platinum Drivers

Platinum is a performance-focused Android/Bionic Mesa Turnip build for Qualcomm Adreno GPUs.

## Platinum v4.0 — controlled performance candidate

- **Platinum-A7xx** — standard A7xx build for Adreno 7xx devices.
- **Platinum-A7xx-OneUI** — separate compatibility package for Adreno 740 devices whose system driver enables the TP UBWC hint.

### Why v4 is based on v1

The v2/v3 ThinLTO profile performed worse than v1 in the user's reported workload. V4 therefore starts from the v1 source/build configuration rather than stacking more aggressive compiler and linker changes.

### What changed in v4

- Keeps v1's Mesa release profile: `-Doptimization=3`, `-Db_ndebug=true`, and LTO disabled.
- Adds only `-fno-plt` to C and C++ compilation as an isolated experiment.
- Does not use ThinLTO, `--lto-O3`, section garbage collection, or identical-code folding.
- CI checks that `-fno-plt` is present in generated Ninja commands and that no LTO flags are present.
- Uses the same Mesa source commit as v1/v2/v3 (`e4415d24616afbeee528a050b6d70f036057408c`) to isolate the one build-flag change.
- Does not change Adreno GPU register values, clocks, voltage, fan controls, GMEM/sysmem policy, or thermal limits.

**Important:** V4 is a test candidate, not a guaranteed faster driver. It is designed to avoid the v2/v3 ThinLTO change that regressed the user's workload, while testing one separate code-generation option. Whether `-fno-plt` improves FPS depends on the workload and must be measured on the target device. V1 remains the known-good fallback.

## Previous versions

- **v1.0:** Mesa release optimisation level 3 and NDEBUG; no ThinLTO.
- **v2.0:** added Clang O3, `-fno-plt`, and ThinLTO.
- **v3.0:** raised ThinLTO back-end optimisation and added section GC and safe ICF.

## Adreno 740 compatibility note

The standard package leaves `enable_tp_ubwc_flag_hint` disabled. This flag must match the system graphics driver; enabling it on devices whose system driver leaves it off can cause corrupted scaling. Use the OneUI package only if the device's system UI glitches with the standard driver and the system driver is known to set this hint.

## Testing

1. Keep v1 available as the fallback.
2. Import v4 into DriverLab and compare it with v1 using identical Vulkan test scenes.
3. Run the same games, scene, resolution, frame cap and settings.
4. Compare average FPS, 1% lows, frame times and crashes.
5. Repeat sustained tests after temperatures stabilise, recording device temperature and power draw if available.

DriverLab: https://github.com/The412Banner/DriverLab

Public comparison reports: https://fauxvkdb.canonspike.com/

FauxVkDB is a results database, not a hosted service that can load and test a private driver ZIP. DriverLab performs the tests locally on the target Android device.

## Build

The `platinum-v4` workflow builds both A7xx variants against the pinned v1 Mesa commit. It verifies the isolated `-fno-plt` flag, checks that no LTO flag is present, validates each ZIP and metadata, and publishes a prerelease only after both builds pass.
