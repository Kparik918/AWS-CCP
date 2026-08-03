#!/usr/bin/env python3
"""
AWS CCP (CLF-C02) - Module 1: Cloud Fundamentals - Practice MCQ Test
======================================================================
Covers: Cloud Computing Basics, AWS Overview, Cloud Deployment Models,
The Six Benefits of Cloud Computing, AWS Global Infrastructure
(Regions/AZs/Edge Locations/Local Zones/Wavelength/Outposts), Shared
Responsibility Model, and High Availability / Disaster Recovery scenarios.

Run:  python3 1-CloudFundamentals.py

EXAM-MODE BEHAVIOR: No feedback is shown per question (matches the real
CLF-C02 exam interface). At the end you get:
  - Overall score
  - Topic-wise breakdown (weakest first, so you know exactly what to re-study)
  - A dedicated "Missed Questions Review" section (only questions you got
    wrong, with your answer, the correct answer, and why)
  - Auto-exported report to Module1-CloudFundamentals-Results.txt
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Module1-CloudFundamentals"

# Each question: (topic, question_text, [options], correct_answer(s), explanation)
# correct_answer(s): a single 0-based int for single-select questions,
#                     OR a list/tuple of 0-based ints for multi-select ("Select TWO/THREE") questions.
QUESTIONS = [
    # ---------------- 1. Cloud Computing Fundamentals ----------------
    ("Cloud Computing Fundamentals",
     "Which of the following best defines cloud computing?",
     ["A dedicated physical data center owned by a single company",
      "On-demand delivery of IT resources over the internet with pay-as-you-go pricing",
      "A type of local area network used only within an office",
      "A backup strategy that stores data on external hard drives"],
     1,
     "Cloud computing is the on-demand delivery of compute, storage, database, and networking resources over the internet, billed on actual usage."),

    ("Cloud Computing Fundamentals",
     "A startup wants to avoid buying physical servers before it even knows if its business will succeed. Which cloud computing shift addresses this directly?",
     ["Trading CapEx for OpEx", "Increasing network bandwidth", "Reducing application code size", "Hiring more IT staff"],
     0,
     "Cloud removes large upfront Capital Expenditure and replaces it with pay-as-you-go Operational Expenditure."),

    ("Cloud Computing Fundamentals",
     "Which characteristic of cloud computing means resources can be provisioned by the customer without requiring human interaction from the provider?",
     ["Broad network access", "On-demand self-service", "Resource pooling", "Measured service"],
     1,
     "On-demand self-service means a customer can provision resources automatically, without needing a human at the provider's side."),

    ("Cloud Computing Fundamentals",
     "True or False: In cloud computing, you always pay a fixed monthly fee regardless of how much you actually use.",
     ["True", "False"],
     1,
     "Cloud computing is pay-as-you-go (variable expense) - usage determines cost, not a flat fixed fee."),

    ("Cloud Computing Fundamentals",
     "A company's traffic grows and shrinks unpredictably throughout the year. Which cloud characteristic lets them upgrade or downgrade resources instantly without downtime?",
     ["Resource pooling", "Scalability and elasticity", "Broad network access", "Vendor lock-in"],
     1,
     "Scalable and elastic resources can grow or shrink instantly to match demand, without planned downtime."),

    ("Cloud Computing Fundamentals",
     "Exam Trap: A question mentions 'on-demand' pricing being available for EC2. Is this the same concept as the general cloud characteristic 'on-demand self-service'?",
     ["Yes, they are identical concepts", "No - 'on-demand self-service' is a general cloud trait; 'On-Demand pricing' is a specific EC2 pricing model", "Yes, both only refer to billing", "No, they are unrelated to AWS entirely"],
     1,
     "This is a classic CCP trap: 'on-demand' as a general cloud characteristic (self-service availability) is different from 'On-Demand' as a specific EC2 pricing model."),

    ("Cloud Computing Fundamentals",
     "What problem did cloud computing primarily solve for companies running on-premises infrastructure before it existed?",
     ["Lack of internet access", "Huge upfront cost and wasted capacity from owning fixed infrastructure regardless of usage", "Too many software licenses", "Excessive employee headcount"],
     1,
     "Before cloud, companies had to buy, rack, power, and maintain their own servers with fixed cost regardless of actual usage - cloud decouples needing compute from owning hardware."),

    ("Cloud Computing Fundamentals",
     "Which of these is NOT one of the core characteristics typically associated with cloud computing?",
     ["Pay-as-you-go pricing", "Resources pooled globally across data centers", "Mandatory multi-year hardware purchase contracts", "Broad network access over the internet"],
     2,
     "Mandatory long-term hardware purchase contracts are the OPPOSITE of cloud computing - cloud avoids upfront ownership entirely."),

    # ---------------- 2. AWS Overview ----------------
    ("AWS Overview",
     "In what year was Amazon Web Services (AWS) launched as a cloud computing platform?",
     ["2002", "2004", "2006", "2010"],
     2,
     "AWS launched in 2006, after starting internally around 2003 to help scale Amazon's own e-commerce infrastructure."),

    ("AWS Overview",
     "Approximately how many AWS services are available across compute, storage, database, networking, ML, and analytics?",
     ["Around 20", "Around 50", "200+", "Exactly 100"],
     2,
     "AWS offers 200+ services spanning nearly every category of IT infrastructure and application building blocks."),

    ("AWS Overview",
     "Which of the following are AWS's major competitors in the cloud market? (Select TWO)",
     ["Microsoft Azure", "Google Cloud Platform (GCP)", "IBM Watson Assistant", "Adobe Creative Cloud"],
     [0, 1],
     "Microsoft Azure and Google Cloud Platform are AWS's primary competitors among the 'big three' cloud providers."),

    ("AWS Overview",
     "Which factor is generally NOT considered a reason for AWS's continued market dominance?",
     ["First-mover advantage", "Broadest and deepest service catalog", "Being the only cloud provider legally allowed in most countries", "Massive continuous infrastructure investment"],
     2,
     "AWS is not a legal monopoly; its dominance comes from first-mover advantage, service breadth, global reach, and continuous investment, not any legal restriction on competitors."),

    ("AWS Overview",
     "AWS's global cloud market share is generally considered to be:",
     ["The smallest among the big three providers", "Roughly the largest among cloud providers, around 30%", "Exactly tied with Azure at all times", "Irrelevant for the CCP exam"],
     1,
     "AWS has consistently held the largest cloud market share globally, ahead of Azure and GCP."),

    # ---------------- 3. Cloud Deployment Models ----------------
    ("Cloud Deployment Models",
     "A highly regulated bank wants full control over its infrastructure and no dependency on any external cloud provider. Which deployment model fits best?",
     ["Public cloud", "On-premises (private)", "Hybrid", "Multi-cloud"],
     1,
     "On-premises/private deployment gives full control and no cloud dependency, suited for tightly regulated industries."),

    ("Cloud Deployment Models",
     "A company is migrating slowly to the cloud and currently runs some workloads on its own servers while others run on AWS, connected via a VPN. Which deployment model is this?",
     ["Public cloud only", "On-premises only", "Hybrid", "Community cloud"],
     2,
     "Hybrid cloud specifically means a mix of cloud and on-premises infrastructure, often connected via VPN or AWS Direct Connect."),

    ("Cloud Deployment Models",
     "Exam Trap: A company uses both AWS and Google Cloud Platform simultaneously for different workloads. Is this considered 'hybrid cloud'?",
     ["Yes, using two providers is the definition of hybrid", "No - using two cloud providers is called multi-cloud, not hybrid", "Yes, but only if VPN is used", "No, this setup is not possible on AWS"],
     1,
     "Hybrid cloud specifically means cloud + on-premises together. Using two different cloud providers is called multi-cloud - a different concept the exam likes to test."),

    ("Cloud Deployment Models",
     "Which cloud deployment model offers the LEAST amount of direct infrastructure control to the customer, but requires no maintenance overhead?",
     ["On-premises", "Public cloud", "Hybrid", "Private data center"],
     1,
     "Public cloud is fully managed by the provider (shared, multi-tenant infrastructure), trading direct control for zero maintenance burden."),

    ("Cloud Deployment Models",
     "A hospital must keep patient records physically on-site for regulatory reasons, but also wants to use AWS analytics services for other non-sensitive workloads. Which model addresses both needs?",
     ["Public cloud only", "On-premises only", "Hybrid cloud", "Multi-cloud"],
     2,
     "Hybrid cloud allows sensitive on-prem workloads (for compliance) to coexist with cloud-based workloads for flexibility and additional services."),

    ("Cloud Deployment Models",
     "For CCP exam purposes, how should 'private cloud' generally be treated relative to 'on-premises'?",
     ["As completely unrelated concepts", "As essentially the same idea for exam purposes", "Private cloud always means public cloud with extra security", "On-premises always means AWS Outposts"],
     1,
     "While technically private cloud can be run by a third party, for CCP purposes on-premises and private cloud are treated as the same idea."),

    ("Cloud Deployment Models",
     "Which of the following is the best real-world trigger phrase for choosing a HYBRID deployment?",
     ["'We want zero infrastructure to manage'", "'We are migrating gradually and have regulatory + agility trade-offs'", "'We only use AWS for everything'", "'We have no compliance requirements at all'"],
     1,
     "Hybrid cloud is chosen specifically when a company is balancing regulatory/legacy constraints with a desire for cloud agility - typically during migration."),

    # ---------------- 4. Six Benefits of Cloud Computing ----------------
    ("Six Benefits of Cloud Computing",
     "A company previously spent lakhs upfront on servers before knowing if their app would succeed. Moving to AWS lets them pay only for what they use. Which of the six benefits does this describe?",
     ["Go Global in Minutes", "Trade Fixed Expense for Variable Expense", "Increase Speed and Agility", "Economies of Scale"],
     1,
     "This is the classic CapEx-to-OpEx shift: fixed upfront expense becomes variable, usage-based expense."),

    ("Six Benefits of Cloud Computing",
     "AWS is able to offer lower prices because it purchases hardware, bandwidth, and electricity in bulk across millions of customers. Which benefit is this?",
     ["Stop Guessing Capacity", "Benefit from Massive Economies of Scale", "Go Global in Minutes", "Increase Speed and Agility"],
     1,
     "Economies of scale means AWS's massive bulk purchasing power lowers costs, and those savings are passed on to customers - no single company could negotiate that scale alone."),

    ("Six Benefits of Cloud Computing",
     "A company used to guess future traffic years in advance, often over-provisioning (wasting money) or under-provisioning (causing outages). Which AWS benefit directly solves this?",
     ["Stop Guessing Capacity", "Economies of Scale", "Go Global in Minutes", "Trade Fixed for Variable Expense"],
     0,
     "Scalability and elasticity remove the need to forecast capacity years ahead - resources adjust automatically to actual demand."),

    ("Six Benefits of Cloud Computing",
     "A team can now deploy new features in minutes instead of the weeks it used to take, allowing faster experimentation and time-to-market. Which benefit is this?",
     ["Increase Speed and Agility", "Stop Spending Money on Data Centers", "Go Global in Minutes", "Economies of Scale"],
     0,
     "Speed and agility refers to the ability to deploy resources and experiment far faster than traditional infrastructure allowed."),

    ("Six Benefits of Cloud Computing",
     "A company no longer needs to hire staff for power, cooling, and physical security of data centers, letting them focus purely on the application. Which benefit is this?",
     ["Stop Guessing Capacity", "Stop Spending Money on Running and Maintaining Data Centers", "Trade Fixed for Variable Expense", "Go Global in Minutes"],
     1,
     "AWS handles the 'undifferentiated heavy lifting' of physical data center operations, freeing internal teams to focus on the application."),

    ("Six Benefits of Cloud Computing",
     "A company wants to launch its service in Japan without building any physical infrastructure there, and can do so within an existing AWS Region in a few clicks. Which benefit is this?",
     ["Go Global in Minutes", "Elasticity", "Economies of Scale", "Trade Fixed for Variable Expense"],
     0,
     "Go Global in Minutes lets companies expand into new geographic markets quickly by deploying into an existing AWS Region, rather than building data centers from scratch."),

    ("Six Benefits of Cloud Computing",
     "Which of the following is NOT one of AWS's officially stated six benefits of cloud computing?",
     ["Trade Fixed Expense for Variable Expense", "Increase Speed and Agility", "Guaranteed 100% uptime with zero possible downtime", "Go Global in Minutes"],
     2,
     "AWS never claims a guarantee of zero possible downtime - that is not one of the six benefits and is factually inaccurate about any cloud provider."),

    ("Six Benefits of Cloud Computing",
     "Exam Trap: A scenario says 'a company wants to lower costs by benefiting from AWS's massive scale' - which of the six benefits is being tested, and NOT which is being tested?",
     ["Economies of Scale is being tested; elasticity is NOT the answer here", "Elasticity is being tested; economies of scale is NOT the answer here", "Speed and Agility is being tested", "Go Global in Minutes is being tested"],
     0,
     "AWS scenario questions test whether you can match the exact trigger phrase ('AWS's scale', 'bulk pricing') to Economies of Scale specifically, not a similar-sounding benefit."),

    ("Six Benefits of Cloud Computing",
     "Which TWO of the six cloud benefits are most directly related to eliminating guesswork and upfront financial risk? (Select TWO)",
     ["Trade Fixed Expense for Variable Expense", "Stop Guessing Capacity", "Go Global in Minutes", "Increase Speed and Agility"],
     [0, 1],
     "Trading fixed for variable expense removes upfront financial risk, while stopping capacity guessing removes the risk of over/under-provisioning."),

    # ---------------- 5. AWS Global Infrastructure ----------------
    ("AWS Global Infrastructure",
     "What is the correct top-to-bottom hierarchy of AWS's physical infrastructure?",
     ["Availability Zones -> Regions -> Edge Locations", "Regions -> Availability Zones -> Edge Locations", "Edge Locations -> Regions -> Availability Zones", "Availability Zones -> Edge Locations -> Regions"],
     1,
     "The hierarchy flows from Regions (independent geographic areas) down to Availability Zones (data centers within a Region) down to Edge Locations (caching sites)."),

    ("AWS Global Infrastructure",
     "What is an Availability Zone (AZ)?",
     ["A globally distributed caching site for CDN content", "One or more physically separate data centers within a Region, with their own power, cooling, and networking", "A single server rack inside one data center", "A third-party data center not owned by AWS"],
     1,
     "An AZ consists of one or more physically separate data centers within a Region, isolated enough to avoid shared disaster but close enough for low-latency synchronous replication."),

    ("AWS Global Infrastructure",
     "Which AWS infrastructure component is used ONLY for content caching (CDN) and CANNOT be used to run EC2 instances?",
     ["Availability Zone", "Region", "Edge Location", "Local Zone"],
     2,
     "Edge Locations exist purely for caching/CDN/DNS purposes (powering CloudFront, Lambda@Edge, Route 53) - you cannot launch EC2 instances there."),

    ("AWS Global Infrastructure",
     "A company wants to protect its application against the failure of a single data center within one geographic area. What should they deploy?",
     ["Single AZ deployment", "Multi-AZ deployment within one Region", "Multi-Region deployment", "Edge Location deployment"],
     1,
     "Multi-AZ deployment spreads instances across 2-3 Availability Zones in the same Region, achieving High Availability if one AZ fails."),

    ("AWS Global Infrastructure",
     "A company needs to protect against an entire Region becoming unavailable due to a natural disaster or geopolitical event. What should they deploy?",
     ["Single AZ deployment", "Multi-AZ deployment", "Multi-Region deployment", "A single Edge Location"],
     2,
     "Multi-Region deployment is used for Disaster Recovery and compliance scenarios where an entire Region could become unavailable."),

    ("AWS Global Infrastructure",
     "Which factor is generally LEAST relevant when choosing which AWS Region to deploy into?",
     ["Latency to the customer base", "Compliance and data residency requirements", "The exact font used on the AWS Console for that Region", "Service availability in that Region"],
     2,
     "Region selection depends on latency, compliance/data residency, cost, and service availability - the AWS Console's appearance is irrelevant."),

    ("AWS Global Infrastructure",
     "Exam Trap: Does one Availability Zone always correspond to exactly one physical data center?",
     ["Yes, always a strict 1:1 mapping", "No - one AZ can contain multiple data centers", "No, an AZ is the same as a Region", "Yes, but only in us-east-1"],
     1,
     "A common CCP trap: AZs are not always exactly one data center - a single AZ can contain multiple data centers."),

    ("AWS Global Infrastructure",
     "Which AWS infrastructure feature is designed to extend a Region closer to large population or industry centers for single-digit-millisecond latency (e.g., gaming, media production)?",
     ["Edge Location", "Local Zone", "Availability Zone", "AWS Outposts"],
     1,
     "Local Zones extend a Region geographically to bring compute and storage closer to large population centers for ultra-low latency use cases."),

    ("AWS Global Infrastructure",
     "Which AWS infrastructure offering physically installs AWS hardware inside a CUSTOMER's own on-premises data center, for workloads that must stay on-prem but still want a consistent AWS experience?",
     ["Wavelength Zones", "AWS Outposts", "Edge Locations", "Local Zones"],
     1,
     "AWS Outposts brings actual AWS hardware into the customer's own data center, enabling a hybrid cloud experience with consistent AWS APIs."),

    ("AWS Global Infrastructure",
     "An India-based e-commerce company wants low latency for its Indian customers, with a secondary Region for disaster recovery. Which setup best fits?",
     ["Single AZ in us-east-1 only", "Primary in ap-south-1 (Mumbai) with Multi-AZ, secondary DR Region like ap-southeast-1", "Single Edge Location in Mumbai only", "On-premises data center in Delhi only"],
     1,
     "Choosing ap-south-1 (Mumbai) minimizes latency for Indian customers, Multi-AZ provides HA, and a secondary Region provides Disaster Recovery."),

    # ---------------- 6. Shared Responsibility Model ----------------
    ("Shared Responsibility Model",
     "Under the AWS Shared Responsibility Model, which of the following is ALWAYS AWS's responsibility, regardless of the service used?",
     ["Guest OS patching", "Physical security of AWS data centers", "Application-level security", "IAM configuration"],
     1,
     "Physical security of AWS's data centers is always AWS's job - security 'OF' the cloud - no service model changes this."),

    ("Shared Responsibility Model",
     "Which of the following is ALWAYS the customer's responsibility, regardless of which AWS service is used?",
     ["Physical hardware maintenance", "Hypervisor management", "Identity and Access Management (IAM) configuration", "Data center cooling systems"],
     2,
     "IAM configuration is always the customer's job - AWS provides the tool, but the customer must configure permissions and access correctly."),

    ("Shared Responsibility Model",
     "For Amazon EC2 (an IaaS service), who is responsible for patching the guest operating system?",
     ["AWS", "The customer", "Neither party", "AWS Support only, upon request"],
     1,
     "For EC2, since it is IaaS, the customer is responsible for patching the guest OS - AWS only manages the underlying hardware and hypervisor."),

    ("Shared Responsibility Model",
     "For Amazon RDS (a managed database service), who is responsible for patching the underlying operating system and database engine?",
     ["The customer", "AWS", "A third-party vendor", "Nobody - it's never patched"],
     1,
     "For managed services like RDS, AWS handles OS and DB engine patching, while the customer still manages database users, access control, and data validation."),

    ("Shared Responsibility Model",
     "AWS announces an OS-level security patch is available for EC2 instances. What is AWS's responsibility in this scenario?",
     ["Automatically applying the patch to all customer instances", "Making the patch available - applying it is the customer's job", "Nothing, since EC2 patching is entirely AWS's job", "Deleting the instance until patched"],
     1,
     "AWS's responsibility ends at making the patch available; applying it to the guest OS is the customer's responsibility for EC2."),

    ("Shared Responsibility Model",
     "How does the Shared Responsibility Model split shift as a service becomes MORE fully managed (e.g., moving from EC2 to S3)?",
     ["AWS takes on progressively LESS responsibility", "AWS takes on progressively MORE responsibility, and the customer's slice shrinks", "The split never changes regardless of service type", "The customer always retains 100% responsibility"],
     1,
     "As a service becomes more managed/abstracted (IaaS to PaaS to SaaS/serverless), AWS handles more of the responsibility and the customer's remaining slice shrinks."),

    ("Shared Responsibility Model",
     "Which of these responsibilities does the customer retain even when using a fully managed service like Amazon S3? (Select TWO)",
     ["Physical security of the storage hardware", "Bucket policies and access permissions", "Data encryption choice", "Underlying storage infrastructure durability"],
     [1, 2],
     "Even for fully managed services like S3, the customer still controls bucket policies/access and chooses how data is encrypted - AWS handles the physical infrastructure and durability."),

    ("Shared Responsibility Model",
     "Exam Trap: If a customer's EC2 instance gets breached because they failed to apply an available OS patch, whose fault is it according to the Shared Responsibility Model?",
     ["AWS's fault, since they host the infrastructure", "The customer's fault, since guest OS patching is their responsibility on EC2", "Neither party is at fault", "It depends on which Region the instance is in"],
     1,
     "Since guest OS patching is explicitly the customer's job on EC2, failing to patch and getting breached is the customer's responsibility, not AWS's."),

    ("Shared Responsibility Model",
     "What is the best one-line way to remember the Shared Responsibility Model's split?",
     ["AWS secures the cloud; customer secures what's in the cloud", "AWS is responsible for everything, the customer for nothing", "The customer is responsible for everything, AWS for nothing", "Responsibility is randomly assigned per incident"],
     0,
     "The core memory trick is: AWS secures security OF the cloud (infrastructure); the customer secures security IN the cloud (their data, access, and configuration)."),

    # ---------------- 7. HA, DR & Real-World Scenarios ----------------
    ("HA, DR & Real-World Scenarios",
     "A cyberattack takes down one entire AWS Region. If the company had a proper Multi-Region DR setup, what generally happens?",
     ["The entire global service goes down with no recovery option", "Traffic can be routed to a healthy Region and service continues with minimal downtime", "AWS automatically refunds all charges", "The company must rebuild everything from scratch"],
     1,
     "With Multi-Region disaster recovery in place, traffic can be redirected to an unaffected Region, allowing service to continue with minimal downtime - this property is called fault tolerance."),

    ("HA, DR & Real-World Scenarios",
     "A global streaming company wants worldwide low-latency content delivery plus regional redundancy. Which combination of AWS infrastructure best supports this?",
     ["Single Region, single AZ", "Multi-Region deployment plus CloudFront using Edge Locations", "On-premises hosting only", "A single Edge Location handling all global traffic"],
     1,
     "Multi-Region deployment provides redundancy and lower latency across geographies, while CloudFront's Edge Locations further reduce latency for content delivery to end users."),

    ("HA, DR & Real-World Scenarios",
     "What is the architectural best-practice assumption that drives the decision to use Multi-AZ and Multi-Region designs?",
     ["That AZs and Regions never fail, so redundancy is optional", "That some AZ or Region will eventually fail, so systems must be designed for that possibility", "That AWS guarantees zero downtime by default", "That redundancy is only needed for government workloads"],
     1,
     "Best-practice architecture assumes failure is inevitable at some point - Multi-AZ and Multi-Region designs exist specifically to survive that eventual failure."),

    ("HA, DR & Real-World Scenarios",
     "A single-AZ deployment is best described as having what critical weakness?",
     ["It is too expensive compared to Multi-AZ", "It represents a single point of failure - one data center issue can take the whole app down", "It cannot connect to the internet", "It automatically triggers Multi-Region failover"],
     1,
     "A single-AZ deployment means a fire, flood, or outage in that one data center can take your entire application down - it is a single point of failure."),

    ("HA, DR & Real-World Scenarios",
     "Which term describes an AWS architecture's ability to continue operating even when part of the system (like a Region) fails?",
     ["Elasticity", "Fault tolerance", "Economies of scale", "Vendor lock-in"],
     1,
     "Fault tolerance is the ability of a system to keep functioning correctly even when a component (such as an entire Region) fails."),

    ("HA, DR & Real-World Scenarios",
     "For a workload that only needs protection against a single data center failure (not a full regional disaster), which design is sufficient and most cost-effective?",
     ["Multi-Region deployment across 3 continents", "Multi-AZ deployment within a single Region", "A single Edge Location", "On-premises backup only"],
     1,
     "Multi-AZ within a single Region is sufficient and more cost-effective than full Multi-Region when the concern is only a single data center failure, not a regional disaster."),
]


def _normalize_correct(correct_answer):
    """Return correct answer(s) as a set of indices, and whether it's multi-select."""
    if isinstance(correct_answer, (list, tuple, set)):
        return set(correct_answer), True
    return {correct_answer}, False


