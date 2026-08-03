#!/usr/bin/env python3
"""
AWS Certified Cloud Practitioner (CLF-C02) — Practice Quiz
MODULE 12: Migration to the AWS Cloud

Topics covered:
  1. AWS Cloud Adoption Framework (CAF)
  2. Three Phases of Migration (Assess / Mobilize / Migrate & Modernize)
  3. The Seven Rs of Migration
  4. Application Discovery Service & Migration Hub
  5. Application/Database Migration Services (MGN, DMS, SCT)
  6. Data Transfer — Online & Offline (DataSync, Transfer Family,
     Direct Connect, Snow Family)

EXAM MODE:
  - No immediate correct/incorrect feedback during the quiz.
  - Full score, topic-wise breakdown, and a "Missed Questions Review"
    are only shown after the quiz is submitted.
  - Results are auto-exported to "Migration to AWS Cloud-Results.txt".

Run:
    python3 12.py
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Migration to AWS Cloud"

# ---------------------------------------------------------------------------
# QUESTIONS
# Each tuple: (topic, question_text, [options], correct_answer, explanation)
#   correct_answer -> single 0-based int for single-select
#   correct_answer -> list/tuple of 0-based ints for multi-select
# ---------------------------------------------------------------------------

QUESTIONS = [

    # ============================= 1. AWS CAF =============================
    ("AWS Cloud Adoption Framework (CAF)",
     "What is the primary purpose of the AWS Cloud Adoption Framework (CAF)?",
     ["To automate the actual migration of workloads to AWS",
      "To provide guidance and best practices that help an organization build an effective cloud migration plan",
      "To convert database schemas between different engines",
      "To track migration progress across multiple teams"],
     1,
     "CAF is a guidance framework focused on organizational readiness, not a hands-on migration tool — it helps a company plan, not execute."),

    ("AWS Cloud Adoption Framework (CAF)",
     "Which of the following are the 6 perspectives of AWS CAF? (Select THREE)",
     ["Business", "Compute", "People", "Governance", "Storage", "Networking"],
     [0, 2, 3],
     "The 6 CAF perspectives are Business, People, Governance, Platform, Security, and Operations — Compute, Storage, and Networking are technical domains, not CAF perspectives."),

    ("AWS Cloud Adoption Framework (CAF)",
     "A company's employees are resisting the shift to cloud operations and there is confusion over who owns which responsibilities post-migration. Which CAF perspective addresses this?",
     ["Platform", "Security", "People", "Governance"],
     2,
     "Organizational change management, upskilling, and role/culture shifts fall under the People perspective, not the technical perspectives."),

    ("AWS Cloud Adoption Framework (CAF)",
     "Under AWS CAF, which perspectives are grouped as 'Business Capabilities' (as opposed to Technical Capabilities)?",
     ["Platform, Security, Operations",
      "Business, People, Governance",
      "Business, Platform, Security",
      "People, Operations, Governance"],
     1,
     "AWS groups Business, People, and Governance as business-owned capabilities, while Platform, Security, and Operations are technical-stakeholder-owned."),

    ("AWS Cloud Adoption Framework (CAF)",
     "EXAM TRAP: A student assumes AWS CAF is purely a technical framework used by engineers to design cloud architecture. What is wrong with this assumption?",
     ["CAF is only used after migration is complete",
      "CAF has 6 perspectives split evenly across business and technical stakeholders — it is not purely technical",
      "CAF is a paid AWS service that must be purchased separately",
      "CAF only applies to database migrations"],
     1,
     "This is a classic exam trap: only 3 of the 6 CAF perspectives (Platform, Security, Operations) are technical — the other 3 are business-owned, so CAF is fundamentally organizational, not just technical."),

    ("AWS Cloud Adoption Framework (CAF)",
     "Which CAF perspective ensures an organization meets its objectives for confidentiality, integrity, and availability during cloud adoption?",
     ["Governance", "Security", "Business", "Operations"],
     1,
     "The Security perspective specifically covers risk and compliance objectives such as confidentiality, integrity, and availability."),

    ("AWS Cloud Adoption Framework (CAF)",
     "A company wants to align its IT investments with measurable business outcomes before starting a migration. Which CAF perspective is most relevant?",
     ["Business", "Platform", "Operations", "People"],
     0,
     "Aligning IT investment with business value and ROI is explicitly the focus of the Business perspective in CAF."),

    # ===================== 2. THREE PHASES OF MIGRATION ====================
    ("Three Phases of Migration",
     "What are the three phases of AWS's migration process, in the correct order?",
     ["Mobilize -> Assess -> Migrate & Modernize",
      "Assess -> Mobilize -> Migrate & Modernize",
      "Assess -> Migrate & Modernize -> Mobilize",
      "Discover -> Assess -> Migrate"],
     1,
     "AWS's migration journey always follows Assess (understand current state) -> Mobilize (build the plan) -> Migrate & Modernize (execute)."),

    ("Three Phases of Migration",
     "A company wants a data-driven cost estimate for moving its workloads to AWS in order to secure budget approval. Which service and phase does this belong to?",
     ["AWS Application Discovery Service — Mobilize phase",
      "AWS Migration Hub — Mobilize phase",
      "AWS Migration Evaluator — Assess phase",
      "AWS Application Migration Service — Migrate & Modernize phase"],
     2,
     "Building the business case with cost estimates is exactly what AWS Migration Evaluator does, and it belongs to the Assess phase."),

    ("Three Phases of Migration",
     "Which service provides a single dashboard to track migration progress across an entire organization, spanning discovery, planning, and execution?",
     ["AWS Application Discovery Service", "AWS Migration Hub", "AWS Migration Evaluator", "AWS Application Migration Service (MGN)"],
     1,
     "AWS Migration Hub is the centralized tracking dashboard — it does not perform discovery or migration itself, only visibility across the journey."),

    ("Three Phases of Migration",
     "EXAM TRAP: A question states a company wants to 'discover on-premises servers and understand which applications depend on which servers.' Which service is this, and why might students pick the wrong one?",
     ["AWS Migration Evaluator — students often confuse cost estimation with technical inventory",
      "AWS Application Discovery Service — students often confuse it with Migration Evaluator because both sound like 'figuring out what we have'",
      "AWS Migration Hub — students often think Migration Hub performs discovery itself",
      "AWS Database Migration Service — students confuse database migration with server discovery"],
     1,
     "Migration Evaluator solves for cost/business case while Application Discovery Service solves for technical inventory and dependency mapping — the exam frequently swaps these two."),

    ("Three Phases of Migration",
     "During which phase would an organization close identified readiness gaps and build a detailed migration plan?",
     ["Assess", "Mobilize", "Migrate & Modernize", "Optimize"],
     1,
     "Mobilize is specifically about building the detailed plan and closing the gaps that were identified during Assess."),

    ("Three Phases of Migration",
     "True or False: AWS Migration Hub actually performs the technical work of migrating servers and databases to AWS.",
     ["True — Migration Hub executes migrations directly",
      "False — Migration Hub only tracks progress; it does not migrate workloads itself",
      "True, but only for database workloads",
      "False — Migration Hub is only used in the Assess phase"],
     1,
     "Migration Hub is purely a tracking/visibility tool; the actual migration work is done by tools like MGN, DMS, and SCT."),

    ("Three Phases of Migration",
     "Which of the following correctly matches phase to primary tool(s)? (Select TWO)",
     ["Assess -> AWS Migration Evaluator",
      "Mobilize -> AWS Application Migration Service (MGN)",
      "Mobilize -> AWS Application Discovery Service",
      "Migrate & Modernize -> AWS Migration Evaluator"],
     [0, 2],
     "Migration Evaluator belongs to Assess, and Application Discovery Service belongs to Mobilize; MGN belongs to Migrate & Modernize, not Mobilize."),

    ("Three Phases of Migration",
     "A company has already assessed cost and built its migration plan, and now needs to move its Oracle database to Aurora with minimal downtime. Which phase are they in?",
     ["Assess", "Mobilize", "Migrate & Modernize", "Optimize"],
     2,
     "Actually executing a database move with tools like DMS/SCT is part of the Migrate & Modernize phase, the final step of the migration journey."),

    # ========================== 3. SEVEN Rs =================================
    ("Seven Rs of Migration",
     "Which migration strategy involves moving an application to AWS with absolutely no code or configuration changes, typically onto EC2?",
     ["Replatform", "Refactor", "Rehost", "Relocate"],
     2,
     "Rehost, or 'lift-and-shift,' means moving the app as-is with zero changes — the fastest, lowest-effort of the 7 Rs that move you to the cloud."),

    ("Seven Rs of Migration",
     "A company migrates its self-managed on-prem database to Amazon RDS as part of moving to AWS, making minor optimizations without a full re-architecture. Which R is this?",
     ["Rehost", "Replatform", "Refactor", "Repurchase"],
     1,
     "Replatform ('lift-tinker-and-shift') involves small optimizations like swapping a self-managed DB for a managed service such as RDS, without rewriting the application."),

    ("Seven Rs of Migration",
     "EXAM TRAP: What is the key distinguishing factor between Rehost and Replatform, which the exam frequently tests?",
     ["Rehost is for databases only, Replatform is for applications only",
      "Rehost = literally zero changes; Replatform = some optimization but not full re-architecture",
      "Rehost is always more expensive than Replatform",
      "Rehost only applies to Windows workloads"],
     1,
     "This is the single most commonly confused pair on the CCP exam: Rehost makes no changes at all, while Replatform makes minor tweaks (like using a managed service) without a major redesign."),

    ("Seven Rs of Migration",
     "A company completely re-architects a monolithic application into microservices and serverless functions to take full advantage of cloud-native features. Which R is this?",
     ["Replatform", "Refactor / Re-architect", "Relocate", "Repurchase"],
     1,
     "Refactor (Re-architect) is the highest-effort strategy, involving a full redesign to use cloud-native features like serverless and microservices."),

    ("Seven Rs of Migration",
     "A company drops its licensed on-premises CRM software and instead subscribes to Salesforce, a SaaS product. Which R does this represent?",
     ["Retain", "Repurchase", "Retire", "Relocate"],
     1,
     "Repurchase means moving to a different product entirely, usually replacing licensed software with a SaaS offering — the CRM-to-Salesforce scenario is a classic exam example."),

    ("Seven Rs of Migration",
     "Which R involves moving infrastructure to the cloud at the hypervisor level without changing anything at the OS or application level, typically via VMware Cloud on AWS?",
     ["Rehost", "Relocate", "Replatform", "Refactor"],
     1,
     "Relocate is specifically an infrastructure/hypervisor-level move — the entire VM environment shifts as-is, distinct from Rehost which moves individual apps/servers into native EC2."),

    ("Seven Rs of Migration",
     "Which two of the 7 Rs strategies do NOT result in a workload moving to the cloud? (Select TWO)",
     ["Refactor", "Retain", "Repurchase", "Retire"],
     [1, 3],
     "Retain (keep it on-prem for now) and Retire (decommission it) are the only two of the 7 Rs where the workload does not end up in the cloud."),

    ("Seven Rs of Migration",
     "EXAM TRAP: A company decides not to migrate a particular application yet due to compliance restrictions, planning to revisit the decision later. Is this a failure to migrate, or a valid strategy?",
     ["It is a failure and should not appear on the exam as a valid choice",
      "It is the valid strategy called Retain — a deliberate business decision, not a failure",
      "It is automatically classified as Retire",
      "It means the company must use Rehost instead"],
     1,
     "The exam sometimes frames Retain as if it were a shortcoming, but it is a legitimate, deliberate migration strategy driven by real business or compliance constraints."),

    ("Seven Rs of Migration",
     "A legacy internal tool is no longer used by anyone in the company. As part of migration planning, the company decides to shut it down instead of migrating it. Which R is this?",
     ["Retain", "Retire", "Refactor", "Rehost"],
     1,
     "Retire means decommissioning an application that is no longer needed — it simply gets turned off rather than migrated."),

    ("Seven Rs of Migration",
     "Which of the following correctly ranks these strategies from LOWEST to HIGHEST typical migration effort?",
     ["Refactor -> Replatform -> Rehost", "Rehost -> Replatform -> Refactor", "Replatform -> Rehost -> Refactor", "Refactor -> Rehost -> Replatform"],
     1,
     "Effort increases from Rehost (no changes) to Replatform (minor optimization) to Refactor (full re-architecture), representing increasing levels of cloud-native redesign."),

    ("Seven Rs of Migration",
     "A company wants to migrate an application to AWS with the fastest possible timeline and zero risk of breaking existing functionality due to code changes. Which strategy best fits?",
     ["Refactor", "Repurchase", "Rehost", "Retain"],
     2,
     "Rehost is the fastest, lowest-risk option because it moves the application as-is with no code changes, minimizing the chance of breaking functionality."),

    ("Seven Rs of Migration",
     "The 7 Rs strategy is applied at which level of granularity within an organization's migration?",
     ["Company-wide — one R applies to the entire migration",
      "Per individual application or workload — different apps can use different Rs",
      "Per AWS Region only",
      "Per employee department"],
     1,
     "Each application in a company's portfolio can use a different R depending on its specific business and technical needs — it is not a single company-wide decision."),

    # ============ 4. APPLICATION DISCOVERY SERVICE & MIGRATION HUB ==========
    ("Application Discovery Service & Migration Hub",
     "A company has no clear documentation of what on-premises servers exist or which applications depend on which servers. Which service should they use?",
     ["AWS Migration Hub", "AWS Application Discovery Service", "AWS Migration Evaluator", "AWS Schema Conversion Tool"],
     1,
     "Application Discovery Service is purpose-built to inventory on-prem servers, configurations, performance data, and dependencies before a migration."),

    ("Application Discovery Service & Migration Hub",
     "Which migration phase does AWS Application Discovery Service primarily belong to?",
     ["Assess", "Mobilize", "Migrate & Modernize", "Optimize"],
     1,
     "Application Discovery Service supports the Mobilize phase by providing the detailed technical inventory needed to build the migration plan."),

    ("Application Discovery Service & Migration Hub",
     "A company has multiple teams migrating different applications simultaneously and leadership wants a single view of overall progress. Which service addresses this?",
     ["AWS Application Discovery Service", "AWS Migration Hub", "AWS DataSync", "AWS Direct Connect"],
     1,
     "Migration Hub is the centralized dashboard designed specifically to give visibility into progress across multiple teams and applications."),

    ("Application Discovery Service & Migration Hub",
     "Which best practice is recommended when running AWS Application Discovery Service?",
     ["Run it for only a few minutes to save cost",
      "Run it for several weeks to capture accurate usage patterns",
      "Only run it after the migration is already complete",
      "Only use it for database workloads"],
     1,
     "Running discovery for an extended period (typically weeks) captures realistic usage patterns rather than a single unrepresentative snapshot."),

    ("Application Discovery Service & Migration Hub",
     "EXAM TRAP: True or False — AWS Migration Hub can migrate workloads on its own once discovery data is imported.",
     ["True — it automatically initiates migrations",
      "False — Migration Hub only tracks progress; the actual migration is performed by tools like MGN, DMS, or SCT",
      "True, but only for EC2 instances",
      "False — Migration Hub cannot be used with Discovery Service data"],
     1,
     "Migration Hub is explicitly a tracking dashboard; it never performs the actual migration work itself, regardless of what data it has imported."),

    ("Application Discovery Service & Migration Hub",
     "Which service would you use BEFORE Migration Hub to actually gather the technical inventory data that Migration Hub can then help track?",
     ["AWS Migration Evaluator", "AWS Application Discovery Service", "AWS Database Migration Service", "AWS Direct Connect"],
     1,
     "Application Discovery Service gathers the raw technical inventory and dependency data, which can then feed into Migration Hub for centralized tracking."),

    # ===== 5. APPLICATION / DATABASE MIGRATION SERVICES (MGN/DMS/SCT) =====
    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "Which AWS service provides automated lift-and-shift migration of servers to AWS with minimal downtime?",
     ["AWS Database Migration Service (DMS)", "AWS Application Migration Service (MGN)", "AWS Schema Conversion Tool (SCT)", "AWS Migration Hub"],
     1,
     "AWS Application Migration Service (MGN) is specifically the automated Rehost tool for migrating servers/applications with minimal downtime."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "EXAM TRAP: Despite being part of the 'Migrate and Modernize' phase name, what is MGN actually best suited for?",
     ["Refactoring applications into microservices",
      "Rehost — lift-and-shift migration, not modernization/refactoring",
      "Converting database schemas between engines",
      "Tracking migration progress across teams"],
     1,
     "Even though the phase is called 'Migrate and Modernize,' MGN itself is a Rehost automation tool, not a refactoring or modernization tool — a common exam trap."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "A company needs to migrate its production database to AWS while keeping the source database operational and up to date throughout the migration. Which service enables this?",
     ["AWS Schema Conversion Tool (SCT)", "AWS Database Migration Service (DMS)", "AWS Application Migration Service (MGN)", "AWS Migration Hub"],
     1,
     "DMS supports continuous replication, keeping the source database live and operational while data is migrated with minimal downtime."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "A company is migrating from an on-premises Oracle database to Amazon Aurora PostgreSQL, a different database engine. What must they use in addition to DMS?",
     ["AWS Migration Hub", "AWS Schema Conversion Tool (SCT)", "AWS Application Migration Service (MGN)", "AWS Direct Connect"],
     1,
     "SCT converts schema and code objects (stored procedures, views, functions) for heterogeneous migrations between different database engines, and works alongside DMS which moves the actual data."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "EXAM TRAP: A student assumes DMS alone can handle a migration from Oracle to Aurora. What is the flaw in this assumption?",
     ["DMS cannot migrate any databases at all",
      "DMS moves data but cannot convert schema/code across different engines — SCT is needed first for heterogeneous migrations",
      "DMS only works with Amazon RDS as a source",
      "DMS requires Direct Connect to function"],
     1,
     "DMS handles data movement, but converting the schema and code objects between different engine types requires SCT — DMS alone cannot perform heterogeneous schema conversion."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "Which of the following correctly describes AWS DMS's support for migration types? (Select TWO)",
     ["Supports homogeneous migrations (e.g., MySQL to MySQL)",
      "Supports heterogeneous migrations (e.g., Oracle to Aurora)",
      "Only supports migrations within the same AWS Region",
      "Requires the source database to be shut down during migration"],
     [0, 1],
     "DMS supports both homogeneous migrations (same engine) and heterogeneous migrations (different engines, typically paired with SCT), and the source database stays operational throughout."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "What does AWS Schema Conversion Tool (SCT) specifically convert?",
     ["Raw data rows from source to target database",
      "Database schema and code objects such as stored procedures, views, and functions",
      "EC2 AMIs from on-prem hypervisors",
      "File-level data to S3"],
     1,
     "SCT converts schema and code objects like stored procedures, views, and functions — it does not move the actual data rows, which is DMS's job."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "A company needs to migrate hundreds of physical and virtual servers to EC2 quickly, without rewriting any application code. Which service is the best fit?",
     ["AWS DMS", "AWS SCT", "AWS Application Migration Service (MGN)", "AWS Transfer Family"],
     2,
     "MGN is purpose-built for automating the Rehost strategy at scale, moving many servers to AWS quickly with minimal downtime and no code changes."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "Which pairing of tools is correct for a heterogeneous database migration?",
     ["DMS converts schema, SCT migrates data",
      "SCT converts schema, DMS migrates data",
      "MGN converts schema, DMS migrates data",
      "SCT migrates data, Migration Hub converts schema"],
     1,
     "The correct division of labor is: SCT converts the schema/code objects first, and then DMS handles the actual data migration."),

    ("Application/Database Migration Services (MGN, DMS, SCT)",
     "Which service would be least relevant if a company is only migrating stateless application servers with no associated database?",
     ["AWS Application Migration Service (MGN)", "AWS Database Migration Service (DMS)", "Amazon EC2", "AWS Application Discovery Service"],
     1,
     "DMS is specifically for database migration; if there's no database involved, DMS has no role in the migration."),

    # ===================== 6. DATA TRANSFER (ONLINE + OFFLINE) =============
    ("Data Transfer (Online + Offline)",
     "A company needs to move large volumes of file data to Amazon S3 on an ongoing, automated, scheduled basis with bandwidth throttling. Which service fits best?",
     ["AWS Transfer Family", "AWS DataSync", "AWS Direct Connect", "AWS Snowball Edge"],
     1,
     "AWS DataSync is designed for automated, scheduled, bandwidth-throttled bulk online transfer to services like S3, EFS, and FSx."),

    ("Data Transfer (Online + Offline)",
     "A company's external partners can only send files using SFTP due to legacy system constraints. Which AWS service supports this directly into S3 or EFS?",
     ["AWS DataSync", "AWS Transfer Family", "AWS Direct Connect", "AWS Snow Family"],
     1,
     "AWS Transfer Family provides fully managed support for SFTP, FTPS, and FTP transfers directly into S3 or EFS, ideal for partner/legacy protocol requirements."),

    ("Data Transfer (Online + Offline)",
     "A logistics company at a remote site has 5 petabytes of data and only a slow, unreliable internet connection. What is the best solution to migrate this data to AWS?",
     ["AWS DataSync", "AWS Transfer Family", "AWS Direct Connect", "AWS Snow Family (Snowball Edge)"],
     3,
     "Petabyte-scale data combined with no/poor internet connectivity is the classic signal for offline transfer via Snowball Edge, not any of the online-transfer services."),

    ("Data Transfer (Online + Offline)",
     "EXAM TRAP: A student sees 'automated' in a scenario describing a petabyte-scale, no-internet remote site and picks AWS DataSync. Why is this wrong?",
     ["DataSync is more expensive than Snowball in all cases",
      "DataSync requires network connectivity to function, which the scenario explicitly rules out",
      "DataSync cannot handle more than 1TB of data",
      "DataSync only works with databases, not files"],
     1,
     "DataSync sounds automated and modern, but it fundamentally requires network connectivity — with no/poor internet at petabyte scale, Snowball Edge is the only workable answer."),

    ("Data Transfer (Online + Offline)",
     "A company needs a persistent, private, high-bandwidth, low-latency connection between its data center and AWS for ongoing hybrid workloads, not just a one-time migration.",
     ["AWS DataSync", "AWS Transfer Family", "AWS Direct Connect", "AWS Snowball Edge"],
     2,
     "Direct Connect establishes a private dedicated network link bypassing the public internet, ideal for ongoing, consistent, low-latency hybrid connectivity."),

    ("Data Transfer (Online + Offline)",
     "EXAM TRAP: Is AWS Direct Connect primarily classified as a migration tool?",
     ["Yes, its core purpose is one-time data migration",
      "No — its core purpose is persistent hybrid connectivity; it can support migration but that is not its primary role",
      "Yes, but only for database migrations",
      "No, it cannot be used during a migration at all"],
     1,
     "Direct Connect's core purpose is an ongoing private network link for hybrid architectures — it can assist with migration, but it is not fundamentally a migration-specific tool."),

    ("Data Transfer (Online + Offline)",
     "Which of the following are considered ONLINE data transfer options? (Select THREE)",
     ["AWS DataSync", "AWS Snowball Edge", "AWS Transfer Family", "AWS Direct Connect"],
     [0, 2, 3],
     "DataSync, Transfer Family, and Direct Connect all require network connectivity and are online options; Snowball Edge is the offline, physical-device option."),

    ("Data Transfer (Online + Offline)",
     "What is a key security feature of AWS Snow Family devices?",
     ["Data is never encrypted to maximize transfer speed",
      "Data is encrypted at rest and in transit, and devices are tamper-resistant",
      "Devices require a permanent internet connection for encryption to apply",
      "Only in-transit encryption is supported, not at-rest"],
     1,
     "Snow Family devices encrypt data both at rest and in transit and use tamper-resistant enclosures, which is important for physically shipped hardware."),

    ("Data Transfer (Online + Offline)",
     "A company wants to sync millions of files from an on-premises NAS to Amazon EFS on a recurring nightly schedule with monitoring and reporting. Which service is the best fit?",
     ["AWS Transfer Family", "AWS DataSync", "AWS Direct Connect", "AWS Snowball Edge"],
     1,
     "DataSync is purpose-built for recurring, monitored, automated bulk file transfers into services like EFS, with scheduling and reporting built in."),

    ("Data Transfer (Online + Offline)",
     "Besides offline data migration, what is another common use case for AWS Snowball Edge devices?",
     ["Running edge computing workloads in remote or rugged environments",
      "Hosting a company's primary production database permanently",
      "Acting as a permanent replacement for Direct Connect",
      "Converting database schemas during migration"],
     0,
     "Snowball Edge devices are also used for edge computing in disconnected, remote, or rugged environments, not just one-time bulk offline transfer."),

    ("Data Transfer (Online + Offline)",
     "EXAM TRAP: A company needs to transfer files to S3 using only the FTP protocol because of a legacy partner system. A student picks AWS DataSync. Why is this incorrect?",
     ["DataSync cannot write to S3 at all",
      "DataSync is a bulk automated sync tool and does not provide FTP/SFTP/FTPS protocol support — that is Transfer Family's role",
      "DataSync only works with on-premises databases",
      "DataSync requires Snowball hardware to function"],
     1,
     "DataSync handles bulk automated file sync, not legacy file-transfer protocols; when the scenario explicitly mentions FTP/SFTP/FTPS, Transfer Family is the correct choice."),

    ("Data Transfer (Online + Offline)",
     "Which decision factor most directly determines whether a company should use an online transfer method versus AWS Snow Family?",
     ["The AWS Region the company operates in",
      "Whether sufficient internet bandwidth/connectivity is available for the data volume involved",
      "Whether the company uses Windows or Linux servers",
      "Whether the company has an AWS support plan"],
     1,
     "The core decision tree factor is bandwidth/connectivity availability relative to data volume — sufficient connectivity favors online tools, insufficient connectivity favors Snow Family."),
]


# ---------------------------------------------------------------------------
# QUIZ ENGINE (reusable as-is across modules)
# ---------------------------------------------------------------------------

def _normalize_correct(correct_answer):
    """Return correct_answer as a sorted tuple of ints, regardless of
    whether it was passed as a single int or a list/tuple of ints."""
    if isinstance(correct_answer, (list, tuple, set)):
        return tuple(sorted(correct_answer))
    return (correct_answer,)


def _shuffle_question(question_tuple):
    """Shuffle the options of a single question, remapping the correct
    answer index(es) accordingly. Returns a new tuple in the same shape."""
    topic, question_text, options, correct_answer, explanation = question_tuple

    correct_indices = _normalize_correct(correct_answer)
    indexed_options = list(enumerate(options))
    random.shuffle(indexed_options)

    new_options = [opt for _, opt in indexed_options]
    old_to_new = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(indexed_options)}
    new_correct_indices = tuple(sorted(old_to_new[i] for i in correct_indices))

    if len(new_correct_indices) == 1:
        new_correct = new_correct_indices[0]
    else:
        new_correct = list(new_correct_indices)

    return (topic, question_text, new_options, new_correct, explanation)


def _format_options(options):
    letters = "ABCDEFGH"
    return "\n".join(f"   {letters[i]}. {opt}" for i, opt in enumerate(options))


def _parse_user_input(raw, num_options, is_multi):
    """Parse raw user input into a sorted tuple of 0-based indices.
    Returns None if input could not be parsed."""
    letters = "ABCDEFGH"
    raw = raw.strip().upper().replace(" ", "")
    if not raw:
        return None

    parts = [p for p in raw.replace(",", "") if p]
    if is_multi:
        # allow forms like "A,C" or "AC"
        parts = list(raw.replace(",", ""))

    try:
        indices = set()
        tokens = raw.split(",") if "," in raw else list(raw)
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            if tok in letters[:num_options]:
                indices.add(letters.index(tok))
            elif tok.isdigit() and 1 <= int(tok) <= num_options:
                indices.add(int(tok) - 1)
            else:
                return None
        if not indices:
            return None
        return tuple(sorted(indices))
    except Exception:
        return None


def run_quiz():
    print("=" * 70)
    print(f"  AWS CCP (CLF-C02) PRACTICE QUIZ — MODULE 12: {MODULE_NAME}")
    print("=" * 70)
    print(f"\nTotal Questions: {len(QUESTIONS)}")
    print("EXAM MODE: Answers are recorded silently. No feedback is shown")
    print("until you finish the full quiz — just like the real exam.\n")
    input("Press Enter to begin...")

    shuffled_questions = [_shuffle_question(q) for q in QUESTIONS]
    random.shuffle(shuffled_questions)

    results = []  # each: dict(topic, question_text, options, selected, correct, explanation, is_correct)

    letters = "ABCDEFGH"

    for i, (topic, question_text, options, correct_answer, explanation) in enumerate(shuffled_questions, 1):
        correct_indices = _normalize_correct(correct_answer)
        is_multi = len(correct_indices) > 1

        print("\n" + "-" * 70)
        print(f"Q{i}. {question_text}")
        if is_multi:
            print(f"   (Select {len(correct_indices)} — e.g. A,C)")
        print(_format_options(options))

        while True:
            prompt = "\nYour answer: "
            raw = input(prompt)
            parsed = _parse_user_input(raw, len(options), is_multi)
            if parsed is None:
                print("   Invalid input — please enter option letter(s), e.g. A or A,C.")
                continue
            if is_multi and len(parsed) != len(correct_indices):
                print(f"   Please select exactly {len(correct_indices)} options.")
                continue
            break

        is_correct = tuple(sorted(parsed)) == tuple(sorted(correct_indices))

        selected_text = ", ".join(f"{letters[idx]}. {options[idx]}" for idx in parsed)
        correct_text = ", ".join(f"{letters[idx]}. {options[idx]}" for idx in correct_indices)

        results.append({
            "topic": topic,
            "question_text": question_text,
            "selected_text": selected_text,
            "correct_text": correct_text,
            "explanation": explanation,
            "is_correct": is_correct,
        })

        print("Answer recorded.")

    print_results(results)


def print_results(results):
    total = len(results)
    correct_count = sum(1 for r in results if r["is_correct"])
    percentage = (correct_count / total * 100) if total else 0

    # Topic-wise breakdown
    topic_totals = defaultdict(int)
    topic_correct = defaultdict(int)
    for r in results:
        topic_totals[r["topic"]] += 1
        if r["is_correct"]:
            topic_correct[r["topic"]] += 1

    topic_breakdown = []
    for topic in topic_totals:
        t_total = topic_totals[topic]
        t_correct = topic_correct[topic]
        t_pct = (t_correct / t_total * 100) if t_total else 0
        topic_breakdown.append((topic, t_correct, t_total, t_pct))

    # weakest-first
    topic_breakdown.sort(key=lambda x: x[3])

    weak_topics = [tb for tb in topic_breakdown if tb[3] < 70]
    missed = [r for r in results if not r["is_correct"]]

    lines = []
    lines.append("=" * 70)
    lines.append(f"  RESULTS — MODULE 12: {MODULE_NAME}")
    lines.append("=" * 70)
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"\nOVERALL SCORE: {correct_count}/{total}  ({percentage:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("TOPIC-WISE BREAKDOWN (weakest first)")
    lines.append("-" * 70)
    for topic, t_correct, t_total, t_pct in topic_breakdown:
        lines.append(f"  {topic:<55} {t_correct}/{t_total}  ({t_pct:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("WEAK TOPICS (< 70% correct)")
    lines.append("-" * 70)
    if weak_topics:
        for topic, t_correct, t_total, t_pct in weak_topics:
            lines.append(f"  ⚠ {topic}: {t_correct}/{t_total} ({t_pct:.1f}%)")
    else:
        lines.append("  None — great job! All topics scored 70% or above.")

    lines.append("\n" + "-" * 70)
    lines.append("MISSED QUESTIONS REVIEW")
    lines.append("-" * 70)
    if missed:
        for idx, r in enumerate(missed, 1):
            lines.append(f"\n{idx}. {r['question_text']}")
            lines.append(f"   Your answer:    {r['selected_text']}")
            lines.append(f"   Correct answer: {r['correct_text']}")
            lines.append(f"   Explanation:    {r['explanation']}")
    else:
        lines.append("  None — you got every question correct!")

    lines.append("\n" + "=" * 70)

    report = "\n".join(lines)
    print("\n" + report)

    # Auto-export
    filename = f"{MODULE_NAME}-Results.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nResults exported to: {filename}")
    except Exception as e:
        print(f"\n[!] Could not export results file: {e}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Exiting without results.")
        sys.exit(0)
