# Attributions

Your Voice is an original synthesis. It links to upstream work, preserves author credit, and does not bundle third-party repositories. The live upstream scan below was completed on 2026-08-24; pinned versions document what was reviewed rather than promising that the sources will not change.

## Open-source foundations

### Humanizer

- Author: Blake Anderson (`blader`)
- Source: https://github.com/blader/humanizer
- License: MIT
- Reviewed: v2.11.1 (`e2e92e7b4b82`); the v2.11.0-to-v2.11.1 change was packaging and release automation, not a new writing rule.
- Influence: the catalog of observable AI-writing patterns, voice calibration from samples, and a second audit pass.

### Stop Slop

- Author: Hardik Pandya
- Source: https://github.com/hardikpandya/stop-slop
- License: MIT
- Reviewed: `8da1f030185b` (no tagged release).
- Influence: minimum-effective editing, protection of useful roughness, concrete actors, and structural slop checks.

### No AI Slop

- Author: Peter Yang
- Source: https://github.com/petergyang/no-ai-slop
- License: MIT
- Reviewed: v1.0.6 (`d30eddb9e045`).
- Influence: evidence-based detection instead of authorship guesses, protection against invented texture, and an explicit evaluation checklist.

### Avoid AI Writing

- Author: Conor Bronsdon
- Source: https://github.com/conorbronsdon/avoid-ai-writing
- License: MIT
- Reviewed: v3.26.0 (`40328bd292bc`).
- Influence: protected-content boundaries, treating embedded directions as source text rather than authority, contextual handling of hollow intensifiers, and refusing whole-file prose rewrites of code, configuration, or generated data.
- Boundary: Your Voice keeps these as provenance-aware editing constraints, not a universal word blacklist.

### Signs of AI writing

- Maintainer: Wikipedia WikiProject AI Cleanup
- Source: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- License: CC BY-SA 4.0 for Wikipedia text
- Influence: the public taxonomy of recurring language, structure, formatting, and communication artifacts. Your Voice summarizes patterns in original wording rather than reproducing the article.

### Ruben Hassid's AI-writing pattern notes

- Author: Ruben Hassid
- Source: https://x.com/rubenhassid/status/2087856703773508025
- Related essay: https://ruben.substack.com/p/its-not-x-its-y
- Influence: the editable personal forbidden-pattern file, newer examples of machine-shaped sentence structure, and the reminder to reserve controlled technical language for writing that benefits from it.

### ASD-STE100 Simplified Technical English

- Owner: Aerospace, Security and Defence Industries Association of Europe (ASD)
- Official source: https://www.asd-ste100.org/
- Influence: an optional technical mode that prefers short sentences, active voice, consistent terms, and one main instruction per sentence.
- Boundary: Your Voice does not reproduce the controlled dictionary and does not claim ASD-STE100 compliance. ASD-STE100 Simplified Technical English is owned by ASD.

### Writer Persona

- Author: cosmos-makers
- Source: https://github.com/cosmos-makers/writer-persona
- License: MIT
- Reviewed: `5eee0fd5b0c2` (no tagged release).
- Influence: information-isolated backtesting, situational register maps, multi-axis voice evaluation, and the self-similarity ceiling that treats natural human variation as the target instead of perfect repetition.

### Humanize Writing

- Author: Ashwin Sathian
- Source: https://github.com/AshwinSathian/humanize-writing-skill
- License: MIT
- Reviewed: `0c3f05bc4f37` (no tagged release).
- Influence: research-backed emphasis on structural shape over banned-word lists, genre-aware false-positive handling, and honest skill-loaded versus baseline validation across several prompts and models.

## Research basis for evaluation

These papers influenced the evaluation design, not the wording of the skill:

