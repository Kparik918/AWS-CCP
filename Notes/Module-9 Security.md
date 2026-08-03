# 📘 MODULE 9 — SECURITY (AWS CCP CLF-C02) — BIBLE NOTES

> **Domain Weight Alert:** Security is Domain 3 in CLF-C02 and carries **~30% of the entire exam** — the single heaviest domain. This module deserves your maximum revision time.

---

## 🗺️ MODULE MAP

```
Security
│
├── 1. Shared Responsibility Model
├── 2. Authentication vs Authorization
├── 3. Access Control (Root User, IAM)
│      ├── IAM Users
│      ├── IAM Groups
│      ├── IAM Policies
│      ├── IAM Roles
│      └── IAM Identity Center (SSO)
├── 4. Secrets & Node Management
│      ├── AWS Secrets Manager
│      └── AWS Systems Manager
├── 5. Network Attacks & Defense
│      ├── DoS / DDoS
│      ├── Security Groups
│      ├── ELB
│      ├── AWS Regions (scale defense)
│      ├── AWS Shield (Standard/Advanced)
│      └── AWS WAF
├── 6. Data Protection
│      ├── Encryption at Rest / in Transit
│      ├── AWS KMS
│      ├── Amazon Macie
│      └── AWS Certificate Manager
└── 7. Detect & Respond
       ├── Amazon Inspector
       ├── Amazon GuardDuty
       ├── Amazon Detective
       └── AWS Security Hub
```

---

## 1️⃣ SHARED RESPONSIBILITY MODEL ★★★★★

### Definition

A framework that splits security duties between **AWS** and the **customer**. Neither party is 100% responsible — security is a _shared_ job.

### Hinglish Analogy 🏢

Socho tum ek **rented flat** mein rehte ho.

- **Building ki safety** (foundation, walls, main gate, fire exits) — ye **builder/society (AWS)** ki zimmedari hai.
- **Apne flat ke andar ka saaman, apna door lock karna, apni cheezein sambhalna** — ye **tumhari (customer)** zimmedari hai.

### The Split

|Responsibility Zone|Owner|What's Included|
|---|---|---|
|**Security OF the cloud**|**AWS**|Hardware, AWS Global Infrastructure, physical data centers, host OS, virtualization layer|
|**Security IN the cloud**|**Customer**|Customer data, client-side encryption, IAM permissions, guest OS patching (on EC2), network/firewall config|
|**Varies by service**|**Shared**|Server-side encryption, network traffic protection, platform/app management, OS/network/firewall config|

```
┌─────────────────────────────────────────────┐
│  CUSTOMER RESPONSIBILITY (Security IN cloud) │
│  • Customer data                             │
│  • Client-side data encryption               │
├─────────────────────────────────────────────┤
│  SHARED (Varies by service)                  │
│  • Server-side encryption                    │
│  • Network traffic protection                │
│  • Platform & application management         │
│  • OS, network, firewall configuration       │
├─────────────────────────────────────────────┤
│  AWS RESPONSIBILITY (Security OF cloud)      │
│  • Software for compute/storage/DB/network   │
│  • Hardware & AWS Global Infrastructure      │
└─────────────────────────────────────────────┘
```

### Key Nuance — "Varies by Service"

- **Managed services** (S3, DynamoDB, RDS-managed patching) → AWS takes on MORE responsibility.
- **Unmanaged/IaaS services** (EC2) → Customer takes on MORE responsibility (guest OS patches, firewall rules, app security).

### 🎯 What AWS is REALLY Testing

AWS isn't testing whether you can recite "AWS secures the cloud, customer secures data in the cloud." AWS is testing whether you can **classify a specific scenario** into the right bucket — e.g., "Who patches the guest OS on an EC2 instance?" → **Customer**, not AWS.

### ⚠️ Common Exam Traps

- A **data breach caused by a misconfigured S3 bucket policy** = **Customer's fault**, not AWS's (AWS gave you the tool; you set the permission).
- AWS is **always** responsible for physical security of data centers — no exceptions, no service dependency.
- For EC2: AWS = hypervisor & hardware; Customer = guest OS, patching, security groups, IAM.
- For RDS: AWS = underlying OS/DB engine patching; Customer = data, access management, encryption choices.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Security split between AWS (of the cloud) and customer (in the cloud)|
|Use Case|Deciding who is liable for a security gap|
|Alternative|N/A (foundational model, not a service)|
|Pricing|Free — it's a framework|
|Common Trap|Confusing "of" vs "in" the cloud|
|Exam Importance|★★★★★|

