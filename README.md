# Platinum Drivers

Platinum is a performance-focused Android/Bionic Mesa Turnip build for Qualcomm Adreno GPUs.

## Current release: Platinum v2.0

- **Platinum-A7xx** — standard A7xx build; the recommended package for most Snapdragon 8 Gen 2 / Adreno 740 devices.
- **Platinum-A7xx-OneUI** — separate A7xx build for devices whose system graphics driver enables the Adreno 740 TP UBWC flag hint (for example, certain newer Samsung One UI firmware builds).

### What changed in v2.0

- Retains the v1.0 v39-derived A7xx device configuration and D32S8 workaround revert.
- Adds Clang `-O3 -fno-plt -flto=thin` for C/C++ compilation and ThinLTO at link time.
- Keeps Meson's `b_lto` option disabled; ThinLTO is passed directly through compiler and linker flags.
- Uses the exact same Mesa source commit as v1.0 (`e4415d24616afbeee528a050b6d70f036057408c`) to isolate the build-profile change for fair A/B testing.
- Does not force GPU clocks, voltage, fan settings, GMEM/sysmem policy or additional UBWC flags.

**Performance target:** 5–10% higher FPS with no measurable temperature increase. This is a target only. No gain or thermal result is claimed until the same device, game, scene, resolution, frame cap and ambient conditions have been tested against v1.0.

### Adreno 740 compatibility note

The standard package leaves `enable_tp_ubwc_flag_hint` disabled, matching the usual Adreno 740 system-driver configuration. This flag must match the system driver; enabling it on devices whose system driver leaves it off can cause corrupted scaling. Use the OneUI package only when the device's system UI glitches with the standard driver and its system driver is known to set this hint.

## Previous release: Platinum v1.0

- **Platinum-A7xx** — standard A7xx build.
- **Platinum-A7xx-OneUI** — A7xx build with the OneUI 8g2 UI glitch fix.
- Used Mesa release optimisation level 3 and NDEBUG without ThinLTO.

## Testing

1. Import the ZIP into **DriverLab** on the Android device.
2. Compare v1.0 and v2.0 using the same Vulkan speed-test scenes.
3. Run the same real games with identical settings and record average FPS, 1% lows and frame times.
4. Check rendering, visual glitches, crashes and Vulkan CTS quick tests.
5. Repeat a sustained workload while recording device temperature, power draw if available, and clock behaviour. Compare after temperatures have stabilised.

DriverLab: https://github.com/The412Banner/DriverLab

Public comparison reports: https://fauxvkdb.canonspike.com/

FauxVkDB is a results database, not a hosted service that can load and test a private driver ZIP. DriverLab performs the actual tests locally on the target Android device.

## Build

The `platinum-v2` workflow builds both A7xx variants against the pinned v1.0 Mesa commit. It checks that the generated Ninja commands contain `-flto=thin`, validates the APK-driver ZIP contents and metadata, and publishes a prerelease only after both variants build successfully.
