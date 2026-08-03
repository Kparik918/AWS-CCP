#!/usr/bin/env python3
"""
====================================================================
AWS Certified Cloud Practitioner (CLF-C02) — FINAL REVISION QUIZ
Module: Revision (covers every service + core theory topic from the
Final Revision Cheat Sheet — Part 1 Core Theory + Part 2 all 22
service categories + Serverless/Auto-Scaling quick tables + exam-
morning trap reminders)

EXAM MODE:
  - No correct/incorrect feedback is shown while attempting questions.
  - Each answer is simply recorded, exactly like the real CLF-C02 exam UI.
  - Full score, topic-wise weak-spot breakdown, and a "Missed Questions
    Review" are shown ONLY after you submit the final question.
  - A results report is auto-exported to "Revision-Results.txt".
====================================================================
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NUMBER = "Revision"
MODULE_NAME = "Revision"

# --------------------------------------------------------------------
# QUESTIONS: (topic, question_text, [options], correct_answer, explanation)
#   correct_answer -> single 0-based int for single-select
#   correct_answer -> list/tuple of 0-based ints for multi-select
# --------------------------------------------------------------------

QUESTIONS = [

    # ============================================================
    # CORE THEORY — Service Models (IaaS/PaaS/SaaS)
    # ============================================================
    ("Core Theory - Service Models",
     "A company wants to run code without provisioning or patching any servers, and only pay for the compute time consumed. Which service model does this describe?",
     ["IaaS", "PaaS (Lambda is often classified as FaaS, a PaaS subset)", "SaaS", "On-premises virtualization"],
     1,
     "Lambda abstracts away servers, OS, and runtime management entirely, leaving you responsible only for your code — the textbook definition of PaaS/FaaS."),

    ("Core Theory - Service Models",
     "Which AWS service is the clearest example of SaaS, where AWS manages the entire application and the customer only configures and uses it?",
     ["Amazon EC2", "Amazon RDS", "Amazon Chime", "AWS Elastic Beanstalk"],
     2,
     "Amazon Chime is a ready-to-use application (communications/meetings) — the customer manages nothing but their usage and configuration, which is the definition of SaaS."),

    ("Core Theory - Service Models",
     "With Amazon EC2 (IaaS), which of the following remains the customer's responsibility?",
     ["Physical data center security", "Hypervisor/virtualization layer", "Guest OS patching and configuration", "Global network infrastructure"],
     2,
     "In IaaS, AWS manages the physical hardware and virtualization layer, but the customer still owns the guest OS, runtime, and application — this is the largest management burden shift compared to PaaS/SaaS."),

    # ============================================================
    # CORE THEORY — Deployment Models
    # ============================================================
    ("Core Theory - Deployment Models",
     "A hospital must keep patient records on-premises for regulatory reasons but wants to burst additional compute workloads into AWS. Which deployment model does this describe?",
     ["Cloud-native", "Hybrid", "On-premises only", "Multi-cloud"],
     1,
     "Mixing on-prem infrastructure (for compliance) with cloud resources for elasticity is the definition of a hybrid deployment, commonly implemented via Direct Connect, Outposts, or Storage Gateway."),

    ("Core Theory - Deployment Models",
     "Which AWS service physically extends AWS infrastructure and APIs into a customer's own data center for a hybrid deployment?",
     ["AWS Outposts", "AWS Snowball", "Amazon CloudFront", "AWS Direct Connect"],
     0,
     "AWS Outposts ships actual AWS-managed racks/hardware to run on-premises, giving a consistent hybrid experience with the same APIs and control plane as the cloud."),

    # ============================================================
    # CORE THEORY — 6 Advantages of Cloud Computing
    # ============================================================
    ("Core Theory - Advantages of Cloud",
     "A startup avoids buying physical servers upfront and instead pays monthly based on actual usage. Which of AWS's official cloud advantages does this represent?",
     ["Go global in minutes", "Trade capital expense for variable expense", "Economies of scale", "Increase speed and agility"],
     1,
     "Not having to spend large capital up front on hardware, and instead paying variable operating expense based on consumption, is precisely the CapEx-to-OpEx advantage AWS markets."),

    ("Core Theory - Advantages of Cloud",
     "A company launches its application in five new AWS Regions worldwide within a single afternoon to reach customers with low latency. Which cloud advantage is this?",
     ["Stop guessing capacity", "Go global in minutes", "Massive economies of scale", "Stop spending on data centers"],
     1,
     "Rapidly deploying infrastructure across multiple geographic Regions without building physical data centers is the 'go global in minutes' advantage."),

    # ============================================================
    # CORE THEORY — TCO
    # ============================================================
    ("Core Theory - TCO",
     "Which AWS tool is used to estimate and compare the cost of running a proposed architecture on AWS?",
     ["AWS Cost Explorer", "AWS Pricing Calculator", "AWS Budgets", "AWS Cost and Usage Report"],
     1,
     "The AWS Pricing Calculator estimates the cost of a planned architecture before you build it, replacing the legacy TCO/Simple Monthly Calculators — this is different from Cost Explorer, which analyzes historical/existing spend."),

    ("Core Theory - TCO",
     "When calculating Total Cost of Ownership (TCO) to justify a cloud migration, which factor is typically UNDER-counted by companies comparing on-prem to AWS?",
     ["Compute hardware cost", "Storage hardware cost", "IT labor, facilities (power/cooling/space), and over-provisioning for peak", "License cost of the OS"],
     2,
     "TCO comparisons often miss hidden on-prem costs like staffing, facilities, and the cost of over-provisioning to handle peak demand — these make on-prem look artificially cheaper than it is."),

    # ============================================================
    # CORE THEORY — Pricing Models (heavy/trap-prone)
    # ============================================================
    ("Core Theory - Pricing Models",
     "A batch-processing workload can tolerate interruptions and needs the cheapest possible compute. Which EC2 pricing model fits best?",
     ["On-Demand", "Reserved Instances", "Spot Instances", "Dedicated Hosts"],
     2,
     "Spot Instances offer up to 90% discount for fault-tolerant, flexible workloads that can handle a 2-minute interruption warning — ideal for batch jobs, not for anything requiring guaranteed uptime."),

    ("Core Theory - Pricing Models",
     "A company has steady, predictable EC2 usage for the next 3 years and wants the deepest possible discount tied to a specific instance family in a specific region. What should they buy?",
     ["Savings Plans", "Reserved Instances", "Spot Instances", "On-Demand"],
     1,
     "Reserved Instances lock in up to ~72% discount for steady, predictable workloads with a 1- or 3-year commitment — Savings Plans are more flexible across instance families/regions but RIs typically give the deepest discount for a fixed configuration."),

    ("Core Theory - Pricing Models",
     "A company wants a committed-spend discount that flexibly applies across EC2 instance families, sizes, OS, and regions — not tied to one specific instance type. What should they use?",
     ["Reserved Instances", "Savings Plans", "Spot Instances", "Dedicated Instances"],
     1,
     "Savings Plans commit to a $/hour spend and automatically apply the discount across instance families and regions, trading some discount depth for flexibility compared to Reserved Instances."),

    ("Core Theory - Pricing Models",
     "A financial services firm must run workloads on physical servers dedicated entirely to them due to strict licensing and compliance requirements. Which pricing/purchasing option fits?",
     ["Spot Instances", "On-Demand Instances", "Dedicated Hosts", "Savings Plans"],
     2,
     "Dedicated Hosts provide a physical server dedicated to a single customer, which is required for certain software licensing models (e.g., per-socket/per-core licenses) and strict compliance needs."),

    # ============================================================
    # CORE THEORY — Shared Responsibility Model (heavy/trap-prone)
    # ============================================================
    ("Core Theory - Shared Responsibility Model",
     "Under the AWS Shared Responsibility Model, which of these is ALWAYS AWS's responsibility regardless of the service used?",
     ["Guest OS patching", "Security groups configuration", "Physical security of data centers", "Customer data encryption choices"],
     2,
     "Physical security of the underlying facilities and hardware is 'security OF the cloud' — this never shifts to the customer, no matter which service (IaaS, PaaS, or serverless) is used."),

    ("Core Theory - Shared Responsibility Model",
     "For Amazon RDS, who is responsible for patching the underlying database engine software?",
     ["The customer, always", "AWS, since RDS is a managed service", "Split 50/50 by contract", "Neither — patching is optional"],
     1,
     "RDS is a managed service, so AWS handles OS and DB engine patching, while the customer remains responsible for things like access management, data, and query/schema design — this is the classic 'security IN the cloud' split."),

    ("Core Theory - Shared Responsibility Model",
     "Select TWO responsibilities that remain with the CUSTOMER even when using a fully serverless service like AWS Lambda or Amazon S3.",
     ["Physical hardware maintenance", "IAM access configuration", "Data classification and encryption choices", "Underlying host OS patching"],
     [1, 2],
     "Even in serverless services, AWS manages all infrastructure and OS patching, but the customer is always responsible for IAM permissions and how their own data is classified/encrypted — 'security IN the cloud' never fully disappears."),

    ("Core Theory - Shared Responsibility Model",
     "A company assumes AWS automatically encrypts and secures all of their S3 bucket contents by default with no configuration needed. What is wrong with this assumption?",
     ["S3 does not support encryption at all", "Bucket permissions and encryption configuration are the customer's responsibility under the Shared Responsibility Model", "AWS only encrypts data in Glacier, not S3", "This assumption is actually correct"],
     1,
     "This is a classic exam trap: AWS secures the underlying infrastructure, but bucket policies, public access settings, and encryption configuration are squarely the customer's responsibility — misconfigured S3 buckets are a top real-world breach cause."),

    # ============================================================
    # CORE THEORY — Support Plans (heavy)
    # ============================================================
    ("Core Theory - Support Plans",
     "A mission-critical production company needs a dedicated Technical Account Manager (TAM) and under-15-minute response times for critical issues. Which support plan is required?",
     ["Business", "Developer", "Enterprise", "Basic"],
     2,
     "Only the Enterprise support plan includes a dedicated TAM and the fastest <15-minute response SLA for business-critical system down issues."),

    ("Core Theory - Support Plans",
     "Which AWS Support plan is free and included automatically with every AWS account?",
     ["Basic", "Developer", "Business", "Enterprise On-Ramp"],
     0,
     "The Basic plan is free for all accounts and includes customer service, documentation, core Trusted Advisor checks, and the Personal Health Dashboard."),

    ("Core Theory - Support Plans",
     "A startup is testing a new application in a dev/test environment and wants business-hours email access to Cloud Support Associates without paying for 24/7 phone support. Which plan fits?",
     ["Basic", "Developer", "Business", "Enterprise"],
     1,
     "The Developer plan is aimed at early development/testing and provides business-hours email access to support engineers, without the 24/7 phone/chat access that Business tier adds."),

    ("Core Theory - Support Plans",
     "Which support tier is the first to include full access to ALL Trusted Advisor checks and 24/7 phone/chat/email support?",
     ["Developer", "Business", "Basic", "Enterprise On-Ramp only"],
     1,
     "Business is the first tier to unlock the full Trusted Advisor check set plus 24/7 phone/chat/email support with <1 hour response for urgent issues — a common exam distinction point."),

    # ============================================================
    # CORE THEORY — AWS CAF
    # ============================================================
    ("Core Theory - AWS CAF",
     "Which AWS CAF perspective focuses on organizational change management, training, and staffing during a cloud transformation?",
     ["Business", "People", "Governance", "Platform"],
     1,
     "The People perspective addresses how a cloud transformation affects staff — training, org change management, and staffing plans — distinct from Governance (risk/value) and Platform (architecture)."),

    ("Core Theory - AWS CAF",
     "Which THREE of the six AWS CAF perspectives are considered 'Technical capabilities' perspectives?",
     ["Business", "Platform", "People", "Security", "Governance", "Operations"],
     [1, 3, 5],
     "Platform, Security, and Operations form the technical capabilities group of AWS CAF, while Business, People, and Governance form the business capabilities group."),

    ("Core Theory - AWS CAF",
     "A company wants to ensure its cloud migration meets compliance objectives and manages security risk appropriately. Which CAF perspective is primarily responsible?",
     ["Operations", "Security", "Platform", "Business"],
     1,
     "The Security perspective of AWS CAF exists specifically to ensure the organization meets its security and compliance objectives throughout the cloud journey."),

    # ============================================================
    # CORE THEORY — Well-Architected Framework
    # ============================================================
    ("Core Theory - Well-Architected Framework",
     "Which Well-Architected Framework pillar focuses specifically on the ability to recover from failures and dynamically meet changing demand?",
     ["Operational Excellence", "Reliability", "Performance Efficiency", "Cost Optimization"],
     1,
     "Reliability is about recovering from infrastructure or service disruptions and dynamically acquiring resources to meet demand, distinct from Performance Efficiency, which is about efficient resource use."),

    ("Core Theory - Well-Architected Framework",
     "Which free AWS tool lets you self-review a workload against the Well-Architected Framework's six pillars?",
     ["AWS Trusted Advisor", "AWS Well-Architected Tool", "AWS Compute Optimizer", "AWS Config"],
     1,
     "The AWS Well-Architected Tool is a free, self-service tool specifically designed to review workloads against the framework's six pillars, unlike Trusted Advisor which gives general best-practice checks."),

    ("Core Theory - Well-Architected Framework",
     "A company wants to reduce its environmental footprint by choosing efficient regions and right-sizing workloads. Which Well-Architected pillar covers this most directly?",
     ["Cost Optimization", "Sustainability", "Reliability", "Security"],
     1,
     "Sustainability was added as the sixth pillar specifically to address minimizing the environmental impact of cloud workloads — this is a newer pillar the exam likes to test recognition of."),

    # ============================================================
    # CORE THEORY — 7 R's of Migration (trap-prone)
    # ============================================================
    ("Core Theory - 7 Rs of Migration",
     "A company moves its on-premises application to EC2 with minimal code changes using AWS Application Migration Service (MGN). Which migration strategy is this?",
     ["Refactor", "Replatform", "Rehost", "Repurchase"],
     2,
     "'Lift and shift' with minimal changes, typically done via AWS MGN, is Rehost — the most common first step in large migrations because it's fast and low-risk."),

    ("Core Theory - 7 Rs of Migration",
     "A company decides to stop using its self-hosted CRM and instead subscribe to a SaaS CRM product. Which migration strategy does this represent?",
     ["Retain", "Repurchase", "Relocate", "Retire"],
     1,
     "Switching to a different product entirely, often SaaS, is called 'Repurchase' or 'drop and shop' — it is not simply moving the same software, but replacing it."),

    ("Core Theory - 7 Rs of Migration",
     "A company redesigns a monolithic application into microservices using Lambda and managed services to be fully cloud-native. Which migration strategy is this?",
     ["Replatform", "Rehost", "Refactor/Re-architect", "Relocate"],
     2,
     "Refactor/Re-architect involves redesigning the application architecture itself to be cloud-native, usually justified by a strong business driver like scalability, not just moving it as-is."),

    ("Core Theory - 7 Rs of Migration",
     "A legacy application is identified as no longer used by anyone and is simply decommissioned before migration planning begins. Which of the 7 Rs is this?",
     ["Retain", "Retire", "Rehost", "Replatform"],
     1,
     "Retire means decommissioning applications that are no longer needed — a common exam trap is confusing this with 'Retain,' which means keeping something on-premises as-is."),

    # ============================================================
    # CORE THEORY — Global Infrastructure
    # ============================================================
    ("Core Theory - Global Infrastructure",
     "Which AWS Global Infrastructure component consists of one or more discrete data centers with independent power, cooling, and networking, connected via low-latency links within a Region?",
     ["Edge Location", "Availability Zone", "Local Zone", "Wavelength Zone"],
     1,
     "An Availability Zone (AZ) is one or more discrete data centers within a Region, isolated from failures in other AZs but connected with low-latency, high-throughput networking."),

    ("Core Theory - Global Infrastructure",
     "A mobile gaming company needs ultra-low-latency compute embedded directly within telecom 5G networks for their real-time multiplayer game. Which AWS infrastructure feature fits?",
     ["Local Zones", "Wavelength Zones", "Edge Locations", "Availability Zones"],
     1,
     "Wavelength Zones embed AWS compute and storage services within telecommunications providers' 5G networks, minimizing latency for applications that need to reach mobile devices extremely fast."),

    ("Core Theory - Global Infrastructure",
     "Which infrastructure component is used by CloudFront and Route 53 to cache content and respond to requests physically closer to end users, and there are more of these than there are Regions or AZs?",
     ["Local Zones", "Edge Locations", "Availability Zones", "Wavelength Zones"],
     1,
     "Edge Locations are the most numerous AWS infrastructure points globally, used by CloudFront (CDN caching) and Route 53 (DNS resolution) to reduce latency for end users."),

    ("Core Theory - Global Infrastructure",
     "A media company in Mumbai wants to extend AWS closer to a large population center for latency-sensitive rendering workloads, without a full Region being available nearby. What should they use?",
     ["Local Zones", "Wavelength Zones", "Direct Connect", "Snow Family"],
     0,
     "Local Zones extend a parent Region's infrastructure closer to large population and industry centers to serve latency-sensitive applications where no full Region exists."),

    # ============================================================
    # CORE THEORY — Compliance & Governance
    # ============================================================
    ("Core Theory - Compliance & Governance",
     "Which AWS service provides on-demand access to compliance reports like SOC 1/2/3, PCI-DSS, and ISO certifications?",
     ["AWS Config", "AWS Artifact", "AWS Audit Manager", "AWS Trusted Advisor"],
     1,
     "AWS Artifact is the self-service portal specifically for downloading AWS's compliance reports and agreements — Audit Manager instead automates evidence collection for the customer's OWN audits."),

    ("Core Theory - Compliance & Governance",
     "A company wants to centrally manage billing across 20 linked AWS accounts and get volume pricing discounts as if they were one account. What feature enables this?",
     ["Service Control Policies", "Consolidated Billing (via AWS Organizations)", "AWS Budgets", "AWS Cost and Usage Report"],
     1,
     "Consolidated Billing, part of AWS Organizations, combines usage across linked accounts into a single payment method and unlocks volume-based discounts across the whole organization."),

    ("Core Theory - Compliance & Governance",
     "Which AWS Organizations feature is used to set guardrails that define the MAXIMUM permissions available to accounts within an Organizational Unit?",
     ["IAM Policies", "Service Control Policies (SCPs)", "Resource-based policies", "Permission Boundaries"],
     1,
     "SCPs act as guardrails at the Organization/OU level, defining the maximum permissions accounts can have — they never grant permissions by themselves, only restrict what IAM can allow."),

    ("Core Theory - Compliance & Governance",
     "According to AWS best practice, how should the AWS account root user be used day-to-day?",
     ["As the primary login for daily administrative tasks", "It should be locked down with MFA and not used for daily work; IAM users/roles should be used instead", "Shared among all team members for convenience", "Deleted immediately after account creation"],
     1,
     "AWS strongly recommends securing the root user with MFA and reserving it only for a small number of account-management tasks, while daily operations should use least-privilege IAM users or roles."),

    # ============================================================
    # CORE THEORY — Common Exam Trap Questions (explicit)
    # ============================================================
    ("Core Theory - Exam Traps",
     "EXAM TRAP: A company needs an active-active database that accepts writes in multiple Regions simultaneously with low-latency global access. Which is CORRECT?",
     ["Aurora Global Database (default configuration)", "DynamoDB Global Tables", "RDS Multi-AZ", "S3 Cross-Region Replication"],
     1,
     "This is a classic CCP trap: Aurora Global Database is primarily single-write-region with cross-region DR/read-scaling (unless write forwarding is explicitly enabled), while DynamoDB Global Tables natively support true multi-active writes across regions."),

    ("Core Theory - Exam Traps",
     "EXAM TRAP: A company needs to move 500 TB of data to AWS but only has a slow, unreliable internet connection. Which service is correct, and which is the trap answer?",
     ["Correct: Snow Family (physical device); Trap: Direct Connect (too slow for a one-time massive transfer)", "Correct: Direct Connect; Trap: Snowball", "Correct: Storage Gateway; Trap: DataSync", "Correct: S3 Transfer Acceleration; Trap: Snowmobile"],
     0,
     "For very large one-time offline transfers, the Snow Family (Snowcone/Snowball/Snowmobile) physically ships data — Direct Connect is a network link and is the wrong (and slower/costlier) tool for a single huge bulk transfer."),

    ("Core Theory - Exam Traps",
     "EXAM TRAP: A company needs to store database credentials that automatically rotate on a schedule. Many candidates incorrectly pick SSM Parameter Store. What's the correct answer and why?",
     ["Parameter Store, because it stores config data", "Secrets Manager, because it supports automatic rotation of secrets like DB credentials", "KMS, because it manages encryption keys", "CloudHSM, because it stores keys"],
     1,
     "Parameter Store is a general-purpose config/parameter store and does NOT auto-rotate by default, while Secrets Manager is purpose-built to securely store AND automatically rotate secrets like database credentials."),

    ("Core Theory - Exam Traps",
     "EXAM TRAP: A security team needs to know exactly WHICH IAM user deleted a specific S3 bucket and when. Which service answers this, and which commonly-confused service does NOT?",
     ["CloudTrail answers this; CloudWatch (metrics/performance monitoring) does not", "CloudWatch answers this; CloudTrail does not", "Config answers this; CloudTrail does not", "Trusted Advisor answers this; Config does not"],
     0,
     "CloudTrail logs 'who did what' — every API call and user identity — making it the tool for auditing actions, while CloudWatch focuses on operational metrics, logs, and alarms, not identity-based auditing."),

    ("Core Theory - Exam Traps",
     "EXAM TRAP: A company wants the cheapest possible DR strategy with a fast recovery time, without running a full always-on duplicate environment in a second region. What's the trap and the correct choice?",
     ["Trap: always maintain a full multi-region active-active stack; Correct: Pilot Light/Warm Standby via AWS Elastic Disaster Recovery", "Trap: use Snowball; Correct: use S3 Glacier", "Trap: use CloudFront; Correct: use Route 53", "Trap: use RDS snapshots only; Correct: use Multi-AZ"],
     0,
     "The exam often tests whether you know that a full always-on multi-region setup is expensive and unnecessary for most DR needs — cheaper Pilot Light/Warm Standby patterns via AWS Elastic Disaster Recovery balance cost and recovery speed."),

    # ============================================================
    # SERVICE CATEGORY 1 — Analytics
    # ============================================================
    ("Analytics",
     "A team wants to run ad-hoc SQL queries directly against data stored in S3 without provisioning any servers, paying only per query. Which service fits?",
     ["Amazon Redshift", "Amazon Athena", "Amazon EMR", "AWS Glue"],
     1,
     "Amazon Athena is a serverless SQL query engine that queries data directly in S3, charging per amount of data scanned — no cluster to manage, unlike Redshift or EMR."),

    ("Analytics",
     "A company needs to crawl multiple data sources, build a data catalog, and transform data between different stores in a serverless ETL pipeline. Which service is designed for this?",
     ["AWS Glue", "Amazon Kinesis", "Amazon MSK", "Amazon QuickSight"],
     0,
     "AWS Glue is a serverless ETL service that crawls sources, builds a catalog, and performs transformations — this is its defining exam use case."),

    ("Analytics",
     "Which service is a managed, petabyte-scale data warehouse purpose-built for OLAP-style analytics queries?",
     ["Amazon RDS", "Amazon Redshift", "Amazon DynamoDB", "Amazon Neptune"],
     1,
     "Amazon Redshift is AWS's managed data warehouse designed for large-scale analytical (OLAP) queries, distinct from RDS which serves OLTP transactional workloads."),

    ("Analytics",
     "A company needs to ingest and process real-time clickstream data at massive scale as it happens. Which service is purpose-built for this?",
     ["Amazon Kinesis", "AWS Data Exchange", "Amazon OpenSearch Service", "Amazon QuickSight"],
     0,
     "Amazon Kinesis is built specifically for real-time streaming data ingestion and processing, such as clickstreams or IoT telemetry."),

    ("Analytics",
     "A company wants to build interactive BI dashboards from their data without managing any backend servers. Which service should they choose?",
     ["Amazon QuickSight", "Amazon EMR", "Amazon Redshift", "AWS Glue"],
     0,
     "Amazon QuickSight is AWS's serverless business intelligence tool for building dashboards and visualizations directly from various data sources."),

    # ============================================================
    # SERVICE CATEGORY 2 — Application Integration
    # ============================================================
    ("Application Integration",
     "A company needs to decouple two application components using a pull-based managed message queue so that messages aren't lost if the consumer is temporarily down. Which service fits?",
     ["Amazon SNS", "Amazon SQS", "Amazon EventBridge", "AWS Step Functions"],
     1,
     "Amazon SQS is a pull-based managed queue used to decouple producers and consumers, buffering messages reliably until they're processed — SNS is push-based pub/sub, not a queue."),

    ("Application Integration",
     "Which service is best suited to orchestrate a multi-step serverless workflow using visual state machines that coordinate Lambda functions and other AWS services?",
     ["Amazon EventBridge", "AWS Step Functions", "Amazon SQS", "Amazon SNS"],
     1,
     "AWS Step Functions is purpose-built as a serverless workflow orchestrator using visual state machines, distinct from SNS/SQS which are messaging primitives, not orchestrators."),

    ("Application Integration",
     "A company wants to fan out a single event to multiple subscribers — email, SMS, an SQS queue, and a Lambda function — all at once. Which service is designed for this?",
     ["Amazon SQS", "Amazon SNS", "AWS Step Functions", "Amazon EventBridge"],
     1,
     "Amazon SNS is a pub/sub push notification service designed exactly for fan-out delivery to multiple heterogeneous subscriber types simultaneously."),

    ("Application Integration",
     "Which service acts as a serverless event bus that routes events between AWS services, SaaS applications, and custom applications based on rules?",
     ["Amazon EventBridge", "Amazon SQS", "AWS Step Functions", "Amazon SNS"],
     0,
     "Amazon EventBridge is the serverless event bus specifically designed to route events by rule-based matching across AWS services, SaaS partners, and custom apps."),

    # ============================================================
    # SERVICE CATEGORY 3 — Business Applications
    # ============================================================
    ("Business Applications",
     "A company wants to launch a cloud-based call center without building any physical telephony infrastructure. Which AWS service fits?",
     ["Amazon Connect", "Amazon SES", "Amazon Chime", "Amazon WorkMail"],
     0,
     "Amazon Connect is AWS's cloud-based contact center service, letting companies set up call centers without physical telephony hardware."),

    ("Business Applications",
     "Which service is designed to send large volumes of transactional and marketing emails at scale?",
     ["Amazon SES", "Amazon Connect", "Amazon SNS", "Amazon WorkMail"],
     0,
     "Amazon SES (Simple Email Service) is purpose-built for sending and receiving bulk transactional and marketing email, unlike SNS which is a general pub/sub notification service."),

    # ============================================================
    # SERVICE CATEGORY 4 — Cloud Financial Management
    # ============================================================
    ("Cloud Financial Management",
     "A finance team needs the most granular, detailed line-item breakdown of AWS costs and usage, exported as CSV to S3 for further analysis. Which service provides this?",
     ["AWS Cost Explorer", "AWS Budgets", "AWS Cost and Usage Report", "AWS Billing Conductor"],
     2,
     "The AWS Cost and Usage Report (CUR) is the most detailed, granular cost/usage data source available, delivered as CSV files to S3 — Cost Explorer is for visualization/forecasting, not raw granular data."),

    ("Cloud Financial Management",
     "Which service allows a company to set custom spending thresholds and receive alerts when actual or forecasted costs exceed them?",
     ["AWS Budgets", "AWS Cost Explorer", "AWS Marketplace", "AWS Billing Conductor"],
     0,
     "AWS Budgets lets you define custom cost, usage, RI, or Savings Plan budgets and triggers alerts when thresholds are breached or forecasted to be breached."),

    ("Cloud Financial Management",
     "A managed service provider wants to customize and rebill AWS costs to its own end customers with custom pricing. Which service supports this?",
     ["AWS Billing Conductor", "AWS Cost Explorer", "AWS Budgets", "AWS Marketplace"],
     0,
     "AWS Billing Conductor is specifically designed to let resellers/MSPs customize and rebill costs to internal teams or external customers using custom billing groups."),

    # ============================================================
    # SERVICE CATEGORY 5 — Compute
    # ============================================================
    ("Compute",
     "A small business wants a simple, fixed-price virtual private server without needing to configure VPCs, security groups, or complex networking. Which service is ideal?",
     ["Amazon EC2", "Amazon Lightsail", "AWS Outposts", "AWS Batch"],
     1,
     "Amazon Lightsail is a simplified VPS product with fixed, predictable pricing aimed at simple workloads — full EC2 offers more control but more complexity."),

    ("Compute",
     "A media company needs to run thousands of parallel batch computing jobs and wants AWS to automatically provision the right amount and type of compute resources for the job queue. Which service fits?",
     ["AWS Batch", "AWS Elastic Beanstalk", "Amazon EC2 Auto Scaling", "AWS Fargate"],
     0,
     "AWS Batch is purpose-built for batch computing jobs, automatically provisioning the optimal compute resources based on job requirements and volume/queue depth."),

    ("Compute",
     "A developer wants to upload application code and have AWS automatically handle provisioning, load balancing, and scaling, without manually configuring the underlying EC2 infrastructure. What should they use?",
     ["AWS Elastic Beanstalk", "Amazon EC2", "AWS Lambda", "Amazon Lightsail"],
     0,
     "Elastic Beanstalk is a PaaS offering — you upload code and AWS handles provisioning, scaling, and deployment infrastructure automatically using EC2 Auto Scaling under the hood."),

    ("Compute",
     "Which AWS compute-related infrastructure is embedded within telecommunications providers' 5G networks for ultra-low-latency use cases?",
     ["AWS Local Zones", "AWS Wavelength", "AWS Outposts", "AWS Batch"],
     1,
     "AWS Wavelength embeds AWS compute and storage services directly within telecom 5G networks, minimizing latency to mobile and connected devices."),

    ("Compute",
     "A retailer needs their own AWS hardware physically installed in their data center for workloads that must remain fully on-premises but managed consistently with the AWS cloud experience. Which service?",
     ["AWS Outposts", "AWS Local Zones", "AWS Wavelength", "AWS Direct Connect"],
     0,
     "AWS Outposts delivers actual AWS hardware/racks to run on-premises, giving a consistent hybrid cloud experience — Local Zones and Wavelength instead extend AWS infrastructure into external locations, not customer premises."),

    # ============================================================
    # SERVICE CATEGORY 6 — Containers
    # ============================================================
    ("Containers",
     "A company wants a fully managed Kubernetes control plane on AWS without managing the Kubernetes masters themselves. Which service fits?",
     ["Amazon ECS", "Amazon EKS", "Amazon ECR", "AWS Fargate"],
     1,
     "Amazon EKS is AWS's managed Kubernetes offering, handling the control plane so customers don't need to manage Kubernetes master nodes themselves."),

    ("Containers",
     "Which service is a private, managed registry for storing and retrieving Docker container images?",
     ["Amazon ECR", "Amazon ECS", "Amazon EKS", "AWS CodeArtifact"],
     0,
     "Amazon ECR (Elastic Container Registry) is the managed Docker image registry, while ECS/EKS are container orchestration services that consume images from it."),

    ("Containers",
     "A company wants AWS-native container orchestration (not Kubernetes) that's tightly integrated with other AWS services. Which service fits?",
     ["Amazon EKS", "Amazon ECS", "Amazon ECR", "AWS Batch"],
     1,
     "Amazon ECS is AWS's own native container orchestration service, distinct from EKS which runs the open-source Kubernetes control plane."),

    # ============================================================
    # SERVICE CATEGORY 7 — Customer Engagement
    # ============================================================
    ("Customer Engagement",
     "A new startup wants free AWS credits, training, and support to help them get started building on AWS. Which program should they apply to?",
     ["AWS IQ", "AWS Activate for Startups", "AWS Managed Services", "AWS Support"],
     1,
     "AWS Activate for Startups provides free credits, training resources, and support specifically designed to help early-stage startups build on AWS."),

    ("Customer Engagement",
     "A company needs to hire a certified freelance AWS expert for a short-term project without going through a full consulting firm. Which service connects them?",
     ["AWS IQ", "AWS Managed Services", "AWS Marketplace", "AWS Activate"],
     0,
     "AWS IQ is a marketplace specifically for finding and hiring AWS-certified freelance experts for project-based work."),

    # ============================================================
    # SERVICE CATEGORY 8 — Database (heavy, Multi-AZ vs Read Replica trap)
    # ============================================================
    ("Database",
     "EXAM TRAP: What is the KEY difference between RDS Multi-AZ and RDS Read Replicas?",
     ["They are functionally identical", "Multi-AZ is for high availability/failover (synchronous, standby not normally readable); Read Replicas are for scaling reads (asynchronous, can be cross-region, and are readable)", "Multi-AZ is for scaling reads; Read Replicas are for failover", "Read Replicas require manual failover but Multi-AZ does not support failover at all"],
     1,
     "This is one of the most commonly tested distinctions on the CCP exam: Multi-AZ exists purely for HA/DR via synchronous replication to a standby (not normally used for read traffic), while Read Replicas scale read throughput asynchronously and can even span regions."),

    ("Database",
     "A gaming company needs a serverless NoSQL database with single-digit millisecond latency at any scale. Which database fits?",
     ["Amazon RDS", "Amazon DynamoDB", "Amazon Neptune", "Amazon Redshift"],
     1,
     "DynamoDB is AWS's serverless NoSQL key-value/document database purpose-built for consistent single-digit millisecond latency at virtually unlimited scale."),

    ("Database",
     "Which managed relational database is compatible with MySQL and PostgreSQL and is known for higher performance and availability than standard RDS engines?",
     ["Amazon Aurora", "Amazon DynamoDB", "Amazon Neptune", "Amazon MemoryDB"],
     0,
     "Amazon Aurora is AWS's own high-performance, MySQL/PostgreSQL-compatible relational database, engineered for greater throughput and availability than standard RDS engines."),

    ("Database",
     "A social network needs a database optimized for storing and querying highly connected data, such as relationships between users. Which service fits?",
     ["Amazon Neptune", "Amazon DynamoDB", "Amazon RDS", "Amazon Redshift"],
     0,
     "Amazon Neptune is a managed graph database purpose-built for highly connected data and relationship-heavy queries, such as social graphs or recommendation engines."),

    ("Database",
     "A company needs a Redis-compatible, durable, in-memory database for microsecond read latency in a mission-critical application. Which service fits?",
     ["Amazon ElastiCache", "Amazon MemoryDB for Redis", "Amazon DynamoDB Accelerator (DAX)", "Amazon Neptune"],
     1,
     "Amazon MemoryDB for Redis provides Redis compatibility with full durability and microsecond read latency, targeted at mission-critical primary database use cases rather than just caching."),

    ("Database",
     "Select TWO databases from the following that are classified as relational (SQL) databases on AWS.",
     ["Amazon DynamoDB", "Amazon RDS", "Amazon Aurora", "Amazon Neptune"],
     [1, 2],
     "Amazon RDS and Amazon Aurora are both relational (SQL) database services, while DynamoDB is NoSQL and Neptune is a graph database — a common multi-select classification trap."),

    # ============================================================
    # SERVICE CATEGORY 9 — Developer Tools
    # ============================================================
    ("Developer Tools",
     "A developer wants a browser-based shell that is pre-authenticated with their AWS console credentials, requiring no local setup. Which service fits?",
     ["AWS Cloud9", "AWS CloudShell", "AWS CLI", "AWS CodeCommit"],
     1,
     "AWS CloudShell provides an instant, browser-based shell pre-authenticated with the console session's credentials — no local install or setup required, unlike the AWS CLI which runs locally."),

    ("Developer Tools",
     "Which service compiles source code, runs tests, and produces deployable build artifacts as part of a CI/CD pipeline?",
     ["AWS CodeDeploy", "AWS CodeBuild", "AWS CodePipeline", "AWS CodeCommit"],
     1,
     "AWS CodeBuild is the managed build service that compiles code and runs tests, distinct from CodeDeploy (which deploys the resulting artifacts) and CodePipeline (which orchestrates the whole pipeline)."),

    ("Developer Tools",
     "A team wants to orchestrate the entire build-test-deploy release process across multiple stages automatically. Which service is the orchestrator?",
     ["AWS CodePipeline", "AWS CodeBuild", "AWS CodeDeploy", "AWS X-Ray"],
     0,
     "AWS CodePipeline is the CI/CD orchestration service that automates and sequences the build, test, and deploy stages, typically calling CodeBuild and CodeDeploy along the way."),

    ("Developer Tools",
     "Which service helps developers debug and analyze performance bottlenecks across distributed microservices by tracing requests end-to-end?",
     ["AWS X-Ray", "Amazon CloudWatch", "AWS CloudTrail", "AWS Config"],
     0,
     "AWS X-Ray provides distributed tracing specifically designed to visualize and debug how requests flow through and perform across microservices."),

    # ============================================================
    # SERVICE CATEGORY 10 — End User Computing
    # ============================================================
    ("End User Computing",
     "A company wants employees to access a fully managed virtual desktop (VDI) from any device. Which service fits?",
     ["Amazon WorkSpaces", "Amazon AppStream 2.0", "Amazon WorkSpaces Web", "AWS Client VPN"],
     0,
     "Amazon WorkSpaces provides managed, persistent cloud-based virtual desktops (VDI), distinct from AppStream 2.0 which streams individual applications rather than a full desktop."),

    ("End User Computing",
     "A software vendor wants to stream a single desktop application to users' browsers without requiring any local installation. Which service is designed for this specific use case?",
     ["Amazon WorkSpaces", "Amazon AppStream 2.0", "AWS Amplify", "Amazon WorkSpaces Web"],
     1,
     "Amazon AppStream 2.0 streams individual applications (not a full desktop) to a browser, ideal for vendors distributing a specific app without installation."),

    # ============================================================
    # SERVICE CATEGORY 11 — Frontend Web and Mobile
    # ============================================================
    ("Frontend Web and Mobile",
     "A startup wants to quickly build, deploy, and host a full-stack web and mobile application with built-in CI/CD, hosting, and backend integration. Which service fits?",
     ["AWS Amplify", "AWS AppSync", "AWS Device Farm", "Amazon API Gateway"],
     0,
     "AWS Amplify is the framework/toolset designed to rapidly build, deploy, and host full-stack web and mobile applications end-to-end."),

    ("Frontend Web and Mobile",
     "Which service allows developers to test their mobile and web applications on real physical devices in the cloud rather than emulators?",
     ["AWS Device Farm", "AWS Amplify", "AWS AppSync", "Amazon Cognito"],
     0,
     "AWS Device Farm provides access to real physical devices in the cloud specifically for app testing, giving more accurate results than emulators."),

    # ============================================================
    # SERVICE CATEGORY 12 — Internet of Things (IoT)
    # ============================================================
    ("Internet of Things (IoT)",
     "Which service securely connects and manages billions of IoT devices, enabling them to interact with cloud applications and each other?",
     ["AWS IoT Core", "AWS IoT Greengrass", "Amazon Kinesis", "AWS Wavelength"],
     0,
     "AWS IoT Core is the core managed service that securely connects and manages billions of IoT devices and routes their data to the cloud."),

    ("Internet of Things (IoT)",
     "A factory needs its IoT devices to keep operating and making local decisions even when their internet connection to AWS is temporarily lost. Which service enables this edge capability?",
     ["AWS IoT Greengrass", "AWS IoT Core", "AWS Outposts", "AWS Wavelength"],
     0,
     "AWS IoT Greengrass extends AWS to edge devices, enabling local compute, messaging, and data sync even during intermittent connectivity — distinct from IoT Core, which is the cloud-side connection hub."),

    # ============================================================
    # SERVICE CATEGORY 13 — Machine Learning
    # ============================================================
    ("Machine Learning",
     "A company wants to automatically extract text and structured data from scanned invoices and forms. Which service fits?",
     ["Amazon Textract", "Amazon Rekognition", "Amazon Comprehend", "Amazon Transcribe"],
     0,
     "Amazon Textract is purpose-built OCR-plus service for extracting text and structured data (like tables and forms) from scanned documents."),

    ("Machine Learning",
     "A company wants to build a chatbot that understands natural spoken or typed language, using the same underlying technology as Amazon Alexa. Which service fits?",
     ["Amazon Lex", "Amazon Polly", "Amazon Comprehend", "Amazon Kendra"],
     0,
     "Amazon Lex is the service for building conversational chatbots/voicebots and is built on the same technology that powers Alexa."),

    ("Machine Learning",
     "Which service converts written text into natural-sounding speech audio?",
     ["Amazon Transcribe", "Amazon Polly", "Amazon Translate", "Amazon Comprehend"],
     1,
     "Amazon Polly performs text-to-speech, the reverse operation of Amazon Transcribe, which converts speech audio into text."),

    ("Machine Learning",
     "A data science team wants a fully managed platform to build, train, and deploy their own custom machine learning models at scale. Which service fits?",
     ["Amazon SageMaker", "Amazon Comprehend", "Amazon Rekognition", "Amazon Kendra"],
     0,
     "Amazon SageMaker is the fully managed end-to-end platform for building, training, and deploying custom ML models, distinct from the pre-built AI services like Rekognition or Comprehend."),

    ("Machine Learning",
     "Select TWO services that are pre-built AI services requiring NO custom model training by the customer.",
     ["Amazon SageMaker", "Amazon Rekognition", "Amazon Comprehend", "AWS Glue"],
     [1, 2],
     "Rekognition (image/video analysis) and Comprehend (NLP) are both ready-to-use pre-trained AI services, while SageMaker is the platform for building and training your OWN custom models."),

    # ============================================================
    # SERVICE CATEGORY 14 — Management and Governance
    # ============================================================
    ("Management and Governance",
     "Which service allows infrastructure to be defined and provisioned as code using declarative templates?",
     ["AWS Config", "AWS CloudFormation", "AWS Control Tower", "AWS Systems Manager"],
     1,
     "AWS CloudFormation is AWS's Infrastructure as Code service, letting you define resources in templates that get provisioned consistently and repeatably."),

    ("Management and Governance",
     "A company wants to track configuration changes to their AWS resources over time and evaluate compliance against defined rules. Which service fits?",
     ["AWS CloudTrail", "AWS Config", "Amazon CloudWatch", "AWS Trusted Advisor"],
     1,
     "AWS Config tracks resource configuration changes over time and evaluates them against compliance rules — distinct from CloudTrail, which logs API activity/actions rather than configuration state."),

    ("Management and Governance",
     "Which service provides automated checks across cost optimization, security, performance, and fault tolerance categories as best-practice recommendations?",
     ["AWS Trusted Advisor", "AWS Config", "AWS Compute Optimizer", "AWS Health Dashboard"],
     0,
     "AWS Trusted Advisor performs automated best-practice checks across cost, security, performance, and fault-tolerance categories, with deeper checks unlocked at higher support tiers."),

    ("Management and Governance",
     "A company wants to quickly set up a secure, compliant, multi-account AWS landing zone with guardrails built in from the start. Which service is designed for this?",
     ["AWS Organizations only", "AWS Control Tower", "AWS Config", "AWS License Manager"],
     1,
     "AWS Control Tower automates the setup of a secure, well-governed multi-account landing zone, building on top of AWS Organizations with pre-configured guardrails."),

    ("Management and Governance",
     "Which service gives ML-based recommendations for right-sizing EC2 instances, EBS volumes, and Lambda functions to optimize cost and performance?",
     ["AWS Trusted Advisor", "AWS Compute Optimizer", "AWS Cost Explorer", "AWS Config"],
     1,
     "AWS Compute Optimizer uses machine learning to analyze utilization and recommend optimal resource sizing across EC2, EBS, and Lambda — distinct from Trusted Advisor's broader best-practice checks."),

    # ============================================================
    # SERVICE CATEGORY 15 — Migration and Transfer
    # ============================================================
    ("Migration and Transfer",
     "Before planning a migration, a company wants to automatically discover their on-premises servers, applications, and dependencies. Which service fits?",
     ["AWS Application Discovery Service", "AWS Application Migration Service", "AWS Migration Hub", "AWS SCT"],
     0,
     "AWS Application Discovery Service is specifically for discovering on-prem servers, apps, and their dependencies to inform migration planning, before any actual migration tooling is used."),

    ("Migration and Transfer",
     "A company needs to migrate their on-premises Oracle database to a different target engine and must first convert the database schema to be compatible. Which service fits?",
     ["AWS DMS", "AWS SCT (Schema Conversion Tool)", "AWS Migration Hub", "AWS Transfer Family"],
     1,
     "AWS SCT converts the source database schema to be compatible with a different target database engine, typically used together with AWS DMS which then migrates the actual data."),

    ("Migration and Transfer",
     "Which service provides a single central dashboard to track the progress of migrations happening across multiple different AWS migration tools?",
     ["AWS Migration Hub", "AWS Application Discovery Service", "AWS DMS", "AWS SCT"],
     0,
     "AWS Migration Hub is the central dashboard that aggregates and tracks migration progress across tools like DMS, MGN, and SCT in one place."),

    ("Migration and Transfer",
     "A company wants to allow external partners to upload files via SFTP directly into an S3 bucket, without managing their own FTP server. Which service fits?",
     ["AWS Transfer Family", "AWS DataSync", "AWS Storage Gateway", "AWS Snowball"],
     0,
     "AWS Transfer Family provides fully managed SFTP/FTPS/FTP endpoints that deliver files directly into S3 or EFS, eliminating the need to run and maintain your own FTP servers."),

    # ============================================================
    # SERVICE CATEGORY 16 — Networking and Content Delivery
    # ============================================================
    ("Networking and Content Delivery",
     "A media company wants to cache and deliver video content to users worldwide from edge locations closest to them. Which service fits?",
     ["Amazon Route 53", "Amazon CloudFront", "AWS Global Accelerator", "AWS Direct Connect"],
     1,
     "Amazon CloudFront is AWS's global CDN, caching content at edge locations closest to end users to reduce latency for content delivery."),

    ("Networking and Content Delivery",
     "A company needs a dedicated, private, high-bandwidth network connection from their on-premises data center to AWS, bypassing the public internet. Which service fits?",
     ["AWS VPN", "AWS Direct Connect", "Amazon VPC", "AWS Global Accelerator"],
     1,
     "AWS Direct Connect provides a dedicated private physical network link to AWS, offering more consistent bandwidth/latency than an internet-based VPN connection."),

    ("Networking and Content Delivery",
     "Which service provides scalable, managed DNS resolution along with domain registration and health checks?",
     ["Amazon CloudFront", "Amazon Route 53", "AWS Global Accelerator", "Amazon API Gateway"],
     1,
     "Amazon Route 53 is AWS's managed DNS service, also handling domain registration and health checks for routing decisions like failover."),

    ("Networking and Content Delivery",
     "A company wants to route user traffic to the healthiest and lowest-latency application endpoint using AWS's global network backbone, improving performance for non-HTTP TCP/UDP traffic too. Which service fits?",
     ["Amazon CloudFront", "AWS Global Accelerator", "Amazon Route 53", "AWS VPN"],
     1,
     "AWS Global Accelerator routes traffic over AWS's global network backbone to the optimal healthy endpoint, and unlike CloudFront (HTTP/S focused), it also improves performance for non-HTTP TCP/UDP traffic."),

    ("Networking and Content Delivery",
     "Which service lets you create, publish, secure, and monitor REST and WebSocket APIs at scale without managing servers?",
     ["Amazon API Gateway", "AWS AppSync", "Amazon VPC", "AWS Direct Connect"],
     0,
     "Amazon API Gateway is the fully managed service purpose-built for creating, publishing, and securing REST/WebSocket APIs, distinct from AppSync which is GraphQL-focused."),

    # ============================================================
    # SERVICE CATEGORY 17 — Security, Identity, and Compliance (heavy)
    # ============================================================
    ("Security, Identity, and Compliance",
     "Which service provides ML-based, intelligent threat detection by continuously analyzing account and network activity logs for malicious behavior?",
     ["Amazon Inspector", "Amazon GuardDuty", "Amazon Macie", "AWS Security Hub"],
     1,
     "Amazon GuardDuty uses machine learning to continuously analyze logs (VPC Flow Logs, DNS, CloudTrail) for malicious or unauthorized behavior — distinct from Inspector, which scans for vulnerabilities in workloads."),

    ("Security, Identity, and Compliance",
     "A company needs to automatically discover and protect sensitive personally identifiable information (PII) stored in their S3 buckets. Which service fits?",
     ["Amazon Macie", "Amazon GuardDuty", "AWS Firewall Manager", "Amazon Detective"],
     0,
     "Amazon Macie uses ML specifically to discover and classify sensitive data like PII within S3, distinct from GuardDuty's broader threat detection scope."),

    ("Security, Identity, and Compliance",
     "Which service provides a single-tenant, dedicated hardware security module for organizations with strict compliance requirements around key storage?",
     ["AWS KMS", "AWS CloudHSM", "AWS Secrets Manager", "AWS Certificate Manager"],
     1,
     "AWS CloudHSM provides dedicated, single-tenant hardware security modules for customers needing full control over cryptographic keys for strict compliance needs, unlike the multi-tenant AWS KMS."),

    ("Security, Identity, and Compliance",
     "Which service provisions, manages, and automatically renews free public SSL/TLS certificates for use with services like CloudFront and ELB?",
     ["AWS CloudHSM", "AWS Certificate Manager (ACM)", "AWS KMS", "AWS Secrets Manager"],
     1,
     "AWS Certificate Manager (ACM) issues and auto-renews free public SSL/TLS certificates for integration with services like CloudFront, ELB, and API Gateway."),

    ("Security, Identity, and Compliance",
     "A company wants to provide sign-up, sign-in, and identity management for their web and mobile app's end users. Which service fits?",
     ["AWS IAM", "Amazon Cognito", "AWS IAM Identity Center", "AWS Directory Service"],
     1,
     "Amazon Cognito is specifically designed for end-user (customer-facing) authentication and authorization in web/mobile apps, distinct from IAM which manages AWS account access for administrators/services."),

    ("Security, Identity, and Compliance",
     "Which service centrally provides Single Sign-On (SSO) access across multiple AWS accounts and business applications, and was formerly known as AWS SSO?",
     ["AWS IAM Identity Center", "Amazon Cognito", "AWS Directory Service", "AWS RAM"],
     0,
     "AWS IAM Identity Center (formerly AWS SSO) provides centralized SSO access across multiple AWS accounts and integrated business applications for workforce identities."),

    ("Security, Identity, and Compliance",
     "Select TWO services that specifically deal with protecting web applications against network and application-layer attacks like DDoS, SQL injection, and cross-site scripting.",
     ["AWS Shield", "AWS WAF", "AWS KMS", "AWS Secrets Manager"],
     [0, 1],
     "AWS Shield protects against DDoS attacks, and AWS WAF filters malicious web traffic like SQL injection and XSS — KMS and Secrets Manager instead deal with encryption keys and secret storage, not traffic filtering."),

    # ============================================================
    # SERVICE CATEGORY 18 — Serverless
    # ============================================================
    ("Serverless",
     "Which service provides serverless compute specifically for running containers without managing any underlying EC2 instances or clusters?",
     ["AWS Fargate", "AWS Lambda", "Amazon EC2", "Amazon Lightsail"],
     0,
     "AWS Fargate is the serverless compute engine for containers (used with ECS or EKS), removing the need to provision or manage EC2 instances or clusters."),

    ("Serverless",
     "EXAM TRAP: What is the maximum execution timeout for a single AWS Lambda function invocation?",
     ["5 minutes", "10 minutes", "15 minutes (900 seconds)", "Unlimited, as long as billing is enabled"],
     2,
     "Lambda's maximum execution timeout is 15 minutes (900 seconds) — this specific number is a frequently tested fact, and workloads needing longer runtime must use a different compute service like Fargate or EC2."),

    ("Serverless",
     "A company wants to run code that automatically scales its concurrency to match incoming request volume, without provisioning capacity ahead of time, paying only per invocation and duration. Which service fits?",
     ["AWS Lambda", "AWS Fargate", "Amazon EC2 Auto Scaling", "AWS Elastic Beanstalk"],
     0,
     "AWS Lambda automatically scales concurrent executions to match request volume with true pay-per-invocation/duration pricing — the purest serverless compute option on AWS."),

    # ============================================================
    # SERVICE CATEGORY 19 — Storage
    # ============================================================
    ("Storage",
     "A company needs persistent block storage that attaches to a single EC2 instance, similar to a virtual hard drive. Which service fits?",
     ["Amazon EFS", "Amazon EBS", "Amazon S3", "Amazon FSx"],
     1,
     "Amazon EBS provides persistent block storage volumes that attach to a single EC2 instance, unlike EFS which is shared file storage accessible by multiple instances simultaneously."),

    ("Storage",
     "A company needs shared file storage that can be mounted concurrently by hundreds of EC2 instances using the NFS protocol. Which service fits?",
     ["Amazon EBS", "Amazon EFS", "Amazon S3 Glacier", "AWS Storage Gateway"],
     1,
     "Amazon EFS is a managed, scalable NFS file system that can be mounted by many EC2 instances simultaneously, unlike EBS which attaches to only one instance at a time."),

    ("Storage",
     "Which storage service offers virtually unlimited object storage with 11 nines of durability, ideal for storing any amount of unstructured data?",
     ["Amazon EBS", "Amazon S3", "Amazon EFS", "Amazon FSx"],
     1,
     "Amazon S3 is AWS's object storage service, offering essentially unlimited scale with eleven nines (99.999999999%) of durability for unstructured data."),

    ("Storage",
     "A company wants extremely low-cost storage for archival data they rarely need to access, and can tolerate retrieval times ranging from minutes to hours. Which service fits?",
     ["Amazon S3 Standard", "Amazon S3 Glacier", "Amazon EBS", "Amazon EFS"],
     1,
     "Amazon S3 Glacier is purpose-built for low-cost archival storage of infrequently accessed data, trading retrieval speed for a much lower storage cost than S3 Standard."),

    ("Storage",
     "A company wants to connect their on-premises applications to cloud storage as if it were local, caching frequently accessed data locally for low-latency access. Which hybrid storage service fits?",
     ["AWS Storage Gateway", "AWS Transfer Family", "Amazon FSx", "AWS Snowball"],
     0,
     "AWS Storage Gateway is a hybrid storage service that connects on-premises applications to AWS cloud storage, often caching frequently accessed data locally for performance."),

    # ============================================================
    # SERVERLESS QUICK TABLE CROSS-CHECK (multi-select)
    # ============================================================
    ("Serverless Quick Table",
     "Select TWO of the following that AWS classifies as serverless services requiring NO capacity provisioning by the customer.",
     ["Amazon Athena", "Amazon EC2", "AWS Step Functions", "Amazon RDS (standard, non-Aurora-Serverless)"],
     [0, 2],
     "Amazon Athena and AWS Step Functions both require zero infrastructure provisioning by the customer — standard EC2 and standard RDS instances, by contrast, require you to select and provision instance capacity."),

    ("Serverless Quick Table",
     "Which mode of Amazon Aurora auto-starts, auto-stops, and scales database capacity to zero when idle, making it serverless?",
     ["Aurora Multi-AZ", "Aurora Global Database", "Aurora Serverless", "Aurora Read Replicas"],
     2,
     "Aurora Serverless is the specific mode that automatically starts, stops, and scales capacity (even down to zero) based on demand, unlike standard Aurora which requires provisioned instances."),

    # ============================================================
    # AUTO-SCALING QUICK TABLE CROSS-CHECK
    # ============================================================
    ("Auto-Scaling Quick Table",
     "Which service acts as the central AWS service capable of scaling EC2, ECS, DynamoDB, Aurora, and Spot Fleets together toward unified target metrics?",
     ["Amazon EC2 Auto Scaling Groups", "AWS Auto Scaling", "AWS Compute Optimizer", "AWS Systems Manager"],
     1,
     "AWS Auto Scaling is the umbrella service that can manage scaling policies across multiple resource types (EC2, ECS, DynamoDB, Aurora, Spot Fleets) together, whereas EC2 Auto Scaling Groups only handle EC2 instances specifically."),

    ("Auto-Scaling Quick Table",
     "EXAM TRAP: For Amazon RDS, which aspect scales automatically, and which requires manual intervention or Application Auto Scaling?",
     ["Storage scales automatically; compute/read replica count requires manual or Application Auto Scaling configuration", "Compute scales automatically; storage must be manually resized", "Both compute and storage scale automatically with zero configuration", "Neither storage nor compute can scale on RDS"],
     0,
     "RDS Storage Autoscaling grows storage automatically as data grows, but scaling compute size or the number of read replicas requires manual changes or explicit Application Auto Scaling configuration — a frequently confused distinction."),

    # ============================================================
    # EXAM-MORNING REMINDERS — Explicit Trap Reinforcement
    # ============================================================
    ("Exam-Morning Reminders",
     "Which statement about Multi-AZ RDS deployments is TRUE?",
     ["The standby replica in another AZ is readable by default and used for scaling reads", "Multi-AZ uses synchronous replication to a standby in another AZ for high availability, and the standby is not readable by default", "Multi-AZ requires the application to manually redirect traffic on failure", "Multi-AZ only works within a single Availability Zone"],
     1,
     "Multi-AZ exists purely for high availability using synchronous replication to a standby that automatically takes over on failure — that standby is not intended for read traffic, which is what Read Replicas are for instead."),

    ("Exam-Morning Reminders",
     "Which statement correctly distinguishes DynamoDB Global Tables from a simple backup/DR solution?",
     ["Global Tables are only for backup, not live traffic", "Global Tables provide multi-region, multi-active replication for global low-latency access AND disaster recovery, not just backup", "Global Tables only replicate to a single secondary region", "Global Tables require manual conflict resolution for every write"],
     1,
     "DynamoDB Global Tables actively serve live read/write traffic across multiple regions simultaneously with automatic conflict resolution — this is fundamentally different from a passive backup that just sits idle until a disaster occurs."),

    ("Exam-Morning Reminders",
     "A candidate remembers 'OpsWorks' from their studies but is unsure what it does. Which description is correct?",
     ["AWS OpsWorks is a container orchestration service similar to ECS", "AWS OpsWorks is a managed configuration management service supporting Chef and Puppet for automating server configuration", "AWS OpsWorks is a serverless ETL service", "AWS OpsWorks is a monitoring and alerting dashboard"],
     1,
     "AWS OpsWorks provides managed Chef and Puppet configuration management to automate server configuration — it is unrelated to container orchestration despite sometimes being confused with ECS due to the 'Ops' naming."),

    ("Exam-Morning Reminders",
     "Which statement is the SAFEST general assumption for the exam when comparing AWS costs to on-premises TCO?",
     ["On-premises is always cheaper long-term regardless of scale", "AWS is typically framed as lower TCO due to no CapEx, no over-provisioning for peak, and pay-only-for-usage pricing", "TCO calculations are irrelevant to the exam", "AWS pricing models are identical to on-premises licensing"],
     1,
     "The exam consistently frames AWS as reducing TCO versus on-premises by removing large capital expenditure, eliminating the need to over-provision for peak demand, and charging only for actual usage."),
]


# --------------------------------------------------------------------
# QUIZ ENGINE — reusable as-is across modules (do not change per module)
# --------------------------------------------------------------------

def _normalize_correct(correct):
    """Return correct answer(s) as a set of 0-based indices."""
    if isinstance(correct, (list, tuple, set)):
        return set(correct)
    return {correct}


def _get_letter(idx):
    return chr(65 + idx)


def _shuffle_question(q):
    """Shuffle a question's options while keeping correct_answer indices valid."""
    topic, question_text, options, correct, explanation = q
    correct_set = _normalize_correct(correct)

    indexed = list(enumerate(options))
    random.shuffle(indexed)

    new_options = [opt for _, opt in indexed]
    old_to_new = {old_idx: new_idx for new_idx, (old_idx, _opt) in enumerate(indexed)}
    new_correct_indices = sorted(old_to_new[i] for i in correct_set)

    new_correct = new_correct_indices if len(new_correct_indices) > 1 else new_correct_indices[0]
    return (topic, question_text, new_options, new_correct, explanation)


