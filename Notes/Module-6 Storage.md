---

## tags: [aws, ccp, module-6, storage, exam-prep] module: "6 - Storage" exam: "AWS Certified Cloud Practitioner (CLF-C02)" status: complete
---
# 📦 MODULE 6 — STORAGE (AWS CCP BIBLE)

> **Why this module matters:** Storage is one of the most heavily tested domains in CLF-C02. AWS loves scenario questions where four services _could_ technically work, but only one is the "textbook correct" answer. This guide is built to kill that ambiguity permanently.



## 🗺️ Module Roadmap

```
STORAGE
├── 1. Storage Fundamentals (Block / Object / File)
├── 2. Amazon EBS (Block Storage)
│     ├── Instance Store (bonus comparison)
│     ├── Snapshots + Lifecycle
├── 3. Amazon S3 (Object Storage)
│     ├── Storage Classes
│     ├── Lifecycle Policies
│     ├── Security
├── 4. Amazon EFS (File Storage)
├── 5. Databases (RDS - brief pointer, full detail in DB module)
├── 6. AWS Storage Gateway (Hybrid Storage)
├── 7. AWS Elastic Disaster Recovery
├── 8. Master Comparison + Decision Tree
└── 9. Final Revision Kit
```

---

## 1️⃣ Storage Fundamentals — Block vs Object vs File

Before touching any AWS service, you need to understand **how data is actually stored behind the scenes**. Every AWS storage service is just a managed wrapper around one of these three models.

### 🧱 Block Storage — "Notebook Pages"

Data is broken into **fixed-size blocks**, each block is independent and addressable.

```
File: "Report.docx"
        ↓ split into
[Block 1] [Block 2] [Block 3] [Block 4]
```

- Agar ek update aata hai, sirf **us particular block** ko rewrite karna padta hai — poora file nahi.
- This makes block storage **fast for frequent small changes** (databases, OS boot volumes).
- AWS Service: **Amazon EBS**

**Hinglish Analogy:** Ek notebook ke individual pages — tum ek specific page pe likh sakte ho bina poori notebook ko chhue.

### 📦 Object Storage — "Warehouse with Labeled Boxes"

Every object is a **self-contained unit**:

```
Object = Data + Metadata + Unique Key (identifier)
```

- Data: actual content (photo, video, backup file)
    
- Metadata: info about the data (content-type, tags, creation date)
    
- Key: unique identifier used to locate the object (e.g., `photos/2026/trip.jpg`)
    
- **Any change → the entire object is rewritten** (no partial edits like block storage).
    
- Best for data that's written once and read many times: backups, videos, static assets, logs.
    
- AWS Service: **Amazon S3**
    

**Hinglish Analogy:** Ek warehouse jisme labeled boxes hain. Har box (object) apne aap mein complete hai apne label (metadata) ke saath. Box ka content change karna hai? Poora naya box banao aur purane ko replace karo.

### 🗂️ File Storage — "Almirah with Labeled Folders"

Data is organized in a **hierarchical structure** — folders inside folders, just like a traditional file system.

```
/shared-drive
   ├── /finance
   │      ├── budget2026.xlsx
   ├── /hr
   │      ├── policies.docx
```

- Best for applications that need **shared, simultaneous access** from multiple servers/users.
- Uses the **NFS protocol** on Linux (or SMB for Windows-style file shares).
- Content Management Systems, media rendering farms, and shared home directories need this model.
- AWS Service: **Amazon EFS** (Linux/NFS), **Amazon FSx** (Windows/SMB, Lustre, NetApp)

**Hinglish Analogy:** Ek almirah with labeled folders — organized hierarchy, specific file nikaal sakte ho aur usme edit kar sakte ho.

### 📊 Quick Comparison Table

|Attribute|Block Storage|Object Storage|File Storage|
|---|---|---|---|
|Unit of storage|Fixed-size block|Object (data+meta+key)|File in folder hierarchy|
|Update behavior|Only changed block rewritten|Entire object rewritten|Only changed file rewritten|
|Access pattern|Single instance (usually)|Anywhere via API/HTTP|Shared, multiple clients|
|Best for|Databases, OS volumes|Backups, media, static sites|Shared drives, CMS|
|AWS Service|EBS|S3|EFS / FSx|
|Protocol|Block-level (attached like a disk)|HTTP/REST API|NFS / SMB|

