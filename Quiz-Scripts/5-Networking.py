#!/usr/bin/env python3
"""
AWS CCP (CLF-C02) - MODULE 5: NETWORKING - Practice MCQ Test
================================================================
Covers: AWS Global Infrastructure (Region/AZ/Edge recap), VPC Fundamentals,
Subnets & Routing, Connectivity Services (IGW, NAT, VPN, Direct Connect,
Client VPN, PrivateLink), Multi-VPC & Hybrid Networking (Peering, Transit
Gateway), Network Security (Security Groups, NACLs), Content Delivery & DNS
(CloudFront, Route 53), API Gateway, and CloudFormation.

Run:  python3 module5_networking_quiz.py

At the end you get:
  - Overall score
  - Topic-wise breakdown (weakest first, flags anything under 70%)
  - List of missed questions with correct answers and explanations
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Module5-Networking"

# Each question: (topic, question_text, [options], correct_answer(s), explanation)
# correct_answer(s): a single 0-based int for single-select questions,
#                     OR a list/tuple of 0-based ints for multi-select ("Select TWO/THREE") questions.
QUESTIONS = [
    # ---------------- Global Infrastructure recap ----------------
    ("Global Infrastructure",
     "What is the correct priority order AWS expects when choosing a Region to deploy into?",
     ["Cost > Features > Latency > Compliance", "Compliance > Latency > Feature Availability > Cost",
      "Latency > Cost > Compliance > Features", "Features > Compliance > Cost > Latency"],
     1,
     "Compliance always wins first, even over cost - a core CCP exam trap."),

    ("Global Infrastructure",
     "A question describes needing High Availability so that an application survives the failure of an entire data center. What is the correct solution?",
     ["Deploy to multiple Regions", "Deploy across multiple Availability Zones within one Region",
      "Deploy to multiple Edge Locations", "Use a single large EC2 instance"],
     1,
     "HA = multi-AZ within a Region. Multi-Region is for disaster recovery/global reach, not standard HA."),

    ("Global Infrastructure",
     "Can you launch an EC2 instance or RDS database directly inside an Edge Location?",
     ["Yes, always", "No - Edge Locations are for caching/content delivery only, not full compute/storage deployment",
      "Only for RDS, not EC2", "Only if using Fargate"],
     1,
     "Edge Locations are lightweight caching/network points (CloudFront, Route 53, Global Accelerator) - not a compute deployment target."),

    # ---------------- VPC Fundamentals ----------------
    ("VPC Fundamentals",
     "What is a VPC?",
     ["A physical data center owned by the customer", "A logically isolated section of the AWS Cloud where you control IPs, subnets, routing, and gateways",
      "A type of EC2 instance", "A DNS routing service"],
     1,
     "VPC = Virtual Private Cloud, your own isolated network within AWS with full control over its design."),

    ("VPC Fundamentals",
     "A VPC lives in how many Regions and spans how many Availability Zones?",
     ["Multiple Regions, one AZ", "Exactly one Region, but can span all AZs within that Region",
      "Exactly one Region, exactly one AZ", "Multiple Regions, multiple AZs"],
     1,
     "A VPC is confined to a single Region, but can span multiple/all AZs within that Region."),

    ("VPC Fundamentals",
     "What does every new AWS account automatically get, per Region?",
     ["A default Transit Gateway", "A default VPC", "A default Direct Connect link", "A default NAT Instance"],
     1,
     "AWS automatically provisions a default VPC in every Region for a new account, though real architectures typically use custom VPCs."),

    # ---------------- Subnets & Routing ----------------
    ("Subnets & Routing",
     "How many Availability Zones can a single subnet span?",
     ["Exactly one - a subnet is always confined to a single AZ", "Up to 3", "As many as the VPC has", "It depends on the subnet size"],
     0,
     "A subnet always lives in exactly one AZ and can never span multiple AZs."),

    ("Subnets & Routing",
     "What determines whether a subnet is 'public' or 'private'?",
     ["The subnet's name in the console", "Whether its route table has a route to an Internet Gateway (0.0.0.0/0 -> IGW)",
      "The instance type launched inside it", "Whether it has an Elastic IP assigned to the VPC"],
     1,
     "A subnet is public specifically because its route table routes internet-bound traffic to an IGW - not because of naming or instance type."),

    ("Subnets & Routing",
     "Where should a production RDS database typically be placed?",
     ["Public subnet, for easy access", "Private subnet, reachable only by the app tier",
      "Directly in an Edge Location", "Outside of any VPC"],
     1,
     "Databases should sit in private subnets, hidden from direct internet access, reachable only through the application tier."),

    # ---------------- Connectivity Services ----------------
    ("Internet Gateway",
     "What are the required components for a resource in a VPC to actually be reachable from the internet?",
     ["Only an Internet Gateway attached to the VPC", "IGW attached + route table entry to the IGW + the resource has a public/Elastic IP - all three together",
      "Only a public IP address", "Only a Security Group allowing traffic"],
     1,
     "Reachability requires all three together: IGW attached, a route to it, and a public IP on the resource."),

    ("Internet Gateway",
     "Is the Internet Gateway bidirectional or outbound-only?",
     ["Outbound-only", "Bidirectional - supports both inbound and outbound traffic", "Inbound-only", "Neither - it only handles DNS"],
     1,
     "IGW allows traffic to flow both into and out of the VPC, unlike NAT Gateway which is outbound-only."),

    ("NAT Gateway",
     "What is the primary purpose of a NAT Gateway?",
     ["Allow resources in a private subnet to initiate outbound internet connections while blocking unsolicited inbound connections",
      "Provide full bidirectional internet access to a private subnet",
      "Act as a firewall at the subnet level",
      "Cache content close to end users"],
     0,
     "NAT Gateway enables outbound-only internet access for private subnet resources - e.g., fetching patches - while blocking inbound-initiated traffic."),

    ("NAT Gateway",
     "Where must a NAT Gateway be deployed?",
     ["In the private subnet it serves", "In a public subnet, so it can reach the Internet Gateway", "Outside the VPC entirely", "In an Edge Location"],
     1,
     "NAT Gateway sits in a public subnet (with its own route to the IGW) so it can relay traffic on behalf of private subnet resources."),

    ("NAT Gateway",
     "Which is the AWS-recommended, fully managed option for outbound-only internet access from a private subnet - versus the legacy, self-managed option?",
     ["NAT Gateway is recommended; NAT Instance is legacy", "NAT Instance is recommended; NAT Gateway is legacy",
      "Both are equally recommended", "Neither - use an Internet Gateway for private subnets"],
     0,
     "NAT Gateway is AWS-managed with built-in HA and up to 100 Gbps; NAT Instance is a self-managed legacy EC2-based approach."),

    ("Site-to-Site VPN vs Direct Connect",
     "Which connectivity option provides an encrypted IPsec tunnel over the PUBLIC internet between on-premises and AWS?",
     ["AWS Direct Connect", "AWS Site-to-Site VPN", "AWS PrivateLink", "AWS Transit Gateway"],
     1,
     "Site-to-Site VPN = encrypted tunnel over the public internet; Direct Connect bypasses the public internet entirely."),

    ("Site-to-Site VPN vs Direct Connect",
     "A company needs 10 Gbps dedicated bandwidth, predictable low latency, and data that never touches the public internet. Budget is not a constraint, and they can wait a few months for setup. What should they use?",
     ["Site-to-Site VPN", "AWS Direct Connect", "AWS Client VPN", "NAT Gateway"],
     1,
     "High bandwidth + predictable performance + private path + budget available + time to wait = Direct Connect."),

    ("Site-to-Site VPN vs Direct Connect",
     "Roughly how long does it typically take to provision AWS Direct Connect?",
     ["Minutes", "Hours to days", "1 to 3 months", "1 year or more"],
     2,
     "Direct Connect requires physical fiber provisioning through a partner, typically taking 1-3 months - never the answer for urgent needs."),

    ("Site-to-Site VPN vs Direct Connect",
     "A small budget-conscious office needs hybrid connectivity to AWS quickly, with bandwidth needs under 1 Gbps. What's the best fit?",
     ["AWS Direct Connect", "Site-to-Site VPN", "AWS Transit Gateway", "VPC Peering"],
     1,
     "Site-to-Site VPN is fast to set up (hours-days) and cheap - ideal for budget-conscious, lower-bandwidth hybrid needs."),

    ("Client VPN",
     "AWS Client VPN is designed for which use case?",
     ["Connecting an entire office network to AWS", "Individual remote users/devices securely connecting to AWS or on-prem resources",
      "Connecting two VPCs together", "Caching content closer to end users"],
     1,
     "Client VPN = user-to-network (individual remote employee access), distinct from Site-to-Site VPN which is network-to-network."),

    ("PrivateLink",
     "What does AWS PrivateLink primarily provide?",
     ["A cheaper alternative to Direct Connect for full internet access", "Private connectivity between VPCs and AWS/SaaS services without traversing the public internet",
      "A managed DNS service", "A subnet-level firewall"],
     1,
     "PrivateLink gives private, non-internet connectivity to AWS services (like S3) or supported SaaS tools via VPC interface endpoints."),

    ("PrivateLink",
     "Compared to using a NAT Gateway to reach an AWS service like S3, what advantage does PrivateLink offer?",
     ["It is always slower but more secure", "It avoids the public internet entirely for that traffic, unlike NAT Gateway which still routes out through the internet",
      "It requires no VPC at all", "It replaces the need for Security Groups"],
     1,
     "NAT Gateway still sends traffic out to the internet to reach AWS services; PrivateLink keeps that traffic entirely private."),

    # ---------------- Multi-VPC & Hybrid Networking ----------------
    ("VPC Peering & Transit Gateway",
     "VPC Peering connects how many VPCs in a single peering connection?",
     ["Exactly 2 VPCs, one-to-one", "Up to 5 VPCs", "Unlimited VPCs", "Only VPCs within the same account"],
     0,
     "VPC Peering is a direct one-to-one connection between exactly two VPCs."),

    ("VPC Peering & Transit Gateway",
     "If VPC-A peers with VPC-B, and VPC-B peers with VPC-C, can VPC-A communicate with VPC-C through VPC-B?",
     ["Yes, automatically", "No - VPC Peering connections are not transitive; A and C would need their own direct peering connection",
      "Only if using IPv6", "Only if all three VPCs are in the same Region"],
     1,
     "VPC Peering is explicitly non-transitive - this limitation is the core reason Transit Gateway exists."),

    ("VPC Peering & Transit Gateway",
     "A company has 15 VPCs across 3 Regions that all need to communicate, and full-mesh peering has become unmanageable. What should they use?",
     ["More VPC Peering connections", "AWS Transit Gateway", "AWS Client VPN", "Amazon Route 53"],
     1,
     "Transit Gateway acts as a central hub, replacing an unmanageable full mesh of point-to-point VPC Peering connections."),

    ("VPC Peering & Transit Gateway",
     "For 10 VPCs to all communicate using full-mesh VPC Peering, how many individual peering connections are needed (using n(n-1)/2)?",
     ["10", "20", "45", "100"],
     2,
     "n(n-1)/2 = 10x9/2 = 45 connections - illustrating why Transit Gateway scales better for many VPCs."),

    # ---------------- Network Security ----------------
    ("Security Groups & NACLs",
     "Security Groups operate at which level, and NACLs operate at which level?",
     ["SG = subnet level, NACL = instance level", "SG = instance (ENI) level, NACL = subnet level",
      "Both operate at the VPC level", "Both operate at the Region level"],
     1,
     "Security Groups protect individual instances (ENIs); NACLs protect entire subnets."),

    ("Security Groups & NACLs",
     "What is the default inbound/outbound behavior of a newly created Security Group?",
     ["Allow all inbound, deny all outbound", "Deny all inbound, allow all outbound",
      "Allow all inbound and outbound", "Deny all inbound and outbound"],
     1,
     "Security Groups default to denying all inbound traffic while allowing all outbound traffic by default."),

    ("Security Groups & NACLs",
     "Which statement about Security Groups and rule types is TRUE?",
     ["SGs support both allow and explicit deny rules", "SGs support only allow rules - there are no explicit deny rules",
      "SGs are always stateless", "SGs operate at the subnet level"],
     1,
     "Security Groups only ever have allow rules; anything not explicitly allowed is implicitly denied."),

    ("Security Groups & NACLs",
     "Which TWO of the following are TRUE about Network ACLs (NACLs)?",
     ["NACLs operate at the subnet level", "NACLs are stateful like Security Groups",
      "NACLs support both allow and explicit deny rules", "NACLs automatically allow return traffic"],
     [0, 2],
     "NACLs are subnet-level (not instance-level) and support explicit allow/deny rules - unlike SGs which are stateful and allow-only."),

    ("Security Groups & NACLs",
     "Is a Security Group stateful or stateless?",
     ["Stateful - if inbound traffic is allowed, the matching return outbound traffic is automatically allowed", "Stateless - both directions must be explicitly allowed",
      "Neither concept applies to Security Groups", "It depends on the instance type"],
     0,
     "Security Groups are stateful: allowing inbound traffic automatically permits the corresponding outbound response, and vice versa."),

    ("Security Groups & NACLs",
     "Is a Network ACL (NACL) stateful or stateless?",
     ["Stateful, like Security Groups", "Stateless - inbound and outbound rules must each be explicitly configured",
      "Stateless only for HTTPS traffic", "Stateful only for outbound traffic"],
     1,
     "NACLs are stateless - unlike SGs, allowing inbound traffic does NOT automatically allow the return outbound traffic; both must be explicit."),

    ("Security Groups & NACLs",
     "Which of these correctly describes the default NACL that comes with a new VPC versus a custom NACL you create yourself?",
     ["Both allow all traffic by default", "The default NACL allows all inbound/outbound traffic; a custom NACL denies all traffic by default until rules are added",
      "Both deny all traffic by default", "Custom NACLs cannot have deny rules"],
     1,
     "The VPC's default NACL allows all traffic out of the box, but any custom NACL you create starts by denying everything until you add rules."),

    ("Security Groups & NACLs",
     "A user reports 'connection refused' errors trying to reach a web server on port 80, even though the server process is confirmed running. What should you check FIRST?",
     ["The Region's compliance settings", "Security Group inbound rules for port 80/443", "The CloudFront cache TTL", "The Direct Connect bandwidth"],
     1,
     "This is a classic exam pattern - connectivity issues to a running server almost always trace back to missing Security Group inbound rules."),

    ("Security Groups & NACLs",
     "NACL rules are evaluated in which manner?",
     ["Randomly", "In numbered order, from lowest to highest, until a matching rule is found", "All rules simultaneously with no order", "Alphabetically by rule name"],
     1,
     "NACL rules are evaluated in numbered order (e.g., rule 100 before rule 200); the first matching rule applies."),

    # ---------------- Content Delivery & DNS ----------------
    ("CloudFront & Route 53",
     "What is Amazon CloudFront primarily used for?",
     ["Managed DNS resolution", "Caching content at edge locations for faster global delivery",
      "Routing traffic over AWS's private backbone for non-HTTP protocols", "Provisioning infrastructure as code"],
     1,
     "CloudFront is AWS's CDN - it caches content at edge locations to reduce latency for global users."),

    ("CloudFront & Route 53",
     "What is Amazon Route 53 primarily used for?",
     ["Content caching", "DNS - translating domain names to IPs, plus health checks and traffic routing",
      "Container orchestration", "Infrastructure as Code"],
     1,
     "Route 53 is AWS's managed DNS service, also handling domain registration, health checks, and routing policies."),

    ("CloudFront & Route 53",
     "A company's static website hosted in us-east-1 is loading slowly for users in Australia and Japan. What is the best fix?",
     ["Switch to Route 53", "Use Amazon CloudFront to cache content closer to those users", "Add more NAT Gateways", "Use AWS Client VPN"],
     1,
     "Global users experiencing slow load times for static/dynamic content is the textbook CloudFront use case."),

    ("CloudFront & Route 53",
     "A company wants to route users automatically to their nearest healthy regional endpoint and stop sending traffic to any endpoint that fails a health check. Which service handles this?",
     ["Amazon CloudFront", "Amazon Route 53", "AWS PrivateLink", "AWS Transit Gateway"],
     1,
     "Route 53 performs health checks and can route traffic away from unhealthy endpoints using policies like latency-based or failover routing."),

    # ---------------- API Gateway ----------------
    ("API Gateway",
     "What is Amazon API Gateway used for?",
     ["Storing container images", "A fully managed service to create, publish, secure, monitor, and scale APIs fronting backends like Lambda or EC2",
      "Managed DNS resolution", "Physical fiber connectivity to AWS"],
     1,
     "API Gateway is the managed 'front door' for APIs, commonly paired with Lambda for serverless backends."),

    ("API Gateway",
     "A typical serverless API architecture pattern looks like which of the following?",
     ["Client -> NAT Gateway -> RDS", "Client -> API Gateway -> Lambda -> Response", "Client -> Direct Connect -> S3", "Client -> NACL -> EC2"],
     1,
     "The classic serverless pattern: Client -> API Gateway -> Lambda -> Response, with API Gateway handling auth/throttling/scaling."),

    # ---------------- CloudFormation ----------------
    ("CloudFormation",
     "In CloudFormation terminology, what is the running, deployed instance of a template called?",
     ["A Blueprint", "A Stack", "A Fleet", "A Node"],
     1,
     "Deploying a CloudFormation template creates a Stack - the actual set of provisioned resources."),

    ("CloudFormation",
     "What AWS feature allows you to deploy the SAME CloudFormation stack consistently across multiple accounts and Regions?",
     ["Transit Gateway", "StackSets", "PrivateLink", "NACLs"],
     1,
     "CloudFormation StackSets extend stack deployment across many accounts and Regions from a single operation."),

    # ---------------- Comparison / Decision / Scenario ----------------
    ("Scenario & Comparison",
     "A German healthcare company must keep patient records within German borders due to legal requirements, even though a cheaper Region is available elsewhere. Which factor wins?",
     ["Cost", "Compliance - always overrides cost/latency/features", "Feature availability", "Whichever Region has more Edge Locations"],
     1,
     "Compliance requirements override cost every single time in AWS exam logic - a non-negotiable rule."),

    ("Scenario & Comparison",
     "An RDS database must remain completely hidden from the internet but still needs to download OS security patches periodically. What is the correct combination?",
     ["Public subnet + Internet Gateway", "Private subnet + NAT Gateway + Security Group allowing only the app tier",
      "Private subnet + no internet access at all", "Public subnet + NACL only"],
     1,
     "Private subnet keeps it hidden; NAT Gateway allows outbound-only patch downloads; Security Group restricts inbound access to just the app tier."),

    ("Scenario & Comparison",
     "A gaming company needs low-latency routing for real-time UDP traffic between global players, where caching doesn't help. What should they use?",
     ["Amazon CloudFront", "AWS Global Accelerator", "Amazon Route 53", "AWS Direct Connect"],
     1,
     "Global Accelerator routes non-cacheable, non-HTTP(S) traffic (like UDP gaming traffic) over AWS's private backbone for lower latency."),

    ("Scenario & Comparison",
     "20 employees need secure individual remote access to AWS resources from their home laptops. Which service fits best?",
     ["Site-to-Site VPN", "AWS Client VPN", "AWS Direct Connect", "VPC Peering"],
     1,
     "Individual user-to-network access = Client VPN. Entire office/network-to-network access = Site-to-Site VPN."),

    ("Scenario & Comparison",
     "An EC2 instance in a private subnet needs the MOST secure possible access to Amazon S3, with zero internet exposure. What should be used?",
     ["NAT Gateway", "AWS PrivateLink (S3 VPC endpoint)", "Internet Gateway", "AWS Client VPN"],
     1,
     "PrivateLink (via a VPC endpoint) provides private access to S3 with no traffic ever touching the public internet, unlike NAT Gateway."),

    ("Scenario & Comparison",
     "A mobile app needs a backend that automatically scales with zero server management. Which combination is the best fit?",
     ["EC2 + NAT Gateway", "API Gateway + Lambda", "Direct Connect + RDS", "VPC Peering + Client VPN"],
     1,
     "API Gateway (managed API front door) + Lambda (serverless compute) is the classic serverless mobile/web backend pattern."),

    ("Scenario & Comparison",
     "Which statement correctly distinguishes CloudFront from Route 53?",
     ["CloudFront is DNS, Route 53 is a CDN", "CloudFront caches content at the edge (CDN); Route 53 is DNS and traffic routing/health checking",
      "They are the same service", "CloudFront only works with Lambda"],
     1,
     "CloudFront = content delivery/caching. Route 53 = DNS resolution, domain routing, and health checks. Frequently confused pairing."),

    ("Scenario & Comparison",
     "A forex trading firm requires sub-5ms latency and unlimited budget for connectivity to AWS. Which connectivity approach best supports this need?",
     ["Site-to-Site VPN", "AWS Direct Connect for predictable, dedicated low-latency connectivity", "AWS Client VPN", "NAT Gateway"],
     1,
     "Predictable, ultra-low latency at high budget points directly to Direct Connect over VPN's internet-dependent performance."),

    ("Scenario & Comparison",
     "Which AWS networking trap is being tested when a question says 'Use Direct Connect for a quick, urgent connectivity need'?",
     ["This is correct - Direct Connect sets up in minutes", "This is a trap - Direct Connect takes 1-3 months to provision and is unsuitable for urgent needs",
      "Direct Connect is only for DNS", "Direct Connect requires no setup time at all"],
     1,
     "Direct Connect's multi-month provisioning timeline makes it the wrong answer for any 'urgent' or 'quick' connectivity scenario."),

    ("Scenario & Comparison",
     "True or False: A single Internet Gateway can be attached to multiple VPCs simultaneously.",
     ["True", "False"],
     1,
     "False - an Internet Gateway is attached to exactly one VPC at a time."),

    ("Scenario & Comparison",
     "Which service would a company use to define and repeatably deploy an identical VPC + subnet + security group setup across 5 AWS accounts?",
     ["AWS Transit Gateway", "AWS CloudFormation (with StackSets)", "Amazon Route 53", "AWS Client VPN"],
     1,
     "CloudFormation (especially with StackSets) is built exactly for consistent, repeatable, multi-account/region infrastructure deployment."),

    ("Scenario & Comparison",
     "Which TWO connectivity options keep traffic completely off the public internet?",
     ["Site-to-Site VPN", "AWS Direct Connect", "AWS PrivateLink", "AWS Client VPN"],
     [1, 2],
     "Direct Connect uses dedicated private fiber, and PrivateLink routes privately to AWS/SaaS services - neither touches the public internet. VPN and Client VPN both use the public internet, just encrypted."),
]

def _normalize_correct(correct_answer):
    """Return correct answer(s) as a set of indices, and whether it's multi-select."""
    if isinstance(correct_answer, (list, tuple, set)):
        return set(correct_answer), True
    return {correct_answer}, False


def run_quiz():
    print("=" * 70)
    print("AWS CCP (CLF-C02) - MODULE 5: NETWORKING - PRACTICE TEST")
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
        verdict = "Verdict: Strong. Module 5 is largely solid - light revision only."
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
    print("Any topic below 70% -> go back into the Module 5 notes for it.")
    print("Topics at 100% -> safe to skip re-reading, just do a final skim.")
    print("=" * 70)

    # ---- Export results to file ----
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
