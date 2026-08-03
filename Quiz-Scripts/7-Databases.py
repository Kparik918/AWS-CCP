#!/usr/bin/env python3
"""
================================================================================
AWS Certified Cloud Practitioner (CLF-C02) — Practice Quiz Engine
Module 7: Database

Covers: AWS DMS | Amazon RDS | Amazon Aurora | NoSQL & Amazon DynamoDB |
        Amazon ElastiCache | DynamoDB Accelerator (DAX) |
        Purpose-Built Databases (DocumentDB, Neptune, Managed Blockchain) |
        AWS Backup | Self-Managed DB on EC2 vs Managed AWS DB Service

Run: python 7-Database.py
================================================================================
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Database"

# --------------------------------------------------------------------------
# QUESTIONS: (topic, question_text, [options], correct_answer, explanation)
# correct_answer -> single 0-based int for single-select
# correct_answer -> list/tuple of 0-based ints for multi-select ("Select TWO/THREE")
# --------------------------------------------------------------------------
QUESTIONS = [

    # ============================== AWS DMS ==============================
    ("AWS DMS",
     "What is the primary purpose of AWS Database Migration Service (DMS)?",
     ["To migrate databases into or within AWS with minimal downtime",
      "To provide in-memory caching for databases",
      "To orchestrate backups across AWS services",
      "To provide a fully managed NoSQL database"],
     0,
     "DMS is purpose-built for migrating databases while keeping the source database operational, unlike caching or backup services which solve different problems."),

    ("AWS DMS",
     "A company wants to migrate an on-premises Oracle database to Amazon Aurora, converting the schema in the process. Which TWO AWS services should be used together?",
     ["AWS DMS",
      "AWS Schema Conversion Tool (SCT)",
      "AWS DataSync",
      "Amazon ElastiCache",
      "AWS Backup"],
     [0, 1],
     "Heterogeneous migrations (different source/target engines) require SCT to convert schema and code, plus DMS to perform the actual data migration with minimal downtime."),

    ("AWS DMS",
     "During an AWS DMS migration, what happens to the source database?",
     ["It goes offline immediately",
      "It remains fully operational throughout the migration",
      "It is deleted after migration starts",
      "It becomes read-only permanently"],
     1,
     "DMS is specifically designed so the source database stays live and operational, minimizing business disruption during migration."),

    ("AWS DMS",
     "[Exam trap] A company needs to transfer large volumes of files from an on-premises file server to Amazon S3. Which service should they use instead of AWS DMS?",
     ["AWS DataSync",
      "AWS DMS",
      "Amazon RDS",
      "Amazon Aurora"],
     0,
     "DMS migrates databases, not general files; AWS DataSync (or the Snow Family for offline bulk transfer) is the correct choice for file-level data movement."),

    ("AWS DMS",
     "What do you primarily pay for while an AWS DMS migration is running?",
     ["The replication instance (compute) provisioned for the migration",
      "The number of database rows migrated",
      "A flat one-time migration fee",
      "DynamoDB read capacity units"],
     0,
     "DMS pricing is based on the compute resources (replication instance) provisioned to perform the migration, similar to paying for any running compute resource."),

    # ============================== Amazon RDS ==============================
    ("Amazon RDS",
     "Which AWS service is best described as a managed relational database service supporting engines like MySQL, PostgreSQL, and SQL Server?",
     ["Amazon RDS",
      "Amazon DynamoDB",
      "Amazon Neptune",
      "AWS Backup"],
     0,
     "RDS is AWS's core managed relational database offering, explicitly supporting these standard SQL engines while AWS handles infrastructure tasks."),

    ("Amazon RDS",
     "Which THREE of the following does AWS automatically handle when you use Amazon RDS instead of self-managing a database?",
     ["OS and database engine patching",
      "Automated backups",
      "Query tuning and schema design",
      "Schema design decisions",
      "Automatic Multi-AZ failover"],
     [0, 1, 4],
     "RDS offloads patching, backups, and automatic failover to AWS, but query tuning and schema design remain the customer's responsibility — a common exam trap."),

    ("Amazon RDS",
     "What is the primary purpose of RDS Multi-AZ deployments?",
     ["To scale read traffic across multiple regions",
      "To provide automatic failover to a standby instance for disaster recovery",
      "To reduce storage costs",
      "To enable NoSQL-style flexible schemas"],
     1,
     "Multi-AZ replicates data synchronously to a standby in a different AZ and automatically fails over during outages — it's an availability/DR feature, not a scaling one."),

    ("Amazon RDS",
     "[Exam trap] A company assumes that enabling RDS Multi-AZ will improve their application's read performance. Why is this assumption incorrect?",
     ["Multi-AZ standby instances exist for disaster recovery, not for serving read traffic",
      "Multi-AZ actually disables all read operations",
      "Multi-AZ only works with DynamoDB",
      "Multi-AZ requires manual failover, so it can't help availability"],
     0,
     "The standby instance in Multi-AZ is not normally queryable — read scaling requires Read Replicas, a completely separate RDS feature."),

    ("Amazon RDS",
     "Which RDS feature is designed specifically to scale read-heavy workloads by offloading traffic from the primary instance?",
     ["Multi-AZ standby",
      "Read Replicas",
      "RDS Performance Insights",
      "AWS Backup"],
     1,
     "Read Replicas create additional queryable copies of data specifically to handle extra read traffic, unlike the Multi-AZ standby which exists purely for failover."),

    ("Amazon RDS",
     "Which RDS feature provides real-time visibility into database load to help identify performance bottlenecks?",
     ["RDS Performance Insights",
      "Amazon ElastiCache",
      "AWS DMS",
      "DynamoDB Auto Scaling"],
     0,
     "Performance Insights is RDS's built-in monitoring dashboard that visualizes database load in real time, helping teams pinpoint bottlenecks quickly."),

    ("Amazon RDS",
     "Which of the following best describes a security foundation that Amazon RDS relies on?",
     ["VPC isolation combined with encryption at rest and in transit",
      "Public internet-only access by default",
      "Manual OS-level firewall configuration by the customer",
      "No encryption support"],
     0,
     "RDS security is built on VPC network isolation plus encryption capabilities, layered with automated backups and Multi-AZ resilience — it is not exposed to the public internet by default."),

    ("Amazon RDS",
     "Which statement about Amazon RDS pricing is accurate?",
     ["It requires large upfront hardware investment",
      "It is pay-as-you-go for compute and storage consumed",
      "It is completely free for unlimited use",
      "It only charges for backups, not compute"],
     1,
     "RDS follows the standard AWS pay-as-you-go model, charging for the compute instance and storage used, eliminating the upfront capital cost of on-prem database hardware."),

    # ============================== Amazon Aurora ==============================
    ("Amazon Aurora",
     "What makes Amazon Aurora architecturally different from standard Amazon RDS engines?",
     ["Aurora uses a distributed, shared storage layer across multiple Availability Zones",
      "Aurora only runs on a single server with no redundancy",
      "Aurora does not support automated backups",
      "Aurora requires manual replica synchronization"],
     0,
     "Aurora's core innovation is a storage layer distributed across 3 AZs that all compute nodes read from directly, fundamentally different from RDS's traditional instance-attached storage model."),

    ("Amazon Aurora",
     "Which relational database engines is Amazon Aurora compatible with? (Select TWO)",
     ["MySQL",
      "PostgreSQL",
      "Oracle",
      "SQL Server",
      "MongoDB"],
     [0, 1],
     "Aurora is compatible only with MySQL and PostgreSQL; Oracle and SQL Server remain exclusive to standard RDS, and MongoDB compatibility belongs to DocumentDB."),

    ("Amazon Aurora",
     "[Exam trap] A question describes a workload needing 'near-instant replica synchronization' and 'continuous backup with minimal performance impact.' Which service does this describe?",
     ["Amazon RDS",
      "Amazon Aurora",
      "Amazon ElastiCache",
      "AWS DMS"],
     1,
     "These are classic Aurora signal phrases — its shared storage architecture lets replicas read the same storage instantly and lets backups run continuously with near-zero performance cost."),

    ("Amazon Aurora",
     "How many read replicas can Amazon Aurora support, compared to traditional RDS?",
     ["Up to 5, fewer than RDS",
      "Up to 15, more than standard RDS typically supports",
      "Unlimited, with no maximum",
      "Aurora does not support read replicas"],
     1,
     "Aurora supports up to 15 read replicas that sync near-instantly via shared storage, significantly more than what traditional RDS replication typically supports."),

    ("Amazon Aurora",
     "What is the maximum point-in-time restore window enabled by Aurora's continuous backup?",
     ["7 days",
      "24 hours",
      "35 days",
      "Aurora does not support point-in-time restore"],
     2,
     "Aurora's continuous, incremental backups allow restoration to any point within a 35-day window, without the performance overhead of traditional scheduled backups."),

    ("Amazon Aurora",
     "A company wants improved throughput and faster replica synchronization for their existing MySQL workload without major application changes. What should they migrate to?",
     ["Amazon DynamoDB",
      "Amazon Aurora",
      "Amazon Neptune",
      "Amazon Managed Blockchain"],
     1,
     "Aurora is MySQL-compatible and offers up to 5x the throughput of standard MySQL with minimal application changes, making it the natural upgrade path."),

    ("Amazon Aurora",
     "Which of these is NOT a good reason to choose Amazon Aurora over standard RDS?",
     ["Need for higher throughput",
      "Need for many fast-syncing read replicas",
      "Extremely tight budget for a simple, low-traffic workload",
      "Need for continuous backup with minimal performance cost"],
     2,
     "Aurora typically costs more than standard RDS, so a simple, low-traffic, budget-constrained workload is better served by standard RDS rather than Aurora's premium performance features."),

    # ====================== NoSQL & Amazon DynamoDB ======================
    ("NoSQL & DynamoDB",
     "In NoSQL terminology, what is the equivalent of a 'row' in a relational database?",
     ["Attribute",
      "Item",
      "Table",
      "Schema"],
     1,
     "NoSQL databases like DynamoDB refer to individual records as 'items,' while 'attributes' correspond to relational 'columns.'"),

    ("NoSQL & DynamoDB",
     "Why do NoSQL databases like DynamoDB not require a fixed schema?",
     ["Because each item can have different attributes, with only the primary key required to be common across items",
      "Because they don't store any data permanently",
      "Because they only support numeric data types",
      "Because they are incompatible with cloud environments"],
     0,
     "NoSQL's key differentiator is flexibility — items in the same table can have completely different attributes, and the primary key is the only mandatory shared element."),

    ("NoSQL & DynamoDB",
     "What is Amazon DynamoDB?",
     ["A fully managed, serverless NoSQL key-value/document database",
      "A managed relational database service",
      "An in-memory caching layer",
      "A graph database for connected data"],
     0,
     "DynamoDB is AWS's flagship serverless NoSQL offering, requiring no infrastructure management while delivering consistent low-latency performance."),

    ("NoSQL & DynamoDB",
     "What latency does DynamoDB aim to provide, regardless of scale?",
     ["Single-digit millisecond performance",
      "Multi-second latency",
      "Latency depends entirely on manual tuning",
      "No latency guarantees exist"],
     0,
     "DynamoDB is engineered to deliver consistent single-digit millisecond latency even as request volume scales dramatically."),

    ("NoSQL & DynamoDB",
     "A staffing company is building an application with unpredictable traffic patterns, needs consistent performance at all times, and wants developers to focus on features rather than database management. Which DynamoDB capability BEST addresses this?",
     ["Manual configuration of read/write capacity units",
      "Auto scaling with provisioned capacity",
      "Fixed storage limit allocation",
      "Predefined schema enforcement"],
     1,
     "Auto scaling with provisioned capacity automatically adjusts throughput to match unpredictable demand, directly satisfying both the consistent-performance requirement and the desire to avoid manual database management."),

    ("NoSQL & DynamoDB",
     "Which DynamoDB feature allows a table's data to be replicated across multiple AWS Regions for global low-latency access?",
     ["Global Tables",
      "Read Replicas",
      "Multi-AZ deployments",
      "DynamoDB Streams"],
     0,
     "Global Tables provide multi-region, multi-active replication so a globally distributed application can read and write data with low latency from any participating region."),

    ("NoSQL & DynamoDB",
     "[Exam trap] A company has data with clear, stable relationships between entities and needs complex multi-table joins. Which database type should they choose?",
     ["DynamoDB",
      "A relational database like RDS or Aurora",
      "Amazon ElastiCache",
      "Amazon Managed Blockchain"],
     1,
     "Despite DynamoDB's popularity, workloads requiring complex joins and stable relational integrity are still best served by relational databases, not NoSQL key-value stores."),

    ("NoSQL & DynamoDB",
     "What is the DynamoDB equivalent of a relational database 'column'?",
     ["Item",
      "Attribute",
      "Table",
      "Primary Key"],
     1,
     "In DynamoDB terminology, 'attribute' maps to a relational 'column,' describing a single piece of data within an item."),

    ("NoSQL & DynamoDB",
     "Which scaling model does DynamoDB primarily use to handle massive, unpredictable traffic without manual server management?",
     ["Vertical scaling only",
      "Serverless, horizontal auto scaling",
      "Manual provisioning of EC2 instances",
      "Fixed capacity with no scaling"],
     1,
     "DynamoDB's serverless architecture scales horizontally and automatically, which is how it handled tens of trillions of requests during peak events without manual intervention."),

    # ============================ Amazon ElastiCache ============================
    ("Amazon ElastiCache",
     "What is the primary function of Amazon ElastiCache?",
     ["A managed in-memory caching service that sits between the application and the database",
      "A managed relational database engine",
      "A service for migrating databases",
      "A centralized backup service"],
     0,
     "ElastiCache stores frequently requested data in memory so it can be served instantly without querying the underlying database."),

    ("Amazon ElastiCache",
     "What happens during a 'cache hit' in an ElastiCache-backed architecture?",
     ["The request is served directly from the cache without reaching the database",
      "The request always fails",
      "The database is queried twice",
      "The cache is cleared automatically"],
     0,
     "A cache hit means the requested data already exists in ElastiCache, so the response is returned immediately without adding load to the underlying database."),

    ("Amazon ElastiCache",
     "What are the TWO primary benefits of placing ElastiCache in front of a database?",
     ["Reduced latency",
      "Reduced cost from fewer database read operations",
      "Increased data write consistency",
      "Elimination of the need for any database",
      "Guaranteed real-time data freshness at all times"],
     [0, 1],
     "ElastiCache's dual value proposition is faster response times (lower latency) and lower database load (fewer reads means cost savings) — it does not replace the database or guarantee perfectly fresh data."),

    ("Amazon ElastiCache",
     "Which open-source engines does Amazon ElastiCache support?",
     ["Valkey and Memcached",
      "MySQL and PostgreSQL",
      "MongoDB and Cassandra",
      "Hadoop and Spark"],
     0,
     "ElastiCache is built on the open-source Valkey and Memcached caching engines, not on relational or big-data engines."),

    ("Amazon ElastiCache",
     "[Exam trap] A question describes a 'general-purpose cache in front of a relational database' without naming a specific caching product. Which service is being described?",
     ["DAX",
      "Amazon ElastiCache",
      "Amazon Aurora",
      "AWS Backup"],
     1,
     "ElastiCache is the general-purpose caching layer suitable for RDS and other databases, whereas DAX is reserved exclusively for DynamoDB."),

    ("Amazon ElastiCache",
     "What type of workload benefits most from Amazon ElastiCache?",
     ["Write-heavy workloads with little data reuse",
      "Read-heavy applications with frequently repeated queries",
      "Applications requiring perfectly fresh data on every single request",
      "Batch processing jobs with no repeated reads"],
     1,
     "Caching only helps when the same data is requested repeatedly; read-heavy workloads with 'hot' data see the biggest latency and cost benefits."),

    # ============================ DAX ============================
    ("DAX",
     "What is Amazon DynamoDB Accelerator (DAX)?",
     ["An in-memory caching layer built exclusively for DynamoDB",
      "A general-purpose cache for any AWS database",
      "A backup service for DynamoDB",
      "A migration tool for NoSQL databases"],
     0,
     "DAX is a DynamoDB-native caching engine, purpose-built and tightly integrated to accelerate DynamoDB reads specifically — unlike ElastiCache's general-purpose design."),

    ("DAX",
     "[Exam trap] A question states a company wants to cache reads 'specifically for their DynamoDB table' to achieve microsecond response times. Which service should they use?",
     ["Amazon ElastiCache",
      "DAX",
      "Amazon Aurora",
      "AWS Backup"],
     1,
     "The phrase 'specifically for DynamoDB' is the key signal — DAX is the purpose-built caching layer for DynamoDB, delivering microsecond-level latency for repeated reads."),

    ("DAX",
     "Can DAX be used to cache data for an Amazon RDS relational database?",
     ["Yes, DAX works with any AWS database",
      "No, DAX works exclusively with DynamoDB",
      "Yes, but only for MySQL-based RDS instances",
      "Only if ElastiCache is disabled first"],
     1,
     "DAX is scoped exclusively to DynamoDB; a relational database like RDS would need ElastiCache instead for caching."),

    ("DAX",
     "What is the main performance benefit DAX provides over standard DynamoDB read requests?",
     ["It converts DynamoDB into a relational database",
      "It further reduces read latency into the microsecond range for read-heavy workloads",
      "It eliminates the need for a primary key",
      "It increases DynamoDB's write throughput"],
     1,
     "DAX sits in front of DynamoDB and caches results, pushing already-fast millisecond reads down into microsecond territory for repeated read patterns."),

    # ==================== Purpose-Built Databases ====================
    ("Purpose-Built Databases",
     "Which AWS database service is MongoDB-compatible and designed for document/JSON data?",
     ["Amazon DocumentDB",
      "Amazon Neptune",
      "Amazon Managed Blockchain",
      "Amazon Aurora"],
     0,
     "DocumentDB is purpose-built for JSON document workloads and is compatible with MongoDB, making it the natural fit for content management and catalog-style semi-structured data."),

    ("Purpose-Built Databases",
     "A company is building a social network feature that needs to efficiently query 'who is connected to whom' relationships. Which database should they use?",
     ["Amazon DynamoDB",
      "Amazon Neptune",
      "Amazon DocumentDB",
      "AWS Backup"],
     1,
     "Neptune is a purpose-built graph database optimized for low-latency, high-throughput queries on connected data such as social graphs and relationship networks."),

    ("Purpose-Built Databases",
     "Which AWS service is best suited for building a supply chain tracking system requiring an immutable, multi-party trusted ledger?",
     ["Amazon Managed Blockchain",
      "Amazon RDS",
      "Amazon ElastiCache",
      "AWS DMS"],
     0,
     "Managed Blockchain provides a distributed ledger designed for scenarios needing immutable transaction history and trust across multiple parties, such as supply chain tracking."),

    ("Purpose-Built Databases",
     "Which purpose-built database is most appropriate for a 'fraud detection' use case involving relationships between entities?",
     ["Amazon Neptune",
      "Amazon DocumentDB",
      "Amazon Managed Blockchain",
      "Amazon ElastiCache"],
     0,
     "Fraud detection relies on analyzing relationships and connections between entities, which is exactly what Neptune's graph database model is optimized for."),

    ("Purpose-Built Databases",
     "Which purpose-built database keyword pairing is CORRECT?",
     ["'MongoDB compatibility' maps to Amazon Neptune",
      "'Supply chain ledger' maps to Amazon DocumentDB",
      "'Connected data and relationships' maps to Amazon Neptune",
      "'Graph queries' maps to Amazon Managed Blockchain"],
     2,
     "Neptune is specifically optimized for connected, relationship-heavy data; the other pairings mismatch the service with the wrong data shape."),

    ("Purpose-Built Databases",
     "Why would a company choose a purpose-built database like DocumentDB or Neptune instead of forcing their data into RDS or DynamoDB?",
     ["Because purpose-built databases are always cheaper",
      "Because the data shape (document, graph, ledger) is more efficiently modeled and queried using a database designed specifically for that shape",
      "Because RDS and DynamoDB cannot store any data at all",
      "Because purpose-built databases require no AWS account"],
     1,
     "Forcing document, graph, or ledger data into a relational or key-value model is inefficient and awkward; purpose-built databases are optimized specifically for those data shapes and query patterns."),

    # ============================ AWS Backup ============================
    ("AWS Backup",
     "What is the primary purpose of AWS Backup?",
     ["A centralized backup management service across multiple AWS services",
      "A caching layer for DynamoDB",
      "A tool for migrating databases between regions",
      "A service exclusively for backing up EC2 instances"],
     0,
     "AWS Backup provides one centralized location to define and manage backup policies across many AWS services, rather than requiring separate configuration for each one."),

    ("AWS Backup",
     "[Exam trap] How does AWS Backup differ from RDS's own automated backup feature?",
     ["They are identical with no meaningful difference",
      "AWS Backup is a centralized layer that can manage backup policies across many services, while RDS automated backups are native to RDS alone",
      "AWS Backup only works with Amazon S3",
      "RDS automated backups are more centralized than AWS Backup"],
     1,
     "RDS automated backups are scoped to RDS itself, while AWS Backup sits above multiple services (RDS, DynamoDB, EFS, EC2 volumes, etc.) to apply unified, centralized backup policies."),

    ("AWS Backup",
     "Which business need is best solved by AWS Backup?",
     ["A company wants consistent backup retention and scheduling policies applied across RDS, DynamoDB, and EFS from one place",
      "A company wants to reduce database read latency",
      "A company wants to migrate an on-prem database to AWS",
      "A company wants a graph database for social connections"],
     0,
     "AWS Backup's core value is centralizing and standardizing backup policy management across multiple different AWS services simultaneously."),

    ("AWS Backup",
     "What type of requirement often points to AWS Backup in an exam scenario?",
     ["Compliance requirements needing centralized backup auditing across services",
      "A need for millisecond query latency",
      "A need for graph-based relationship queries",
      "A need for schema-flexible data storage"],
     0,
     "Centralized backup auditing and consistent policy enforcement across multiple AWS services is the classic signal phrase pointing to AWS Backup."),

    # ============ Self-Managed DB on EC2 vs Managed AWS DB Service ============
    ("Self-Managed vs Managed",
     "Which scenario justifies using a self-managed database on EC2 instead of a fully managed AWS database service?",
     ["A developer needs full control over the OS, database installation, and configuration",
      "A developer wants AWS to handle patching and backups automatically",
      "A developer wants to scale without licensing complications",
      "A developer has a small dataset well within RDS's size limits"],
     0,
     "The one legitimate reason to give up a managed service's convenience is needing OS- or engine-level control that managed services intentionally abstract away."),

    ("Self-Managed vs Managed",
     "What is the core trade-off between managed AWS database services and self-managed databases on EC2?",
     ["Managed services trade control for convenience; self-managed trades convenience for control",
      "Managed services are always slower than self-managed ones",
      "Self-managed databases have no operational overhead",
      "There is no meaningful trade-off between the two"],
     0,
     "Choosing a managed service means AWS handles operational tasks but limits configuration control, while self-managing on EC2 restores full control at the cost of taking on all operational responsibility."),

    ("Self-Managed vs Managed",
     "[Exam trap] A company says they want AWS to handle routine maintenance tasks like backups and patching. Does this favor a self-managed database on EC2 or a managed AWS database service?",
     ["Self-managed on EC2",
      "Managed AWS database service (e.g., RDS)",
      "Neither option handles maintenance",
      "Both handle maintenance identically"],
     1,
     "Wanting AWS to handle routine maintenance is a defining benefit of managed services, not a reason to choose self-management — this phrasing is a common exam trap distractor."),

    ("Self-Managed vs Managed",
     "Which of the following is something a self-managed database on EC2 provides that a managed service like RDS does NOT?",
     ["Full root/OS-level access and control over the database engine configuration",
      "Automatic Multi-AZ failover",
      "Automated backups",
      "Managed patching"],
     0,
     "Self-managing on EC2 grants full OS and engine-level access, which managed services intentionally restrict in exchange for handling operational tasks like failover, backups, and patching automatically."),

    ("Self-Managed vs Managed",
     "A team needs a highly specialized, legacy-compatible database configuration that isn't supported by any AWS managed database engine. What should they use?",
     ["A fully managed AWS database service like RDS",
      "A self-managed database installed on an EC2 instance",
      "Amazon DynamoDB",
      "AWS Backup"],
     1,
     "When a required configuration or legacy compatibility need falls outside what managed services support, self-hosting on EC2 is the only way to get that level of customization."),
]


# --------------------------------------------------------------------------
# Core helpers
# --------------------------------------------------------------------------
def _normalize_correct(correct):
    """Return correct answer(s) as a set of 0-based indices."""
    if isinstance(correct, (list, tuple, set)):
        return set(correct)
    return {correct}


def _clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_quiz():
    questions = QUESTIONS.copy()
    random.shuffle(questions)

    total = len(questions)
    score = 0
    topic_stats = defaultdict(lambda: [0, 0])   # topic -> [correct, total]
    missed = []

    print("=" * 70)
    print(f"  AWS CLF-C02 PRACTICE QUIZ — MODULE 7: {MODULE_NAME.upper()}")
    print(f"  Total Questions: {total}")
    print("=" * 70)
    print("For multi-select questions, enter comma-separated letters (e.g., A,C)")
    print("Press Ctrl+C at any time to exit early.\n")

    try:
        for idx, q in enumerate(questions, 1):
            topic, question_text, options, correct, explanation = q
            correct_set = _normalize_correct(correct)

            option_indices = list(range(len(options)))
            random.shuffle(option_indices)
            shuffled_options = [options[i] for i in option_indices]
            new_correct_indices = {option_indices.index(ci) for ci in correct_set}

            is_multi = len(correct_set) > 1

            print(f"\nQ{idx}. [{topic}] {question_text}")
            for i, opt in enumerate(shuffled_options):
                letter = chr(65 + i)
                print(f"  {letter}) {opt}")

            if is_multi:
                n_needed = len(correct_set)
                prompt = f"Select {n_needed} answers (e.g., A,C): "
            else:
                prompt = "Your answer: "

            raw = input(prompt).strip().upper()
            user_letters = [x.strip() for x in raw.replace(" ", "").split(",") if x.strip()]
            user_indices = {ord(l) - 65 for l in user_letters if l.isalpha()}

            topic_stats[topic][1] += 1

            if user_indices == new_correct_indices:
                print("✅ Correct!")
                score += 1
                topic_stats[topic][0] += 1
            else:
                correct_letters = ", ".join(sorted(chr(65 + i) for i in new_correct_indices))
                print(f"❌ Incorrect. Correct answer: {correct_letters}")
                missed.append({
                    "num": idx,
                    "topic": topic,
                    "question": question_text,
                    "options": shuffled_options,
                    "correct_indices": new_correct_indices,
                    "user_indices": user_indices,
                    "explanation": explanation,
                })

            print(f"💡 {explanation}")

    except KeyboardInterrupt:
        print("\n\nQuiz exited early by user.")

    print_results(score, total, topic_stats, missed)


def print_results(score, total, topic_stats, missed):
    attempted = sum(v[1] for v in topic_stats.values())
    pct = (score / attempted * 100) if attempted else 0

    print("\n" + "=" * 70)
    print("  QUIZ RESULTS")
    print("=" * 70)
    print(f"Score: {score}/{attempted} ({pct:.1f}%)")

    if pct >= 90:
        print("Status: 🌟 Excellent! Exam-ready territory.")
    elif pct >= 70:
        print("Status: ✅ Passing range — keep reinforcing weak topics below.")
    else:
        print("Status: ⚠️ Below passing threshold — review flagged topics before the exam.")

    # --- Topic-wise breakdown, weakest first ---
    print("\n" + "-" * 70)
    print("  TOPIC-WISE BREAKDOWN (weakest first)")
    print("-" * 70)

    topic_results = []
    for topic, (c, t) in topic_stats.items():
        p = (c / t * 100) if t else 0
        topic_results.append((topic, c, t, p))
    topic_results.sort(key=lambda x: x[3])

    for topic, c, t, p in topic_results:
        flag = "  ⚠️ BELOW 70%" if p < 70 else ""
        print(f"  {topic:<28} {c}/{t}  ({p:.1f}%){flag}")

    # --- Missed questions review ---
    if missed:
        print("\n" + "-" * 70)
        print("  MISSED QUESTIONS REVIEW")
        print("-" * 70)
        for m in missed:
            print(f"\nQ{m['num']}. [{m['topic']}] {m['question']}")
            for i, opt in enumerate(m["options"]):
                letter = chr(65 + i)
                marker = ""
                if i in m["correct_indices"]:
                    marker = " ✅ (correct)"
                elif i in m["user_indices"]:
                    marker = " ❌ (your answer)"
                print(f"  {letter}) {opt}{marker}")
            print(f"  💡 {m['explanation']}")
    else:
        print("\n🎉 No missed questions — perfect run!")

    # --- Auto-export results to file ---
    filename = f"{MODULE_NAME}-Results.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write(f"AWS CLF-C02 PRACTICE QUIZ RESULTS — MODULE 7: {MODULE_NAME.upper()}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Score: {score}/{attempted} ({pct:.1f}%)\n\n")

            f.write("-" * 70 + "\n")
            f.write("TOPIC-WISE BREAKDOWN (weakest first)\n")
            f.write("-" * 70 + "\n")
            for topic, c, t, p in topic_results:
                flag = "  <-- BELOW 70%" if p < 70 else ""
                f.write(f"{topic:<28} {c}/{t}  ({p:.1f}%){flag}\n")

            if missed:
                f.write("\n" + "-" * 70 + "\n")
                f.write("MISSED QUESTIONS REVIEW\n")
                f.write("-" * 70 + "\n")
                for m in missed:
                    f.write(f"\nQ{m['num']}. [{m['topic']}] {m['question']}\n")
                    for i, opt in enumerate(m["options"]):
                        letter = chr(65 + i)
                        marker = ""
                        if i in m["correct_indices"]:
                            marker = " (correct)"
                        elif i in m["user_indices"]:
                            marker = " (your answer)"
                        f.write(f"  {letter}) {opt}{marker}\n")
                    f.write(f"  Explanation: {m['explanation']}\n")
            else:
                f.write("\nNo missed questions — perfect run!\n")

        print(f"\n📄 Results exported to: {filename}")
    except OSError as e:
        print(f"\n⚠️ Could not export results to file: {e}")


if __name__ == "__main__":
    run_quiz()