### 🎯 What AWS is REALLY testing

AWS isn't testing whether you can define block/object/file. AWS is testing whether, given a **business scenario** (e.g., "1000 EC2 instances need to read/write the same files simultaneously"), you can correctly map it to **file storage → EFS**, not EBS (single-attach) or S3 (not a real filesystem).

⭐ **Exam Importance:** ★★★★★

---

## 2️⃣ Amazon EBS — Elastic Block Store

### Definition

EBS is AWS's **block storage** service — network-attached virtual hard disks for EC2 instances.

### Why AWS provides this / problem it solves

EC2's own local storage (**instance store**) is volatile — data dies when the instance stops. Businesses need **persistent** storage that survives reboots/terminations and can be reattached elsewhere. EBS solves this.

### 🆚 EBS vs EC2 Instance Store

|Attribute|EBS|Instance Store|
|---|---|---|
|Persistence|Survives stop/terminate (unless configured otherwise)|Volatile — lost on stop/terminate (like RAM)|
|Cost|Extra cost (pay per GB/IOPS)|Included free with instance|
|Latency|Slightly higher (network-attached)|Very low (physically attached to host)|
|Attach/Detach|Yes, to any compatible instance in the same AZ|No — tied to the specific physical host|
|Use case|Databases, boot volumes, persistent app data|Cache, buffers, temporary scratch data, replicated data|

**Hinglish Analogy:** Instance Store = hotel room ka furniture (aata hai free, but checkout karte hi gayab). EBS = tumhara khud ka suitcase jo tum kisi bhi room mein le ja sakte ho.

### When to use EBS

- Databases running on EC2 (needs persistent, low-latency block storage)
- Boot volumes for EC2 instances
- Applications requiring **consistent, high IOPS** performance

### When NOT to use EBS

- Shared access across multiple instances simultaneously → use **EFS**
- Static files/media/backups accessed via web → use **S3**
- Temporary/scratch data where cost matters more than persistence → **Instance Store**

### Key Facts

- **Independent lifecycle** — an EBS volume exists separately from the EC2 instance; it persists even after instance termination (unless "Delete on Termination" is set).
- Can be **detached from one instance and attached to another** (within the same Availability Zone).
- Multiple volume types available (SSD/HDD-backed) to balance **cost vs performance** — you can upgrade/downgrade based on need and budget.
- Can move data across AZs using **Snapshots**.

### 📸 EBS Snapshots

A snapshot is a **point-in-time backup** of an EBS volume, stored in S3 behind the scenes.

**Incremental storage concept:**

```
Snap-1 (Sunday):    ■■■■  (4 blocks — full baseline)
Snap-2 (Wednesday): ■■    (only 2 NEW/changed blocks stored)
                    Total unique data stored = 6 blocks, NOT 8
```

- **Initial snapshot** = full copy of all data blocks in use at that point in time (the baseline).
- **Subsequent snapshots** = only the **changed blocks** since the last snapshot are captured (incremental) — smaller & faster.
- Despite being incremental, **each snapshot still behaves as a full point-in-time restore point** — AWS manages the block references automatically.
- **Deleting a snapshot** only removes data unique to that snapshot; data still referenced by other snapshots is preserved.
- Each incremental snapshot references prior snapshots, forming a **chain** enabling point-in-time recovery.

**AWS Data Lifecycle Manager (DLM):**

- Manually taking daily snapshots across a large multi-instance architecture is tedious.
- DLM **automates** the creation, retention, and deletion of EBS snapshots and EBS-backed AMIs based on a policy/schedule.

### Security Considerations

- EBS volumes support **encryption at rest** (AWS KMS-backed).
- Snapshots of encrypted volumes are automatically encrypted.

### ⚠️ Common Exam Traps