def _ask_question(qnum, q):
    """Display a question, collect the user's answer, and record it (no feedback shown)."""
    topic, question_text, options, correct, explanation = q
    correct_set = _normalize_correct(correct)
    is_multi = len(correct_set) > 1

    print(f"\nQ{qnum}. {question_text}\n")
    for i, opt in enumerate(options):
        print(f"   {_get_letter(i)}. {opt}")

    if is_multi:
        prompt = f"\nSelect {len(correct_set)} answers, comma-separated (e.g. A,C): "
    else:
        prompt = "\nYour answer: "

    while True:
        raw = input(prompt).strip().upper().replace(" ", "")
        if not raw:
            print("Please enter an answer.")
            continue
        parts = [p for p in raw.split(",") if p]
        try:
            selected = set(ord(p) - 65 for p in parts)
        except Exception:
            print("Invalid input — use letters like A or A,C")
            continue
        if any(s < 0 or s >= len(options) for s in selected):
            print("Invalid option letter — try again.")
            continue
        if is_multi and len(selected) != len(correct_set):
            print(f"Please select exactly {len(correct_set)} options for this question.")
            continue
        if not is_multi and len(selected) != 1:
            print("Please select exactly 1 option for this question.")
            continue
        break

    print("Answer recorded.")
    return selected, correct_set


