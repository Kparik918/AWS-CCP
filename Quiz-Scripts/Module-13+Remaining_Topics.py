#!/usr/bin/env python3
"""
AWS CCP (CLF-C02) — Combined Practice Quiz
Module 13 (Well-Architected + Dev Tools + Business Apps + EUC + IoT Core)
  + Remaining Services Bible (28 previously unchecked services)

Engine features:
- Shuffled answer options every run
- Multi-select support (questions requiring 2+ correct answers)
- Per-section weak-spot tracking
- Auto-incrementing result log (results_log.txt)
"""

import random
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# QUESTION BANK
# Each question: dict with keys:
#   q        -> question text
#   options  -> list of option strings
#   answer   -> list of correct option strings (len 1 = single select, len>1 = multi)
#   section  -> topic tag for weak-spot tracking
#   explain  -> short explanation shown after answering
# ---------------------------------------------------------------------------

QUESTIONS = [
    # ---------------- Well-Architected Framework ----------------
    {
        "q": "A company wants to evaluate its architecture against AWS best practices for free, using the AWS Console. Which service?",
        "options": ["AWS Trusted Advisor", "AWS Well-Architected Tool", "AWS Config", "Amazon Inspector"],
        "answer": ["AWS Well-Architected Tool"],
        "section": "Well-Architected Framework",
        "explain": "Well-Architected Tool is the free, self-service console tool that reviews workloads against the 6 pillars and gives an improvement report.",
    },
    {
        "q": "How many pillars does the current AWS Well-Architected Framework (CLF-C02) have?",
        "options": ["4", "5", "6", "7"],
        "answer": ["6"],
        "section": "Well-Architected Framework",
        "explain": "6 pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability (newest pillar).",
    },
    {
        "q": "Which pillar of the Well-Architected Framework specifically addresses minimizing environmental impact?",
        "options": ["Cost Optimization", "Performance Efficiency", "Sustainability", "Reliability"],
        "answer": ["Sustainability"],
        "section": "Well-Architected Framework",
        "explain": "Sustainability is the 6th (newest) pillar, focused on reducing energy/carbon footprint, e.g. preferring Lambda over always-on EC2 for spiky workloads.",
    },
    {
        "q": "True or False: The AWS Well-Architected Tool automatically fixes architecture issues it finds.",
        "options": ["True", "False"],
        "answer": ["False"],
        "section": "Well-Architected Framework",
        "explain": "The tool only gives recommendations — you still have to implement the fixes yourself.",
    },
    {
        "q": "What does the AWS Well-Architected Tool support for industry-specific reviews?",
        "options": ["Custom Lenses", "Custom Regions", "Custom IAM Roles", "Custom VPCs"],
        "answer": ["Custom Lenses"],
        "section": "Well-Architected Framework",
        "explain": "Custom lenses (e.g. IoT Lens, Serverless Lens, SaaS Lens) provide tailored question sets for specific workload types.",
    },

    # ---------------- Dev / Automation Tools ----------------
    {
        "q": "Which service compiles source code, runs tests, and produces deployable packages?",
        "options": ["AWS CodePipeline", "AWS CodeBuild", "AWS CodeDeploy", "AWS X-Ray"],
        "answer": ["AWS CodeBuild"],
        "section": "Dev Tools",
        "explain": "CodeBuild is the managed build/compile/test service — one stage of the CI/CD pipeline.",
    },
    {
        "q": "A company wants to automate its entire build-test-deploy release process end to end. Which service?",
        "options": ["AWS CodeBuild", "AWS CodeCommit", "AWS CodePipeline", "AWS CodeArtifact"],
        "answer": ["AWS CodePipeline"],
        "section": "Dev Tools",
        "explain": "CodePipeline is the orchestrator that ties CodeCommit → CodeBuild → CodeDeploy together into one automated release workflow.",
    },
    {
        "q": "A microservices app has intermittent slow responses and the team needs to find which service is the bottleneck. Which service helps?",
        "options": ["Amazon CloudWatch", "AWS X-Ray", "AWS Config", "AWS CloudTrail"],
        "answer": ["AWS X-Ray"],
        "section": "Dev Tools",
        "explain": "X-Ray traces a request end-to-end across microservices, pinpointing where delays/errors occur — unlike CloudWatch, which does metrics/logs, not request-path tracing.",
    },
    {
        "q": "Which statement about CodePipeline is TRUE?",
        "options": [
            "CodePipeline compiles code itself",
            "CodePipeline is the orchestration layer; it calls CodeBuild/CodeDeploy to do the actual work",
            "CodePipeline replaces the need for CodeCommit",
            "CodePipeline is only for Lambda deployments",
        ],
        "answer": ["CodePipeline is the orchestration layer; it calls CodeBuild/CodeDeploy to do the actual work"],
        "section": "Dev Tools",
        "explain": "CodePipeline does not build code itself — it's the conveyor belt that calls other tools at each stage.",
    },
    {
        "q": "Which service provides a managed, browser-based IDE for writing, running, and debugging code?",
        "options": ["AWS CloudShell", "AWS Cloud9", "AWS CodeStar", "AWS AppConfig"],
        "answer": ["AWS Cloud9"],
        "section": "Dev Tools",
        "explain": "Cloud9 is a full cloud-based IDE. CloudShell is just a quick pre-authenticated terminal, not a full dev environment.",
    },
    {
        "q": "Which service gives you a quick, pre-authenticated browser-based shell directly from the AWS Console with no setup?",
        "options": ["AWS Cloud9", "AWS CloudShell", "AWS CLI", "AWS CodeArtifact"],
        "answer": ["AWS CloudShell"],
        "section": "Dev Tools",
        "explain": "CloudShell = quick terminal, pre-installed AWS CLI, accessible right from the console. Cloud9 is a full IDE, which is heavier.",
    },
    {
        "q": "A team needs to securely store and share npm/pip/Maven package dependencies for their build pipeline. Which service?",
        "options": ["AWS CodeArtifact", "AWS CodeCommit", "Amazon ECR", "AWS CodeStar"],
        "answer": ["AWS CodeArtifact"],
        "section": "Dev Tools",
        "explain": "CodeArtifact is the managed artifact/package repository — CodeCommit is for source code (Git), not packages.",
    },
    {
        "q": "Which service lets you deploy and manage application feature flags with gradual rollout and automatic rollback on error, without redeploying code?",
        "options": ["AWS AppConfig", "AWS CodeDeploy", "AWS Systems Manager", "AWS CloudFormation"],
        "answer": ["AWS AppConfig"],
        "section": "Dev Tools",
        "explain": "AppConfig manages application configuration and feature flags with controlled, safe rollout.",
    },
    {
        "q": "Which service automates code deployments to EC2, Lambda, and ECS, supporting blue/green deployments?",
        "options": ["AWS CodeBuild", "AWS CodeDeploy", "AWS CodePipeline", "AWS CodeCommit"],
        "answer": ["AWS CodeDeploy"],
        "section": "Dev Tools",
        "explain": "CodeDeploy is the deploy stage of the CI/CD pipeline, supporting rolling and blue/green deployment strategies.",
    },
    {
        "q": "Which service provides a single unified dashboard to manage CodeCommit + CodeBuild + CodeDeploy + CodePipeline together, with quick project templates?",
        "options": ["AWS CodeStar", "AWS Systems Manager", "AWS Launch Wizard", "AWS Service Catalog"],
        "answer": ["AWS CodeStar"],
        "section": "Dev Tools",
        "explain": "CodeStar is the unified project dashboard tying together the whole dev-tools suite.",
    },

    # ---------------- App Dev / Business Apps ----------------
    {
        "q": "Which service lets a client fetch data from multiple backend sources (DynamoDB, Lambda, RDS) in a single GraphQL query?",
        "options": ["Amazon API Gateway", "AWS AppSync", "AWS Amplify", "Amazon EventBridge"],
        "answer": ["AWS AppSync"],
        "section": "App Dev / Business Apps",
        "explain": "AppSync = managed GraphQL API service, combining multiple data sources into one query. API Gateway is typically REST-style.",
    },
    {
        "q": "A startup wants to quickly build and deploy a full-stack web/mobile app with integrated frontend hosting, backend auth/APIs/storage, and CI/CD. Which service?",
        "options": ["AWS Amplify", "AWS AppSync", "AWS Elastic Beanstalk", "AWS CodeStar"],
        "answer": ["AWS Amplify"],
        "section": "App Dev / Business Apps",
        "explain": "Amplify is the full-stack app dev + deploy + hosting toolkit, ideal for fast startup development.",
    },
    {
        "q": "A company needs a cloud-based customer support call/chat center without physical infrastructure. Which service?",
        "options": ["Amazon SES", "Amazon Connect", "Amazon Pinpoint", "AWS IoT Core"],
        "answer": ["Amazon Connect"],
        "section": "App Dev / Business Apps",
        "explain": "Amazon Connect provides your business's customers a cloud contact center (voice + chat) to reach you.",
    },
    {
        "q": "A company needs to send millions of order-confirmation and OTP emails reliably. Which service?",
        "options": ["Amazon Connect", "Amazon SES", "AWS AppSync", "Amazon SNS"],
        "answer": ["Amazon SES"],
        "section": "App Dev / Business Apps",
        "explain": "SES handles bulk transactional/marketing email at scale. Connect is for voice/chat, not email.",
    },

    # ---------------- End-User Computing ----------------
    {
        "q": "Employees need a full persistent virtual desktop (own OS, apps, files) accessible remotely. Which service?",
        "options": ["Amazon AppStream 2.0", "Amazon WorkSpaces", "WorkSpaces Secure Browser", "AWS Cloud9"],
        "answer": ["Amazon WorkSpaces"],
        "section": "End-User Computing",
        "explain": "WorkSpaces = full persistent VDI (Virtual Desktop Infrastructure), like a company laptop in the cloud.",
    },
    {
        "q": "Contractors need temporary access to ONE specific licensed application (e.g. CAD software), with no install and no full desktop. Which service?",
        "options": ["Amazon WorkSpaces", "Amazon AppStream 2.0", "WorkSpaces Secure Browser", "AWS AppConfig"],
        "answer": ["Amazon AppStream 2.0"],
        "section": "End-User Computing",
        "explain": "AppStream 2.0 streams a single application — like Netflix, but for software — without a full desktop OS.",
    },
    {
        "q": "Users only need to access a few internal SaaS/web apps, nothing else — no full desktop, no installed apps. Which service is most restrictive and fits best?",
        "options": ["Amazon WorkSpaces", "Amazon AppStream 2.0", "Amazon WorkSpaces Secure Browser", "AWS IoT Core"],
        "answer": ["Amazon WorkSpaces Secure Browser"],
        "section": "End-User Computing",
        "explain": "Secure Browser gives only a locked-down secure browser session — the most restrictive of the 3 EUC options.",
    },
    {
        "q": "Which EUC service is typically NON-persistent, unlike Amazon WorkSpaces?",
        "options": ["Amazon WorkSpaces", "Amazon AppStream 2.0", "Both are persistent", "Neither is persistent"],
        "answer": ["Amazon AppStream 2.0"],
        "section": "End-User Computing",
        "explain": "WorkSpaces = persistent (saved desktop state). AppStream 2.0 = typically non-persistent (streamed app session).",
    },

    # ---------------- IoT ----------------
    {
        "q": "A factory wants to connect thousands of sensors securely to the cloud for real-time data. Which service?",
        "options": ["AWS IoT Greengrass", "AWS IoT Core", "Amazon Kinesis", "AWS Snow Family"],
        "answer": ["AWS IoT Core"],
        "section": "IoT",
        "explain": "IoT Core is the managed cloud connectivity/device-management layer for IoT devices.",
    },
    {
        "q": "Which IoT service allows devices to run local compute/ML inference at the edge, even when disconnected from the cloud?",
        "options": ["AWS IoT Core", "AWS IoT Greengrass", "AWS Snowball Edge", "Amazon Kinesis"],
        "answer": ["AWS IoT Greengrass"],
        "section": "IoT",
        "explain": "Greengrass extends IoT Core to the edge — devices keep working offline and sync once reconnected.",
    },

    # ---------------- Remaining Services: Cloud Financial Mgmt ----------------
    {
        "q": "An AWS Partner wants to create custom 'pro forma' bills to resell AWS services to their own clients at a markup. Which service?",
        "options": ["AWS Cost Explorer", "AWS Budgets", "AWS Billing Conductor", "AWS Cost and Usage Report"],
        "answer": ["AWS Billing Conductor"],
        "section": "Remaining Services",
        "explain": "Billing Conductor is built for custom billing groups / resale / chargeback scenarios, unlike Cost Explorer or Budgets which are for your own cost analysis.",
    },

    # ---------------- Remaining Services: Customer Engagement ----------------
    {
        "q": "A startup founder wants AWS credits and technical support/training resources. Which program?",
        "options": ["AWS IQ", "AWS Activate for Startups", "AWS Managed Services", "AWS Support"],
        "answer": ["AWS Activate for Startups"],
        "section": "Remaining Services",
        "explain": "AWS Activate for Startups gives startups AWS credits plus training and technical resources.",
    },
    {
        "q": "A company needs a certified AWS expert for a one-off consulting project, billed via AWS invoice. Which service?",
        "options": ["AWS Managed Services (AMS)", "AWS IQ", "AWS Support Enterprise", "AWS Activate"],
        "answer": ["AWS IQ"],
        "section": "Remaining Services",
        "explain": "AWS IQ is a marketplace for hiring AWS-certified independent experts for short-term project work.",
    },
    {
        "q": "A company has no in-house ops team and wants AWS to directly operate/manage its AWS infrastructure on an ongoing basis. Which service?",
        "options": ["AWS IQ", "AWS Managed Services (AMS)", "AWS Activate", "AWS Trusted Advisor"],
        "answer": ["AWS Managed Services (AMS)"],
        "section": "Remaining Services",
        "explain": "AMS = AWS itself acts as the managed service provider, running ongoing infrastructure operations for you.",
    },
    {
        "q": "Which AWS Support plan tier is the FIRST to include 24/7 phone/chat/email support and full Trusted Advisor checks?",
        "options": ["Basic", "Developer", "Business", "Enterprise On-Ramp"],
        "answer": ["Business"],
        "section": "Remaining Services",
        "explain": "24/7 support and full Trusted Advisor checks start from the Business plan onward.",
    },
    {
        "q": "Which AWS Support plan is required to get a DEDICATED Technical Account Manager (TAM)?",
        "options": ["Business", "Enterprise On-Ramp", "Enterprise", "Developer"],
        "answer": ["Enterprise"],
        "section": "Remaining Services",
        "explain": "A fully dedicated TAM is Enterprise-only. Enterprise On-Ramp gets a pool of TAMs, not a dedicated one.",
    },
    {
        "q": "What is the primary purpose of the AWS Concierge support team (Enterprise / Enterprise On-Ramp plans)?",
        "options": [
            "Deep technical architecture reviews",
            "Billing, account, and administrative queries",
            "24/7 infrastructure monitoring",
            "Writing application code for customers",
        ],
        "answer": ["Billing, account, and administrative queries"],
        "section": "Remaining Services",
        "explain": "Concierge handles billing/account/admin queries so the TAM's time stays focused on technical/architecture issues.",
    },

    # ---------------- Remaining Services: Database ----------------
    {
        "q": "A company needs a Redis-compatible in-memory database that can also serve as a DURABLE primary database (not just a cache). Which service?",
        "options": ["Amazon ElastiCache", "Amazon MemoryDB for Redis", "Amazon DynamoDB Accelerator (DAX)", "Amazon Aurora"],
        "answer": ["Amazon MemoryDB for Redis"],
        "section": "Remaining Services",
        "explain": "MemoryDB is durable (multi-AZ transaction log) and can be a primary database, unlike ElastiCache which is a non-durable caching layer.",
    },

    # ---------------- Remaining Services: Frontend/Mobile & IoT ----------------
    {
        "q": "A mobile dev team wants to test their app on real physical Android/iOS devices in the cloud, without buying the devices. Which service?",
        "options": ["AWS Amplify", "AWS Device Farm", "AWS AppSync", "Amazon AppStream 2.0"],
        "answer": ["AWS Device Farm"],
        "section": "Remaining Services",
        "explain": "Device Farm provides real physical devices/browsers in the cloud for app testing.",
    },

    # ---------------- Remaining Services: Management & Governance ----------------
    {
        "q": "A company needs to deploy a complex third-party app like SAP on AWS with guided, best-practice sizing and configuration. Which service?",
        "options": ["AWS CloudFormation", "AWS Launch Wizard", "AWS Service Catalog", "AWS Control Tower"],
        "answer": ["AWS Launch Wizard"],
        "section": "Remaining Services",
        "explain": "Launch Wizard guides deployment/sizing of complex third-party workloads like SAP, SQL Server, Active Directory.",
    },
    {
        "q": "A team wants to find and bulk-manage AWS resources across services based on tags. Which tool?",
        "options": ["AWS Config", "AWS Resource Groups and Tag Editor", "AWS Systems Manager", "AWS Trusted Advisor"],
        "answer": ["AWS Resource Groups and Tag Editor"],
        "section": "Remaining Services",
        "explain": "Resource Groups and Tag Editor let you organize, find, and bulk-tag resources across services.",
    },

    # ---------------- Remaining Services: Security ----------------
    {
        "q": "A finance company needs dedicated, single-tenant hardware for cryptographic key storage to meet strict compliance (FIPS 140-2 Level 3). Which service?",
        "options": ["AWS KMS", "AWS CloudHSM", "AWS Secrets Manager", "AWS Certificate Manager"],
        "answer": ["AWS CloudHSM"],
        "section": "Remaining Services",
        "explain": "CloudHSM = dedicated single-tenant hardware with full customer control. KMS is multi-tenant/managed, easier but less control.",
    },
    {
        "q": "A mobile app needs to let its own END-USERS sign up and sign in (including social login via Google/Facebook). Which service?",
        "options": ["AWS IAM", "Amazon Cognito", "AWS Directory Service", "AWS IAM Identity Center"],
        "answer": ["Amazon Cognito"],
        "section": "Remaining Services",
        "explain": "Cognito handles authentication for external app end-users. IAM is for internal AWS resource access control (employees/services), not app customers.",
    },
    {
        "q": "A company already runs on-premises Microsoft Active Directory and wants to integrate/connect it with AWS resources. Which service?",
        "options": ["Amazon Cognito", "AWS Directory Service", "AWS IAM Identity Center", "AWS Organizations"],
        "answer": ["AWS Directory Service"],
        "section": "Remaining Services",
        "explain": "Directory Service (via AD Connector) integrates existing on-prem AD with AWS, or provides managed Microsoft AD / Simple AD.",
    },
    {
        "q": "A company with many AWS accounts wants to centrally enforce WAF rules and Shield protections across the entire organization from one place. Which service?",
        "options": ["AWS WAF", "AWS Firewall Manager", "AWS Shield Advanced", "AWS Organizations"],
        "answer": ["AWS Firewall Manager"],
        "section": "Remaining Services",
        "explain": "Firewall Manager centrally manages WAF/Shield/Security Group rules at the AWS Organizations level, across multiple accounts.",
    },
    {
        "q": "A company wants to share a VPC subnet with another AWS account without duplicating the resource. Which service?",
        "options": ["AWS Direct Connect", "AWS RAM (Resource Access Manager)", "AWS Transit Gateway", "AWS PrivateLink"],
        "answer": ["AWS RAM (Resource Access Manager)"],
        "section": "Remaining Services",
        "explain": "RAM securely shares resources like subnets and Transit Gateways across accounts without duplicating them.",
    },

    # ---------------- Multi-select examples ----------------
    {
        "q": "(Select TWO) Which of the following are part of the AWS Developer Tools CI/CD suite covered in this module/bible?",
        "options": ["AWS CodeBuild", "Amazon Connect", "AWS CodeDeploy", "AWS IoT Core"],
        "answer": ["AWS CodeBuild", "AWS CodeDeploy"],
        "section": "Dev Tools",
        "explain": "CodeBuild (build/test) and CodeDeploy (deploy) are both CI/CD pipeline stages. Connect and IoT Core belong to other categories.",
    },
    {
        "q": "(Select TWO) Which services are specifically about END-USER COMPUTING (EUC)?",
        "options": ["Amazon WorkSpaces", "Amazon AppStream 2.0", "AWS Cloud9", "Amazon Connect"],
        "answer": ["Amazon WorkSpaces", "Amazon AppStream 2.0"],
        "section": "End-User Computing",
        "explain": "WorkSpaces (full desktop) and AppStream 2.0 (app streaming) are both EUC services. Cloud9 is a dev IDE; Connect is a contact center.",
    },
    {
        "q": "(Select TWO) Which of these are TRUE about the Well-Architected Framework?",
        "options": [
            "It has 6 pillars including Sustainability",
            "It is itself a paid AWS service",
            "The Well-Architected Tool applying it is free",
            "It automatically remediates architecture issues",
        ],
        "answer": ["It has 6 pillars including Sustainability", "The Well-Architected Tool applying it is free"],
        "section": "Well-Architected Framework",
        "explain": "Framework = free concept/checklist (not a paid service itself); Tool = free service that applies it and gives recommendations (no auto-fix).",
    },
]