- "EBS automatically syncs to S3 every X minutes" → **FALSE**. EBS persistence comes from being an **independent, network-attached volume**, not automatic S3 syncing. Snapshots (a separate, manual/scheduled action) are stored in S3 — but that's not automatic real-time replication.
- EBS is often confused with instance store — remember: **EBS persists, Instance Store does not.**
- EBS volumes are (mostly) **single-instance attach** — don't confuse with EFS's multi-instance shared access. (Note: `io1`/`io2` Multi-Attach exists but is an edge case, rarely tested at CCP level.)
- Snapshots are **incremental**, not full copies each time — a very common exam trap.

### 🏢 Real AWS Scenario

> AnyCompany is migrating on-prem VMs to AWS. They previously lost data whenever a VM crashed. **How does EBS solve this?** ✅ Correct answer: EBS volumes exist independently from the EC2 instance and persist even after the instance is terminated. ❌ Trap answers: "EBS auto-syncs to S3 every 5 minutes" / "EBS caches data in memory" — both are fabricated behaviors.

### 30-Second Revision — EBS

| | |
|---|---|
|**Definition**|Persistent block storage for EC2|
|**Use Case**|Databases, boot volumes, low-latency apps|
|**Alternative**|Instance Store (temp), EFS (shared file), S3 (object)|
|**Pricing**|Pay per GB provisioned + IOPS (varies by volume type)|
|**Common Trap**|"Auto-syncs to S3" is false; snapshots are incremental, not full|
|**Exam Importance**|★★★★★|

---

## 3️⃣ Amazon S3 — Simple Storage Service

### Definition

S3 is AWS's **object storage** service for storing and retrieving virtually unlimited amounts of data, organized into **buckets**.

### Why AWS provides this / problem it solves

Businesses need to store massive, growing amounts of unstructured data (images, videos, backups, logs, static websites) **without managing any physical infrastructure**, while getting near-100% durability and global accessibility over HTTP.

### Core Concepts

- Every piece of data is stored as an **object** inside a **bucket** (buckets = top-level containers, similar to folders/directories).
- **Maximum object size:** 5 TB per object — **no cap on total bucket size**.
- **Versioning** supported — like Git commits, keeps historical versions of an object.
- Objects reside redundantly across **3+ Availability Zones/facilities** within a Region.
- **Durability:** 99.999999999% (11 nines) — this is about _not losing data_, not about _uptime_.
- Common use cases: static website hosting, backups, data lakes, content distribution, archival, compliance retention.

**Hinglish Analogy:** S3 = Google Drive; a bucket = ek folder jo tumne Drive mein banaya, jisme objects (files) store hote hain aur jinki sharing/access control tum khud manage karte ho.

### 🏢 Real AWS Scenario

A company hosts a website's static assets (HTML, images) on S3. A sudden traffic spike hits the site. Because S3 is a **fully managed service**, scaling to absorb the spike is handled automatically by AWS — no capacity planning needed by the customer.

### 🔒 S3 Security

|Feature|What it does|
|---|---|
|**Default access**|Private by default — nothing is public unless explicitly configured|
|**Bucket Policies**|JSON-based policies controlling who can access the bucket/objects|
|**Presigned URLs**|Grant **temporary**, time-limited access to a specific object|
|**S3 Access Points**|Simplified, scoped access management (conceptually similar to fine-grained ACLs)|
|**S3 Access Logs**|Logs and tracks every request — who accessed what, when|
|**Block Public Access**|Account/bucket-level setting that can override a bucket policy and force objects to stay private|

### ⚠️ Common Exam Trap — Block Public Access

> Scenario: A bucket policy allows public access, but users still can't view the images. ✅ **Most likely cause: "Block Public Access" settings are enabled at the account or bucket level** — this setting **overrides** bucket policies. This is one of AWS's favorite trick questions — students assume the bucket policy is the only control, forgetting the account-level override.

### 🧊 S3 Storage Classes

Storage class = trade-off dial between **cost**, **retrieval speed**, and **availability**, chosen based on how often the data is accessed.

