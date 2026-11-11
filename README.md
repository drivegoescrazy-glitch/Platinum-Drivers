# Platinum Drivers

Platinum v1 is a conservative performance-focused A7xx Android/Bionic Turnip build based on the repository's v39 source tag.

## v1.0 packages

- **Platinum-A7xx** — standard A7xx build.
- **Platinum-A7xx-OneUI** — A7xx build with the inherited OneUI 8g2 UI glitch fix.

These builds target Adreno 7xx devices. The A8xx packages are intentionally not included in v1.0: the inherited A8xx patch sets did not apply cleanly to the newer Mesa revision in earlier CI attempts, and they need a separate rebase and validation pass.

## What changed for Platinum v1

- LLVM ThinLTO is enabled to optimise CPU-side driver code across translation units.
- Mesa release optimisation level 3 and NDEBUG are selected explicitly.
- Existing v39 GPU, shader, GMEM and UBWC behaviour is retained rather than changing unverified hardware cache values.
- No forced sysmem mode, GPU clock changes, thermal-throttle overrides or speculative shader patches are included.

ThinLTO may reduce CPU-side driver overhead, but performance and temperature changes depend on the device, game and workload. No FPS or temperature improvement is claimed until measured on hardware.

## Testing

1. Validate the ZIP structure (done by CI).
2. Import the ZIP into **DriverLab** on the Android device.
3. Run Vulkan CTS quick checks, rendering basics and repeated runs.
4. Compare the stock driver and Platinum v1 with the same DriverLab speed-test scenes.
5. Check actual games for visual errors, crashes and frame-time consistency.
6. Repeat a sustained workload while recording device temperature and performance over time.

DriverLab: https://github.com/The412Banner/DriverLab

Public comparison reports: https://fauxvkdb.canonspike.com/

FauxVkDB is a results database, not a hosted service that can load and test a private driver ZIP. DriverLab performs the actual tests locally on the target Android device.

## Build

The `platinum-v1` GitHub Actions workflow resolves one Mesa commit and builds both A7xx packages against that same revision. It publishes a GitHub prerelease only after both ZIPs build and pass archive checks.
