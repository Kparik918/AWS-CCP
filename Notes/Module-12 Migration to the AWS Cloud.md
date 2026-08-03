# 📦 MODULE 12: MIGRATION TO THE AWS CLOUD — BIBLE NOTES

### AWS Certified Cloud Practitioner (CLF-C02) | Complete Study Guide

---

## 🗺️ MODULE MAP

```
Migration Journey
│
├── 1. AWS Cloud Adoption Framework (CAF)  → "Are we READY to migrate?"
├── 2. Three Phases of Migration           → "HOW do we execute migration?"
├── 3. Seven Rs of Migration (7 Rs)        → "WHAT strategy per application?"
├── 4. Application Discovery & Planning    → tools that tell you WHAT you have
├── 5. Application/Database Migration      → tools that MOVE the workload
└── 6. Data Transfer (Online + Offline)    → tools that MOVE the data
```

**Why this order matters (exam logic):** AWS wants you to think like a consultant walking into a company — first assess _readiness_ (CAF), then decide _strategy_ (7 Rs), then _execute_ (3 phases + tools). Most exam questions test whether you can slot a tool/service into the right stage of this journey.

---

## 1️⃣ AWS CLOUD ADOPTION FRAMEWORK (CAF) ★★★★★

### Definition

AWS CAF is a **framework of guidance and best practices** (not a service, not code) that helps organizations develop an efficient, effective plan to move to the cloud. It doesn't do migration — it prepares the _organization_ for migration.

### Why AWS provides this

Companies fail migrations not because of technology, but because of **people, process, and organizational gaps**. CAF forces a company to look beyond "just move servers" and consider business, people, governance, security etc.

### Hinglish Analogy 🏠

Socho tumhara ghar shift ho raha hai new city mein. Sirf saaman uthake truck mein daalna kaafi nahi hai — tumhe sochna padega: **budget** (Business), **kaun kya karega** (People), **rules/society permissions** (Governance), **naya ghar ka layout** (Platform), **security guard/locks** (Security), **daily chores kaise chalenge** (Operations). CAF yehi 6 cheezein company ko sochne pe force karta hai before the "cloud shift truck" chale.

### The 6 Perspectives of AWS CAF

|#|Perspective|Focus|Simple Explanation|
|---|---|---|---|
|1|**Business**|Business value|Align IT investments with business outcomes/ROI|
|2|**People**|Org change management|Upskilling, roles, culture shift for cloud|
|3|**Governance**|Business risk management|Skills & processes to align IT strategy with business strategy|
|4|**Platform**|Technical architecture|Understanding cloud-based platform architecture — hybrid, modern apps|
|5|**Security**|Risk & compliance|Ensuring org meets security objectives for confidentiality, integrity, availability|
|6|**Operations**|Day-to-day running|Define how day-to-day, quarterly, and yearly business is conducted post-migration|

### 🧠 Memory Trick — Acronym

**"BPG-PSO"** doesn't roll off the tongue, so use grouping instead:

> **"Business People Govern the Platform Securely & Operate it"**

Or split into two buckets (this is how AWS itself groups them — **very testable**):

|Bucket|Perspectives|Owned by|
|---|---|---|
|**Business Capabilities**|Business, People, Governance|Business stakeholders|
|**Technical Capabilities**|Platform, Security, Operations|Technical stakeholders|

⚠️ **Exam trap:** Students often think CAF is a _technical_ tool only. CAF is **primarily a business + organizational framework** — Platform/Security/Operations are only 3 of the 6, and even those are guidance, not hands-on migration tools.

### What AWS is REALLY testing

AWS isn't testing whether you can recite 6 words. AWS is testing whether you understand that **successful migration = organizational readiness, not just technical capability**. If a question describes a company struggling with "who owns what" or "employees resistant to change," that's the **People** perspective, not Platform.

### 30-Second Revision

- **Definition:** Best-practices framework to prepare org for cloud migration
- **Use case:** Before starting any large-scale migration
- **6 Perspectives:** Business, People, Governance, Platform, Security, Operations
- **Common Trap:** Thinking it's purely technical — it's business + technical (3+3)
- **Exam Importance:** ★★★★★

---

## 2️⃣ THREE PHASES OF MIGRATION ★★★★★

### Overview Diagram