|Storage Class|Access Pattern|Retrieval Speed|Relative Cost|Notes|
|---|---|---|---|---|
|**S3 Standard**|Frequent access|Milliseconds|Higher|Default, general purpose|
|**S3 Standard-IA** (Infrequent Access)|Accessed less often|Milliseconds|Lower than Standard|Same fast retrieval, cheaper storage|
|**S3 One Zone-IA**|Infrequent, non-critical|Milliseconds|Lower than Standard-IA|Data in **single AZ only** → cheaper but **less resilient** (AZ failure = data loss risk)|
|**S3 Intelligent-Tiering**|Unknown/changing pattern|Milliseconds|Small monitoring fee|**Automatically** moves objects between tiers based on access patterns|
|**S3 Glacier Instant Retrieval**|Rare access, need fast retrieval|Milliseconds|Low|Archival but instant read when needed|
|**S3 Glacier Flexible Retrieval**|Archival|Minutes to hours|Very low|Cheaper than Instant Retrieval, slower|
|**S3 Glacier Deep Archive**|Long-term archival|Hours (up to 12h)|Lowest|Cheapest tier, slowest retrieval|

**Hinglish Analogy (One Zone-IA):** Isme cost kam hoga kyuki data ek hi AZ mein rahega — lekin agar us AZ ko kuch ho gaya, toh data gone. **Kam cost, kam reliability.**

### 🔁 S3 Lifecycle Policies

Automate the movement of objects between storage classes (and eventual deletion) based on **age/access rules** — no manual intervention needed.

```
S3 Standard → (30 days) → S3 Standard-IA → (90 days) → S3 Glacier → (365 days) → Delete
     ①              ②                ②                    ③
```

- **Transition actions:** define WHEN an object moves to another storage class.
- **Expiration actions:** define WHEN an object is permanently deleted.

**Example:** Transition objects to Standard-IA after 30 days → archive to Glacier Deep Archive after 1 year.

**Related tools:**

- **S3 Storage Class Analysis** — analyzes access patterns and _recommends_ the best lifecycle policy for you.
- **S3 Intelligent-Tiering** — fully managed service that automatically shifts objects between tiers, removing the need to define manual rules.

### Metadata — Two Types

|Type|Examples|
|---|---|
|**System-defined**|File name, date of creation, last modified|
|**User-defined**|Custom key-value tags added by the user|

### ⚠️ Common Exam Traps — S3

- S3 is **NOT** a file system — it has no true folder hierarchy (folders in the console are a UI illusion using key prefixes).
- **11 nines is durability, not availability.** Availability (uptime) is a separate, lower SLA figure (e.g., 99.9%).
- One Zone-IA and Glacier options trade **resilience for cost** — don't pick them for critical, irreplaceable data unless cost is the explicit priority.
- Confusing **Standard-IA** (millisecond retrieval) with **Glacier Flexible Retrieval** (minutes-to-hours retrieval) — both are "infrequent access" in spirit but very different retrieval speeds.

### 30-Second Revision — S3

|                     |                                                                               |
| ------------------- | ----------------------------------------------------------------------------- |
| **Definition**      | Object storage for virtually unlimited data via buckets                       |
| **Use Case**        | Static websites, backups, data lakes, media storage                           |
| **Alternative**     | EFS (shared filesystem), EBS (block, single-instance)                         |
| **Pricing**         | Pay for storage used + requests + retrieval (varies by class)                 |
| **Common Trap**     | Block Public Access overrides bucket policy; 11 nines = durability not uptime |
| **Exam Importance** | ★★★★★                                                                         |

---

## 4️⃣ Amazon EFS — Elastic File System

### Definition

EFS is a **fully managed, elastic, shared file storage** service for use with AWS Cloud services and on-premises resources. Built on the **NFS protocol**.

### Why AWS provides this / problem it solves

Applications that need **multiple compute instances to read/write the same files at the same time** (shared home directories, content management systems, web-serving farms) can't use EBS (mostly single-attach) or S3 (not a real filesystem). EFS fills this gap.

### Key Facts

- Create one file system → **multiple EC2 instances can mount and access it simultaneously**.
- **Regional** service — automatically **replicates data across multiple Availability Zones** for high availability.
- Supports **thousands of concurrent NFS connections**.
- **Automatic scaling** — storage capacity grows as you add data and shrinks as you remove it (no manual provisioning).
- Ideal for **collaborative and distributed workloads**.

### EFS Storage Classes

