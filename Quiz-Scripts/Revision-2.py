#!/usr/bin/env python3
"""
AWS Certified Cloud Practitioner (CLF-C02) - MEGA REVISION QUIZ
Covers all 4 exam domains: Cloud Concepts, Security & Compliance,
Cloud Technology & Services, Billing/Pricing/Support.

Exam-mode: no feedback shown until the full quiz is submitted.
At the end, generates a topic-wise weak-area report and auto-exports
a results file. Paste that exported report back to Claude for analysis.
"""

import random
import json
from datetime import datetime

# ---------------------------------------------------------------------------
# QUESTION BANK
# Each question: id, domain, topic, question, options(A-D), answer, explanation
# ---------------------------------------------------------------------------

QUESTIONS = [
    # ---------------- DOMAIN 1: CLOUD CONCEPTS ----------------
    {"id": 1, "domain": "Cloud Concepts", "topic": "Well-Architected Framework",
     "q": "Which Well-Architected Framework pillar focuses on running workloads effectively while minimizing environmental impact?",
     "options": {"A": "Operational Excellence", "B": "Sustainability", "C": "Performance Efficiency", "D": "Cost Optimization"},
     "answer": "B",
     "explanation": "Sustainability is the 6th pillar, added later, focused on minimizing environmental impacts of running cloud workloads."},

    {"id": 2, "domain": "Cloud Concepts", "topic": "Cloud Economics",
     "q": "A company wants to shift from a CapEx to an OpEx spending model. Which cloud benefit does this describe?",
     "options": {"A": "Economies of scale", "B": "Trade fixed expense for variable expense", "C": "Increase speed and agility", "D": "Go global in minutes"},
     "answer": "B",
     "explanation": "Paying only for what you use (variable expense) instead of large upfront infrastructure investment (fixed CapEx) is the classic OpEx benefit."},

    {"id": 3, "domain": "Cloud Concepts", "topic": "Scalability",
     "q": "What is the key difference between vertical scaling and horizontal scaling?",
     "options": {"A": "Vertical adds more instances; horizontal increases instance size", "B": "Vertical increases instance size; horizontal adds more instances", "C": "They are the same thing", "D": "Vertical only applies to storage"},
     "answer": "B",
     "explanation": "Vertical scaling = bigger instance (more CPU/RAM). Horizontal scaling = more instances added, which is generally preferred in cloud for elasticity/fault tolerance."},

    {"id": 4, "domain": "Cloud Concepts", "topic": "Migration Strategies",
     "q": "Which of the 6 R's migration strategy involves moving an application to the cloud with NO changes to the code?",
     "options": {"A": "Refactor", "B": "Replatform", "C": "Rehost (lift-and-shift)", "D": "Repurchase"},
     "answer": "C",
     "explanation": "Rehost / lift-and-shift = moving the app as-is with no code changes, fastest migration method."},

    {"id": 5, "domain": "Cloud Concepts", "topic": "AWS Global Infrastructure",
     "q": "What is a Region composed of?",
     "options": {"A": "A single data center", "B": "Multiple isolated Availability Zones", "C": "A single Availability Zone", "D": "Edge locations only"},
     "answer": "B",
     "explanation": "A Region is a physical location containing multiple isolated Availability Zones (AZs), each with one or more discrete data centers."},

    {"id": 6, "domain": "Cloud Concepts", "topic": "AWS Global Infrastructure",
     "q": "What is the minimum number of Availability Zones an AWS Region typically has?",
     "options": {"A": "1", "B": "2", "C": "3", "D": "5"},
     "answer": "B",
     "explanation": "AWS Regions have a minimum of 2 (most have 3+) isolated AZs to enable high availability and fault tolerance."},

    {"id": 7, "domain": "Cloud Concepts", "topic": "Cloud Deployment Models",
     "q": "Running some IT resources on-premises and some in the AWS Cloud describes which deployment model?",
     "options": {"A": "All-in cloud", "B": "Hybrid", "C": "On-premises", "D": "Private cloud"},
     "answer": "B",
     "explanation": "Hybrid deployment connects existing on-premises infrastructure with cloud resources."},

    # ---------------- DOMAIN 2: SECURITY & COMPLIANCE ----------------
    {"id": 8, "domain": "Security", "topic": "Shared Responsibility Model",
     "q": "In the AWS Shared Responsibility Model, who is responsible for patching the guest operating system on an EC2 instance?",
     "options": {"A": "AWS", "B": "The customer", "C": "Both equally", "D": "AWS Support"},
     "answer": "B",
     "explanation": "For EC2 (IaaS), customer is responsible for guest OS patching, software, and data. AWS handles 'security OF the cloud' (physical infra, hypervisor)."},

    {"id": 9, "domain": "Security", "topic": "Shared Responsibility Model",
     "q": "For a managed service like Amazon RDS, who patches the underlying database engine software?",
     "options": {"A": "The customer", "B": "AWS", "C": "A third party", "D": "Nobody, it's not needed"},
     "answer": "B",
     "explanation": "RDS is a managed service; AWS handles underlying OS and DB engine patching, shifting more responsibility to AWS vs self-managed EC2 databases."},

    {"id": 10, "domain": "Security", "topic": "IAM",
     "q": "What is the recommended best practice for the AWS account root user?",
     "options": {"A": "Use it for daily administrative tasks", "B": "Share its credentials with the whole team", "C": "Enable MFA and avoid using it for everyday tasks", "D": "Delete it after account creation"},
     "answer": "C",
     "explanation": "Root user should have MFA enabled, credentials locked away, and only be used for account-level tasks that require it -- not daily operations."},

    {"id": 11, "domain": "Security", "topic": "IAM",
     "q": "Which IAM feature allows you to grant temporary access to AWS resources without creating a permanent IAM user?",
     "options": {"A": "IAM Group", "B": "IAM Role", "C": "IAM Policy", "D": "Access Key"},
     "answer": "B",
     "explanation": "IAM Roles provide temporary security credentials via STS, ideal for cross-account access, federation, and EC2 instance permissions."},

    {"id": 12, "domain": "Security", "topic": "Encryption",
     "q": "By default, is data encrypted at rest in a new Amazon S3 bucket?",
     "options": {"A": "Yes, S3 applies SSE-S3 encryption by default to all new objects", "B": "No, encryption must always be manually enabled", "C": "Only for Glacier storage class", "D": "Only if versioning is enabled"},
     "answer": "A",
     "explanation": "Since Jan 2023, Amazon S3 automatically applies SSE-S3 server-side encryption to all new objects by default at no additional cost."},

    {"id": 13, "domain": "Security", "topic": "Encryption",
     "q": "Which statement about Amazon EBS volume encryption is correct?",
     "options": {"A": "EBS volumes are encrypted by default account-wide with no configuration", "B": "EBS encryption-by-default can be enabled per-region as an account setting", "C": "EBS volumes can never be encrypted", "D": "Only EBS snapshots can be encrypted, not volumes"},
     "answer": "B",
     "explanation": "EBS encryption is NOT on by default account-wide out of the box -- but you CAN turn on 'Encryption by default' as a per-Region account setting so all new volumes/snapshots are auto-encrypted."},

    {"id": 14, "domain": "Security", "topic": "WAF & Shield",
     "q": "Which service protects web applications from common exploits like SQL injection and cross-site scripting by filtering HTTP/HTTPS requests?",
     "options": {"A": "AWS Shield", "B": "AWS WAF", "C": "AWS Firewall Manager", "D": "Security Groups"},
     "answer": "B",
     "explanation": "AWS WAF (Web Application Firewall) lets you create rules to filter web traffic based on conditions like IP, SQLi, XSS patterns -- it operates at Layer 7."},

    {"id": 15, "domain": "Security", "topic": "WAF & Shield",
     "q": "What does AWS Shield protect against?",
     "options": {"A": "SQL injection attacks", "B": "DDoS attacks", "C": "Malware on EC2 instances", "D": "Unauthorized IAM access"},
     "answer": "B",
     "explanation": "AWS Shield protects against Distributed Denial of Service (DDoS) attacks. Shield Standard is free/automatic; Shield Advanced offers enhanced protection + cost protection at added cost."},

    {"id": 16, "domain": "Security", "topic": "WAF & Shield",
     "q": "A company wants to centrally manage AWS WAF rules and Shield Advanced protections across multiple accounts. Which service should they use?",
     "options": {"A": "AWS Organizations", "B": "AWS Firewall Manager", "C": "AWS Config", "D": "IAM Policies"},
     "answer": "B",
     "explanation": "AWS Firewall Manager centrally configures and manages firewall rules (WAF, Shield Advanced, Security Groups) across accounts in an AWS Organization."},

    {"id": 17, "domain": "Security", "topic": "Key Management",
     "q": "A company needs a single-tenant, dedicated hardware device to manage encryption keys for strict compliance requirements. Which service fits?",
     "options": {"A": "AWS KMS", "B": "AWS CloudHSM", "C": "AWS Secrets Manager", "D": "ACM"},
     "answer": "B",
     "explanation": "CloudHSM provides dedicated, single-tenant FIPS 140-2 Level 3 validated hardware, vs KMS which is a shared multi-tenant managed service."},

    {"id": 18, "domain": "Security", "topic": "Key Management",
     "q": "Which service is purpose-built for storing and automatically rotating database credentials?",
     "options": {"A": "Systems Manager Parameter Store", "B": "AWS Secrets Manager", "C": "IAM", "D": "AWS KMS"},
     "answer": "B",
     "explanation": "Secrets Manager natively supports automatic rotation (e.g. with RDS); Parameter Store can store secrets but has no native rotation."},

    {"id": 19, "domain": "Security", "topic": "Compliance",
     "q": "Which AWS resource provides on-demand access to security and compliance documentation (like SOC reports, ISO certifications)?",
     "options": {"A": "AWS Trusted Advisor", "B": "AWS Artifact", "C": "AWS Config", "D": "AWS Inspector"},
     "answer": "B",
     "explanation": "AWS Artifact is the self-service portal for compliance reports and agreements (SOC, PCI, ISO, BAA, etc.)."},

    {"id": 20, "domain": "Security", "topic": "Monitoring & Detection",
     "q": "Which service uses machine learning to continuously monitor for malicious activity and unauthorized behavior across your AWS accounts?",
     "options": {"A": "Amazon Inspector", "B": "Amazon GuardDuty", "C": "AWS Config", "D": "AWS CloudTrail"},
     "answer": "B",
     "explanation": "GuardDuty is a threat detection service using ML and threat intelligence to identify anomalous/malicious activity (e.g. compromised instances, unusual API calls)."},

    {"id": 21, "domain": "Security", "topic": "Monitoring & Detection",
     "q": "Which service assesses EC2 instances and container images for software vulnerabilities and unintended network exposure?",
     "options": {"A": "Amazon Inspector", "B": "Amazon Macie", "C": "AWS Config", "D": "GuardDuty"},
     "answer": "A",
     "explanation": "Amazon Inspector automatically scans workloads (EC2, ECR images, Lambda) for known software vulnerabilities (CVEs) and network reachability issues."},

    {"id": 22, "domain": "Security", "topic": "Monitoring & Detection",
     "q": "Which service uses ML to discover and protect sensitive data like PII stored in Amazon S3?",
     "options": {"A": "Amazon Macie", "B": "Amazon Inspector", "C": "AWS Config", "D": "GuardDuty"},
     "answer": "A",
     "explanation": "Amazon Macie specializes in discovering and classifying sensitive data (PII, credentials) within S3 buckets."},

    {"id": 23, "domain": "Security", "topic": "DDoS & Network Security",
     "q": "Which statement correctly differentiates a Security Group from a Network ACL?",
     "options": {"A": "Security Groups are stateless; NACLs are stateful", "B": "Security Groups operate at subnet level; NACLs at instance level", "C": "Security Groups are stateful and instance-level; NACLs are stateless and subnet-level", "D": "There is no difference"},
     "answer": "C",
     "explanation": "Security Groups: stateful, instance-level, allow-rules only. NACLs: stateless, subnet-level, allow AND deny rules, evaluated in order."},

    # ---------------- DOMAIN 3: TECHNOLOGY & SERVICES ----------------
    {"id": 24, "domain": "Technology", "topic": "Compute - EC2",
     "q": "Which EC2 pricing model offers the largest discount but can be interrupted by AWS with a 2-minute warning?",
     "options": {"A": "On-Demand", "B": "Reserved Instances", "C": "Spot Instances", "D": "Savings Plans"},
     "answer": "C",
     "explanation": "Spot Instances offer up to 90% discount vs On-Demand but AWS can reclaim capacity with a 2-minute interruption notice -- best for fault-tolerant, flexible workloads."},

    {"id": 25, "domain": "Technology", "topic": "Compute - EC2",
     "q": "A company has predictable, steady-state workloads running for 1-3 years. Which pricing model minimizes cost?",
     "options": {"A": "On-Demand", "B": "Spot Instances", "C": "Reserved Instances / Savings Plans", "D": "Dedicated Hosts only"},
     "answer": "C",
     "explanation": "Reserved Instances or Savings Plans offer significant discounts (up to 72%) for steady-state, predictable usage committed over 1 or 3 years."},

    {"id": 26, "domain": "Technology", "topic": "Compute - Serverless",
     "q": "What is the maximum execution time for a single AWS Lambda function invocation?",
     "options": {"A": "5 minutes", "B": "15 minutes", "C": "1 hour", "D": "Unlimited"},
     "answer": "B",
     "explanation": "Lambda functions have a maximum timeout of 15 minutes per invocation; for longer-running tasks, consider Fargate, EC2, or Step Functions."},

    {"id": 27, "domain": "Technology", "topic": "Compute - Containers",
     "q": "A company wants to run containers WITHOUT managing any underlying EC2 servers. Which service/launch type fits?",
     "options": {"A": "ECS with EC2 launch type", "B": "ECS or EKS with Fargate launch type", "C": "Plain EC2 with Docker installed", "D": "Elastic Beanstalk"},
     "answer": "B",
     "explanation": "Fargate is the serverless compute engine for containers -- works with both ECS and EKS, removing the need to provision/manage EC2 instances."},

    {"id": 28, "domain": "Technology", "topic": "Storage - S3",
     "q": "Which S3 storage class is best for data accessed once a quarter, needing millisecond retrieval, at the lowest storage cost among instantly-accessible tiers?",
     "options": {"A": "S3 Standard", "B": "S3 Standard-IA", "C": "S3 Intelligent-Tiering", "D": "S3 Glacier Instant Retrieval"},
     "answer": "D",
     "explanation": "S3 Glacier Instant Retrieval is designed for rarely accessed data (quarterly) that still needs millisecond retrieval, cheaper than Standard-IA for archival-frequency access."},

    {"id": 29, "domain": "Technology", "topic": "Storage - S3",
     "q": "Which S3 feature automatically moves objects between access tiers based on changing access patterns, without performance impact or operational overhead?",
     "options": {"A": "S3 Lifecycle Policies", "B": "S3 Intelligent-Tiering", "C": "S3 Versioning", "D": "S3 Replication"},
     "answer": "B",
     "explanation": "S3 Intelligent-Tiering monitors access patterns and automatically moves objects between tiers (frequent/infrequent/archive) to optimize cost with no retrieval fees."},

    {"id": 30, "domain": "Technology", "topic": "Storage - Block/File",
     "q": "Which storage type must you use for an EC2 instance's root volume by default?",
     "options": {"A": "Amazon S3", "B": "Amazon EBS (or instance store for some types)", "C": "Amazon EFS", "D": "Amazon FSx"},
     "answer": "B",
     "explanation": "EC2 root volumes are backed by Amazon EBS (persistent block storage) in most cases, or instance store (ephemeral) for instance-store-backed AMIs."},

    {"id": 31, "domain": "Technology", "topic": "Storage - Block/File",
     "q": "Which storage service provides a scalable, fully-managed NFS file system that can be mounted concurrently by thousands of EC2 instances?",
     "options": {"A": "Amazon EBS", "B": "Amazon S3", "C": "Amazon EFS", "D": "Amazon Glacier"},
     "answer": "C",
     "explanation": "EFS (Elastic File System) is a shared, elastic NFS file system for Linux workloads, mountable by many EC2 instances simultaneously -- unlike EBS which attaches to one instance at a time."},

    {"id": 32, "domain": "Technology", "topic": "Databases",
     "q": "Which database service is best suited for a relational, ACID-compliant transactional application (like an e-commerce order system)?",
     "options": {"A": "Amazon DynamoDB", "B": "Amazon RDS / Aurora", "C": "Amazon Redshift", "D": "Amazon ElastiCache"},
     "answer": "B",
     "explanation": "RDS/Aurora are managed relational databases (SQL, ACID transactions) ideal for structured transactional workloads."},

    {"id": 33, "domain": "Technology", "topic": "Databases",
     "q": "Which AWS database service is a fully managed, serverless key-value and document NoSQL database with single-digit millisecond performance at any scale?",
     "options": {"A": "Amazon RDS", "B": "Amazon DynamoDB", "C": "Amazon Redshift", "D": "Amazon Neptune"},
     "answer": "B",
     "explanation": "DynamoDB is AWS's serverless NoSQL database, built for massive scale with consistent low-latency performance."},

    {"id": 34, "domain": "Technology", "topic": "Databases",
     "q": "Which service is purpose-built for large-scale data warehousing and complex analytical (OLAP) queries?",
     "options": {"A": "Amazon RDS", "B": "Amazon Redshift", "C": "Amazon DynamoDB", "D": "Amazon ElastiCache"},
     "answer": "B",
     "explanation": "Redshift is AWS's data warehouse service, optimized for complex analytical queries across large datasets (OLAP), unlike RDS which is optimized for OLTP."},

    {"id": 35, "domain": "Technology", "topic": "Databases",
     "q": "Which service provides in-memory caching to significantly speed up application response times, commonly used for session storage or DB query caching?",
     "options": {"A": "Amazon ElastiCache", "B": "Amazon RDS", "C": "Amazon S3", "D": "AWS Storage Gateway"},
     "answer": "A",
     "explanation": "ElastiCache (Redis or Memcached) provides fully managed in-memory data stores for caching, reducing load on primary databases."},

    {"id": 36, "domain": "Technology", "topic": "Networking",
     "q": "Which AWS service provides a dedicated, private, physical network connection between an on-premises data center and AWS?",
     "options": {"A": "Site-to-Site VPN", "B": "AWS Direct Connect", "C": "VPC Peering", "D": "Transit Gateway"},
     "answer": "B",
     "explanation": "Direct Connect provides a dedicated physical line -- more consistent bandwidth/latency than VPN, but takes longer to provision and costs more."},

    {"id": 37, "domain": "Technology", "topic": "Networking",
     "q": "Which service should be used to connect many VPCs and on-premises networks together through a single hub, avoiding the non-transitive limitation of VPC peering?",
     "options": {"A": "VPC Peering", "B": "AWS Transit Gateway", "C": "Internet Gateway", "D": "NAT Gateway"},
     "answer": "B",
     "explanation": "Transit Gateway acts as a central hub, enabling transitive routing between many VPCs and on-premises networks -- VPC Peering connections are NOT transitive."},

    {"id": 38, "domain": "Technology", "topic": "Networking",
     "q": "Which component allows resources in a PRIVATE subnet to initiate outbound connections to the internet, while remaining unreachable from the internet?",
     "options": {"A": "Internet Gateway", "B": "NAT Gateway", "C": "VPC Peering", "D": "Security Group"},
     "answer": "B",
     "explanation": "NAT Gateway enables outbound-only internet access for private subnet resources (e.g. for patching) without exposing them to inbound internet traffic."},

    {"id": 39, "domain": "Technology", "topic": "Content Delivery",
     "q": "Which service caches content at edge locations worldwide to reduce latency for end users accessing static/dynamic web content?",
     "options": {"A": "Amazon Route 53", "B": "Amazon CloudFront", "C": "AWS Global Accelerator", "D": "Elastic Load Balancer"},
     "answer": "B",
     "explanation": "CloudFront is AWS's CDN, caching content at edge locations to reduce latency for end users."},

    {"id": 40, "domain": "Technology", "topic": "Management & Monitoring",
     "q": "Which service tracks configuration changes to AWS resources over time and checks compliance against desired configurations?",
     "options": {"A": "AWS CloudTrail", "B": "AWS Config", "C": "Amazon CloudWatch", "D": "AWS Trusted Advisor"},
     "answer": "B",
     "explanation": "AWS Config records resource configuration changes over time and evaluates compliance against defined rules -- different from CloudTrail (API call logging)."},

    {"id": 41, "domain": "Technology", "topic": "Management & Monitoring",
     "q": "Which service logs and tracks every API call made within an AWS account, useful for governance and auditing 'who did what'?",
     "options": {"A": "AWS Config", "B": "AWS CloudTrail", "C": "Amazon CloudWatch", "D": "VPC Flow Logs"},
     "answer": "B",
     "explanation": "CloudTrail is the API activity/audit log -- captures identity, time, and details of every API call for governance and security auditing."},

    # ---------------- DOMAIN 4: BILLING, PRICING & SUPPORT ----------------
    {"id": 42, "domain": "Billing", "topic": "Support Plans",
     "q": "Which AWS Support plan is the minimum required to get access to a Technical Account Manager (TAM)?",
     "options": {"A": "Basic", "B": "Developer", "C": "Business", "D": "Enterprise (On-Ramp or Enterprise)"},
     "answer": "D",
     "explanation": "A dedicated TAM is included only with Enterprise On-Ramp and Enterprise Support plans, not Business support."},

    {"id": 43, "domain": "Billing", "topic": "Support Plans",
     "q": "Which support plan provides 24/7 access to Cloud Support Engineers via phone, chat, and email, with a 1-hour response time for urgent cases?",
     "options": {"A": "Basic", "B": "Developer", "C": "Business", "D": "None, all plans have this"},
     "answer": "C",
     "explanation": "Business Support offers 24/7 phone/chat/email access with <1 hour response for production-system-down cases; Developer support has business-hours email only."},

    {"id": 44, "domain": "Billing", "topic": "Pricing Tools",
     "q": "Which tool helps estimate the cost of AWS services BEFORE deploying any resources?",
     "options": {"A": "AWS Cost Explorer", "B": "AWS Pricing Calculator", "C": "AWS Budgets", "D": "AWS Cost and Usage Report"},
     "answer": "B",
     "explanation": "AWS Pricing Calculator estimates costs for planned/hypothetical architectures BEFORE deployment. Cost Explorer analyzes ACTUAL historical spend."},

    {"id": 45, "domain": "Billing", "topic": "Pricing Tools",
     "q": "Which tool lets you set custom cost/usage thresholds and receive alerts when you exceed (or are forecasted to exceed) them?",
     "options": {"A": "AWS Budgets", "B": "AWS Cost Explorer", "C": "AWS Pricing Calculator", "D": "Trusted Advisor"},
     "answer": "A",
     "explanation": "AWS Budgets lets you set custom cost/usage/RI-utilization thresholds and triggers alerts, including forecasted overages."},

    {"id": 46, "domain": "Billing", "topic": "Cost Management",
     "q": "Which AWS feature allows a management account to consolidate billing across multiple linked accounts and gain volume pricing discounts?",
     "options": {"A": "IAM Roles", "B": "AWS Organizations - Consolidated Billing", "C": "AWS Budgets", "D": "AWS Cost Explorer"},
     "answer": "B",
     "explanation": "Consolidated Billing (part of AWS Organizations) combines usage across linked accounts into a single bill and can unlock volume pricing/RI sharing."},

    {"id": 47, "domain": "Billing", "topic": "Trusted Advisor",
     "q": "Which categories does AWS Trusted Advisor check across?",
     "options": {"A": "Only cost optimization", "B": "Cost Optimization, Performance, Security, Fault Tolerance, Service Limits", "C": "Only security", "D": "Only service limits"},
     "answer": "B",
     "explanation": "Trusted Advisor evaluates 5 categories: Cost Optimization, Performance, Security, Fault Tolerance, and Service Limits (full checks require Business/Enterprise support)."},
]

