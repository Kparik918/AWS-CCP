#!/usr/bin/env python3
"""
AWS CCP (CLF-C02) - Module: Global Infrastructure & CloudFormation - Practice MCQ Test
=========================================================================================
Covers: Global Infrastructure big picture, Regions, Availability Zones, Data Centers,
Edge Locations & the global network service family (CloudFront, Route 53, Global
Accelerator, Local Zones, Wavelength), and AWS CloudFormation (IaC).

Run:  python3 global_infra_cfn_quiz.py

At the end you get:
  - Overall score
  - Topic-wise breakdown (so you know exactly which topic to re-study)
  - List of missed questions with correct answers and explanations
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "GlobalInfra-CloudFormation"

# Each question: (topic, question_text, [options], correct_answer(s), explanation)
# correct_answer(s): a single 0-based int for single-select questions,
#                     OR a list/tuple of 0-based ints for multi-select ("Select TWO/THREE") questions.
QUESTIONS = [
    # ---------------- 1. Global Infrastructure - Big Picture ----------------
    ("Global Infrastructure Overview",
     "What is the correct hierarchy of AWS's global infrastructure, from largest to smallest?",
     ["Availability Zone > Region > Data Center", "Region > Availability Zone > Data Center",
      "Data Center > Region > Availability Zone", "Edge Location > Region > Availability Zone"],
     1,
     "Region (largest, geographic area) contains multiple AZs, each AZ contains one or more Data Centers."),

    ("Global Infrastructure Overview",
     "Why does AWS build its infrastructure across multiple geographically separate Regions rather than one giant Region?",
     ["To make pricing more complex", "To provide fault tolerance, low latency to users worldwide, and to meet data residency/compliance requirements",
      "Because a single Region cannot legally host more than 3 AZs", "To force customers into Reserved Instances"],
     1,
     "Multiple regions = disaster isolation, lower latency to global users, and compliance/data sovereignty options."),

    # ---------------- 2. Regions - Deep Dive ----------------
    ("Regions",
     "Which statement about AWS Regions is TRUE?",
     ["All AWS services are available in every Region", "Not all AWS services are available in every Region - availability varies by Region",
      "A Region contains exactly one Availability Zone", "Regions share the same physical power and networking infrastructure"],
     1,
     "Newer/specialized services often roll out to major Regions first; not every service is in every Region."),

    ("Regions",
     "A company must keep all customer data physically within Germany due to legal/regulatory requirements. Which AWS concept directly addresses this?",
     ["Choosing an appropriate AWS Region", "Choosing more Availability Zones", "Using more Edge Locations", "Using a Dedicated Host"],
     0,
     "Region selection is how you control the physical/geographic location of your data for compliance/data residency."),

    ("Regions",
     "What is a key factor businesses consider when choosing which AWS Region to deploy into?",
     ["The color scheme of the AWS Console in that Region", "Compliance/data residency, latency to end users, service availability, and cost",
      "The number of Availability Zones must always be exactly 6", "Only the price of S3 storage"],
     1,
     "Region selection criteria: compliance, latency, feature/service availability, and pricing differences."),

    ("Regions",
     "How many Availability Zones does an AWS Region contain AT MINIMUM (per AWS's stated design)?",
     ["1", "2", "3", "5"],
     1,
     "AWS regions are designed with a minimum of 2 (though most now have 3+) AZs for redundancy."),

    # ---------------- 3. Availability Zones ----------------
    ("Availability Zones",
     "What is an Availability Zone (AZ)?",
     ["A single server rack", "One or more discrete data centers with redundant power, networking, and connectivity, isolated from failures in other AZs within the same Region",
      "A synonym for a Region", "A CDN caching location"],
     1,
     "An AZ = one or more physically isolated data centers, engineered to be independent of failures in other AZs."),

    ("Availability Zones",
     "Why do AWS best practices recommend deploying an application across MULTIPLE Availability Zones?",
     ["To reduce the total AWS bill automatically", "To achieve high availability and fault tolerance - if one AZ fails, others continue serving traffic",
      "Because a single AZ cannot host an EC2 instance", "It is legally mandated worldwide"],
     1,
     "Multi-AZ deployment is the core pattern for high availability - isolates the blast radius of a single AZ failure."),

    ("Availability Zones",
     "AZs within the same Region are connected via what kind of network links?",
     ["Public internet only", "High-bandwidth, low-latency private links between AZs", "Satellite links", "No direct connection exists between AZs"],
     1,
     "AZs are interconnected with high-speed, low-latency, redundant private fiber links."),

    ("Availability Zones",
     "How are Availability Zones typically named/identified?",
     ["By a random UUID", "By the Region code plus a letter, e.g., us-east-1a, us-east-1b", "By city name only", "By a numeric IP range"],
     1,
     "AZs are named as Region code + letter suffix, e.g., us-east-1a, us-east-1b, us-east-1c."),

    # ---------------- 4. Data Centers ----------------
    ("Data Centers",
     "What makes up an Availability Zone at the physical level?",
     ["One or more physical data centers", "A single virtual machine", "A CloudFront edge node", "A Region boundary"],
     0,
     "An AZ is composed of one or more physical, discrete data centers."),

    ("Data Centers",
     "Which of these is a design goal for AWS data centers within an AZ?",
     ["Sharing power and cooling with data centers in other AZs to reduce cost",
      "Redundant power, networking, and cooling to minimize the risk of a single point of failure",
      "Being located in exactly the same building as all other Regions' data centers",
      "Requiring manual failover by the customer during any outage"],
     1,
     "AWS data centers are built with redundancy in power, cooling, and networking to avoid single points of failure."),

    # ---------------- 5. Edge Locations & Global Network Service Family ----------------
    ("Edge Locations & Global Network",
     "What is the primary purpose of AWS Edge Locations?",
     ["To run full EC2 workloads at reduced cost", "To cache content and provide services (like CloudFront and Route 53) closer to end users, reducing latency",
      "To act as backup Availability Zones", "To store long-term backups of RDS databases"],
     1,
     "Edge locations exist to bring content/services physically closer to end users for lower latency - primarily via CloudFront."),

    ("Edge Locations & Global Network",
     "There are significantly MORE Edge Locations worldwide than there are AWS Regions. Why?",
     ["Edge Locations require far less infrastructure and are meant to be widely distributed close to users, unlike full Regions",
      "Edge Locations replaced Regions entirely", "It's a marketing statistic with no technical reason", "Regions were discontinued in favor of Edge Locations"],
     0,
     "Edge locations are lightweight caching/delivery points, so AWS can deploy far more of them than full Regions."),

    ("Edge Locations & Global Network",
     "Which AWS service is a highly available and scalable Domain Name System (DNS) web service?",
     ["Amazon CloudFront", "Amazon Route 53", "AWS Global Accelerator", "AWS Direct Connect"],
     1,
     "Route 53 is AWS's DNS service, also offering domain registration and health checking/routing policies."),

    ("Edge Locations & Global Network",
     "Which service improves the availability and performance of applications by routing traffic through AWS's global network infrastructure using static Anycast IP addresses, rather than caching content?",
     ["Amazon CloudFront", "AWS Global Accelerator", "Amazon Route 53", "AWS Outposts"],
     1,
     "Global Accelerator routes traffic over AWS's private backbone network using static IPs - improves performance for non-cacheable/dynamic traffic, unlike CloudFront which caches content."),

    ("Edge Locations & Global Network",
     "What is the key difference between CloudFront and Global Accelerator?",
     ["CloudFront is for DNS, Global Accelerator is for CDN caching",
      "CloudFront caches static/dynamic content at edge locations; Global Accelerator optimizes routing of (often non-cacheable) traffic over AWS's backbone using static IPs",
      "They are identical services with different names", "Global Accelerator only works within a single Availability Zone"],
     1,
     "CloudFront = content caching/CDN. Global Accelerator = network-level routing optimization, useful for TCP/UDP traffic, gaming, VoIP, non-HTTP use cases."),

    ("Edge Locations & Global Network",
     "AWS Local Zones and AWS Wavelength Zones both extend AWS infrastructure closer to users. What is the key distinguishing feature of Wavelength Zones specifically?",
     ["They are embedded within telecommunications providers' 5G networks for ultra-low-latency mobile/edge applications",
      "They are located inside customer data centers", "They only support S3 storage", "They replace the need for Regions entirely"],
     0,
     "AWS Wavelength embeds AWS compute/storage inside telecom providers' 5G networks, targeting ultra-low-latency mobile edge use cases."),

    ("Edge Locations & Global Network",
     "Which of the following is NOT part of AWS's edge/global network service family?",
     ["Amazon CloudFront", "AWS Global Accelerator", "Amazon Route 53", "Amazon RDS Multi-AZ"],
     3,
     "RDS Multi-AZ is a database high-availability feature, not part of the edge/global network service family."),

    # ---------------- 6. AWS CloudFormation ----------------
    ("CloudFormation",
     "What is AWS CloudFormation?",
     ["A monitoring and alerting service", "AWS's native Infrastructure as Code (IaC) service used to model and provision AWS resources using templates",
      "A container orchestration service", "A billing and cost management tool"],
     1,
     "CloudFormation lets you define AWS infrastructure as code (JSON/YAML templates) and provision it repeatably."),

    ("CloudFormation",
     "In which file formats can a CloudFormation template be written?",
     ["Only XML", "JSON or YAML", "Only proprietary AWS binary format", "HCL only"],
     1,
     "CloudFormation templates are written in JSON or YAML (HCL is Terraform's language, not CloudFormation's)."),

    ("CloudFormation",
     "What is the correct AWS terminology for the actual set of resources that gets created when a CloudFormation template is deployed?",
     ["A Template", "A Stack", "A Fleet", "A Blueprint"],
     1,
     "When you deploy a CloudFormation template, the resulting collection of provisioned resources is called a Stack."),

    ("CloudFormation",
     "How much does AWS charge for using the CloudFormation service itself (excluding the cost of resources it provisions)?",
     ["A flat monthly fee", "A per-template licensing fee", "CloudFormation itself is free - you only pay for the underlying AWS resources it creates",
      "A percentage of your total AWS bill"],
     2,
     "CloudFormation is a free service; charges only apply to the actual resources (EC2, RDS, etc.) it provisions."),

    ("CloudFormation",
     "What happens to the resources in a CloudFormation Stack if you delete the Stack?",
     ["Nothing happens - resources remain untouched forever", "By default, CloudFormation automatically deletes all resources it created as part of that stack",
      "Only EC2 instances are deleted, all other resources remain", "The stack cannot be deleted once created"],
     1,
     "Deleting a Stack, by default, tears down all resources CloudFormation created for it - a key benefit for clean environment teardown."),

    ("CloudFormation",
     "What is the main benefit of using CloudFormation instead of manually creating resources through the AWS Console?",
     ["It's the only way to create an S3 bucket", "Consistent, repeatable, version-controllable infrastructure that can be redeployed identically across environments/regions",
      "It removes the need for an AWS account", "It bypasses IAM permissions entirely"],
     1,
     "IaC's core value: consistency, repeatability, version control, and eliminating manual configuration drift."),

    ("CloudFormation",
     "Which AWS tool lets developers define CloudFormation templates using familiar programming languages (Python, TypeScript, Java) instead of raw JSON/YAML?",
     ["AWS CDK (Cloud Development Kit)", "AWS SAM only", "AWS Config", "AWS Systems Manager"],
     0,
     "AWS CDK lets you write infrastructure in real programming languages, which then synthesizes into CloudFormation templates under the hood."),

    ("CloudFormation",
     "CloudFormation is best described as AWS's native alternative to which widely used third-party tool?",
     ["Jenkins", "Terraform", "Docker", "Ansible for configuration management only"],
     1,
     "Terraform is the most common third-party/multi-cloud IaC tool that CloudFormation is directly compared to."),

    ("CloudFormation",
     "A company needs to provision the EXACT SAME set of AWS resources (VPC, EC2, RDS, security groups) consistently across dev, staging, and production environments. What is the BEST solution?",
     ["Manually recreate resources in the Console for each environment", "Use a CloudFormation template and deploy it as a separate Stack per environment",
      "Use only IAM policies", "Use Amazon Lightsail for consistency"],
     1,
     "This is the textbook CloudFormation use case - one template, deployed repeatably and consistently as distinct stacks."),

    # ---------------- Comparison / Decision Tree style ----------------
    ("Comparison & Decision-Making",
     "A gaming company needs to reduce latency for real-time UDP traffic between players across the globe, where content caching (like CloudFront) doesn't apply. Which service fits best?",
     ["Amazon CloudFront", "AWS Global Accelerator", "Amazon Route 53", "AWS Outposts"],
     1,
     "Global Accelerator optimizes routing for non-cacheable, latency-sensitive traffic like UDP/TCP gaming traffic over AWS's backbone."),

    ("Comparison & Decision-Making",
     "A media streaming company wants to cache video content close to viewers worldwide to reduce buffering and latency. Which service is the correct choice?",
     ["Amazon Route 53", "Amazon CloudFront", "AWS Global Accelerator", "AWS CloudFormation"],
     1,
     "CloudFront is the CDN purpose-built for caching content (video, images, static assets) at edge locations."),

    ("Comparison & Decision-Making",
     "Which AWS global infrastructure concept would a company reference when explaining they deployed their application redundantly to survive the failure of an entire data center cluster within one geographic area?",
     ["Multiple Regions", "Multiple Availability Zones within a single Region", "Multiple Edge Locations", "A single Dedicated Host"],
     1,
     "Multi-AZ deployment specifically protects against failure of one data center cluster (an AZ) within a Region."),

    ("Comparison & Decision-Making",
     "A company wants to serve users with extremely low latency across two entirely different continents (e.g., disaster recovery across geography, not just within one area). What should they use?",
     ["Multiple Availability Zones only", "Multiple Regions", "A single Edge Location", "A single Dedicated Host"],
     1,
     "Cross-continent redundancy/low latency requires deploying to multiple Regions - AZs alone stay within one Region's geography."),

    ("Comparison & Decision-Making",
     "Which pairing correctly matches the service with its PRIMARY function?",
     ["Route 53 = CDN caching, CloudFront = DNS routing", "Route 53 = DNS, CloudFront = CDN/content caching",
      "Global Accelerator = DNS, Route 53 = CDN caching", "CloudFormation = DNS, Route 53 = Infrastructure as Code"],
     1,
     "Route 53 = DNS and domain services. CloudFront = CDN for caching content at the edge. Don't mix these up."),

    ("Comparison & Decision-Making",
     "True or False: An Availability Zone can span multiple Regions.",
     ["True", "False"],
     1,
     "False - an AZ always belongs to exactly one Region; it never spans across Regions."),

    ("Comparison & Decision-Making",
     "Which of these is the correct order of increasing geographic/architectural scope, from smallest to largest?",
     ["Data Center < Availability Zone < Region < Edge Location network", "Data Center < Availability Zone < Region",
      "Region < Availability Zone < Data Center", "Availability Zone < Data Center < Region"],
     1,
     "Data Center (smallest physical unit) < Availability Zone (one or more data centers) < Region (multiple AZs)."),

    ("Comparison & Decision-Making",
     "A question describes needing infrastructure to be 'version-controlled, repeatable, and automatically torn down cleanly after a test environment is no longer needed.' Which AWS service/concept is being described?",
     ["Amazon CloudFront", "AWS CloudFormation (Stacks)", "AWS Global Accelerator", "Multiple Availability Zones"],
     1,
     "Repeatable, version-controlled infra with clean teardown = CloudFormation Stacks, which can be deleted to remove all their resources."),

    ("Comparison & Decision-Making",
     "For ultra-low-latency mobile applications that need compute embedded directly within a telecom provider's 5G network, which AWS infrastructure offering is correct?",
     ["AWS Local Zones", "AWS Wavelength", "Amazon CloudFront", "AWS Outposts"],
     1,
     "AWS Wavelength is specifically embedded in telco 5G networks for ultra-low-latency mobile edge compute - Local Zones are metro-area extensions, not telco-embedded."),

    ("Comparison & Decision-Making",
     "What is the key difference between AWS Local Zones and standard AWS Regions?",
     ["Local Zones are a smaller extension of a parent Region placed closer to large population/industry centers, offering a subset of services with low latency, rather than being a full independent Region",
      "Local Zones and Regions are identical in every way", "Local Zones only support S3", "Local Zones replace the need for Availability Zones"],
     0,
     "Local Zones extend a 'parent' Region closer to end users in specific metro areas, offering select services (often compute/storage) for latency-sensitive workloads, without being full independent Regions."),
]

def _normalize_correct(correct_answer):
    """Return correct answer(s) as a set of indices, and whether it's multi-select."""
    if isinstance(correct_answer, (list, tuple, set)):
        return set(correct_answer), True
    return {correct_answer}, False


