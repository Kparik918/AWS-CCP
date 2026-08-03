"""
AWS Certified Cloud Practitioner (CLF-C02)
Module 11 — Pricing & Support
Exam-Mode Practice Quiz

Behavior:
- Questions and options are shuffled each run.
- No per-question correct/incorrect feedback (matches real exam interface).
- Full results (score, topic-wise breakdown, weak topics, missed-question
  review) are shown only after the quiz is submitted, and auto-exported
  to a text file.
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Pricing & Support"

# ---------------------------------------------------------------------------
# QUESTIONS
# Each tuple: (topic, question_text, [options], correct_answer, explanation)
# correct_answer: int (single-select) or list/tuple of ints (multi-select)
# ---------------------------------------------------------------------------

QUESTIONS = [

    # ---------------- 1. PRICING FUNDAMENTALS ----------------
    ("Pricing Fundamentals",
     "Which AWS pricing fundamental allows a customer to pay a discounted rate by committing to a 1-year or 3-year usage term?",
     ["Pay as you go", "Save when you commit", "Pay less by using more", "Free Tier"],
     1,
     "Committing to a usage term (like Reserved Instances or Savings Plans) trades flexibility for a lower rate, which is the 'save when you commit' pricing philosophy."),

    ("Pricing Fundamentals",
     "A startup has highly unpredictable traffic and does not want any upfront commitment. Which pricing philosophy fits best?",
     ["Save when you commit", "Pay less by using more", "Pay as you go", "Consolidated Billing"],
     2,
     "Pay-as-you-go removes upfront commitment and lets customers pay only for what they consume, which suits unpredictable workloads."),

    ("Pricing Fundamentals",
     "Which of the following is generally FREE on AWS?",
     ["Data transfer OUT to the internet", "Data transfer IN to AWS", "Storage over the free tier limit", "Reserved Instance upfront fees"],
     1,
     "Data transfer into AWS is generally free; AWS primarily charges for outbound data transfer to the internet, which is a classic exam trap."),

    ("Pricing Fundamentals",
     "Select the THREE dimensions AWS primarily bills customers on.",
     ["Compute", "Storage", "Data transfer OUT", "Number of IAM users created"],
     [0, 1, 2],
     "AWS pricing fundamentally centers on compute time used, storage consumed, and outbound data transfer; IAM users themselves are not a billable dimension."),

    ("Pricing Fundamentals",
     "A stable enterprise workload runs 24/7 for the foreseeable future with predictable usage. Which pricing strategy is most cost-efficient?",
     ["Pay as you go with On-Demand only", "Commitment-based pricing (Reserved Instances/Savings Plans)", "AWS Marketplace subscription", "Free Tier"],
     1,
     "Predictable, always-on workloads benefit most from committing to usage over time, unlocking the 'save when you commit' discount."),

    ("Pricing Fundamentals",
     "Why does AWS's pricing model appeal to businesses moving away from traditional data centers?",
     ["It eliminates the need for security", "It converts capital expenditure (CapEx) into operational expenditure (OpEx)", "It guarantees zero cost", "It removes the need for any support plan"],
     1,
     "AWS removes the large upfront capital investment in hardware, letting customers pay for usage as an operating expense instead."),

    # ---------------- 2. BILLING ACCOUNT MODELS ----------------
    ("Billing Account Models",
     "A company has three AWS accounts (Dev, Test, Prod) and wants ONE combined invoice while still keeping the accounts isolated for security. What should they use?",
     ["Single Account Billing", "AWS Marketplace", "Consolidated Billing via AWS Organizations", "AWS Support Plans"],
     2,
     "Consolidated Billing, a feature of AWS Organizations, merges usage from linked accounts into a single invoice while each account remains isolated for access and resources."),

    ("Billing Account Models",
     "EXAM TRAP: Does Consolidated Billing give the Payer (Management) Account access to resources in the linked accounts?",
     ["Yes, it automatically grants full resource access", "No, it only merges billing; resource access is separate and still requires explicit permissions", "Yes, but only for EC2 resources", "No, Consolidated Billing is unrelated to AWS Organizations"],
     1,
     "Consolidated Billing is a billing-only feature; it does not grant the management account access to member accounts' resources, which is a frequently tested distinction."),

    ("Billing Account Models",
     "What is a key financial benefit of Consolidated Billing for a company with many linked accounts?",
     ["Each account gets its own separate volume discount tier", "Combined usage across accounts can reach volume pricing tiers and share Reserved Instance/Savings Plan benefits faster", "It removes the need for a Support Plan", "It automatically applies the Free Tier to every linked account indefinitely"],
     1,
     "Because usage is combined across linked accounts, the organization can reach volume discount thresholds and share RI/Savings Plans benefits sooner than any single small account could alone."),

    ("Billing Account Models",
     "A solo developer running one small project with no other AWS accounts should use:",
     ["Consolidated Billing", "Single Account Billing", "Enterprise Support", "AWS Partner Network"],
     1,
     "With only one account and no need for shared invoicing, single account billing is sufficient and simplest."),

    ("Billing Account Models",
     "Which AWS service must be used to enable Consolidated Billing?",
     ["AWS Budgets", "AWS Trusted Advisor", "AWS Organizations", "AWS Marketplace"],
     2,
     "Consolidated Billing is a feature provided under AWS Organizations, which links multiple accounts under one management (payer) account."),

    # ---------------- 3. BILLING & COST MANAGEMENT TOOLS ----------------
    ("Billing & Cost Management Tools",
     "A company wants to estimate the monthly cost of an architecture BEFORE deploying anything on AWS. Which tool should they use?",
     ["AWS Cost Explorer", "AWS Budgets", "AWS Pricing Calculator", "AWS Compute Optimizer"],
     2,
     "AWS Pricing Calculator is a free, pre-purchase estimation tool used to model costs of a hypothetical architecture before deployment."),

    ("Billing & Cost Management Tools",
     "EXAM TRAP: A finance team wants to be ALERTED when spending is about to exceed a set threshold. Which tool do they need?",
     ["AWS Cost Explorer", "AWS Budgets", "AWS Pricing Calculator", "AWS Trusted Advisor"],
     1,
     "AWS Budgets is the proactive/preventive tool that sends alerts when usage or cost approaches or exceeds a defined threshold; Cost Explorer is reactive/historical, which is the classic point of confusion."),

    ("Billing & Cost Management Tools",
     "Which tool would a DevOps engineer use to analyze which service cost the most last quarter and forecast next quarter's spend?",
     ["AWS Budgets", "AWS Cost Explorer", "AWS Pricing Calculator", "AWS Marketplace"],
     1,
     "AWS Cost Explorer visualizes historical cost and usage data and provides forecasting, making it the right tool for reviewing past spend and predicting trends."),

    ("Billing & Cost Management Tools",
     "A company is running EC2 instances at consistently low CPU utilization and wants data-driven rightsizing recommendations. Which service should they use?",
     ["AWS Compute Optimizer", "AWS Budgets", "AWS Pricing Calculator", "AWS Organizations"],
     0,
     "AWS Compute Optimizer uses machine learning on historical utilization data to recommend optimal resource types and sizes, reducing cost from over-provisioning."),

    ("Billing & Cost Management Tools",
     "Which service centrally manages multiple AWS accounts and also enables Consolidated Billing?",
     ["AWS Budgets", "AWS Organizations", "AWS Cost Explorer", "AWS Trusted Advisor"],
     1,
     "AWS Organizations is used to centrally manage multiple accounts and is the service through which Consolidated Billing is enabled."),

    ("Billing & Cost Management Tools",
     "EXAM TRAP: Service Control Policies (SCPs) and Consolidated Billing are both found under AWS Organizations. What is the key difference between them?",
     ["They are the same feature with two names", "SCPs handle governance/permissions, while Consolidated Billing handles cost/invoicing — they serve different purposes", "SCPs are a billing feature and Consolidated Billing is a security feature", "SCPs only work with Enterprise Support"],
     1,
     "SCPs are a governance tool for controlling permissions across accounts, while Consolidated Billing is purely a billing/invoicing feature; conflating the two is a common exam trap."),

    ("Billing & Cost Management Tools",
     "Select the TWO tools that are primarily used to track and manage costs AFTER usage has already occurred, rather than before.",
     ["AWS Pricing Calculator", "AWS Cost Explorer", "AWS Billing and Cost Management Console", "AWS Marketplace"],
     [1, 2],
     "Cost Explorer and the Billing and Cost Management Console both deal with actual incurred costs and invoices, while the Pricing Calculator is used before deployment to estimate future cost."),

    ("Billing & Cost Management Tools",
     "Where would a finance manager go each month to download the official invoice PDF and check applied discounts?",
     ["AWS Cost Explorer", "AWS Billing and Cost Management Console", "AWS Compute Optimizer", "AWS Trusted Advisor"],
     1,
     "The Billing and Cost Management Console is the central hub for viewing and downloading invoices and monitoring credits and discounts."),

    ("Billing & Cost Management Tools",
     "A company wants recommendations for downsizing an oversized Auto Scaling group without impacting performance. Which service provides this?",
     ["AWS Budgets", "AWS Compute Optimizer", "AWS Pricing Calculator", "AWS Cost Explorer"],
     1,
     "AWS Compute Optimizer analyzes utilization patterns of resources including Auto Scaling groups and recommends optimal, cost-effective configurations."),

    ("Billing & Cost Management Tools",
     "EXAM TRAP: Does AWS Budgets automatically stop or terminate resources once a spending limit is exceeded?",
     ["Yes, always automatically", "No — by default it only sends alerts; automated actions must be explicitly configured", "Yes, but only for EC2", "No, Budgets cannot trigger any automated action at all"],
     1,
     "By default, AWS Budgets is an alerting tool, not a hard spending cutoff; automated stop actions are possible but require explicit configuration, which many candidates assume is automatic."),

    ("Billing & Cost Management Tools",
     "A company wants to see a visual forecast of what next month's AWS bill will likely be, based on trends from the past six months. Which tool is best suited?",
     ["AWS Cost Explorer", "AWS Pricing Calculator", "AWS Organizations", "AWS Marketplace"],
     0,
     "AWS Cost Explorer includes forecasting capability built on historical cost and usage trends, making it suitable for predicting near-future spend."),

    ("Billing & Cost Management Tools",
     "Which of the following is NOT a function of AWS Organizations?",
     ["Enabling Consolidated Billing", "Enforcing Service Control Policies", "Central account management", "Providing per-second cost forecasting graphs"],
     3,
     "Cost forecasting graphs are a function of AWS Cost Explorer, not AWS Organizations, which focuses on account governance and consolidated billing."),

    # ---------------- 4. AWS SUPPORT PLANS ----------------
    ("AWS Support Plans",
     "EXAM TRAP: Basic Support's 24/7 customer service covers which type of issues?",
     ["Full technical support for all AWS services", "Account and billing support only, not technical support", "Only security incidents", "Only Trusted Advisor issues"],
     1,
     "Basic Support's 24/7 customer service is limited to account and billing questions; it explicitly excludes technical support, a very commonly tested trap."),

    ("AWS Support Plans",
     "Which Support Plan is free and automatically included with every AWS account?",
     ["Developer", "Business", "Basic", "Enterprise On-Ramp"],
     2,
     "Basic Support is free and automatically included for all AWS accounts, providing core Trusted Advisor checks, forums, and account/billing support only."),

    ("AWS Support Plans",
     "A solo developer building an MVP wants an affordable safety net to email AWS support with technical questions during business hours. Which plan fits best?",
     ["Basic", "Developer", "Business", "Enterprise"],
     1,
     "Developer Support is the low fixed-fee entry-level paid plan offering single-contact, business-hours email support, ideal for individuals experimenting or building early-stage projects."),

    ("AWS Support Plans",
     "EXAM TRAP: Which Support Plan(s) include access to a Technical Account Manager (TAM)? Select TWO.",
     ["Business", "Enterprise On-Ramp (pooled TAM)", "Developer", "Enterprise (dedicated TAM)"],
     [1, 3],
     "A TAM is only available starting at Enterprise On-Ramp (pooled access) and Enterprise (dedicated); Business Support does not include a TAM at all, which is a frequently tested trap."),

    ("AWS Support Plans",
     "An e-commerce company running a live production website needs 24/7 phone, chat, and email support with a fast response if checkout goes down. Which plan is most appropriate?",
     ["Basic", "Developer", "Business", "None of the above"],
     2,
     "Business Support provides 24/7 phone/chat/email access, Full Trusted Advisor, and response times as fast as 1 hour for production-down issues, matching a production e-commerce need."),

    ("AWS Support Plans",
     "A large bank runs a mission-critical system where even 1 minute of downtime causes major financial loss. Which Support Plan is most appropriate?",
     ["Business", "Enterprise On-Ramp", "Enterprise", "Developer"],
     2,
     "Enterprise Support offers the fastest response times (as fast as ~15 minutes for business-critical system down) plus a dedicated TAM, suited for mission-critical workloads."),

    ("AWS Support Plans",
     "EXAM TRAP: Which Support Plans include only the 7 core Trusted Advisor checks rather than the full check set?",
     ["Business and Enterprise", "Basic and Developer", "Enterprise On-Ramp and Enterprise", "All plans include full checks"],
     1,
     "Basic and Developer plans only include the 7 core Trusted Advisor checks; Full Trusted Advisor (all check categories) requires Business tier or above."),

    ("AWS Support Plans",
     "What distinguishes Enterprise On-Ramp from full Enterprise Support?",
     ["On-Ramp has no Trusted Advisor access", "On-Ramp provides a pooled group of TAMs rather than one dedicated TAM, with slightly slower response tiers", "On-Ramp is completely free", "On-Ramp only supports Basic-tier accounts"],
     1,
     "Enterprise On-Ramp bridges Business and full Enterprise by offering pooled access to a group of TAMs and faster (but not the fastest) response times, rather than a single dedicated TAM."),

    ("AWS Support Plans",
     "How is pricing generally structured for the Business, Enterprise On-Ramp, and Enterprise Support Plans?",
     ["A flat monthly fee regardless of usage", "Based on a percentage of monthly AWS usage (with a minimum)", "Completely free once Basic Support is active", "Priced per support ticket submitted"],
     1,
     "Business, Enterprise On-Ramp, and Enterprise Support pricing is generally tiered as a percentage of monthly AWS usage with a minimum charge, unlike Developer's flat fee."),

    ("AWS Support Plans",
     "Which Support Plan uses a flat fixed fee rather than usage-based pricing?",
     ["Business", "Developer", "Enterprise", "Enterprise On-Ramp"],
     1,
     "Developer Support is priced as a low flat fixed fee, while Business, Enterprise On-Ramp, and Enterprise scale with a percentage of usage."),

    ("AWS Support Plans",
     "Select the TWO features that are exclusive to Business Support and above (not available on Basic or Developer).",
     ["24/7 phone support", "Full AWS Trusted Advisor (all checks)", "AWS Personal Health Dashboard", "Support Forums / re:Post"],
     [0, 1],
     "24/7 phone support and Full Trusted Advisor checks both begin at the Business tier; the Personal Health Dashboard and community forums are available on every plan including Basic."),

    ("AWS Support Plans",
     "A company on Business Support is planning a major planned event, like a big holiday sale, and wants proactive guidance to manage the risk. What optional feature can help?",
     ["Infrastructure Event Management (available as an add-on)", "Trust and Safety Center", "AWS Partner Network", "Consolidated Billing"],
     0,
     "Infrastructure Event Management is available as an add-on starting at Business Support and provides proactive guidance for planned high-risk events."),

    ("AWS Support Plans",
     "A company currently on Developer Support has scaled up and now runs a live production application needing 24/7 phone support with unlimited contacts. What is the minimum plan they should upgrade to?",
     ["Business", "Basic", "Stay on Developer", "AWS Marketplace subscription"],
     0,
     "Business Support is the minimum tier that adds 24/7 phone/chat/email access and unlimited contacts, which Developer does not provide."),

    # ---------------- 5. AWS MARKETPLACE ----------------
    ("AWS Marketplace",
     "What is AWS Marketplace?",
     ["A support ticketing system", "A curated digital catalog to find, buy, and deploy third-party software that runs on AWS", "A free community Q&A forum", "AWS's internal billing dashboard"],
     1,
     "AWS Marketplace is a curated catalog where customers can find, test, purchase, and deploy third-party software that runs on AWS infrastructure."),

    ("AWS Marketplace",
     "EXAM TRAP: Is software purchased through AWS Marketplace built and maintained by AWS?",
     ["Yes, always", "No — it is built by Independent Software Vendors (ISVs), even though billing is consolidated into the AWS invoice", "Yes, but only ML-related software", "No, Marketplace software cannot be billed through AWS"],
     1,
     "Marketplace software comes from third-party Independent Software Vendors, not AWS itself; the key benefit is that billing is still folded into the customer's existing AWS invoice."),

    ("AWS Marketplace",
     "A company wants to purchase a third-party Web Application Firewall (WAF) product that runs on AWS instead of building one in-house. What should they use?",
     ["AWS Partner Network", "AWS Trusted Advisor", "AWS Marketplace", "AWS re:Post"],
     2,
     "AWS Marketplace is the digital storefront for buying vetted third-party software, like a WAF, that deploys directly onto AWS infrastructure."),

    ("AWS Marketplace",
     "Which pricing options are typically available for software purchased on AWS Marketplace? Select TWO.",
     ["Pay-as-you-go", "Annual subscription", "Only lifetime one-time purchase", "Only free-of-charge licensing"],
     [0, 1],
     "AWS Marketplace software commonly offers flexible pricing, including pay-as-you-go and annual subscription options, in addition to some free listings."),

    ("AWS Marketplace",
     "What is a key business benefit of using AWS Marketplace instead of building software in-house?",
     ["It guarantees a dedicated TAM", "It reduces Total Cost of Ownership (TCO) by leveraging existing vetted solutions instead of building from scratch", "It replaces the need for a Support Plan", "It automatically upgrades a customer's Support Plan tier"],
     1,
     "AWS Marketplace reduces Total Cost of Ownership by giving customers access to already-built, vetted third-party solutions instead of requiring in-house development."),

    # ---------------- 6. AWS PARTNER NETWORK (APN) ----------------
    ("AWS Partner Network (APN)",
     "What is the AWS Partner Network (APN)?",
     ["A support plan tier above Enterprise", "A global community/program for consulting and technology businesses that build solutions using AWS", "A free-tier eligible service for new accounts", "A billing tool for tracking partner discounts"],
     1,
     "APN is a global program connecting technology and consulting companies that build AWS-based solutions and services, helping customers find specialized implementation help."),

    ("AWS Partner Network (APN)",
     "A retail company hosting on AWS wants a specialized analytics/ML partner to help build a personalization engine. Where would they look?",
     ["AWS Trust and Safety Center", "AWS Partner Network (APN)", "AWS Budgets", "AWS re:Post"],
     1,
     "The AWS Partner Network connects customers with specialized consulting and technology partners for implementation help, such as building a personalization engine."),

    ("AWS Partner Network (APN)",
     "EXAM TRAP: Is APN a type of AWS Support Plan?",
     ["Yes, it is the highest support tier", "No, APN is a partner/consulting ecosystem program, distinct from Support Plans and TAM access", "Yes, it replaces the need for Enterprise Support", "No, APN is only available to AWS employees"],
     1,
     "APN is a partner ecosystem program for consulting and technology companies, not a customer support plan; confusing it with Enterprise Support/TAM access is a common trap."),

    ("AWS Partner Network (APN)",
     "Which of the following is a benefit AWS provides to companies that join the AWS Partner Network?",
     ["Guaranteed dedicated TAM for all their end customers", "Funding benefits, partner events, and specialized training/certification tracks", "Free unlimited EC2 usage", "Automatic Enterprise Support upgrade"],
     1,
     "APN offers partners funding benefits, access to partner events, and specialized training and certification tracks to help them build, market, and sell on AWS."),

    # ---------------- 7. AWS RE:POST & TRUST AND SAFETY CENTER ----------------
    ("AWS re:Post & Trust and Safety Center",
     "What is AWS re:Post?",
     ["A paid ticketing system with guaranteed response times", "A free, community-driven Q&A platform for AWS users", "A tool for reporting phishing or malware hosted on AWS", "A Support Plan tier"],
     1,
     "AWS re:Post is a free, community-powered Q&A platform where users share knowledge and help each other solve AWS-related problems."),

    ("AWS re:Post & Trust and Safety Center",
     "EXAM TRAP: Does AWS re:Post replace the need for a paid AWS Support Plan?",
     ["Yes, it fully replaces paid support with guaranteed SLAs", "No — it supplements paid support but has no guaranteed response times, since it is community-driven", "Yes, but only for Enterprise customers", "No, re:Post is not related to AWS at all"],
     1,
     "re:Post is free and community-driven with no guaranteed official response time, so it supplements but does not replace paid Support Plans, which is a key exam distinction."),

    ("AWS re:Post & Trust and Safety Center",
     "Where should someone report that an AWS-hosted resource is being used for phishing or malware distribution?",
     ["AWS re:Post", "AWS Trust and Safety Center", "AWS Marketplace", "AWS Budgets"],
     1,
     "The AWS Trust and Safety Center is the central place to report abusive activity, such as phishing or malware, occurring on AWS infrastructure."),

    ("AWS re:Post & Trust and Safety Center",
     "Which statement correctly differentiates AWS re:Post from the Trust and Safety Center?",
     ["re:Post handles abuse reports; Trust and Safety Center is for technical Q&A", "re:Post is community Q&A for technical help; Trust and Safety Center is for reporting platform abuse", "They are the same service with two names", "Both are part of the Enterprise Support Plan only"],
     1,
     "re:Post serves as free community-driven technical Q&A, while the Trust and Safety Center exists specifically to report abusive or malicious activity on the AWS platform."),

    # ---------------- CROSS-TOPIC / SCENARIO / TRAP MIX ----------------
    ("Billing & Cost Management Tools",
     "SCENARIO: A company wants to see one invoice for 5 linked AWS accounts, get alerted before overspending, and estimate the cost of a new architecture before building it. Match the THREE correct tools respectively. Select THREE.",
     ["AWS Organizations (Consolidated Billing)", "AWS Budgets", "AWS Pricing Calculator", "AWS Trusted Advisor"],
     [0, 1, 2],
     "Consolidated Billing under AWS Organizations merges invoices, AWS Budgets provides overspend alerts, and the AWS Pricing Calculator estimates cost before deployment — three distinct tools for three distinct needs."),

    ("Pricing Fundamentals",
     "A company transfers a large volume of data from an on-premises data center INTO an S3 bucket for backup purposes. What will they generally be charged for this transfer?",
     ["A high per-GB outbound fee", "Nothing — data transfer IN to AWS is generally free", "A flat monthly support fee", "The same as Enterprise Support pricing"],
     1,
     "Data transfer into AWS (inbound) is generally free of charge; only outbound data transfer to the internet is typically billed."),

    ("AWS Support Plans",
     "EXAM TRAP: A company on the Business Support Plan asks for a dedicated Technical Account Manager. Can Business Support provide this?",
     ["Yes, all paid plans include a dedicated TAM", "No — a dedicated TAM is exclusive to Enterprise Support; Business Support does not include any TAM", "Yes, but only during business hours", "No, only Basic Support includes a TAM"],
     1,
     "A dedicated TAM is only available on Enterprise Support, with Enterprise On-Ramp offering a pooled version; Business Support includes neither, making this a high-frequency trap."),

    ("Billing Account Models",
     "What happens to per-account resource isolation when a company enables Consolidated Billing across its AWS Organizations accounts?",
     ["All accounts merge into a single account", "Resource isolation is unaffected — Consolidated Billing only merges the invoice, not access or resources", "IAM users automatically get access to every linked account", "All accounts lose their individual account IDs"],
     1,
     "Consolidated Billing is strictly a billing feature; each linked account keeps its own resource and access isolation unless separately configured otherwise."),
]


# ---------------------------------------------------------------------------
# QUIZ ENGINE (reusable across modules — do not change per module)
# ---------------------------------------------------------------------------

def _normalize_correct(correct):
    """Always return correct answer(s) as a sorted list of ints."""
    if isinstance(correct, (list, tuple)):
        return sorted(correct)
    return [correct]


def _num_word(n):
    words = {2: "TWO", 3: "THREE", 4: "FOUR"}
    return words.get(n, str(n))


def run_quiz():
    print("=" * 70)
    print(f"AWS CCP (CLF-C02) — MODULE 11: {MODULE_NAME}")
    print("EXAM MODE: Answers are recorded silently. Results appear at the end.")
    print("=" * 70)

    quiz_questions = list(QUESTIONS)
    random.shuffle(quiz_questions)

    results = []

    for idx, q in enumerate(quiz_questions, 1):
        topic, question_text, options, correct, explanation = q
        correct_norm = _normalize_correct(correct)

        indices = list(range(len(options)))
        random.shuffle(indices)
        shuffled_options = [options[i] for i in indices]
        new_correct = sorted(indices.index(ci) for ci in correct_norm)

        is_multi = len(new_correct) > 1

        print(f"\nQ{idx}. {question_text}")
        if is_multi:
            print(f"   (Select {_num_word(len(new_correct))})")
        for i, opt in enumerate(shuffled_options):
            print(f"  {chr(65 + i)}. {opt}")

        if is_multi:
            raw = input(f"Your answer ({len(new_correct)} letters, comma-separated, e.g. A,C): ").strip().upper()
            selected = sorted({
                ord(c.strip()) - 65
                for c in raw.split(",")
                if c.strip() and c.strip()[0].isalpha()
            })
        else:
            raw = input("Your answer (single letter): ").strip().upper()
            selected = [ord(raw[0]) - 65] if raw and raw[0].isalpha() else []

        is_correct = selected == new_correct

        results.append({
            "topic": topic,
            "question_text": question_text,
            "options": shuffled_options,
            "selected": selected,
            "correct": new_correct,
            "explanation": explanation,
            "is_correct": is_correct,
        })

        print("Answer recorded.")

    print_results(results)


def _letters(indices, options):
    if not indices:
        return "(no answer given)"
    return ", ".join(f"{chr(65 + i)}. {options[i]}" for i in indices)


def print_results(results):
    total = len(results)
    correct_count = sum(1 for r in results if r["is_correct"])
    pct = (correct_count / total * 100) if total else 0.0

    topic_stats = defaultdict(lambda: [0, 0])  # [correct, total]
    for r in results:
        topic_stats[r["topic"]][1] += 1
        if r["is_correct"]:
            topic_stats[r["topic"]][0] += 1

    topic_breakdown = []
    for topic, (c, t) in topic_stats.items():
        topic_pct = (c / t * 100) if t else 0.0
        topic_breakdown.append((topic, c, t, topic_pct))
    topic_breakdown.sort(key=lambda x: x[3])  # weakest first

    weak_topics = [tb for tb in topic_breakdown if tb[3] < 70.0]
    missed = [r for r in results if not r["is_correct"]]

    lines = []
    lines.append("=" * 70)
    lines.append(f"RESULTS — MODULE 11: {MODULE_NAME}")
    lines.append("=" * 70)
    lines.append(f"Score: {correct_count}/{total} ({pct:.1f}%)")
    lines.append("")
    lines.append("Topic-Wise Breakdown (weakest first):")
    for topic, c, t, topic_pct in topic_breakdown:
        lines.append(f"  - {topic}: {c}/{t} ({topic_pct:.1f}%)")
    lines.append("")

    if weak_topics:
        lines.append("⚠ Weak Topics (<70%):")
        for topic, c, t, topic_pct in weak_topics:
            lines.append(f"  - {topic}: {topic_pct:.1f}%")
    else:
        lines.append("No topics fell below 70%. Solid performance across the board.")
    lines.append("")

    lines.append("Missed Questions Review:")
    lines.append("-" * 70)
    if not missed:
        lines.append("None — all questions answered correctly.")
    else:
        for i, r in enumerate(missed, 1):
            lines.append(f"{i}. {r['question_text']}")
            lines.append(f"   Your answer:    {_letters(r['selected'], r['options'])}")
            lines.append(f"   Correct answer: {_letters(r['correct'], r['options'])}")
            lines.append(f"   Explanation: {r['explanation']}")
            lines.append("")

    report = "\n".join(lines)
    print("\n" + report)

    export_filename = f"{MODULE_NAME}-Results.txt"
    try:
        with open(export_filename, "w", encoding="utf-8") as f:
            f.write(report)
            f.write(f"\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"\nReport exported to: {os.path.abspath(export_filename)}")
    except OSError as e:
        print(f"\nCould not export report: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\nQuiz interrupted.")
        sys.exit(1)