---

## 2️⃣ AUTHENTICATION vs AUTHORIZATION ★★★★★

| |Authentication|Authorization|
|---|---|---|
|**Question answered**|"Who are you?"|"What are you allowed to do?"|
|**Happens**|First (login step)|After login|
|**AWS tools**|IAM Users, root user, MFA, IAM Identity Center|IAM Policies, resource-based policies|
|**Hinglish**|Society ke gate pe ID card dikhana|Andar jaake sirf apne floor ka lift button dabana|

### Why AWS Provides This

To ensure **only verified identities** get in (authentication), and even verified identities only get **exactly the access they need** (authorization) — supporting **least privilege**.

### 🎯 What AWS is REALLY Testing

AWS is testing whether you know that a user can be **authenticated but still not authorized** — i.e., logging in successfully doesn't mean you can do everything.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Auth = identity verification; Authz = permission granting|
|Use Case|Every AWS Console/API interaction|
|Common Trap|Thinking login = full access|
|Exam Importance|★★★★★|

---

## 3️⃣ ACCESS CONTROL — ROOT USER & IAM ★★★★★

### 3.1 Root User

**Definition:** The account created when you first sign up for AWS — has **unrestricted access** to all resources and billing.

**Hinglish Analogy 🏠:** Root user = **ghar ka malik** jiske paas har room ki master key hai — Linux ke `root` user jaisa, "sab kuch kar sakta hai."

**Best Practices:**

- Set a **strong password + MFA** immediately.
- **Never use root for daily tasks** — only for emergency/account-level actions (e.g., changing support plan, closing account).
- Create an IAM user/admin role for everyday work instead.

⚠️ **Exam Trap:** AWS exam LOVES asking "what is the first thing you should do after creating an AWS account?" → **Enable MFA on root + create an IAM admin user**, not "start launching EC2 instances."

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Superuser account with full, unrestricted access|
|Use Case|Emergency/account-level tasks only|
|Alternative|IAM admin user/role for daily work|
|Common Trap|Using root for everyday operations|
|Exam Importance|★★★★☆|

---

### 3.2 IAM (Identity and Access Management) ★★★★★

**Definition:** A **global, free** AWS service to securely manage identities (who) and permissions (what) for AWS resources.

**Why AWS Provides It:** Without IAM, everyone would need root credentials — a massive security risk. IAM enables **granular, least-privilege access**.

**Core Principle — Least Privilege:**

> "Jisko jitni zarurat hai, utni hi permission do." By default, a new IAM user has **ZERO permissions** — everything is **implicitly denied** until explicitly allowed.

```
New IAM User Created
        │
        ▼
  Default = DENY everything
        │
        ▼
  Admin explicitly ALLOWs via Policy
        │
        ▼
  User can now perform only allowed actions
```

#### IAM Users

- Represents a **single individual identity** logging into AWS.
- Has long-term credentials (password for console, access keys for CLI/API).

#### IAM Policies

- **JSON documents** that define what's Allowed/Denied.
- Basic structure:

```json
{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "s3:ListBucket",
    "Resource": "arn:aws:s3:::coffee_shop_reports"
  }
}
```

|Element|Meaning|
|---|---|
|`Version`|Policy language version (almost always `2012-10-17`)|
|`Effect`|`Allow` or `Deny`|
|`Action`|Which API call on which service (e.g., `s3:ListBucket`)|
|`Resource`|The specific ARN (Amazon Resource Name) the action applies to|

⚠️ **Exam Trap:** An explicit **Deny always overrides an Allow** — even if another policy allows the same action, Deny wins.

#### IAM Groups

- A collection of IAM users, managed together.
- Attach a policy to the **group** → it automatically applies to **all members**.
- Best practice: assign permissions via groups, not individual users, for easier management at scale.

**Hinglish Analogy 🏢:** Group = **department** in an office (HR, Finance, Engineering). Ek policy company-wide announce karo per department, sab log automatically cover ho jaate hain.

#### IAM Roles

- **Temporary** credentials with associated permissions — **no static username/password**.
- Assumed by a **trusted entity** (an AWS service, an application, or a federated user) for a limited session.
- Avoids the need to create IAM users when temporary or service-to-service access is needed.

