# ⚙️ MODULE 3: COMPUTE SERVICES — THE COMPLETE AWS CCP BIBLE

> **Exam:** AWS Certified Cloud Practitioner (CLF-C02) **Module Theme:** How AWS lets you run code and applications — from full-control virtual machines, to serverless functions, to containers, to fully managed platforms — and how to pick the right one for a given business scenario.

---

## 📚 Table of Contents

1. Compute Fundamentals — The Big Picture
2. IaaS vs PaaS vs SaaS
3. Amazon EC2 — Virtual Machines
4. Serverless Computing
5. AWS Lambda
6. Containers — Fundamentals
7. Amazon ECS & EKS
8. AWS Fargate
9. Amazon ECR
10. Edge Locations & CloudFront (Compute-Adjacent)
11. Elastic Beanstalk
12. AWS Batch
13. Amazon Lightsail
14. AWS Outposts
15. Master Comparison Tables
16. Decision Trees
17. Common Exam Questions Bank
18. Quick Reference Cheat Sheet
19. Acronym Cheat Sheet
20. Top 20 Revision Points
21. Common CCP Question Patterns
22. Final Decision Matrix
23. Cross-Links to Related Modules

---

## 1. Compute Fundamentals — The Big Picture

### What Is "Compute" in AWS?

Compute = the CPU + memory resources that run your applications. AWS provides these resources in many shapes; you choose how much control vs how much convenience you want.

**Hinglish Analogy — Restaurant Owner:** Compute = your kitchen. You either:

- Build your own kitchen (on-premises servers)
- Rent a shared kitchen (EC2 — IaaS)
- Order cooked food from someone else's kitchen (Lambda/Fargate — Serverless)
- Get a ready-made tiffin service (SaaS)

### The Core Compute Landscape

```
AWS COMPUTE LANDSCAPE
─────────────────────────────────────────────────────
VIRTUAL MACHINES        CONTAINERS         SERVERLESS
    │                       │                   │
  EC2                    ECS/EKS             Lambda
  Lightsail              Fargate
  Outposts               ECR (registry)
─────────────────────────────────────────────────────
MANAGED PLATFORMS       BATCH PROCESSING
    │                       │
Elastic Beanstalk        AWS Batch
─────────────────────────────────────────────────────
```

**Exam Importance:** ★★★★★ Critical (sets up every other section in this module)

---

## 2. IaaS vs PaaS vs SaaS

> **MUST KNOW for CCP Exam** — a question on this is nearly guaranteed.

### The Control Spectrum

```
MORE CONTROL ◄──────────────────────────────────► LESS CONTROL
    │                    │                              │
  IaaS                 PaaS                           SaaS
(You manage most)  (AWS manages more)         (AWS manages everything)
```

### Detailed Breakdown

|Layer|IaaS|PaaS|SaaS|
|---|---|---|---|
|**Full Form**|Infrastructure as a Service|Platform as a Service|Software as a Service|
|**You manage**|OS, Runtime, App, Data|App, Data|Nothing|
|**AWS manages**|Virtualization, Hardware, Networking|+ OS, Runtime, Middleware|Everything|
|**AWS Example**|EC2|Elastic Beanstalk|Amazon Chime, WorkSpaces|
|**Non-AWS Example**|Rackspace|Heroku, Google App Engine|Gmail, Google Slides, Zoom|
|**Best for**|Full control needed|Developers who don't want infra work|End users|

**Hinglish Analogy:**

- **IaaS** = Plot kharido, ghar khud banao (AWS gives land + bricks, you do the rest)
- **PaaS** = Bare flat lo (walls ready, tum furniture daalo = sirf code likho)
- **SaaS** = Hotel mein rehte ho (sab kuch ready — sirf use karo)

### 🎯 What AWS Is REALLY Testing

AWS isn't testing whether you can define IaaS/PaaS/SaaS. AWS is testing whether you can **map a business need to the correct layer** — a scenario saying "developer wants to focus only on code, no infra work" must trigger PaaS/Elastic Beanstalk in your head, not EC2.

> ⚠️ **EXAM TRAP:** EC2 = IaaS. Elastic Beanstalk = PaaS. Don't confuse "managed service" language with SaaS — Elastic Beanstalk still requires you to write and deploy your own application code, which makes it PaaS, not SaaS.

### 30-Second Revision — IaaS/PaaS/SaaS

| | |
|---|---|
|**Definition**|Cloud service models by how much AWS manages for you|
|**Use Case**|Choosing the right abstraction level for a workload|
|**Alternative**|N/A — these are categories, not competing services|
|**Pricing**|N/A — pricing depends on the specific service chosen|
|**Common Trap**|Calling Elastic Beanstalk "SaaS" because it's managed|
|**Exam Importance**|★★★★★ Critical|

---

## 3. Amazon EC2 — Virtual Machines

### Definition

**Amazon Elastic Compute Cloud (EC2)** = resizable virtual servers (VMs) in the cloud. It is AWS's most fundamental compute service — an IaaS offering.

### Why AWS Provides It

To let customers rent raw, fully configurable compute capacity on demand instead of buying and maintaining physical servers.

### Real-World Problem It Solves

Buying physical servers means large upfront cost, slow provisioning, and wasted capacity when demand is low. EC2 lets you launch a server in minutes and pay only for what you use.

**Hinglish Analogy:** EC2 = renting your own computer in the cloud. You choose the OS, choose the RAM, configure everything your way.

### Key Concepts

|Concept|Meaning|
|---|---|
|**Instance**|A single virtual server|
|**AMI (Amazon Machine Image)**|The instance's blueprint/template (OS + software)|
|**Instance Type**|CPU, RAM, storage configuration (e.g., `t2.micro`)|
|**Security Group**|Virtual firewall for the instance|
|**Key Pair**|Public-private key for SSH login|
|**Elastic IP**|Static public IP address|
|**User Data**|Bootstrap script that runs at instance launch|

### EC2 Instance Type Families (Know the Categories, Not Exact Names)

