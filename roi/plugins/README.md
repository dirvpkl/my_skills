# plugins — roi

`manifest.json` answers two separate questions and they must not merge:

- `modules` — what is inside this skill (references/, scripts/ are not
  registered; only loadable reference modules are).
- `dependencies` — which other skills of the collection load alongside
  this one (`base`, `workplanx`).

`planned` holds reserved, not-built pieces — currently the stock-library
wild-shot. Validate after any edit:

```
python -I <catalog>\workplanx\scripts\validate_manifest.py <skill-dir>
```
