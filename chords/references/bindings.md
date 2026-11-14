# bindings — the chord table

User-edited data. One row per binding; phrase matching is case-insensitive
substring. `target` kinds: `skill` (one sibling), `bundle` (several, loaded
together in the same turn), `action` (no skill loads; the described step runs).
An explicit /<skill-name> command (wherever the harness maps /name → skill)
always beats a chord on collision — record the canonical /command in the
row's note when one exists.
Add new rows at the bottom, newest last; never delete a row without the
user's word. After EVERY edit of this table, run
`python -I scripts/make_cheatsheet.py` — it renders the one-page card to the
Desktop (`chords-cheatsheet.md`); a stale card is a lie. What belongs here:
phrases the user actually types and their resolved targets. What does NOT
belong here: skill routing rules (those live in each skill's trigger),
session logs, one-off jokes the user did not confirm as bindings.

| phrase (RU / EN aliases) | target | kind | note |
|---|---|---|---|
| "побрейнштормим", "можешь поискать", "обсудим идею" | solution-search + workplanx + spine | bundle | pure think/brainstorm ask — the old thinking router's stack (thinking skill deleted 2026-11-14, owner: «хочу это как чорд»); idea-talk answers from spine alone, real pre-decision opens the workplanx topic + gate |
| "перепроверь себя", "перепроверь", "чекни потом", "double-check it" | fresh-eyes | skill | finished work only |
| "пока не зелёное", "until green", "крутись" | loop | skill | iterate until the condition holds |
| "разложи на карточки", "это большая цель" | mission | skill | multi-session decomposition |
| "покопай что нового", "find what's new" | researcher | skill | explicit research request only |
| "что сделано?", "отчитайся", "recap" | Recap the session in base's Report shape: what was done, what was refused/asked, next human action — no skill loads | action | the user asks this between work bursts |
| "гит ворктри", "worktree", "ворктри" | git-workflow | skill | version control for ANY project work (code, notes, brainstorms, RE, montage) — promoted top-level 2026-11-14; base keeps the repo pre-flight + worktree preference |
| "надо написать", "что-то написать", "напиши доку", "напиши мд", "write it up" | coding | skill | ANY writing task — even plain .md — routes to coding (owner rule 2026-11-12) |
| "чекни логи", "чекни прокси", "check logs", "что сломалось" | workplanx | skill | opens the project topic workflow; owner's phrase carries the intent, specifics always arrive in the NEXT message (pasted logs/links/new tasks) — mine those, don't invent a procedure |
| "редеплой", "redeploy" | workplanx | skill | same: phrase + follow-up bundle ("редеплой, можешь редеплоить. и вот проблемы...") — route into the topic workflow |
| "адаптируйся", "adapt", "расскажи че тут", "что за проект тут" | workplanx | skill | session-entry ritual: load the topic folder and report context; specifics come from the follow-up |
| "автономно", "автономно хуярить", "autonomous" | Work to the end with no intermediate questions, then one report with receipts — EXCEPT the deny classes, which always stop and ask: mass/public-facing/prod/destructive/unsafe/no-proxy/credentials. Fence = risk classes checked per action, never trusted to agent memory | action | owner-approved with mandatory fences 2026-11-14; class table from OWASP agentic + permission-mode practice, wording drafted in [[11-14-workplanx-gates-and-tags]] |
| "перескажи проект", "что я откладывал", "что мы обсуждали", "что мы делали", "напомни все", "напомни весь диалог", "перескажи мне", "перескажи с момента X", "recap" | recap | skill | read-only collector: rg hashtag pass over .workplanx + git log + memory index, fixed 11-section form; built 2026-11-14, verified |
| "пиши" | Proceed with the step just described — AUTONOMOUSLY: work it to the end with no intermediate questions, report with receipts; the deny classes still stop and ask (mass/public/prod/destructive/unsafe/no-proxy/credentials). No skill loads — pure protocol word | action | owner ruling 2026-11-14: «пиши — это автономность»; substring match also catches «напиши…» — the explicit writing-task row above wins there; do not treat bare «пиши» as a writing task |
| "думалка", "думалки", "подумай", "давай подумаем", "расскажи тут про что мы делали", "завершай думалкой", "утренний рекап", "что ночью было", "утренняя выжимка", "morning recap" | recap + solution-search + workplanx + spine + roi + busywork | bundle | the think-first mega-bundle (thinking router folded 2026-11-14): spine governs stance, solution-search drives method, workplanx owns the topic+gate — idea-talk = spine alone, real pre-decision = folder+gate before any build; roi prices the gems, busywork surfs for fresh finds; «завершай думалкой» = close the pass with this bundle; COLLISION NOTE: the full phrase «расскажи тут про что мы делали» routes HERE (recap+think stack), the bare «что мы делали» routes to the recap skill row; MORNING variant runs recap FIRST (owner merge 2026-11-14); phrases «вайлдшоты»→renamed 2026-11-14 (owner: «Не вайлдшоты») |
| "добить проект", "добить", "дожми" | workplanx + coding + loop | bundle | finish what's pending: topic folder state → code until green → loop on the verdict |
| "пореверсить", "пореверсим", "реверс" | reverse-engineer-anything | skill | REA pass on the target (owner: «есть настроение пореверсить») |
| "монтаж", "запускай монтаж" | davinci-editing | skill | DaVinci Resolve editing pass via davinci-resolve-mcp |
| "на сегодня", "закругляйся", "на сегодня всё" | workplanx (afterword) + fresh-eyes + recap | bundle | end-of-night close: afterword in the topic, fresh-eyes judging, morning extract ready (owner rhythm: works till ~04:00) |
| "что я забыла?", "что забыла", "покажи слоты" | action | rg `#slot` across all .workplanx topics + report every open slot — the anti-lost-idea ritual | |
| "какие скиллы?", "какие чорды?", "каталог скиллов" | action | list the collection folders + the bindings table, one line each | |
| "пихну другому агенту", "хендофф", "выгрузка для другого агента", "сводка для агента", "передай другому агенту", "запиши все-все-все" | handoff | skill | structured context file for a fresh agent |
| "цени находку", "roi находки", "это сток?", "сколько стоит эта находка", "roi этих находок", "любой бы это нашёл", "стоит ли это продавать" | roi | skill | cold-control stock gate + six-criteria scoring |
| "лбдн", "LBDN", "hustle", "бизиворк", "busywork", "когда делать нехуй", "пошурши" | Forced lazy-surf pass: free-roam READ-ONLY (no secrets) — internet wandering, reflection, router peers; what ggfr does = chain-walking. REAL wall-clock 10 min default, owner overrides verbally. Report findings only, or honest zero | action | = the ИБД/forced-serendipity behavior; design lives in [[11-12-forced-serendipity-skill]]; installed name = **busywork** (owner pick 2026-11-14); LBDN = Look Busy Do Nothing (owner) |
| "ресерчь", "ресерчь новые сайты", "поресерчить", "я хочу чтобы ты ресерчил", "поищи еще сервисов", "погугли про это", "поищи в интернете про это" | researcher | skill | relocated from skill descriptions 2026-11-14 (personal phrases live here, not in skill files) |
| "можешь коммитить", "коммитни", "пушни", "мердж" | git-workflow | skill | relocated 2026-11-14 |
| "вотчер", "нужен вотчер", "проверь вотчером" | watchdog | skill | relocated 2026-11-14 |
| "солюшнсерчер", "юзани на последок", "брейншторминг" | solution-search | skill | relocated 2026-11-14 |
| "оцени мои проектики", "как тебе идея", "накинь вайлдшотов", "постреляй вайлдшотами", "давай spine", "any wild shots" | spine | skill | relocated 2026-11-14 |
| "нужен ревью", "не забудь фреш айс", "ревью, что-то осталось?" | fresh-eyes | skill | relocated 2026-11-14 |
| "спека для другого агента", "я другому агенту пихну", "запиши все-все-все" | handoff | skill | relocated 2026-11-14 (extends хендофф row) |
| "что мы тут делали", "что мы тут с тобой обсуждали" | recap | skill | relocated 2026-11-14 (extends перескажи row) |
| "секреты", "не свети", "чекни что печатаешь" | boundaries | skill | relocated 2026-11-14 |
| "хочу скилл подготовить", "допили скиллы", "поправь скилл" | skill-scaffolder | skill | relocated 2026-11-14 |
| "оцени ценность находки", "это сток?", "любой бы это нашёл", "стоит ли это продавать" | roi | skill | relocated 2026-11-14 (extends цени находку row) |
| "чини", "пофикси", "напиши", "почини", "сделай фичу" | coding | skill | relocated 2026-11-14 (extends надо-написать row) |
| "пиши все в вокпланх", "адаптируйся тут", "здарова", "прочитай скиллы" | workplanx | skill | relocated 2026-11-14 (extends адаптируйся row) |