|Family|Optimized For|Use Case|
|---|---|---|
|**General Purpose** (t, m)|Balance of CPU/RAM/Network|Web servers, small databases|
|**Compute Optimized** (c)|High CPU|Video encoding, gaming servers, ML inference|
|**Memory Optimized** (r, x)|High RAM|In-memory databases, real-time analytics|
|**Storage Optimized** (i, d)|High disk I/O|Data warehousing, distributed file systems|
|**Accelerated Computing** (p, g, inf)|GPU/FPGA|ML training, graphics rendering|

> ⚠️ **EXAM TIP:** You don't need to memorize exact instance type names — just understand which _family category_ fits which use case.

### EC2 Pricing Models

> **MUST KNOW** — this topic appears very frequently on the exam.

|Pricing Model|How It Works|Savings|Best For|
|---|---|---|---|
|**On-Demand**|Pay per hour/second, no commitment|0% (baseline)|Unpredictable workloads, testing|
|**Reserved Instances**|1 or 3 year commitment|Up to 72%|Steady-state, predictable workloads|
|**Savings Plans**|Commit to $/hour for 1-3 years|Up to 66%|Flexible, can change instance type|
|**Spot Instances**|Bid on unused EC2 capacity|Up to 90%|Fault-tolerant, flexible, batch jobs|
|**Dedicated Hosts**|Physical server reserved for you|Varies|Compliance/licensing requirements|

**Hinglish Analogy (Pricing):**

- **On-Demand** = Ola/Uber — jab chahiye tab lo. Mehenga but no commitment.
- **Reserved** = Monthly bus pass — advance pay karo, discount milega.
- **Savings Plans** = Flexible bus pass — monthly spend commit karo, koi bhi bus/route le sako.
- **Spot** = Standby flight ticket — bahut sasta, but AWS kabhi bhi wapas le sakta hai.
- **Dedicated Host** = Apni private car (sirf tumhari car road pe) — compliance ke liye.

> ⚠️ **EXAM TRAP:** Spot Instances are for **fault-tolerant** workloads only. If AWS reclaims the instance, the application must not crash. Never use Spot for critical databases or stateful, non-resumable jobs.

### EC2 Auto Scaling

- Automatically increases/decreases EC2 instance count based on demand.
- Works with **Elastic Load Balancing (ELB)**.
- **Scale Out** = add instances (demand up). **Scale In** = remove instances (demand down).

```
Traffic Up   ──► Auto Scaling ──► New instances launch
Traffic Down ──► Auto Scaling ──► Extra instances terminate
```

> ⚠️ **EXAM TIP:** Auto Scaling = elasticity, a core AWS benefit. "Automatically handles traffic spikes" in a question → Auto Scaling.

### Elastic Load Balancing (ELB)

- Distributes incoming traffic across multiple EC2 instances.
- Acts as the **single point of contact** for clients.
- Works with Auto Scaling to achieve high availability.

```
User Requests
     │
     ▼
Elastic Load Balancer
     │
  ┌──┼──┐
  ▼  ▼  ▼
EC2 EC2 EC2
(distributed load)
```

### When to Use EC2

Full control over OS/runtime, long-running or unpredictable workloads, legacy applications needing specific configurations, or when no managed alternative fits the need.

### When NOT to Use EC2

Short event-driven tasks (use Lambda), containerized microservices where you don't want server management (use Fargate), simple low-traffic websites (use Lightsail).

### Security Considerations

- Security Groups act as a stateful virtual firewall attached to the instance.
- Key Pairs control SSH access — never share private keys.
- IAM roles (not hardcoded credentials) should be attached to instances for AWS API access.

### Real Scenario

A bank running a legacy core-banking application that needs a specific OS version and full network control deploys it on EC2 with Reserved Instances for predictable, discounted long-term cost.

### 🎯 What AWS Is REALLY Testing

AWS isn't testing whether you know EC2 is a virtual machine. AWS is testing whether you know **when EC2 is the better choice vs Lambda, Fargate, or Elastic Beanstalk** — i.e., whether the scenario calls for full control and long-running processes vs convenience and automatic scaling.

### 30-Second Revision — EC2

| | |
|---|---|
|**Definition**|Virtual servers in the cloud, full user control|
|**Use Case**|Long-running, customizable, unpredictable-duration workloads|
|**Alternative**|Lambda (short/event-driven), Fargate (containers, no server mgmt)|
|**Pricing**|On-Demand, Reserved, Savings Plans, Spot, Dedicated Hosts|
|**Common Trap**|Using Spot for critical, non-interruptible workloads|
|**Exam Importance**|★★★★★ Critical|

---

## 4. Serverless Computing

### Definition

Serverless = servers still exist, but you never have to think about them — AWS provisions, scales, patches, and maintains them for you.

**Hinglish Analogy:** Electricity supply — plug in and current flows. You don't need to know how the power plant works. Same with serverless — run your code, AWS handles the infrastructure.

### Serverless vs Traditional (EC2)

|Traditional (EC2)|Serverless (Lambda)|
|---|---|
|You provision the server|No server provisioning worry|
|You install/patch the OS|AWS patches everything|
|You scale manually/configure Auto Scaling|Auto scales by default|
|You pay even during idle time|Pay only when code runs|
|You manage availability|AWS manages availability|

### 🎯 What AWS Is REALLY Testing

AWS is testing whether you understand serverless is **not one service** — it's a category. Both Lambda (functions) and Fargate (containers) are serverless. A common trap is assuming "serverless" means only Lambda.

**Exam Importance:** ★★★★★ Critical

---

## 5. AWS Lambda

### Definition

**AWS Lambda** = AWS's primary serverless compute service. Your code runs in response to events — without managing any server.

**Hinglish Analogy:** A motion-sensor light at home — someone arrives (event), light turns on (function runs). No one arrives, light stays off, no electricity wasted. Same with Lambda — trigger comes, code runs; no trigger, zero cost.

