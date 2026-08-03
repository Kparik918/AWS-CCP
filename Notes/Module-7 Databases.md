# Module 7 — AWS Databases

### AWS Certified Cloud Practitioner (CLF-C02) — Complete Study Guide

---

## 📋 Module Roadmap

| #   | Topic                                                             | Exam Frequency |
| --- | ----------------------------------------------------------------- | :------------: |
| 1   | Database Fundamentals (Relational vs Non-Relational)              |     ★★★★★      |
| 2   | AWS DMS (Database Migration Service)                              |     ★★★☆☆      |
| 3   | Amazon RDS                                                        |     ★★★★★      |
| 4   | Amazon Aurora                                                     |     ★★★★★      |
| 5   | NoSQL & Amazon DynamoDB                                           |     ★★★★★      |
| 6   | Amazon ElastiCache                                                |     ★★★★☆      |
| 7   | DynamoDB Accelerator (DAX)                                        |     ★★★☆☆      |
| 8   | Purpose-Built Databases (DocumentDB, Neptune, Managed Blockchain) |     ★★★☆☆      |
| 9   | AWS Backup                                                        |     ★★★☆☆      |
| 10  | Self-Managed DB on EC2 vs Managed AWS DB Service                  |     ★★★★☆      |

**Core CLF-C02 objective mapped here:** Domain 2 (Cloud Architecture) — identify appropriate AWS service based on compute, database, or storage needs; Domain 4 (Billing & Support) — pricing/managed-service value proposition.

---

## 1. Database Fundamentals

A **database** is an organized collection of data — think of it as many tables/collections working together so an application can store, retrieve, and relate information reliably.

### 🍵 Hinglish Analogy — Coffee Shop Register

Socho ek **Coffee Store Database** hai. Isme do tables hain:

- **`coffee`** table → customer ki details rakhta hai (`customer_id`, `customer_name`, `phone`)
- **`orders`** table → order ki details rakhta hai (`order_id`, `product`, `customer_id`)

Dono tables ke beech `customer_id` common hai — ye ek **relationship** bana deta hai jisse hum tables ko **join** karke poori picture nikaal sakte hain (kis customer ne kya order kiya). Isi relationship ki wajah se ise **relational database** kehte hain.

### Two Broad Families

```
                    DATABASES
                       │
       ┌───────────────┴───────────────┐
       │                               │
  RELATIONAL (SQL)              NON-RELATIONAL (NoSQL)
  Fixed schema, tables,         Flexible schema, key-value
  rows, columns, joins          / document / graph structures
  → RDS, Aurora                 → DynamoDB, DocumentDB, Neptune
```

| Aspect        | Relational (SQL)                      | Non-Relational (NoSQL)               |
| ------------- | ------------------------------------- | ------------------------------------ |
| Schema        | Fixed, rigid — every row same columns | Flexible — items can differ          |
| Structure     | Tables with rows & columns            | Key-value, document, graph, etc.     |
| Relationships | Strong (joins via foreign keys)       | Weak/denormalized                    |
| Best for      | Structured, transactional data        | Rapidly changing, massive-scale data |
| AWS Examples  | RDS, Aurora                           | DynamoDB, DocumentDB, Neptune        |

**What AWS is REALLY testing:** AWS isn't testing whether you can define "table" or "row." AWS is testing whether you can read a business scenario and immediately know: _does this data have a rigid, relationship-heavy shape (→ RDS/Aurora), or is it unpredictable/scales massively (→ DynamoDB)?_

---

## 2. AWS Database Migration Service (AWS DMS)

**Definition:** A service that migrates databases into AWS (or between databases) — from on-premises, EC2, or another cloud — into RDS, Aurora, or other targets.

|Section|Detail|
|---|---|
|Why AWS built it|Manually migrating databases risks long downtime and data loss|
|Problem it solves|Moving a live production database with minimal/zero downtime|
|Key capability|Source database **stays fully operational** during migration|
|When to use|Any homogeneous (Oracle→Oracle) or heterogeneous (Oracle→Aurora, using **AWS Schema Conversion Tool** alongside) migration|
|When NOT to use|You're not migrating a database at all — this isn't a general data-transfer tool (use DataSync/Transfer Family for files)|

