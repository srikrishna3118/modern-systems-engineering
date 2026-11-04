# Course 06 – Financial Systems

**Duration:** 3 weeks. **Prerequisite:** Course 02. Course 05's event and window material helps for fraud features.

## Overview

This course examines the design of high-reliability, compliance-driven financial systems, covering payments, trading platforms, and risk management.

## Topics

- High-availability and fault-tolerant system design — [Lecture 1](lectures/lecture-01-payments-idempotency-availability.md)
- Payment processing and transaction management — Lecture 1
- Idempotency and exactly-once semantics — Lecture 1
- Regulatory compliance (PCI-DSS, SOX) — [Lecture 2](lectures/lecture-02-compliance-fraud-audit.md)
- Fraud detection systems — Lecture 2
- Audit logging and data integrity — Lecture 2

## Learning Objectives

- Design financial systems that meet reliability and compliance requirements.
- Implement idempotent and transactionally safe operations.
- Build fraud detection pipelines using real-time data.

## How to complete this course

1. Read Lecture 1 and do the ledger lab. The smoke test is the invariant: replay does not move money twice, and the balances sum to zero.
2. Read Lecture 2. Write down the timeout default you would ship for a fraud check, and why.
3. Read the Stripe case study after the lab, and compare their idempotency key with yours.

## Lectures

- [Lecture 1: Payments, Idempotency, and Availability](lectures/lecture-01-payments-idempotency-availability.md)
- [Lecture 2: Compliance, Fraud, and the Audit Log](lectures/lecture-02-compliance-fraud-audit.md)

## Labs

- [Payment Ledger](labs/payment-ledger) — double-entry, idempotency keys, audit log

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). The course-local file is a pointer.

- [Stripe payment system](../case-studies/stripe-payment-system.md) — the assigned study
- [Stripe payment processing](../case-studies/stripe-payment-processing.md) — shorter companion note on the same system

Trading-platform design is not a separate case study in this repository. Use Lecture 1's rule (refuse a write you cannot order) as the starting point if you extend the course in that direction.
