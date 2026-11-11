# Platinum Drivers

Platinum is an Android/Bionic Mesa Turnip Vulkan driver build for Qualcomm Adreno GPUs.

## Platinum v5.0 — A7xx balanced build

V5 is aimed at the AYN Thor Base (Snapdragon 8 Gen 2, Adreno 740). It combines a current upstream Mesa base with a conservative GMEM/SYSMEM autotuner adjustment. The goal is sustainable performance: smooth frame pacing and efficient memory traffic without forcing maximum GPU clocks.

### Packages

- **Platinum-A7xx** — standard Adreno 7xx package. Start with this.
- **Platinum-A7xx-OneUI** — same driver, with the Adreno 740 TP UBWC hint enabled. Use only on firmware whose system driver enables that hint and where the standard package causes UI flicker or scaling corruption.

## V5 changes

- **Current upstream Mesa:** pinned to `20a455bed795148c07a3adc3eed1e84c5ed4a785`, the Mesa revision used by Banners-Turnip v27.0.0-20261111-r3.
- **Upstream KGSL fixes:** build-time assertions confirm the zero-timeout timestamp poll and syncobj-merge fixes are present. These prevent known KGSL synchronisation problems; the zero-timeout fix is particularly relevant to Vulkan/DX12-on-KGSL workloads.
- **Balanced GMEM autotuner:** adopts WinNative's conservative adjustment to the estimated GMEM bandwidth multiplier (11/10 → 10/10). This affects the GMEM-versus-SYSMEM heuristic, not GPU clocks or voltage.
- **Per-game A7xx compatibility:** adds Turnip SSBO-emulation defaults only for MIO and UNCHARTED: Legacy of Thieves Collection, where large storage-buffer ranges can exceed A7xx's default limit.
- **Current A7xx device configuration:** removes the old v1-era D32S8 revert and gen1 preamble override rather than carrying those historical modifications onto current Mesa.
- **OneUI compatibility:** ports the idempotent Adreno 740 UBWC-hint script and limits it to the OneUI package.

## Power and performance policy

V5 intentionally uses normal KGSL power management. It does **not** force `PWR_MAX`, disable the GPU governor, change clocks or voltage, force GMEM/SYSMEM, enable ThinLTO, or change thermal limits.

Why not include the maximum-clock mode from some other driver builds? Those modes explicitly increase power draw and are a poor fit for a combined lower-heat / better-battery target. V5 instead keeps the GPU free to ramp as the workload requires, while making a modest adjustment to the rendering-mode estimate.

The autotuner change is a heuristic, not a hardware benchmark. It may improve bandwidth behaviour on some scenes and make no difference on others. It is not possible to guarantee higher FPS, lower temperatures, or longer battery runtime without testing on the actual Adreno 740 device.

## Testing

Compare V5 against V1 in the same games and scenes, with the same resolution, graphics settings, frame cap, battery level, and room temperature.

Record:
- Average FPS and 1% lows.
- Frame-time consistency / stutter count.
- Device temperature after the same sustained run.
- Battery percentage or power draw over the same time window.
- Visual glitches, crashes, and shader compilation behaviour.

Do not judge a driver from a brief cold start: repeat a longer run after temperatures stabilise. Keep V1 as the fallback until V5 shows a repeatable improvement.

### Useful project references

- [Mesa Turnip / Freedreno documentation](https://docs.mesa3d.org/drivers/freedreno.html)
- [Banners-Turnip — upstream Mesa builds and A7xx KGSL fixes](https://github.com/The412Banner/Banners-Turnip)
- [WinNative Drivers — balanced and performance variants](https://github.com/WinNative-Emu/Drivers)
- [DriverLab — local Android driver testing](https://github.com/The412Banner/DriverLab)
- [FauxVkDB — public Vulkan benchmark results](https://fauxvkdb.canonspike.com/)

FauxVkDB is a results database, not a hosted service for uploading and testing a private ZIP. DriverLab performs tests locally on the target Android device.

## Build and CI

The `platinum-v5` workflow builds standard and OneUI packages against the same pinned Mesa SHA. It validates the Mesa revision, balanced autotuner expression, KGSL fixes, absence of LTO flags, ZIP integrity, and metadata before publishing both assets.
