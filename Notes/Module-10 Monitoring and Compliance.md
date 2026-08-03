# Module 10 — Monitoring & Compliance in AWS

### AWS Certified Cloud Practitioner (CLF-C02) — Master Study Guide

---

## 0. Module Roadmap

```
SECURE  →  MONITOR  →  AUDIT  →  ENSURE COMPLIANCE
(Module 9)  (this module)  (this module)  (this module)
```

Krish, yeh 4-step cycle hi is poore module ka backbone hai:

1. **Secure Systems** – pehle security practices/controls implement karo (IAM, SGs, encryption — Module 9).
2. **Monitor Systems** – phir dekho ki wo security features effective hain ya nahi, aur overall infra ka health kaisa hai. → **CloudWatch**
3. **Conduct Audits** – check karo ki sab kuch business goals aur regional/legal compliance (GDPR, HIPAA) ke hisaab se ho raha hai ya nahi. → **CloudTrail, Config, Audit Manager**
4. **Ensure Compliance** – maintain karo ki wo compliance time ke saath bani rahe. → **AWS Artifact, Organizations, Control Tower**

Think of it like running a restaurant: pehle kitchen secure karo (locks, hygiene rules), phir CCTV se monitor karo (CloudWatch), phir kabhi kabhi surprise audit karwao (CloudTrail/Config), aur last mein FSSAI certificate maintain karo (Artifact/Compliance).

---

## 1. Amazon CloudWatch ★★★★★

### Definition

CloudWatch is AWS's native **monitoring and observability service**. It actively collects **metrics, logs, and events** from AWS resources — both running (active) resources and resources at rest — and gives you dashboards, alarms, and log analysis in one console.

> ⚠️ Exam trap: CloudWatch does **not** just "have a dashboard." The dashboard is a _feature_; the core job is **collecting and acting on metrics/logs/events**.

### Why AWS provides this

Without visibility, you're flying blind — you won't know if an EC2 instance is dying, if costs are spiking, or if a security event just happened. CloudWatch is the "eyes and ears" of your AWS account.

### Real-world problem it solves

- "Is my EC2 instance overloaded right now?"
- "My app went down at 3 AM — what happened?"
- "Notify me automatically before something breaks."

### Core Components

| Component                | What it does                                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| **Metrics**              | Numerical data points over time — CPUUtilization, NetworkIn/Out, StatusCheckFailed, DiskReadOps, etc.  |
| **Dashboards**           | Auto-refreshing visual boards — no manual refresh needed, always current data                          |
| **Alarms**               | Watch a metric against a threshold (e.g., CPU > 90%) and trigger an action when crossed                |
| **Logs**                 | Centralized log storage — organized into **Log Groups** → **Log Streams**, with configurable retention |
| **Logs Insights**        | Query language to search/analyze log data (e.g., find all errors in the last week)                     |
| **Events / EventBridge** | React to state changes (e.g., EC2 instance stopped) in near real-time                                  |

### Monitoring Granularity (High-Yield Fact)

| Monitoring Type                 | Interval           | Cost |
| ------------------------------- | ------------------ | ---- |
| **Basic (Standard) Monitoring** | 5-minute intervals | Free |
| **Detailed Monitoring**         | 1-minute intervals | Paid |

### CloudWatch Alarms — What They Actually Trigger

```
Metric crosses threshold (e.g., EC2 CPU ≥ 90%)
            │
            ▼
     CloudWatch Alarm fires
            │
   ┌────────┼─────────┬──────────────┐
   ▼        ▼          ▼              ▼
Stop/Terminate   SNS Notification  Auto Scaling   Invoke Lambda
   EC2           (email/SMS to      (add/remove    (custom
                  developer)         instances)     automation)
```

### When to Use

- Real-time infrastructure/application monitoring
- Setting up automated responses to performance issues
- Centralizing and querying logs from EC2, Lambda, RDS, etc.
- Cost/performance/reliability tracking

### When NOT to Use

