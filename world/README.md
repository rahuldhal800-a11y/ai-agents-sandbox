# Digital World

This package is the first world substrate for the AI Digital Being Research Laboratory.

It deliberately has no external API dependency. The world is a local deterministic
simulation containing:

- a procedural Earth-like grid
- terrain, elevation, temperature, water, and resources
- simulation time and deterministic ticks
- entities with energy, inventory, and memory
- observation and movement primitives

The next layers can add physiology, perception, learning, communication, culture,
economics, and evolving tool/capability systems without changing the world substrate.

Run the demo with:

```bash
python -m world.run
```
