# Course 03 – Cloud Infrastructure

**Duration:** 4 weeks. **Prerequisite:** Course 02.

## Overview

This course covers cloud platforms, infrastructure-as-code, and modern operations practices for building reliable and scalable systems.

## Topics

- Cloud provider fundamentals (AWS, GCP, Azure) — [Lecture 1](lectures/lecture-01-cloud-networking-security.md)
- Networking and security in the cloud — Lecture 1
- Infrastructure as Code with Terraform — [Lecture 2](lectures/lecture-02-iac-kubernetes-serverless-finops.md)
- Container orchestration with Kubernetes — Lecture 2
- Serverless architectures — Lecture 2
- Cost optimization and FinOps — Lecture 2

## Learning Objectives

- Provision and manage cloud infrastructure using code.
- Deploy containerized applications to Kubernetes.
- Design secure and cost-effective cloud architectures.

## How to complete this course

1. Read Lecture 1, then Lecture 2.
2. Run the Kubernetes lab locally (`python smoke_test.py` in the solution, or Compose) and read the manifests even if you do not have a cluster.
3. Read the case studies and write down, for each, which failure is isolated and which cost is accepted.

## Lectures

- [Lecture 1: Cloud Foundations, Networking, and Security](lectures/lecture-01-cloud-networking-security.md)
- [Lecture 2: IaC, Kubernetes, Serverless, and Cost](lectures/lecture-02-iac-kubernetes-serverless-finops.md)

## Labs

- [Kubernetes Deployment](labs/kubernetes-deployment) — image, probes, requests and limits, Service

## Case studies

Canonical copies live in [`../case-studies/`](../case-studies/). Course-local files are pointers.

- [Kubernetes orchestration](../case-studies/kubernetes-orchestration.md)
- [AWS cell architecture](../case-studies/aws-cell-architecture.md)
- [AWS Aurora](../case-studies/aws-aurora.md) — a managed database, as the contrast to running state yourself