- Deep security-audit trail of **who did what API call** → that's **CloudTrail**, not CloudWatch
- Compliance evidence collection → **Audit Manager**
- Resource _configuration_ drift tracking → **AWS Config**

### CloudWatch vs CloudTrail (Most Confused Pair on the Exam)

|Feature|CloudWatch|CloudTrail|
|---|---|---|
|**Purpose**|Performance/operational **monitoring**|**Auditing** — who did what, when, from where|
|**Data type**|Metrics, logs, events (system behavior)|API calls / user activity|
|**Core question answered**|"Is my system healthy?"|"Who did what, where, and when?"|
|**Triggers alarms/automation**|✅ Yes|❌ No (but can feed CloudTrail logs into CloudWatch)|
|**Retention**|Configurable per Log Group|Indefinite by default (stored in S3)|

**Memory trick:** CloudWatch **watches** (performance), CloudTrail **trails** (footprints/history of actions).

### What AWS is REALLY Testing

AWS isn't testing whether you know CloudWatch "shows graphs." AWS is testing whether you can **distinguish CloudWatch (performance monitoring) from CloudTrail (activity/API auditing)**, and whether you know CloudWatch Alarms can trigger real automated actions (not just alerts).

### Hinglish Analogy

CloudWatch ek **CCTV + smart alarm system** hai apni dukaan ke liye — camera feed dikhata hai (dashboard), aur agar koi threshold cross ho (jaise fridge ka temp bahut zyada ho jaaye), toh khud hi alarm bajata hai aur AC on kar deta hai (auto-remediation).

### 30-Second Revision

- **Definition:** Real-time metrics, logs, dashboards, alarms for AWS resources
- **Use Case:** Performance monitoring + automated alerting
- **Alternative:** CloudTrail (for API/activity auditing, not performance)
- **Pricing:** Basic monitoring free (5-min); detailed monitoring paid (1-min)
- **Common Trap:** Confusing CloudWatch (performance) with CloudTrail (audit trail)
- **Exam Importance:** ★★★★★

---

## 2. Understanding APIs (Foundational Concept for CloudTrail) ★★★☆☆

### Definition

An **API (Application Programming Interface)** is the method through which a customer/system interacts with an application. An **API Call** is the actual request sent by the customer/service to trigger an action.

### Why this matters for the exam

CloudTrail's entire job is to log **API calls**. If you don't understand that "launching an EC2 instance via console" is _itself_ an API call behind the scenes, CloudTrail won't make sense.

```
User clicks "Launch Instance" in AWS Console
            │
            ▼
   Console sends an API request (e.g., RunInstances)
            │
            ▼
   AWS service processes it → EC2 instance created
            │
            ▼
   CloudTrail silently logs: WHO called RunInstances,
   WHEN, FROM WHERE, WITH WHAT PARAMETERS
```

### Hinglish Analogy

API ek **waiter** hai restaurant mein. Aap (user) order do (request), waiter kitchen (backend) tak le jaata hai, kitchen data prepare karta hai, aur waiter wapas laake deta hai (response). Har order waiter ke through logged hota hai — that log is essentially what CloudTrail captures.

---

## 3. AWS CloudTrail ★★★★★

### Definition

CloudTrail logs **every interaction/API call** made to AWS services — console actions, CLI commands, SDK calls, and even calls made by other AWS services on your behalf.

### Why AWS provides this

For security, compliance, and operational troubleshooting: you need a tamper-proof record answering **"Who did what, where, and when?"**

### Core Components

|Component|Function|
|---|---|
|**CloudTrail Events**|Stores every individual API request as an event|
|**CloudTrail Logs**|Stores the actual log files, securely, in an **S3 bucket**|
|**CloudTrail Insights**|Analyzes logs for anomalies — unusual error rates, unusual request volumes|

### Key Properties (High-Yield)

- Every API request/action gets logged — automatically, account-wide
- Logs can be **saved indefinitely**
- Stored in **secure S3 buckets**
- **Tamper-proof** (integrity validation available)
- Logs can be **shipped to another AWS account** easily (centralized security account pattern)

