# Technical Decisions

Key engineering decisions and their rationale. Each entry follows the
format: **Context → Options → Choice → Why**.

---

## D1. Deployment target: WebAssembly via pygbag

**Context**: Subject (Chapter VII) requires packaging for a public platform
(Steam/Itch.io). Browser deployment gives the widest reach with zero
install for reviewers.

**Options**: (a) Desktop-only via PyInstaller; (b) WASM via pygbag to
itch.io.

**Choice**: WASM via pygbag → itch.io.

**Why**: No-install browser play; itch.io supports HTML uploads natively;
pygbag is the standard Python→WASM toolchain. Cost: must avoid blocking I/O
and use async main loop.

## D2. Game library: pygame-ce

**Context**: Need a 2D rendering + input + audio library compatible with
pygbag.

**Options**: (a) pygame; (b) pygame-ce (community edition); (c) arcade.

**Choice**: pygame-ce.

**Why**: Drop-in pygame API, actively maintained, well-supported by
pygbag, smaller WASM bundle than arcade.

## D3. Movement model: grid-based with pixel interpolation

**Context**: Pac-Man is fundamentally tile-based; free-form physics would
break ghost AI and collision.

**Options**: (a) Pure grid (teleport between cells); (b) free pixel
movement; (c) grid-locked with smooth interpolation.

**Choice**: Grid-locked with interpolation.

**Why**: Authentic feel of the original, simple collision (same-tile
matching), deterministic ghost pathfinding on the grid. `player.py` queues
the next direction and applies it at cell centers.

## D4. Ghost AI: Euclidean chase + BFS spawn-return

**Context**: Subject leaves chase behavior open; ghosts need distinct,
playable behavior.

**Options**: (a) Pure random; (b) A* to player; (c) greedy Euclidean in
chase, BFS only when returning home after being eaten.

**Choice**: Greedy Euclidean for chase/scatter, BFS for spawn mode.

**Why**: Euclidean is cheap and feels right (ghosts converge but can be
juked); BFS guarantees eaten ghosts find their way back to a corner.
No-U-turn rule at intersections preserves the classic feel.

## D5. Rendering: pre-rendered maze surface

**Context**: Redrawing ~500 wall tiles per frame at 60 FPS is wasteful.

**Options**: (a) Draw walls each frame; (b) cache the maze to a Surface
once per level.

**Choice**: Cache to Surface in `Maze._render_maze_to_surface`.

**Why**: One blit per frame instead of hundreds; maze is static for the
level lifetime.

## D6. RNG isolation: local `random.Random` instances

**Context**: Pacgum placement, ghost behavior, and fruit selection all need
randomness, but mixing them in the global RNG breaks determinism per seed.

**Options**: (a) Use the global `random` module; (b) local `random.Random`
instances per subsystem.

**Choice**: Local instances, seeded per level.

**Why**: Deterministic layouts per `cfg.seed` (reproducible defense
demos); ghosts and pacgums don't perturb each other's sequences.

## D7. Config schema: stdlib `dataclass` (not pydantic)

**Context**: Need typed config with defaults and validation.

**Options**: (a) pydantic; (b) stdlib `dataclass` + manual validation.

**Choice**: `dataclass` + custom `_sanitize()` pipeline.

**Why**: No extra dependency (smaller WASM bundle); full control over
clamping/type-checking/error messages; avoids pydantic's WASM startup cost.
Trade-off: more hand-written validation code.

## D8. Async main loop with `await asyncio.sleep(0)`

**Context**: pygbag requires cooperative yielding or the browser tab
freezes.

**Options**: (a) Synchronous `while True`; (b) async loop yielding each
frame.

**Choice**: `async def pacman(...)` with `await asyncio.sleep(0)` per frame.

**Why**: Mandatory for WASM; harmless on desktop (asyncio runs the same
game loop). See R1.

## D9. JSON-with-comments: line-based stripping

**Context**: Subject (§V.2) requires `#` comment support in JSON config.

**Options**: (a) A JSON5/comment-json library; (b) regex/line-strip before
`json.loads`.

**Choice**: Strip lines whose first non-whitespace char is `#` or `//`.

**Why**: Zero dependencies, sufficient for the documented config style.
Limitation: inline trailing comments are not supported (documented in
README).

## D10. Level count: fixed cap of 10 (not infinite)

**Context**: Subject (§VI.7) requires "at least 10" levels.

**Options**: (a) Infinite procedurally-generated levels; (b) fixed cap.

**Choice**: `NUM_LEVELS = 10` in `constants.py`, victory on completion.

**Why**: Bounded scope for a course project; finite win state is testable;
maze seed is `cfg.seed + level - 1` so extending is trivial if needed.
README previously claimed "infinite" — to be reconciled.
