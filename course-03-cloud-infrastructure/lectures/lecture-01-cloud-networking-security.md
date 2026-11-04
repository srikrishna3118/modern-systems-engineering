# Lecture 1: Cloud Foundations, Networking, and Security

## Overview

A cloud account is someone else's data center plus an API. This lecture covers what that API is actually selling (compute, network, storage, identity) and the two controls that decide whether the account is safe to put a service in: the network path, and who is allowed to call it.

## Topics

### 1. What a cloud provider is selling

AWS, GCP, and Azure use different names for the same four primitives:

- **Compute.** Virtual machines, and the smaller unit of a container you do not patch yourself.
- **Network.** An isolated network (VPC), subnets, routes, and a way in from the internet (load balancer, public IP).
- **Storage.** Block disks for a single machine, object storage for bytes that many machines read, and managed databases.
- **Identity.** A principal (user, role, service account) and a policy that allows specific actions on specific resources.

The provider does not sell reliability. It sells the parts you assemble into a reliability story: more than one machine, more than one availability zone, and a data store that replicates. An availability zone is a data center (or a tight group of them) with independent power and network. A region is a set of zones close enough for synchronous replication and far enough that one fire does not take all of them.

Design default for this curriculum: one region, at least two zones, and no single virtual machine whose death deletes the only copy of state.

### 2. Regions, accounts, and blast radius

Put production and experiments in separate accounts (or projects). A runaway script with permission to delete buckets should not be holding production credentials. Share what must be shared (a container registry, a network) on purpose, through a narrow role, not by reusing one admin key.

Inside an account, a region outage is the failure you are designing for once the service matters. Multi-region is a product decision, covered in [Course 07](../../course-07-advanced-system-design/lectures/lecture-02-global-multi-region.md). Until you have that requirement, two zones and tested backups are the honest design.

### 3. Networking

Draw the path of one request before you open a security group to the world.

```
 internet
    │
    ▼
 load balancer     (public subnet)
    │
    ▼
 application       (private subnet, no public IP)
    │
    ▼
 database          (private subnet, accepts traffic only from the app)
```

- The load balancer is the only thing with a public address.
- Security groups (or firewall rules) are allow-lists on the instance. The database allows the application port from the application group, and nothing else.
- Private subnets reach the internet outbound through a NAT, for package installs and webhooks, without accepting inbound connections.
- DNS names are what clients use. IPs change when you replace a machine. Do not hard-code them.

### 4. Identity is the real perimeter

A private subnet does not help if every pod in the account can read every bucket. The cloud's strong control is IAM:

- Humans get roles they assume, with a time limit, not long-lived access keys on a laptop.
- Each service gets its own role that can do the few actions it needs (`s3:GetObject` on one bucket, not `s3:*`).
- The application does not store a cloud secret. The platform injects the role.

This is the same idea as [zero trust](../../course-07-advanced-system-design/lectures/lecture-05-security-zero-trust.md), applied to the cloud API. "It is inside the VPC" is not an authorization decision.

### 5. Shared responsibility

The provider is responsible for the physical network, the hypervisor, and the durability they document for a managed service. You are responsible for your data, your IAM policies, your guest OS patches if you run VMs, and the application. Object storage will not save you from a bucket policy that says `Principal: *`.

Read the durability and availability numbers for the service you picked, and notice the difference. Availability is "can I reach it." Durability is "is the byte still there after a disk dies." They are not the same SLO.

## Key Takeaways

1. **Compute, network, storage, and identity** are the whole product. Learn them once; the vendor names are a dictionary.
2. **Two zones in one region** is the default availability design. Multi-region is a later, explicit choice.
3. **Only the load balancer is public.** The database accepts traffic from the application and nothing else.
4. **IAM roles, scoped to one service,** are the perimeter that subnets cannot replace.
5. **You own your data and your policies.** The provider owns the hardware.

## Further Reading

- [AWS cell architecture](../../case-studies/aws-cell-architecture.md) — limiting how much of the cloud one failure can take.
- [Lecture 2](lecture-02-iac-kubernetes-serverless-finops.md) — describing this layout in code, and what it costs.
- [Kubernetes lab](../labs/kubernetes-deployment) — the compute primitive you will actually deploy.
