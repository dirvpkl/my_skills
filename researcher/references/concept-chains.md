# Concept chains

Referenced by SKILL.md and patterns.md. A divergent-expansion technique: grow a
topic outward along association and graph sources instead of intuition. Use it
when the question is open ("what could we do with X", "what is adjacent to X",
"what to make of X") — a literal search answers the question asked; chains answer
the question that should have been asked.

## The move

1. **Seed** — 1-3 nouns of the *class*, not the user's literal examples (same
   anti-anchoring rule as everywhere else: user nouns are illustrations).
2. **Walk the graph sources** (classes below): collect real edges — concept →
   relation → concept, paper → neighbor paper, user → next page. Only edges you
   actually retrieved count; log which source each edge came from, and the
   association strength when the dataset has one.
3. **Map nodes by hop distance**: 1 hop = directly on an edge; 2 hops = through a
   shared intermediate; 3 hops = cross-domain. 20-30 nodes is a healthy map.
4. **Quick demand check per top node**: one search each — is there a paying
   audience, an existing market, a gap? A node without evidence stays a hypothesis.
5. **Feed forward**: top nodes become seeds for divergent passes (prisms,
   brainstorm routes). The map itself lives in the topic folder — it is storage
   for thinking, not evidence.

## Source classes for walking (tool availability varies per session)

- **Free-association norms** — datasets of "what follows this word in people's
  heads" with association strengths (e.g. USF Free Association Norms, Small World
  of Words). Direct edge source; downloadable; strongest for "what is adjacent in
  the human mind".
- **Lexical graphs** — WordNet-class synonym/hypernym graphs via NLTK; interactive
  visualizations of the same graph (e.g. Visuwords) are handy for eyeballing a
  node's neighborhood before scripting the walk. Good for renaming a node into
  searchable vocabulary, weak for demand.
- **Concept graphs** — ConceptNet-class API graphs of everyday relations. Broad
  but flaky: whole sessions have gone by with the API down (502). Rule: when a
  graph source is down, substitute a sibling source and log the substitution —
  a down API is a routing event, not a dead end.
- **User-clickstream datasets** — real hop chains of mass users between pages
  (Wikimedia Clickstream: per-language monthly dumps, streamable, minutes to
  filter). The crowd's attention chains with counts. Note: search traffic into a
  page is an upper bound of interest, not proof of purchasing demand.
- **Paper graphs** — citation/similarity graphs over research: OpenAlex
  (`related_to:` filter, generous limits; a reliable substitute when other graph
  APIs rate-limit or die), Semantic Scholar Graph API (rate-limits aggressively),
  Connected Papers / Litmaps-class sites (visual, no public API). Best for
  technology and algorithm adjacency.
- **Embedding similar-page search** — Exa-class neural search ("find pages like
  this one") — top-k semantic retrieval over the live web; the natural final hop
  when a node already has a concrete exemplar URL.

## Anti-patterns

- Inventing edges from memory instead of retrieving them. An unretrieved edge is
  a guess wearing a graph costume.
- Presenting hop distance as evidence. Distance says "adjacent", never "wanted".
- Anchoring seeds on the user's literal examples. The seed is the class.
- Letting the map become the deliverable. The deliverable is still findings with
  demand evidence; the map only widens where to look.
- Walking without logging the source per edge — an unlabeled map cannot be
  re-walked or audited by the next session.
