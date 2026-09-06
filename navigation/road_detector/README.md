# Standalone road detector

This is intentionally separate from the navigation project.

Pipeline:

1. HSV color filter creates road candidates.
2. Connected-component geometry removes small/square noise.
3. Conservative morphology reconnects nearby road pixels.
4. A ray scan estimates the strongest road direction from the player.

Debug image:

- red = raw color candidates
- green = surviving road mask
- white dot = player
- white arrow = strongest direction

The current HSV values are only initial calibration for the supplied minimap. If geometry filtering is still too
permissive, the next step should be continuity/curve detection rather than more HSV tweaking.
