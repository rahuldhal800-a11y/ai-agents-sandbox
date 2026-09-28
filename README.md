# ai-agents-sandbox

A local experimental digital world for autonomous digital beings.

## Genesis world

The current browser world is intentionally **WebGL-free** for machines where Chrome/WebGL is unavailable. It uses the browser Canvas 2D API to software-render a perspective/isometric 3D-style environment from the live Python simulation.

It contains:
- terrain and water
- forest and trees
- roads
- homes/buildings
- a computer laboratory
- a visible Genesis being
- live Genesis position, energy and age
- autonomous simulation, memory and model-free learning
- browser text and voice interaction
- operator kill switch

No paid AI API or pretrained LLM is required for the Genesis core.

## Run

    git pull
    python -m pip install -e ".[dev]"
    pytest -q
    python -m digital_world.server

Open `http://localhost:8765`.

If Chrome has WebGL disabled, that is expected to be fine: the world renderer does not use WebGL or Three.js.

## Architecture

    GOAL -> PERCEIVE -> CHOOSE/ACTION -> OBSERVE RESULT -> SCORE -> REMEMBER -> LEARN -> REPEAT

The 3D presentation is a visualization of the simulation state; the simulation itself remains Python state and is not dependent on the renderer.