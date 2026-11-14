# requirements — skills

Реестр коллекции в формате «как питоновский requirements»: кто, зачем и
не заменяет ли уже кого-то. Один блок — один скилл: `[Skill](откуда)` —
для чего и зачем — примечания о замещении.

## Ядро (всегда)

- [base](./base/SKILL.md) — базовые правила агента: делегирование,
  деструктив с подтверждением, целостность данных; управляет всеми
  задачами включая разговорные. Заменителей не имеет.
- [chords](./chords/SKILL.md) — шорткаты хозяина: фраза → скилл/действие
  («подумай», «что сделано?»). Заменяет собой «вспоминай мои привычки».

## Think-first (пакет thinking)

- [thinking](./thinking/SKILL.md) — диспетчер думалок; сам правил не
  несёт, грузит тройку ниже одной пачкой.
- [solution-search](./solution-search/SKILL.md) — метод поиска подхода:
  глаголы, лестница less-make, URL-доказательства, 2-3 кандидата.
- [spine](./spine/SKILL.md) — своя позиция в идеях: тейки каждый ход,
  вайлдшоты с ярлыками, без рефлексивного согласия и лести.
- [workplanx](./workplanx/SKILL.md) — папка топика
  (plan/search/decision/log/gate) + голос хозяина в логе (1.10.0).

## Код (пакет coding)

- [coding](./coding/SKILL.md) — coding dispatcher: docker, process-tiers,
  code-quality, testing, logging, external-integrations live inside the
  package; boundaries, proxy-egress, git-workflow moved out to top level
  as mandatory sibling dependencies (split 2026-11-14).
- [ponytail](../../.zcode/skills/ponytail/SKILL.md) — ленивый сеньор
- [frontend-design](../../.zcode/skills/frontend-design/SKILL.md) — вкус и общий вид при сборке/редизайне UI: токены, типографика, «не AI-штамп»; ставится как критик и как проводка для сборки. Из anthropics/skills (MIT), вендор в .zcode/skills.
  (vendored из DietrichGebert/ponytail, MIT): лестница минимального
  изменения, уровни lite/full/ultra. ЖИВЁТ ВО ВСТРОЕННЫХ
  (.zcode/skills), не в коллекции.

## Вынесены из coding (сплит 2026-11-14)

- [boundaries](./boundaries/SKILL.md) — secrets, credentials, logs,
  chat/transcript hygiene, browser data, out-of-project access; loads on
  ANY task that could touch sensitive data, not only code. Was
  coding/security; stays a mandatory coding dependency.
- [proxy-egress](./proxy-egress/SKILL.md) — outbound proxy wiring with no
  silent direct fallbacks: per-library behavior, fallback hunting, live
  verification. Was coding/proxy-egress; stays a mandatory coding
  dependency.
- [git-workflow](./git-workflow/SKILL.md) — version control for any project
  work (code, notes, brainstorms, reverse-engineering, montage, scripts),
  not only code. Was coding/git-workflow; stays a mandatory coding
  dependency.

## Процесс

- [fresh-eyes](./fresh-eyes/SKILL.md) — чистоглазая приёмка готового
  (quality/conformance) свежим агентом, который не видел, как писалось.
- [mission](./mission/SKILL.md) — большая цель → доска карточек,
  карточные сессии.
- [loop](./loop/SKILL.md) — гонять задачу итерациями до зелёного
  предиката.
- [researcher](./researcher/SKILL.md) — автономный ресёрч нового/ншого
  на тему.
- [watchdog](./watchdog/SKILL.md) — надзорный тик за процессом/сессией
  без вмешательства в его работу.
- [roi](./roi/SKILL.md) — value-scoring for produced findings: cold-model
  stock gate + six criteria (lens/staleness/actionability/cost/verifiability),
  verdict blocks. Replaces nothing; researcher finds — roi prices what was
  found.

## Встроенные, вне папки коллекции

- [reverse-engineer-anything](../../.zcode/skills/reverse-engineer-anything/SKILL.md) —
  REA: реверс бинарников/Electron/прошивок через REA MCP; грузится по
  явной задаче реверса. Заменителей в коллекции нет.
- [ponytail](../../.zcode/skills/ponytail/SKILL.md) — ленивый сеньор;
  зависимость coding (см. строку выше в «Код»).
- chords — [chords](./chords/SKILL.md) из коллекции; его таблица
  биндингов — references/bindings.md, обновляется по словам хозяина.

## Внешние, не в реестре

- skill-caffolder'ы ZCode (skill-creator, plugin-creator) — встроенные,
  живут в ZCode, не здесь.