def run_quiz():
    print("=" * 70)
    print("AWS CCP (CLF-C02) - MODULE 1: CLOUD FUNDAMENTALS - PRACTICE TEST")
    print(f"Total Questions: {len(QUESTIONS)}")
    print("=" * 70)
    print("\nEXAM MODE: No feedback is shown per question - just like the real exam.")
    print("For single-answer questions, enter one number (e.g. 2).")
    print("For 'Select TWO/THREE' questions, enter comma-separated numbers (e.g. 2,4).")
    print("Type 'q' at any time to quit early and see partial results.\n")
    input("Press Enter to begin...")

    shuffled = QUESTIONS.copy()
    random.shuffle(shuffled)

    total = 0
    correct = 0
    topic_stats = defaultdict(lambda: [0, 0])  # topic -> [correct, total]
    missed = []
    log_lines = []  # for file export

    for i, (topic, q, options, correct_answer, explanation) in enumerate(shuffled, 1):
        correct_set, is_multi = _normalize_correct(correct_answer)
        n_correct = len(correct_set)

        # Shuffle option order so correct answer(s) aren't always in the same position
        correct_texts = {options[idx] for idx in correct_set}
        options = options.copy()
        random.shuffle(options)
        correct_set = {idx for idx, opt in enumerate(options) if opt in correct_texts}

        q_display = q
        if is_multi:
            q_display += f"  (Select {n_correct})"

        print(f"\nQ{i}. {q_display}")
        for idx, opt in enumerate(options, 1):
            print(f"  {idx}. {opt}")

        while True:
            raw = input("Your answer: ").strip().lower()
            if raw == 'q':
                print_results(correct, total, topic_stats, missed, log_lines)
                sys.exit(0)
            parts = [p.strip() for p in raw.split(',') if p.strip()]
            if parts and all(p.isdigit() and 1 <= int(p) <= len(options) for p in parts):
                ans_indices = {int(p) - 1 for p in parts}
                break
            print(f"Invalid input. Enter number(s) 1-{len(options)} (comma-separated if multiple), or 'q' to quit.")

        total += 1
        topic_stats[topic][1] += 1

        your_texts = ", ".join(options[idx] for idx in sorted(ans_indices))
        correct_texts_str = ", ".join(options[idx] for idx in sorted(correct_set))

        print("Answer recorded.")

        if ans_indices == correct_set:
            correct += 1
            topic_stats[topic][0] += 1
            log_lines.append(f"Q{i}. CORRECT\n{q_display}\nYour answer: {your_texts}\n")
        else:
            missed.append((topic, q_display, correct_texts_str, your_texts, explanation))
            log_lines.append(f"Q{i}. INCORRECT\n{q_display}\nYour answer: {your_texts}\nCorrect answer: {correct_texts_str}\nWhy: {explanation}\n")

    print_results(correct, total, topic_stats, missed, log_lines)