DOMAIN_WEIGHTAGE = {
    "Cloud Concepts": "24%",
    "Security": "30%",
    "Technology": "34%",
    "Billing": "12%",
}

# ---------------------------------------------------------------------------
# QUIZ ENGINE
# ---------------------------------------------------------------------------

def run_quiz(shuffle=True, num_questions=None):
    questions = QUESTIONS.copy()
    if shuffle:
        random.shuffle(questions)
    if num_questions:
        questions = questions[:num_questions]

    print("=" * 70)
    print("AWS CLOUD PRACTITIONER (CLF-C02) - MEGA REVISION TEST")
    print(f"Total Questions: {len(questions)} | Exam Mode: No feedback until submission")
    print("=" * 70)
    print()

    user_answers = {}

    for i, q in enumerate(questions, 1):
        print(f"Q{i}. [{q['domain']} / {q['topic']}]")
        print(q["q"])
        for opt_key in sorted(q["options"].keys()):
            print(f"   {opt_key}. {q['options'][opt_key]}")
        while True:
            ans = input("Your answer (A/B/C/D): ").strip().upper()
            if ans in q["options"]:
                break
            print("Invalid input. Enter A, B, C, or D.")
        user_answers[q["id"]] = ans
        print()

    return grade_quiz(questions, user_answers)


