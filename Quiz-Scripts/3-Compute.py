#!/usr/bin/env python3
"""
AWS CCP (CLF-C02) - Module 3: Compute Services - Practice MCQ Test
====================================================================
Covers: Compute fundamentals, IaaS/PaaS/SaaS, EC2, Serverless, Lambda,
Containers, ECS/EKS, Fargate, ECR, CloudFront (compute-adjacent),
Elastic Beanstalk, AWS Batch, Lightsail, Outposts.

Run:  python3 module3_compute_quiz.py

At the end you get:
  - Overall score
  - Topic-wise breakdown (so you know exactly which topic to re-study)
  - List of missed questions with correct answers (no explanations shown
    during the test itself - pure exam simulation)
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Module3-Compute"

# Each question: (topic, question_text, [options], correct_answer(s), explanation)
# correct_answer(s): a single 0-based int for single-select questions,
#                     OR a list/tuple of 0-based ints for multi-select ("Select TWO/THREE") questions.
QUESTIONS = [
    # ---------------- 1. Compute Fundamentals ----------------
    ("Compute Fundamentals",
     "Which of the following best describes 'compute' in the context of AWS?",
     ["Storage capacity available to an application",
      "The processing power (CPU/RAM) used to run applications and workloads",
      "The network bandwidth allocated to a VPC",
      "The database throughput available to an application"],
     1,
     "Compute refers to the processing resources (CPU, memory) needed to run workloads."),

    ("Compute Fundamentals",
     "A company wants full control over the OS, patching schedule, and underlying configuration of its servers. Which compute model fits best?",
     ["Fully managed PaaS", "IaaS (e.g., EC2)", "SaaS", "Serverless only"],
     1,
     "IaaS (like EC2) gives the customer control over the OS and above."),

    # ---------------- 2. IaaS vs PaaS vs SaaS ----------------
    ("IaaS vs PaaS vs SaaS",
     "Which AWS service is the best example of PaaS?",
     ["Amazon EC2", "AWS Elastic Beanstalk", "Amazon S3", "AWS Direct Connect"],
     1,
     "Elastic Beanstalk manages the underlying infrastructure while you focus on code - classic PaaS."),

    ("IaaS vs PaaS vs SaaS",
     "Gmail and Salesforce are examples of which cloud service model?",
     ["IaaS", "PaaS", "SaaS", "FaaS"],
     2,
     "Fully finished, ready-to-use software delivered over the internet = SaaS."),

    ("IaaS vs PaaS vs SaaS",
     "In the shared responsibility model, which layer does the customer ALWAYS manage, regardless of IaaS, PaaS, or SaaS?",
     ["Physical hardware", "Data and access management", "Hypervisor", "Data center physical security"],
     1,
     "Customer always manages their own data and identity/access controls, no matter the service model."),

    # ---------------- 3. Amazon EC2 ----------------
    ("EC2",
     "Which EC2 pricing model can be interrupted by AWS with a 2-minute warning?",
     ["On-Demand", "Reserved Instances", "Spot Instances", "Savings Plans"],
     2,
     "Spot Instances use spare capacity and can be reclaimed by AWS with a 2-minute notice."),

    ("EC2",
     "You need to run a short, unpredictable workload with no long-term commitment and want to pay only for what you use, at standard rates. Which pricing model fits?",
     ["Reserved Instances", "On-Demand", "Spot Instances", "Dedicated Hosts"],
     1,
     "On-Demand = pay-as-you-go, no commitment, ideal for unpredictable/short workloads."),

    ("EC2",
     "Which EC2 instance type family is optimized for high-performance computing and batch processing requiring heavy CPU power?",
     ["T-family (burstable)", "C-family (compute optimized)", "R-family (memory optimized)", "I-family (storage optimized)"],
     1,
     "C-family = Compute optimized, for CPU-intensive workloads."),

    ("EC2",
     "Which EC2 purchasing option guarantees capacity reservation in a specific Availability Zone for a fee, even without long-term commitment?",
     ["Spot Instance", "On-Demand Capacity Reservation", "Reserved Instance", "Savings Plan"],
     1,
     "On-Demand Capacity Reservations reserve capacity in a specific AZ without requiring a 1 or 3 year term."),

    ("EC2",
     "A financial firm has strict compliance rules stating that no other AWS customer's instance may ever run on the same physical hardware. Which tenancy option satisfies this at the LOWEST cost?",
     ["Default (shared) tenancy", "Dedicated Instance", "Dedicated Host", "Spot Instance"],
     1,
     "Dedicated Instance guarantees no other AWS account shares the hardware, and is cheaper than a Dedicated Host."),

    ("EC2",
     "Which EC2 storage option is EPHEMERAL, meaning data is lost when the instance is stopped or terminated?",
     ["EBS (Elastic Block Store)", "EFS (Elastic File System)", "Instance Store", "S3"],
     2,
     "Instance Store is physically attached, temporary storage - data is lost on stop/terminate."),

    ("EC2",
     "What is the DEFAULT tenancy setting for a newly launched EC2 instance if nothing is specified?",
     ["Dedicated", "Host", "Shared (default)", "Isolated"],
     2,
     "Default tenancy means the instance may share hardware with other AWS accounts (isolated logically, not physically)."),

    # ---------------- 4. Serverless Computing ----------------
    ("Serverless",
     "Which of the following is a TRUE characteristic of serverless computing?",
     ["You must patch the underlying OS",
      "You provision and manage the servers",
      "You are not responsible for managing or provisioning servers",
      "You pay a flat monthly fee regardless of usage"],
     2,
     "Serverless = no server management; AWS handles provisioning, scaling, and patching."),

    ("Serverless",
     "Which billing model is typical of serverless services like Lambda?",
     ["Pay for a fixed reserved capacity always running",
      "Pay only for the compute time actually consumed",
      "Pay a flat annual license fee",
      "Pay based on number of employees using it"],
     1,
     "Serverless typically bills per invocation/execution time - true consumption-based pricing."),

    # ---------------- 5. AWS Lambda ----------------
    ("Lambda",
     "What is the MAXIMUM execution timeout for a single AWS Lambda function invocation?",
     ["5 minutes", "10 minutes", "15 minutes", "30 minutes"],
     2,
     "Lambda has a hard max timeout of 15 minutes (900 seconds), non-negotiable."),

    ("Lambda",
     "What is the DEFAULT timeout for a newly created Lambda function?",
     ["3 seconds", "15 seconds", "1 minute", "15 minutes"],
     0,
     "Default Lambda timeout is 3 seconds - a common trap causing 'mysterious' timeouts."),

    ("Lambda",
     "A workload needs to process a queue of tasks but each task could occasionally run for 25 minutes. Which service should you use INSTEAD of plain Lambda?",
     ["Lambda with increased timeout", "Fargate or EC2/Batch", "Lambda with more memory", "Lambda with provisioned concurrency"],
     1,
     "Since Lambda cannot exceed 15 min under any configuration, long-running tasks need Fargate, EC2, or AWS Batch."),

    ("Lambda",
     "Which AWS service helps orchestrate multiple Lambda functions into a longer, multi-step workflow that can span beyond 15 minutes overall?",
     ["AWS Step Functions", "Amazon EventBridge", "AWS CloudTrail", "Amazon SQS"],
     0,
     "Step Functions chains Lambda invocations into a state machine, letting the overall workflow exceed 15 minutes even though each Lambda step stays under it."),

    ("Lambda",
     "Lambda automatically scales by doing what in response to increased number of incoming requests?",
     ["Increasing the memory of a single execution",
      "Running multiple instances of the function concurrently",
      "Queuing requests until off-peak hours",
      "Requiring manual Auto Scaling Group configuration"],
     1,
     "Lambda scales out by running many concurrent executions automatically - no ASG needed."),

    # ---------------- 6. Containers - Fundamentals ----------------
    ("Containers Fundamentals",
     "What is the KEY difference between a container and a traditional virtual machine?",
     ["Containers include a full guest OS, VMs do not",
      "Containers share the host OS kernel, making them lighter weight than VMs",
      "Containers are always slower to start than VMs",
      "VMs cannot be used on AWS"],
     1,
     "Containers virtualize at the OS level and share the host kernel, making them much lighter and faster to start than VMs."),

    ("Containers Fundamentals",
     "Which file is used to define how a Docker container image should be built?",
     ["docker-compose.yml", "Dockerfile", "task-definition.json", "buildspec.yml"],
     1,
     "A Dockerfile contains the instructions to build a container image."),

    # ---------------- 7. ECS & EKS ----------------
    ("ECS & EKS",
     "What does ECS stand for and what is it?",
     ["Elastic Compute Server - a virtual machine service",
      "Elastic Container Service - AWS's native container orchestration service",
      "Elastic Cluster Storage - a storage service for containers",
      "Enterprise Container System - a third-party tool"],
     1,
     "ECS = Elastic Container Service, AWS's own container orchestrator."),

    ("ECS & EKS",
     "A company already has deep Kubernetes expertise and wants to migrate existing Kubernetes workloads to AWS with minimal changes. Which service fits best?",
     ["Amazon ECS", "Amazon EKS", "AWS Lambda", "AWS Elastic Beanstalk"],
     1,
     "EKS = Elastic Kubernetes Service, AWS's managed Kubernetes offering - ideal for existing K8s workloads."),

    ("ECS & EKS",
     "In ECS, what are the two available launch types for running containers?",
     ["Spot and On-Demand", "EC2 launch type and Fargate launch type", "Reserved and Dedicated", "Standard and Convertible"],
     1,
     "ECS containers can run on self-managed EC2 instances (EC2 launch type) or serverless via Fargate."),

    # ---------------- 8. Fargate ----------------
    ("Fargate",
     "What is the primary benefit of AWS Fargate over the EC2 launch type for ECS/EKS?",
     ["Cheaper for all workloads",
      "You no longer need to provision or manage the underlying EC2 servers",
      "It only works with Windows containers",
      "It provides GPU acceleration by default"],
     1,
     "Fargate is serverless compute for containers - no EC2 instances to manage or patch."),

    ("Fargate",
     "Fargate can be used with which two AWS container orchestration services?",
     ["ECS and EKS", "ECS and Lambda", "EKS and Elastic Beanstalk", "ECR and Lightsail"],
     0,
     "Fargate is a compute engine usable with both ECS and EKS."),

    # ---------------- 9. ECR ----------------
    ("ECR",
     "What is Amazon ECR primarily used for?",
     ["Running containers directly",
      "A fully managed Docker container image registry to store, manage, and deploy container images",
      "Monitoring container health",
      "Orchestrating container scaling"],
     1,
     "ECR = Elastic Container Registry, for storing and managing container images (similar to Docker Hub)."),

    ("ECR",
     "Which of these integrates natively with ECR to pull container images for deployment?",
     ["Amazon RDS", "ECS and EKS", "AWS Direct Connect", "Amazon Route 53"],
     1,
     "ECS and EKS pull container images directly from ECR during deployment."),

    # ---------------- 10. Edge Locations & CloudFront ----------------
    ("Edge & CloudFront",
     "What is the primary purpose of Amazon CloudFront?",
     ["Running serverless compute functions",
      "A Content Delivery Network (CDN) that caches content at edge locations closer to users",
      "Managing container orchestration",
      "Providing dedicated physical servers"],
     1,
     "CloudFront is AWS's CDN, caching content at edge locations to reduce latency."),

    ("Edge & CloudFront",
     "What are 'Edge Locations' in AWS's global infrastructure?",
     ["Backup AWS Regions", "Sites used only for AWS internal operations",
      "Sites closer to end users used to cache content and reduce latency (e.g., for CloudFront)",
      "Locations where EC2 Dedicated Hosts are stored"],
     2,
     "Edge locations are geographically distributed sites that cache content for services like CloudFront to reduce latency."),

    ("Edge & CloudFront",
     "Which AWS service lets you run lightweight compute code AT the edge location, closer to the end user, alongside CloudFront?",
     ["AWS Lambda@Edge", "AWS Fargate", "Amazon EKS", "AWS Batch"],
     0,
     "Lambda@Edge lets you run Lambda functions at CloudFront edge locations for low-latency processing."),

    # ---------------- 11. Elastic Beanstalk ----------------
    ("Elastic Beanstalk",
     "What is AWS Elastic Beanstalk?",
     ["A container registry", "A PaaS offering that automatically handles deployment, capacity provisioning, load balancing, and scaling for your application code",
      "A pure IaaS virtual machine service", "A database migration tool"],
     1,
     "Elastic Beanstalk is AWS's PaaS - you upload code, it handles the infrastructure."),

    ("Elastic Beanstalk",
     "With Elastic Beanstalk, who retains access to the underlying resources (EC2, ELB, ASG) it provisions?",
     ["No one - it's a black box", "The customer still has full access to the underlying resources if needed", "Only AWS support", "Only third-party partners"],
     1,
     "Even though EB automates provisioning, customers retain access/control over the underlying resources it creates."),

    # ---------------- 12. AWS Batch ----------------
    ("AWS Batch",
     "What is AWS Batch designed for?",
     ["Real-time interactive web applications",
      "Efficiently running hundreds/thousands of batch computing jobs, automatically provisioning the optimal compute resources",
      "Hosting static websites",
      "Managing DNS routing"],
     1,
     "AWS Batch dynamically provisions the right amount/type of compute for batch jobs, then scales down when done."),

    ("AWS Batch",
     "AWS Batch runs its jobs using which underlying compute options?",
     ["Only Lambda", "EC2 and Fargate", "Only Lightsail", "Only Dedicated Hosts"],
     1,
     "AWS Batch can run jobs on EC2 (including Spot) or Fargate under the hood."),

    # ---------------- 13. Lightsail ----------------
    ("Lightsail",
     "Amazon Lightsail is best suited for which type of use case?",
     ["Enterprise-scale, complex multi-tier architectures",
      "Simple, low-cost, easy-to-launch virtual private servers for simple web apps, blogs, or small projects",
      "High-performance computing clusters",
      "Managed Kubernetes at scale"],
     1,
     "Lightsail is AWS's simplified VPS offering aimed at simple workloads and beginners, with predictable flat pricing."),

    ("Lightsail",
     "Which of these is a KEY selling point of Lightsail pricing?",
     ["Pay strictly per second with no predictability", "Simple, predictable flat monthly pricing bundling compute, storage, and data transfer", "Free forever with no limits", "Billed only in Reserved Instance terms"],
     1,
     "Lightsail offers bundled, flat-rate monthly pricing - simple and predictable, unlike granular EC2 billing."),

    # ---------------- 14. Outposts ----------------
    ("Outposts",
     "What does AWS Outposts provide?",
     ["A fully virtual, cloud-only compute service",
      "Physical AWS-managed hardware racks installed in the customer's own on-premises data center, extending AWS infrastructure and services on-prem",
      "A discount program for long-term EC2 commitments",
      "A container registry service"],
     1,
     "Outposts brings actual AWS hardware into your on-prem data center for a consistent hybrid experience."),

    ("Outposts",
     "A hospital needs extremely low-latency access to patient data processed locally due to regulatory and latency requirements, but still wants a consistent AWS experience/APIs. Which service fits best?",
     ["AWS Lightsail", "AWS Outposts", "Amazon EKS", "AWS Elastic Beanstalk"],
     1,
     "Outposts is designed exactly for low-latency, on-premises, data-residency-sensitive workloads while staying on AWS's control plane."),

    # ---------------- Comparison / Decision Tree style ----------------
    ("Comparison & Decision-Making",
     "A startup wants to deploy a web app quickly without managing servers, load balancers, or scaling policies manually, but still wants access to underlying resources if needed later. Which service is the BEST fit?",
     ["Amazon EC2", "AWS Elastic Beanstalk", "AWS Outposts", "Amazon Lightsail"],
     1,
     "Elastic Beanstalk automates deployment/scaling (PaaS) while still exposing the underlying resources - best fit for 'quick deploy but flexible later.'"),

    ("Comparison & Decision-Making",
     "A media company needs to run thousands of short-lived video transcoding batch jobs efficiently, provisioning the right compute automatically. Which service is BEST?",
     ["AWS Batch", "AWS Lambda", "Amazon Lightsail", "AWS Outposts"],
     0,
     "AWS Batch is purpose-built for large-scale batch job processing with automatic compute provisioning."),

    ("Comparison & Decision-Making",
     "A company wants to run containers without managing any EC2 instances at all, while keeping full Kubernetes API compatibility. Which combination fits?",
     ["ECS with EC2 launch type", "EKS with Fargate", "Lightsail with Docker", "Lambda with containers only"],
     1,
     "EKS gives Kubernetes compatibility; pairing it with Fargate removes the need to manage EC2 instances."),

    ("Comparison & Decision-Making",
     "Which compute service should you choose if your application code needs to run only in response to specific events (e.g., a file upload to S3), for a few seconds at a time?",
     ["EC2", "AWS Lambda", "AWS Outposts", "Amazon Lightsail"],
     1,
     "Event-driven, short-duration execution is the classic Lambda use case."),

    ("Comparison & Decision-Making",
     "Which of the following compute options does NOT require you to manage or patch an underlying operating system?",
     ["EC2 Reserved Instance", "EC2 Dedicated Host", "AWS Lambda", "EC2 Spot Instance"],
     2,
     "Lambda is serverless - AWS manages the OS entirely. All EC2 options require customer OS management."),

    ("Comparison & Decision-Making",
     "For a workload requiring GPU-based per-socket licensed software that must run on isolated, visible physical hardware, which is the correct compute + tenancy choice?",
     ["Lambda", "EC2 with Dedicated Host tenancy", "Fargate", "Lightsail"],
     1,
     "Per-socket/core licensing (BYOL) combined with hardware visibility requirements = EC2 Dedicated Host."),

    ("Comparison & Decision-Making",
     "Which pair correctly matches 'orchestration service' to 'AWS-native vs open-source standard'?",
     ["ECS = open-source standard, EKS = AWS-native", "ECS = AWS-native, EKS = open-source Kubernetes standard", "Both ECS and EKS are open-source", "Both ECS and EKS are AWS-native only"],
     1,
     "ECS is AWS's proprietary orchestrator; EKS is AWS's managed version of the open-source Kubernetes standard."),

    ("Comparison & Decision-Making",
     "A question describes a workload that must scale to zero when idle and only be billed when actively processing HTTP requests, with no infrastructure management. Which combo best fits (ignoring cost optimization nuances)?",
     ["EC2 On-Demand", "Lambda (possibly behind API Gateway)", "Lightsail", "Dedicated Host"],
     1,
     "'Scale to zero + billed only when active + zero infra management' is the signature description of Lambda."),

    ("Comparison & Decision-Making",
     "Which service would you pick for a simple WordPress blog with predictable low traffic and a desire for the SIMPLEST possible setup and flat billing?",
     ["Amazon EC2 with manual Auto Scaling", "Amazon Lightsail", "Amazon EKS", "AWS Outposts"],
     1,
     "Lightsail is explicitly designed for simple, low-traffic workloads like blogs, with flat predictable pricing."),

    ("Comparison & Decision-Making",
     "True or False: Both AWS Fargate and AWS Lambda are considered 'serverless' compute options.",
     ["True", "False"],
     0,
     "Both remove the need to provision/manage servers - Fargate for containers, Lambda for functions."),
]

def _normalize_correct(correct_answer):
    """Return correct answer(s) as a set of indices, and whether it's multi-select."""
    if isinstance(correct_answer, (list, tuple, set)):
        return set(correct_answer), True
    return {correct_answer}, False


def run_quiz():
    print("=" * 70)
    print("AWS CCP (CLF-C02) - MODULE 3: COMPUTE SERVICES - PRACTICE TEST")
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
        verdict = "Verdict: Strong. Module 3 is largely solid - light revision only."
    elif pct >= 70:
        verdict = "Verdict: Decent, but gaps exist. Revisit weak topics below before moving on."
    else:
        verdict = "Verdict: Needs deeper study. Don't move to Module 4 yet."
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
        line = f"{topic:28s} [{bar}] {c}/{t} ({p:.0f}%){flag}"
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
