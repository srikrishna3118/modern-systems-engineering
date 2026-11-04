# Lecture 2: Infrastructure as Code, Kubernetes, Serverless, and Cost

## Overview

Clicking through a console does not survive the next incident or the next teammate. This lecture covers describing infrastructure in code, running containers under Kubernetes, knowing when a function is a better fit than a cluster, and reading the bill as an engineering signal.

## Topics

### 1. Infrastructure as code

Terraform (and its equivalents) records the resources you want and computes the changes to get there. The source of truth is the repository, not someone's memory of a console session.

A useful layout:

- **Modules** for one concept (a service and its load balancer, a database and its subnet group).
- **A state file** that remembers what was created, stored remotely, locked so two applies cannot race.
- **Separate states** for network, data, and applications, so a bad application apply cannot destroy the database.
- **Plan, then apply.** Read the plan. A destroy of a database should look shocking in review.

```
  *.tf in git  →  terraform plan  →  review  →  terraform apply  →  cloud API
                       │
                       └── remote state (locked)
```

Two traps. First, importing by hand and then letting the code drift: the next apply will "fix" production back to whatever the file says. Second, secrets in `.tf` files. Pass them in from a secret manager or from the CI environment. The state file contains sensitive values too; lock down who can read it.

The Kubernetes lab is infrastructure as code at the application layer (YAML manifests). Terraform usually owns the cluster itself, the database, and the DNS. Manifests own what runs on the cluster. Do not manage the same object from both.

### 2. Containers and Kubernetes

A container image is the application plus its user-space dependencies, built once and run the same way on a laptop and in the cluster. The image does not include the host kernel, the secret, or the data.

Kubernetes adds the control loop:

- A **Deployment** says "keep N copies of this image running." A node death is handled by starting a replacement. That is the availability mechanism.
- A **Service** is a stable name and address in front of pods whose IPs change.
- **Probes.** Liveness restarts a stuck process. Readiness stops sending traffic to a process that is up but not ready (still loading, or failing its dependency). The [lab](../labs/kubernetes-deployment) wires both.
- **Requests and limits.** Requests are what the scheduler reserves. Limits are the ceiling. A pod with no limit is how one bug starves the node.
- **Rolling updates** start new pods before old ones terminate (`maxUnavailable: 0` when you can afford the extra capacity).

```
  Deployment ──▶ Pods (image, probes, limits)
                    │
                 Service ──▶ stable DNS inside the cluster
                    │
            Ingress / load balancer ──▶ the internet
```

What Kubernetes does not do: it does not replicate your database, and it does not make a single-replica pod highly available. N replicas of a stateless process is the feature. State stays in a managed database or a volume with its own replication story.

### 3. Serverless

A function (Lambda, Cloud Functions, Azure Functions) runs code on demand, scales the number of executions with the number of events, and charges for the time used. It fits work that is event-shaped and intermittent: resize an uploaded image, react to a queue message, run a scheduled cleanup.

It fits badly when:

- You need a long-lived connection (a WebSocket fan-out, a gRPC stream).
- Cold-start latency breaks the budget. A function that has not run recently may take hundreds of milliseconds to start.
- You need a local disk, a GPU, or more than a few minutes of CPU.
- The "function" has quietly become a web service with ten routes. That wants a service, not a pile of handlers sharing a database by accident.

Use serverless at the edges of a system (ingestion, glue, scheduled jobs). Use a service for the request path you have a latency SLO on, unless you have measured the cold start and it is inside the SLO.

### 4. Networking and security, applied

From [Lecture 1](lecture-01-cloud-networking-security.md), the rules that show up in the manifests and the Terraform:

- The load balancer is public. The pods and the database are not.
- The pod's service account can touch its bucket and its queue, and cannot administer the cluster.
- Images come from your registry, pinned by digest when you care about what is actually running.
- Cluster admin credentials are not on developer laptops. CI has a role that can deploy one namespace.

### 5. Cost and FinOps

The bill is a utilization report. Read it as one.

- **Compute waste** is idle replicas and oversized requests. A pod requesting 4 CPU and using 0.2 is paying for 4.
- **Data transfer** is the surprise. Cross-zone and cross-region bytes, and bytes out to the internet, cost more than the disk they sat on. A chatty microservice mesh across zones can cost more than the instances.
- **Storage** grows forever unless lifecycle rules delete or tier old objects. Logs and build artifacts are the usual culprits.
- **Managed services** cost more than software you run yourself and cost less than the engineer who would have run it. Buy the database. Think harder about the data-transfer line.

Tag resources with the service that owns them, or the bill is one number and nobody can act on it. A budget alarm is a production alert. It should page the team that can stop the spend, not a shared inbox.

The [Shopify flash sale](../../case-studies/shopify-flash-sale-scaling.md) case is the cost conversation in the other direction: pre-warming capacity you will need for a known spike is cheaper than failing the spike. Autoscaling that reacts after the traffic arrives is too late for a launch, and leaving that capacity up all month is the FinOps bug.

## Key Takeaways

1. **Terraform plan is a code review.** Remote state, locked, with secrets kept out of the files.
2. **Kubernetes keeps N stateless copies alive.** Probes, requests, and limits are part of the manifest, not an afterthought.
3. **Serverless fits intermittent, event-shaped work.** It is a poor home for long-lived connections and tight latency SLOs you have not measured.
4. **Do not manage the same object from Terraform and from manifests.**
5. **Tag spend, watch data transfer, and alarm on the budget.** Idle capacity and cross-zone bytes are the usual leaks.

## Further Reading

- [Kubernetes orchestration](../../case-studies/kubernetes-orchestration.md)
- [Kubernetes lab](../labs/kubernetes-deployment)
- [AWS cell architecture](../../case-studies/aws-cell-architecture.md)
