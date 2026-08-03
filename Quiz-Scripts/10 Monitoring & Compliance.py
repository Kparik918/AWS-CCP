#!/usr/bin/env python3
"""
AWS Certified Cloud Practitioner (CLF-C02)
Module 10 — Monitoring And Compliance
Exam-Mode Practice Quiz Script

Covers: CloudWatch, APIs (foundational), CloudTrail, AWS Config, Audit Manager,
AWS Artifact, AWS Organizations, Control Tower / Service Catalog / License Manager,
AWS Health, Trusted Advisor, IAM Access Analyzer, Compliance (GDPR/HIPAA, Shared
Responsibility Model).

Behavior:
- Questions and options are shuffled per run.
- During the quiz, no correct/incorrect feedback is given per question — only
  "Answer recorded." (real exam-mode behavior).
- After submission, print_results() reveals score, topic-wise weakest-first
  breakdown, weak-topic flags (<70%), and a Missed Questions Review.
- Final report is auto-exported to "Monitoring And Compliance-Results.txt".
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Monitoring And Compliance"

# ---------------------------------------------------------------------------
# QUESTIONS
# Each tuple: (topic, question_text, [options], correct_answer, explanation)
# correct_answer: single 0-based int for single-select
# correct_answer: list/tuple of 0-based ints for multi-select ("Select TWO/THREE")
# ---------------------------------------------------------------------------

QUESTIONS = [
    # ---------------- CloudWatch (heavy weight) ----------------
    ("CloudWatch",
     "What is the PRIMARY purpose of Amazon CloudWatch?",
     ["To log every API call made across an AWS account",
      "To collect and act on metrics, logs, and events for monitoring the health and performance of AWS resources",
      "To store AWS's own compliance certifications and audit reports",
      "To centrally manage permissions across multiple AWS accounts"],
     1,
     "CloudWatch's core job is collecting metrics/logs/events to answer 'is my system healthy?' — the dashboard is just one feature, not the whole service."),

    ("CloudWatch",
     "A company wants to be notified automatically when an EC2 instance's CPU utilization exceeds 90%, and have Auto Scaling add more instances in response. Which CloudWatch feature enables this?",
     ["CloudWatch Logs Insights", "CloudWatch Alarms", "CloudWatch Events only", "CloudWatch Dashboards"],
     1,
     "CloudWatch Alarms watch a metric against a threshold and can trigger real actions such as SNS notifications, Auto Scaling, Lambda invocations, or stopping/terminating instances."),

    ("CloudWatch",
     "What is the interval and cost of AWS's Basic (Standard) EC2 monitoring in CloudWatch?",
     ["1-minute intervals, free", "5-minute intervals, free", "1-minute intervals, paid", "5-minute intervals, paid"],
     1,
     "Basic monitoring reports metrics every 5 minutes at no extra cost; Detailed Monitoring provides 1-minute intervals but costs extra."),

    ("CloudWatch",
     "Which of the following can a CloudWatch Alarm trigger when a metric breaches its threshold? (Select TWO)",
     ["Send an SNS notification to a developer", "Automatically add or remove EC2 instances via Auto Scaling",
      "Generate a SOC 2 compliance report", "Sign a Business Associate Addendum (BAA)"],
     [0, 1],
     "CloudWatch Alarms can trigger SNS notifications and Auto Scaling actions (as well as Lambda invocations or stopping/terminating instances); compliance reports and BAAs come from Audit Manager and Artifact, not CloudWatch."),

    ("CloudWatch",
     "A CloudWatch Log Group contains what kind of structure?",
     ["Log Streams, which organize individual log data from a resource", "SCPs applied to member accounts",
      "Configuration snapshots of resources over time", "API call records with source IP addresses"],
     0,
     "CloudWatch Logs are organized into Log Groups, which contain Log Streams — the sequences of log events from a specific source, with configurable retention."),

    ("CloudWatch",
     "EXAM TRAP: A CCP exam question states 'CloudWatch is just a dashboard for viewing graphs.' What is the flaw in this statement?",
     ["There is no flaw — that is CloudWatch's only function",
      "The dashboard is only one feature; CloudWatch's core function is collecting and acting on metrics, logs, and events",
      "CloudWatch does not have dashboards at all",
      "Dashboards are actually a CloudTrail feature, not CloudWatch"],
     1,
     "This is a classic exam trap — CloudWatch's real value is active collection and automated response (alarms, actions) on metrics/logs/events, not just visualization."),

    ("CloudWatch",
     "Which query capability lets you search and analyze log data within CloudWatch (e.g., find all ERROR entries from the last 7 days)?",
     ["CloudTrail Insights", "CloudWatch Logs Insights", "AWS Config Rules", "Trusted Advisor Security Checks"],
     1,
     "CloudWatch Logs Insights provides a purpose-built query language for searching and analyzing log data stored in CloudWatch Logs."),

    # ---------------- APIs (foundational, light weight) ----------------
    ("APIs",
     "In the context of AWS, what is an 'API call'?",
     ["A phone call made to AWS support", "The actual request sent to trigger an action against an AWS service",
      "A CloudWatch alarm notification", "A billing invoice generated monthly"],
     1,
     "An API call is the request a user, script, or service sends to AWS to perform an action — even clicking a button in the console generates an API call behind the scenes."),

    ("APIs",
     "Why is understanding API calls foundational to understanding CloudTrail?",
     ["CloudTrail only logs CLI commands, not console actions",
      "CloudTrail's entire job is logging API calls, including those made silently by the console UI",
      "API calls are unrelated to CloudTrail's function",
      "CloudTrail converts API calls into CloudWatch metrics"],
     1,
     "Every action in AWS — console clicks, CLI commands, SDK calls — happens via an API call, and CloudTrail's core function is logging exactly these calls."),

    # ---------------- CloudTrail (heavy weight) ----------------
    ("CloudTrail",
     "What core question does AWS CloudTrail answer?",
     ["Is my system healthy right now?", "Who did what, where, and when?",
      "Is my resource configured the way it should be?", "Is AWS's own infrastructure certified compliant?"],
     1,
     "CloudTrail is the auditing service — it provides a tamper-proof record of account activity to answer 'who did what, when, and from where.'"),

    ("CloudTrail",
     "Where are CloudTrail log files stored?",
     ["DynamoDB tables", "Securely in S3 buckets", "CloudWatch Log Groups only", "AWS Artifact repository"],
     1,
     "CloudTrail delivers log files securely to S3 buckets, where they can be retained indefinitely and validated for integrity."),

    ("CloudTrail",
     "A security team discovers that an S3 bucket's permissions were changed to public. Which service would they use to find exactly WHO made that change and when?",
     ["AWS Config", "CloudWatch", "CloudTrail", "Trusted Advisor"],
     2,
     "CloudTrail logs the specific API call (e.g., PutBucketAcl), including the IAM identity, timestamp, and source IP — exactly what's needed for this kind of forensic investigation."),

    ("CloudTrail",
     "What does CloudTrail Insights specifically help detect?",
     ["Configuration drift in EBS volumes", "Anomalies such as unusual error rates or unusual API request volumes",
      "Idle Reserved Instances", "Publicly exposed IAM roles"],
     1,
     "CloudTrail Insights analyzes logged events to surface anomalous activity patterns, like spikes in error rates or unusual call volumes, that may indicate a problem."),

    ("CloudTrail",
     "EXAM TRAP: Which statement correctly distinguishes CloudWatch from CloudTrail?",
     ["CloudWatch tracks 'who did it', CloudTrail tracks system performance",
      "CloudWatch watches performance/operational health, CloudTrail trails API activity and user actions",
      "They are two names for the exact same service", "CloudTrail can trigger Auto Scaling actions, CloudWatch cannot"],
     1,
     "This is one of the most tested distinctions on the CCP exam: CloudWatch = performance/operational monitoring; CloudTrail = activity/API auditing. CloudTrail does not trigger alarms or automation on its own."),

    ("CloudTrail",
     "By default, how long can CloudTrail management event logs be retained when delivered to S3?",
     ["30 days maximum", "90 days maximum", "Indefinitely", "7 days, unless Detailed Monitoring is enabled"],
     2,
     "CloudTrail logs stored in S3 can be kept indefinitely, subject to the customer's own lifecycle/retention policy on the bucket."),

    # ---------------- AWS Config ----------------
    ("AWS Config",
     "What does AWS Config primarily assess?",
     ["Who performed a specific API action", "Whether resource configurations match defined rules, and tracks configuration changes over time",
      "AWS's own SOC and ISO compliance reports", "Cost optimization opportunities across accounts"],
     1,
     "AWS Config continuously evaluates and records resource configurations against rules you define, enabling drift detection and compliance reporting."),

    ("AWS Config",
     "A company wants to continuously verify that every new EBS volume created has encryption enabled, and be alerted if one doesn't. Which service fits best?",
     ["CloudTrail", "AWS Config", "AWS Artifact", "AWS Health"],
     1,
     "This is a configuration-state compliance check over time — exactly what AWS Config Rules are designed for, including optional auto-remediation via Systems Manager."),

    ("AWS Config",
     "EXAM TRAP: Can AWS Config tell you WHICH IAM user made a specific configuration change?",
     ["Yes, Config natively logs the identity of every change", "No — Config shows configuration state/history, not who made the change (that's CloudTrail's job)",
      "Yes, but only for EC2 resources", "No, Config cannot track changes at all"],
     1,
     "AWS Config focuses on 'what changed' in a resource's configuration over time; determining 'who' made the change requires cross-referencing CloudTrail."),

    ("AWS Config",
     "Which capability allows AWS Config to fix non-compliant resources automatically?",
     ["Integration with Systems Manager Automation documents", "CloudTrail Insights", "Trusted Advisor remediation checks", "AWS Artifact agreements"],
     0,
     "AWS Config can trigger auto-remediation of non-compliant resources through Systems Manager Automation documents."),

    # ---------------- Audit Manager ----------------
    ("Audit Manager",
     "What is the primary function of AWS Audit Manager?",
     ["Providing AWS's own SOC/ISO compliance certifications", "Automating the collection of evidence needed to prove compliance with regulatory frameworks like GDPR or HIPAA",
      "Logging every API call made in an account", "Managing multi-account governance via SCPs"],
     1,
     "Audit Manager continuously and automatically gathers evidence (often pulling from CloudTrail and Config) to streamline formal compliance audits."),

    ("Audit Manager",
     "Audit Manager primarily aggregates evidence from which two services?",
     ["Trusted Advisor and IAM Access Analyzer", "CloudTrail and AWS Config", "AWS Health and License Manager", "Service Catalog and Control Tower"],
     1,
     "Audit Manager sits on top of CloudTrail (activity logs) and AWS Config (configuration state) as an evidence-aggregation and reporting layer for formal audits."),

    ("Audit Manager",
     "EXAM TRAP: A company needs evidence of ITS OWN compliance with PCI-DSS for an external auditor. Which service should they use?",
     ["AWS Artifact, since it covers all compliance needs", "AWS Audit Manager, since it collects the customer's own compliance evidence",
      "AWS Health", "License Manager"],
     1,
     "Audit Manager collects evidence about the customer's workloads/resources; AWS Artifact instead provides AWS's own compliance documentation — a very common point of confusion."),

    # ---------------- AWS Artifact ----------------
    ("AWS Artifact",
     "What does AWS Artifact provide?",
     ["A customer's own resource configuration compliance evidence", "On-demand access to AWS's own security and compliance documentation, reports, and agreements",
      "Real-time performance metrics for AWS resources", "A curated catalog of approved AWS resources for self-service deployment"],
     1,
     "AWS Artifact is a self-service portal for AWS's own compliance documents — SOC/ISO/PCI reports and agreements like BAAs — proving AWS's infrastructure itself is certified."),

    ("AWS Artifact",
     "What are the two types of content available in AWS Artifact?",
     ["Metrics and Logs", "Agreements and Reports", "Rules and Remediations", "Accounts and Organizational Units"],
     1,
     "AWS Artifact Agreements let you manage/accept agreements like BAAs, while AWS Artifact Reports provide third-party audit reports such as SOC and ISO certifications."),

    ("AWS Artifact",
     "EXAM TRAP: A healthcare company needs to sign a Business Associate Addendum (BAA) with AWS for HIPAA purposes. Which service handles this?",
     ["AWS Audit Manager", "AWS Artifact Agreements", "AWS Config", "AWS Organizations"],
     1,
     "BAAs and similar data-usage agreements with AWS are managed through AWS Artifact Agreements, not Audit Manager (which handles the customer's own evidence collection)."),

    ("AWS Artifact",
     "How much does AWS Artifact cost to use?",
     ["Pay per report downloaded", "Free", "Priced per assessment", "Included only with Enterprise Support"],
     1,
     "AWS Artifact is free to use — it simply provides self-service access to AWS's existing compliance documentation."),

    # ---------------- AWS Organizations ----------------
    ("AWS Organizations",
     "In AWS Organizations, what is the relationship between the management account and member accounts?",
     ["All accounts have identical, independent billing with no relationship", "The management (parent) account centrally governs and can enforce policies on member (child) accounts",
      "Member accounts control the management account's permissions", "There is no billing relationship between accounts"],
     1,
     "AWS Organizations lets one management account centrally govern multiple member accounts, including consolidated billing and Service Control Policies (SCPs)."),

    ("AWS Organizations",
     "How does AWS Organizations help REDUCE costs across multiple accounts?",
     ["By deleting unused resources automatically", "Through consolidated billing, which combines usage across accounts to reach volume pricing tiers faster and can share Reserved Instance / Savings Plan discounts",
      "By restricting all accounts to the Free Tier only", "Organizations has no cost benefit, only governance benefit"],
     1,
     "Consolidated billing combines usage across all member accounts, helping the organization reach volume discount tiers sooner and enabling sharing of unused Reserved Instance or Savings Plan discounts across accounts."),

    ("AWS Organizations",
     "EXAM TRAP: Do Service Control Policies (SCPs) grant permissions to IAM users in member accounts?",
     ["Yes, SCPs grant permissions directly to all users", "No — SCPs only set the MAXIMUM available permissions; they restrict, they never grant access on their own",
      "Yes, but only for root users", "SCPs are unrelated to permissions entirely"],
     1,
     "This is a heavily tested trap: SCPs act as permission boundaries/guardrails. Even if an IAM policy allows an action, an SCP can still block it — and SCPs alone never grant access."),

    ("AWS Organizations",
     "What feature of AWS Organizations allows you to apply SCPs to a group of accounts at once instead of one by one?",
     ["Organizational Units (OUs)", "CloudWatch Log Groups", "Trusted Advisor categories", "License Manager pools"],
     0,
     "Organizational Units (OUs) let you group member accounts and apply SCPs collectively, simplifying governance at scale."),

    # ---------------- Control Tower / Service Catalog / License Manager ----------------
    ("Control Tower & Service Catalog",
     "What is the relationship between AWS Control Tower and AWS Organizations?",
     ["They are unrelated, competing services", "Control Tower is built ON TOP OF Organizations, automating a best-practice multi-account landing zone setup",
      "Organizations is built on top of Control Tower", "Control Tower replaces the need for Organizations entirely"],
     1,
     "Control Tower is essentially an automated, opinionated setup wizard that uses Organizations under the hood to quickly establish a secure, compliant multi-account environment."),

    ("Control Tower & Service Catalog",
     "What is the PRIMARY purpose of AWS Service Catalog?",
     ["To log API activity across accounts", "To let admins create a curated catalog of approved AWS resources that end users can self-service deploy without full AWS console access",
      "To manage third-party software license usage", "To provide AWS's own compliance certifications"],
     1,
     "Service Catalog lets organizations standardize and govern what resources users can launch — via approved, pre-built CloudFormation-based products — without granting broad IAM permissions."),

    ("Control Tower & Service Catalog",
     "A company wants developers to be able to launch only pre-approved, standardized infrastructure (e.g., an approved EC2 template) without giving them full EC2 permissions. Which service fits best?",
     ["AWS Service Catalog", "AWS Config", "Trusted Advisor", "AWS Health"],
     0,
     "Service Catalog provides self-service access to admin-approved 'products' (CloudFormation templates), enforcing governance while removing the need for broad direct permissions."),

    ("Control Tower & Service Catalog",
     "What does AWS License Manager help track and manage?",
     ["AWS service quota limits", "Third-party software license usage and costs (e.g., Windows Server, Oracle) across an AWS footprint",
      "SCP boundaries across Organizational Units", "CloudWatch alarm thresholds"],
     1,
     "License Manager is specifically for tracking and enforcing third-party software licensing, which is distinct from AWS's own service limits/quotas."),

    ("Control Tower & Service Catalog",
     "EXAM TRAP: Is AWS License Manager the same thing as AWS service limit tracking?",
     ["Yes, they are identical", "No — License Manager tracks third-party software licenses, while AWS service quotas/limits are a separate concept (tracked via Service Quotas/Trusted Advisor)",
      "Yes, License Manager replaced Service Quotas", "No, License Manager only applies to AWS-native services"],
     1,
     "A common trap: License Manager is about third-party software licensing costs/compliance, not AWS account service limits, which fall under Service Quotas and Trusted Advisor's Service Limits category."),

    # ---------------- AWS Health ----------------
    ("AWS Health",
     "What does AWS Health provide that the public AWS Service Health Dashboard does NOT?",
     ["General service status visible to all customers", "Account-specific events, planned changes, and notifications relevant to YOUR resources",
      "SOC/ISO compliance reports", "Consolidated billing across accounts"],
     1,
     "AWS Health delivers personalized, account-specific information about events and changes affecting your resources, unlike the general public Service Health Dashboard."),

    ("AWS Health",
     "EXAM TRAP: A company wants to know about an AWS-side outage specifically affecting THEIR account's resources. Which is the correct tool?",
     ["The public AWS Service Health Dashboard, since it shows all outages", "AWS Health, since it is account-specific",
      "AWS Artifact", "License Manager"],
     1,
     "The public Service Health Dashboard shows general, all-customer service status; AWS Health is the account-specific tool the exam expects for personalized impact/outage information."),

    # ---------------- Trusted Advisor ----------------
    ("Trusted Advisor",
     "What are the five categories of checks performed by AWS Trusted Advisor?",
     ["Cost, Performance, Security, Fault Tolerance, Service Limits", "Compliance, Governance, Billing, Networking, Storage",
      "Metrics, Logs, Events, Dashboards, Alarms", "Agreements, Reports, Rules, Evidence, Certificates"],
     0,
     "Trusted Advisor's five categories — Cost Optimization, Performance, Security, Fault Tolerance, and Service Limits — are a high-yield memorization item for the CCP exam."),

    ("Trusted Advisor",
     "EXAM TRAP: Does the AWS Basic support plan include full access to all Trusted Advisor checks?",
     ["Yes, all checks are always free", "No — Basic/Developer plans get only a handful of core checks; full access across all five categories requires Business or Enterprise Support",
      "Yes, but only for Fault Tolerance checks", "No, Trusted Advisor requires a separate paid subscription regardless of support plan"],
     1,
     "A very common trap: Basic and Developer support tiers only unlock a limited set of checks (mainly security); the full set of best-practice checks needs Business or Enterprise Support."),

    ("Trusted Advisor",
     "A company wants proactive recommendations about idle EC2 instances, unused Reserved Instances, and potential cost savings. Which service is designed for this?",
     ["Trusted Advisor's Cost Optimization category", "CloudTrail Insights", "AWS Config Rules", "IAM Access Analyzer"],
     0,
     "Trusted Advisor's Cost Optimization category specifically flags idle or underutilized resources and unused Reserved Instances to help reduce spend."),

    ("Trusted Advisor",
     "What distinguishes Trusted Advisor from CloudWatch?",
     ["Trusted Advisor provides prescriptive best-practice recommendations, while CloudWatch provides raw metrics/logs/alarms data",
      "They are functionally identical services", "CloudWatch only works with Enterprise Support", "Trusted Advisor cannot check security settings"],
     0,
     "Trusted Advisor goes beyond raw data by giving proactive, prescriptive recommendations across cost, performance, security, fault tolerance, and service limits."),

    # ---------------- IAM Access Analyzer ----------------
    ("IAM Access Analyzer",
     "What is the primary purpose of IAM Access Analyzer?",
     ["To track software license usage", "To identify resources shared with external entities and validate policies against least-privilege best practices",
      "To log every API call made in an account", "To provide AWS's own SOC/ISO reports"],
     1,
     "IAM Access Analyzer specifically detects unintended external access to resources (like public S3 buckets) and helps enforce least-privilege IAM policies."),

    ("IAM Access Analyzer",
     "A company wants to check whether any S3 bucket has accidentally been made publicly accessible. Which service is BEST suited for this?",
     ["AWS Config only", "IAM Access Analyzer", "AWS Health", "License Manager"],
     1,
     "IAM Access Analyzer is purpose-built to detect unintended external/public access to resources such as S3 buckets, IAM roles, and KMS keys."),

    ("IAM Access Analyzer",
     "EXAM TRAP: How does IAM Access Analyzer differ from Trusted Advisor's security checks?",
     ["They are identical in scope", "Access Analyzer focuses specifically on external access and least-privilege analysis, while Trusted Advisor covers a broader range of best-practice checks (cost, performance, security, fault tolerance, service limits)",
      "Trusted Advisor only checks IAM, while Access Analyzer checks billing", "Access Analyzer requires Enterprise Support, but Trusted Advisor does not"],
     1,
     "Access Analyzer is a narrow, deep tool for external access/least-privilege; Trusted Advisor is broader but shallower, spanning five different categories beyond just access."),

    # ---------------- Compliance / Regulations / Shared Responsibility ----------------
    ("Compliance",
     "GDPR primarily governs which of the following?",
     ["Healthcare data protection in the USA", "Personal data protection and privacy in the EU",
      "Software licensing agreements globally", "AWS's internal service limits"],
     1,
     "GDPR (General Data Protection Regulation) is an EU regulation focused on protecting personal data and privacy."),

    ("Compliance",
     "HIPAA primarily governs which of the following?",
     ["Protected health information (PHI) in the USA", "Personal data privacy in the EU",
      "Software license compliance", "Multi-account governance structures"],
     0,
     "HIPAA (Health Insurance Portability and Accountability Act) is a US regulation focused on protecting health information (PHI)."),

    ("Compliance",
     "Under the AWS Shared Responsibility Model as applied to compliance, which statement is correct?",
     ["AWS is responsible for proving compliance of everything, including customer data configurations",
      "AWS proves its own infrastructure is compliant (via Artifact), while customers are responsible for proving their own workloads are compliant (via Config, CloudTrail, Audit Manager)",
      "Customers are responsible for AWS's physical data center security", "Compliance responsibility does not follow the shared responsibility model"],
     1,
     "AWS secures and certifies the infrastructure 'of the cloud' (proven via Artifact); customers must configure, monitor, and prove compliance of what they put 'in the cloud' using tools like Config, CloudTrail, and Audit Manager."),

    ("Compliance",
     "A company needs to hand external auditors both (a) proof that AWS's own infrastructure meets PCI-DSS, and (b) proof that the company's own workloads meet PCI-DSS. Which TWO services are needed? (Select TWO)",
     ["AWS Artifact (for AWS's own certification)", "AWS Audit Manager (for the company's own evidence)",
      "AWS License Manager", "CloudWatch Dashboards"],
     [0, 1],
     "AWS Artifact supplies AWS's own compliance documentation, while Audit Manager aggregates the customer's own evidence of workload compliance — together covering both sides of the Shared Responsibility Model."),

    # ---------------- Mixed scenario / decision-tree style ----------------
    ("Scenario",
     "A company wants automated alerts sent whenever CPU usage on a fleet of EC2 instances crosses 85%, with no manual checking required. Which service should they configure?",
     ["AWS Config Rules", "CloudWatch Alarms", "CloudTrail Insights", "IAM Access Analyzer"],
     1,
     "This is a real-time performance threshold scenario, which is exactly what CloudWatch Alarms are designed to automate."),

    ("Scenario",
     "A regulated company must retain proof of every configuration change AND every user action taken on their AWS resources for a future audit. Which TWO services together provide this? (Select TWO)",
     ["AWS Config (configuration history)", "CloudTrail (user/API activity history)", "AWS Health", "License Manager"],
     [0, 1],
     "AWS Config tracks what a resource's configuration looked like over time, while CloudTrail tracks who performed the actions that caused those changes — together giving a complete audit trail."),

    ("Scenario",
     "A startup with 40 AWS accounts across different teams wants fast, guardrail-based setup of a secure multi-account environment following AWS best practices, without manually configuring everything themselves. What should they use?",
     ["AWS Organizations alone, manually configured", "AWS Control Tower", "AWS Service Catalog", "Trusted Advisor"],
     1,
     "Control Tower automates the setup of a secure, compliant multi-account landing zone with guardrails, built on top of Organizations — ideal for fast, best-practice setup."),

    ("Scenario",
     "A finance company needs to prove to internal management which employees have access to sensitive S3 buckets from OUTSIDE the organization's AWS accounts. Which service directly answers this?",
     ["Trusted Advisor", "IAM Access Analyzer", "AWS Config", "AWS Health"],
     1,
     "IAM Access Analyzer is purpose-built to identify resources, such as S3 buckets, that are accessible from outside the account or organization."),

    ("Scenario",
     "Which service would BEST help a company understand if they are underutilizing purchased Reserved Instances, in addition to flagging open security groups and missing Multi-AZ setups?",
     ["Trusted Advisor", "AWS Artifact", "License Manager", "Service Catalog"],
     0,
     "Trusted Advisor's Cost Optimization, Security, and Fault Tolerance categories together cover unused RIs, open ports, and missing Multi-AZ/backup configurations."),

    ("Scenario",
     "EXAM TRAP: A question describes a company wanting 'proof that AWS data centers are ISO 27001 certified' for their own internal auditors. Which service should they use, and why is Audit Manager the WRONG choice here?",
     ["AWS Artifact — because it holds AWS's own third-party certification reports, whereas Audit Manager collects the CUSTOMER's own compliance evidence",
      "AWS Audit Manager — because it certifies AWS's data centers directly", "AWS Config — because it tracks physical data center configuration",
      "CloudTrail — because it logs AWS's internal API calls"],
     0,
     "This distinction is a classic trap: Artifact = AWS's own certifications/reports; Audit Manager = evidence about the CUSTOMER's workloads, not AWS's infrastructure."),

    ("Scenario",
     "A company onboarding many new AWS accounts wants developers to launch only pre-approved CloudFormation-based resource templates, while security teams retain centralized SCP-based guardrails across all accounts. Which TWO services are needed together? (Select TWO)",
     ["AWS Service Catalog (approved self-service resources)", "AWS Organizations (centralized SCP guardrails)",
      "AWS Health", "CloudWatch Logs Insights"],
     [0, 1],
     "Service Catalog handles curated, self-service resource deployment for developers, while Organizations provides the overarching multi-account SCP governance layer — these commonly work together."),
]

# ---------------------------------------------------------------------------
# QUIZ ENGINE (reusable across modules — do not modify structure)
# ---------------------------------------------------------------------------


def _normalize_correct(correct_answer):
    """Normalize correct_answer into a sorted tuple of ints, whether it was
    given as a single int or a list/tuple of ints (multi-select)."""
    if isinstance(correct_answer, (list, tuple, set)):
        return tuple(sorted(correct_answer))
    return (correct_answer,)


def _shuffle_question(topic, question_text, options, correct_answer, explanation):
    """Return a shuffled copy of a question: options shuffled, correct_answer
    indices remapped accordingly."""
    correct_indices = _normalize_correct(correct_answer)
    indexed_options = list(enumerate(options))
    random.shuffle(indexed_options)

    new_options = [opt for _, opt in indexed_options]
    old_to_new = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(indexed_options)}
    new_correct = tuple(sorted(old_to_new[i] for i in correct_indices))

    if len(new_correct) == 1:
        new_correct_final = new_correct[0]
    else:
        new_correct_final = new_correct

    return (topic, question_text, new_options, new_correct_final, explanation)


def build_shuffled_quiz():
    """Shuffle question order and each question's option order."""
    quiz = [
        _shuffle_question(topic, q_text, opts, correct, expl)
        for (topic, q_text, opts, correct, expl) in QUESTIONS
    ]
    random.shuffle(quiz)
    return quiz


