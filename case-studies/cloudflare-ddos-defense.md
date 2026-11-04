# Case Study: Cloudflare DDoS Defense – Protecting the Internet at Scale

## Overview

Cloudflare mitigates some of the largest DDoS attacks ever recorded (>2 Tbps) across 200+ data centers. Its architecture defends millions of websites against volumetric attacks, protocol exploits, and application-layer attacks in real-time.

## Key Challenges

- **Petabits/Day Traffic**: Processing and filtering terabits per second of attack traffic
- **Attack Diversity**: Attacks span L3/L4 (TCP, UDP) to L7 (HTTP); each requires different detection/mitigation
- **False Positives**: Blocking legitimate traffic loses customers; precision is critical
- **Speed**: Blocking decisions must be made in milliseconds; no time for expensive computation

## Architecture Highlights

- **Anycast Network**: BGP anycast distributes attack traffic across all edge locations, turning massive attacks into manageable per-PoP loads
- **eBPF Firewalls**: XDP (eXpress Data Path) programs in the Linux kernel filter packets at line rate (millions/sec/core)
- **dosd (Daemon)**: Userspace daemon that analyzes attack traffic, generates firewall rules, pushes to XDP
- **Centralized Detection (Gatebot)**: Global anomaly detection consumes sampled metrics, disseminates blocking rules to all PoPs
- **Layered Defense**: L3/L4 volumetric filtering + L7 challenge/block (CAPTCHA, JavaScript challenge)

## Technology Stack

- Go (detection/control plane), Rust (performance-critical code), C (eBPF)
- eBPF/XDP (kernel-space filtering), custom time-series metrics (billions of metrics/day)

## Lessons Learned

1. **Anycast turns attacks into distributed load** — Global routing distributes attacks; each PoP handles only a fraction
2. **eBPF/XDP enables kernel-bypass filtering** — User-space packet processing is too slow; kernel-space filtering achieves line-rate throughput
3. **Centralized detection + local enforcement** — Global rules are detected centrally and enforced locally; balances visibility and latency
4. **Layered defenses are necessary** — L3/L4 filtering (volumetric) + L7 challenge/block (sophistication); single layer insufficient
5. **Sampling and aggregation reduce signal** — Processing billions of packets requires sampling; aggregated metrics still provide attack visibility

## Where this fits in the curriculum

- [Course 07, Lecture 4: Rate limiting](../course-07-advanced-system-design/lectures/lecture-04-rate-limiting.md) and [Lecture 5: Security](../course-07-advanced-system-design/lectures/lecture-05-security-zero-trust.md) — the edge layer under application limits.
- [Course 07, Exercise 3: Rate limiter](../course-07-advanced-system-design/exercises/03-rate-limiter.md) — what this system deliberately does *not* do (per-token API quotas).
- Course pointer: [course 07 wrapper](../course-07-advanced-system-design/case-studies/cloudflare-ddos-defense.md).

## Further Reading

- [Cloudflare DDoS Protection](https://www.cloudflare.com/ddos/)
- [DDoS Protection with eBPF and XDP (Cloudflare Blog)](https://blog.cloudflare.com/)