### How Lambda Works

```
1. Code Upload ──► Into a Lambda Function
       │
2. Trigger ──────► Set an event source (API call, S3 upload, etc.)
       │
3. Event Fires ──► AWS automatically runs your code
       │
4. Scale ────────► Thousands of requests? Lambda scales automatically
       │
5. Pay ──────────► Only for execution time
```

### Lambda Triggers (Event Sources)

|Trigger Type|Example|
|---|---|
|**HTTP Request**|API Gateway → Lambda|
|**File Upload**|S3 bucket upload → Lambda|
|**Database Change**|DynamoDB Stream → Lambda|
|**Schedule**|CloudWatch Events (cron) → Lambda|
|**Message Queue**|SQS/SNS → Lambda|

**Real Scenario:** Instagram-style photo upload → S3 trigger → Lambda function → auto-resize image and generate thumbnail.

### Lambda Key Facts (MUST KNOW)

|Feature|Detail|
|---|---|
|**Max Execution Time**|**15 minutes (900 seconds)** — critical limit|
|**Languages Supported**|Python, Node.js, Java, C#, Go, Ruby, PowerShell|
|**Custom Runtime**|Any language, via Lambda Layers|
|**Pricing**|Per request + per 100ms of execution time|
|**Free Tier**|1 million requests/month + 400,000 GB-seconds free|
|**Scaling**|Automatic, supports concurrent executions|
|**Managed by AWS**|Patching, security, infrastructure — all AWS|

> ⚠️ **EXAM CRITICAL:** If code runs **longer than 15 minutes**, do NOT use Lambda. Use EC2 or AWS Batch instead.

### Lambda Pricing (Simplified)

- **Pay for:** number of requests + duration (rounded to nearest 1ms)
- **Never pay for:** idle time, provisioning, patching
- Cheapest option for low-frequency or bursty workloads.

### Lambda vs EC2

| |Lambda|EC2|
|---|---|---|
|**Server Management**|AWS does it|You do it|
|**Scaling**|Automatic|Manual/Auto Scaling|
|**Cost Model**|Pay per invocation|Pay per hour (even idle)|
|**Max Runtime**|15 min|Unlimited|
|**Best for**|Short, event-driven tasks|Long-running, heavy workloads|

> ⚠️ **EXAM TIP:** Keywords "event-driven", "no server management", "pay only when runs" → **Lambda**.

### When to Use / When NOT to Use

- **Use:** short bursts of code triggered by events, APIs, file processing, glue logic between services.
- **NOT for:** long-running jobs (>15 min), stateful applications, or heavy batch processing — use AWS Batch or EC2 instead.

### 🎯 What AWS Is REALLY Testing

AWS is testing whether you can spot the **15-minute ceiling** as the deciding factor between Lambda and AWS Batch/EC2 in scenario questions — this is one of the single most repeated traps in the whole Compute domain.

### 30-Second Revision — Lambda

| | |
|---|---|
|**Definition**|Event-driven serverless function execution|
|**Use Case**|Short, event-triggered tasks (image resize, API backend)|
|**Alternative**|AWS Batch/EC2 for jobs longer than 15 minutes|
|**Pricing**|Per request + per 100ms execution time; generous free tier|
|**Common Trap**|Using Lambda for jobs that exceed 15 minutes|
|**Exam Importance**|★★★★★ Critical|

---

## 6. Containers — Fundamentals

### Definition

A container = a lightweight, portable environment packaging an application with all its dependencies.

**Hinglish Analogy:** Shipping containers — standard size, fits on any ship/truck. Similarly, a Docker container runs on any machine with a container engine.

### Container vs Virtual Machine

```
VIRTUAL MACHINE                    CONTAINER
────────────────────               ────────────────────
┌──────────┐                      ┌──────┐ ┌──────┐
│  App A   │                      │App A │ │App B │
├──────────┤                      ├──────┤ ├──────┤
│Guest OS  │ ← Full OS install    │Libs  │ │Libs  │
├──────────┤   (GBs of space)     └──┬───┘ └──┬───┘
│Hypervisor│                         │ Container Engine
├──────────┤                         │ (Docker)
│Host OS   │                      ┌──┴───────┐
├──────────┤                      │  Host OS │
│ Hardware │                      └──────────┘
└──────────┘
Heavy (GBs, minutes to start)    Light (MBs, seconds to start)
```

### Container Key Points

|Feature|Container|
|---|---|
|**Size**|Megabytes (much smaller than VMs)|
|**Startup Time**|Seconds (vs minutes for VMs)|
|**Isolation**|Process-level (shares host OS kernel)|
|**Portability**|Runs anywhere Docker runs|
|**Scaling**|Very fast to scale|

### Container Image vs Container

- **Image** = read-only template/blueprint — like an AMI for VMs.
- **Container** = a running instance of an image — like an EC2 instance.

**Hinglish Analogy:** Image = recipe, Container = the baked cake.

### Why Containers?

- Works the same on dev machine and production (consistency)
- Fast deploy, fast scale
- Ideal for microservices architecture

**Exam Importance:** ★★★★☆ Very Common

---

## 7. Amazon ECS & EKS

### The Problem: Container Orchestration

Running one container is easy. Managing hundreds is hard — which are running, what happens on crash, how to scale with traffic. **Container orchestration** solves this.

### AWS ECS — Elastic Container Service

**Definition:** AWS's managed, AWS-native container orchestration service.

|Feature|Detail|
|---|---|
|**Type**|AWS-proprietary|
|**Complexity**|Simpler|
|**Integration**|Deep AWS integration (IAM, ALB, CloudWatch)|
|**Control**|You define tasks; ECS manages the rest|
|**Good for**|Teams already on AWS, simpler setups|

**Hinglish Analogy:** ECS = company's own HR department — works by AWS's rules, deeply integrated, simpler.

### AWS EKS — Elastic Kubernetes Service

**Definition:** AWS's managed **Kubernetes** service — Kubernetes itself is open-source.