def print_results(correct, total, topic_stats, missed, log_lines=None):
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    if total == 0:
        print("No questions answered.")
        return

    pct = (correct / total) * 100
    summary_lines = []
    summary_lines.append(f"AWS CCP (CLF-C02) - {MODULE_NAME} - PRACTICE TEST RESULTS")
    summary_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary_lines.append("=" * 70)
    summary_lines.append(f"Overall Score: {correct}/{total} ({pct:.1f}%)")

    print(f"\nOverall Score: {correct}/{total} ({pct:.1f}%)")

    if pct >= 85:
        verdict = "Verdict: Strong. Module 1 is largely solid - light revision only."
    elif pct >= 70:
        verdict = "Verdict: Decent, but gaps exist. Revisit weak topics below before moving on."
    else:
        verdict = "Verdict: Needs deeper study. Don't move to Module 2 yet."
    print(verdict)
    summary_lines.append(verdict)

    print("\n" + "-" * 70)
    print("TOPIC-WISE BREAKDOWN (sorted weakest first)")
    print("-" * 70)
    summary_lines.append("\n" + "-" * 70)
    summary_lines.append("TOPIC-WISE BREAKDOWN (sorted weakest first)")
    summary_lines.append("-" * 70)

    rows = []
    for topic, (c, t) in topic_stats.items():
        p = (c / t) * 100 if t else 0
        rows.append((p, c, t, topic))
    rows.sort()  # weakest first

    for p, c, t, topic in rows:
        bar_len = int(p / 5)
        bar = "#" * bar_len + "-" * (20 - bar_len)
        flag = "  <-- REVISE" if p < 70 else ""
        line = f"{topic:32s} [{bar}] {c}/{t} ({p:.0f}%){flag}"
        print(line)
        summary_lines.append(line)

    if missed:
        print("\n" + "-" * 70)
        print("MISSED QUESTIONS REVIEW - REVIEW THESE")
        print("-" * 70)
        summary_lines.append("\n" + "-" * 70)
        summary_lines.append("MISSED QUESTIONS REVIEW - REVIEW THESE")
        summary_lines.append("-" * 70)
        for topic, q, correct_ans, your_ans, explanation in missed:
            block = (f"\n{q}\n"
                     f"  Your answer:    {your_ans}\n"
                     f"  Correct answer: {correct_ans}\n"
                     f"  Why: {explanation}")
            print(block)
            summary_lines.append(block)

    print("\n" + "=" * 70)
    print("Any topic below 70% -> go back into the detailed module notes for it.")
    print("Topics at 100% -> safe to skip re-reading, just do a final skim.")
    print("=" * 70)

    filename = f"{MODULE_NAME}-Results.txt"
    try:
        full_report = "\n".join(summary_lines)
        if log_lines:
            full_report += "\n\n" + "-" * 70 + "\nFULL QUESTION LOG (in order answered)\n" + "-" * 70 + "\n\n"
            full_report += "\n".join(log_lines)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_report + "\n")
        print(f"\nResults saved to: {os.path.abspath(filename)}")
    except OSError as e:
        print(f"\nCould not save results file: {e}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted.")