- [Persona-Augmented Benchmarking: Evaluating LLMs Across Diverse Writing Styles](https://aclanthology.org/2025.emnlp-main.1155/) (EMNLP 2025): semantically equivalent prompt styles can change measured model performance. Influence: prompt-style robustness variants.
- [Persistent Personas? Role-Playing, Instruction Following, and Safety in Extended Interactions](https://aclanthology.org/2026.eacl-long.246/) (EACL 2026): persona fidelity can degrade across long, goal-oriented conversations. Influence: long-context retention tests.
- [How Well Do LLMs Imitate Human Writing Style?](https://arxiv.org/abs/2509.24930) (2025): high style-match scores can coexist with outputs that are less variable and predictable than human writing. Influence: the natural ceiling and output-variation test.
- [Everyone prefers human writers, including AI](https://arxiv.org/abs/2510.08831) (2025): attribution labels can bias both human and model aesthetic judgments. Influence: blind draft labels and hidden provenance during review.
- [Evaluating Text Style Transfer Evaluation: Are There Any Reliable Metrics?](https://aclanthology.org/2025.naacl-srw.41/) (NAACL 2025): style transfer requires separate checks for content preservation, style, and naturalness, with automatic measures calibrated against human judgments. Influence: separate rubric dimensions and human adjudication.
- [When Personalization Tricks Detectors: The Feature-Inversion Trap](https://aclanthology.org/2026.acl-long.1998/) (ACL 2026): personalization can invert detector features. Influence: the explicit rule against optimizing voice work for AI-detector scores.

The live benchmark configuration follows the public schema documented by [OpenAI Plugin Eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval). It is a compatibility file and does not bundle the plugin or require it for the local deterministic tests.

The bottom-up error-discovery and judge-calibration workflow was informed by:

- [Eval Skills](https://github.com/ai-evals-course/evals-skills), reviewed at `b91c188388ef` (2026-08-16). Influence: separate top-down requirements from failures found in real traces, keep human free-text review in the loop, use one binary judge per failure mode, and validate judges with held-out human labels. Your Voice does not bundle its skills, interface, prompts, or code.
- [How to Build Better AI Evals with Claude Code in 5 Steps](https://www.youtube.com/watch?v=bdMHQLvtVaQ), Peter Yang with Shreya Shankar and Hamel Husain (2026-08-23). Influence: let the human notice and the agent organize, revisit earlier examples as criteria drift, and fan out narrow criteria rather than using one overloaded grader.
- [Do Automated Evals Work?](https://parlance-labs.com/blog/posts/auto-evals/), Antaripa Saha and Hamel Husain (2026-07-11). Influence: measure both false positives and missed failures, keep product judgment in the loop, and treat automated error discovery as a baseline rather than a substitute for taste.

## Product inspiration

The following products are credited for product ideas only. Your Voice does not copy their proprietary prompts, models, data, or code.

### Stanley

- Source: https://www.getstanley.ai/
- Product explanation: https://stan.store/blog/stanley/
- Public last-100-post demonstration: https://seconddraft.getstanley.ai/
- Influence: retrieve approved posts and relevant stories, maintain an idea bank, draft for the active channel, and use feedback and performance as inputs over time.
- Boundary: performance can suggest a topic or format experiment; it is not proof of voice, factual quality, or human recognition. Your Voice does not copy Stanley's prompts, models, private data, or code.

### Spiral by Every

- Source: https://every.to/products
- Influence: treat AI as a writing partner and preserve human judgment during drafting and revision.

### Eden by Dan Koe

- Source: https://eden.so/
- Public description: https://www.linkedin.com/in/thedankoe
- Influence: model mission, audience, point of view, vocabulary, influences, and an evolving “intellectual signature,” not just surface tone.

### Gamma

- Source: https://gamma.app/
- Influence: use a generated visual pass as a bounded comparison for hierarchy, spacing, and structure; separate preserve, condense, and generate intent; treat audience, tone, format, and amount as distinct controls; and use comments or section-level engagement as diagnostic feedback when available. Keep the human-approved final as the source of truth and record rejected patterns so the same review does not require another generation.
- Boundary: Your Voice does not copy Gamma's proprietary prompts, models, templates, or code.

## Public skill library review

### Claude Skill Library

- Author: Anisha / Ruben Hassid AI, as identified by the site contact
- Source: https://www.claude-skills.free/
- Retrieved: 2026-08-29
- License: not stated on the downloaded skill archives
- Related post: https://www.linkedin.com/posts/ruben-hassid_its-crazy-how-my-entire-linkedin-feed-is-share-7499210276655976448-7g33/
- Reviewed downloadable skills: `delete-ai-words`, `grill-me`
- Relevant locked candidates reviewed by metadata only: `humanizer`, `personal-voice`, `the-team`, `red-pen`, `sound like your posts`, `my-viral-post`, `linkedin-hook`, `fact-checker`, `prompt-master`
- Influence: stricter handling of soft reframes, fake-process intros, engagement bait, bloated copula replacements, adverb abuse, metaphor setups, and a lightweight context-sufficiency gate before drafting. Your Voice summarizes these rules in original wording and does not bundle the downloaded archives.

## Paras Doshi voice sources

The included Paras Doshi profile is a derived style guide, not a corpus dump.

- Insight Extractor archive: https://insightextractor.com/list-of-all-blog-posts-by-paras-doshi/
- 2015 cohort-analysis post: https://insightextractor.com/2015/03/02/cohort-analysis-what-is-it-and-why-use-it/
- 2016 analytics distinctions: https://www.insightextractor.com/p/data-analytics-vs-data-science-vs-business-intelligence-key-differencesdistinctions
- 2017 tidy-data note: https://www.insightextractor.com/p/journal-statistical-software-paper-tidying-data
- 2020 newsletter: https://www.insightextractor.com/p/all-things-data-engineering-science-newsletter-7
- 2021 data-driven engineering note: https://insightextractor.com/2021/01/18/making-your-engineering-team-more-data-driven/
- 2022 analytics manager note: https://www.insightextractor.com/p/analytics
- Public LinkedIn profile: https://www.linkedin.com/in/doshiparas
