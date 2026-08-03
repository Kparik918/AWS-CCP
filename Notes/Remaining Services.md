# AWS CCP (CLF-C02) — Remaining Services Bible

> Ye sab wo services hain jo checklist me unchecked thi. Har service ka: **kya hai + kya karta hai + exam angle + common confusion (agar hai)**.

---

## 💰 Cloud Financial Management

### AWS Billing Conductor

- **Kya hai:** Custom billing/cost allocation tool — mainly resellers aur large orgs ke liye jo apne sub-accounts/customers ko **custom pricing plans** dena chahte hain.
- **Real use case:** Socho tum AWS Partner ho aur apne clients ko markup ke saath resell karte ho — Billing Conductor se tum unke liye custom "pro forma" bills bana sakte ho, actual AWS cost se alag.
- **Exam angle:** "Custom billing groups create karna hai apne customers ke liye" → Billing Conductor. Cost Explorer/Budgets se confuse mat karna — wo tumhare khud ke cost analysis/alerts ke liye hain, Billing Conductor **resale/chargeback** ke liye hai.

---

## 🤝 Customer Engagement

### AWS Activate for Startups

- **Kya hai:** Startups ke liye program — AWS credits, technical support, training resources deta hai.
- **Exam angle:** "Startup founder AWS credits chahta hai" → Activate. Simple recall question.

### AWS IQ

- **Kya hai:** Marketplace jahan tum AWS-certified independent experts/consultants hire kar sakte ho short-term project work ke liye (billing bhi AWS invoice ke through hoti hai).
- **Exam angle:** "Need a certified AWS expert for a one-off project" → AWS IQ.

### AWS Managed Services (AMS)

- **Kya hai:** AWS khud tumhare AWS infrastructure ko **operate/manage** karta hai (ongoing infrastructure management) — jaise ek managed service provider hire karna, but AWS khud.
- **Exam angle:** "Company ke paas in-house ops team nahi hai, AWS ko infra manage karwana hai" → AMS.

### AWS Support

- **Kya hai:** Support plans — **Basic (free), Developer, Business, Enterprise On-Ramp, Enterprise**.
- **Exam angle — YE HIGH YIELD HAI:**

|Plan|Key Feature|
|---|---|
|Basic|Free, sirf billing/account support, forums|
|Developer|Email support, business hours, 1 contact|
|Business|24/7 phone/chat/email, <1hr response for urgent, Trusted Advisor full checks, API access|
|Enterprise On-Ramp|Concierge support (limited), TAM pool|
|Enterprise|**Dedicated TAM (Technical Account Manager)**, <15 min response for critical, Concierge support team|

- Trap: "Dedicated TAM" = **Enterprise only**. "24/7 support" starts from Business plan onwards.

---

## 🗄️ Database

### Amazon MemoryDB for Redis

- **Kya hai:** Redis-compatible, **durable, in-memory** database — ElastiCache se alag kyuki ye **primary database** ke roop me use ho sakta hai (data durability guaranteed via multi-AZ transaction log), sirf caching layer nahi.
- **Exam angle:** ElastiCache vs MemoryDB confusion:
    - **ElastiCache** = caching layer, data loss acceptable (in-memory only, no durability by default)
    - **MemoryDB** = durable, can be your primary DB, ultra-low latency + persistence dono

---

## 🛠️ Developer Tools

_(Ye sab "AWS Developer Tools suite" ke parts hain — CI/CD pipeline ka pura lifecycle cover karte hain)_

### AWS AppConfig

- **Kya hai:** Application configuration aur feature flags ko **deploy/manage** karta hai bina code redeploy kiye, controlled rollout ke saath (gradual rollout + auto rollback on error).
- **Exam angle:** "Feature flags safely rollout karna hai" → AppConfig.

### AWS CLI (Command Line Interface)

- **Kya hai:** Terminal se AWS services ko control karne ka tool — commands likh ke resources manage karna.
- **Exam angle:** Bas basic recall — "command line se AWS manage karna" → CLI. Tumhe already pata hoga practically.

### AWS Cloud9

- **Kya hai:** Cloud-based **IDE** (code editor) — browser me hi code likho, run karo, debug karo. Preconfigured with AWS CLI.
- **Exam angle:** "Browser-based IDE for coding" → Cloud9.

### AWS CloudShell

- **Kya hai:** Browser-based **shell/terminal** directly console se accessible — pre-authenticated, AWS CLI pre-installed. Cloud9 se alag: Cloud9 IDE hai (full dev environment), CloudShell sirf ek quick terminal hai.
- **Exam angle:** "Quick shell access console se, bina setup ke" → CloudShell.

### AWS CodeArtifact

- **Kya hai:** Managed **artifact repository** — software packages/dependencies (npm, pip, Maven packages) securely store aur share karne ke liye.
- **Exam angle:** "Package/dependency management for our build pipeline" → CodeArtifact.

### AWS CodeCommit

- **Kya hai:** Managed **Git-based source control** (like private GitHub, hosted by AWS). ⚠️ Note: AWS naye customers ke liye ye service deprecate kar chuka hai (2024 se), lekin CCP exam me abhi bhi aa sakta hai conceptually.
- **Exam angle:** "Store source code securely, Git-based" → CodeCommit.

### AWS CodeDeploy

- **Kya hai:** **Automates code deployments** — EC2, Lambda, ECS, on-premises servers pe. Blue/green aur rolling deployments support karta hai.
- **Exam angle:** Pura CI/CD pipeline yaad rakho:

|Stage|Service|
|---|---|
|Source (code store)|CodeCommit|
|Build (compile/test)|CodeBuild ✅ (already known)|
|Deploy (rollout)|CodeDeploy|
|Orchestrate (pura pipeline automate)|CodePipeline ✅ (already known)|