|Class|Resilience|Relative Cost|
|---|---|---|
|**EFS Standard / Standard-IA**|Multi-AZ|Higher (highest durability/availability)|
|**EFS One Zone / One Zone-IA**|Single AZ|Lower (reduced resilience)|
|**EFS Archive**|Cold/rarely accessed data|Up to 50% cheaper than Standard-IA — for data accessed a few times a year or less|

### 🆚 EBS vs EFS vs S3

|Attribute|EBS|EFS|S3|
|---|---|---|---|
|Storage type|Block|File|Object|
|Attach to|1 EC2 instance (mostly)|Many EC2 instances simultaneously|Accessed via HTTP API, not "attached"|
|Protocol|Block device|NFS|REST API|
|Scaling|Manual resize|Automatic|Automatic (virtually unlimited)|
|Best for|Databases, boot volumes|Shared file access, CMS|Static assets, backups, data lakes|
|AZ scope|Single AZ (per volume)|Multi-AZ (Standard)|Multi-AZ (3+ facilities) by default|
|Cost|Moderate|Higher than EBS/S3|Lowest per GB (esp. cold tiers)|

### 🎯 What AWS is REALLY testing

AWS is testing whether you recognize the phrase **"multiple instances need simultaneous shared access to files"** as the trigger for EFS — this is the #1 giveaway phrase in CCP scenario questions.

### Note on FSx

- Similar concept to EFS but supports **other protocols** (SMB, iSCSI, Lustre) — useful when the on-prem infrastructure is **Windows-based** and needs a native file-share experience, or for high-performance computing (Lustre).

### 30-Second Revision — EFS

| | |
|---|---|
|**Definition**|Managed, elastic, shared NFS file storage|
|**Use Case**|Shared file access across many EC2 instances (CMS, collaborative apps)|
|**Alternative**|EBS (single-attach block), FSx (Windows/SMB, Lustre)|
|**Pricing**|Pay for storage used, auto-scales up/down|
|**Common Trap**|Confusing EFS (multi-instance, Linux/NFS) with EBS (single-instance, block)|
|**Exam Importance**|★★★★☆|

---

## 5️⃣ Databases — Quick Pointer (RDS)

For structured data that needs to be **organized, queried, analyzed, and modified frequently**, AWS recommends managed database services rather than raw block/object/file storage.

- **Amazon RDS** — managed relational database service (MySQL, PostgreSQL, etc.)
- Full depth (RDS vs DynamoDB, Aurora, etc.) is covered in the **Databases module** — this module only needs you to recognize that "structured, queryable, frequently-modified data" → **database service**, not S3/EBS/EFS directly.

⭐ **Exam Importance:** ★★★☆☆ (for this module — full weight lives in the DB module)

---

## 6️⃣ AWS Storage Gateway — Hybrid Storage Bridge

### Definition

A **fully managed hybrid-cloud storage service** that connects on-premises environments to virtually unlimited AWS cloud storage.

### Why AWS provides this / problem it solves

Storage Gateway is best when a company **doesn't want to change their existing on-prem application/workflow** (legacy compatibility or business choice) but still wants **AWS storage benefits** (scalability, durability, backup, disaster recovery). It acts as a **bridge**: the on-prem application keeps using its standard protocol (file/block/tape), while the backend automatically syncs to AWS storage (S3/EBS/Glacier).

**Hinglish Analogy (Tape Gateway):** Socho tumhare दादा जी को sirf cassette player use karna aata hai, computer nahi. Tum unhe ek "fake cassette player" dete ho jo dikhta/chalta bilkul cassette jaisa hai, lekin peeche se wo recording seedha cloud storage mein save ho rahi hai. दादा जी ko kuch naya seekhna nahi pada, aur recording bhi safe cloud mein pahunch gayi.

### Three Types

|Type|On-prem app sees|Backend (AWS) reality|
|---|---|---|
|**S3 File Gateway**|Normal file folder|Data stored as **S3 objects**; frequently accessed data cached locally for low latency|
|**Volume Gateway**|Block disk (iSCSI)|**EBS volumes/snapshots**|
|**Tape Gateway**|Physical tape drive (Virtual Tape Library / VTL)|Data → S3, and (if old/rarely accessed) automatically → **Glacier** for archival|

**Volume Gateway — two modes:**

