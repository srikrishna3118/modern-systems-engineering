# Case Study: GitHub Code Review at Scale

## Overview

GitHub hosts over 200 million repositories and processes millions of pull requests daily. Its code review system is the backbone of collaborative software development, enabling distributed teams to maintain code quality, enforce standards, and ship reliable software. This case study examines the engineering behind GitHub's pull request and code review infrastructure.

## Key Challenges

- **Scale**: Millions of pull requests opened daily, each requiring diff computation, status checks, and notifications
- **Diff Performance**: Computing and rendering diffs for repositories with millions of files and deep commit histories
- **Merge Conflicts**: Detecting and presenting merge conflicts in near-real-time as branches diverge
- **CI/CD Integration**: Orchestrating thousands of status checks per minute across external and internal CI systems
- **Global Availability**: Maintaining low-latency access for developers worldwide

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Web / API                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│  │ Pull     │  │ Diff Service  │  │ Status Check          │ │
│  │ Request  │  │ (libgit2 /   │  │ Aggregator            │ │
│  │ Service  │  │  dgit)       │  │ (Webhooks + Checks)   │ │
│  └────┬─────┘  └──────┬───────┘  └───────────┬───────────┘ │
│       │               │                      │              │
│  ┌────▼───────────────▼──────────────────────▼───────────┐  │
│  │                  Git Storage Layer                     │  │
│  │          (Spokes — 3-replica Git cluster)              │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐    │
│  │ Notifications│  │ CODEOWNERS │  │ Branch Protection│    │
│  │ Service      │  │ Engine     │  │ Rules Engine     │    │
│  └──────────────┘  └────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Spokes (Git Storage)**: GitHub's distributed Git storage system uses a 3-replica architecture. Every repository is stored on a primary and two replicas. Writes go to the primary and are synchronously replicated before acknowledgment.

2. **Diff Service**: Computes file-level and line-level diffs using an optimized version of `libgit2`. Large diffs are computed asynchronously and cached. The diff service handles:
   - Three-dot diffs (merge-base comparison)
   - File rename detection
   - Binary file identification
   - Whitespace-aware rendering

3. **Pull Request Merge Engine**: Implements multiple merge strategies:
   - Merge commit (default)
   - Squash and merge
   - Rebase and merge
   - Merge queues (serialized testing of PRs in batches)

4. **CODEOWNERS Engine**: Parses `CODEOWNERS` files and maps changed file paths to required reviewers using glob pattern matching. Enforces review requirements via branch protection rules.

5. **Status Checks Aggregator**: Collects results from CI systems (GitHub Actions, external webhooks) and computes a composite pass/fail status. Supports required checks, which gate mergeability.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Ruby (Rails), Go (performance-critical services) |
| Git Storage | Spokes (custom 3-replica cluster), libgit2 |
| Database | MySQL (Vitess sharded), Redis |
| Search | Elasticsearch (code search), Blackbird (new code search) |
| Queue | Kafka, Redis-backed job queues |
| CI/CD | GitHub Actions (runner fleet on Azure) |

## Design Decisions & Trade-offs

### Three-Dot Diff vs Two-Dot Diff
GitHub uses a **three-dot diff** for pull requests, comparing branches from their merge-base rather than the branch tip. This shows only the changes introduced in the PR, not changes merged into the base branch since the PR was created.

### Optimistic Merge Checks
Rather than computing mergeability on every push to the base branch, GitHub uses an optimistic approach: mergeability is computed lazily when the PR page is viewed, and cached until invalidated by a push to either branch.

### Merge Queues
For high-velocity repositories, merge queues batch multiple approved PRs, create a temporary merge of the batch, run CI on the combined result, and only merge if CI passes. This prevents the "semantic conflict" problem where individually-passing PRs break when merged together.

## Lessons Learned

1. **Lazy computation beats eager computation at scale** — Computing diffs and merge status on-demand with caching is far more efficient than pre-computing for every event.

2. **Three-replica synchronous writes ensure durability** — Losing a Git repository is catastrophic; Spokes' 3-replica design tolerates single-node failures without data loss.

3. **Code review is a sociotechnical system** — CODEOWNERS, required reviewers, and branch protection rules encode organizational policies into the development workflow.

4. **Merge queues solve the "last-mile" CI problem** — Testing PRs in isolation is insufficient; merge queues test the combined result before landing code.

5. **Incremental migration is key** — GitHub migrated from a monolithic Ruby application to Go microservices incrementally, extracting performance-critical paths (diff computation, Git operations) first.

## Further Reading

- [GitHub Engineering Blog](https://github.blog/category/engineering/)
- [How We Build GitHub](https://github.blog/2023-02-15-how-we-build-github/)
- [Upgrading GitHub to Ruby 3.2](https://github.blog/2023-04-25-upgrading-github-com-to-ruby-3-2/)
- [The Technology Behind GitHub's New Code Search](https://github.blog/2023-02-06-the-technology-behind-githubs-new-code-search/)