**⚠ Common Exam Trap:** DMS is for **migrating**, not for ongoing replication as a permanent solution (though it can do continuous replication). Don't confuse DMS (databases) with **AWS DataSync** (files/storage) or **Snow Family** (bulk offline transfer).

**30-Second Revision**

- **Definition:** Migrates databases into/within AWS with minimal downtime
- **Use case:** On-prem Oracle DB → Amazon Aurora, live cutover
- **Alternative:** Manual export/import (slow, downtime-heavy)
- **Pricing:** Pay for the replication instance (compute) while migration runs
- **Trap:** Not a general file transfer tool
- **Exam Importance:** ★★★☆☆

---

## 3. Amazon RDS (Relational Database Service)

### Definition

A **managed** service for running relational databases in the cloud. AWS handles everything an on-prem DBA would normally do manually.

### Why AWS Provides It

Running your own database server means you handle OS patching, hardware failure, backups, replication, and scaling yourself. RDS removes that operational burden so teams focus on the application, not the database plumbing.

### What RDS Manages For You

|Task|Who handles it|
|---|---|
|OS/DB engine patching|AWS (automated)|
|Backups|AWS (automated + point-in-time recovery)|
|Disaster recovery|AWS (via Multi-AZ)|
|Failover|AWS (automatic, no manual intervention)|
|Hardware redundancy|AWS|
|Query tuning, schema design|**You**|

### Supported Engines

MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora (Aurora is technically an RDS-family engine but is treated as its own product due to its architecture — see Section 4).

### High Availability — Multi-AZ Deployments

RDS **automatically replicates data to a standby instance in a different Availability Zone**. During a system failure, scheduled maintenance, or an AZ disruption, RDS **automatically fails over to the standby** — no manual intervention needed. This gives continuous operation with minimal downtime.

```
        Availability Zone A                 Availability Zone B
     ┌───────────────────────┐          ┌───────────────────────┐
     │   RDS Primary (Live)  │──sync──▶ │   RDS Standby (Idle)  │
     │  handles all traffic  │  repl.   │  activates on failure │
     └───────────────────────┘          └───────────────────────┘
              │ AZ-A goes down ──▶ automatic failover to AZ-B
```

> **Read Replicas ≠ Multi-AZ standby.** Read Replicas are for **scaling read traffic** (can be same or cross-region, and are queryable). A Multi-AZ **standby** is for **disaster recovery** and is not normally queryable directly.

### Performance & Monitoring

- **Automated backups + Read Replicas** offload read traffic from the primary instance.
- **RDS Performance Insights** gives real-time monitoring of database load, helping you spot and fix bottlenecks quickly.

### Security

Multiple layers: **VPC isolation**, **encryption at rest and in transit**, automated backups, and Multi-AZ resiliency against failures.

### Pricing Model (CCP depth)

Pay-as-you-go for the compute instance + storage consumed — no large upfront hardware investment. This is the core managed-service value pitch: lower **upfront** cost, lower **operational** cost (patching/backup/monitoring automated).

### When to Use RDS

- You need a traditional relational/SQL database
- Your workload needs joins, transactions, strict schema
- You want AWS to handle admin overhead

### When NOT to Use RDS

- Data has no fixed schema or changes shape frequently → **DynamoDB**
- You need extreme write/read throughput with near-instant replica sync → **Aurora**
- You need full OS-level control of the database server → **Self-managed DB on EC2**

**What AWS is REALLY testing:** Not "what is RDS." AWS wants to know if you understand _why paying for a managed service is often cheaper than "free" self-hosting_ once you count staff time, downtime risk, and patching effort.

**⚠ Common Exam Traps**

