# skills — my skills

Личная коллекция скиллов (одна папка = один скилл: SKILL.md +
plugins/manifest.json). Здесь же — **requirements.md**: реестр
зависимостей в формате питоновского requirements — кто, откуда, зачем и
не заменяет ли уже кого-то. Дополняй его при добавлении/сносе скиллов;
ридми — про устройство коллекции, requirements — про состав и связи.

## Папки

- `<skill>/SKILL.md` — сам скилл; `<skill>/plugins/manifest.json` —
  модули и зависимости; `<skill>/references/` — данные скилла
  (например, у chords таблица биндингов живёт в references/bindings.md).
- `runtime.toml` — настройки раннера коллекции.

## How skills teach

The collection teaches HOW to think, not rules. Rules govern actions only
(dangerous, destructive, outward-facing); thinking stays free — the more
initiative an agent writes, the more ideas exist, and ideas are the most
valuable output. When in doubt, a skill shows the flow and an example,
never a fence for thought. (Owner principle, 2026-11-14.)

## Встроенные, НЕ из коллекции

Часть скиллов живёт вне my_skills, во встроенных
(`C:\Users\orlando\.zcode\skills\`), и подключается зависимостями
пакетов. **Что там и зачем — смотри requirements.md** (раздел
«Встроенные, вне папки коллекции»): там pони и REA с причинами и
примечаниями о замещении, чтобы этот файл не растолстал.