```
┌──────────┐      ┌───────────┐      ┌───────────────────────┐
│  ASSESS  │ ───► │ MOBILIZE  │ ───► │ MIGRATE & MODERNIZE    │
└──────────┘      └───────────┘      └───────────────────────┘
"Kahan khade      "Plan banao,       "Ab actually shift karo
 hain hum?"        gaps fix karo"     aur better bhi banao"
```

### Phase 1: ASSESS

**Purpose:** Understand your _current state_ and build the business case for moving to AWS.

- **Key question:** "What do we have, and what would it cost/look like on AWS?"
- **Primary Service:** **AWS Migration Evaluator**
    - Analyzes current on-prem setup
    - Gives **data-driven cost estimates** for moving to AWS
    - Builds the **business case** for migration (helps get budget approval)

### Phase 2: MOBILIZE

**Purpose:** Build the detailed migration plan and **close readiness gaps** found in Assess phase.

- **Key question:** "What exactly do we have, and how do we track fixing gaps?"
- **Primary Services:**
    - **AWS Application Discovery Service** — discovers on-prem servers, their configs, performance, and interdependencies (which app talks to which server/database)
    - **AWS Migration Hub** — a **single dashboard** to track progress across the entire migration (discovery → planning → execution)

### Phase 3: MIGRATE AND MODERNIZE

**Purpose:** The actual execution — move workloads AND improve them where sensible.

- **Key question:** "How do we move it with minimal downtime, and modernize where it makes sense?"
- **Primary Services:**
    - **AWS Application Migration Service (MGN)** — automated lift-and-shift with minimal downtime
    - **AWS Database Migration Service (DMS)** — for databases
    - **AWS Schema Conversion Tool (SCT)** — when converting between different database engines (e.g., Oracle → Aurora)

### Comparison Table: Assess vs Mobilize vs Migrate&Modernize

|Aspect|Assess|Mobilize|Migrate & Modernize|
|---|---|---|---|
|Goal|Build business case|Build migration plan|Execute migration|
|Key Tool|Migration Evaluator|Discovery Service + Migration Hub|MGN + DMS + SCT|
|Output|Cost estimate|Readiness/gap plan|Migrated workload|
|Analogy|Ghar dekhna & budget banana|Packing list banana|Truck mein saaman lo aur shift karo|

### ⚠️ Common Exam Traps

- Confusing **Migration Evaluator** (Assess — cost/business case) with **Application Discovery Service** (Mobilize — technical inventory/dependencies). Both sound like "figuring out what we have" but they solve different problems: Evaluator = **cost**, Discovery = **technical detail**.
- **Migration Hub** does NOT migrate anything itself — it's a **tracking dashboard**.

### What AWS is REALLY testing

AWS isn't testing tool names in isolation. AWS is testing whether you know **which phase a tool belongs to** — if a scenario says "we need to understand cost before asking for budget," that's Migration Evaluator (Assess). If it says "we need to track progress across teams," that's Migration Hub (Mobilize).

### 30-Second Revision

- **3 Phases:** Assess → Mobilize → Migrate & Modernize
- **Assess tool:** Migration Evaluator (cost/business case)
- **Mobilize tools:** Application Discovery Service (inventory) + Migration Hub (tracking)
- **Migrate tools:** MGN (apps), DMS (databases), SCT (schema conversion)
- **Trap:** Evaluator ≠ Discovery Service — cost vs technical detail
- **Exam Importance:** ★★★★★

---

## 3️⃣ THE SEVEN Rs OF MIGRATION (7 Rs) ★★★★★

### Definition

Seven common **strategies** for migrating any individual application/workload to AWS. Each application in a company's portfolio might use a _different_ R depending on its business/technical needs.

### The Diagram (Logic)

```
                                    ┌──► 1. Relocate    (move VMs as-is, no changes, hypervisor-level)
                                    ├──► 2. Rehost      (lift-and-shift)
Applications ──► Discovery Phase ──┼──► 3. Replatform   (lift-tinker-shift)
   to migrate      (analyze each)  ├──► 4. Refactor     (re-architect for cloud-native)
                                    ├──► 5. Repurchase   (drop it, buy SaaS instead)
                                    ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
                                    ├──► 6. Retain      (keep on-prem, don't migrate now)
                                    └──► 7. Retire      (decommission — not needed anymore)
```

_(Dotted line separates: top 5 = "moves to cloud", bottom 2 = "doesn't move to cloud")_

