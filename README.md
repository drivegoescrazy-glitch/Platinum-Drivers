# Platinum Drivers

Platinum is a performance-focused Android/Bionic Mesa Turnip build for Qualcomm Adreno GPUs.

## Current release: Platinum v3.0

- **Platinum-A7xx** — standard A7xx build; recommended for most Snapdragon 8 Gen 2 / Adreno 740 devices.
- **Platinum-A7xx-OneUI** — separate A7xx build for devices whose system graphics driver enables the Adreno 740 TP UBWC flag hint.

### What changed in v3.0

- Retains the v1/v2 v39-derived A7xx configuration and D32S8 workaround revert.
- Retains Clang `-O3 -fno-plt -flto=thin`.
- Raises the LLD ThinLTO backend optimisation level to `--lto-O3` (LLD's default is O2).
- Emits function/data sections and enables `--gc-sections` to discard unreachable sections.
- Enables LLD `--icf=safe` to fold eligible identical read-only/code sections without the more aggressive unsafe ICF mode.
- Adds CI checks to ensure every v3 linker/compiler flag is present in the generated Ninja commands.
- Uses the exact same Mesa source commit as v2.0 (`e4415d24616afbeee528a050b6d70f036057408c`) so the compiler/linker profile is the primary change in the A/B comparison.
- Does not change GPU clocks, voltage, fan controls, GMEM/sysmem policy, or device register values.

**Performance objective:** improve driver-side CPU overhead and reduce unused/duplicate code. The previous 5–10% FPS target with no measurable temperature increase remains an unverified goal, not a guarantee. GPU-bound workloads may see little or no FPS change.

## Previous releases

### Platinum v2.0
- Adds Clang `-O3 -fno-plt -flto=thin`.
- Uses the same v39-derived configuration and Mesa source commit.

### Platinum v1.0
- Uses Mesa release optimisation level 3 and NDEBUG without ThinLTO.

## Adreno 740 compatibility note

The standard package leaves `enable_tp_ubwc_flag_hint` disabled, matching the usual Adreno 740 system-driver configuration. This flag must match the system driver; enabling it on devices whose system driver leaves it off can cause corrupted scaling. Use the OneUI package only when the device's system UI glitches with the standard driver and its system driver is known to set this hint.

## Testing

1. Import the ZIP into **DriverLab** on the Android device.
2. Compare v2.0 and v3.0 with identical Vulkan benchmark scenes and settings.
3. Run identical game scenes and record average FPS, 1% lows and frame times.
4. Check rendering, visual glitches, crashes and Vulkan CTS quick tests.
5. Repeat a sustained workload while recording device temperature, power draw if available, and clock behaviour after temperatures stabilise.

DriverLab: https://github.com/The412Banner/DriverLab

Public comparison reports: https://fauxvkdb.canonspike.com/

FauxVkDB is a results database, not a hosted service that can load and test a private driver ZIP. DriverLab performs the actual tests locally on the target Android device.

## Build

The `platinum-v3` workflow builds both A7xx variants against the pinned v2.0 Mesa commit. It verifies ThinLTO, LTO O3, section garbage collection and safe ICF in the generated commands, validates both package archives and metadata, and publishes a prerelease only after both variants build successfully.