- **Cached Mode:** All data lives in AWS; only frequently-used data is cached locally.
- **Stored Mode:** All data stays on-prem; periodic EBS snapshots are sent to AWS for backup/DR purposes.

### 🏢 Real AWS Scenario

> AnyCompany has a large collection of on-prem files that need backup to AWS. They want local access to frequently used files, cloud storage for cost savings, and **minimal changes** to existing file-sharing workflows. ✅ Correct answer: **S3 File Gateway** (local file access + cloud backend + no workflow change) ❌ Trap answers: Volume Gateway (block-based, not file-based) and Tape Gateway (built for backup software expecting physical tape, not general file sharing).

### ⚠️ Common Exam Trap

Matching the **right gateway type to the right on-prem protocol** is the classic trap:

- Need **file shares** → S3 File Gateway
- Need **block/iSCSI disks** → Volume Gateway
- Legacy backup software expecting **physical tape** → Tape Gateway

### 30-Second Revision — Storage Gateway

| | |
|---|---|
|**Definition**|Hybrid bridge connecting on-prem apps to AWS storage|
|**Use Case**|Keep existing on-prem workflow, gain AWS storage benefits|
|**Alternative**|Direct migration to S3/EBS/EFS (if workflow change is acceptable)|
|**Pricing**|Pay for storage used + data transfer|
|**Common Trap**|Matching gateway type (File/Volume/Tape) to correct on-prem protocol|
|**Exam Importance**|★★★★☆|

---

## 7️⃣ AWS Elastic Disaster Recovery (DRS)

### Definition

A fully managed service that streamlines the recovery of **physical, virtual, and cloud-based servers** into AWS.

### How it works

- Provides **continuous, block-level replication** that maintains exact server replicas.
- Minimal time between backup/replication intervals → enables **rapid recovery** when a disaster (outage, failure, ransomware) hits.

### When to use it

- Business continuity / disaster recovery planning for critical workloads (on-prem or cloud) that cannot tolerate long recovery times.

### 🆚 Elastic Disaster Recovery vs Snapshots/Backups

|Attribute|Elastic Disaster Recovery|EBS Snapshots|
|---|---|---|
|Purpose|Full server-level DR (near real-time)|Point-in-time volume backup|
|Recovery speed|Fast (continuous replication, minimal RPO)|Depends on snapshot frequency|
|Scope|Entire server (physical/virtual/cloud)|Single EBS volume|

### 30-Second Revision — Elastic Disaster Recovery

|                     |                                                                           |
| ------------------- | ------------------------------------------------------------------------- |
| **Definition**      | Managed DR service with continuous block-level server replication         |
| **Use Case**        | Fast recovery of critical servers after a disaster                        |
| **Alternative**     | Manual snapshot-based backup/restore (slower, higher RPO)                 |
| **Common Trap**     | Don't confuse with simple EBS snapshots — DRS is continuous & server-wide |
| **Exam Importance** | ★★★☆☆                                                                     |

---
### AWS Snowball — Physical Data Transfer Service

**Core idea:** Jab data itna bada ho ki internet se transfer karna slow/impractical/expensive ho, AWS aapko **physical device** bhejta hai. Aap data locally copy karte ho, device wapas bhejte ho, AWS data ko S3 mein load kar deta hai.

**Family mein kaun kaun hai (comparison table):**

|Device|Capacity|Use Case|Compute?|
|---|---|---|---|
|**Snowcone**|~8 TB (HDD) / 14 TB (SSD)|Small, edge, space-constrained locations; can be mailed OR connected online via DataSync|Yes (small EC2 instances)|
|**Snowball Edge (Storage Optimized)**|~80 TB usable|Large-scale data migration, storage-heavy|Minimal|
|**Snowball Edge (Compute Optimized)**|~42 TB + GPU option|Edge computing — ML inference, video processing at edge|Yes (EC2, Lambda)|
|**Snowmobile**|Up to 100 PB per truck|Exabyte-scale, literal shipping container on a truck|No|

**Decision tree (exam-style thinking):**

```
Data size?
├── < 10 TB, need edge compute too → Snowcone
├── 10–80 TB, mainly storage → Snowball Edge Storage Optimized
├── Need GPU/compute at edge → Snowball Edge Compute Optimized
└── > 10 PB (seriously huge) → Snowmobile
```