### Detailed Breakdown

|#|Strategy|What it means|Effort|Hinglish Analogy|
|---|---|---|---|---|
|1|**Relocate**|Move infrastructure to cloud **without changing anything** — usually via VMware Cloud on AWS, whole hypervisor moves|Lowest|Poore ka poora building crane se utha ke naye plot pe rakh do — andar kuch nahi badla|
|2|**Rehost**|"Lift-and-shift" — move app as-is to EC2, no code changes|Low|Ghar ka saaman jaise ka waisa naye ghar mein rakh diya|
|3|**Replatform**|"Lift-tinker-and-shift" — small optimizations, e.g., moving DB to RDS instead of self-managed DB on EC2|Medium|Naye ghar mein shift kiya but kitchen ka stove upgrade kar diya|
|4|**Refactor / Re-architect**|Reimagine app using **cloud-native features** (serverless, microservices) — driven by strong business need (scale, cost, agility)|High|Poora ghar redesign kiya smart-home features ke saath|
|5|**Repurchase**|Move to a different product — usually drop old licensed software, **buy SaaS** (e.g., CRM → Salesforce)|Low-Medium|Purana furniture bech ke naya ready-made kharida|
|6|**Retain**|Keep it on-prem for now — not ready/worth migrating yet (compliance, recently upgraded, etc.)|None|Kuch saaman abhi purane ghar mein hi rehne do|
|7|**Retire**|Turn off/decommission — app no longer useful|None (removal)|Purana tootafuta saaman phenk diya|

### 🧠 Memory Trick

**"5 R's move you, 2 R's don't"**

> _Relocate, Rehost, Replatform, Refactor, Repurchase_ → **go to cloud** _Retain, Retire_ → **stay behind or disappear**

Alternate mnemonic sentence: **"Really Renovated Restaurants Repurchase Relocated Retained Retiring furniture"** (order: Relocate, Rehost, Replatform, Refactor, Repurchase, Retain, Retire)

### ⚠️ Common Exam Traps

- **Rehost vs Replatform:** Rehost = literally NO changes. Replatform = SOME optimization (e.g., moving to managed DB) but not full re-architecture. This is the **#1 confused pair** on the real exam.
- **Refactor vs Replatform:** Refactor = major code/architecture change (e.g., monolith → microservices/serverless). Replatform = minor tweaks only.
- **Relocate vs Rehost:** Relocate is specifically **infrastructure-level move (hypervisor)**, usually associated with VMware Cloud on AWS — no OS/app-level change at all, whereas Rehost moves individual apps/servers into native EC2.
- **Retain is a valid strategy**, not "failure to migrate" — exam sometimes frames it as a deliberate business decision (e.g., compliance blocks it).

### What AWS is REALLY testing

AWS isn't testing if you can list 7 words. AWS is testing whether, given a **business scenario**, you can pick the correct R. E.g.: _"Company wants to move a legacy app to cloud with zero code changes and fastest speed"_ → **Rehost**. _"Company wants to drop its on-prem CRM and use a cloud subscription instead"_ → **Repurchase**.

### 30-Second Revision

- **7 Rs:** Relocate, Rehost, Replatform, Refactor, Repurchase, Retain, Retire
- **Move to cloud:** first 5 | **Stay/remove:** last 2
- **Trap:** Rehost (no change) vs Replatform (small optimization) vs Refactor (major re-architecture)
- **Exam Importance:** ★★★★★

---

## 4️⃣ APPLICATION & DATABASE MIGRATION SERVICES

### 4.1 AWS Application Discovery Service ★★★★☆

|Field|Detail|
|---|---|
|**Definition**|Discovers on-premises server inventory, connections, configuration & performance data|
|**Solves**|"We don't even know what apps/servers we have or how they talk to each other"|
|**Phase**|Mobilize|
|**When to use**|Before planning a migration — need dependency mapping|
|**When NOT to use**|If infra is already fully documented/small|
|**Best Practice**|Run discovery for weeks to capture accurate usage patterns|

### 4.2 AWS Migration Hub ★★★☆☆

|Field|Detail|
|---|---|
|**Definition**|Centralized dashboard — discovery → assessment → planning → implementation tracking|
|**Solves**|"Multiple teams migrating different apps, no single view of progress"|
|**Phase**|Mobilize (spans whole journey)|
|**Key Point**|It **tracks**, does not itself migrate|

