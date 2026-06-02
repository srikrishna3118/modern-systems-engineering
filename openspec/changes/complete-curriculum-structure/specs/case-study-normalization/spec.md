## ADDED Requirements

### Requirement: Case studies have a canonical source of truth
The repository SHALL define one canonical source-of-truth location for reusable case studies, and course materials SHALL reference that source consistently.

#### Scenario: A course assigns a case study
- **WHEN** a syllabus, roadmap, or getting-started path references a case study
- **THEN** it links to the canonical version rather than an untracked duplicate

### Requirement: Canonical case studies use a consistent structural format
Each canonical case study SHALL use a consistent structure that includes overview, key challenges, architecture, core components or technology stack, design decisions or lessons learned, and further reading.

#### Scenario: Learner compares case studies across domains
- **WHEN** a learner opens two canonical case studies from different courses
- **THEN** both expose a comparable structure for architectural analysis and trade-off discussion

### Requirement: Courses curate case studies explicitly
Each course SHALL identify its required case studies and map them to the canonical case-study library using stable links.

#### Scenario: Course-specific required reading is published
- **WHEN** a learner follows a course syllabus or roadmap entry
- **THEN** the required case studies for that course are listed explicitly and resolve to canonical case-study files