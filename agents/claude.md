# Claude Agent — backend-architect-neural

> Packaging for Claude Code / Claude API. Canonical activation remains `SKILL.md`.

## Installation
```bash
# Claude Code: add as skill
cp -r backend-skill /path/to/claude/skills/backend-architect-neural
# or reference via SKILL.md path in your prompt
```

## Activation
```
Use the skill at: backend-skill/SKILL.md
Follow BRAIN.md pipeline → NEURAL_ROUTING.md → domain ROOT.md
```

## Included
All domains, engines, playbooks, checklists, and research registry. See `openai.yaml` for full file list.

## Integrity
```bash
python tools/validate_neurons.py --max-warnings 0
python tools/check_links.py --strict
python tools/freshness.py --days 400
```