**Real Example of an IAM Role:** An EC2 instance running an application that needs to read/write to an S3 bucket. Instead of hardcoding AWS access keys inside the app (a huge security risk if leaked), you attach an **IAM Role** to the EC2 instance. The instance automatically receives **temporary, auto-rotating credentials** via the instance metadata service — no static keys stored anywhere.

**Federation Example:** A company has 5,000 employees already using **Microsoft Active Directory (corporate credentials)** for login. Instead of creating 5,000 separate IAM users, the company sets up **federation** — corporate AD credentials are mapped to an IAM Role. When an employee logs in with their existing corporate ID, AWS grants them temporary access matching that role's permissions, without AWS ever storing their corporate password.

| |IAM User|IAM Role|
|---|---|---|
|Credentials|Long-term (password/access keys)|Temporary (auto-expiring)|
|Best for|A specific human needing ongoing console/CLI access|Services, apps, federated/cross-account access|
|Risk if leaked|High (static, valid until rotated)|Low (expires automatically)|

#### IAM Identity Center (formerly AWS SSO)

- Used to set up **Single Sign-On (SSO)** across multiple AWS accounts and business applications.
- Employees log in **once** and get access to all authorized accounts/apps without separate logins for each.

**Hinglish Analogy 🎫:** Ek **college ID card** jisse tum library, canteen, aur hostel — sabme entry le sakte ho, alag alag card ki zarurat nahi.

### 🎯 What AWS is REALLY Testing (IAM)

AWS isn't testing whether you can write a JSON policy from scratch. AWS is testing whether you know **when to use a User vs a Group vs a Role** — e.g., "An application on EC2 needs S3 access" → answer is always **Role**, never hardcoded user access keys.

### Comparison Table — IAM Users vs Groups vs Roles vs Identity Center

|Feature|IAM User|IAM Group|IAM Role|IAM Identity Center|
|---|---|---|---|---|
|Represents|Single identity|Collection of users|Temporary assumable identity|Centralized SSO access|
|Credentials|Long-term|N/A (inherits from users)|Temporary|Federated/SSO session|
|Typical use|Individual person|Managing many users at once|EC2/Lambda/cross-account access, federation|Multi-account workforce access|

### ⚠️ Common Exam Traps

- IAM is a **global service** — not region-specific.
- New IAM users have **no permissions by default** (implicit deny).
- **Explicit Deny beats Allow**, always.
- **Roles ≠ Users** — Roles have NO permanent credentials.
- MFA should be enabled on **root user immediately**, and ideally on privileged IAM users too.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Service to manage identities and permissions for AWS resources|
|Use Case|Controlling who can do what, across users/apps/services|
|Alternative|Root user (emergency only)|
|Pricing|Free|
|Common Trap|Default-deny; Deny overrides Allow|
|Exam Importance|★★★★★|

---

## 4️⃣ SECRETS & SYSTEMS MANAGEMENT

### 4.1 AWS Secrets Manager ★★★★☆

**Definition:** Securely stores, **rotates**, and retrieves secrets — database credentials, API keys, and other sensitive info — throughout their lifecycle.

**Why AWS Provides It:** Hardcoding passwords/API keys in code is a top cause of breaches. Secrets Manager centralizes and **automatically rotates** these secrets.

**Hinglish Analogy 🔐:** Ek **locker system** jisme sensitive cheezein (passwords) rakhi jaati hain, aur locker ki key khud-ba-khud time-to-time badalti rehti hai (auto-rotation) taaki purani key kaam na kare agar leak ho jaaye.