### 4.3 AWS Application Migration Service (MGN) ★★★★☆

|Field|Detail|
|---|---|
|**Definition**|Automated lift-and-shift (**Rehost**) service — migrates apps to AWS with minimal downtime|
|**Solves**|"We need to move many servers quickly without rewriting them"|
|**Phase**|Migrate and Modernize|
|**Best For**|Rehost strategy specifically|
|**Exam Trap**|MGN = **Rehost tool**, not a refactoring/modernization tool despite being in the "Migrate **and Modernize**" phase name|

### 4.4 AWS Database Migration Service (DMS) ★★★★★

|Field|Detail|
|---|---|
|**Definition**|Migrates databases to AWS quickly & securely; supports **homogeneous** (same engine, e.g., MySQL→MySQL) and **heterogeneous** (different engine, e.g., Oracle→Aurora) migrations|
|**Solves**|"Need to move production DB with minimal downtime"|
|**Key Feature**|Source DB **stays operational** during migration (continuous replication)|
|**Works with**|AWS SCT (for heterogeneous/different-engine conversions)|

### 4.5 AWS Schema Conversion Tool (SCT) ★★★☆☆

|Field|Detail|
|---|---|
|**Definition**|Converts database **schema and code objects** (stored procedures, views, functions) from one DB engine to another|
|**Solves**|"We're switching database engines (e.g., commercial Oracle → open-source Aurora/PostgreSQL) and need the schema/code converted"|
|**Used with**|AWS DMS — SCT converts the schema, DMS migrates the data|

### DMS vs SCT — Comparison Table

|Aspect|AWS DMS|AWS SCT|
|---|---|---|
|Moves|**Data**|**Schema & code objects**|
|Use when|Same or different engine|Different engine (heterogeneous)|
|Downtime|Minimal (continuous replication)|N/A (conversion, not data transfer)|
|Analogy|Truck jo saaman transport kare|Naye ghar ke hisaab se furniture ka design badalne wala engineer|

### ⚠️ Common Exam Traps

- Thinking DMS alone can convert schemas across engines — **you need SCT first** for heterogeneous migrations.
- Confusing MGN (app migration) with DMS (database migration) — different workload types entirely.

### What AWS is REALLY testing

AWS is testing whether you can match the **type of workload** (application vs database, same engine vs different engine) to the **correct tool**, not just recognize service names.

### 30-Second Revision

- **Discovery Service:** finds what you have (Mobilize)
- **Migration Hub:** tracks progress (Mobilize)
- **MGN:** moves apps/servers (Rehost) — Migrate phase
- **DMS:** moves database data — Migrate phase
- **SCT:** converts schema for different engines — pairs with DMS
- **Exam Importance:** ★★★★★

---

## 5️⃣ DATA TRANSFER: ONLINE VS OFFLINE ★★★★★

### Decision Tree

```
Need to move data to AWS?
│
├── Is internet/bandwidth available & sufficient?
│      │
│      YES → ONLINE TRANSFER
│      │        ├── Bulk files to S3/EFS/FSx?           → AWS DataSync
│      │        ├── SFTP/FTPS/FTP file sharing?          → AWS Transfer Family
│      │        └── Need dedicated private high-bandwidth
│      │            network connection?                  → AWS Direct Connect
│      │
│      NO → OFFLINE TRANSFER
│               └── Petabyte-scale data, no/poor internet,
│                   remote location?                      → AWS Snow Family (Snowball Edge)
```

### 5.1 AWS DataSync ★★★★☆

- **Definition:** Managed service for automating & accelerating **online** bulk data transfer to/between S3, EFS, FSx
- **Solves:** "We need to move large amounts of file data quickly and reliably, with scheduling/monitoring"
- **Features:** Bandwidth throttling, migration scheduling, task filtering/reporting, rapid replication
- **Use case:** Ongoing or one-time large file migrations (not databases)

### 5.2 AWS Transfer Family ★★★☆☆

- **Definition:** Fully managed support for file transfers over **SFTP, FTPS, FTP** directly into/out of S3 and EFS
- **Solves:** "Our partners/clients only support legacy FTP-based transfer protocols"
- **Note:** Not meant for massive bulk data — more for **protocol-based file sharing**

### 5.3 AWS Direct Connect ★★★★☆

