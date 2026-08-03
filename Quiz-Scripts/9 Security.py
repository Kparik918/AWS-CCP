#!/usr/bin/env python3
"""
====================================================================
 AWS CERTIFIED CLOUD PRACTITIONER (CLF-C02)
 MODULE 9 — SECURITY — PRACTICE MCQ QUIZ (EXAM MODE)
====================================================================

Covers:
    1. Shared Responsibility Model
    2. Authentication vs Authorization
    3. Access Control (Root User, IAM: Users, Groups, Policies, Roles,
       IAM Identity Center / SSO)
    4. Secrets & Node Management (Secrets Manager, Systems Manager)
    5. Network Attacks & Defense (DoS/DDoS, Security Groups, ELB,
       AWS Regions, AWS Shield, AWS WAF)
    6. Data Protection (Encryption at Rest/in Transit, KMS, Macie, ACM)
    7. Detect & Respond (Inspector, GuardDuty, Detective, Security Hub)

EXAM MODE BEHAVIOR:
    - No immediate correct/incorrect feedback during the quiz.
    - Each answer is simply "recorded".
    - Full results (score, topic breakdown, weak topics, missed
      questions review) are revealed only after the entire quiz is
      submitted, and auto-exported to a results .txt file.

Domain Weight Reminder: Security is the heaviest CLF-C02 domain (~30%).
====================================================================
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Module 9 - Security"

# ====================================================================
# QUESTIONS
# Format: (topic, question_text, [options], correct_answer, explanation)
#   correct_answer -> single 0-based int for single-select
#   correct_answer -> list/tuple of 0-based ints for multi-select
# ====================================================================

QUESTIONS = [
    # ---------------------------------------------------------------
    # 1. SHARED RESPONSIBILITY MODEL
    # ---------------------------------------------------------------
    ("Shared Responsibility Model",
     "Under the AWS Shared Responsibility Model, which of the following is ALWAYS the responsibility of AWS, regardless of the service used?",
     ["Configuring IAM permissions", "Physical security of data centers",
      "Patching the guest operating system on EC2", "Encrypting customer data client-side"],
     1,
     "AWS always owns 'security OF the cloud', which includes physical data center security, hardware, and global infrastructure — this never shifts to the customer."),

    ("Shared Responsibility Model",
     "A company's S3 bucket is left publicly accessible due to a misconfigured bucket policy, resulting in a data leak. Who is responsible for this incident under the Shared Responsibility Model?",
     ["AWS, because they own the S3 infrastructure", "The customer, because access control configuration is 'security IN the cloud'",
      "Both parties equally, split 50/50", "Neither — this is considered an unavoidable AWS Ffault"],
     1,
     "AWS provides the S3 service and its security controls, but configuring policies and permissions correctly is the customer's responsibility — this is a classic exam trap."),

    ("Shared Responsibility Model",
     "For Amazon EC2 (an unmanaged/IaaS-style service), which of the following is the CUSTOMER's responsibility?",
     ["The hypervisor and underlying hardware", "Guest OS patching and security group configuration",
      "Physical security of the facility", "Decommissioning of old physical disks"],
     1,
     "For EC2, AWS manages the hypervisor and hardware, while the customer manages the guest OS, patching, firewall (security group) rules, and application-level security."),

    ("Shared Responsibility Model",
     "Which statement best describes how the Shared Responsibility Model applies to managed services like Amazon RDS compared to unmanaged services like EC2?",
     ["Managed services shift more responsibility to AWS; unmanaged services shift more to the customer",
      "Managed and unmanaged services always carry identical customer responsibility",
      "Managed services always eliminate all customer responsibility entirely",
      "Unmanaged services are always more secure than managed services"],
     0,
     "With managed services (like RDS), AWS takes on more operational responsibility such as OS/engine patching, whereas unmanaged services (like EC2) leave more in the customer's hands."),

    # ---------------------------------------------------------------
    # 2. AUTHENTICATION vs AUTHORIZATION
    # ---------------------------------------------------------------
    ("Authentication vs Authorization",
     "Which term describes the process of verifying 'who you are' when accessing AWS?",
     ["Authorization", "Authentication", "Encryption", "Federation"],
     1,
     "Authentication answers 'who are you?' and happens at login, via mechanisms like passwords, access keys, or MFA."),

    ("Authentication vs Authorization",
     "A user successfully logs into the AWS Console with valid credentials but receives an 'Access Denied' error when trying to launch an EC2 instance. What does this best illustrate?",
     ["The user was never authenticated", "Authentication succeeded, but authorization failed due to insufficient permissions",
      "IAM is malfunctioning", "The Shared Responsibility Model was violated"],
     1,
     "This is a classic exam trap: successful login (authentication) does not guarantee permission to perform every action (authorization) — permissions are governed separately by IAM policies."),

    # ---------------------------------------------------------------
    # 3. ACCESS CONTROL — ROOT USER & IAM
    # ---------------------------------------------------------------
    ("Root User",
     "What is the recommended best practice regarding the AWS root user?",
     ["Use it for all daily administrative tasks", "Enable MFA immediately and reserve it only for emergency/account-level tasks",
      "Delete it as soon as the account is created", "Share its credentials with all team members for convenience"],
     1,
     "The root user has unrestricted access to everything including billing, so AWS recommends securing it with MFA and using an IAM admin user for day-to-day work instead."),

    ("Root User",
     "According to AWS best practices, what should be among the FIRST actions taken after creating a new AWS account?",
     ["Launch a production EC2 fleet", "Enable MFA on the root user and create an IAM admin user",
      "Delete the default VPC", "Purchase Reserved Instances"],
     1,
     "AWS exam questions frequently test this: the very first security steps are securing the root user with MFA and creating an IAM user/role for daily operations."),

    ("IAM",
     "What type of AWS service is IAM, in terms of scope and pricing?",
     ["Regional and paid per user", "Global and free", "Regional and free", "Global and paid per policy"],
     1,
     "IAM is a global service (not tied to a specific Region) and is free to use — a frequently tested fact on the CCP exam."),

    ("IAM",
     "By default, what level of access does a newly created IAM user have?",
     ["Full administrator access", "Read-only access to all services", "Zero permissions (implicit deny)", "Access equal to the root user"],
     2,
     "New IAM users start with zero permissions — everything is implicitly denied until an administrator explicitly grants access via a policy."),

    ("IAM Policies",
     "In an IAM policy, if one policy explicitly ALLOWS an action and another policy explicitly DENIES the same action for the same user, what is the result?",
     ["The Allow takes precedence", "The Deny takes precedence", "AWS averages the two into partial access", "The action is undefined and causes an error"],
     1,
     "An explicit Deny always overrides an Allow in IAM policy evaluation, no matter how many other policies grant access — this is a heavily tested trap."),

    ("IAM Policies",
     "Which of the following are core elements found in an IAM policy JSON document? (Select THREE)",
     ["Effect", "Action", "Resource", "Firewall", "Subnet"],
     [0, 1, 2],
     "IAM policy documents are built from elements such as Version, Effect (Allow/Deny), Action (the API call), and Resource (the ARN it applies to) — Firewall and Subnet are networking concepts, not IAM policy elements."),

    ("IAM Users",
     "An IAM User is best described as which of the following?",
     ["A temporary identity assumed by a trusted entity", "A single individual identity with long-term credentials",
      "A collection of permissions applied to multiple people", "A centralized SSO portal"],
     1,
     "An IAM User represents one specific individual and typically holds long-term credentials such as a console password or access keys."),

    ("IAM Groups",
     "What is the primary benefit of assigning IAM policies to IAM Groups rather than to individual IAM Users?",
     ["Groups provide stronger encryption than individual users", "Groups make managing permissions for many users at scale easier",
      "Groups automatically rotate credentials", "Groups bypass the need for authentication"],
     1,
     "Attaching a policy to a Group applies it to every member automatically, making permission management far easier at scale than managing each user individually."),

    ("IAM Roles",
     "A company wants an application running on an EC2 instance to access an S3 bucket WITHOUT hardcoding any AWS access keys in the application code. What should they use?",
     ["An IAM User with long-term access keys stored in the code", "An IAM Role attached to the EC2 instance",
      "The root user's credentials", "AWS Secrets Manager only, with no IAM involvement"],
     1,
     "IAM Roles provide temporary, automatically rotating credentials to trusted entities like EC2 instances, eliminating the security risk of hardcoded static access keys."),

    ("IAM Roles",
     "How do the credentials associated with an IAM Role differ from those of an IAM User?",
     ["Role credentials are temporary and auto-expiring; User credentials are typically long-term",
      "Role credentials never expire; User credentials always expire within 24 hours",
      "There is no difference — both use identical credential types",
      "Roles cannot be assumed by AWS services, only by humans"],
     0,
     "IAM Roles issue temporary, auto-rotating credentials for a limited session, while IAM Users typically have long-term credentials such as passwords or static access keys."),

    ("IAM Roles",
     "A company has 5,000 employees who already authenticate using Microsoft Active Directory. They want these employees to access AWS without creating 5,000 separate IAM users. What is this scenario an example of?",
     ["IAM Groups", "Federation using an IAM Role", "Root user delegation", "AWS Secrets Manager rotation"],
     1,
     "Federation maps existing corporate credentials (e.g., Active Directory) to an IAM Role, granting temporary AWS access without needing to create individual IAM users for every employee."),

    ("IAM Identity Center",
     "What is the primary purpose of AWS IAM Identity Center (formerly AWS SSO)?",
     ["Encrypting data across AWS accounts", "Providing single sign-on access across multiple AWS accounts and business applications",
      "Automatically rotating database passwords", "Scanning EC2 instances for vulnerabilities"],
     1,
     "IAM Identity Center allows users to log in once and gain access to multiple AWS accounts and applications without separate credentials for each."),

    ("IAM",
     "A company needs an application on EC2 to read/write to DynamoDB, and separately needs to manage permissions for 50 human employees who log into the console daily. Which combination best fits AWS best practices? (Select TWO)",
     ["Use an IAM Role for the EC2 application", "Hardcode long-term access keys into the EC2 application",
      "Organize the 50 employees into IAM Groups with appropriate policies", "Give all 50 employees root credentials"],
     [0, 2],
     "Best practice pairs IAM Roles for service-to-service access (like EC2 to DynamoDB) with IAM Groups for managing permissions of multiple human users efficiently."),

    # ---------------------------------------------------------------
    # 4. SECRETS & NODE MANAGEMENT
    # ---------------------------------------------------------------
    ("AWS Secrets Manager",
     "A company needs to store database credentials and have them automatically rotated on a scheduled basis. Which service should they use?",
     ["AWS Systems Manager Parameter Store", "AWS Secrets Manager", "AWS KMS", "Amazon Macie"],
     1,
     "AWS Secrets Manager is purpose-built to securely store secrets like database credentials and API keys, and natively supports automatic rotation."),

    ("AWS Secrets Manager",
     "A company only needs to store non-sensitive configuration values (not credentials) and wants to minimize cost. What is the more cost-effective choice compared to Secrets Manager?",
     ["AWS Systems Manager Parameter Store", "Amazon Macie", "AWS Shield Advanced", "AWS Certificate Manager"],
     0,
     "Systems Manager Parameter Store is a cheaper option for storing configuration data that doesn't require the automatic secret-rotation capabilities of Secrets Manager."),

    ("AWS Systems Manager",
     "A company has 500 EC2 instances spread across 3 Regions and needs to patch a critical vulnerability on all of them from a centralized location. Which service should they use?",
     ["AWS Secrets Manager", "AWS Systems Manager (Patch Manager)", "Amazon Inspector", "AWS Shield"],
     1,
     "AWS Systems Manager provides centralized visibility and automation — including Patch Manager — to manage nodes across accounts and Regions from one place."),

    ("Secrets & Node Management",
     "What is the key difference between AWS Secrets Manager and AWS Systems Manager?",
     ["Secrets Manager focuses on secure secret storage/rotation; Systems Manager focuses on centralized node management and automation",
      "They are two names for the exact same service", "Systems Manager only works with S3 buckets",
      "Secrets Manager is used exclusively for DDoS protection"],
     0,
     "Secrets Manager is specialized for secrets like credentials and API keys, while Systems Manager provides broader fleet-wide management, automation, and patching capabilities."),

    # ---------------------------------------------------------------
    # 5. NETWORK ATTACKS & DEFENSE
    # ---------------------------------------------------------------
    ("DoS / DDoS",
     "What is the key difference between a DoS attack and a DDoS attack?",
     ["DoS originates from a single source; DDoS originates from multiple distributed sources",
      "DoS is always more damaging than DDoS", "DDoS only targets databases, while DoS targets web servers",
      "There is no meaningful difference between the two"],
     0,
     "A DoS attack comes from a single attacking machine, while a DDoS attack is distributed across many compromised machines ('zombie bots'), making it larger scale and harder to block."),

    ("DoS / DDoS",
     "In a UDP flood attack, why does the target system experience resource exhaustion even though no real application-level connection is ever established?",
     ["Because UDP requires encryption keys to be generated for every packet",
      "Because the target must check each random port for a listening application and reply with ICMP 'destination unreachable' messages",
      "Because UDP packets are always larger than TCP packets",
      "Because UDP automatically triggers a full TCP handshake"],
     1,
     "UDP is connectionless, so the target wastes resources checking for a listening application on random ports and generating ICMP responses, even without a genuine connection ever being made."),

    ("Security Groups",
     "How do Security Groups contribute to defending against network attacks?",
     ["They encrypt all data at rest automatically", "They act as a stateful, instance-level firewall that only allows legitimate traffic",
      "They provide DDoS diagnostics and a response team", "They discover PII in S3 buckets"],
     1,
     "Security Groups operate at the instance level as stateful, allow-only firewalls, reducing the attack surface by only permitting explicitly approved traffic."),

    ("ELB",
     "How does an Elastic Load Balancer help defend against DDoS attacks?",
     ["It absorbs incoming traffic first, preventing backend EC2 instances from being directly overwhelmed",
      "It automatically deletes malicious IAM users", "It encrypts data using KMS keys",
      "It scans for vulnerabilities in EC2 AMIs"],
     0,
     "ELB sits in front of backend instances and absorbs traffic spikes at the Region level, shielding EC2 instances from being directly hit by an attack."),

    ("AWS Regions",
     "How does the scale of AWS Regions act as a defense layer against DDoS attacks?",
     ["Regions automatically block all inbound traffic", "The massive infrastructure capacity makes a meaningful attack prohibitively expensive to sustain",
      "Regions eliminate the need for Security Groups", "Regions provide free legal counsel during an attack"],
     1,
     "AWS Regions offer such large infrastructure capacity that an attacker would need an enormous and costly effort just to meaningfully disrupt service, making cost itself a deterrent."),

    ("AWS Shield",
     "Which tier of AWS Shield is automatically included for free with every AWS account?",
     ["Shield Advanced", "Shield Standard", "Shield Enterprise", "Shield Premium"],
     1,
     "Shield Standard is free and automatically enabled for all AWS customers, protecting against the most common and frequently occurring DDoS attacks."),

    ("AWS Shield",
     "A company wants detailed DDoS attack diagnostics, cost protection, and access to a 24/7 DDoS Response Team (DRT). Which service/tier should they choose?",
     ["Shield Standard", "Shield Advanced", "AWS WAF only", "Amazon Inspector"],
     1,
     "Shield Advanced is the paid tier that adds detailed diagnostics, cost protection, and access to the AWS DDoS Response Team, unlike the free Standard tier."),

    ("AWS Shield",
     "Which statement about AWS Shield pricing is a common exam trap to avoid falling for?",
     ["Assuming both Standard and Advanced tiers are free", "Assuming Shield only works with EC2",
      "Assuming Shield replaces the need for Security Groups", "Assuming Shield is a manual, non-automated service"],
     0,
     "A common mistake is assuming all of Shield is free — only Shield Standard is free and automatic, while Shield Advanced is a paid subscription with extra features."),

    ("AWS WAF",
     "A company needs to protect its web application against SQL injection and cross-site scripting (XSS) attacks. Which service should they use?",
     ["AWS Shield Standard", "AWS WAF", "AWS Systems Manager", "Amazon Macie"],
     1,
     "AWS WAF operates at the application layer (Layer 7) and can be configured with custom rules in a Web ACL to block attacks like SQL injection and XSS."),

    ("AWS WAF",
     "What term describes the rule set that AWS WAF uses to allow or block incoming requests?",
     ["Security Group", "Web ACL (Access Control List)", "Route Table", "Network ACL"],
     1,
     "AWS WAF filters requests based on rules defined in a Web ACL — this specific terminology is frequently tested on the CCP exam."),

    ("AWS WAF",
     "Which statement correctly distinguishes AWS WAF from AWS Shield?",
     ["WAF operates at the application layer (L7) with customizable rules; Shield focuses on network/transport-layer (L3/L4) DDoS protection",
      "WAF and Shield are identical services with different names",
      "Shield operates at the application layer while WAF handles network-layer DDoS",
      "WAF requires a paid subscription while Shield Standard and Advanced are both free"],
     0,
     "WAF is a customizable, rule-based application-layer firewall (HTTP/HTTPS), while Shield is purpose-built for network and transport-layer DDoS protection — they complement rather than replace each other."),

    ("Network Attacks & Defense",
     "A company wants a layered defense strategy against DDoS attacks. Which of the following are valid layers in that defense strategy? (Select THREE)",
     ["Security Groups", "AWS Shield", "AWS WAF", "Amazon Macie", "AWS Certificate Manager"],
     [0, 1, 2],
     "Security Groups, Shield, and WAF are all part of the network attack defense stack; Macie handles sensitive data discovery and ACM handles SSL/TLS certificates — unrelated to DDoS defense."),

    # ---------------------------------------------------------------
    # 6. DATA PROTECTION
    # ---------------------------------------------------------------
    ("Encryption at Rest/Transit",
     "Data sitting idle inside an S3 bucket, not currently being accessed or transferred, is an example of which type of protection state?",
     ["Encryption in transit", "Encryption at rest", "Federation", "Authorization"],
     1,
     "Encryption at rest protects data while it is idle and stored, such as objects sitting in an S3 bucket or a database."),

    ("Encryption at Rest/Transit",
     "Which AWS service(s) provide encryption at rest by default, automatically, without requiring the customer to manually enable it? (Select TWO)",
     ["Amazon S3", "Amazon EBS (default volumes)", "Amazon DynamoDB", "Amazon EC2 instance store"],
     [0, 2],
     "Amazon S3 and DynamoDB encrypt data at rest by default automatically, whereas EBS encryption is available but must generally be enabled rather than being automatic by default — a classic exam trap."),

    ("Encryption at Rest/Transit",
     "Data traveling from a database to an application over the network, secured using SSL/TLS, is an example of which type of protection?",
     ["Encryption at rest", "Encryption in transit", "IAM authorization", "Vulnerability scanning"],
     1,
     "Encryption in transit protects data while it is actively moving between systems, commonly secured via protocols like SSL/TLS."),

    ("AWS KMS",
     "What is the primary function of AWS Key Management Service (KMS)?",
     ["Storing and auto-rotating database passwords", "Creating, storing, and managing cryptographic keys used to encrypt/decrypt data",
      "Scanning S3 for exposed PII", "Filtering malicious HTTP requests"],
     1,
     "AWS KMS centralizes the creation, storage, and lifecycle management of cryptographic keys used across AWS services for encryption and decryption."),

    ("AWS KMS",
     "A common exam trap is confusing AWS KMS with which other service?",
     ["AWS Secrets Manager", "Amazon Macie", "AWS Certificate Manager", "AWS Shield"],
     0,
     "KMS manages encryption keys, while Secrets Manager manages secrets/credentials — they serve related but distinct purposes and are frequently confused on the exam."),

    ("Amazon Macie",
     "A healthcare company wants to ensure patient records (PII) are not accidentally exposed in a publicly accessible S3 bucket. Which service should they use?",
     ["Amazon Macie", "AWS Certificate Manager", "AWS Systems Manager", "Amazon Detective"],
     0,
     "Amazon Macie uses machine learning and automation to discover, monitor, and protect sensitive data such as PII stored specifically in Amazon S3."),

    ("Amazon Macie",
     "What is an important limitation to remember about Amazon Macie for the exam?",
     ["It only protects DynamoDB tables, not S3", "It is focused specifically on S3, not a general-purpose DLP tool across all AWS services",
      "It requires Shield Advanced to function", "It replaces the need for IAM policies entirely"],
     1,
     "Macie's sensitive data discovery capability is centered on Amazon S3, not a general data-loss-prevention solution spanning every AWS service."),

    ("AWS Certificate Manager",
     "A company wants to enable HTTPS on its Application Load Balancer using SSL/TLS certificates that AWS manages and renews automatically. Which service should they use?",
     ["AWS Certificate Manager (ACM)", "AWS KMS", "AWS Secrets Manager", "Amazon GuardDuty"],
     0,
     "AWS Certificate Manager provisions, manages, and automatically renews SSL/TLS certificates for use with services like ALB, CloudFront, and API Gateway."),

    ("AWS Certificate Manager",
     "What is a key limitation of AWS Certificate Manager (ACM)?",
     ["It manages SSL/TLS certificates for encryption in transit, but does NOT perform encryption at rest",
      "It only works with on-premises servers", "It cannot renew certificates automatically",
      "It replaces AWS KMS entirely"],
     0,
     "ACM is scoped to certificate management for encryption in transit (HTTPS); it does not handle encryption at rest, which is the domain of services like KMS."),

    ("Data Protection",
     "Which service would be most appropriate for each need: (1) managing SSL/TLS certificates, (2) managing encryption keys, (3) discovering PII in S3? Match correctly.",
     ["ACM / KMS / Macie", "KMS / Macie / ACM", "Macie / ACM / KMS", "Secrets Manager / ACM / KMS"],
     0,
     "ACM manages SSL/TLS certificates for transit encryption, KMS manages cryptographic keys, and Macie discovers sensitive data like PII in S3 — mapping these correctly is a common scenario-based exam question."),

    # ---------------------------------------------------------------
    # 7. DETECT & RESPOND
    # ---------------------------------------------------------------
    ("Amazon Inspector",
     "A company wants to run automated vulnerability assessments against its EC2 fleet to check for exposed instances and vulnerable software versions. Which service should they use?",
     ["Amazon Inspector", "Amazon GuardDuty", "Amazon Detective", "AWS Security Hub"],
     0,
     "Amazon Inspector performs automated, proactive vulnerability assessments, with a heavy focus on EC2, flagging vulnerable software and deviations from best practices."),

    ("Amazon GuardDuty",
     "Which service continuously monitors network activity and data streams for intelligent, ongoing threat detection?",
     ["Amazon Inspector", "Amazon GuardDuty", "AWS Certificate Manager", "AWS Systems Manager"],
     1,
     "Amazon GuardDuty provides continuous, intelligent threat detection by monitoring network activity and data streams in near real time, much like a 24/7 CCTV camera."),

    ("Amazon Detective",
     "After Amazon GuardDuty flags a suspicious finding, which service is used to investigate and visualize logs to determine the root cause?",
     ["Amazon Detective", "Amazon Inspector", "AWS WAF", "AWS Shield"],
     0,
     "Amazon Detective is used AFTER a threat is detected to analyze and visualize logs, helping investigators determine the root cause of a security finding."),

    ("AWS Security Hub",
     "A company wants a single dashboard that aggregates security findings from multiple AWS security services. Which service should they use?",
     ["AWS Security Hub", "Amazon Macie", "AWS Systems Manager", "AWS Certificate Manager"],
     0,
     "AWS Security Hub aggregates findings from services like GuardDuty, Inspector, and Macie into one comprehensive dashboard — it is not itself a detection engine."),

    ("Detect & Respond",
     "What is the correct logical order of operations across the Detect & Respond services, from proactive scanning to final aggregation?",
     ["GuardDuty → Detective → Inspector → Security Hub",
      "Inspector → GuardDuty → Detective → Security Hub",
      "Security Hub → Inspector → GuardDuty → Detective",
      "Detective → Inspector → Security Hub → GuardDuty"],
     1,
     "The typical sequence is: Inspector proactively scans for vulnerabilities, GuardDuty continuously detects active threats, Detective investigates the root cause after detection, and Security Hub aggregates all findings into one dashboard."),

    ("Detect & Respond",
     "Which of the following is a common exam trap regarding Amazon Inspector and Amazon GuardDuty?",
     ["Assuming both services are identical and interchangeable", "Confusing Inspector's proactive vulnerability scanning with GuardDuty's continuous, reactive threat monitoring",
      "Assuming Inspector only works on S3 buckets", "Assuming GuardDuty requires manual daily activation"],
     1,
     "A very common exam trap is mixing up Inspector (proactive vulnerability scanning, EC2-focused) with GuardDuty (continuous, ongoing threat detection) — they serve different phases of security operations."),

    ("Detect & Respond",
     "A company wants to know: 'Is there malware or suspicious activity happening on my network RIGHT NOW?' Which service best answers this?",
     ["Amazon Inspector", "Amazon GuardDuty", "AWS Certificate Manager", "AWS Secrets Manager"],
     1,
     "GuardDuty is designed for continuous, ongoing monitoring to detect active threats as they happen, unlike Inspector which performs periodic vulnerability scans."),

    ("Detect & Respond",
     "Which THREE of the following are part of AWS's 'Detect & Respond' security service category?",
     ["Amazon Inspector", "Amazon GuardDuty", "AWS Security Hub", "AWS Certificate Manager", "AWS Secrets Manager"],
     [0, 1, 2],
     "Inspector, GuardDuty, and Security Hub (along with Detective) form the Detect & Respond category; ACM and Secrets Manager belong to certificate management and secrets management respectively."),

    # ---------------------------------------------------------------
    # MIXED / SCENARIO / CROSS-TOPIC
    # ---------------------------------------------------------------
    ("Scenario",
     "A startup wants free, automatic protection against the most common DDoS attacks without paying for a subscription. What should they rely on?",
     ["AWS Shield Advanced", "AWS Shield Standard", "AWS WAF with a custom Web ACL", "Amazon GuardDuty"],
     1,
     "Shield Standard is free and automatically enabled for every AWS account, covering the most common and frequently occurring DDoS attacks at no extra cost."),

    ("Scenario",
     "A finance company must ensure database credentials used by their application are never hardcoded and are rotated automatically every 30 days. Which service directly satisfies this requirement?",
     ["AWS Systems Manager Parameter Store", "AWS Secrets Manager", "AWS Certificate Manager", "AWS KMS"],
     1,
     "AWS Secrets Manager is specifically designed to securely store secrets and supports automatic, scheduled rotation, unlike Parameter Store which lacks native secret rotation."),

    ("Scenario",
     "A company wants to verify that no IAM policy anywhere in their account accidentally grants public access to a sensitive S3 bucket containing an explicit Deny rule set by security. What key IAM behavior guarantees the Deny rule wins even if other policies allow access?",
     ["Least privilege scoring", "Explicit Deny always overrides any Allow", "IAM Roles override IAM Policies",
      "Federation takes precedence over local policies"],
     1,
     "IAM's policy evaluation logic guarantees that an explicit Deny statement always overrides any Allow statement, regardless of how many other policies grant access — a critical exam trap to remember."),

    ("Scenario",
     "A company needs to differentiate between who logged into the AWS Console (identity verification) and what that person is permitted to do once inside. Which two concepts describe this distinction?",
     ["Encryption and decryption", "Authentication and Authorization", "Federation and Delegation", "Detection and Response"],
     1,
     "Authentication verifies identity ('who are you'), while authorization determines permitted actions ('what can you do') — two distinct steps in the access control process."),

    ("Scenario",
     "An e-commerce company's checkout page is being hit by thousands of infected IoT devices worldwide sending simultaneous login requests, exhausting server resources. Which AWS service(s) directly address this threat? (Select TWO)",
     ["AWS Shield", "AWS WAF", "Amazon Macie", "AWS Certificate Manager"],
     [0, 1],
     "This scenario describes a DDoS attack; AWS Shield defends at the network/transport layer while AWS WAF can add application-layer rules to block malicious request patterns — Macie and ACM are unrelated to this threat type."),
]

# ====================================================================
# QUIZ ENGINE (reusable across modules — do not modify per-module)
# ====================================================================


def _normalize_correct(correct_answer):
    """Return correct answer(s) as a sorted list of ints, regardless of
    whether the source was a single int or a list/tuple of ints."""
    if isinstance(correct_answer, (list, tuple, set)):
        return sorted(correct_answer)
    return [correct_answer]


def _shuffle_question(topic, question_text, options, correct_answer, explanation):
    """Shuffle the order of options for a single question, remapping the
    correct answer index/indices accordingly."""
    correct_indices = _normalize_correct(correct_answer)
    indexed_options = list(enumerate(options))
    random.shuffle(indexed_options)

    new_options = [opt for _, opt in indexed_options]
    old_to_new = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(indexed_options)}
    new_correct = sorted(old_to_new[old_idx] for old_idx in correct_indices)

    if not isinstance(correct_answer, (list, tuple, set)):
        new_correct = new_correct[0]

    return topic, question_text, new_options, new_correct, explanation


def run_quiz():
    print("=" * 70)
    print(f" AWS CCP (CLF-C02) PRACTICE QUIZ — {MODULE_NAME.upper()}")
    print(" EXAM MODE: No feedback shown until the quiz is fully submitted.")
    print("=" * 70)
    print(f"\nTotal Questions: {len(QUESTIONS)}\n")
    input("Press ENTER to begin...\n")

    quiz_questions = list(QUESTIONS)
    random.shuffle(quiz_questions)

    results = []  # list of dicts: topic, question, options, selected, correct, explanation

    for q_num, (topic, question_text, options, correct_answer, explanation) in enumerate(quiz_questions, start=1):
        topic, question_text, options, correct_answer, explanation = _shuffle_question(
            topic, question_text, options, correct_answer, explanation
        )

        is_multi = isinstance(correct_answer, (list, tuple, set))
        correct_list = _normalize_correct(correct_answer)

        print("-" * 70)
        print(f"Question {q_num}/{len(quiz_questions)}  [{topic}]")
        if is_multi:
            print(f"(Select {len(correct_list)}) {question_text}")
        else:
            print(question_text)
        print()
        for i, opt in enumerate(options):
            letter = chr(65 + i)
            print(f"   {letter}. {opt}")
        print()

        if is_multi:
            raw = input(f"Enter {len(correct_list)} letters separated by commas (e.g. A,C): ").strip().upper()
            selected_letters = [x.strip() for x in raw.split(",") if x.strip()]
            selected_indices = sorted({ord(l) - 65 for l in selected_letters if l.isalpha() and 0 <= ord(l) - 65 < len(options)})
        else:
            raw = input("Enter your answer letter: ").strip().upper()
            selected_indices = ord(raw) - 65 if raw.isalpha() and 0 <= ord(raw) - 65 < len(options) else -1

        print(">> Answer recorded.\n")

        results.append({
            "topic": topic,
            "question": question_text,
            "options": options,
            "selected": selected_indices,
            "correct": correct_answer,
            "is_multi": is_multi,
            "explanation": explanation,
        })

    print_results(results)


def _format_selected(selected, options, is_multi):
    if is_multi:
        if not selected:
            return "(no answer)"
        return ", ".join(f"{chr(65+i)}. {options[i]}" for i in selected)
    else:
        if selected == -1:
            return "(no answer)"
        return f"{chr(65+selected)}. {options[selected]}"


def _format_correct(correct, options, is_multi):
    correct_list = _normalize_correct(correct)
    return ", ".join(f"{chr(65+i)}. {options[i]}" for i in correct_list)


def print_results(results):
    total = len(results)
    correct_count = 0
    topic_stats = defaultdict(lambda: [0, 0])  # topic -> [correct, total]
    missed = []

    for r in results:
        correct_list = _normalize_correct(r["correct"])
        if r["is_multi"]:
            is_correct = sorted(r["selected"]) == sorted(correct_list)
        else:
            is_correct = r["selected"] == correct_list[0]

        topic_stats[r["topic"]][1] += 1
        if is_correct:
            correct_count += 1
            topic_stats[r["topic"]][0] += 1
        else:
            missed.append(r)

    percentage = (correct_count / total * 100) if total else 0

    lines = []
    lines.append("=" * 70)
    lines.append(f" QUIZ RESULTS — {MODULE_NAME.upper()}")
    lines.append("=" * 70)
    lines.append(f"\nOverall Score: {correct_count}/{total} ({percentage:.1f}%)\n")

    lines.append("-" * 70)
    lines.append("TOPIC-WISE BREAKDOWN (weakest first)")
    lines.append("-" * 70)
    topic_percentages = []
    for topic, (c, t) in topic_stats.items():
        pct = (c / t * 100) if t else 0
        topic_percentages.append((topic, c, t, pct))
    topic_percentages.sort(key=lambda x: x[3])

    for topic, c, t, pct in topic_percentages:
        lines.append(f"  {topic:<35} {c}/{t}  ({pct:.1f}%)")

    weak_topics = [tp for tp in topic_percentages if tp[3] < 70]
    lines.append("")
    lines.append("-" * 70)
    lines.append("WEAK TOPICS (< 70% correct) — REVISE THESE FIRST")
    lines.append("-" * 70)
    if weak_topics:
        for topic, c, t, pct in weak_topics:
            lines.append(f"  ⚠ {topic} — {pct:.1f}%")
    else:
        lines.append("  None! All topics scored 70% or above. Great work.")

    lines.append("")
    lines.append("-" * 70)
    lines.append("MISSED QUESTIONS REVIEW")
    lines.append("-" * 70)
    if missed:
        for i, r in enumerate(missed, start=1):
            lines.append(f"\n{i}. [{r['topic']}] {r['question']}")
            lines.append(f"   Your answer:    {_format_selected(r['selected'], r['options'], r['is_multi'])}")
            lines.append(f"   Correct answer: {_format_correct(r['correct'], r['options'], r['is_multi'])}")
            lines.append(f"   Why: {r['explanation']}")
    else:
        lines.append("  No missed questions — perfect score!")

    lines.append("\n" + "=" * 70)
    lines.append(f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)

    report = "\n".join(lines)
    print("\n" + report)

    export_filename = f"{MODULE_NAME.replace(' ', '_')}-Results.txt"
    try:
        with open(export_filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📄 Results exported to: {os.path.abspath(export_filename)}")
    except OSError as e:
        print(f"\n⚠ Could not export results file: {e}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted by user. Exiting.")
        sys.exit(0)