|Feature|Detail|
|---|---|
|**Type**|Open-source (Kubernetes)|
|**Complexity**|More complex|
|**Portability**|Kubernetes standard → switch cloud easily|
|**Control**|Maximum flexibility|
|**Good for**|Existing Kubernetes users, multi-cloud, complex setups|

**Hinglish Analogy:** EKS = hiring a universal contractor — open standard, works anywhere, more complex to manage.

### ECS vs EKS — Quick Comparison

|                 | ECS               | EKS                           |
| --------------- | ----------------- | ----------------------------- |
| **Technology**  | AWS-native        | Kubernetes (open source)      |
| **Complexity**  | Simpler           | More complex                  |
| **Flexibility** | Less              | More                          |
| **Cost**        | No Kubernetes fee | EKS cluster fee + EC2/Fargate |
| **Portability** | AWS-locked        | Portable across clouds        |
| **Best for**    | AWS-native apps   | Kubernetes users, enterprise  |

> ⚠️ **EXAM TIP:** "Kubernetes" keyword → EKS. "Simpler, AWS-native orchestration" → ECS.

### 🎯 What AWS Is REALLY Testing

AWS is testing whether you know ECS ≠ Kubernetes. This is a very common trap — people assume ECS "is" Kubernetes because both orchestrate containers.

### 30-Second Revision — ECS/EKS

| | |
|---|---|
|**Definition**|Container orchestration services (AWS-native vs Kubernetes)|
|**Use Case**|Managing many containers reliably at scale|
|**Alternative**|Each other, depending on Kubernetes requirement|
|**Pricing**|ECS: pay for compute only; EKS: + cluster fee|
|**Common Trap**|Thinking ECS = Kubernetes|
|**Exam Importance**|★★★★☆ Very Common|

---

## 8. AWS Fargate

### Definition

**AWS Fargate** = a serverless compute _engine_ for containers — works with both ECS and EKS. With Fargate, you never manage EC2 instances; you just define containers.

### Fargate vs EC2 (as the launch type for containers)

| |EC2 Launch Type|Fargate Launch Type|
|---|---|---|
|**You manage**|EC2 instances, OS, patching|Nothing (serverless)|
|**Control**|Full|Less|
|**Cost**|Pay for EC2 instance|Pay per container resources|
|**Scaling**|Manual/Auto Scaling groups|Automatic|
|**Best for**|Full control needed|Dev teams wanting simplicity|

**Hinglish Analogy:**

- **ECS/EKS + EC2** = build your own kitchen and cook in it
- **ECS/EKS + Fargate** = use a cloud kitchen — you give the recipe, kitchen management is someone else's job

> ⚠️ **EXAM TIP:** "No server management for containers" or "serverless containers" → **Fargate**.

> ⚠️ **EXAM TRAP:** Fargate does **not replace** ECS/EKS — Fargate is the compute engine, ECS/EKS is the orchestrator. They work together, not as alternatives to each other.

### 🎯 What AWS Is REALLY Testing

AWS is testing whether you understand Fargate answers the question "who manages the servers under my containers?" — not "how are my containers orchestrated?" (that's ECS/EKS's job).

### 30-Second Revision — Fargate

|                     |                                               |
| ------------------- | --------------------------------------------- |
| **Definition**      | Serverless compute engine for containers      |
| **Use Case**        | Run containers without managing EC2 instances |
| **Alternative**     | EC2 launch type (for full control)            |
| **Pricing**         | Pay per vCPU/memory used by containers        |
| **Common Trap**     | Thinking Fargate replaces ECS/EKS             |
| **Exam Importance** | ★★★★☆ Very Common                             |

---

## 9. Amazon ECR

### Definition

**Amazon Elastic Container Registry (ECR)** = AWS's private Docker image registry for storing, managing, and deploying container images.

Think of it as: **DockerHub's AWS version** — private, and securely integrated with ECS/EKS.

### The Full Container Workflow

```
                    WHERE DO IMAGES COME FROM?
                           │
                    ┌──────▼──────┐
                    │  Amazon ECR │ ◄── Push your container images here
                    │  (Registry) │
                    └──────┬──────┘
                           │ Pull image
              WHO MANAGES ORCHESTRATION?
          ┌────────────────┴────────────────┐
          ▼                                 ▼
    ┌───────────┐                   ┌───────────┐
    │  AWS ECS  │                   │  AWS EKS  │
    │(AWS-native│                   │(Kubernetes│
    │   mgmt)   │                   │  mgmt)    │
    └─────┬─────┘                   └─────┬─────┘
          │        WHERE DOES IT RUN?     │
          └──────────────┬────────────────┘
                   ┌─────┴─────┐
                   ▼           ▼
              ┌────────┐  ┌─────────┐
              │ AWS EC2│  │ Fargate │
              │(You    │  │(Server- │
              │manage) │  │ less)   │
              └────────┘  └─────────┘
```

> ⚠️ **EXAM TRAP:** ECR = store the image. ECS/EKS = run the image. Two completely different roles — don't mix them up.

### 30-Second Revision — ECR

| | |
|---|---|
|**Definition**|Private Docker image registry|
|**Use Case**|Securely store/manage container images before deployment|
|**Alternative**|DockerHub (public, non-AWS-native)|
|**Pricing**|Pay for storage + data transfer|
|**Common Trap**|Confusing ECR (storage) with ECS/EKS (execution)|
|**Exam Importance**|★★★☆☆ Good to Know|

---

## 10. Edge Locations & CloudFront (Compute-Adjacent)

> Not strictly "compute," but tested heavily alongside this module because it affects application delivery architecture decisions.

### The Problem: Latency for Global Users

If your server is in Mumbai and a user accesses it from New York, the request is slow. Distance = Latency.

### Amazon CloudFront — CDN

**Definition:** AWS's Content Delivery Network (CDN) — delivers content globally with low latency by caching it near users.

