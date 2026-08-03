#!/usr/bin/env python3
"""
AWS CCP (CLF-C02) - Module 2: Compute & Messaging Services - Practice MCQ Test
=================================================================================
Covers: AWS Compute Landscape Overview, EC2 Fundamentals & Instance Families,
Launching EC2 (AMI/Key Pairs/Security Groups), Ways to Access AWS, EC2 Pricing
Models, AWS Lambda, Elastic Beanstalk, Amazon Lightsail, Containers (ECS/EKS/
Fargate), Scalability & Elasticity, EC2 Auto Scaling, Load Balancing,
Messaging (SQS/SNS/EventBridge), and Amazon CloudWatch.

Run:  python3 2-ComputeMessaging.py

EXAM-MODE BEHAVIOR: No feedback is shown per question (matches the real
CLF-C02 exam interface). At the end you get:
  - Overall score
  - Topic-wise breakdown (weakest first, so you know exactly what to re-study)
  - A dedicated "Missed Questions Review" section (only questions you got
    wrong, with your answer, the correct answer, and why)
  - Auto-exported report to Module2-ComputeMessaging-Results.txt
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "Module2-ComputeMessaging"

# Each question: (topic, question_text, [options], correct_answer(s), explanation)
# correct_answer(s): a single 0-based int for single-select questions,
#                     OR a list/tuple of 0-based ints for multi-select ("Select TWO/THREE") questions.
QUESTIONS = [
    # ---------------- 1. Compute Landscape Overview ----------------
    ("Compute Landscape Overview",
     "A company wants zero server management and to pay only when their code actually runs. Which compute service fits best?",
     ["Amazon EC2", "AWS Lambda", "Amazon Lightsail", "Amazon EKS"],
     1,
     "Lambda is serverless - zero infrastructure management, billed only for actual compute time used."),

    ("Compute Landscape Overview",
     "A team wants to deploy a web app quickly without manually configuring EC2, load balancers, and Auto Scaling separately, but might want to peek under the hood later. Which service fits?",
     ["AWS Lambda", "Amazon Lightsail", "AWS Elastic Beanstalk", "AWS Outposts"],
     2,
     "Elastic Beanstalk automatically provisions EC2, ELB, and ASG for you (PaaS), while still exposing the underlying resources if needed."),

    ("Compute Landscape Overview",
     "Which compute option is described as needing 'full control over the OS/VM, custom software stack, or a long-running predictable workload'?",
     ["AWS Lambda", "Amazon EC2", "Amazon Lightsail", "AWS Fargate"],
     1,
     "EC2 (IaaS) is the right choice when full OS/software control and long-running predictability are required."),

    # ---------------- 2. EC2 Fundamentals ----------------
    ("EC2 Fundamentals",
     "What service model category does Amazon EC2 belong to?",
     ["SaaS", "PaaS", "IaaS", "FaaS"],
     2,
     "EC2 provides resizable virtual machines - this is Infrastructure as a Service (IaaS), sometimes called Compute as a Service."),

    ("EC2 Fundamentals",
     "How is Amazon EC2 typically billed?",
     ["A flat annual license fee regardless of usage", "Only while the instance is actually running", "Only when the instance is stopped", "A one-time purchase fee"],
     1,
     "EC2 is billed per second/hour of actual running time - stopped or terminated instances don't incur compute charges."),

    ("EC2 Fundamentals",
     "Which of these is a valid reason to choose EC2 over Lambda or Lightsail?",
     ["The workload is short and event-driven", "The workload is a legacy application that can't be easily re-architected as serverless", "The workload is a simple static website with very low traffic", "The team wants AWS to fully manage all infrastructure with zero visibility"],
     1,
     "EC2 fits legacy applications needing full OS control that can't easily be re-architected for serverless or simplified platforms."),

    ("EC2 Fundamentals",
     "What happens to EC2 compute billing when an instance is stopped (not terminated)?",
     ["Compute charges continue at full rate", "Compute charges stop; only attached storage (like EBS) may still incur charges", "The instance is automatically deleted after 24 hours", "Billing doubles as a penalty"],
     1,
     "When stopped, EC2 compute charges stop, though attached storage volumes may continue to incur their own charges."),

    # ---------------- 3. EC2 Instance Families ----------------
    ("EC2 Instance Families",
     "A company needs to run a standard web server with balanced CPU, RAM, and network needs. Which instance family fits best?",
     ["Compute Optimized (C-series)", "General Purpose (T/M-series)", "Memory Optimized (R-series)", "Storage Optimized (I-series)"],
     1,
     "General Purpose instances (T, M series) offer a balanced mix of CPU, RAM, and network - the default choice when no special need is specified."),

    ("EC2 Instance Families",
     "A media company needs to run heavy video transcoding and scientific modeling workloads requiring high vCPU-to-RAM ratio. Which family fits?",
     ["Memory Optimized", "Compute Optimized", "Storage Optimized", "General Purpose"],
     1,
     "Compute Optimized instances (C-series) are built for high-CPU workloads like video transcoding, batch processing, and scientific modeling."),

    ("EC2 Instance Families",
     "A financial firm runs an in-memory database (like Redis) requiring massive RAM relative to CPU. Which instance family fits best?",
     ["Storage Optimized", "Accelerated Computing", "Memory Optimized", "General Purpose"],
     2,
     "Memory Optimized instances (R, X, Z series) provide large RAM relative to CPU, ideal for in-memory databases and real-time analytics."),

    ("EC2 Instance Families",
     "A company running Cassandra/MongoDB needs high-speed, high-throughput local disk I/O. Which instance family fits?",
     ["Storage Optimized", "Compute Optimized", "General Purpose", "Memory Optimized"],
     0,
     "Storage Optimized instances (I, D, H series) provide high-speed local disk I/O, ideal for NoSQL databases and distributed file systems."),

    ("EC2 Instance Families",
     "A team training deep learning models needs attached GPU hardware. Which instance family fits?",
     ["General Purpose", "Accelerated Computing", "Storage Optimized", "Memory Optimized"],
     1,
     "Accelerated Computing instances (P, G, F, Inf series) include attached GPU/TPU/FPGA hardware, ideal for ML training and graphics rendering."),

    # ---------------- 4. Launching EC2 (AMI, Key Pairs, Security Groups) ----------------
    ("Launching EC2 Components",
     "What does an AMI (Amazon Machine Image) define when launching an EC2 instance?",
     ["Only the network firewall rules", "The OS, pre-installed software, and configuration used to launch the instance", "Only the SSH key used for access", "Only the billing plan for the instance"],
     1,
     "An AMI is a pre-configured template defining OS, pre-installed software, and configuration - the 'blueprint' for launching an instance."),

    ("Launching EC2 Components",
     "In an EC2 key pair, which key does AWS keep attached to the instance, and which does the user download and keep private?",
     ["AWS keeps the private key; user downloads the public key", "AWS keeps the public key; user downloads the private key (once)", "Both keys stay with AWS permanently", "Both keys are downloaded by the user"],
     1,
     "The public key stays with AWS attached to the instance; the private key is downloaded once by the user - if lost, recovery is difficult."),

    ("Launching EC2 Components",
     "What is the default inbound traffic behavior of a newly created Security Group before any rules are configured?",
     ["Allow all inbound traffic", "Deny all inbound traffic", "Allow inbound only from AWS Support", "Allow inbound only on port 443"],
     1,
     "By default, a new Security Group denies all inbound traffic until you explicitly configure allow rules; outbound is allowed by default."),

    ("Launching EC2 Components",
     "Which of the following is TRUE about EC2 Security Groups? (Select TWO)",
     ["They are stateful", "They support explicit deny rules", "They only support allow rules", "They operate at the subnet level, not instance level"],
     [0, 2],
     "Security Groups are stateful (matching return traffic is auto-allowed) and only support allow rules - there is no explicit deny like NACLs have."),

    ("Launching EC2 Components",
     "Exam Trap: If you lose your EC2 private key for a Linux instance, what generally happens?",
     ["AWS automatically emails you a replacement key", "You generally cannot recover SSH access the normal way - key management best practices matter", "The instance automatically becomes publicly accessible", "Nothing changes; passwords are used instead"],
     1,
     "Losing a private key typically means you cannot recover SSH access through the normal method - this is why proper key management is emphasized."),

    # ---------------- 5. Ways to Access AWS ----------------
    ("Ways to Access AWS",
     "Which method of accessing AWS is best suited for automation and scripting of repetitive, batch operations?",
     ["AWS Management Console", "AWS CLI", "Physical data center visit", "Postal mail request"],
     1,
     "The AWS CLI (command-line interface) is best for automation and scripting, unlike the manual, GUI-based Management Console."),

    ("Ways to Access AWS",
     "A developer wants to integrate AWS functionality directly inside their own application code (e.g., using Python). Which access method fits?",
     ["AWS Management Console", "AWS SDK (e.g., boto3 for Python)", "AWS CLI only", "Physical support ticket"],
     1,
     "AWS SDKs (like boto3 for Python) let developers integrate AWS calls directly into their applications programmatically."),

    # ---------------- 6. EC2 Pricing Models ----------------
    ("EC2 Pricing Models",
     "Which EC2 pricing model offers up to ~90% discount but can be reclaimed by AWS with a 2-minute warning?",
     ["On-Demand", "Reserved Instances", "Spot Instances", "Dedicated Hosts"],
     2,
     "Spot Instances use AWS's spare capacity at steep discounts but can be interrupted with only a 2-minute warning."),

    ("EC2 Pricing Models",
     "A company has a steady-state production database running continuously for the next 3 years and wants the best discount for that specific instance type. Which pricing model fits best?",
     ["Spot Instances", "On-Demand", "Reserved Instances", "Dedicated Host"],
     2,
     "Reserved Instances offer up to ~72% discount for a locked commitment (1 or 3 years) to a specific instance type - ideal for predictable, steady-state workloads."),

    ("EC2 Pricing Models",
     "What is the KEY difference between a Reserved Instance and a Savings Plan?",
     ["Reserved Instance is locked to a specific instance type/Region; Savings Plan commits to a flexible dollar amount per hour", "They are identical in every way", "Savings Plans can never be resold; Reserved Instances always can be resold in bulk", "Reserved Instances apply to Lambda; Savings Plans apply only to EC2"],
     0,
     "Reserved Instances lock you to a specific instance type/Region (unless Convertible), while Savings Plans commit to a flexible dollar-amount per hour that applies more broadly."),

    ("EC2 Pricing Models",
     "Which type of Savings Plan can also apply its discount to AWS Lambda and Fargate usage, not just EC2?",
     ["EC2 Instance Savings Plans", "Compute Savings Plans", "Reserved Instances", "Dedicated Host pricing"],
     1,
     "Compute Savings Plans are the most flexible - applying across any instance family, size, OS, Region, and even Lambda/Fargate usage."),

    ("EC2 Pricing Models",
     "A pharmaceutical company has software licensed per physical CPU socket and needs full visibility into the physical server. Which EC2 pricing/tenancy option fits best?",
     ["On-Demand with default tenancy", "Spot Instance", "Dedicated Host", "Reserved Instance with shared tenancy"],
     2,
     "Dedicated Hosts reserve an entire physical server with full visibility into sockets/cores - ideal for per-socket licensing requirements."),

    ("EC2 Pricing Models",
     "Which is the CORRECT cheapest-to-most-expensive order of EC2 pricing models?",
     ["On-Demand < Spot < Reserved < Dedicated Host", "Spot < Reserved/Savings Plans < On-Demand < Dedicated Host", "Dedicated Host < On-Demand < Reserved < Spot", "Reserved < Spot < On-Demand < Dedicated Host"],
     1,
     "The correct cost order (cheapest to most expensive) is: Spot < Reserved/Savings Plans < On-Demand < Dedicated Instance < Dedicated Host."),

    ("EC2 Pricing Models",
     "Exam Trap: A team wants the CHEAPEST possible pricing for a CRITICAL, always-on production database that cannot tolerate interruption. Should they choose Spot Instances?",
     ["Yes, Spot is always cheapest so it's the right choice", "No - Spot can be interrupted with a 2-minute warning; Reserved/Savings Plans fit critical steady-state workloads better", "Yes, but only if using Windows Server", "No, they should use On-Demand exclusively for all critical workloads"],
     1,
     "Even though Spot is cheapest, its interruptibility makes it unsuitable for critical, always-on workloads - Reserved Instances or Savings Plans are the correct discount option for predictable critical workloads."),

    # ---------------- 7. AWS Lambda ----------------
    ("AWS Lambda",
     "AWS Lambda is best classified as which service model?",
     ["IaaS", "PaaS", "FaaS (Function as a Service)", "SaaS"],
     2,
     "Lambda is Function as a Service (FaaS) - you upload code and AWS manages everything else, including scaling and infrastructure."),

    ("AWS Lambda",
     "How is AWS Lambda billed?",
     ["A flat monthly fee regardless of usage", "Per number of requests plus compute duration (GB-seconds)", "Per EC2 instance-hour", "Per gigabyte of storage only"],
     1,
     "Lambda charges per number of requests and compute duration (down to the millisecond) - true pay-per-use with zero charge when idle."),

    ("AWS Lambda",
     "A company wants to automatically generate a thumbnail every time a user uploads a photo to S3, and uploads happen unpredictably throughout the day. Which service is the best fit?",
     ["Amazon EC2 running 24/7", "AWS Lambda triggered by an S3 event", "Amazon Lightsail", "AWS Outposts"],
     1,
     "Lambda is ideal for unpredictable, event-driven tasks like this - no server sits idle waiting for the next upload."),

    ("AWS Lambda",
     "Which of the following is a valid limitation of AWS Lambda that would push a workload back toward EC2 instead?",
     ["Lambda cannot process any HTTP requests", "Lambda has a maximum execution time limit per invocation, unsuitable for long-running batch jobs", "Lambda requires manual server patching", "Lambda cannot scale automatically"],
     1,
     "Lambda has a hard maximum execution time limit per invocation - workloads needing to run for hours should use EC2, Fargate, or AWS Batch instead."),

    ("AWS Lambda",
     "Exam Trap: Is AWS Lambda always the cheapest compute option, regardless of traffic volume?",
     ["Yes, Lambda is always the cheapest option no matter the volume", "No - at very high, constant, predictable throughput, a reserved EC2 fleet can be cheaper than Lambda's per-request pricing", "Yes, because Lambda has no billing at all", "No, Lambda is never appropriate for production workloads"],
     1,
     "While Lambda is excellent for bursty/unpredictable workloads, at very high constant throughput a reserved EC2 fleet can actually work out cheaper than Lambda's per-request pricing."),

    # ---------------- 8. Elastic Beanstalk ----------------
    ("Elastic Beanstalk",
     "What is AWS Elastic Beanstalk?",
     ["A container image registry", "A PaaS that automatically handles deployment, provisioning, load balancing, and scaling for uploaded application code", "A pure IaaS virtual machine rental service", "A serverless function execution engine"],
     1,
     "Elastic Beanstalk is AWS's PaaS offering - upload your code and AWS automatically provisions and manages the EC2/ELB/ASG infrastructure underneath."),

    ("Elastic Beanstalk",
     "Even though Elastic Beanstalk automates infrastructure provisioning, what access does the customer retain?",
     ["No access at all - it's a complete black box", "Full access to the underlying EC2, ELB, and ASG resources it creates, if needed", "Only read-only access via AWS Support", "Access only after paying an additional fee"],
     1,
     "Unlike fully abstracted services like Lambda, Elastic Beanstalk still exposes and grants access to the underlying EC2, load balancer, and Auto Scaling resources it provisions."),

    ("Elastic Beanstalk",
     "Exam Trap: Is Elastic Beanstalk a 'serverless' service like Lambda?",
     ["Yes, Beanstalk has no underlying servers at all", "No - Beanstalk still runs on EC2/ELB/ASG underneath; it just automates their setup", "Yes, because AWS manages the deployment process", "No, because Beanstalk cannot deploy web applications"],
     1,
     "Elastic Beanstalk is PaaS, not serverless - it still runs on EC2, ELB, and ASG underneath, unlike Lambda which is fully abstracted."),

    # ---------------- 9. Amazon Lightsail ----------------
    ("Amazon Lightsail",
     "Amazon Lightsail is best suited for which type of use case?",
     ["Enterprise-scale, complex multi-tier architectures", "Simple websites, small blogs, and beginner-friendly projects with predictable, bundled pricing", "High-performance computing clusters", "Managed Kubernetes at massive scale"],
     1,
     "Lightsail is a simplified, bundled VPS aimed at simple workloads and beginners who want an easier on-ramp than raw EC2 configuration."),

    ("Amazon Lightsail",
     "What is a key differentiator of Lightsail's pricing compared to standard EC2 pricing?",
     ["Lightsail has no pricing at all - it's free", "Lightsail bundles compute, storage, and data transfer into one flat, predictable monthly rate", "Lightsail bills per API call only", "Lightsail is always more expensive than Dedicated Hosts"],
     1,
     "Lightsail offers flat, bundled monthly pricing covering compute, storage, and data transfer together - easier to predict than EC2's à la carte billing."),

    # ---------------- 10. Containers (ECS/EKS/Fargate) ----------------
    ("Containers (ECS/EKS/Fargate)",
     "What is Amazon ECS?",
     ["A managed Kubernetes service", "AWS's own native container orchestration service", "A serverless function execution engine", "A content delivery network"],
     1,
     "ECS (Elastic Container Service) is AWS's proprietary, native container orchestration service."),

    ("Containers (ECS/EKS/Fargate)",
     "A team already has deep Kubernetes expertise and wants to migrate existing Kubernetes workloads to AWS with minimal changes. Which service fits best?",
     ["Amazon ECS", "Amazon EKS", "AWS Lambda", "Amazon Lightsail"],
     1,
     "EKS (Elastic Kubernetes Service) is AWS's managed Kubernetes offering, ideal for teams already standardized on the Kubernetes API."),

    ("Containers (ECS/EKS/Fargate)",
     "What is the relationship between AWS Fargate and ECS/EKS?",
     ["Fargate is a competing alternative that replaces ECS and EKS entirely", "Fargate is a serverless compute engine (launch type) that works WITH both ECS and EKS, removing the need to manage EC2 instances", "Fargate only works with Lambda, not containers", "Fargate is a container image registry"],
     1,
     "Fargate is not a competitor to ECS/EKS - it's a serverless compute engine that works with either, removing the need to manage the underlying EC2 instances."),

    ("Containers (ECS/EKS/Fargate)",
     "Exam Trap: If a question specifically mentions 'Kubernetes,' which AWS container service should you pick?",
     ["ECS, since it is AWS-native", "EKS, since ECS is AWS's proprietary orchestrator, not Kubernetes-based", "Fargate, as a standalone orchestrator", "AWS Outposts"],
     1,
     "When a question specifically says 'Kubernetes,' the answer is EKS - ECS is AWS's own proprietary orchestrator and is not Kubernetes-based."),

    # ---------------- 11. Scalability & Elasticity ----------------
    ("Scalability & Elasticity",
     "What is the key difference between 'scalability' and 'elasticity'?",
     ["They are synonyms with no real difference", "Scalability is the capability to grow; elasticity is the automatic, real-time act of growing/shrinking", "Scalability only applies to storage; elasticity only applies to compute", "Elasticity requires manual intervention while scalability does not"],
     1,
     "Scalability is a system design property (the capability to grow), while elasticity is the automatic, real-time act of scaling up or down based on demand - a system can be scalable without being elastic."),

    ("Scalability & Elasticity",
     "Manually resizing a single EC2 instance from t2.micro to t2.large is an example of which type of scaling?",
     ["Scale Out (horizontal)", "Scale Up (vertical)", "Elastic scaling", "Auto Scaling"],
     1,
     "Scale Up (vertical scaling) means upgrading the same machine's resources - same instance, more power."),

    ("Scalability & Elasticity",
     "Adding more EC2 instances (e.g., going from 1 instance to 3) to handle increased load is an example of which type of scaling?",
     ["Scale Up (vertical)", "Scale Out (horizontal)", "Manual patching", "Dedicated Hosting"],
     1,
     "Scale Out (horizontal scaling) means adding more machines rather than upgrading a single one - the modern cloud-native default."),

    ("Scalability & Elasticity",
     "Which type of scaling generally has a hard ceiling and often requires downtime to resize?",
     ["Scale Out (horizontal)", "Scale Up (vertical)", "Auto Scaling", "Load balancing"],
     1,
     "Vertical scaling (scale up) has a hard ceiling - the biggest instance type available - and usually requires downtime to resize."),

    # ---------------- 12. EC2 Auto Scaling ----------------
    ("EC2 Auto Scaling",
     "In an EC2 Auto Scaling Group, what does the 'Minimum' setting control?",
     ["The maximum number of instances allowed even at peak load", "The number of instances that always keep running, even at zero load", "The target instance count under normal conditions", "The number of Availability Zones used"],
     1,
     "The Minimum setting ensures a floor number of instances always keeps running, even during periods of zero load, guaranteeing baseline availability."),

    ("EC2 Auto Scaling",
     "Which AWS service does an Auto Scaling Group rely on to monitor metrics like CPU usage and trigger scaling policies?",
     ["Amazon CloudWatch", "Amazon SNS", "AWS CloudTrail", "Amazon Route 53"],
     0,
     "CloudWatch monitors metrics like CPU usage, and Auto Scaling policies (e.g., 'if CPU > 70%, add instance') act on those CloudWatch metrics."),

    ("EC2 Auto Scaling",
     "An ASG is set with Min=2, Desired=2, Max=5. If traffic spikes heavily, what is the MOST instances the ASG will ever launch?",
     ["2", "3", "5", "Unlimited"],
     2,
     "The Maximum setting (5 in this case) is the hard ceiling - the ASG will never exceed this count regardless of how high traffic spikes."),

    # ---------------- 13. Load Balancing ----------------
    ("Load Balancing",
     "What problem does a Load Balancer primarily solve?",
     ["It encrypts data at rest", "It distributes incoming traffic evenly across multiple instances to avoid overloading any single one", "It replaces the need for Availability Zones", "It automatically writes application code"],
     1,
     "A Load Balancer distributes incoming traffic across multiple instances, preventing any single instance from being overloaded while others sit idle."),

    ("Load Balancing",
     "Which AWS Load Balancer operates at Layer 7 (Application layer) and supports routing based on URL path or host?",
     ["Network Load Balancer (NLB)", "Application Load Balancer (ALB)", "Gateway Load Balancer (GLB)", "Classic Load Balancer (CLB) only"],
     1,
     "The Application Load Balancer (ALB) operates at Layer 7, understanding HTTP/HTTPS content and supporting path/host-based routing."),

    ("Load Balancing",
     "Which AWS Load Balancer is best suited for extreme performance, low latency, and static IP requirements such as gaming or IoT?",
     ["Application Load Balancer (ALB)", "Network Load Balancer (NLB)", "Gateway Load Balancer (GLB)", "Classic Load Balancer (CLB)"],
     1,
     "The Network Load Balancer (NLB) operates at Layer 4 (TCP/UDP), offering extreme performance and low latency, ideal for gaming and IoT."),

    ("Load Balancing",
     "Which AWS Load Balancer is designed for deploying and scaling third-party virtual security appliances like firewalls and IDS/IPS transparently?",
     ["Application Load Balancer (ALB)", "Network Load Balancer (NLB)", "Gateway Load Balancer (GLB)", "Classic Load Balancer (CLB)"],
     2,
     "The Gateway Load Balancer (GLB) operates at Layer 3 and is purpose-built for transparently inserting third-party security appliances into traffic flow."),

    ("Load Balancing",
     "Exam Trap: Does a Load Balancer alone automatically replace a failed, unhealthy instance?",
     ["Yes, Load Balancers always replace failed instances on their own", "No - a Load Balancer only stops sending traffic to unhealthy instances; replacing them requires pairing with Auto Scaling", "Yes, but only for ALB, not NLB", "No, Load Balancers cannot detect unhealthy instances at all"],
     1,
     "A Load Balancer's health checks stop routing traffic to unhealthy instances, but actually replacing a failed instance requires pairing the Load Balancer with an Auto Scaling Group."),

    # ---------------- 14. Messaging (SQS/SNS/EventBridge) ----------------
    ("Messaging (SQS/SNS/EventBridge)",
     "What is the core function of Amazon SQS?",
     ["Instantly broadcasting a message to many subscribers", "A managed message queue where producers place messages and consumers retrieve/process them independently", "Routing events based on complex conditional rules", "Monitoring EC2 CPU usage"],
     1,
     "SQS is a managed message queue that decouples producers from consumers - messages persist until a consumer retrieves and processes them."),

    ("Messaging (SQS/SNS/EventBridge)",
     "What is the core function of Amazon SNS?",
     ["A pull-based work queue for batch processing", "A pub/sub service that instantly broadcasts one message to many subscribers at once", "A rules engine for routing SaaS events", "A monitoring and alerting-only service with no messaging capability"],
     1,
     "SNS is a publish-subscribe (pub/sub) broadcast service - one message is pushed instantly to all subscribers (email, SMS, Lambda, etc.)."),

    ("Messaging (SQS/SNS/EventBridge)",
     "Exam Trap: A question describes 'orders waiting to be processed at the workers' own pace.' Which messaging service is being described - SQS or SNS?",
     ["SNS, since it involves multiple workers", "SQS, since this describes a pull-based queue, not an instant broadcast", "Both are equally correct", "Neither - this describes EventBridge"],
     1,
     "This is the classic SQS pattern - a pull-based queue where messages persist until a consumer/worker picks them up at their own pace, unlike SNS's instant broadcast."),

    ("Messaging (SQS/SNS/EventBridge)",
     "Which AWS messaging service is the most advanced, supporting rules-based routing and filtering across AWS services, SaaS apps, and custom applications?",
     ["Amazon SQS", "Amazon SNS", "Amazon EventBridge", "Amazon CloudWatch"],
     2,
     "EventBridge is the most advanced of the three - a serverless event bus supporting conditional, rules-based routing across a wide range of event sources including SaaS apps."),

    ("Messaging (SQS/SNS/EventBridge)",
     "A CloudWatch alarm detects high CPU and needs to simultaneously alert via email, SMS, and Slack. Which service is the best fit?",
     ["Amazon SQS", "Amazon SNS", "AWS Batch", "Amazon EBS"],
     1,
     "SNS's pub/sub fan-out model is ideal for simultaneously notifying multiple channels (email, SMS, Slack) the instant an alarm fires."),

    ("Messaging (SQS/SNS/EventBridge)",
     "A video file is uploaded to S3, and this should automatically trigger a Lambda function to transcode it, with no polling required. Which service is the best fit for this conditional, event-driven trigger?",
     ["Amazon SQS", "Amazon SNS", "Amazon EventBridge", "AWS CloudTrail"],
     2,
     "EventBridge's rules-based routing is designed exactly for this kind of conditional, event-driven trigger from a source like S3 to a target like Lambda."),

    ("Messaging (SQS/SNS/EventBridge)",
     "Which TWO of the following are true about SQS's Visibility Timeout feature? (Select TWO)",
     ["It hides a message from other workers while one worker is processing it", "It permanently deletes the message from the queue", "It helps avoid duplicate processing of the same message", "It broadcasts the message to all subscribers immediately"],
     [0, 2],
     "SQS's Visibility Timeout hides an in-progress message from other consumers, which helps prevent duplicate processing while one worker handles it."),

    # ---------------- 15. Amazon CloudWatch ----------------
    ("Amazon CloudWatch",
     "What is Amazon CloudWatch primarily used for?",
     ["Storing large media files", "AWS's native monitoring and observability service, collecting metrics/logs and triggering alarms", "Running serverless container workloads", "Managing DNS routing between Regions"],
     1,
     "CloudWatch is AWS's native monitoring service - it collects metrics and logs and can trigger alarms/actions when thresholds are crossed."),

    ("Amazon CloudWatch",
     "In the context of Auto Scaling, what role does CloudWatch play?",
     ["CloudWatch directly launches and terminates EC2 instances on its own, with no other service involved", "CloudWatch monitors metrics like CPU usage; the Auto Scaling policy and ASG are what actually act on the alarm", "CloudWatch only stores billing invoices", "CloudWatch replaces the need for a Load Balancer"],
     1,
     "CloudWatch monitors and reports metrics (like CPU%), but it is the Auto Scaling Group and its scaling policy that actually acts on the alarm to launch or terminate instances."),

    ("Amazon CloudWatch",
     "Which CloudWatch component is responsible for triggering a notification or action when a metric crosses a defined threshold?",
     ["Metrics", "Logs", "Alarms", "Dashboards"],
     2,
     "CloudWatch Alarms are specifically the component that triggers notifications/actions when a monitored metric crosses a defined threshold."),
]


def _normalize_correct(correct_answer):
    """Return correct answer(s) as a set of indices, and whether it's multi-select."""
    if isinstance(correct_answer, (list, tuple, set)):
        return set(correct_answer), True
    return {correct_answer}, False


def run_quiz():
    print("=" * 70)
    print("AWS CCP (CLF-C02) - MODULE 2: COMPUTE & MESSAGING SERVICES - PRACTICE TEST")
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
        verdict = "Verdict: Strong. Module 2 is largely solid - light revision only."
    elif pct >= 70:
        verdict = "Verdict: Decent, but gaps exist. Revisit weak topics below before moving on."
    else:
        verdict = "Verdict: Needs deeper study. Don't move to Module 3 yet."
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