### When to Use

- Security investigations ("who deleted this S3 bucket?")
- Compliance audits requiring proof of activity
- Operational troubleshooting of unexpected changes

### When NOT to Use

- Performance monitoring (CPU, memory, network) → use **CloudWatch**
- Checking whether resource _configuration_ matches a desired state → use **AWS Config**

### AWS Config vs CloudTrail (Second Most Confused Pair)

|Feature|AWS Config|CloudTrail|
|---|---|---|
|**Answers**|"What does my resource look like _right now_ vs before?" (configuration state/drift)|"Who made the API call that changed it?" (activity/identity)|
|**Focus**|Resource **configuration history**|**User/API activity** history|
|**Can generate compliance reports?**|✅ Yes, based on custom rules|Not directly (feeds evidence to Audit Manager)|
|**Typical use**|Drift detection, compliance rule evaluation|Security forensics, "who did it"|

**Memory trick:** Config tracks the **"What changed"**, CloudTrail tracks the **"Who changed it."**

### What AWS is REALLY Testing

AWS isn't testing whether you know CloudTrail "logs stuff." AWS is testing whether you know CloudTrail is the tool for **accountability (who/what/when)**, distinct from Config (configuration state) and CloudWatch (performance).

### Real AWS Scenario

A bank notices an S3 bucket permission was changed to public. Security team opens **CloudTrail** → finds the exact IAM user, timestamp, and source IP that made the `PutBucketAcl` API call.

### Hinglish Analogy

CloudTrail ek **building ka CCTV + entry register** hai jo har insaan ka aana-jaana (API call) note karta hai — kaun aaya, kab aaya, kya kiya — permanently, tamper-proof register mein.

### 30-Second Revision

- **Definition:** Logs every API call/activity across your AWS account
- **Use Case:** Security auditing, "who did what, when, where"
- **Alternative:** AWS Config (for configuration state, not activity)
- **Pricing:** One copy of management events free; additional trails/data events cost extra
- **Common Trap:** Mixing up with CloudWatch (performance) or Config (configuration)
- **Exam Importance:** ★★★★★

---

## 4. AWS Config ★★★★☆

### Definition

AWS Config **assesses, audits, and evaluates the configurations** of your AWS resources against rules you define, and tracks configuration changes over time.

### Why AWS provides this

Organizations need to know: "Are my resources configured the way they're supposed to be?" — e.g., "Is encryption always enabled on every new EBS volume?"

### Key Capabilities

- You define expectations/standards → Config continuously monitors and evaluates resources against them
- Tracks **configuration history / drift** over time
- Can **auto-remediate** non-compliant resources (via Systems Manager automation)
- Generates **compliance reports**

### When to Use

- Governance — ensuring resources always match organizational standards
- Drift detection (e.g., someone manually disabled encryption)
- Feeding evidence into compliance frameworks

### When NOT to Use

- If you need "who did it" → CloudTrail
- If you need real-time performance metrics → CloudWatch

### What AWS is REALLY Testing

AWS is testing whether you know Config is about **desired-state configuration compliance**, not activity logging or performance.

### 30-Second Revision

- **Definition:** Tracks & evaluates AWS resource configurations against defined rules
- **Use Case:** Compliance rule enforcement, configuration drift detection
- **Alternative:** CloudTrail (activity, not config state)
- **Pricing:** Pay per configuration item recorded + per rule evaluation
- **Common Trap:** Thinking Config logs "who" made a change (it doesn't — that's CloudTrail)
- **Exam Importance:** ★★★★☆

---

## 5. AWS Audit Manager ★★★☆☆

### Definition

A **managed service** that automates the **collection of evidence** needed to prove your organization meets specific compliance frameworks (e.g., GDPR, HIPAA, PCI-DSS).

### Why AWS provides this

Manually gathering "proof" for auditors (screenshots, config exports, logs) is slow and error-prone. Audit Manager automates continuous evidence collection.