**Hinglish Analogy:** A nationwide retail chain's warehouse network — content is copied to the location nearest the user. The user doesn't know where the content actually came from, but it's much faster.

### How CloudFront Works

```
ORIGIN SERVER               EDGE NETWORK                USER
(Actual Content)                                     (End User)
      │                                                   │
  ┌───┴──────┐     ┌──────────────────┐    ┌─────────────┴────┐
  │ S3 Bucket│     │  Regional Edge   │    │  Edge Location   │
  │ EC2/ALB  │◄────│  Cache           │◄───│  (Closest to     │
  │ Custom   │     │  (Less-popular   │    │   user)          │
  │ Origin   │     │  Content)        │    │  Popular Content  │
  └──────────┘     └──────────────────┘    └──────────────────┘

Actual datacenter       Middle tier               Nearest PoP
```

### Three-Tier Flow

|Tier|What's Stored|Speed|
|---|---|---|
|**Edge Location**|Popular/frequently accessed content|Fastest (nearest to user)|
|**Regional Edge Cache**|Less popular content (bigger cache)|Medium|
|**Origin**|All content (source of truth)|Slowest (actual server)|

**Flow:** User → Edge Location → (cache miss) Regional Edge Cache → (still miss) Origin.

### Edge Locations vs AZs vs Regions

| |Regions|Availability Zones (AZs)|Edge Locations|
|---|---|---|---|
|**Purpose**|Geographically separate data center clusters|Physical data centers within a Region|Content caching points|
|**Count**|~30+ Regions|Multiple per Region|400+ worldwide|
|**What runs here**|All AWS services|EC2, RDS, S3, etc.|CloudFront, Route 53|
|**Capability**|Full compute|Full compute|Cache only|

> ⚠️ **EXAM TIP:** Edge Locations > AZs > Regions in count. Edge Locations are **NOT** full data centers.

### AWS Global Accelerator (Bonus)

- Routes traffic through AWS's global network (not the public internet).
- Improves performance for non-cacheable, dynamic content (APIs).
- Complements CloudFront — for content that can't simply be cached.

| |CloudFront|Global Accelerator|
|---|---|---|
|**Best for**|Static content, media|Dynamic content, APIs|
|**Caching**|Yes|No|
|**Performance mechanism**|CDN caching|AWS network routing|

**Exam Importance:** ★★★★☆ Very Common (also covered in Module 4 — Going Global)

---

## 11. Elastic Beanstalk

### Definition

**AWS Elastic Beanstalk** = a managed PaaS that automatically deploys, manages, and scales your application. Your job: just upload the code.

**Hinglish Analogy:** A furnished apartment — everything ready (infrastructure), you just bring your own belongings (code).

### How It Works

```
Developer ──► Code Upload ──► Elastic Beanstalk
                                      │
                         Auto handles:
                         ✓ EC2 provisioning
                         ✓ Load Balancer setup
                         ✓ Auto Scaling config
                         ✓ Health monitoring
                         ✓ Application deployment
```

### Key Features

|Feature|Detail|
|---|---|
|**Type**|PaaS — you manage app + data, AWS manages the rest|
|**Languages**|Java, .NET, Python, Node.js, Ruby, Go, Docker|
|**Underlying Resources**|Still uses EC2, ALB, Auto Scaling (managed for you)|
|**Control**|You still have access to the underlying AWS resources|
|**Cost**|Pay only for underlying resources — no extra Beanstalk fee|

> ⚠️ **EXAM TIP:** "Developer wants to focus only on code, doesn't want to manage infra" → Elastic Beanstalk. Beanstalk itself is free; you pay for underlying EC2/ALB/etc.

### Beanstalk vs EC2 vs Lambda

| |Lambda|Elastic Beanstalk|EC2|
|---|---|---|---|
|**Control**|Least|Medium|Most|
|**Management**|Zero|Minimal|Full|
|**Scaling**|Auto|Auto|Manual/Auto Scaling|
|**Runtime limit**|15 min|No limit|No limit|
|**Best for**|Short event-driven|Web apps, APIs|Full custom control|

### 🎯 What AWS Is REALLY Testing

AWS is testing whether you know Elastic Beanstalk is a **deployment/orchestration layer on top of EC2** — not a separate compute type. It's still "your infrastructure," just automated.

### 30-Second Revision — Elastic Beanstalk

| | |
|---|---|
|**Definition**|PaaS for automated app deployment and scaling|
|**Use Case**|Deploying web apps/APIs without manual infra setup|
|**Alternative**|EC2 (full control), Lambda (event-driven, short tasks)|
|**Pricing**|Free service; pay for underlying resources only|
|**Common Trap**|Thinking Beanstalk has its own separate infra cost|
|**Exam Importance**|★★★★☆ Very Common|

---

## 12. AWS Batch

### Definition

**AWS Batch** = a managed service for running large-scale batch computing workloads. It automatically schedules and manages compute resources for batch jobs.

**Hinglish Analogy:** A factory manufacturing 10,000 products at once instead of one at a time — batch processing means processing all the data together, in parallel.

### Key Characteristics

|Feature|Detail|
|---|---|
|**Workload Type**|Batch (not real-time/event-driven)|
|**Scaling**|Auto scales based on job queue|
|**Infrastructure**|Managed by AWS|
|**Parallelism**|Yes — multiple jobs run simultaneously|
|**Integration**|Uses EC2 and Fargate launch types under the hood|

### Use Cases

- Scientific computing (genomics research, simulations)
- Financial risk analysis
- Media transcoding (overnight video rendering)
- ML model training on large datasets
- Log processing (millions of log files)

### Batch vs Lambda

| |Lambda|AWS Batch|
|---|---|---|
|**Duration**|Max 15 min|Unlimited|
|**Trigger**|Event-driven|Job queue|
|**Scale**|Concurrent invocations|Parallel batch jobs|
|**Best for**|Short, fast tasks|Long, large-scale jobs|

