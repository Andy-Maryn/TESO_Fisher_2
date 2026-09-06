# Minimap calibration

This is intentionally separate from the navigation implementation.

Run:

```text
python calibrate_minimap.py "Fri Sep  4 21_40_27 2026 298515 221476 10289 19 270 269.jpeg"
```

The tool crops the current 1920x1080 minimap at `(1640, 0, 1920, 280)`.

Keys:

- `R` — road
- `W` — water
- `S` — save JSON
- `Q` / `Esc` — exit

Tune the sliders until the magenta mask covers the intended class and
does not cover terrain/icons. The saved JSON is calibration data only; it
does not modify the project.
