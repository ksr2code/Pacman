# Project Management

This directory documents the management of the Pac-Man project, in line with
the requirements of Chapter VIII of the subject. The work was tracked
informally during development (git history + pair sessions) and formalized
here for the peer review.

## Methodology

- **Approach**: lightweight iterative/incremental (Agile-inspired), no formal
  framework. Two-person team, pair programming on hard problems, individual
  work on parallel features.
- **Cadence**: short sessions (1-3 days), each ending with a runnable build.
  Commits double as the progress log (see [timeline.md](timeline.md)).
- **Tracking**: git commits + branch state. No external Kanban board was
  used; this docs/ set is the retrospective record.
- **Quality gate**: `make lint` (flake8 + mypy) green before merge; manual
  playtest before each milestone.

## Documents

| Document | Purpose |
|----------|---------|
| [team.md](team.md) | Team organization, ownership, decision-making |
| [timeline.md](timeline.md) | Phase breakdown reconstructed from git history |
| [gantt.md](gantt.md) | Visual Gantt chart (Mermaid, rendered by GitHub) |
| [risks.md](risks.md) | Risk register with mitigations |
| [decisions.md](decisions.md) | Key technical decisions and their rationale |
| [acceptance-tests.md](acceptance-tests.md) | Feature acceptance test plan and results |