> ⚠️ **EXAM TIP:** "Large scale", "parallel processing", "batch jobs", "overnight processing" → AWS Batch. Not Lambda — Lambda has the 15-minute ceiling.

### 30-Second Revision — AWS Batch

| | |
|---|---|
|**Definition**|Managed service for large-scale, parallel batch jobs|
|**Use Case**|Long-running or scheduled bulk data processing|
|**Alternative**|Lambda (short tasks), EC2 (manual control)|
|**Pricing**|Pay for underlying EC2/Fargate compute used|
|**Common Trap**|Trying to force a 4-hour job into Lambda|
|**Exam Importance**|★★★★☆ Very Common|

---

## 13. Amazon Lightsail

### Definition

**Amazon Lightsail** = a simplified cloud service for small businesses, developers, and beginners — virtual servers (VPS), storage, databases, and networking at a **fixed monthly price**.

**Hinglish Analogy:** AWS's "beginner mode" — like a smartphone's "easy mode" that hides complex settings and gives a simple interface.

### Key Features

|Feature|Detail|
|---|---|
|**Pricing**|Predictable flat monthly rate|
|**Complexity**|Very simple — no complex AWS console|
|**Resources**|VPS, managed databases, object storage, CDN|
|**Best for**|Blogs, small websites, dev/test, learning AWS|

### Lightsail vs EC2

| |Lightsail|EC2|
|---|---|---|
|**Complexity**|Simple — beginner-friendly console|Complex — full AWS console|
|**Pricing**|Fixed monthly (predictable)|Variable — per hour/second|
|**Customization**|Limited (pre-configured bundles)|Extensive — instance types, networking, storage|
|**Scaling**|Manual only (limited)|Full Auto Scaling + Load Balancing|
|**Networking**|Basic (built-in firewall)|Advanced — VPC, subnets, security groups|
|**OS/Software**|Pre-built blueprints (LAMP, WordPress)|Any AMI — full control|
|**AWS ecosystem integration**|Limited|Deep integration with all AWS services|
|**Best for**|Blogs, small sites, dev/test, learning AWS|Any serious production workload|
|**Migrate to EC2?**|Yes — when you outgrow Lightsail|N/A|

> ⚠️ **EXAM TIP:** "Simple", "small business", "low-traffic website", "predictable pricing", "beginners" → **Lightsail**.

### 30-Second Revision — Lightsail

| | |
|---|---|
|**Definition**|Simplified VPS with fixed monthly pricing|
|**Use Case**|Small websites, blogs, learning AWS, dev/test|
|**Alternative**|EC2 (for production-scale, full-control needs)|
|**Pricing**|Fixed monthly bundle price|
|**Common Trap**|Assuming Lightsail has full EC2 capabilities|
|**Exam Importance**|★★★☆☆ Good to Know|

---

## 14. AWS Outposts

### Definition

**AWS Outposts** = AWS-managed physical hardware installed in your own on-premises data center — bringing the AWS cloud experience to your building.

**Hinglish Analogy:** A pizza outlet normally cooks in its own kitchen and delivers. Outposts means AWS installs its own kitchen and staff inside _your_ building, but AWS still manages it — you get the AWS experience, on-premises.

### Key Features

|Feature|Detail|
|---|---|
|**Physical Hardware**|AWS-managed racks installed at your site|
|**Consistency**|Same AWS APIs, tools, and services on-premises|
|**Connectivity**|Connected to an AWS Region (hybrid)|
|**Latency**|Ultra-low — hardware is physically near you|
|**Management**|AWS manages the hardware|

### Why Use Outposts?

|Reason|Explanation|
|---|---|
|**Low Latency**|Manufacturing plants, trading systems needing <1ms latency|
|**Data Residency**|Government/healthcare — data must stay in-country|
|**Offline Operations**|Remote sites with limited internet (oil rigs, mining)|
|**Legacy Migration**|Gradually migrate on-premises workloads to cloud|
|**Compliance**|Regulatory requirements to keep data local|

### Hybrid Cloud Options (Related Services)

|Service|What It Does|
|---|---|
|**AWS Outposts**|AWS hardware at your site|
|**AWS Storage Gateway**|Connects on-premises to AWS storage|
|**AWS Direct Connect**|Dedicated network connection to AWS|
|**AWS VPN**|Encrypted tunnel to AWS over the internet|

> ⚠️ **EXAM TIP:** "On-premises", "low latency", "data residency", "hybrid cloud", "regulatory data location compliance" → **AWS Outposts**.

### 30-Second Revision — Outposts

| | |
|---|---|
|**Definition**|AWS-managed hardware installed at your physical site|
|**Use Case**|Hybrid cloud, ultra-low latency, data residency|
|**Alternative**|Direct Connect/VPN (network link, not physical hardware)|
|**Pricing**|Hardware + service fees|
|**Common Trap**|Thinking Outposts is a purely virtual/remote service|
|**Exam Importance**|★★★★☆ Very Common|

---

## 15. Master Comparison Tables

### 15.1 All Compute Services — At a Glance

|Service|Type|Server Management|Scaling|Duration Limit|Cost Model|
|---|---|---|---|---|---|
|**EC2**|VM|You manage|Auto Scaling|Unlimited|Per hour|
|**Lambda**|Serverless function|AWS manages|Automatic|15 minutes|Per request|
|**Elastic Beanstalk**|PaaS|AWS manages|Auto|Unlimited|Underlying resources|
|**ECS**|Container orchestration|You/Fargate|Auto|Unlimited|EC2 or Fargate|
|**EKS**|Kubernetes|You/Fargate|Auto|Unlimited|EC2 or Fargate + cluster fee|
|**Fargate**|Serverless containers|AWS manages|Auto|Unlimited|Per vCPU/memory|
|**AWS Batch**|Batch processing|AWS manages|Auto|Unlimited|Per EC2/Fargate used|
|**Lightsail**|Simplified VPS|AWS manages|Limited|Unlimited|Fixed monthly|
|**Outposts**|On-premises cloud|AWS manages|Manual|Unlimited|Hardware + service fees|