### AWS CodeStar

- **Kya hai:** Unified dashboard jo CodeCommit + CodeBuild + CodeDeploy + CodePipeline sabko ek jagah manage karta hai — quick project setup templates ke saath. (Ye bhi legacy ho chuka hai but exam me concept aa sakta hai.)
- **Exam angle:** "Ek single dashboard se pura dev pipeline manage karna" → CodeStar.

---

## 📱 Frontend Web and Mobile

### AWS Device Farm

- **Kya hai:** Real physical mobile/tablet devices (aur browsers) pe apni app ko **test** karne ka service — cloud me hosted real device farm.
- **Exam angle:** "App ko real Android/iOS devices pe test karna hai without buying devices" → Device Farm.

---

## 📡 Internet of Things (IoT)

### AWS IoT Greengrass

- **Kya hai:** IoT Core ka **edge computing extension** — IoT devices pe local compute/ML inference chalane deta hai bina hamesha cloud se connect hue (offline bhi kaam karta hai, phir sync karta hai jab connection aaye).
- **Exam angle:** IoT Core vs Greengrass:
    - **IoT Core** = cloud me devices connect/manage karna
    - **Greengrass** = **edge/local** processing, device khud "thoda smart" ban jata hai, cloud se disconnect hone pe bhi function karta rahe

---

## ⚙️ Management and Governance

### AWS Launch Wizard

- **Kya hai:** Guided wizard jo complex third-party applications (SAP, SQL Server, Active Directory) ko AWS pe deploy karne me help karta hai — sizing, config, aur deployment automate karta hai best-practices ke hisaab se.
- **Exam angle:** "SAP workload ko AWS pe deploy karna hai, best practice sizing ke saath" → Launch Wizard.

### AWS Resource Groups and Tag Editor

- **Kya hai:** Apne AWS resources ko **tags ke basis pe organize/group** karna aur ek jagah se manage karna. Tag Editor se bulk tagging kar sakte ho.
- **Exam angle:** "Multiple resources ko tag ke basis pe find/manage karna hai across services" → Resource Groups & Tag Editor.

---

## 🔐 Security, Identity, and Compliance

### AWS CloudHSM

- **Kya hai:** **Dedicated, single-tenant hardware** security module — cryptographic keys store karne ke liye, jab tumhe **full control** chahiye hardware pe (FIPS 140-2 Level 3 compliance ke liye).
- **Exam angle — KMS vs CloudHSM (bohot common trap):**

| |AWS KMS|AWS CloudHSM|
|---|---|---|
|Tenancy|Multi-tenant (shared)|**Single-tenant (dedicated hardware)**|
|Control|AWS manages keys|**Tumhara full control** over HSM|
|Use case|General encryption needs|Strict compliance (govt, finance) needing dedicated HW|
|Ease|Easy, managed|Zyada complex, tumhe manage karna padta hai|

### Amazon Cognito

- **Kya hai:** **User authentication/authorization** service for web & mobile apps — tumhare **app ke end-users** ke liye sign-up/sign-in (social login — Google/Facebook — bhi support karta hai). IAM se bilkul alag!
- **Exam angle — IAM vs Cognito (VERY high yield trap):**
    - **IAM** = AWS resources access control ke liye (internal — employees, services)
    - **Cognito** = tumhari **app ke customers/end-users** ke login/signup ke liye (external, app users)
    - Trick line: "Mobile app users ko sign-in feature dena hai" → Cognito, NOT IAM.

### AWS Directory Service

- **Kya hai:** Managed **Microsoft Active Directory** in AWS — ya toh AWS Managed Microsoft AD, ya AD Connector (on-premises AD ko AWS se connect karna), ya Simple AD.
- **Exam angle:** "Company already on-prem AD use karti hai, AWS resources ke saath integrate karna hai" → Directory Service (AD Connector variant).

### AWS Firewall Manager

- **Kya hai:** **Centralized security policy management** across multiple AWS accounts/resources — WAF rules, Shield protections, Security Groups ek jagah se enforce karta hai **Organizations level pe**.
- **Exam angle:** WAF vs Firewall Manager:
    - **WAF** = ek resource pe rules apply karna (single app-level firewall)
    - **Firewall Manager** = **saari organization** me centrally WAF/Shield rules enforce karna, multi-account setup me

### AWS RAM (Resource Access Manager)

- **Kya hai:** AWS resources (jaise subnets, Transit Gateway) ko **securely share** karna across multiple AWS accounts — bina resource duplicate kiye.
- **Exam angle:** "VPC subnet ko doosre AWS account ke saath share karna hai bina copy kiye" → RAM.

---

## 🎯 Quick Revision Table — Sabse Zyada Exam-Trap Wale Pairs

|Confusion Pair|Difference in 1 line|
|---|---|
|KMS vs CloudHSM|KMS = shared/managed, CloudHSM = dedicated/full-control hardware|
|IAM vs Cognito|IAM = internal AWS access, Cognito = app ke external end-users|
|WAF vs Firewall Manager|WAF = single resource rule, Firewall Manager = org-wide central policy|
|IoT Core vs Greengrass|Core = cloud connectivity, Greengrass = edge/offline compute|
|Cloud9 vs CloudShell|Cloud9 = full IDE, CloudShell = quick browser terminal|
|ElastiCache vs MemoryDB|ElastiCache = cache (non-durable), MemoryDB = durable primary DB|
|CodeCommit vs CodeArtifact|CodeCommit = source code (Git), CodeArtifact = packages/dependencies|

---

## Progress Update

- Ye note cover karta hai: **~28 previously unchecked services**
- Baaki checklist ke saath combine karke ab tumhara CCP scope **~95/95 services** complete ho jayega revision ke liye.