def grade_quiz(questions, user_answers):
    results = []
    domain_stats = {}
    topic_stats = {}

    for q in questions:
        user_ans = user_answers.get(q["id"])
        correct = (user_ans == q["answer"])
        results.append({
            "id": q["id"],
            "domain": q["domain"],
            "topic": q["topic"],
            "question": q["q"],
            "your_answer": user_ans,
            "correct_answer": q["answer"],
            "is_correct": correct,
            "explanation": q["explanation"],
        })

        d = domain_stats.setdefault(q["domain"], {"correct": 0, "total": 0})
        d["total"] += 1
        d["correct"] += int(correct)

        t = topic_stats.setdefault(q["topic"], {"correct": 0, "total": 0})
        t["total"] += 1
        t["correct"] += int(correct)

    total_correct = sum(r["is_correct"] for r in results)
    total_questions = len(results)
    overall_pct = round((total_correct / total_questions) * 100, 1) if total_questions else 0

    print_report(results, domain_stats, topic_stats, total_correct, total_questions, overall_pct)
    export_results(results, domain_stats, topic_stats, total_correct, total_questions, overall_pct)

    return results


def print_report(results, domain_stats, topic_stats, total_correct, total_questions, overall_pct):
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Overall Score: {total_correct}/{total_questions} ({overall_pct}%)")
    print()

    print("--- Domain-wise Breakdown ---")
    for domain, stats in sorted(domain_stats.items()):
        pct = round((stats["correct"] / stats["total"]) * 100, 1)
        weight = DOMAIN_WEIGHTAGE.get(domain, "")
        flag = "  <-- WEAK" if pct < 70 else ""
        print(f"{domain} (exam weight {weight}): {stats['correct']}/{stats['total']} ({pct}%){flag}")
    print()

    print("--- Topic-wise Breakdown ---")
    for topic, stats in sorted(topic_stats.items(), key=lambda x: (x[1]['correct']/x[1]['total'])):
        pct = round((stats["correct"] / stats["total"]) * 100, 1)
        flag = "  <-- WEAK" if pct < 70 else ""
        print(f"{topic}: {stats['correct']}/{stats['total']} ({pct}%){flag}")
    print()

    wrong = [r for r in results if not r["is_correct"]]
    if wrong:
        print("--- Questions Missed (Review These) ---")
        for r in wrong:
            print(f"\nQ{r['id']} [{r['domain']} / {r['topic']}]")
            print(f"  {r['question']}")
            print(f"  Your answer: {r['your_answer']} | Correct: {r['correct_answer']}")
            print(f"  Why: {r['explanation']}")
    else:
        print("Perfect score! No weak areas detected in this run.")
    print()


