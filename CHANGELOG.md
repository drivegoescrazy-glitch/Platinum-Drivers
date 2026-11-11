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
