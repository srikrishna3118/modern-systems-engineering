## ADDED Requirements

### Requirement: Curriculum documents reflect implemented assets
The curriculum SHALL describe a consistent implemented asset set across the top-level README, Getting Started guide, curriculum roadmap, and course syllabi. Learner-facing documents MUST NOT promise lectures, labs, exercises, or solutions that are absent from the repository.

#### Scenario: Inconsistent course promises are reconciled
- **WHEN** a course asset is referenced by more than one learner-facing document
- **THEN** each reference describes the same implemented scope, required work, and asset availability

### Requirement: Each course defines a learner contract
Each course SHALL include a syllabus that states prerequisites, learning objectives, required course assets, and the expected completion path for that course.

#### Scenario: Learner enters a course folder
- **WHEN** a learner reads a course syllabus
- **THEN** the learner can determine what to study, what to build, and which case studies or labs are required without consulting conflicting documents

### Requirement: Promised foundational exercises exist in the repository
Any foundational exercises promised as part of the curriculum SHALL exist as concrete course assets in the repository with discoverable locations.

#### Scenario: Roadmap promises foundational exercises
- **WHEN** the roadmap or syllabus states that Course 01 includes hands-on exercises
- **THEN** the repository contains those exercises in the Course 01 asset tree