- RDS is **not serverless** by default (Aurora Serverless is a separate variant)
- Multi-AZ is for **availability/DR**, not read scaling — that's what Read Replicas are for
- RDS still requires **you** to choose instance size/storage — it's managed, not fully autonomous

### 🍵 Hinglish Analogy — Restaurant with Full Staff

RDS ek **fully-staffed restaurant** jaisa hai — chef (compute), waiter (queries), cleaning staff (patching), sab AWS provide karta hai. Tumhe bas menu (schema) design karna hai aur order (queries) dena hai.

**30-Second Revision**

- **Definition:** Managed relational database service (MySQL, PostgreSQL, Oracle, SQL Server, MariaDB)
- **Use case:** Traditional structured/transactional apps needing joins
- **Alternative:** Aurora (faster), DynamoDB (non-relational), self-managed DB on EC2 (full control)
- **Pricing:** Pay-as-you-go compute + storage
- **Common Trap:** Multi-AZ ≠ read scaling; that's Read Replicas
- **Exam Importance:** ★★★★★

---

## 4. Amazon Aurora

### Definition

AWS's own **cloud-native, MySQL- and PostgreSQL-compatible** relational database engine, re-architected for the cloud from the ground up — not just "RDS with extra features."

### Why AWS Built It

Traditional RDS uses instance-attached (EBS) storage with "normal" database-style replication — good, but not built to exploit the cloud's distributed nature. Aurora was designed specifically to remove that ceiling.

### The Core Architectural Difference

|                                            | Amazon RDS                                  | Amazon Aurora                                                                                    |
| ------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Storage model                              | Traditional instance-attached (EBS) storage | **Distributed, shared storage layer** across 3 AZs                                               |
| Replica sync                               | Normal database replication (slower)        | Compute nodes (writer + replicas) read directly from shared storage → **near-instant sync**      |
| Backup performance impact                  | Can add load                                | Continuous backup is **baked into the storage layer**, not bolted on — near-zero performance hit |
| Throughput (MySQL-compatible)              | Standard MySQL baseline                     | Up to **5x** the throughput of standard MySQL                                                    |
| Max read replicas                          | Fewer, and slower to sync                   | Up to **15**, across Availability Zones                                                          |
| Backup retention (continuous, incremental) | Standard automated backup window            | Continuous + incremental, restorable up to **35 days**                                           |
| Scaling                                    | Traditional (manual/planned)                | Automatic storage scaling                                                                        |
| Maturity                                   | "Traditional"                               | "Modern" cloud-native                                                                            |

```
        RDS Storage Model                      Aurora Storage Model
   ┌───────────┐   ┌───────────┐         ┌────────────────────────────┐
   │  Primary  │──▶│  Standby  │         │   Distributed Shared Storage │
   │ (own EBS) │   │ (own EBS) │         │        (across 3 AZs)        │
   └───────────┘   └───────────┘         └───────┬─────────┬───────────┘
                                                  │         │
                                            ┌─────▼───┐ ┌───▼─────┐
                                            │ Writer  │ │ Replica │  ...up to 15
                                            └─────────┘ └─────────┘
```

### When to Use Aurora

- You're already using MySQL/PostgreSQL and want higher performance without re-architecting the app
- You need many fast-syncing read replicas
- High-transaction workloads (I/O distributed across multiple storage nodes)

### When NOT to Use Aurora

- Budget-constrained simple workloads where standard RDS is "good enough" (Aurora typically costs more)
- Non-relational/flexible-schema data → DynamoDB
- Need Oracle/SQL Server specifically → Aurora doesn't support these engines; stick with RDS

**What AWS is REALLY testing:** Whether you know Aurora isn't "RDS v2" — it's testing if you understand _why_ it's faster: the storage architecture itself, not just "better hardware."

**⚠ Common Exam Trap:** Questions describing "high throughput," "fast replica sync," or "continuous backup with minimal performance cost" almost always point to **Aurora**, not RDS — even if the question never says the word "Aurora."

### 🍵 Hinglish Analogy

