# Minimap navigation (no ML)

This package implements the first navigation prototype without a neural network.

## Pipeline

1. Capture/crop the ESO minimap.
2. Detect large water regions using deterministic colour + morphology rules.
3. Detect road candidates using local brightness contrast.
4. Detect the player marker from the cyan minimap marker.
5. Build a walkable local cost map: water is forbidden, road is cheaper than terrain.
6. Run A* to the nearest visible water shore or to any requested minimap point.
7. Return a path and a relative minimap bearing for the next waypoint.

## Current assumptions

The supplied test screenshot is 1920x1080 and the minimap occupies approximately
`x=1640..1920`, `y=0..280`. Put these values into `MinimapConfig.region` when the
UI layout is different.

The current road detector is deliberately conservative about dependencies but is
still heuristic: ESO map decorations can look like roads. The road mask is used
as a *preference*, not as an obstacle map, so false positives do not make the
character walk through water.

## Manual test

```text
python tools/minimap/analyze_sample.py
```

The script prints detected player/water/road statistics and creates
`../minimap_navigation_debug.png` relative to the project directory.

The debug image uses:
- cyan circle: detected player
- magenta overlay: road candidates
- blue overlay: detected water
- green line: planned path to nearest water shore
- blue dot: selected shore target