def prompt_answer(options, is_multi):
    """Prompt the user for an answer and return a normalized tuple of 0-based
    indices representing their selection."""
    while True:
        raw = input("\nYour answer: ").strip()
        if not raw:
            print("Please enter an answer.")
            continue
        parts = [p.strip() for p in raw.replace(",", " ").split()]
        try:
            picks = sorted(set(int(p) - 1 for p in parts))
        except ValueError:
            print("Invalid input. Enter option number(s), e.g. '2' or '1 3'.")
            continue

        if any(p < 0 or p >= len(options) for p in picks):
            print(f"Please enter number(s) between 1 and {len(options)}.")
            continue

        if not is_multi and len(picks) != 1:
            print("This question expects a single answer.")
            continue

        if is_multi and len(picks) < 2:
            print("This question expects multiple (Select TWO/THREE) answers.")
            continue

        return tuple(picks)


def run_quiz():
    print("=" * 70)
    print(f"AWS CCP (CLF-C02) — MODULE 10: {MODULE_NAME}")
    print("EXAM MODE — Answers are recorded silently. No feedback until submission.")
    print("=" * 70)

    quiz = build_shuffled_quiz()
    total = len(quiz)
    print(f"\nTotal Questions: {total}\n")

    records = []  # list of dicts: topic, question, options, user_answer, correct_answer, explanation, is_multi

    for i, (topic, question_text, options, correct_answer, explanation) in enumerate(quiz, start=1):
        is_multi = isinstance(correct_answer, (list, tuple))
        print("-" * 70)
        print(f"Q{i}/{total}  [{topic}]")
        if is_multi:
            print(f"(Select {'TWO' if len(correct_answer) == 2 else 'THREE' if len(correct_answer) == 3 else len(correct_answer)}) {question_text}")
        else:
            print(question_text)
        for idx, opt in enumerate(options, start=1):
            print(f"  {idx}. {opt}")

        user_answer = prompt_answer(options, is_multi)
        print("Answer recorded.")

        records.append({
            "topic": topic,
            "question": question_text,
            "options": options,
            "user_answer": user_answer,
            "correct_answer": _normalize_correct(correct_answer),
            "explanation": explanation,
        })

    print_results(records)