def run_quiz():
    print("=" * 72)
    print(f"AWS CCP (CLF-C02) — {MODULE_NAME} Practice Quiz")
    print("EXAM MODE: No feedback is shown per question — just like the real exam.")
    print("Full results, topic breakdown, and missed-question review appear at the end.")
    print("=" * 72)

    shuffled_questions = [_shuffle_question(q) for q in QUESTIONS]
    random.shuffle(shuffled_questions)

    results = []
    total = len(shuffled_questions)
    for i, q in enumerate(shuffled_questions, 1):
        topic, question_text, options, correct, explanation = q
        print(f"\n[{i}/{total}]", end="")
        selected, correct_set = _ask_question(i, q)
        is_correct = selected == correct_set
        results.append({
            "topic": topic,
            "question": question_text,
            "options": options,
            "selected": selected,
            "correct_set": correct_set,
            "is_correct": is_correct,
            "explanation": explanation,
        })

    print_results(results)


def print_results(results):
    total = len(results)
    correct_count = sum(1 for r in results if r["is_correct"])
    pct = (correct_count / total * 100) if total else 0.0

    topic_stats = defaultdict(lambda: [0, 0])  # topic -> [correct, total]
    for r in results:
        topic_stats[r["topic"]][1] += 1
        if r["is_correct"]:
            topic_stats[r["topic"]][0] += 1

    lines = []
    lines.append("=" * 72)
    lines.append(f"AWS CCP (CLF-C02) — {MODULE_NAME} — FINAL RESULTS")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 72)
    lines.append(f"\nOVERALL SCORE: {correct_count}/{total}  ({pct:.1f}%)\n")

    lines.append("-" * 72)
    lines.append("TOPIC-WISE BREAKDOWN (weakest first)")
    lines.append("-" * 72)
    topic_rows = []
    for topic, (c, t) in topic_stats.items():
        p = (c / t * 100) if t else 0.0
        topic_rows.append((p, topic, c, t))
    topic_rows.sort(key=lambda x: x[0])
    for p, topic, c, t in topic_rows:
        lines.append(f"  {topic:<40} {c}/{t:<4} ({p:.1f}%)")

    weak_topics = [topic for p, topic, c, t in topic_rows if p < 70]
    lines.append("\n" + "-" * 72)
    lines.append("WEAK TOPICS FLAGGED (<70% correct)")
    lines.append("-" * 72)
    if weak_topics:
        for t in weak_topics:
            lines.append(f"  \u26a0 {t}")
    else:
        lines.append("  None — solid performance across every topic!")

    missed = [r for r in results if not r["is_correct"]]
    lines.append("\n" + "-" * 72)
    lines.append(f"MISSED QUESTIONS REVIEW ({len(missed)} missed out of {total})")
    lines.append("-" * 72)
    if missed:
        for idx, r in enumerate(missed, 1):
            chosen_str = ", ".join(
                f"{_get_letter(i)}. {r['options'][i]}" for i in sorted(r["selected"])
            )
            correct_str = ", ".join(
                f"{_get_letter(i)}. {r['options'][i]}" for i in sorted(r["correct_set"])
            )
            lines.append(f"\n{idx}. {r['question']}")
            lines.append(f"   Your answer:    {chosen_str}")
            lines.append(f"   Correct answer: {correct_str}")
            lines.append(f"   Why: {r['explanation']}")
    else:
        lines.append("\n  No missed questions — perfect run!")

    report = "\n".join(lines)
    print("\n" + report)

    filename = f"{MODULE_NAME}-Results.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport exported to: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\nCould not export report: {e}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted by user. Exiting without saving results.")
        sys.exit(0)
