# Discussion: complete-curriculum-structure

## Challenge Report

### Challenge 1: Scope bundling increases partial completion risk
- **Source**: Proposal §What Changes (all four bullets)
- **Assumption**: Documentation alignment, case-study normalization, and lab content creation can be completed as a single coordinated change
- **Failure mode**: If implementation time runs out, the change could leave documentation partially aligned, some labs complete while others remain placeholders, and case-study ownership still unclear — worse than the current state
- **Risk category**: integration
- **Mitigation**: Define explicit completion criteria for each capability before implementation starts, and implement in dependency order (docs first, then case studies, then labs) so partial completion still delivers value

### Challenge 2: "Minimum complete lab standard" lacks concrete criteria
- **Source**: Design §Decision 3
- **Assumption**: "Lab overview, prerequisites, setup, implementation milestones, validation steps, experiment rubric, starter-code surface, and solution surface" is sufficiently specific for consistent implementation
- **Failure mode**: Different implementers could interpret "validation steps" or "experiment rubric" differently, leading to inconsistent lab quality across courses
- **Risk category**: correctness
- **Mitigation**: Define and document a reference lab structure with concrete examples before implementing Course 01 exercises or placeholder lab replacements. Use one existing complete lab as the normalization template.

### Challenge 3: Course 02 lab scope remains unresolved
- **Source**: Design §Open Questions, second bullet
- **Assumption**: The Course 02 lab scope question can be resolved during implementation
- **Failure mode**: If this decision is deferred, task 2.2 (update Course 02 syllabus) cannot be completed correctly, blocking downstream lab work
- **Risk category**: integration
- **Mitigation**: Resolve the Course 02 scope question during the discuss phase, not during implementation. Recommendation: narrow to the roadmap-level promise (2 labs) to maintain contract consistency, and defer additional labs to a future change.

### Challenge 4: Case-study normalization effort underestimated
- **Source**: Design §Decision 5, Tasks §3.2
- **Assumption**: Normalizing case studies to a consistent structure is straightforward given existing high-quality examples
- **Failure mode**: With ~20 case studies in the global library, applying a consistent format could consume significant time and risk introducing errors or content loss during reformatting
- **Risk category**: performance
- **Mitigation**: Limit normalization scope to only case studies explicitly referenced by course curricula. Leave unreferenced case studies in their current format to reduce scope. Prioritize structural consistency over exhaustive coverage.

### Challenge 5: Removing course-local case studies could break existing workflows
- **Source**: Design §Decision 1, Risks/Trade-offs first bullet
- **Assumption**: Updating all references within this change is sufficient to prevent breaking learner workflows
- **Failure mode**: External bookmarks, citations in forums or blog posts, or local learner notes could point to course-local case-study paths that no longer exist, creating a poor experience for returning learners
- **Risk category**: ux
- **Mitigation**: Instead of deleting course-local case-study files, replace them with lightweight redirect files that reference the canonical location. Include a deprecation notice and the canonical path so learners can update their bookmarks.

## Counter-Designs

### Option 1: Three-phase sequential approach
Instead of bundling documentation, case studies, and labs into one change, split into three sequential changes: (1) documentation alignment only, (2) case-study canonicalization, (3) lab completion. Each change is smaller and easier to review.

**Pros**: Reduces risk per change, allows validation after each phase, easier to roll back individual pieces.

**Cons**: Increases coordination overhead across three changes, learners still see inconsistent state between phases, first phase (documentation-only) might reduce promises without delivering new value.

**Trade-offs**: Safety vs. momentum. Sequential approach is safer but takes longer to resolve learner confusion.

### Option 2: Documentation-only alignment
Align all learner-facing documents to the current implemented state without adding any new content. Explicitly mark Course 01 exercises, Course 04 RAG lab, and Course 06 payment ledger lab as "planned" or "coming soon" in the curriculum roadmap.

**Pros**: Minimal scope, fast to implement, eliminates misleading promises immediately.

**Cons**: Reduces curriculum ambition, doesn't solve the core problem (missing promised assets), learners still can't complete the advertised curriculum.

**Trade-offs**: Honesty vs. completeness. This approach is honest about current state but doesn't close the gap.

### Option 3: Lab-first content creation
Implement all missing labs (Course 01 exercises, Course 04 RAG, Course 06 payment ledger, normalize existing labs) first, then update documentation to reflect the new reality. Ensures docs never overstate implementation.

**Pros**: Guarantees documentation accuracy, delivers tangible learner value before changing contracts.

**Cons**: Learners face confusing documentation during lab implementation, harder to justify lab work without aligned curriculum contract, risks duplicating effort if lab direction changes.

**Trade-offs**: Truth-first vs. clarity-first. This approach prioritizes implementation truth but leaves learners confused during transition.

**Recommendation**: Endorse the original bundled proposal with amendments from Challenge mitigations. The bundled approach resolves learner confusion faster than sequential phases, delivers more value than documentation-only, and provides clearer guidance than lab-first. Key amendments: resolve Course 02 scope now (narrow to 2 labs), define explicit lab completion criteria before implementation, limit case-study normalization to referenced studies, and use redirect files instead of deleting course-local case studies.

## Decisions Made

- **D1**: Proceed with the bundled approach, but add explicit acceptance criteria to each task group before starting implementation to reduce partial completion risk. — *The bundled approach resolves learner confusion faster, but needs clearer success metrics.*

- **D2**: Resolve Course 02 lab scope immediately: narrow the Course 02 syllabus to match the roadmap-level promise of 2 labs (Chat System and Kafka Pipeline), and remove unsupported syllabus entries for Labs 3 and 4. — *Deferring this decision blocks implementation; narrowing maintains contract consistency.*

- **D3**: Limit case-study normalization scope to only case studies explicitly referenced by course curricula. Leave unreferenced global case studies in their current format. — *This reduces normalization effort while still delivering structural consistency where it matters most.*

- **D4**: Do not delete course-local case-study files. Replace them with lightweight redirect files containing a deprecation notice and a link to the canonical case-study location. — *This prevents breaking external bookmarks while guiding learners toward the canonical source.*

- **D5**: Before implementing Course 01 exercises or placeholder lab replacements, define a concrete reference lab structure by documenting the existing Chat System or Kubernetes Deployment lab as the normalization template. — *This ensures consistent interpretation of "minimum complete lab standard."*

- **D6**: Implement task groups in dependency order: curriculum contract alignment first, case-study normalization second, lab completion third. — *This ensures partial completion still delivers incremental value if implementation time runs short.*
