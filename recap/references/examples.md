# recap — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Records, not chat memory

**Good:** the recap is rebuilt from log.md, decision.md, and git log — every line traceable to a file + date or a commit.
**Bad:** "from what I remember of our sessions, we did A, then B."
Rationale: the project's memory is on disk, not in chat — chat-recall alone never fills a recap, and a guess never ships as history.

## Verbatim means verbatim

**Good:** the parked ask quotes the owner's exact words from the decision file.
**Bad:** summarizing the owner's verdict into the agent's own phrasing "for readability."
Rationale: verdicts and parked asks are quoted verbatim — a paraphrase is the agent's interpretation, not the owner's words, and the distinction is the whole point.

## A gap is reported as a gap

**Good:** "Asked-not-done — none found in the records."
**Bad:** padding the empty section with something plausible "so the recap doesn't look thin."
Rationale: empty sections are data, not omissions — filling a gap by inference manufactures history that never happened.

## Read-only stays read-only

**Good:** the recap spots a mislabeled `#wildshot` and reports the discrepancy as a finding.
**Bad:** "correcting" the hashtag to a recommendation in the file while recapping.
Rationale: a recap summarizes and never edits project files — relabeling a wildshot into a recommendation silently rewrites the project's record.