### 15.2 Container Orchestration Choices

| |ECS + EC2|ECS + Fargate|EKS + EC2|EKS + Fargate|
|---|---|---|---|---|
|**Kubernetes**|No|No|Yes|Yes|
|**Server management**|You|AWS|You|AWS|
|**Complexity**|Medium|Low|High|Medium|
|**Best for**|AWS teams needing control|Simpler serverless containers|Kubernetes + control|Kubernetes + serverless|

### 15.3 EC2 vs Lambda vs Fargate vs Elastic Beanstalk

| |EC2|Lambda|Fargate|Elastic Beanstalk|
|---|---|---|---|---|
|**Model**|IaaS|Serverless function|Serverless container|PaaS|
|**You manage**|OS + app|Just code|Just container|Just app code|
|**Runtime limit**|None|15 min|None|None|
|**Best for**|Full control|Event-driven, short tasks|Containers, no server mgmt|Deploy app, no infra work|

---

## 16. Decision Trees

### 16.1 Which Compute Service Should I Use?

```
START: What kind of workload?
            │
    ┌───────┼────────────┐
    ▼       ▼            ▼
EVENT-    CONTAINERS   TRADITIONAL
DRIVEN    /MICRO-      APP/SERVER
    │     SERVICES         │
    ▼         │            │
AWS Lambda    │        Want full
(< 15 min)    │        control?
              │         ┌──┴──┐
         Need server    │     │
         management?   YES    NO
          ┌───┴───┐    │     │
          │       │    ▼     ▼
         NO      YES   EC2  Elastic
          │       │        Beanstalk
          ▼       ▼
       Fargate  EC2 +
               ECS/EKS

SPECIAL CASES:
├── Batch/long-running jobs → AWS Batch
├── Simple website/small biz → Lightsail
├── On-premises + AWS needed → Outposts
└── Global fast content delivery → CloudFront
```

### 16.2 Serverless or Not?

```
Need compute?
   │
   ▼
Is it a short, event-triggered task (< 15 min)?
   │
  YES ──► Lambda
   │
  NO
   │
   ▼
Is it containerized and you don't want to manage servers?
   │
  YES ──► Fargate (with ECS or EKS)
   │
  NO
   │
   ▼
Need full VM control?
   │
  YES ──► EC2
```

---

## 17. Common Exam Questions Bank

**Q1:** A developer wants to run code without managing any servers. The code runs for 30 seconds triggered by an API call. Which service? **A:** AWS Lambda — serverless, event-driven, < 15 min ✅

**Q2:** A company has a code execution job that takes 4 hours to complete and runs every night. Which service? **A:** AWS Batch — long-running batch job, > 15 minutes ✅ (Not Lambda!)

**Q3:** A startup wants to deploy their Python web app on AWS without managing EC2, load balancers, or auto scaling manually. Which service? **A:** AWS Elastic Beanstalk — PaaS, automated deployment ✅

**Q4:** A company needs to run containers on AWS without managing underlying servers. Which combination? **A:** ECS or EKS + **AWS Fargate** ✅

**Q5:** A government organization must keep all data within India due to compliance. They want AWS services. What should they use? **A:** AWS Outposts — on-premises, data residency compliance ✅

**Q6:** A video streaming company wants to reduce latency for global users. Which service? **A:** Amazon CloudFront (Edge Locations) ✅

**Q7:** A small business owner wants a simple, affordable, predictable-price virtual server for their blog. Which service? **A:** Amazon Lightsail ✅

**Q8:** A company already uses Kubernetes and wants to run it on AWS with maximum flexibility. Which service? **A:** Amazon EKS ✅

**Q9:** Which pricing model gives up to 90% discount on EC2 but can be interrupted? **A:** Spot Instances ✅

**Q10:** What is the maximum execution time for an AWS Lambda function? **A:** 15 minutes (900 seconds) ✅

**Q11:** Which layer of the cloud model gives you the most control? **A:** IaaS (Infrastructure as a Service) — example: EC2 ✅

**Q12:** A factory has machines that need < 1ms response time from cloud services and unreliable full internet connectivity. Which service? **A:** AWS Outposts ✅

**Q13:** What is the difference between an AMI and an EC2 instance? **A:** AMI is the template/blueprint; EC2 instance is the running virtual machine created from that AMI ✅

**Q14:** Which service automatically distributes incoming traffic across multiple EC2 instances? **A:** Elastic Load Balancing (ELB) ✅

**Q15:** A company needs to store and manage their Docker container images privately on AWS. Which service? **A:** Amazon Elastic Container Registry (ECR) ✅

---

## 18. Quick Reference Cheat Sheet

|Service|One-Line Summary|Key Differentiator|CCP Exam Keyword|
|---|---|---|---|
|**EC2**|Virtual servers on AWS|Full control, IaaS|"Virtual machine", "full control"|
|**AWS Lambda**|Run code without servers|Event-driven, < 15 min, pay per use|"Serverless", "event-driven", "no servers"|
|**Elastic Beanstalk**|Auto-deploy web apps|PaaS, dev just uploads code|"Just deploy code", "no infra management"|
|**ECS**|AWS-native container orchestration|Simpler, AWS integrated|"Containers", "AWS-native orchestration"|
|**EKS**|Kubernetes on AWS|Open-source, portable, complex|"Kubernetes"|
|**Fargate**|Serverless compute for containers|No EC2 management needed|"Serverless containers"|
|**ECR**|Private Docker image registry|Store/manage container images|"Container images", "Docker registry"|
|**AWS Batch**|Large-scale batch job processing|Long-running, parallel jobs|"Batch", "large-scale processing", "overnight jobs"|
|**Lightsail**|Simplified cloud for beginners|Fixed price, simple VPS|"Simple", "predictable price", "small business"|
|**Outposts**|AWS hardware at your site|On-premises + cloud consistency|"On-premises", "data residency", "hybrid cloud"|
|**CloudFront**|Global CDN for fast content delivery|Edge caching, low latency|"Fast delivery globally", "CDN", "edge"|
|**Auto Scaling**|Automatically adjusts EC2 count|Elasticity, handles traffic spikes|"Automatically scale", "traffic spikes"|
|**ELB**|Distributes traffic across instances|High availability|"Load balancer", "distribute traffic"|

