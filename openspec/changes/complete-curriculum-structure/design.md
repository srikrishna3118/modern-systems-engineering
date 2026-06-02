## Context

The repository already has a strong top-level information architecture, but the course contract is inconsistent. Top-level documents describe a complete curriculum with finished labs and coordinated course materials, while several course folders still contain placeholder labs, partial case-study mirrors, or syllabi that overstate what is present. This change spans multiple courses and documentation layers, so it needs an explicit design rather than ad hoc file-by-file cleanup.

The current state also mixes two case-study models: a global case-study library and partial per-course case-study copies. That makes ownership unclear and creates drift risk as case studies evolve.

## Goals / Non-Goals

**Goals:**
- Establish a single, coherent learner contract across top-level guides and course syllabi.
- Normalize case-study ownership and formatting so course curation does not depend on duplicated content.
- Bring all promised labs to a minimum complete standard with README guidance, starter material, solution material, validation steps, and experiment framing.
- Resolve the highest-impact structural gaps first: Course 01 exercises, placeholder labs in Courses 04 and 06, and inconsistent course promises.

**Non-Goals:**
- Author a full lecture series for every course in this change.
- Expand the curriculum beyond the scope already promised by the repository.
- Introduce a new content management system or automated curriculum generator.

## Decisions

### Decision 1: Use the global case-study library as the canonical source
The global `case-studies/` directory will be treated as the source of truth for reusable case studies. Course materials will curate and link to canonical case studies instead of maintaining parallel copies by default.

Alternative considered: keep separate per-course case-study copies. Rejected because it increases maintenance cost and makes structural normalization harder.

### Decision 2: Align documents to the implemented curriculum contract, using current public promises as the baseline
The roadmap, README, and Getting Started guide define the public learner contract. Course-local overclaims will be corrected, while high-value promised assets that are currently missing but small enough to add in this change will be implemented.

Alternative considered: reduce all top-level promises to match the thinnest current implementation. Rejected because it would lower the curriculum ambition instead of completing the most important gaps.

### Decision 3: Standardize labs around a minimum complete lab format
Every promised lab will be normalized to include: lab overview, prerequisites, setup, implementation milestones, validation steps, experiment rubric, starter-code surface, and solution surface.

Alternative considered: limit this change to documentation cleanup only. Rejected because learner confusion is caused partly by missing assets, not just wording.

### Decision 4: Resolve scope mismatches by prioritizing concrete learner outcomes
Course 01 will gain the promised foundational exercises. Courses 04 and 06 will replace placeholder lab directories with real starter and solution content. Course 02 will be evaluated against the roadmap-level promise; unsupported extra syllabus entries will be removed unless fully implemented in this change.

Alternative considered: implement every aspirational lab mentioned anywhere in the repo. Rejected because it expands scope without first fixing contract consistency.

### Decision 5: Use the strongest existing case-study structure as the normalization template
Existing high-quality case studies that already include architecture, challenges, design decisions, lessons learned, and further reading will serve as the formatting reference for normalization.

Alternative considered: invent a new bespoke template unrelated to current content. Rejected because it would create needless rewrite work.

## Risks / Trade-offs

- [Risk] Normalizing to a canonical case-study source may break existing course-local links. → Mitigation: update all course and top-level references within the same change.
- [Risk] Adding missing lab scaffolds broadens the change substantially. → Mitigation: define a minimum complete lab standard and prioritize only promised labs.
- [Risk] Aligning documents to implemented assets may force some course-level reductions. → Mitigation: prefer implementing missing high-value assets before reducing promises, and only trim unsupported overclaims.
- [Risk] Structural consistency work may overshadow content depth improvements. → Mitigation: treat this change as a foundation pass that enables later depth-oriented changes.

## Migration Plan

1. Inventory learner-facing promises and actual course assets.
2. Decide and document the canonical case-study model.
3. Update top-level curriculum documents and course syllabi to the aligned contract.
4. Add or complete missing promised lab assets, prioritizing placeholder and absent labs.
5. Normalize lab READMEs with validation and experiment sections.
6. Validate links, lab surfaces, and OpenSpec artifact completeness before implementation handoff.

Rollback is file-based: individual content changes can be reverted without schema or runtime migration concerns.

## Open Questions

- Should course-local case-study folders retain lightweight wrapper files for discoverability, or should they be removed entirely in favor of canonical global links?
- For Course 02, is it preferable to add two additional labs later under a separate change, or permanently narrow the syllabus to the two labs already promised at the roadmap level?