# Course 01 – Engineering Foundations

**Duration:** 4 weeks. **Prerequisite:** none.

## Overview

This course covers the core principles of software and systems engineering, providing the foundational knowledge required for all subsequent courses.

## Topics

- Software design principles (SOLID, DRY, KISS)
- Systems thinking and complexity
- Reliability and fault tolerance fundamentals
- API design and documentation
- Version control best practices
- Code review and collaboration workflows

## Learning Objectives

- Understand fundamental design principles used in modern systems.
- Apply systems thinking to break down complex engineering problems.
- Build and document APIs following industry standards.
- Measure a reliability change (retries, circuit breakers) instead of only describing it.

## How to complete this course

1. Read both lectures.
2. Do the API lab, then the reliability lab. Each README has a setup, a validation curl or script, and an experiment.
3. Read the two case studies and note which lecture idea they are an example of.

## Lectures

- [Lecture 1: Engineering Fundamentals](lectures/lecture-01-engineering-fundamentals.md) — SOLID, systems thinking, reliability, APIs, version control
- [Lecture 2: Building Scalable Systems](lectures/lecture-02-building-scalable-systems.md) — vertical and horizontal scaling, caching, partitioning, replication, consistency, load balancing

## Labs

- [API Task Service](labs/api-task-service) — contracts, validation, pagination
- [Reliability Toolkit](labs/reliability-toolkit) — retries, backoff, circuit breaker

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). Files in this course's `case-studies/` folder are pointers.

- [AWS cell architecture](../case-studies/aws-cell-architecture.md) — isolation as a reliability strategy
- [Uber's microservices migration](../case-studies/uber-microservices-migration.md) — splitting a system without stopping it