def export_results(results, domain_stats, topic_stats, total_correct, total_questions, overall_pct):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ccp_mega_quiz_results_{timestamp}.json"

    export_data = {
        "timestamp": timestamp,
        "overall_score": f"{total_correct}/{total_questions}",
        "overall_percentage": overall_pct,
        "domain_breakdown": {
            d: {
                "score": f"{s['correct']}/{s['total']}",
                "percentage": round((s["correct"] / s["total"]) * 100, 1),
                "exam_weight": DOMAIN_WEIGHTAGE.get(d, ""),
            } for d, s in domain_stats.items()
        },
        "topic_breakdown": {
            t: {
                "score": f"{s['correct']}/{s['total']}",
                "percentage": round((s["correct"] / s["total"]) * 100, 1),
            } for t, s in topic_stats.items()
        },
        "missed_questions": [
            {
                "id": r["id"], "domain": r["domain"], "topic": r["topic"],
                "question": r["question"], "your_answer": r["your_answer"],
                "correct_answer": r["correct_answer"],
            } for r in results if not r["is_correct"]
        ],
    }

    with open(filename, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"Results exported to: {filename}")
    print("Paste the contents of this file (or the summary above) back to Claude for weak-area analysis.")


if __name__ == "__main__":
    run_quiz(shuffle=True)
