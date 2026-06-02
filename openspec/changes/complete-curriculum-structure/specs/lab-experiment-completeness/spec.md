## ADDED Requirements

### Requirement: Promised labs provide complete scaffolds
Every lab promised by the curriculum SHALL include a lab README, a starter-code surface, and a solution surface that match the lab's stated learning objectives.

#### Scenario: Learner starts a promised lab
- **WHEN** a learner opens any lab referenced by the curriculum
- **THEN** the lab contains enough starter material to begin implementation and enough solution material to support comparison after completion

### Requirement: Labs include executable validation paths
Each lab SHALL document setup, run, and validation steps that let a learner verify behavior using documented commands, checks, or observable outcomes.

#### Scenario: Learner wants to verify a lab outcome
- **WHEN** the learner completes the implementation steps
- **THEN** the lab README provides an explicit validation path for confirming the lab works as intended

### Requirement: Labs include experiment-driven learning outcomes
Each lab SHALL include at least one concrete experiment or comparison exercise that connects the implementation to a systems trade-off such as latency, throughput, consistency, backpressure, scaling, or correctness.

#### Scenario: Learner completes the core implementation
- **WHEN** the learner reaches the reflection or extension part of the lab
- **THEN** the lab provides at least one experiment that requires observing and explaining a systems trade-off