RESULTS_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_log.txt")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_next_run_number():
    if not os.path.exists(RESULTS_LOG):
        return 1
    with open(RESULTS_LOG, "r") as f:
        lines = [l for l in f if l.strip().startswith("Run #")]
    return len(lines) + 1


def ask_question(idx, total, qdata):
    print(f"\nQ{idx}/{total}  [{qdata['section']}]")
    print(qdata["q"])

    options = qdata["options"][:]
    random.shuffle(options)

    multi = len(qdata["answer"]) > 1
    if multi:
        print("(Multiple correct answers — enter comma-separated letters, e.g. A,C)")

    letters = [chr(65 + i) for i in range(len(options))]
    for letter, opt in zip(letters, options):
        print(f"  {letter}) {opt}")

    while True:
        raw = input("Your answer: ").strip().upper()
        if not raw:
            print("Please enter an answer.")
            continue
        picks = [p.strip() for p in raw.split(",") if p.strip()]
        if all(p in letters for p in picks):
            break
        print(f"Invalid input. Use letters from {', '.join(letters)}.")

    chosen_options = [options[letters.index(p)] for p in picks]
    correct = set(chosen_options) == set(qdata["answer"])

    if correct:
        print("✅ Correct!")
    else:
        print(f"❌ Incorrect. Correct answer: {', '.join(qdata['answer'])}")
    print(f"💡 {qdata['explain']}")

    return correct


