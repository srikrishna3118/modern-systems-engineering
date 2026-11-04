# Lecture 5: Security Architecture and Zero Trust

## Overview

Security architecture is the set of decisions about what each component is allowed to believe. The traditional network perimeter trusted anything inside the VPC. That model fails once laptops, CI, third parties, and a compromised pod all sit on "the inside." Zero trust replaces location-based trust with identity checked on every call.

## Topics

### 1. Trust boundaries

Draw the boundary before the protocol. A boundary is any place where data or a request crosses from one authority to another:

- Browser to API gateway
- Gateway to an internal service
- Service to database
- Production to analytics (a common place card data leaks)
- Your network to a payment processor or an identity provider

On each arrow, write what is proven (a user, a service, a device) and what is encrypted. If you cannot name it, the arrow is an implicit allow.

### 2. Zero trust, in operational terms

Zero trust is four habits, not a product:

1. **Authenticate every request**, user and service. A network position is not an identity.
2. **Authorize the specific action** (this subject, this resource, this verb), not "is an employee."
3. **Assume the network is hostile.** Encrypt internal traffic. Segment so a foothold in one service is not a foothold in the database.
4. **Continuously evaluate.** A stolen token should expire. A laptop that falls out of compliance should lose access without waiting for a password rotation.

```
 client                         mesh / gateway                    service
   │  user credential                 │  service identity             │
   │ ───────────────────────────────▶ │ ────────────────────────────▶ │
   │         TLS + short-lived token  │   mTLS, scoped token          │
   │                                  │   policy: subject+action      │
```

Service-to-service calls use a workload identity (SPIFFE-style certificates, or the cloud IAM identity of the pod) with a lifetime measured in hours, not a shared API key baked into an image.

### 3. Identity for users

- **Sessions.** An httpOnly, Secure cookie or a short-lived access token plus a rotating refresh token. Store only a hash of refresh tokens so a database leak does not mint sessions.
- **Passwords.** A slow password hash (Argon2 or bcrypt). Breach detection matters more than an extra character rule.
- **Phishing-resistant second factors** for anything that moves money or changes a payout destination.
- **Least privilege in the token.** A token that can call every API is a stolen skeleton key. Scope it, and keep admin actions on a separate, more tightly logged path.

### 4. Data, not just doors

Authentication does not protect data that has already been copied.

- **Classify.** Card numbers, secrets, and message contents are not the same as a public username.
- **Minimize.** Do not store what you can tokenize. Stripe's model is the reference: the PAN lives in a dedicated vault, and the rest of the platform sees a token. See [Stripe](../../case-studies/stripe-payment-system.md).
- **Encrypt with a purpose.** TLS protects the wire. Disk encryption protects a stolen volume. Application-level encryption, with keys the database role cannot unwrap, protects a stolen database backup. Use the one that matches the threat.
- **Secrets** live in a manager, injected at runtime, rotated, and never committed. A secret in a container image is a secret in every registry mirror.

### 5. Abuse, availability, and audit

Security is also the ability to stay up and to explain what happened.

- **Layer the filters.** Volumetric junk dies at the edge. Application abuse (credential stuffing, card testing) dies at a rate limit and a risk check. [Cloudflare](../../case-studies/cloudflare-ddos-defense.md) is the edge half of this; a [rate limiter](lecture-04-rate-limiting.md) is the application half.
- **Audit the mutations.** Financial and admin actions append an immutable log: who, what, when, from where, and the request id. The log is not the table you update in place.
- **Fail safely.** A dependency timeout on a fraud check should not become an automatic approve. Write down the default for every security decision.

### 6. Supply chain and change

Most large incidents are a trusted path that was too wide: a CI role that can deploy to production, a library update nobody reviewed, an admin token in a laptop shell history.

- Production deploys come from CI identity, not from a developer laptop.
- Separate build, publish, and deploy permissions.
- Pin and review dependencies. A lockfile is a security control.

## Key Takeaways

1. **Draw trust boundaries** and name the identity on each arrow.
2. **Zero trust means authenticate, authorize, encrypt, and expire**, including inside the VPC.
3. **Scope tokens and use workload identity** for service calls. Shared static keys do not survive an incident.
4. **Tokenize and minimize sensitive data** so most services never see it.
5. **Audit mutations and choose a safe default** when a security check cannot run.

## Further Reading

- NIST SP 800-207, *Zero Trust Architecture* — the short definition behind the jargon.
- [Stripe Payment System](../../case-studies/stripe-payment-system.md) — tokenization, idempotency, and audit.
- [Cloudflare DDoS Defense](../../case-studies/cloudflare-ddos-defense.md) — identity is not the only control; the edge still has to shed load.
