# Case Study: Cloudflare DDoS Defense

## Overview
Cloudflare sits in front of millions of websites and applications, absorbing and mitigating some of the largest distributed denial-of-service (DDoS) attacks ever recorded — including attacks exceeding 2 Tbps. This case study examines how Cloudflare's global network architecture enables it to detect and neutralize volumetric and application-layer attacks in real time.

## Key Challenges
- **Scale**: Processing and filtering petabits of traffic per day across 200+ data centers.
- **Speed**: Detecting attack patterns and applying mitigations within seconds.
- **Accuracy**: Blocking malicious traffic without disrupting legitimate users.
- **Variety**: Defending against volumetric (L3/L4), protocol, and application-layer (L7) attacks simultaneously.

## Architecture Highlights

### Anycast Network
Cloudflare uses BGP anycast to advertise the same IP address ranges from all of its 200+ data centers worldwide. When an attacker sends traffic to a Cloudflare-protected IP, that traffic is naturally distributed to the nearest Cloudflare PoP (Point of Presence) by internet routing. This inherently distributes attack traffic across the entire network rather than concentrating it in one location.

### dosd – Denial of Service Daemon
Each Cloudflare server runs `dosd`, a userspace daemon that analyzes packet headers using eBPF programs in the Linux kernel. `dosd` can generate and push firewall rules (expressed as XDP/eBPF programs) in milliseconds, dropping attack packets before they consume any significant CPU.

### Gatebot – Centralized Detection
`Gatebot` is Cloudflare's centralized DDoS detection service. It consumes sampled traffic metrics from all PoPs, identifies attack signatures (e.g., unusual packet rates from specific ASNs, HTTP floods targeting a single URL), and propagates mitigation rules globally.

### flowtrackd – Advanced TCP DDoS Protection
For sophisticated TCP-based attacks, Cloudflare developed `flowtrackd`, a stateful TCP flow tracking daemon. It validates TCP handshakes at line rate using eBPF, distinguishing legitimate connections from spoofed or malformed SYN floods without requiring full kernel TCP stack processing.

### L7 Mitigation and Managed Rules
For HTTP/HTTPS traffic, Cloudflare applies a layered ruleset (Managed Rules + customer-defined WAF rules) powered by its Ruleset Engine. Suspicious requests can be challenged (CAPTCHA, JS challenge) rather than outright blocked, minimizing false positives.

## Technology Stack
- **Languages**: Go, Rust (eBPF programs in C)
- **Kernel tech**: eBPF, XDP (eXpress Data Path) for kernel-bypass packet processing
- **Routing**: BGP anycast across 200+ PoPs
- **Observability**: Custom time-series metrics pipeline, real-time traffic analytics

## Lessons Learned
1. Distributing attack traffic across a global anycast network turns a massive single-target attack into a manageable distributed load.
2. eBPF/XDP enables kernel-bypass packet filtering that can drop millions of packets per second per core.
3. Combining centralized detection (Gatebot) with local enforcement (dosd) provides both global visibility and low-latency mitigation.
4. Layered defenses (L3/L4 + L7) are necessary because attackers adapt when one layer is blocked.

## Further Reading
- [Cloudflare Blog – How Cloudflare Fights DDoS Attacks](https://blog.cloudflare.com/cloudflare-ddos-protection/)
- [Cloudflare Blog – L7 DDoS Protection with Cloudflare](https://blog.cloudflare.com/l7-ddos-protection/)
- [Cloudflare Blog – eBPF, XDP, and the Cloudflare Network](https://blog.cloudflare.com/how-cloudflare-uses-ebpf-xdp/)