---

## 19. Acronym Cheat Sheet

|Acronym|Full Form|What It Does|
|---|---|---|
|**EC2**|Elastic Compute Cloud|Virtual machines|
|**AMI**|Amazon Machine Image|VM template/blueprint|
|**ECS**|Elastic Container Service|AWS container orchestration|
|**EKS**|Elastic Kubernetes Service|Kubernetes on AWS|
|**ECR**|Elastic Container Registry|Docker image registry|
|**ELB**|Elastic Load Balancer|Traffic distribution|
|**CDN**|Content Delivery Network|Global content caching (CloudFront)|
|**VPS**|Virtual Private Server|Simple virtual machine (Lightsail)|
|**IaaS**|Infrastructure as a Service|EC2, raw compute|
|**PaaS**|Platform as a Service|Elastic Beanstalk|
|**SaaS**|Software as a Service|Gmail, Zoom|
|**PoP**|Point of Presence|Edge Location|
|**AZ**|Availability Zone|Physical data center cluster in a Region|

---

## 20. Top 20 Revision Points

1. **Lambda = 15 min max** — the single most common exam trap. Beyond that, use AWS Batch or EC2.
2. **Serverless = Lambda (functions) + Fargate (containers)** — both are serverless.
3. **ECS ≠ EKS** — ECS is AWS-native, EKS runs actual Kubernetes.
4. **Fargate = compute engine, ECS/EKS = orchestrator** — they work together, not as substitutes.
5. **Outposts = physical hardware at YOUR site** — not a virtual/remote service.
6. **Edge Locations ≠ Regions or AZs** — they're cache points, not full data centers.
7. **IaaS → EC2, PaaS → Elastic Beanstalk, SaaS → Gmail** — near-guaranteed exam question.
8. **Spot Instances = up to 90% discount but interruptible** — fault-tolerant workloads only.
9. **Lightsail = fixed monthly price, simplified** — not full EC2 capability.
10. **ECR = store images, ECS/EKS = run images** — two separate roles.
11. Auto Scaling + ELB together = elasticity + high availability for EC2 fleets.
12. AMI = blueprint; EC2 instance = the running VM created from that blueprint.
13. Reserved Instances (up to 72% off) fit steady-state workloads; Savings Plans (up to 66% off) offer more flexibility.
14. Dedicated Hosts exist for compliance/licensing requirements needing a physical, single-tenant server.
15. Container ≠ VM — containers share the host OS kernel, making them lighter and faster to start.
16. AWS Batch handles unlimited-duration, parallel, large-scale jobs — Lambda cannot.
17. Elastic Beanstalk itself is free — you only pay for the EC2/ALB/etc. it provisions.
18. CloudFront caches static/dynamic content; Global Accelerator optimizes routing for non-cacheable/dynamic content — don't confuse the two.
19. Global Accelerator uses AWS's private network, not the public internet.
20. Outposts is used for low latency, data residency, offline/limited-connectivity operations, and gradual cloud migration.

---

## 21. Common CCP Question Patterns

- **Duration-based trap:** Scenario gives a job duration (30 sec vs 4 hours) to force a choice between Lambda and AWS Batch/EC2.
- **"No server management" phrasing:** Tests whether you correctly identify Lambda (functions) vs Fargate (containers) based on whether the workload is function code or a containerized app.
- **Service model classification:** Gives a scenario and asks which of IaaS/PaaS/SaaS it represents.
- **Near-identical-sounding pairs:** ECS vs EKS, CloudFront vs Global Accelerator, Fargate vs ECS/EKS — deliberately worded to test precise understanding, not memorization.
- **Cost/discount recall:** Asks which pricing model gives which discount range (Spot ~90%, Reserved ~72%, Savings Plans ~66%).
- **Compliance/data residency scenarios:** Point toward Outposts as the answer whenever "on-premises" + "data residency" + "hybrid" appear together.

---

## 22. Final Decision Matrix

|Scenario|Best Service|
|---|---|
|Upload file → auto resize image|Lambda|
|Run web app, don't want infra work|Elastic Beanstalk|
|Full control over server|EC2|
|Run Docker containers, no server management|ECS/EKS + Fargate|
|Process 10 million records overnight|AWS Batch|
|Small WordPress blog on a budget|Lightsail|
|Bank with strict data residency laws|Outposts|
|Speed up video streaming globally|CloudFront|
|Microservices at scale, using Kubernetes|EKS|
|Simple container orchestration on AWS|ECS|
|Store private Docker images|ECR|
|Distribute traffic across EC2 instances|Elastic Load Balancing (ELB)|
|Automatically handle traffic spikes|Auto Scaling|

---

## 23. Cross-Links to Related AWS Services (Other Modules)

- **Module 4 (Going Global):** CloudFront, Global Accelerator, Outposts, Region/AZ concepts are shared directly with this module's infrastructure hierarchy content.
- **Module 5 (Networking):** EC2 instances live inside VPCs/subnets; Security Groups (mentioned here) are covered in depth alongside NACLs in Networking.
- **Module 6 (Storage):** EBS volumes attach to EC2 instances; S3 is a common CloudFront/Lambda origin/trigger source.
- **Module 7 (Databases):** RDS often runs on EC2-backed infrastructure; DynamoDB Streams are a Lambda trigger source.
- **Module 9 (Security):** IAM roles attached to EC2/Lambda for permissions; Security Groups as a first line of defense.
- **Module 11 (Pricing):** EC2 pricing models (On-Demand, Reserved, Spot, Savings Plans) tie directly into the broader AWS Pricing module.

---

**Status: Ready for AWS CCP Exam ✅**