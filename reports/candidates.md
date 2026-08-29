# Your Voice discovery candidates

Generated: 2026-08-24

Discovery does not imply endorsement or adoption. Check provenance, license, code, privacy, and eval impact.

- [Arindaag760/humanizer-cli](https://github.com/Arindaag760/humanizer-cli)
  - updated: `2026-08-25T04:07:22Z`
  - license: `MIT`
  - description: Detect AI-written text with 33 checks, right in your terminal. Offline, no API key, no dependencies.

## Tracked upstreams

- [blader/humanizer](https://github.com/blader/humanizer)
  - reviewed: `v2.11.1`
  - latest release: `v2.11.1`
  - head: `e2e92e7b4b82`
  - pushed: `2026-08-19T05:58:53Z`
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
  - reviewed: `v3.26.0`
  - latest release: `v3.26.0`
  - head: `40328bd292bc`
  - pushed: `2026-08-24T17:41:39Z`
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop)
  - reviewed: `v1.0.6`
  - latest release: `v1.0.6`
  - head: `d30eddb9e045`
  - pushed: `2026-08-06T04:20:10Z`
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
  - reviewed: `8da1f030185b`
  - latest release: `none`
  - head: `8da1f030185b`
  - pushed: `2026-03-17T18:50:39Z`
- [cosmos-makers/writer-persona](https://github.com/cosmos-makers/writer-persona)
  - reviewed: `5eee0fd5b0c2`
  - latest release: `none`
  - head: `5eee0fd5b0c2`
  - pushed: `2026-04-01T11:50:28Z`
- [AshwinSathian/humanize-writing-skill](https://github.com/AshwinSathian/humanize-writing-skill)
  - reviewed: `0c3f05bc4f37`
  - latest release: `none`
  - head: `0c3f05bc4f37`
  - pushed: `2026-08-18T00:25:49Z`

## Candidate Review: Claude Skill Library

- Source: https://www.claude-skills.free/
- Retrieved: 2026-08-29
- License: not stated on downloadable archives
- Decision: adopt only deduped rule gaps; do not vendor downloaded skills.

## Reviewed from downloaded archives

- `delete-ai-words`: overlaps heavily with Your Voice, Humanizer, Stop Slop, and No AI Slop. Adopted the missing stricter checks for soft reframes, engagement bait, bloated substitute verbs, metaphor setups, and a wider small vocabulary audit.
- `grill-me`: too broad for the default Your Voice workflow because it mandates 10-15 questions before most non-trivial builds. Adopted only the narrower writing-relevant rule: check context sufficiency before blank-slate drafting and ask only questions that would change the output.

## Reviewed from linked LinkedIn post

- URL: https://www.linkedin.com/posts/ruben-hassid_its-crazy-how-my-entire-linkedin-feed-is-share-7499210276655976448-7g33/
- Source note: Paras provided a `lnkd.in` short link that resolved to this post.
- Decision: most listed tells already existed in Your Voice. Added the missing audit coverage for fake-process intros, “realm,” standalone “crucial/pivotal,” and adverb-abuse constructions like “quietly runs.”
- Listed skills: `/writer`, `/editor`, `/fact-checker`, `/anti-AI style`, `/ban-the-AI-words`, `/ban-the-AI-patterns`, `/sound like your posts`, `/humanizer`, `/red-pen`, `/self-critique`, `/auto-block-banned-words`.
- Dedupe: these map to existing Your Voice modes and latch passes, so no separate subskills were added.

## Reviewed from public metadata only

- `humanizer`: likely duplicate of existing Your Voice scope; archive required unlock.
- `personal-voice`: likely duplicate of existing voice profile workflow; archive required unlock.
- `the-team`: likely duplicate of existing writer/editor/fact-check latch pass; archive required unlock.
- `red-pen`: likely overlaps with audit mode; archive required unlock.
- `sound like your posts`: likely overlaps with approved-sample calibration; archive required unlock.
- `my-viral-post` and `linkedin-hook`: relevant to channel-specific drafting but high risk of viral-template flattening; archive required unlock.
- `fact-checker`: relevant to the truth pass, but archive required unlock.
- `prompt-master`: possibly relevant to spec creation, but archive required unlock.