**When to Use:** Storing DB credentials, API keys that need automatic rotation. **When NOT to Use:** Simple config values that aren't secret (use Systems Manager Parameter Store instead — cheaper).

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Secure storage + auto-rotation for secrets|
|Use Case|DB credentials, API keys|
|Alternative|Systems Manager Parameter Store (non-sensitive config, cheaper)|
|Common Trap|Confusing with Parameter Store (Parameter Store doesn't auto-rotate secrets natively)|
|Exam Importance|★★★★☆|

---

### 4.2 AWS Systems Manager ★★★☆☆

**Definition:** Provides a **centralized view** of nodes (servers/instances) across accounts, Regions, and even multi-cloud/hybrid environments. Automates registry edits, user management, and security patching.

**Real-World Scenario:** A company with 500 EC2 instances across 3 regions needs to patch a critical vulnerability on all of them simultaneously — Systems Manager's **Patch Manager** does this centrally instead of manually logging into each instance.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Centralized node visibility, automation & patching|
|Use Case|Fleet-wide management, patching, automation|
|Common Trap|Confusing with Secrets Manager (different purpose)|
|Exam Importance|★★★☆☆|

---

## 5️⃣ NETWORK ATTACKS & DEFENSE

### 5.1 DoS vs DDoS ★★★★☆

| |DoS|DDoS|
|---|---|---|
|Full form|Denial of Service|Distributed Denial of Service|
|Source|**Single** attacker/machine|**Multiple** compromised machines ("zombie bots")|
|Scale|Smaller|Much larger, harder to block by IP|

```
DoS:            Attacker ──────────► Target (floods with traffic)

DDoS:            Attacker
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Zombie Bot   Zombie Bot   Zombie Bot
        │           │           │
        └───────────┼───────────┘
                     ▼
                  Target (overwhelmed from many sources)
```

**Real-Life Example:** Imagine a popular restaurant where hundreds of fake customers (recruited by a rival) walk in at once, order nothing, and just occupy every table — real customers can't get seated. That's the "denial of service" to genuine customers.

**AWS Infra Example:** An e-commerce site's login page on EC2 behind an ALB gets hit by thousands of infected IoT devices worldwide, all sending login requests per second — the app server's CPU/connections max out and real shoppers can't check out.

**UDP Flood Attack:** A specific DDoS technique where the attacker sends a massive number of **UDP packets** to random ports on the target. The target has to check for an application listening on each port, reply with "destination unreachable" ICMP packets, and this processing overhead exhausts resources — even though no actual application-level connection was ever made (UDP is connectionless, unlike TCP).

### Defense Layers

```
Layer 1: Security Groups     → Only allow legitimate traffic (stateful firewall)
Layer 2: Elastic Load Balancer → Absorbs traffic before it reaches your servers
Layer 3: AWS Regions          → Massive infra capacity makes attacks expensive to sustain
Layer 4: AWS Shield            → Purpose-built DDoS protection
Layer 5: AWS WAF               → Blocks malicious traffic at the application layer
```

#### Security Groups (defense role)

- Operate at the **instance level**, allow-only rules, **stateful**.
- Only let in "proper" request traffic — reduces attack surface right away.

#### Elastic Load Balancing (ELB) (defense role)

- ELB absorbs incoming traffic **first**, so your backend EC2 instances aren't directly overwhelmed.
- Operates at the Region level — massive built-in capacity to shrug off spikes.

#### AWS Regions (defense role)

- A Region's sheer infrastructure capacity makes it **extremely expensive** for an attacker to meaningfully disrupt service — you'd need an enormous, costly attack to even dent it.

**Hinglish:** Itna bada attack karna hoga ki balance bigadne ke liye bhi attacker ko bohot paisa aur resource lagega — cost hi deterrent ban jaata hai.

### 30-Second Revision (DoS/DDoS)

|Field|Value|
|---|---|
|Definition|Attacks that flood a system to deny service to legit users|
|Use Case|Understanding what Shield/WAF protect against|
|Common Trap|Confusing single-source (DoS) with multi-source (DDoS)|
|Exam Importance|★★★★☆|

---

### 5.2 AWS Shield ★★★★★

| |Shield Standard|Shield Advanced|
|---|---|---|
|**Cost**|**Free**, automatic for all AWS customers|**Paid** subscription|
|**Protects against**|Most common, frequently occurring DDoS attacks|Sophisticated, large-scale DDoS attacks|
|**Extras**|Real-time detection & mitigation|Detailed attack diagnostics, 24/7 DDoS Response Team (DRT), cost protection, integrates with CloudFront, Route 53, ELB|
|**Integration**|N/A|Can combine with AWS WAF for custom mitigation rules|

**Hinglish Analogy 🛡️:** Shield Standard = **building ka basic security guard**, free hota hai sabke liye. Shield Advanced = **VIP private security team** jo detailed report bhi deti hai aur emergency mein directly involve hoti hai.

### 🎯 What AWS is REALLY Testing

AWS isn't testing whether Shield exists. AWS is testing whether you know Shield **Standard is free & automatic**, while **Advanced is paid** and adds diagnostics + expert response — a very common exam distinction.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Managed DDoS protection service|
|Use Case|Protecting apps/network from DDoS|
|Alternative|WAF (application-layer, rule-based)|
|Pricing|Standard = free; Advanced = paid|
|Common Trap|Thinking both tiers are free|
|Exam Importance|★★★★★|

---

### 5.3 AWS WAF (Web Application Firewall) ★★★★★

**Definition:** A firewall that monitors and filters HTTP/HTTPS requests to your web applications based on rules in a **Web ACL (Access Control List)**.

**How It Works:**

```
Incoming Request → AWS WAF checks IP against Web ACL
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
      IP is blocked            IP is allowed
      → Access DENIED          → Access GRANTED
```

**Why AWS Provides It:** Protects against **application-layer** attacks (SQL injection, cross-site scripting) — different from Shield, which focuses on network/transport-layer DDoS.

### Comparison: Shield vs WAF

| |AWS Shield|AWS WAF|
|---|---|---|
|Protects against|DDoS (network/transport layer, L3/L4)|Application-layer attacks (L7) — SQLi, XSS, bad bots|
|Rule-based?|Automatic detection|**Customizable rules** you define|
|Pricing|Standard free / Advanced paid|Pay per Web ACL + per rule + per request|
|Can combine?|Yes — Shield + WAF together for complex DDoS mitigation|Yes|

### 🎯 What AWS is REALLY Testing

AWS is testing whether you know **WAF works at Layer 7 (application/HTTP)** while **Shield works at the network layer** — and that they complement each other rather than compete.

### ⚠️ Common Exam Traps

- WAF ≠ Shield. WAF = **application-layer**, custom rules based on IP/request patterns. Shield = **DDoS-specific**, network-layer.
- WAF works via **Web ACLs** — remember this term specifically, exam loves it.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Application-layer firewall filtering HTTP(S) requests via Web ACLs|
|Use Case|Blocking malicious IPs, SQLi/XSS protection|
|Alternative|Shield (network-layer DDoS)|
|Common Trap|Mixing up WAF (app layer) with Shield (network layer)|
|Exam Importance|★★★★★|

---

## 6️⃣ DATA PROTECTION ★★★★★

### 6.1 Encryption — At Rest vs In Transit

**Hinglish Analogy 🔒:** Encryption = **lock-and-key system**. Data ko encrypt (lock) karo, sirf sahi key waale hi usse decrypt (unlock) kar sakte hain.

|Type|Definition|Example|
|---|---|---|
|**At Rest**|Data is idle, stored somewhere (not moving)|Data sitting in an S3 bucket or database|
|**In Transit**|Data is actively moving between systems|Data traveling from a database to an application over the network (secured via SSL/TLS)|

```
[Data at Rest]  ──(encrypted, idle in storage)──►  🔒 kX24*j1htY:#
       │
       │  SSL/TLS (Encryption in Transit)
       ▼
[Data moving across network]  ──►  Destination server (decrypts on arrival)
```

### Default Encryption at Rest by Service

|Service|Default Encryption at Rest?|
|---|---|
|**Amazon S3**|✅ Yes — all new buckets and uploaded objects encrypted at rest by default|
|**Amazon EBS**|Volumes & snapshots **can be** encrypted (boot + data volumes)|
|**Amazon DynamoDB**|✅ Yes — server-side encryption enabled on all table data, using KMS keys|

⚠️ **Exam Trap:** S3 and DynamoDB encryption at rest is **default/automatic**; EBS encryption is **available but must be enabled** (not automatic on default volumes unless account-level default encryption is turned on).

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Protecting data while stored (at rest) or moving (in transit)|
|Use Case|Every service handling sensitive data|
|Alternative|N/A — core concept|
|Common Trap|Assuming all services auto-encrypt by default (S3/DynamoDB do, EBS varies)|
|Exam Importance|★★★★★|

---

### 6.2 AWS KMS (Key Management Service) ★★★★★

**Definition:** A managed service to **create, store, and manage cryptographic (encryption) keys** used to encrypt/decrypt data across AWS services.

**Hinglish Analogy 🗝️:** KMS = ek **password manager** jisme saari keys safely stored aur managed hoti hain — tumhe manually keys yaad rakhne ki zarurat nahi.

**Why AWS Provides It:** Centralizes key lifecycle management (creation, rotation, disabling, deletion) with strict access control via IAM — critical for compliance.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Managed cryptographic key creation/storage service|
|Use Case|Powering encryption for S3, EBS, DynamoDB, RDS, etc.|
|Common Trap|Confusing KMS (keys) with Secrets Manager (secrets/credentials)|
|Exam Importance|★★★★★|

---

### 6.3 Amazon Macie ★★★☆☆

**Definition:** Uses **machine learning + automation** to discover, monitor, and protect **sensitive data** (like PII) stored in Amazon S3.

**Real-World Scenario:** A healthcare company wants to ensure no patient records (PII) are sitting in a publicly accessible S3 bucket by mistake — Macie scans and flags this automatically.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|ML-based sensitive data discovery for S3|
|Use Case|Finding/protecting PII, compliance audits|
|Common Trap|Macie is S3-focused, not a general DLP for all services|
|Exam Importance|★★★☆☆|

---

### 6.4 AWS Certificate Manager (ACM) ★★★☆☆

**Definition:** Provisions, manages, and renews **SSL/TLS certificates** for use with AWS services — enabling **encryption in transit**.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Manages SSL/TLS certificates|
|Use Case|HTTPS on ALB, CloudFront, API Gateway|
|Common Trap|ACM handles certs; it does NOT do encryption at rest|
|Exam Importance|★★★☆☆|

---

## 7️⃣ DETECT & RESPOND SERVICES ★★★★★

_(This is where "Prevent & Protect" hands off to "Detect & Respond.")_

```
   PREVENT & PROTECT              DETECT & RESPOND
 (IAM, Security Groups,      (Inspector, GuardDuty,
  Shield, WAF, Encryption)    Detective, Security Hub)
```

|Service|Role|Analogy|
|---|---|---|
|**Amazon Inspector**|Runs **automated vulnerability assessments** against infrastructure (heavy focus on EC2) — checks for exposed instances, deviations from best practices, vulnerable software versions. Gives prioritized findings by severity, retrievable via API.|Health check-up ka doctor — scan karke bataata hai kya galat hai|
|**Amazon GuardDuty**|**Continuously monitors** network activity & data streams for threats using intelligent threat detection|CCTV camera jo 24/7 activity watch karta hai|
|**Amazon Detective**|Used **after** a threat/vulnerability is detected — analyzes and visualizes logs to investigate root cause|Detective jo crime scene ke baad investigation karta hai|
|**AWS Security Hub**|**Aggregates** findings from multiple security services into one comprehensive dashboard|Ek control room jaha saari security services ki reports ek jagah dikhti hain|

### Order of Operations

```
1. Inspector    → finds vulnerabilities (proactive scan)
2. GuardDuty    → detects active threats (continuous monitoring)
3. Detective    → investigates root cause (post-detection analysis)
4. Security Hub → aggregates everything into one dashboard
```

### 🎯 What AWS is REALLY Testing

AWS is testing whether you can **sequence** these four services correctly — i.e., know that GuardDuty _detects_, Detective _investigates after detection_, Inspector _scans for vulnerabilities proactively_, and Security Hub _aggregates_ — not just that they exist.

### ⚠️ Common Exam Traps

- **Inspector** = vulnerability assessment (proactive, EC2-focused).
- **GuardDuty** = continuous threat detection (reactive/ongoing monitoring).
- **Detective** = root-cause investigation AFTER GuardDuty flags something.
- **Security Hub** = the "dashboard of dashboards," not a detection engine itself.

### 30-Second Revision

|Field|Value|
|---|---|
|Definition|Suite of detect-and-respond security services|
|Use Case|Vulnerability scanning, threat detection, investigation, aggregation|
|Common Trap|Mixing up Inspector (vulnerabilities) vs GuardDuty (active threats)|
|Exam Importance|★★★★★|

---

# 🏁 MODULE END — QUICK REFERENCE

## 📊 Quick Summary Table

|Category|Services|
|---|---|
|Foundational Model|Shared Responsibility Model|
|Identity Management|IAM (Users, Groups, Roles, Policies), IAM Identity Center, Root User|
|Secrets/Node Mgmt|Secrets Manager, Systems Manager|
|Network Defense|Security Groups, ELB, Regions, Shield, WAF|
|Data Protection|KMS, Macie, ACM, Encryption at Rest/Transit|
|Detect & Respond|Inspector, GuardDuty, Detective, Security Hub|

## 🔤 Acronym Cheat Sheet

|Acronym|Full Form|
|---|---|
|IAM|Identity and Access Management|
|SSO|Single Sign-On|
|MFA|Multi-Factor Authentication|
|KMS|Key Management Service|
|WAF|Web Application Firewall|
|ACM|AWS Certificate Manager|
|ACL|Access Control List|
|ARN|Amazon Resource Name|
|DDoS|Distributed Denial of Service|
|PII|Personally Identifiable Information|
|DRT|DDoS Response Team (Shield Advanced)|

## 🎯 Top 20 Revision Points

1. Shared Responsibility: AWS = **of** the cloud; Customer = **in** the cloud.
2. Authentication = who you are; Authorization = what you can do.
3. Root user = unrestricted access — use only for emergencies, enable MFA immediately.
4. IAM is **global** and **free**.
5. New IAM users get **zero permissions** by default (implicit deny).
6. **Explicit Deny always overrides Allow.**
7. IAM Policies are JSON: Version, Effect, Action, Resource.
8. IAM Groups = easy permission management for multiple users at once.
9. IAM Roles = **temporary** credentials, no static keys — ideal for EC2/apps/federation.
10. IAM Identity Center = SSO across multiple AWS accounts/apps.
11. Secrets Manager = auto-**rotates** secrets (DB creds, API keys).
12. Systems Manager = centralized node management + patching.
13. DoS = single source; DDoS = multiple ("zombie bot") sources.
14. Defense layers: Security Groups → ELB → Regions → Shield → WAF.
15. Shield **Standard = free**; Shield **Advanced = paid** with diagnostics + DRT.
16. WAF operates at the **application layer** via **Web ACLs**; Shield operates at network layer.
17. S3 & DynamoDB encrypt at rest **by default**; EBS encryption must be enabled.
18. KMS manages **encryption keys**; Secrets Manager manages **secrets/credentials** — don't confuse them.
19. Macie = ML-based sensitive data (PII) discovery in **S3 only**.
20. Detect & Respond order: **Inspector (scan) → GuardDuty (detect) → Detective (investigate) → Security Hub (aggregate)**.

## 🧩 Common CCP Question Patterns

- "Who is responsible for X?" → Apply Shared Responsibility Model.
- "A company wants to eliminate hardcoded credentials in EC2 code" → **IAM Role**.
- "A company needs to protect against Layer 7 SQL injection" → **AWS WAF**.
- "A company wants free basic DDoS protection" → **Shield Standard**.
- "A company wants detailed DDoS attack diagnostics + expert response team" → **Shield Advanced**.
- "A company needs to auto-rotate database passwords" → **Secrets Manager**.
- "A company wants to know if PII is exposed in S3" → **Amazon Macie**.
- "A company wants a single dashboard of all security findings" → **AWS Security Hub**.
- "A company wants continuous, intelligent threat monitoring" → **Amazon GuardDuty**.
- "A company wants automated vulnerability scanning of EC2 fleet" → **Amazon Inspector**.

## 🌳 Final Decision Matrix — "Which Security Service Do I Need?"

```
Need to control WHO can access WHAT?
        │
        ▼
      IAM (Users/Groups/Roles/Policies)

Need to protect against network-layer DDoS?
        │
        ▼
      AWS Shield (Standard=free / Advanced=paid)

Need to filter application-layer (HTTP) threats like SQLi/XSS?
        │
        ▼
      AWS WAF

Need to manage encryption KEYS?
        │
        ▼
      AWS KMS

Need to manage database/API SECRETS with rotation?
        │
        ▼
      AWS Secrets Manager

Need to find sensitive data (PII) in S3?
        │
        ▼
      Amazon Macie

Need to scan EC2 fleet for vulnerabilities?
        │
        ▼
      Amazon Inspector

Need continuous threat monitoring?
        │
        ▼
      Amazon GuardDuty

Need to investigate a detected threat's root cause?
        │
        ▼
      Amazon Detective

Need ONE dashboard for all security findings?
        │
        ▼
      AWS Security Hub
```

## 🔗 Cross-Links to Related Modules

- **Module on Compute (EC2)** → IAM Roles attach directly to EC2 instances.
- **Module on Storage (S3)** → Default encryption at rest, Macie scans S3, bucket policies overlap with IAM.
- **Module on Networking (VPC)** → Security Groups vs NACLs (stateful vs stateless — revisit in networking module).
- **Module on Databases (RDS/DynamoDB)** → KMS-backed encryption at rest.
- **Module on Compliance** → AWS Artifact, Security Hub findings feed into compliance reporting.

---

**End of Module 9 — Security BIBLE Notes** 📘 _Exam Weight Reminder: This is the highest-weighted domain (~30%) on CLF-C02 — revise this module last before the exam for maximum retention._