RDS = traditional dhaba jaha har table apna alag kitchen use karta hai (slow, independent). Aurora = ek **central shared kitchen** jisse saare tables (replicas) directly khaana utha rahe hain — isliye sabko ekdum fresh aur fast mil raha hai.

**30-Second Revision**

- **Definition:** Cloud-native, MySQL/PostgreSQL-compatible DB with distributed shared storage
- **Use case:** High-throughput, high-availability relational workloads
- **Alternative:** RDS (cheaper, traditional), DynamoDB (non-relational)
- **Pricing:** Higher than RDS, but pay-as-you-go
- **Common Trap:** "5x throughput," "near-instant replica sync," "continuous backup, no performance hit" = Aurora signal words
- **Exam Importance:** ★★★★★

---

## 5. NoSQL & Amazon DynamoDB

### Why NoSQL Exists

Relational databases enforce a **rigid schema** — every row must have the same columns. Real businesses often can't guarantee that: one customer order might have extra fields (size, loyalty points, delivery address) that another doesn't. NoSQL removes the fixed-schema constraint.

### Terminology Translation

|SQL Term|NoSQL Term|
|---|---|
|Row|**Item**|
|Column|**Attribute**|
|Table|Table (same name, different internal structure)|
|Primary Key|Primary Key (still required — the _only_ thing every item must share)|

### 🍵 Worked Example — Coffee Orders (NoSQL)

```json
// Item 1
{
  "order_id": "1001",
  "customer_name": "Krish",
  "coffee": "Cappuccino",
  "price": 150
}

// Item 2 — has extra attributes, and that's fine
{
  "order_id": "1002",
  "customer_name": "Aman",
  "coffee": "Latte",
  "price": 180,
  "size": "Large",
  "extra_shot": true
}

// Item 3 — even a nested object is fine
{
  "order_id": "1003",
  "customer_name": "Priya",
  "coffee": "Espresso",
  "price": 100,
  "loyalty_points_used": 20,
  "delivery_address": { "city": "Ahmedabad", "pincode": "380001" }
}
```

Har item ke columns/attributes alag ho sakte hain — sirf `order_id` (primary key) sabme common hai. **Yehi hai NoSQL ka main differentiator.**

### Amazon DynamoDB

**Definition:** AWS's fully managed, serverless, key-value/document NoSQL database.

|Feature|Detail|
|---|---|
|Latency|**Single-digit millisecond** performance at any scale|
|Infrastructure|**Serverless** — zero server management, AWS handles all of it|
|Scaling|**Auto scaling with provisioned capacity** — automatically adjusts capacity to match real traffic; keeps performance consistent during unpredictable peaks while optimizing cost during quieter periods|
|Global reach|**Global Tables** — replicate a table across multiple AWS Regions, so a global app's data is fast and available everywhere|
|Proof of scale|During **Prime Day 2024**, DynamoDB handled tens of trillions of API calls over 48 hours, peaking at **146 million requests/second** — with **zero manual scaling intervention**|

### When to Use DynamoDB

- Data shape is unpredictable or evolves over time
- You need massive scale with no infrastructure management
- You need consistently low latency regardless of traffic spikes

### When NOT to Use DynamoDB

- You need complex multi-table joins / strict relational integrity → RDS/Aurora
- Your data is inherently tabular and stable in shape

**What AWS is REALLY testing:** Not the definition of NoSQL. AWS is testing whether, given a scenario ("unpredictable traffic," "wants to focus on features, not database management," "schema keeps changing"), you can immediately eliminate the RDS/Aurora options and land on DynamoDB.

### ⚠ Solved Exam Question (from your notes)

> _A staffing resource company is building an application that must store employee information with unpredictable traffic patterns. Their application requires consistent performance at all times, and the development team wants to focus on features rather than database management tasks. Which Amazon DynamoDB capability BEST addresses the needs for this workload?_