**The bandwidth math (exam loves this):**  
Rule of thumb — if transferring your data over your available internet connection would take **more than a week**, physical transfer (Snowball) usually wins. AWS's own guidance: if it'd take **more than ~1 week** at your bandwidth, use Snowball instead of network transfer.

**Direction — not just "to on-prem":**

- **Import:** On-prem → AWS Cloud (most common — backups, archives, DB migration into S3)
- **Export:** AWS Cloud → on-prem (data retrieval, DR restore to local infra)

⚠️ **Exam trap:** Snowball is NOT primarily a "cloud to on-prem" service — it's bidirectional, but import (on-prem→cloud) dominates real-world usage and exam scenarios.

**What AWS is REALLY testing:**

1. **Snowcone vs Snowball Edge vs Snowmobile** — sizing based on data volume in the question (they'll give you a TB/PB number, you match device).
2. **Snowball ≠ pure storage** — Compute Optimized variants run **Lambda/EC2 at the edge**, useful in disconnected/remote environments (oil rigs, ships, field research) — not just "big USB drive."
3. **AWS DataSync** is the sister service for **online** large-scale transfer (when you DO have decent bandwidth) — don't confuse the two. Snowball = offline/physical, DataSync = online/automated.
4. **Security:** Data on Snowball devices is encrypted (256-bit), and device is tamper-resistant — often tested alongside shared responsibility model questions.

**One-line memory hook:** _Snowball = "jab internet slow, courier bhejo"; Snowmobile = "jab data itna bada, truck bhejo."_
---

## 8️⃣ Master Comparison & Decision Tree

### 🔑 Final Recap Table

|Service|Best For|Key Trait|
|---|---|---|
|**S3**|Static web assets, backups, general object storage|Scalable, cheap, not for frequent rewrites|
|**EBS**|Databases, transactional workloads on single EC2|Block-level, low-latency, high IOPS|
|**EFS**|Shared file access across many instances/devices|Multi-AZ, auto-scaling file system|
|**Storage Gateway**|Hybrid on-prem ↔ cloud, minimal workflow change|Bridges file/block/tape to S3/EBS/Glacier|
|**Elastic Disaster Recovery**|Fast full-server recovery after disaster|Continuous block-level replication|

### 🌳 Decision Tree

```
Need to store data on AWS?
│
├── Is it structured & needs frequent querying?
│     └── YES → Use a Database (RDS, DynamoDB, etc.)
│
├── Does ONE EC2 instance need fast, persistent block-level storage?
│     └── YES → EBS
│
├── Do MULTIPLE instances need simultaneous shared file access?
│     └── YES → EFS (Linux/NFS) or FSx (Windows/SMB, Lustre)
│
├── Is it unstructured data (media, backups, static site, logs)?
│     └── YES → S3 (pick storage class based on access frequency)
│
├── Is it on-prem data that needs a cloud backend WITHOUT changing workflow?
│     └── YES → Storage Gateway (File / Volume / Tape based on protocol)
│
└── Need fast recovery of entire servers after failure/disaster?
      └── YES → AWS Elastic Disaster Recovery
```

### 🧠 One-Line Exam Trigger Phrases

|Phrase in the question|Correct Service|
|---|---|
|"static website / web assets"|**S3**|
|"database on EC2 / rapid read-write, high IOPS"|**EBS** (Provisioned IOPS for high performance)|
|"multiple users/devices need simultaneous shared access to files"|**EFS**|
|"minimize changes to on-prem workflow, still want cloud backup"|**Storage Gateway**|
|"recover physical/virtual servers quickly after a disaster"|**Elastic Disaster Recovery**|
|"data loss when VM crashed, need persistence independent of instance"|**EBS**|
|"archive data accessed a few times a year, cost is priority"|**S3 Glacier Deep Archive**|
|"bucket policy allows public access but users still can't view objects"|**Block Public Access setting**|

---

## 9️⃣ Final Revision Kit

### 📋 Acronym Cheat Sheet

|Acronym|Full Form|
|---|---|
|EBS|Elastic Block Store|
|S3|Simple Storage Service|
|EFS|Elastic File System|
|FSx|(Windows/Lustre File Storage)|
|DLM|Data Lifecycle Manager|
|VTL|Virtual Tape Library|
|IA|Infrequent Access|
|DRS|(AWS) Elastic Disaster Recovery|
|NFS|Network File System|
|RPO|Recovery Point Objective|

### 🎯 Top 20 Revision Points

1. Block storage = fixed-size blocks, only changed block rewritten → EBS.
2. Object storage = data+metadata+key, entire object rewritten on change → S3.
3. File storage = hierarchical, shared access, NFS-based → EFS.
4. Instance Store = free, low-latency, but **volatile** (dies on stop/terminate).
5. EBS volumes have an **independent lifecycle** — persist after instance termination.
6. EBS volumes can be detached/reattached to another instance (same AZ).
7. EBS Snapshots are **incremental** after the first (full) snapshot.
8. Deleting a snapshot only removes data unique to it; shared data is preserved.
9. **AWS Data Lifecycle Manager (DLM)** automates snapshot creation/retention/deletion.
10. S3 objects max **5 TB**; buckets have **no size cap**.
11. S3 durability = **11 nines (99.999999999%)** — this is durability, not uptime/availability.
12. S3 is **private by default**; access needs explicit bucket policies/ACLs.
13. **Block Public Access** at account/bucket level **overrides** bucket policies — top exam trap.
14. S3 Storage Classes trade cost vs retrieval speed: Standard → IA → Intelligent-Tiering → Glacier tiers.
15. S3 Lifecycle Policies = Transition actions (move between classes) + Expiration actions (delete).
16. EFS is **regional**, replicates across multiple AZs, supports thousands of concurrent NFS connections.
17. EFS **automatically scales** storage up and down — no manual provisioning.
18. Storage Gateway types: **S3 File Gateway** (files→S3), **Volume Gateway** (block→EBS, Cached/Stored modes), **Tape Gateway** (virtual tape→S3/Glacier).
19. Elastic Disaster Recovery = continuous block-level replication for fast full-server recovery.
20. When a question says "multiple instances, shared access, same files simultaneously" → answer is almost always **EFS**, not EBS or S3.

### 🧩 Common CCP Question Patterns

- "A company experienced data loss when a VM crashed. How does AWS solve this?" → **EBS independent lifecycle**
- "Users report they can't access public S3 images despite a public bucket policy." → **Block Public Access**
- "On-prem app can't change its workflow but wants cloud backup." → **Storage Gateway (pick type based on protocol)**
- "Data accessed a few times a year, cost is the top priority." → **S3 Glacier Deep Archive**
- "Multiple EC2 instances need to read/write the same files at once." → **EFS**
- "Need fast, low-latency scratch storage, don't care about persistence." → **Instance Store**

### 🧮 Final Decision Matrix

|Requirement|Pick|
|---|---|
|Persistent block storage, single instance|EBS|
|Temporary, ultra-low-latency, free|Instance Store|
|Object storage, HTTP access, unlimited scale|S3|
|Shared file access across many instances|EFS|
|Windows-native file shares / HPC workloads|FSx|
|Hybrid on-prem + cloud, minimal workflow change|Storage Gateway|
|Fast full-server disaster recovery|Elastic Disaster Recovery|
|Structured, queryable, frequently modified data|RDS / Database services|

### 🔗 Cross-links to Related AWS Services

- **Databases module** → RDS, DynamoDB, Aurora (deep dive on structured data storage)
- **Compute module** → EC2 (instance store relationship), Lambda (stateless, no persistent local storage)
- **Security module** → KMS (encryption for EBS/S3), IAM (bucket policies, access control)
- **Networking module** → Direct Connect/VPN (often paired with Storage Gateway for hybrid setups)

---

## ✅ Module 6 — Complete

**Coverage check:** Block/Object/File fundamentals ✔ | EBS + Snapshots + DLM ✔ | Instance Store comparison ✔ | S3 + Storage Classes + Lifecycle + Security ✔ | EFS + FSx pointer ✔ | Storage Gateway (all 3 types) ✔ | Elastic Disaster Recovery ✔ | Decision tree + trigger phrases ✔ | Exam traps ✔

**Next up:** Module 7 (per your curriculum sequence).