### Key Points

- Pre-built frameworks for common regulations
- Continuously and automatically collects evidence (pulls from CloudTrail, Config, etc.)
- Produces audit-ready reports

### Audit Manager vs AWS Config vs CloudTrail

|Service|Core Job|
|---|---|
|**CloudTrail**|Raw activity logs (who did what)|
|**AWS Config**|Configuration state/compliance rules|
|**Audit Manager**|Aggregates evidence from the above **specifically for formal audits/compliance frameworks**|

### What AWS is REALLY Testing

AWS wants you to know Audit Manager sits **on top of** CloudTrail/Config as an evidence-aggregation and reporting layer for formal audits — it doesn't collect raw data itself from scratch.

### 30-Second Revision

- **Definition:** Automates compliance evidence collection & audit-readiness
- **Use Case:** Preparing for formal regulatory/industry audits
- **Alternative:** Manual evidence gathering (slow, error-prone)
- **Pricing:** Pay per assessment/evidence collected
- **Common Trap:** Confusing it with AWS Artifact (which provides AWS's _own_ compliance docs, not your evidence)
- **Exam Importance:** ★★★☆☆

---

## 6. AWS Artifact ★★★☆☆

### Definition

A **self-service portal** providing on-demand access to AWS's **own** security and compliance documentation — reports, certifications, and agreements.

### Two Types

|Type|What it Provides|
|---|---|
|**AWS Artifact Agreements**|Manage & accept agreements with AWS regarding data usage (e.g., BAA for HIPAA, GDPR-related agreements)|
|**AWS Artifact Reports**|Third-party audit reports (SOC 1/2/3, ISO certifications, PCI reports) that prove AWS's infrastructure itself is compliant — useful for your own auditors/employees to reference|

### ⚠️ Common Exam Trap

AWS Artifact gives you documentation **about AWS's compliance** (AWS's side of the Shared Responsibility Model), **NOT** your own resource compliance evidence. Don't confuse it with Audit Manager (which is about **your** evidence) or Config (your resource state).

### What AWS is REALLY Testing

AWS is testing whether you understand the **Shared Responsibility Model**: Artifact proves AWS is compliant "of the cloud"; YOU still need Config/Audit Manager/CloudTrail to prove your workloads are compliant "in the cloud."

### 30-Second Revision