|Option|Verdict|
|---|---|
|Manual configuration of read/write capacity units|❌ Contradicts "focus on features, not DB management"|
|**Auto scaling with provisioned capacity**|✅ **Correct** — handles unpredictable traffic + consistent performance automatically|
|Fixed storage limit allocation|❌ Not a real DynamoDB selling point, contradicts scalability need|
|Predefined schema enforcement|❌ Opposite of DynamoDB's flexible-schema nature|

**Technique used (and it's a valid exam strategy):** eliminate options that are **definitely wrong** first, then eliminate options that are **probably wrong**, until one clearly correct answer remains — even without 100% certainty upfront.

**30-Second Revision**

- **Definition:** Fully managed, serverless NoSQL key-value/document database
- **Use case:** Unpredictable traffic, flexible/evolving schema, need serverless scale
- **Alternative:** RDS/Aurora (structured, relational data)
- **Pricing:** Pay for provisioned/auto-scaled capacity (or on-demand mode)
- **Common Trap:** "Focus on features, not DB management" + "unpredictable traffic" = DynamoDB auto scaling signal
- **Exam Importance:** ★★★★★

---

## 6. RDS/Aurora vs DynamoDB — The Core CCP Decision

### Comparison Table

|Aspect|RDS / Aurora|DynamoDB|
|---|---|---|
|Data model|Relational (tables, joins)|NoSQL (key-value/document)|
|Schema|Fixed|Flexible|
|Scaling|Vertical (mostly), some read scaling|Massive horizontal, serverless|
|Latency|Milliseconds, depends on query complexity|Single-digit ms, consistently|
|Management|Managed, but you pick instance type/size|Fully serverless, no instance sizing|
|Best for|Known, relationship-heavy data|Unpredictable, rapidly evolving data|

### Quick Mental Model (Exam-Ready)

> **RDS/Aurora = "I know my data shape, I need relationships between tables."** **DynamoDB = "My data shape changes, I need it to scale massively without me managing servers."**

### Decision Tree

```
Need a database?
        │
        ▼
Is the data structured with clear relationships (joins needed)?
        │
   ┌────┴────┐
  YES        NO
   │          │
   ▼          ▼
Need extreme         Use DynamoDB
throughput/           (flexible schema,
fast replica sync?    serverless, massive scale)
   │
 ┌─┴─┐
YES   NO
 │     │
 ▼     ▼
Aurora  RDS
```

---

## 7. Amazon ElastiCache

### Definition

A **managed in-memory caching service** that sits between the application/customer and the database, storing frequently-requested (cached) data for extremely fast retrieval.

### Why It Exists / Problem It Solves

Every read that hits the database costs time and money. If the same data is requested repeatedly (e.g., a popular product page), re-querying the database each time is wasteful.

### How It Works

```
   Customer Request
         │
         ▼
   ┌───────────┐   cache hit?  ──Yes──▶  Respond directly (fast, cheap)
   │ElastiCache│
   └───────────┘
         │ cache miss
         ▼
   ┌───────────┐
   │    RDS    │ ──▶ Respond (slower) + populate cache for next time
   └───────────┘
```

If the requested data is found in the cache (cache hit), the request **never even reaches RDS** — response comes straight from ElastiCache. This reduces **latency** and reduces **cost** (fewer read operations hitting the database).

### Key Facts

- **Serverless-style management** — scaling and infrastructure are handled by AWS
- Built on open-source engines: **Valkey** and **Memcached**
- Reduces read load on the primary database → cost savings

### When to Use

- Read-heavy applications with repeated/hot queries
- Need to shave milliseconds off response time (session storage, leaderboards, real-time analytics)

### When NOT to Use

- Write-heavy workloads with little data reuse
- Data must always be perfectly fresh (cache can serve slightly stale data)

**What AWS is REALLY testing:** Whether you understand ElastiCache's _position in the architecture_ (in front of the database) and its _dual benefit_ — lower latency **and** lower cost — not just "it's a cache."

**⚠ Common Exam Trap:** Don't confuse ElastiCache (general-purpose cache for RDS/other databases) with **DAX** (cache built specifically and only for DynamoDB — see next section).

### 🍵 Hinglish Analogy

ElastiCache ek **tez waiter** jaisa hai jo popular dishes (frequently accessed data) already tray me leke ready khada hai — customer ko kitchen (database) tak jaane ki zaroorat hi nahi padti.

**30-Second Revision**

- **Definition:** Managed in-memory caching layer in front of a database
- **Use case:** Reduce latency & DB read load for frequently accessed data
- **Alternative:** DAX (DynamoDB-only caching)
- **Pricing:** Pay for cache node capacity
- **Common Trap:** ElastiCache works with RDS/general DBs; DAX works only with DynamoDB
- **Exam Importance:** ★★★★☆

---

## 8. DynamoDB Accelerator (DAX)

### Definition

An in-memory caching layer **built exclusively for DynamoDB**, using a DynamoDB-native caching engine.

|Aspect|Detail|
|---|---|
|Works with|**Only DynamoDB** (not RDS, not other databases)|
|Purpose|Further reduce DynamoDB read latency (microseconds) for read-heavy workloads|
|Relationship to ElastiCache|DAX is purpose-built and tightly integrated for DynamoDB; ElastiCache is general-purpose|

**⚠ Common Exam Trap:** If a question says "cache **specifically** for DynamoDB" → **DAX**. If it says "cache in front of a relational database (RDS)" or is generic → **ElastiCache**.

**30-Second Revision**

- **Definition:** DynamoDB-native in-memory cache
- **Use case:** Microsecond-level read performance for DynamoDB
- **Alternative:** ElastiCache (general purpose, works with RDS too)
- **Pricing:** Pay for DAX cluster nodes
- **Common Trap:** DAX ≠ works with RDS
- **Exam Importance:** ★★★☆☆

---

## 9. Purpose-Built Databases

AWS provides several databases each optimized for a **specific data shape** — a classic CCP scenario-matching topic.

|Service|Data Type|Real-World Use Case|
|---|---|---|
|**Amazon DocumentDB**|Document data (JSON), **MongoDB-compatible**|Content management, catalogs, semi-structured/complex data|
|**Amazon Neptune**|Graph data — relationships & connections|Social networks (e.g., LinkedIn-style connections), fraud detection, recommendation engines|
|**Amazon Managed Blockchain**|Distributed ledger / blockchain|Supply chain tracking, multi-party trust, immutable transaction history|

### Amazon Neptune — Detail

Provides **low-latency, high-throughput performance for both read and write operations**, making it well suited for real-time applications working with **connected data** (e.g., "who is connected to whom" queries).

### Scenario-Matching Cheat Sheet (Exam Framing)

|Question Phrase|Correct Service|
|---|---|
|"Complex/varied/semi-structured data," "content management," "MongoDB compatibility"|**DocumentDB**|
|"Relationships," "connections," "social network," "fraud detection"|**Neptune**|
|"Supply chain," "immutable ledger," "trust between multiple parties"|**Managed Blockchain**|

**What AWS is REALLY testing:** Whether you can pattern-match business language ("social network," "supply chain," "MongoDB") to the _right purpose-built database_, without needing deep technical knowledge of graph theory or blockchain internals.

**30-Second Revision (all three)**

- **Definition:** Purpose-built managed databases for non-relational, non-key-value data shapes
- **Use case:** Document (DocumentDB) / Graph (Neptune) / Ledger (Managed Blockchain)
- **Alternative:** Forcing this data into RDS or DynamoDB (inefficient/awkward)
- **Common Trap:** Mixing up which keyword maps to which service
- **Exam Importance:** ★★★☆☆

---

## 10. AWS Backup

### Definition

A **centralized, one-stop backup service** for AWS data and databases — instead of configuring backup separately for each service (RDS, DynamoDB, EFS, EC2 volumes, etc.), AWS Backup manages it all from one place with unified policies.

### When to Use

- Organizations wanting consistent backup policies (retention, scheduling) across multiple AWS services
- Compliance requirements needing centralized backup auditing

**30-Second Revision**

- **Definition:** Centralized backup management across AWS services
- **Use case:** Unified backup policy instead of per-service backup configuration
- **Alternative:** Manually configuring native backup for each service separately
- **Common Trap:** Don't confuse with RDS's own automated backups — AWS Backup is the _centralized_ layer across many services
- **Exam Importance:** ★★★☆☆

---

## 11. Self-Managed Database (on EC2) vs. Fully Managed AWS Database Service

This is a frequently tested **"when NOT to use managed services"** scenario.

### ⚠ Solved Exam Question (from your notes)

> _Which option describes a scenario where an unmanaged solution like a database installed directly onto an Amazon EC2 instance would be preferable to using a fully managed AWS database service?_

|Option|Verdict|
|---|---|
|**A developer needs full control over the database and access to its underlying OS, database installation, and configuration.**|✅ **Correct** — this is precisely what a managed service takes away from you|
|A developer has a database size smaller than the max limits imposed by RDS|❌ Not a reason to avoid managed service|
|A developer wants AWS to handle routine maintenance (backups/patching)|❌ This is an argument _for_ RDS, not against it|
|A developer wants to scale without licensing complications|❌ Also an argument _for_ a managed service|

### The Core Trade-Off

| |Managed (RDS/Aurora/DynamoDB)|Self-Managed (DB on EC2)|
|---|---|---|
|OS-level access|❌ No|✅ Full root/OS access|
|Custom DB engine version/config/plugins|Limited to what AWS supports|✅ Anything you want|
|Patching, backups, failover|AWS handles it|You handle it|
|Operational overhead|Low|High|
|Best for|Standard workloads, teams wanting to focus on the app|Highly specialized configs, legacy compatibility, licensing edge cases|

**What AWS is REALLY testing:** Whether you know managed services trade **control** for **convenience** — and can recognize the _one_ legitimate reason to give up that convenience: needing OS/engine-level control that AWS's managed layer doesn't expose.

**30-Second Revision**

- **Definition:** Running a database yourself on EC2 vs. using RDS/Aurora/DynamoDB
- **Use case for self-managed:** Need full OS/engine-level control or unsupported configuration
- **Alternative:** RDS/Aurora (managed) for everything else
- **Common Trap:** "Wants AWS to handle backups/patching/scaling" always points to _managed_, not self-managed
- **Exam Importance:** ★★★★☆

---

## 📚 Module-End Revision Kit

### Quick Summary Table

|Service|Type|Managed?|Best For|
|---|---|---|---|
|AWS DMS|Migration tool|Managed|Migrating databases into/within AWS|
|Amazon RDS|Relational|Managed|Standard SQL workloads|
|Amazon Aurora|Relational|Managed|High-throughput, fast-replicating SQL workloads|
|Amazon DynamoDB|NoSQL (key-value)|Fully serverless|Unpredictable scale, flexible schema|
|Amazon ElastiCache|In-memory cache|Managed|Reducing DB latency/cost generally|
|DAX|In-memory cache|Managed|Reducing latency for DynamoDB specifically|
|Amazon DocumentDB|NoSQL (document)|Managed|MongoDB-compatible JSON workloads|
|Amazon Neptune|NoSQL (graph)|Managed|Connected/relationship data|
|Managed Blockchain|Distributed ledger|Managed|Multi-party trust, supply chain|
|AWS Backup|Backup orchestration|Managed|Centralized backup across services|
|Self-managed DB on EC2|Any|Unmanaged|Full OS/engine control needed|

### Acronym Cheat Sheet

|Acronym|Meaning|
|---|---|
|RDS|Relational Database Service|
|DMS|Database Migration Service|
|DAX|DynamoDB Accelerator|
|NoSQL|"Not only SQL" — non-relational databases|
|AZ|Availability Zone|
|SCT|Schema Conversion Tool (pairs with DMS for heterogeneous migrations)|

### Top 20 Revision Points

1. Relational DB = fixed schema, tables joined by common keys (e.g., `customer_id`).
2. AWS DMS migrates databases into AWS with minimal source downtime.
3. RDS = managed relational DB; AWS handles patching, backups, DR, failover, redundancy.
4. RDS Multi-AZ = automatic failover to a standby in another AZ — for **availability**, not read scaling.
5. Read Replicas = for scaling **read** traffic, separate concept from Multi-AZ.
6. RDS Performance Insights = real-time load monitoring to spot bottlenecks.
7. RDS security = VPC isolation + encryption at rest/in transit.
8. Aurora = MySQL/PostgreSQL-compatible, cloud-native, distributed shared storage across 3 AZs.
9. Aurora replicas sync near-instantly because they read from shared storage, not independent copies.
10. Aurora continuous backup has near-zero performance cost — it's built into the storage layer.
11. Aurora = up to 5x MySQL throughput, up to 15 read replicas, 35-day continuous/incremental backup.
12. NoSQL = flexible schema; SQL "row"→NoSQL "item", SQL "column"→NoSQL "attribute".
13. DynamoDB = fully managed, serverless, single-digit millisecond latency.
14. DynamoDB Auto Scaling with provisioned capacity = handles unpredictable traffic automatically.
15. DynamoDB Global Tables = multi-region replication for global low-latency access.
16. Mental model: RDS/Aurora = "I know my data shape, need relationships." DynamoDB = "data shape changes, need massive serverless scale."
17. ElastiCache = general-purpose in-memory cache in front of a database; reduces latency AND cost.
18. DAX = in-memory cache built exclusively for DynamoDB.
19. DocumentDB (JSON/MongoDB) vs Neptune (graph/relationships) vs Managed Blockchain (ledger/trust) — match by keyword.
20. Choose self-managed DB on EC2 only when you need OS/engine-level control unavailable in managed services.

### Common CCP Question Patterns

- "Unpredictable traffic + wants to focus on features, not DB management" → **DynamoDB auto scaling**
- "Needs full OS/engine access and control" → **Self-managed on EC2**
- "High throughput, fast replica sync, continuous backup with low performance impact" → **Aurora**
- "Reduce read load / latency for a relational database" → **ElastiCache**
- "Reduce latency specifically for DynamoDB" → **DAX**
- "MongoDB compatibility" → **DocumentDB**
- "Social network / connections / fraud detection" → **Neptune**
- "Supply chain / multi-party ledger" → **Managed Blockchain**
- "Migrate on-prem database with minimal downtime" → **AWS DMS**
- "Centralized backup policy across many AWS services" → **AWS Backup**

### Final Decision Matrix

|Your Data / Need Is...|Choose|
|---|---|
|Structured, relational, standard performance needs|Amazon RDS|
|Structured, relational, need max performance/scale|Amazon Aurora|
|Flexible/unpredictable schema, massive serverless scale|Amazon DynamoDB|
|Need to cache in front of RDS/general DB|Amazon ElastiCache|
|Need to cache in front of DynamoDB specifically|DAX|
|JSON/document, MongoDB-compatible|Amazon DocumentDB|
|Graph/relationship-heavy data|Amazon Neptune|
|Immutable multi-party ledger|Managed Blockchain|
|Migrating an existing database into AWS|AWS DMS|
|Centralized backup across multiple services|AWS Backup|
|Full OS/engine-level control required|Self-managed DB on EC2|

### Cross-Links to Related AWS Services (Other Modules)

- **EC2** — compute host for self-managed databases; also the "no managed service" comparison point
- **VPC & Security Groups** — RDS security relies on VPC isolation covered in networking modules
- **IAM** — controls who can access/manage database resources
- **S3** — often used as a backup/export target alongside RDS/DynamoDB
- **CloudWatch** — underlying monitoring engine behind RDS Performance Insights alerts

---

_Module 7 — Databases: Complete ✅_