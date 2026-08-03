#!/usr/bin/env python3
"""
================================================================================
 AWS Certified Cloud Practitioner (CLF-C02) — Practice Quiz
 MODULE 6: STORAGE
================================================================================

Covers:
  1. Storage Fundamentals (Block / Object / File)
  2. Amazon EBS (Block Storage) — Instance Store comparison, Snapshots + Lifecycle
  3. Amazon S3 (Object Storage) — Storage Classes, Lifecycle Policies, Security
  4. Amazon EFS (File Storage)
  5. Databases (RDS — brief pointer)
  6. AWS Storage Gateway (Hybrid Storage)
  7. AWS Elastic Disaster Recovery
  8. Master Comparison + Decision Tree
  9. Final Revision Kit (Snowball family, trigger phrases, exam traps)

Run:  python3 Module6-Storage.py
================================================================================
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Module 6: Storage"

# ==============================================================================
# QUESTIONS
# Format: (topic, question_text, [options], correct_answer, explanation)
#   - correct_answer: int (0-based) for single-select
#   - correct_answer: list/tuple of ints (0-based) for multi-select
# ==============================================================================

QUESTIONS = [

    # --------------------------------------------------------------------
    # 1. STORAGE FUNDAMENTALS (Block / Object / File)
    # --------------------------------------------------------------------
    ("Storage Fundamentals",
     "Which storage model breaks data into fixed-size, independently addressable units so that only the changed unit needs to be rewritten on an update?",
     ["Object storage", "Block storage", "File storage", "Archive storage"],
     1,
     "Block storage splits data into fixed-size blocks, so an update only rewrites the affected block instead of the whole file — this is why it's fast for databases and OS volumes."),

    ("Storage Fundamentals",
     "In object storage, what three components make up a single object?",
     ["Blocks, sectors, and a filename", "Data, metadata, and a unique key", "Rows, columns, and an index", "Header, footer, and a checksum"],
     1,
     "An S3 object is a self-contained unit of data + metadata (info about the data) + a unique key used to locate it — there is no partial update, the whole object is replaced on change."),

    ("Storage Fundamentals",
     "Which AWS storage service is built on the file storage model and uses the NFS protocol for shared access?",
     ["Amazon EBS", "Amazon S3", "Amazon EFS", "AWS Snowball"],
     2,
     "File storage organizes data hierarchically and needs a protocol like NFS (Linux) or SMB (Windows) for shared, simultaneous access — that's exactly what EFS provides."),

    ("Storage Fundamentals",
     "A company says '1,000 EC2 instances must read and write the same set of files at the same time.' Which storage model should you map this requirement to?",
     ["Block storage", "Object storage", "File storage", "Instance store"],
     2,
     "Simultaneous shared access to the same files across many instances is the defining trigger phrase for file storage (EFS), not block (single-instance) or object (not a real filesystem)."),

    ("Storage Fundamentals",
     "Which of the following is TRUE about updating data in object storage versus block storage?",
     ["Both rewrite only the changed portion", "Object storage rewrites the entire object; block storage rewrites only the changed block", "Block storage rewrites the entire volume; object storage rewrites only changed bytes", "Neither supports updates"],
     1,
     "This is a core conceptual exam point: object storage has no partial-write capability — any change means the entire object is replaced, while block storage can update just the affected block."),

    # --------------------------------------------------------------------
    # 2. AMAZON EBS (incl. Instance Store, Snapshots + Lifecycle)
    # --------------------------------------------------------------------
    ("EBS",
     "What is the primary purpose of Amazon EBS?",
     ["Globally distributed object storage accessed via HTTP", "Persistent, network-attached block storage for EC2 instances", "A managed NFS file share for multiple instances", "A physical device for offline data transfer"],
     1,
     "EBS provides persistent block-level storage that survives instance stop/terminate, solving the volatility problem of EC2's local instance store."),

    ("EBS",
     "A company lost data every time an on-prem VM crashed because storage was tied to the physical host. Which AWS behavior directly solves this once migrated to EC2 with EBS?",
     ["EBS automatically syncs to S3 every 5 minutes", "EBS volumes have an independent lifecycle and persist even after instance termination", "EBS caches all data in instance memory", "EBS replicates data to instance store automatically"],
     1,
     "EBS volumes exist independently of the EC2 instance and persist after termination (unless 'Delete on Termination' is set) — the auto-sync-to-S3 and memory-caching options are fabricated exam traps."),

    ("EBS",
     "Which statement correctly distinguishes EC2 Instance Store from EBS?",
     ["Instance store is persistent; EBS is volatile", "Instance store is volatile and free; EBS is persistent and costs extra", "Both are volatile and free", "Both are persistent and billed per GB"],
     1,
     "Instance store is physically attached, very low-latency, and included free — but data is lost on stop/terminate, unlike EBS which is durable, network-attached, and billed separately."),

    ("EBS",
     "Which workload is the BEST fit for EC2 Instance Store rather than EBS?",
     ["A production relational database requiring durability", "A boot volume that must survive instance termination", "Temporary cache or buffer data where cost matters more than persistence", "Long-term compliance archival data"],
     2,
     "Instance store is ideal for ultra-low-latency, temporary scratch data (caches, buffers) since it's free but volatile — it should never be used for data that must survive a stop/terminate."),

    ("EBS",
     "An EBS volume can be detached from one EC2 instance and attached to another, but with what key constraint?",
     ["It can be attached to an instance in any Region", "It can only be attached to an instance in the same Availability Zone", "It can only be reattached to the exact same instance", "It must first be converted into an S3 object"],
     1,
     "EBS volumes are AZ-scoped — reattachment across instances is supported, but only within the same Availability Zone; moving across AZs requires a snapshot first."),

    ("EBS",
     "What is an EBS snapshot, and where is it stored behind the scenes?",
     ["A live clone of the volume stored on the same EC2 host", "A point-in-time backup of an EBS volume, stored in Amazon S3", "A memory dump stored in Instance Store", "A configuration file stored in IAM"],
     1,
     "Snapshots are point-in-time backups of EBS volumes and are stored durably in S3 behind the scenes, even though customers interact with them through the EC2/EBS console."),

    ("EBS",
     "EXAM TRAP: After the first snapshot of an EBS volume, how do subsequent snapshots behave?",
     ["Each subsequent snapshot is a full, independent copy of all data", "Each subsequent snapshot is incremental, capturing only changed blocks since the last snapshot", "Subsequent snapshots overwrite the previous snapshot entirely", "Subsequent snapshots are stored only in EBS, never in S3"],
     1,
     "This is one of the most commonly tested EBS traps: only the first snapshot is a full copy; every snapshot after that is incremental, storing just the changed blocks, though each still acts as a full restore point."),

    ("EBS",
     "If you delete an intermediate EBS snapshot in a chain, what happens to the data it references?",
     ["All data in that snapshot is deleted, breaking every later snapshot", "Only data unique to that snapshot is removed; data still referenced by other snapshots is preserved", "The entire volume is deleted", "Nothing happens until the volume itself is deleted"],
     1,
     "AWS manages block references automatically across the snapshot chain, so deleting one snapshot only removes blocks that no other snapshot depends on."),

    ("EBS",
     "Which AWS feature automates the creation, retention, and deletion of EBS snapshots and EBS-backed AMIs on a schedule?",
     ["S3 Lifecycle Policies", "AWS Storage Gateway", "AWS Data Lifecycle Manager (DLM)", "Amazon EFS Lifecycle Management"],
     2,
     "DLM is purpose-built to remove the manual burden of taking and cleaning up EBS snapshots/AMIs across large fleets by applying a policy-based schedule."),

    ("EBS",
     "Are EBS volumes and their snapshots encrypted at rest?",
     ["EBS supports encryption via KMS, and snapshots of encrypted volumes are automatically encrypted", "EBS cannot be encrypted at all", "Only snapshots can be encrypted, never the source volume", "Encryption requires a third-party tool outside AWS"],
     0,
     "EBS integrates natively with AWS KMS for encryption at rest, and any snapshot taken from an encrypted volume automatically inherits that encryption."),

    # --------------------------------------------------------------------
    # 3. AMAZON S3 (Storage Classes, Lifecycle Policies, Security)
    # --------------------------------------------------------------------
    ("S3",
     "What is the maximum size of a single object in Amazon S3?",
     ["1 TB", "5 TB", "500 GB", "There is no maximum object size"],
     1,
     "A single S3 object can be up to 5 TB, but there is no cap on the total size of a bucket — you can store virtually unlimited data overall."),

    ("S3",
     "EXAM TRAP: S3's famous '11 nines' (99.999999999%) figure refers to what?",
     ["Availability (uptime)", "Durability (probability of not losing data)", "Latency guarantee", "Encryption strength"],
     1,
     "11 nines is a durability statistic about data not being lost, not an uptime/availability SLA — availability is a separate, lower figure (e.g., 99.9%), and mixing these up is a classic CCP trap."),

    ("S3",
     "By default, who can access objects in a newly created S3 bucket?",
     ["Anyone on the internet, by default", "Only the bucket owner — S3 buckets are private by default", "Only users in the same VPC", "Only IAM users tagged 'S3Admin'"],
     1,
     "S3 buckets and objects are private by default; public access requires explicit configuration such as a bucket policy, and even then can be blocked by account/bucket settings."),

    ("S3",
     "A bucket policy explicitly grants public read access to objects, but users still get Access Denied when viewing images. What is the MOST LIKELY cause?",
     ["The objects are corrupted", "'Block Public Access' is enabled at the account or bucket level and is overriding the bucket policy", "S3 does not support public access under any configuration", "The images exceed the 5 TB size limit"],
     1,
     "This is one of AWS's favorite trick questions: the account/bucket-level 'Block Public Access' setting overrides bucket policies, so even a permissive policy won't work if this setting is enabled."),

    ("S3",
     "Which S3 feature grants temporary, time-limited access to a specific private object without changing the bucket's overall permissions?",
     ["Bucket Policy", "S3 Access Points", "Presigned URL", "S3 Versioning"],
     2,
     "A presigned URL is generated with an expiration time and grants temporary access to one object, which is ideal for sharing private content briefly without altering bucket-wide permissions."),

    ("S3",
     "Which S3 storage class keeps data with the same millisecond retrieval speed as Standard, but at a lower storage cost, and is best for data accessed less frequently?",
     ["S3 Glacier Flexible Retrieval", "S3 Standard-IA", "S3 Glacier Deep Archive", "S3 One Zone-IA"],
     1,
     "S3 Standard-IA offers the same millisecond retrieval as S3 Standard but at a lower storage price, trading off a per-GB retrieval fee for infrequently accessed data."),

    ("S3",
     "EXAM TRAP: How does S3 One Zone-IA differ from S3 Standard-IA in terms of resilience?",
     ["They have identical resilience; only pricing differs", "One Zone-IA stores data in a single Availability Zone, making it cheaper but less resilient to AZ failure", "One Zone-IA is more resilient because it uses dedicated hardware", "One Zone-IA replicates data globally across Regions"],
     1,
     "One Zone-IA trades resilience for cost by storing data in only one AZ — if that AZ is lost, the data is lost, so it should never be used for critical, irreplaceable data."),

    ("S3",
     "Which S3 storage class is designed for unknown or unpredictable access patterns and automatically moves objects between tiers?",
     ["S3 Standard", "S3 Intelligent-Tiering", "S3 Glacier Instant Retrieval", "S3 One Zone-IA"],
     1,
     "S3 Intelligent-Tiering monitors access patterns and automatically shifts objects between frequent and infrequent tiers for a small monitoring fee, removing the need to guess access patterns upfront."),

    ("S3",
     "A company needs to archive compliance data that is accessed only a few times a year, and cost is the top priority, with retrieval times of hours being acceptable. Which storage class fits best?",
     ["S3 Standard", "S3 Glacier Instant Retrieval", "S3 Glacier Deep Archive", "S3 One Zone-IA"],
     2,
     "S3 Glacier Deep Archive is the cheapest storage tier, designed for long-term archival where retrieval can take up to about 12 hours, matching a cost-first, rarely-accessed use case."),

    ("S3",
     "EXAM TRAP: What is the key difference between S3 Standard-IA and S3 Glacier Flexible Retrieval?",
     ["They are functionally identical", "Standard-IA offers millisecond retrieval, while Glacier Flexible Retrieval takes minutes to hours", "Glacier Flexible Retrieval offers millisecond retrieval, while Standard-IA takes hours", "Only Glacier supports encryption"],
     1,
     "Both are considered 'infrequent access' in spirit, but they differ drastically in retrieval speed — Standard-IA still returns data in milliseconds, while Glacier Flexible Retrieval takes minutes to hours; confusing these is a very common exam trap."),

    ("S3",
     "What do S3 Lifecycle Policy 'transition actions' and 'expiration actions' do, respectively?",
     ["Transition actions delete objects; expiration actions move objects between classes", "Transition actions move objects between storage classes; expiration actions permanently delete objects", "Both only delete objects, at different times", "Both only change object permissions"],
     1,
     "Lifecycle policies automate data management: transition actions define when an object moves to a cheaper storage class, and expiration actions define when it is permanently deleted."),

    ("S3",
     "Which S3 feature analyzes access patterns on a bucket and recommends the best lifecycle policy to apply?",
     ["S3 Storage Class Analysis", "S3 Transfer Acceleration", "S3 Object Lock", "S3 Replication"],
     0,
     "S3 Storage Class Analysis observes how objects are actually accessed over time and provides recommendations for which lifecycle transitions would save the most cost."),

    ("S3",
     "Is Amazon S3 a true hierarchical file system with real folders?",
     ["Yes, S3 buckets contain a real nested folder structure like a file system", "No, S3 has no true folder hierarchy — 'folders' in the console are a UI illusion based on key prefixes", "S3 folders only exist for encrypted buckets", "S3 folders exist only in Intelligent-Tiering"],
     1,
     "This is a conceptual exam trap: S3 is flat object storage where each object has a unique key, and the 'folder' appearance in the console is purely a visual grouping by key prefix, not a real filesystem hierarchy."),

    ("S3",
     "Select TWO features that help control and audit who can access objects in an S3 bucket.",
     ["S3 Storage Class Analysis", "Bucket Policies", "S3 Access Logs", "AWS Data Lifecycle Manager"],
     [1, 2],
     "Bucket Policies define who is allowed to access a bucket/objects, while S3 Access Logs record every request made against the bucket for auditing — Storage Class Analysis and DLM are unrelated to access control."),

    ("S3",
     "What are the two categories of metadata that can be attached to an S3 object?",
     ["Public metadata and private metadata", "System-defined metadata and user-defined metadata", "Static metadata and dynamic metadata", "Primary metadata and secondary metadata"],
     1,
     "System-defined metadata includes things like file name and last-modified date, while user-defined metadata consists of custom key-value tags added by the object owner."),

    # --------------------------------------------------------------------
    # 4. AMAZON EFS
    # --------------------------------------------------------------------
    ("EFS",
     "What core capability does Amazon EFS provide that distinguishes it from EBS?",
     ["Single-instance block-level attachment", "Simultaneous, shared file access for multiple EC2 instances over NFS", "Archival tape emulation for on-prem backup software", "Global HTTP-based object access"],
     1,
     "EFS is a managed file storage service built on NFS, purpose-built for scenarios where many EC2 instances need to read/write the same files at the same time — something EBS mostly cannot do."),

    ("EFS",
     "Is Amazon EFS a Regional or a single-AZ service by default (Standard class)?",
     ["Single-AZ only", "Regional — it automatically replicates data across multiple Availability Zones", "Global across all AWS Regions", "It has no AZ or Region scope at all"],
     1,
     "EFS Standard is a Regional service that replicates data across multiple AZs for high availability, unlike EBS volumes which live in a single AZ."),

    ("EFS",
     "How does EFS handle storage capacity as data is added or removed?",
     ["Customers must manually resize the file system", "It automatically scales storage capacity up and down with no manual provisioning", "Capacity is fixed at creation and cannot change", "Capacity only grows, never shrinks"],
     1,
     "EFS automatically grows and shrinks storage capacity as files are added or deleted, removing the manual resizing burden that exists with EBS volumes."),

    ("EFS",
     "A company runs a content management system where dozens of EC2 instances must all read and write the same set of files concurrently. Which service is the best fit?",
     ["Amazon EBS", "Amazon S3", "Amazon EFS", "AWS Snowball"],
     2,
     "The phrase 'multiple instances need simultaneous shared access to files' is the number one giveaway trigger for EFS in CCP scenario questions."),

    ("EFS",
     "Which AWS service is the better fit than EFS when an on-prem environment is Windows-based and needs native SMB file-share support, or requires Lustre for HPC?",
     ["Amazon FSx", "AWS Storage Gateway", "Amazon S3", "AWS Snowmobile"],
     0,
     "Amazon FSx supports protocols beyond NFS — including SMB (Windows-native) and Lustre (high-performance computing) — making it the better choice for those specific needs versus EFS."),

    # --------------------------------------------------------------------
    # 5. DATABASES (RDS pointer)
    # --------------------------------------------------------------------
    ("Databases (RDS pointer)",
     "A company needs to store structured data that must be frequently queried, joined, and modified. Which type of AWS service should this map to, rather than raw block/object/file storage?",
     ["Amazon S3", "A managed database service such as Amazon RDS", "AWS Storage Gateway", "Amazon EBS Snapshots"],
     1,
     "Structured, queryable, frequently-modified data belongs in a managed database service like RDS rather than being force-fit into S3/EBS/EFS, which are optimized for different access patterns."),

    ("Databases (RDS pointer)",
     "What is Amazon RDS?",
     ["An object storage service for unstructured data", "A managed relational database service supporting engines like MySQL and PostgreSQL", "A hybrid on-prem-to-cloud storage bridge", "A physical appliance for bulk data transfer"],
     1,
     "RDS is AWS's managed relational database service, handling tasks like patching and backups for engines such as MySQL and PostgreSQL — full depth is covered in the dedicated Databases module."),

    # --------------------------------------------------------------------
    # 6. AWS STORAGE GATEWAY
    # --------------------------------------------------------------------
    ("Storage Gateway",
     "What is the core purpose of AWS Storage Gateway?",
     ["To replace all on-prem infrastructure immediately", "To act as a hybrid bridge, letting on-prem applications keep their existing protocol while data syncs to AWS storage in the background", "To provide a physical device for one-time bulk data migration", "To provide GPU compute at the network edge"],
     1,
     "Storage Gateway is ideal when a company doesn't want to change its existing on-prem workflow but still wants AWS storage benefits like scalability and durability — it bridges the old protocol to S3/EBS/Glacier behind the scenes."),

    ("Storage Gateway",
     "Which Storage Gateway type presents on-prem applications with a normal file folder, while storing the data as S3 objects behind the scenes?",
     ["Volume Gateway", "Tape Gateway", "S3 File Gateway", "AWS DataSync"],
     2,
     "S3 File Gateway lets applications keep using standard file shares while AWS transparently stores the data as S3 objects, caching frequently accessed files locally for low latency."),

    ("Storage Gateway",
     "A company's backup software expects a physical tape library, but they want to move that backup workflow to the cloud without replacing the software. Which Storage Gateway type fits?",
     ["S3 File Gateway", "Volume Gateway", "Tape Gateway", "AWS Elastic Disaster Recovery"],
     2,
     "Tape Gateway emulates a physical Virtual Tape Library (VTL) so legacy backup software keeps working unmodified, while data is actually stored in S3 and, for old/rarely accessed tapes, moved to Glacier."),

    ("Storage Gateway",
     "In Volume Gateway's 'Cached Mode,' where does the primary copy of the data live?",
     ["Entirely on-premises, with periodic snapshots sent to AWS", "Entirely in AWS, with only frequently-used data cached locally on-prem", "Split evenly across two on-prem data centers", "Nowhere — cached mode does not store data"],
     1,
     "In Cached Mode, all data lives in AWS and only the frequently accessed subset is cached on-premises for low-latency access, which is the opposite of Stored Mode where all data stays on-prem."),

    ("Storage Gateway",
     "SCENARIO: AnyCompany wants local access to frequently used files, cloud-based cost savings, and minimal disruption to its existing file-sharing workflow. Which is the correct choice, and which are the traps?",
     ["Volume Gateway is correct because it handles files natively", "Tape Gateway is correct because it's the cheapest option", "S3 File Gateway is correct; Volume Gateway (block-based) and Tape Gateway (built for tape backup software) are traps here", "AWS Snowmobile is correct for this use case"],
     2,
     "The requirement describes file-based local caching with cloud backing and no workflow change — the textbook match is S3 File Gateway, while Volume Gateway (iSCSI/block) and Tape Gateway (VTL emulation) solve different underlying protocols."),

    # --------------------------------------------------------------------
    # 7. AWS ELASTIC DISASTER RECOVERY
    # --------------------------------------------------------------------
    ("Elastic Disaster Recovery",
     "What does AWS Elastic Disaster Recovery (DRS) primarily provide?",
     ["Point-in-time backups of a single EBS volume", "Continuous, block-level replication for fast, full-server recovery into AWS", "A physical device for bulk data migration", "Automated S3 lifecycle transitions"],
     1,
     "DRS maintains near real-time replicas of entire physical, virtual, or cloud-based servers, enabling rapid full-server recovery with minimal recovery point objective (RPO) after a disaster."),

    ("Elastic Disaster Recovery",
     "How does AWS Elastic Disaster Recovery differ in scope from a simple EBS snapshot?",
     ["They are functionally identical", "DRS replicates an entire server continuously; an EBS snapshot is a point-in-time backup of a single volume", "EBS snapshots cover entire servers, while DRS only covers one volume", "DRS is slower to recover than restoring from a snapshot"],
     1,
     "DRS operates at the whole-server level with continuous replication for a minimal RPO, whereas an EBS snapshot only captures a single volume at a specific point in time and requires manual restoration steps."),

    # --------------------------------------------------------------------
    # 8. MASTER COMPARISON + DECISION TREE
    # --------------------------------------------------------------------
    ("Master Comparison & Decision Tree",
     "Select THREE AWS storage services and correctly match the general category: which of the following are primarily SINGLE-instance or object-based (not built for simultaneous multi-instance file access)?",
     ["Amazon EBS", "Amazon EFS", "Amazon S3", "AWS Storage Gateway"],
     [0, 2, 3],
     "EBS is (mostly) single-instance block storage, S3 is object storage accessed via HTTP API rather than a shared filesystem, and Storage Gateway bridges to S3/EBS/Glacier — EFS is the outlier purpose-built for simultaneous multi-instance file access."),

    ("Master Comparison & Decision Tree",
     "A question states: 'A database on EC2 needs rapid read-write performance and high IOPS.' Which service should you select?",
     ["Amazon S3", "Amazon EFS", "Amazon EBS (with Provisioned IOPS)", "AWS Storage Gateway"],
     2,
     "High-IOPS, low-latency, single-instance database performance is the textbook trigger for EBS, ideally with Provisioned IOPS volume types for the most demanding workloads."),

    ("Master Comparison & Decision Tree",
     "Which service should be selected when the question emphasizes 'minimize changes to an on-prem workflow while still gaining cloud backup benefits'?",
     ["Amazon EFS", "AWS Storage Gateway", "Amazon S3 Glacier Deep Archive", "AWS Elastic Disaster Recovery"],
     1,
     "Storage Gateway exists specifically to preserve existing on-prem application behavior/protocols while transparently backing data up to AWS, which is exactly this trigger phrase."),

    ("Master Comparison & Decision Tree",
     "In the master decision tree, what is the FIRST question you should ask about a new storage requirement?",
     ["Is the data structured and does it need frequent querying?", "Is the data accessed a few times a year?", "Does it need Multi-AZ replication?", "Is the company using Windows on-prem?"],
     0,
     "The decision tree starts by ruling structured, queryable, frequently-modified data out to a database service (like RDS) before considering block, file, or object storage options."),

    # --------------------------------------------------------------------
    # 9. FINAL REVISION KIT (Snowball family, acronyms, trigger phrases)
    # --------------------------------------------------------------------
    ("Final Revision Kit",
     "A company needs to migrate approximately 60 TB of data to AWS and estimates it would take over a week using their available internet bandwidth. What is the recommended solution?",
     ["AWS DataSync only", "AWS Snowball Edge (Storage Optimized)", "Amazon S3 Transfer Acceleration", "Amazon EFS replication"],
     1,
     "AWS's own guidance is that if network transfer would take more than about a week, a physical device wins — and at ~60 TB, Snowball Edge Storage Optimized (about 80 TB usable) is the right sizing choice over Snowcone or Snowmobile."),

    ("Final Revision Kit",
     "Which Snowball family device is designed for exabyte-scale migrations, physically arriving as a shipping container on a truck?",
     ["Snowcone", "Snowball Edge (Compute Optimized)", "Snowball Edge (Storage Optimized)", "Snowmobile"],
     3,
     "Snowmobile is the extreme end of the Snowball family, capable of transferring up to 100 PB per truck for truly massive, exabyte-scale migrations."),

    ("Final Revision Kit",
     "EXAM TRAP: Which statement about AWS Snowball's typical direction of data movement is most accurate?",
     ["Snowball is exclusively a cloud-to-on-prem export tool", "Snowball is bidirectional, but import (on-prem to AWS Cloud) dominates real-world usage and exam scenarios", "Snowball can only be used for encrypted government data", "Snowball requires a live internet connection at all times"],
     1,
     "Snowball supports both import and export, but the exam and real-world usage skew heavily toward import (on-prem to cloud) scenarios like backups, archives, and database migrations."),

    ("Final Revision Kit",
     "Which AWS service is the 'online' counterpart to Snowball, used for automated large-scale data transfer when decent bandwidth IS available?",
     ["AWS Storage Gateway", "AWS DataSync", "Amazon FSx", "AWS Elastic Disaster Recovery"],
     1,
     "DataSync automates online data transfer at scale, whereas Snowball is the offline/physical option — the exam frequently tests whether you can distinguish the two based on bandwidth availability."),

    ("Final Revision Kit",
     "Select TWO Snowball Edge variants and their defining trait.",
     ["Snowball Edge (Storage Optimized) — maximizes usable storage capacity", "Snowball Edge (Compute Optimized) — includes GPU/compute for edge processing like ML inference", "Snowmobile — mails as a small handheld device", "Snowcone — carries up to 100 PB"],
     [0, 1],
     "Storage Optimized prioritizes raw capacity (~80 TB usable) for bulk migrations, while Compute Optimized adds GPU/EC2/Lambda capability for edge processing such as ML inference or video analysis in disconnected environments."),

    ("Final Revision Kit",
     "What does the acronym 'DLM' stand for in the context of this module?",
     ["Data Loss Management", "Data Lifecycle Manager", "Durable Layer Migration", "Deep Latency Monitor"],
     1,
     "DLM (Data Lifecycle Manager) automates EBS snapshot and AMI creation, retention, and deletion according to a defined policy."),

    ("Final Revision Kit",
     "Which trigger phrase in an exam question most reliably points to Amazon EFS as the answer?",
     ["'archive data accessed a few times a year'", "'multiple users/devices need simultaneous shared access to files'", "'database on EC2, rapid read-write, high IOPS'", "'minimize changes to on-prem workflow'"],
     1,
     "CCP scenario questions repeatedly use 'multiple instances/users need simultaneous shared file access' as the unmistakable trigger phrase for EFS."),

    ("Final Revision Kit",
     "SCENARIO: A finance team needs to recover physical, on-prem servers as quickly as possible after a ransomware event, with minimal data loss. Which service is designed for this?",
     ["AWS Storage Gateway (Tape Gateway)", "AWS Elastic Disaster Recovery", "Amazon S3 Glacier Deep Archive", "AWS Data Lifecycle Manager"],
     1,
     "AWS Elastic Disaster Recovery is purpose-built for fast, full-server recovery through continuous block-level replication, minimizing the recovery point objective (RPO) during events like ransomware attacks."),

    ("Final Revision Kit",
     "Which statement correctly matches an AWS storage service to its underlying protocol?",
     ["EBS uses NFS; EFS uses block-level attachment", "S3 uses a REST/HTTP API; EFS uses NFS; EBS uses block-level device attachment", "S3 uses NFS; EBS uses REST API", "All three services use the same protocol"],
     1,
     "Each service is defined by its access protocol: S3 is accessed via HTTP/REST API, EFS uses the NFS protocol for file sharing, and EBS is attached to an instance as a block device."),

    ("Final Revision Kit",
     "Data on AWS Snowball devices is protected using what security measure by default?",
     ["No encryption; physical custody is the only protection", "256-bit encryption, with a tamper-resistant device", "Encryption only if the customer installs third-party software", "Encryption only for Snowmobile, not Snowcone/Snowball Edge"],
     1,
     "Snowball devices use 256-bit encryption and tamper-resistant hardware by default, which is frequently tested alongside shared responsibility model questions."),

]


# ==============================================================================
# QUIZ ENGINE (unchanged logic — mirrors Module 5 Networking script)
# ==============================================================================

def _normalize_correct(correct_answer):
    """Return correct_answer as a sorted tuple of ints, regardless of input type."""
    if isinstance(correct_answer, (list, tuple, set)):
        return tuple(sorted(correct_answer))
    return (correct_answer,)


def run_quiz():
    questions = QUESTIONS[:]
    random.shuffle(questions)

    score = 0
    total = len(questions)
    topic_stats = defaultdict(lambda: [0, 0])  # topic -> [correct, total]
    missed_questions = []

    print("=" * 80)
    print(f" AWS CCP (CLF-C02) PRACTICE QUIZ — {MODULE_NAME}")
    print("=" * 80)
    print(f"\nTotal Questions: {total}")
    print("Answer using the option number(s). For multi-select questions,")
    print("separate multiple answers with commas (e.g., 1,3)\n")
    input("Press Enter to begin...")

    for i, (topic, question_text, options, correct_answer, explanation) in enumerate(questions, 1):
        correct_set = _normalize_correct(correct_answer)
        is_multi = len(correct_set) > 1

        # Shuffle options while tracking correct positions
        indexed_options = list(enumerate(options))
        random.shuffle(indexed_options)

        # Map old index -> new index
        old_to_new = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(indexed_options)}
        new_correct_set = tuple(sorted(old_to_new[c] for c in correct_set))

        print("\n" + "-" * 80)
        print(f"Q{i}. [{topic}]")
        if is_multi:
            print(f"(Select {len(correct_set)}) {question_text}")
        else:
            print(question_text)
        print()

        for new_idx, (_, opt_text) in enumerate(indexed_options):
            print(f"  {new_idx + 1}. {opt_text}")

        print()
        while True:
            try:
                raw = input("Your answer: ").strip()
                if not raw:
                    print("Please enter an answer.")
                    continue
                chosen = sorted(int(x.strip()) - 1 for x in raw.split(","))
                if any(c < 0 or c >= len(indexed_options) for c in chosen):
                    print(f"Please enter number(s) between 1 and {len(indexed_options)}.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter number(s) separated by commas.")

        chosen_set = tuple(sorted(set(chosen)))
        topic_stats[topic][1] += 1

        if chosen_set == new_correct_set:
            print("\n✅ CORRECT!")
            score += 1
            topic_stats[topic][0] += 1
        else:
            correct_labels = ", ".join(str(c + 1) for c in new_correct_set)
            print(f"\n❌ INCORRECT. Correct answer: {correct_labels}")
            missed_questions.append((topic, question_text, indexed_options, new_correct_set, explanation, chosen_set))

        print(f"\n💡 Explanation: {explanation}")

    print_results(score, total, topic_stats, missed_questions)


def print_results(score, total, topic_stats, missed_questions):
    percentage = (score / total * 100) if total > 0 else 0

    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append(f" QUIZ RESULTS — {MODULE_NAME}")
    output_lines.append("=" * 80)
    output_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"\nFINAL SCORE: {score}/{total} ({percentage:.1f}%)")

    if percentage >= 90:
        verdict = "🏆 Excellent! You're exam-ready on this module."
    elif percentage >= 70:
        verdict = "✅ Good job! Review your weak topics below before the exam."
    else:
        verdict = "⚠️  Needs more review — focus heavily on the flagged topics below."
    output_lines.append(f"\n{verdict}")

    output_lines.append("\n" + "-" * 80)
    output_lines.append(" TOPIC-WISE BREAKDOWN (weakest first)")
    output_lines.append("-" * 80)

    topic_results = []
    for topic, (correct, total_t) in topic_stats.items():
        pct = (correct / total_t * 100) if total_t > 0 else 0
        topic_results.append((topic, correct, total_t, pct))
    topic_results.sort(key=lambda x: x[3])

    for topic, correct, total_t, pct in topic_results:
        flag = "  ⚠️  BELOW 70% — REVIEW THIS TOPIC" if pct < 70 else ""
        output_lines.append(f"  {topic:<35} {correct}/{total_t}  ({pct:.0f}%){flag}")

    if missed_questions:
        output_lines.append("\n" + "-" * 80)
        output_lines.append(" MISSED QUESTIONS — REVIEW")
        output_lines.append("-" * 80)
        for idx, (topic, question_text, indexed_options, correct_set, explanation, chosen_set) in enumerate(missed_questions, 1):
            output_lines.append(f"\n{idx}. [{topic}] {question_text}")
            for new_idx, (_, opt_text) in enumerate(indexed_options):
                marker = ""
                if new_idx in correct_set:
                    marker = " ✅ (correct)"
                elif new_idx in chosen_set:
                    marker = " ❌ (your answer)"
                output_lines.append(f"     {new_idx + 1}. {opt_text}{marker}")
            output_lines.append(f"     💡 {explanation}")
    else:
        output_lines.append("\n🎉 No missed questions — perfect run!")

    output_lines.append("\n" + "=" * 80)

    report = "\n".join(output_lines)
    print("\n\n" + report)

    filename = f"{MODULE_NAME.replace(':', '').replace(' ', '-')}-Results.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📄 Results exported to: {os.path.abspath(filename)}")
    except OSError as e:
        print(f"\n⚠️  Could not export results: {e}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
        sys.exit(0)