def run_quiz():
    clear_screen()
    print("=" * 70)
    print(" AWS CCP (CLF-C02) — Module 13 + Remaining Services Bible — MCQ Test")
    print("=" * 70)

    n_input = input(f"\nTotal questions available: {len(QUESTIONS)}. How many do you want? (Enter = all): ").strip()
    num_q = len(QUESTIONS) if not n_input else max(1, min(len(QUESTIONS), int(n_input)))

    pool = QUESTIONS[:]
    random.shuffle(pool)
    quiz_set = pool[:num_q]

    section_stats = {}  # section -> [correct, total]
    score = 0

    for i, qdata in enumerate(quiz_set, start=1):
        sec = qdata["section"]
        section_stats.setdefault(sec, [0, 0])
        section_stats[sec][1] += 1

        if ask_question(i, num_q, qdata):
            score += 1
            section_stats[sec][0] += 1

    # ---------------- Summary ----------------
    pct = (score / num_q) * 100
    print("\n" + "=" * 70)
    print(f" RESULT: {score}/{num_q}  ({pct:.1f}%)")
    print("=" * 70)

    print("\nSection-wise breakdown (weak-spot flagging):")
    weak_spots = []
    for sec, (correct, total) in sorted(section_stats.items()):
        sec_pct = (correct / total) * 100
        flag = "  ⚠️ WEAK SPOT" if sec_pct < 70 else ""
        print(f"  {sec:<28} {correct}/{total}  ({sec_pct:.0f}%){flag}")
        if sec_pct < 70:
            weak_spots.append(sec)

    if weak_spots:
        print(f"\n👉 Focus revision on: {', '.join(weak_spots)}")
    else:
        print("\n👍 No weak spots below 70% — solid run!")

    # ---------------- Log result ----------------
    run_no = get_next_run_number()
    with open(RESULTS_LOG, "a") as f:
        f.write(f"Run #{run_no} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                 f"Score: {score}/{num_q} ({pct:.1f}%) | "
                 f"Weak spots: {', '.join(weak_spots) if weak_spots else 'None'}\n")

    print(f"\nResult logged to: {RESULTS_LOG}  (Run #{run_no})")
    print("Good luck for the exam! 🚀\n")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Bye!")
        sys.exit(0)