def run_quiz():
    print("=" * 70)
    print("AWS CCP (CLF-C02) - GLOBAL INFRASTRUCTURE & CLOUDFORMATION - PRACTICE TEST")
    print(f"Total Questions: {len(QUESTIONS)}")
    print("=" * 70)
    print("\nFor single-answer questions, enter one number (e.g. 2).")
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

        print(f"\nQ{i}. [{topic}]")
        print(q_display)
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

        if ans_indices == correct_set:
            correct += 1
            topic_stats[topic][0] += 1
            print("Correct.")
            log_lines.append(f"Q{i}. [{topic}] CORRECT\n{q_display}\nYour answer: {your_texts}\n")
        else:
            print(f"Incorrect. Correct answer: {correct_texts_str}")
            missed.append((topic, q_display, correct_texts_str, your_texts, explanation))
            log_lines.append(f"Q{i}. [{topic}] INCORRECT\n{q_display}\nYour answer: {your_texts}\nCorrect answer: {correct_texts_str}\nWhy: {explanation}\n")

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
        verdict = "Verdict: Strong. This module is largely solid - light revision only."
    elif pct >= 70:
        verdict = "Verdict: Decent, but gaps exist. Revisit weak topics below before moving on."
    else:
        verdict = "Verdict: Needs deeper study. Don't move to the next module yet."
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
        line = f"{topic:30s} [{bar}] {c}/{t} ({p:.0f}%){flag}"
        print(line)
        summary_lines.append(line)

    if missed:
        print("\n" + "-" * 70)
        print("MISSED QUESTIONS - REVIEW THESE")
        print("-" * 70)
        summary_lines.append("\n" + "-" * 70)
        summary_lines.append("MISSED QUESTIONS - REVIEW THESE")
        summary_lines.append("-" * 70)
        for topic, q, correct_ans, your_ans, explanation in missed:
            block = (f"\n[{topic}] {q}\n"
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