- **Definition:** Establishes a **private, dedicated network connection** between on-premises and AWS (bypasses public internet)
- **Solves:** "We need consistent high-bandwidth, low-latency, more secure connectivity to AWS" (e.g., ongoing hybrid workloads, not just migration)
- **When to use:** Ongoing hybrid architecture, large consistent data transfer, latency-sensitive workloads
- **When NOT to use:** One-time small transfers (overkill, takes weeks to provision)

### 5.4 AWS Snow Family (Snowball Edge – Storage Optimized) ★★★★★

- **Definition:** Physical, rugged, high-performance NVMe storage devices for **offline** data migration
- **Solves:** "No/poor internet, remote location, multi-petabyte data — can't transfer online in reasonable time"
- **Benefits:** High compute performance, large storage capacity, gigabytes/sec throughput even offline
- **Use cases:** Offline bulk migration; also edge computing in secure/rugged environments
- **Security:** Data encrypted at rest and in transit; tamper-resistant enclosure

### Comparison Table: Online Transfer Options

|Service|Best For|Protocol/Method|Scale|
|---|---|---|---|
|**DataSync**|Automated bulk file migration|Managed agent-based|Large, ongoing|
|**Transfer Family**|Partner/client file exchange|SFTP/FTPS/FTP|Small-medium, protocol-driven|
|**Direct Connect**|Dedicated network link|Private physical connection|Ongoing hybrid, high bandwidth|

### ⚠️ Common Exam Traps

- **"No internet / remote location / petabytes of data"** → this phrase = **Snowball**, not DataSync. Students often pick DataSync because it sounds "automated" but DataSync **requires network connectivity**.
- **Direct Connect is NOT a migration tool per se** — it's ongoing private connectivity; it CAN be used to support migration, but its core purpose is a persistent hybrid link.
- Confusing **Transfer Family** (protocol-based, FTP-style) with **DataSync** (bulk automated sync) — Transfer Family is for **partners using legacy protocols**, not bulk migration.

### 🧠 Memory Trick

> **"Sync bulk. Transfer via FTP. Direct = private pipe. Snow = no internet."**

### What AWS is REALLY testing

AWS isn't testing whether you know Snowball is a "box." AWS is testing whether you recognize **bandwidth/connectivity constraints in a scenario** and choose online vs offline data transfer accordingly.

### 30-Second Revision

- **Online:** DataSync (bulk automated), Transfer Family (SFTP/FTP), Direct Connect (private dedicated link)
- **Offline:** Snow Family / Snowball Edge (no/poor internet, petabyte scale)
- **Trap:** "no internet + huge data" = Snowball, always
- **Exam Importance:** ★★★★★

---

## 📊 MODULE END: QUICK REFERENCE

### Quick Summary Table — All Services by Phase

|Phase|Service|Purpose|
|---|---|---|
|Assess|Migration Evaluator|Cost estimate & business case|
|Mobilize|Application Discovery Service|Server/app inventory & dependencies|
|Mobilize|Migration Hub|Centralized progress tracking|
|Migrate & Modernize|Application Migration Service (MGN)|App lift-and-shift|
|Migrate & Modernize|Database Migration Service (DMS)|Database migration|
|Migrate & Modernize|Schema Conversion Tool (SCT)|Schema/code conversion (diff engines)|
|Data Transfer (Online)|DataSync|Bulk automated file transfer|
|Data Transfer (Online)|Transfer Family|SFTP/FTPS/FTP transfers|
|Data Transfer (Online)|Direct Connect|Private dedicated network link|
|Data Transfer (Offline)|Snow Family (Snowball Edge)|Offline petabyte-scale migration|

### Acronym Cheat Sheet

|Acronym|Full Form|
|---|---|
|**CAF**|Cloud Adoption Framework|
|**7 Rs**|Relocate, Rehost, Replatform, Refactor, Repurchase, Retain, Retire|
|**DMS**|Database Migration Service|
|**SCT**|Schema Conversion Tool|
|**MGN**|Application Migration Service (product code name)|

### Top 20 Revision Points

