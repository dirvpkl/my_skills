# plugins — boundaries

`manifest.json` answers two separate questions and they must not merge:

- `modules` — what is inside this skill (the verbatim-preserved
  sensitive-data memo; SKILL.md's rules are the core, not registered).
- `dependencies` — which other skills of the collection load alongside
  this one (currently none: boundaries is a universal guard loaded BY
  others — coding declares it a mandatory sibling — it does not pull
  skills in itself).

`planned` is empty but the skill is expected to grow: future memo
extensions land as additional reference modules here instead of new
hand-written path references in SKILL.md. Validate after any edit:

```
python -I scripts/validate_manifest.py
```