def print_results(records):
    total = len(records)
    correct_count = sum(1 for r in records if r["user_answer"] == r["correct_answer"])
    pct = (correct_count / total) * 100 if total else 0

    topic_stats = defaultdict(lambda: [0, 0])  # topic -> [correct, total]
    for r in records:
        topic_stats[r["topic"]][1] += 1
        if r["user_answer"] == r["correct_answer"]:
            topic_stats[r["topic"]][0] += 1

    topic_pct = {
        topic: (c / t * 100 if t else 0)
        for topic, (c, t) in topic_stats.items()
    }
    weakest_first = sorted(topic_pct.items(), key=lambda x: x[1])

    lines = []
    lines.append("=" * 70)
    lines.append(f"AWS CCP (CLF-C02) — MODULE 10: {MODULE_NAME} — RESULTS")
    lines.append("=" * 70)
    lines.append(f"\nOverall Score: {correct_count}/{total} ({pct:.1f}%)\n")

    lines.append("Topic-Wise Breakdown (weakest first):")
    lines.append("-" * 70)
    for topic, p in weakest_first:
        c, t = topic_stats[topic]
        lines.append(f"  {topic:35s} {c}/{t}  ({p:.1f}%)")

    weak_topics = [topic for topic, p in weakest_first if p < 70]
    lines.append("\nWeak Topics (<70%):")
    lines.append("-" * 70)
    if weak_topics:
        for topic in weak_topics:
            c, t = topic_stats[topic]
            lines.append(f"  ⚠ {topic} — {c}/{t} ({topic_pct[topic]:.1f}%)")
    else:
        lines.append("  None — solid performance across all topics!")

    missed = [r for r in records if r["user_answer"] != r["correct_answer"]]
    lines.append(f"\nMissed Questions Review ({len(missed)} missed):")
    lines.append("=" * 70)
    if not missed:
        lines.append("  None — perfect score!")
    else:
        for i, r in enumerate(missed, start=1):
            chosen_str = ", ".join(r["options"][idx] for idx in r["user_answer"])
            correct_str = ", ".join(r["options"][idx] for idx in r["correct_answer"])
            lines.append(f"\n{i}. [{r['topic']}] {r['question']}")
            lines.append(f"   Your answer:     {chosen_str}")
            lines.append(f"   Correct answer:  {correct_str}")
            lines.append(f"   Explanation:     {r['explanation']}")

    lines.append("\n" + "=" * 70)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)

    report = "\n".join(lines)
    print("\n" + report)

    export_filename = f"{MODULE_NAME}-Results.txt"
    try:
        with open(export_filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n[Report exported to: {os.path.abspath(export_filename)}]")
    except OSError as e:
        print(f"\n[Could not export report: {e}]")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Exiting.")
        sys.exit(0)
