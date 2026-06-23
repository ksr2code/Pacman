# Gantt Chart

Rendered inline by GitHub. To export a PNG for slides, click the chart in
the GitHub UI → "Download PNG".

```mermaid
gantt
    title Pac-Man — Project Timeline (May 5 – Jun 23, 2026)
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d

    section Bootstrap
    Repo & uv environment      :done, p1a, 2026-05-05, 10d
    Project skeleton           :done, p1b, after p1a, 4d

    section Core Engine
    Maze integration           :done, p2a, 2026-05-15, 4d
    Player movement            :done, p2b, after p2a, 3d
    Ghost AI                   :done, p2c, after p2b, 4d
    Collision & scoring        :done, p2d, after p2c, 3d

    section Game Systems
    Pacgums & supers           :done, p3a, 2026-05-24, 3d
    Levels & highscore         :done, p3b, after p3a, 2d
    UI screens & HUD           :done, p3c, after p3b, 3d

    section WASM & Packaging
    pygbag async compat        :done, p4a, 2026-05-31, 2d
    itch.io deploy             :done, p4b, after p4a, 4d

    section Hardening
    Lint & config validation   :done, p5a, 2026-06-22, 2d
    PM documentation           :done, p5b, after p5a, 1d
```

Notes:
- Gaps in the calendar reflect parallel coursework, not blocked work.
- Phase boundaries align with milestone commits, not calendar weeks.