- **Definition:** On-demand access to AWS's own compliance reports & agreements
- **Use Case:** Downloading SOC/ISO/PCI reports, signing BAAs
- **Alternative:** N/A (unique service)
- **Pricing:** Free
- **Common Trap:** Thinking it audits YOUR resources (it doesn't — it's AWS's own compliance docs)
- **Exam Importance:** ★★★☆☆

---

## 7. AWS Organizations ★★★★☆

### Definition

Provides **central management/governance of multiple AWS accounts** under a single organization.

### Key Concepts

- One account becomes the **management (parent) account**; others are **member (child) accounts**
- Uses **SCPs (Service Control Policies)** to enforce permission boundaries on individual accounts or **Organizational Units (OUs)**
- Enables consolidated billing across all accounts

### ⚠️ Common Exam Trap

SCPs set the **maximum available permissions** — they don't _grant_ permissions themselves. Even if an IAM policy allows an action, an SCP can still **block** it. SCPs never grant access on their own.

### When to Use

- Managing multiple teams/departments/environments (dev, test, prod) under separate accounts
- Enforcing org-wide guardrails (e.g., "no account can disable CloudTrail")
- Consolidated billing for cost savings

### Hinglish Analogy

AWS Organizations ek **joint family ka mukhiya (parent account)** hai — sabhi child accounts (bhai-behen) ke liye rules (SCPs) set karta hai ki kaun kya kar sakta hai, chahe unki individual permission slip mein kuch bhi likha ho.

### 30-Section Revision

- **Definition:** Central management of multiple AWS accounts
- **Use Case:** Multi-account governance, consolidated billing
- **Alternative:** Managing accounts individually (not scalable)
- **Pricing:** Free
- **Common Trap:** Thinking SCPs grant permissions (they only restrict/set boundaries)
- **Exam Importance:** ★★★★☆

---

## 8. AWS Control Tower, Service Catalog & License Manager ★★★☆☆

|Service|Definition|Use Case|
|---|---|---|
|**AWS Control Tower**|Sets up and governs a secure, compliant, **multi-account AWS environment** based on best practices (built on top of Organizations)|Fast, guardrail-based landing zone setup for new organizations|
|**AWS Service Catalog**|Create, share, and organize a **curated catalog** of approved AWS services/resources|Letting teams self-serve approved infrastructure without giving them free rein|
|**AWS License Manager**|Manage software licenses and fine-tune licensing costs|Tracking/enforcing 3rd-party software license usage (e.g., Windows Server, Oracle) across your AWS footprint|

### Control Tower vs Organizations

- **Organizations** = the underlying multi-account structure/permission engine (SCPs)
- **Control Tower** = an automated, opinionated **setup wizard** on top of Organizations that applies guardrails and best-practice account structures out of the box

### What AWS is REALLY Testing

AWS wants you to recognize these as **governance-at-scale** tools, not to memorize deep configuration steps. Just know **what problem each one solves**.

---

## 9. AWS Health ★★★☆☆

### Definition

AWS Health is the **go-to data source for events and changes affecting the health** of your AWS Cloud resources — notifies you about service events, planned changes, and account-specific notifications.

### Benefits

- Timely, actionable guidance to remedy issues
- Integrated and automated for use at scale
- Account-specific (unlike the public AWS Service Health Dashboard, which shows general service status)

### Use Cases

- Viewing account-specific health information
- Planning for lifecycle events (e.g., scheduled maintenance)
- Troubleshooting an ongoing incident

### ⚠️ Common Exam Trap

Don't confuse **AWS Health Dashboard (account-specific)** with the **AWS Service Health Dashboard (general/public, all-customer service status)**. CCP exam sometimes tests this distinction.

### 30-Second Revision

- **Definition:** Account-specific service health/event notifications
- **Use Case:** Planned maintenance alerts, incident troubleshooting
- **Alternative:** Public AWS Service Health Dashboard (general, not account-specific)
- **Pricing:** Free (Business/Enterprise support gets richer features)
- **Common Trap:** Confusing account-specific vs public-general health dashboards
- **Exam Importance:** ★★★☆☆

---

## 10. AWS Trusted Advisor ★★★★☆

### Definition

Continuously evaluates your AWS environment using **best-practice checks** across five categories, and gives recommendations.

### The 5 Categories (High-Yield — Memorize)

|Category|What it Checks|
|---|---|
|**Cost Optimization**|Idle/underutilized resources, unused Reserved Instances|
|**Performance**|Service limits, overutilized instances|
|**Security**|Open ports, MFA on root, public S3 buckets, IAM use|
|**Fault Tolerance**|Backups, Multi-AZ, Auto Scaling configuration|
|**Service Limits**|Tracking usage against AWS account quotas|

### Memory Trick

**"C-P-S-F-S"** → **C**ost, **P**erformance, **S**ecurity, **F**ault Tolerance, **S**ervice Limits. Think: **"Costly Performance Sinks Fault-tolerant Services"** (silly sentence, but it sticks).

### Support Plan Tiers

|Support Plan|Trusted Advisor Access|
|---|---|
|**Basic / Developer**|A handful of core checks (mainly security)|
|**Business / Enterprise**|Full access — hundreds of checks across all 5 categories|

### What AWS is REALLY Testing

AWS is testing whether you know Trusted Advisor gives **proactive, prescriptive recommendations** (not just data like CloudWatch) — and whether full access requires **Business/Enterprise support**.

### 30-Second Revision

- **Definition:** Automated best-practice checks & recommendations across 5 categories
- **Use Case:** Proactive cost/security/performance optimization
- **Alternative:** Manual audits (slow, incomplete)
- **Pricing:** Free (limited checks); full checks need Business/Enterprise Support
- **Common Trap:** Assuming all checks are free on Basic support — they're not
- **Exam Importance:** ★★★★☆

---

## 11. IAM Access Analyzer ★★★☆☆

### Definition

Analyzes **external access** to your resources (S3 buckets, IAM roles, KMS keys, etc.) and validates that policies match your intended security posture — helping achieve **least privilege**.

### Benefits

- Identifies resources shared with external entities (outside your account/org)
- Validates IAM policies against best practices
- Automates IAM policy reviews
- Helps remediate unused access

### Use Cases

- "Is this S3 bucket accidentally public?"
- "Which IAM roles have unused permissions I can remove?"

### IAM Access Analyzer vs AWS Config vs Trusted Advisor

|Service|Focus|
|---|---|
|**IAM Access Analyzer**|External/least-privilege **access** analysis specifically|
|**AWS Config**|General resource **configuration** compliance (broader than just access)|
|**Trusted Advisor**|Broad best-practice checks (cost, performance, security, fault tolerance)|

### What AWS is REALLY Testing

AWS wants you to know this tool specifically targets **unintended external access and least-privilege enforcement**, which is a common real-world security gap (e.g., accidental public S3 buckets).

### 30-Second Revision

- **Definition:** Finds unintended external access & validates least-privilege
- **Use Case:** Catching public/over-shared resources, IAM cleanup
- **Alternative:** Manual policy review (slow, error-prone)
- **Pricing:** Free for basic external access analysis
- **Common Trap:** Confusing with Trusted Advisor's broader security checks
- **Exam Importance:** ★★★☆☆

---

## 12. Compliance — The Big Picture ★★★★☆

### Definition

**Compliance** = making sure everything in the company meets fixed standards — both the organization's own internal standards AND external regulatory/legal standards (e.g., **GDPR**, **HIPAA**) depending on where the cloud infrastructure and its data are located.

### Key Regulatory Acts to Recognize (Recognition-level only for CCP)

|Regulation|Region/Domain|Focus|
|---|---|---|
|**GDPR**|EU|Personal data protection & privacy|
|**HIPAA**|USA (Healthcare)|Protected health information (PHI)|

### AWS Compliance / Customer Compliance Center

A resource hub showing AWS's compliance-enabling services in one place, plus access to whitepapers like the **AWS Risk and Security whitepaper**, and customer stories about compliance journeys.

### The Compliance Toolchain (How These Services Work Together)

```
                    ┌────────────────────┐
                    │  Define Standards   │
                    │ (org policy / law)  │
                    └─────────┬───────────┘
                              ▼
        ┌─────────────────────────────────────────┐
        │            AWS Config                     │
        │   (checks resource config vs standard)     │
        └─────────────────────┬─────────────────────┘
                              ▼
        ┌─────────────────────────────────────────┐
        │            CloudTrail                      │
        │   (logs WHO/WHAT/WHEN changed anything)     │
        └─────────────────────┬─────────────────────┘
                              ▼
        ┌─────────────────────────────────────────┐
        │           Audit Manager                    │
        │  (aggregates evidence for formal audits)    │
        └─────────────────────┬─────────────────────┘
                              ▼
        ┌─────────────────────────────────────────┐
        │           AWS Artifact                     │
        │ (proves AWS's own infra is certified/compliant) │
        └─────────────────────────────────────────┘
```

### What AWS is REALLY Testing

AWS is testing the **Shared Responsibility Model applied to compliance**: AWS secures/certifies the infrastructure (Artifact proves this); YOU are responsible for configuring, monitoring, and proving compliance of what you put IN the cloud (Config, CloudTrail, Audit Manager, IAM Access Analyzer).

---

## 13. Master Decision Tree — "Which Monitoring/Compliance Service Do I Need?"

```
What do you need to know?
        │
        ├── "Is my system performing well right now?" ────────→ CloudWatch
        │
        ├── "Who did what action, and when?" ──────────────────→ CloudTrail
        │
        ├── "Is my resource CONFIGURED the way it should be?" ─→ AWS Config
        │
        ├── "I need evidence for a formal compliance audit" ───→ AWS Audit Manager
        │
        ├── "I need AWS's OWN compliance certificates" ────────→ AWS Artifact
        │
        ├── "Manage governance across MANY accounts" ──────────→ AWS Organizations
        │        └── "...with automated best-practice setup" ──→ AWS Control Tower
        │
        ├── "Is anything externally/publicly exposed?" ────────→ IAM Access Analyzer
        │
        ├── "General best-practice recommendations" ───────────→ Trusted Advisor
        │
        └── "Is there a service outage/change affecting ME?" ──→ AWS Health
```

---

## 14. Full Service Comparison Table

|Service|Category|Core Question Answered|Key Trap|
|---|---|---|---|
|**CloudWatch**|Monitoring|"Is my system healthy?"|Confused with CloudTrail|
|**CloudTrail**|Auditing|"Who did what, when, where?"|Confused with Config|
|**AWS Config**|Configuration Compliance|"Is my resource configured correctly?"|Doesn't show "who"|
|**Audit Manager**|Audit Evidence|"Can I prove compliance to an auditor?"|Confused with Artifact|
|**AWS Artifact**|AWS's Own Compliance Docs|"Is AWS itself certified/compliant?"|Confused with Audit Manager|
|**AWS Organizations**|Multi-Account Governance|"How do I manage many accounts centrally?"|SCPs restrict, don't grant|
|**Control Tower**|Automated Governance Setup|"How do I set up a compliant landing zone fast?"|Built ON TOP of Organizations|
|**Service Catalog**|Curated Resource Catalog|"How do I let teams self-serve safely?"|Not for compliance evidence|
|**License Manager**|Software License Tracking|"Am I over-using licensed software?"|Not related to AWS service limits|
|**AWS Health**|Account-Specific Health|"Is there an issue affecting MY account?"|Confused with public Service Health Dashboard|
|**Trusted Advisor**|Best-Practice Recommendations|"What should I optimize/fix?"|Full checks need Business+ Support|
|**IAM Access Analyzer**|External Access Analysis|"Is anything unintentionally exposed?"|Confused with Trusted Advisor security checks|

---

## 15. Acronym Cheat Sheet

|Acronym|Full Form|
|---|---|
|**API**|Application Programming Interface|
|**GDPR**|General Data Protection Regulation|
|**HIPAA**|Health Insurance Portability and Accountability Act|
|**SCP**|Service Control Policy|
|**OU**|Organizational Unit|
|**PHI**|Protected Health Information|
|**SOC**|System and Organization Controls (report type in Artifact)|

---

## 16. Top 20 Revision Points

1. CloudWatch = **performance monitoring** (metrics, dashboards, alarms, logs).
2. CloudWatch basic monitoring = 5-min intervals, free; detailed = 1-min, paid.
3. CloudWatch Alarms can trigger: stop/terminate EC2, SNS notify, Auto Scaling, Lambda.
4. CloudTrail = **API/activity auditing** — "who did what, when, where."
5. CloudTrail logs stored securely & tamper-proof in **S3**; can be kept indefinitely.
6. CloudTrail Insights = anomaly detection on error rates/request volumes.
7. AWS Config = **configuration compliance/drift detection**, not activity logs.
8. Audit Manager = **automates evidence collection** for formal audits.
9. AWS Artifact = access to **AWS's own** compliance reports/agreements (SOC, ISO, BAA).
10. AWS Artifact has 2 types: **Agreements** and **Reports**.
11. AWS Organizations = central multi-account management via **SCPs**.
12. SCPs **restrict** max permissions — they never **grant** permissions.
13. Control Tower = automated best-practice setup **built on top of** Organizations.
14. Service Catalog = curated, approved resource catalog for self-service.
15. License Manager = tracks/manages **software licenses**, not AWS service limits.
16. AWS Health = **account-specific** event/health notifications (not public dashboard).
17. Trusted Advisor's 5 categories: **Cost, Performance, Security, Fault Tolerance, Service Limits**.
18. Full Trusted Advisor checks require **Business/Enterprise Support**.
19. IAM Access Analyzer = finds **unintended external access**, supports least privilege.
20. Compliance in the cloud = **Shared Responsibility** — AWS proves infra compliance (Artifact); YOU prove workload compliance (Config, CloudTrail, Audit Manager).

---

## 17. Common CCP Question Patterns

- _"A company needs to know who deleted an S3 bucket. Which service?"_ → **CloudTrail**
- _"A company wants automatic alerts when EC2 CPU exceeds 80%."_ → **CloudWatch Alarms**
- _"A company wants to verify that all EBS volumes are encrypted at all times."_ → **AWS Config**
- _"A company needs to hand auditors proof of PCI-DSS compliance."_ → **AWS Audit Manager** (their evidence) + **AWS Artifact** (AWS's certification)
- _"A company wants centralized control over 50 AWS accounts."_ → **AWS Organizations** (+ **Control Tower** for automated best-practice setup)
- _"A company wants to know if any S3 bucket is publicly accessible."_ → **IAM Access Analyzer**
- _"A company wants free general recommendations on cost & security."_ → **Trusted Advisor** (note: full access needs Business+ support)
- _"A company wants to know about an AWS-side outage affecting their account specifically."_ → **AWS Health**

---

## 18. Final Decision Matrix

|Need|Best Service|
|---|---|
|Real-time performance metrics|CloudWatch|
|Automated response to a threshold breach|CloudWatch Alarms|
|Centralized, searchable logs|CloudWatch Logs + Logs Insights|
|Full history of API calls / user activity|CloudTrail|
|Detect config drift / enforce config rules|AWS Config|
|Prepare audit-ready compliance evidence|AWS Audit Manager|
|Download AWS's compliance certificates|AWS Artifact|
|Manage many AWS accounts centrally|AWS Organizations|
|Quick, guardrail-based multi-account setup|AWS Control Tower|
|Let teams deploy only pre-approved resources|AWS Service Catalog|
|Track 3rd-party software license usage|AWS License Manager|
|See account-specific AWS events/outages|AWS Health|
|Get broad best-practice recommendations|Trusted Advisor|
|Detect unintended external resource access|IAM Access Analyzer|

---

## 19. Cross-Links to Related Modules

- **Module 9 (Security)** → IAM, Security Groups, NACLs, encryption — the "Secure" step that CloudWatch/CloudTrail then monitor and audit.
- **Module 7 (Databases)** → RDS/DynamoDB metrics feed into CloudWatch the same way EC2 does.
- **Future AWS SAA topics** → Deeper CloudWatch custom metrics, Config custom rules, and multi-account landing zone architecture with Control Tower.

---

### Quick Summary Table

|#|Service|One-Line Purpose|Exam Weight|
|---|---|---|---|
|1|CloudWatch|Performance monitoring, alarms, logs|★★★★★|
|2|CloudTrail|API/activity audit trail|★★★★★|
|3|AWS Config|Configuration compliance tracking|★★★★☆|
|4|Audit Manager|Automated audit evidence collection|★★★☆☆|
|5|AWS Artifact|AWS's own compliance docs/agreements|★★★☆☆|
|6|AWS Organizations|Multi-account governance via SCPs|★★★★☆|
|7|Control Tower|Automated compliant landing zone setup|★★★☆☆|
|8|Service Catalog|Curated self-service resource catalog|★★☆☆☆|
|9|License Manager|Software license tracking|★★☆☆☆|
|10|AWS Health|Account-specific health/event notifications|★★★☆☆|
|11|Trusted Advisor|Best-practice recommendations (5 categories)|★★★★☆|
|12|IAM Access Analyzer|External access & least-privilege analysis|★★★☆☆|

---

_End of Module 10 — Monitoring & Compliance in AWS_