1. CAF = organizational readiness framework, NOT a migration tool itself
2. CAF has 6 Perspectives: Business, People, Governance, Platform, Security, Operations
3. CAF splits into Business capabilities (Business/People/Governance) + Technical capabilities (Platform/Security/Operations)
4. 3 Phases of Migration: Assess → Mobilize → Migrate & Modernize
5. Assess = Migration Evaluator (cost/business case)
6. Mobilize = Application Discovery Service (inventory) + Migration Hub (tracking)
7. Migrate & Modernize = MGN (apps) + DMS (databases) + SCT (schema)
8. 7 Rs = strategy PER application, not company-wide
9. First 5 Rs move to cloud; last 2 (Retain, Retire) don't
10. Rehost = zero changes (lift-and-shift); Replatform = minor optimization; Refactor = major re-architecture
11. Relocate = infrastructure/hypervisor-level move (e.g., VMware Cloud on AWS)
12. Repurchase = switch to a different (often SaaS) product entirely
13. Retain = valid deliberate decision to NOT migrate yet
14. DMS moves data; SCT converts schema — used together for heterogeneous migrations
15. MGN is specifically a Rehost automation tool
16. DataSync = automated bulk online transfer to S3/EFS/FSx
17. Transfer Family = SFTP/FTPS/FTP protocol-based transfers
18. Direct Connect = private dedicated ongoing network link (not just migration)
19. Snow Family/Snowball Edge = offline transfer when no/poor internet + huge data volume
20. Migration Hub tracks — it does NOT execute migrations itself

### Common CCP Question Patterns

- _"A company wants a quick cost estimate before migration → which service?"_ → Migration Evaluator
- _"A company doesn't know what servers/apps it has → which service?"_ → Application Discovery Service
- _"A company wants zero code changes, fastest migration → which R?"_ → Rehost
- _"A company is replacing on-prem CRM with a cloud subscription → which R?"_ → Repurchase
- _"A company has petabytes of data and poor internet in a remote location → which service?"_ → Snowball Edge
- _"A company needs a dedicated, consistent, high-bandwidth private connection to AWS → which service?"_ → Direct Connect
- _"Converting an Oracle database schema to Aurora PostgreSQL → which tool(s)?"_ → SCT (schema) + DMS (data)

### Final Decision Matrix

|Scenario Signal|Correct Answer|
|---|---|
|"before we commit budget, estimate cost"|Migration Evaluator|
|"map dependencies between our servers"|Application Discovery Service|
|"single dashboard to track all migrating teams"|Migration Hub|
|"move VMs as-is with minimal downtime"|MGN (Rehost)|
|"move production DB, keep source live"|DMS|
|"different DB engine, convert schema first"|SCT + DMS|
|"bulk file sync to S3, scheduled + automated"|DataSync|
|"partner only supports FTP"|Transfer Family|
|"ongoing dedicated private link to AWS"|Direct Connect|
|"no internet, remote site, petabytes of data"|Snowball Edge|

### Cross-Links to Related AWS Services

- **Storage destinations for migrated data:** Amazon S3, Amazon EFS, Amazon FSx (see Module on Storage)
- **Compute target for Rehost/Replatform:** Amazon EC2 (see Module on Compute)
- **Database targets:** Amazon RDS, Amazon Aurora, Amazon DynamoDB (see Module on Databases)
- **Networking foundation for Direct Connect:** Amazon VPC (see Module on Networking)
- **Security for data in transit/at rest during migration:** AWS KMS, IAM (see Module on Security)

---

## 🎯 EXAM-STYLE PRACTICE QUESTIONS (Self-Test)

1. Which AWS CAF perspective focuses on aligning IT investments with business outcomes?
2. A company needs to know exactly which on-prem servers depend on which — which service?
3. What is the key difference between Rehost and Replatform?
4. Which migration strategy involves switching from a licensed CRM to a SaaS product?
5. Which service converts database schema when migrating between different database engines?
6. A company has 5PB of data and only a slow, unreliable internet connection at a remote factory. What should they use?
7. True or False: AWS Migration Hub performs the actual data migration.
8. Which phase of migration does AWS Migration Evaluator belong to?
9. Name the two 7 Rs strategies that do NOT move a workload to the cloud.
10. Which service would a company use for a private, dedicated, ongoing high-bandwidth connection to AWS?

_(Answers: 1-Business, 2-Application Discovery Service, 3-Rehost=no changes vs Replatform=minor optimization, 4-Repurchase, 5-SCT, 6-Snowball Edge, 7-False (it only tracks), 8-Assess, 9-Retain & Retire, 10-Direct Connect)_

---

_End of Module 12 — Migration to the AWS Cloud | CLF-C02 BIBLE Notes_