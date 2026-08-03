# 📘 MODULE 11 — PRICING AND SUPPORT

### AWS Certified Cloud Practitioner (CLF-C02) — BIBLE Notes

---

## 🎯 MODULE ROADMAP

```
Pricing Fundamentals
        │
        ▼
Billing Models (Single vs Consolidated)
        │
        ▼
Billing & Cost Management Tools
   (Organizations, Billing Console, Budgets, Cost Explorer,
    Compute Optimizer, Pricing Calculator)
        │
        ▼
AWS Support Plans
   (Basic → Developer → Business → Enterprise On-Ramp → Enterprise)
        │
        ▼
Other Support Resources
   (re:Post, Trust & Safety Center, Marketplace, APN)
```

---

## 1️⃣ AWS PRICING FUNDAMENTALS ★★★★★

### The 3 Fundamental Pricing Drivers

| Driver                     | Meaning                                                        | Hinglish                                                                             |
| -------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Pay as you go**          | Pay only for what you use, no upfront commitment               | Jitna usage utna payment — bijli ka bill jaisa                                       |
| **Save when you commit**   | Commit to usage over a period (1 or 3 years) → discounted rate | Jaise gym ka annual membership — advance commit karo, per-visit cost kam ho jata hai |
| **Pay less by using more** | Volume-based discounts — usage badhao, per-unit cost ghata do  | Wholesale market — jitna zyada kharido, utna sasta per-unit                          |

**Why AWS provides this:** AWS wants to remove the capital expenditure (CapEx) barrier that traditional data centers had, converting it into operational expenditure (OpEx), while still rewarding customers who commit to predictable usage.

### 🧠 What AWS is REALLY testing

AWS isn't testing whether you can recite the three pricing models. AWS is testing whether you can **match a business scenario to the correct pricing philosophy** — e.g., a startup with unpredictable traffic → Pay-as-you-go; a stable enterprise workload running 24/7 for 3 years → commitment-based savings (Reserved Instances/Savings Plans).

### Where AWS Charges You (The 3 Billing Dimensions)

```
                ┌───────────────────────────┐
                │   WHAT AWS BILLS YOU FOR   │
                └───────────────────────────┘
                          │
     ┌────────────────────┼────────────────────┐
     ▼                     ▼                    ▼
  COMPUTE               STORAGE          DATA TRANSFER (OUT)
Kitni der resource    Kitna storage      Outbound data transfer
use hua (hours/       use kiya            hi charge hota hai
seconds)              (GB/month)          (Inbound is FREE)
```

⚠️ **Exam Trap:** Data transfer **IN** to AWS is generally **free**. Only **data transfer OUT** to the internet is charged (with exceptions like inter-AZ/inter-region transfer). This is one of the most repeated CCP trick points.

### 30-Second Revision — Pricing Fundamentals

- **Definition:** 3 pricing philosophies — pay-as-you-go, commitment discounts, volume discounts
- **Use Case:** Choosing the right cost strategy per workload predictability
- **Billed On:** Compute time, Storage amount, Outbound data transfer
- **Common Trap:** Inbound data transfer = free; only outbound is charged
- **Exam Importance:** ★★★★★

---

## 2️⃣ BILLING ACCOUNT MODELS ★★★★☆

### A. Single Account Billing

One AWS account → usage tracked and billed **only for that account**.

- **Hinglish analogy:** Ek akela dukaandar apna khud ka bill bharta hai — koi sharing nahi.
- **When to use:** Solo developers, small startups, single-team projects.
- **Limitation:** No consolidated visibility, no volume discount sharing across teams.

### B. Consolidated Billing (via AWS Organizations)

Multiple AWS accounts are linked under **one Management (Payer) Account**. All individual account usage rolls up into **one combined invoice**.

```
Example:
Management (Payer) Account
│
├── Development Account   → Bill: $120
├── Testing Account       → Bill: $80
├── Production Account    → Bill: $500
│
└── TOTAL INVOICE: $700  (one single bill sent to Payer Account)
```

- **Why AWS provides this:** Large organizations run many teams/projects across many accounts (a security & isolation best practice) — but finance teams still want **ONE invoice** to reconcile, plus **shared volume discounts**.
- **Real-world problem it solves:** A company with Dev, Test, and Prod as separate AWS accounts (for isolation/security) would otherwise get 3 separate invoices and lose out on bulk pricing tiers. Consolidated Billing merges usage to hit volume discount thresholds faster **and** simplifies accounting.
- **Key benefit:** Combined usage across linked accounts can qualify for **volume pricing tiers and Reserved Instance/Savings Plan sharing** that a single small account might never reach alone.
- **Security note:** Each linked account remains **isolated** for resources/access — consolidated billing does NOT mean shared access, only shared billing.

### 🧠 What AWS is REALLY testing

AWS isn't testing whether you know Consolidated Billing merges invoices. AWS is testing whether you understand it's a **feature of AWS Organizations** used for **multi-account governance + volume discount optimization**, not a security/access-sharing mechanism.

### 30-Second Revision — Billing Models

- **Definition:** Single account = 1 bill for 1 account; Consolidated = 1 bill for many linked accounts
- **Use Case:** Multi-team/multi-environment orgs wanting one invoice + shared discounts
- **Alternative:** N/A (Consolidated Billing is the standard multi-account approach)
- **Common Trap:** Consolidated billing ≠ shared resource access; it's billing-only
- **Exam Importance:** ★★★★☆

---

## 3️⃣ BILLING & COST MANAGEMENT SERVICES ★★★★★

This is a **cluster of services** that AWS CCP loves to test as "which tool does what" matching questions.

### Quick Comparison Table

| Service                                     | Purpose                                                                             | Key Verb                  | Hinglish One-Liner                                                       |
| ------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------ |
| **AWS Organizations**                       | Centrally manage multiple accounts + enables Consolidated Billing                   | _Manage & Group_          | Sab accounts ka ek parivar banata hai                                    |
| **AWS Billing and Cost Management Console** | Central dashboard to view/download invoices, monitor discounts & credits            | _View & Track_            | Bill dekhne ka dashboard                                                 |
| **AWS Budgets**                             | Set custom cost/usage limits + get alerts before overspending                       | _Alert & Prevent_         | Ghar ka monthly budget alarm                                             |
| **AWS Cost Explorer**                       | Visualize, analyze historical cost/usage + forecast future costs                    | _Visualize & Forecast_    | Cost ka graph/report banane wala                                         |
| **AWS Compute Optimizer**                   | Recommends optimal AWS resource configurations to reduce cost & improve performance | _Recommend & Rightsize_   | "Tum overpowered resource use kar rahe ho, chhota lo" bolne wala advisor |
| **AWS Pricing Calculator**                  | Free web tool to **estimate costs BEFORE deployment**                               | _Estimate (Pre-purchase)_ | Kharidne se pehle ka price quotation                                     |

> Note: The notes mention "AWS Cost Optimizer" — the correct current AWS service name is **AWS Compute Optimizer**, which analyzes usage patterns and recommends optimal instance types/sizes to reduce cost and improve performance.

### 📌 Deep Dive: Each Service

#### AWS Organizations

- **Definition:** Service to centrally manage and govern multiple AWS accounts.
- **Why AWS provides this:** Enterprises need account-level isolation (security) but still want centralized control.
- **Features:** Consolidated Billing, Service Control Policies (SCPs) for governance, automated account creation.
- **When to use:** Any company with 2+ AWS accounts.
- **Exam trap:** ⚠️ SCP (governance/permissions) is a _different_ feature from Consolidated Billing (cost) — both live under Organizations but serve different purposes.

#### AWS Billing and Cost Management Console

- **Definition:** The central hub for all things billing — invoices, credits, discounts, spend trends.
- **Real-world scenario:** A finance manager logs in monthly to download the invoice PDF and check if Reserved Instance discounts were applied correctly.

#### AWS Budgets

- **Definition:** Proactive tool — set a **maximum (and minimum)** cost/usage threshold and get **alerted** (email/SNS) when you approach or exceed it.
- **Why AWS provides this:** Prevents "bill shock" — a very common real fear for students and startups on free tier.
- **When to use:** Anyone worried about accidental overspend (e.g., forgot to shut down an EC2 instance).
- **When NOT to use:** It does not _automatically stop_ resources by default — it's an **alerting** tool, not a hard cutoff (though it CAN trigger automated actions if configured).
- ⚠️ **Exam Trap:** Budgets = **proactive/preventive** (before/during spend). Cost Explorer = **reactive/analytical** (after spend, historical). This distinction is a favorite CCP trap.

#### AWS Cost Explorer

- **Definition:** Visualization and analysis tool for reviewing **historical** cost/usage patterns with **forecasting** capability.
- **Real-world scenario:** A DevOps engineer wants to see "which service cost the most last quarter" — Cost Explorer, not Budgets.
- **Memory trick:** "Cost **Explorer** = **Explore** the past + peek into the future (forecast)."

#### AWS Compute Optimizer

- **Definition:** Uses machine learning to analyze historical utilization and recommend optimal AWS resource types/sizes (EC2, EBS, Lambda, Auto Scaling groups).
- **Why AWS provides this:** Many customers over-provision "just in case," wasting money. Compute Optimizer gives **data-driven rightsizing recommendations**.
- **Real-world scenario:** A company running oversized EC2 instances at 10% CPU utilization — Compute Optimizer suggests downsizing, cutting cost without hurting performance.

#### AWS Pricing Calculator

- **Definition:** Free, web-based **pre-purchase estimation tool** — build a hypothetical architecture and get an estimated monthly/annual cost.
- **When to use:** BEFORE deploying — for budgeting/proposal purposes.
- **When NOT to use:** Not for tracking actual/real incurred costs (that's Cost Explorer/Billing Console).
- ⚠️ **Exam Trap:** Pricing Calculator = **estimate before you build**. Cost Explorer = **analyze after you've spent**. Confusing these two is one of the most common CCP mistakes.

### 🌳 Decision Tree — Which Cost Tool Do I Need?

```
Need to know cost BEFORE deploying anything?
        │
        Yes → AWS Pricing Calculator
        │
        No
        │
Want to PREVENT overspending with alerts?
        │
        Yes → AWS Budgets
        │
        No
        │
Want to ANALYZE past spend / forecast trend?
        │
        Yes → AWS Cost Explorer
        │
        No
        │
Want recommendations to RIGHTSIZE resources?
        │
        Yes → AWS Compute Optimizer
        │
        No
        │
Want ONE invoice across MULTIPLE accounts?
        │
        Yes → AWS Organizations (Consolidated Billing)
```

### 30-Second Revision — Cost Management Tools

- **Definition:** A toolkit for estimating, tracking, alerting, analyzing, and optimizing AWS costs
- **Use Case:** Cost governance across the full lifecycle — before, during, and after spend
- **Alternative Mapping:** Pricing Calculator (before) → Budgets (during/prevent) → Cost Explorer (after/analyze) → Compute Optimizer (optimize)
- **Common Trap:** Pricing Calculator vs Cost Explorer vs Budgets — timing is the key differentiator
- **Exam Importance:** ★★★★★

---

## 4️⃣ AWS SUPPORT PLANS ★★★★★

AWS offers **4 tiers** of support (Basic, Developer, Business, Enterprise — with Enterprise having an "On-Ramp" sub-tier). This is one of the **highest-yield topics** in the entire CLF-C02 exam.

### 🧠 What AWS is REALLY testing

AWS isn't testing whether you can list plan names. AWS is testing whether you can **match a company's size/urgency/risk profile to the correct support tier** — especially recognizing **response time SLAs** and **who gets a Technical Account Manager (TAM)**.

### Master Comparison Table

|Feature|Basic|Developer|Business|Enterprise On-Ramp|Enterprise|
|---|---|---|---|---|---|
|**Cost**|Free (all accounts)|Low fixed fee|% of usage (tiered)|% of usage (tiered)|% of usage (tiered)|
|**Target Audience**|Everyone|Experimenting / early-stage business|Production workloads on AWS|Growing businesses w/ critical workloads|Business/mission-critical workloads|
|**24/7 Customer Service**|✅ (account/billing only)|✅|✅|✅|✅|
|**AWS Trusted Advisor**|✅ (core checks only)|✅ (core checks)|✅ (Full — all checks)|✅ Full|✅ Full|
|**Support Forums / re:Post**|✅|✅|✅|✅|✅|
|**AWS Personal Health Dashboard**|✅|✅|✅|✅|✅|
|**Direct technical support (phone/chat/email)**|❌|Email only|✅ Phone, Chat, Email|✅|✅|
|**Infrastructure Event Management**|❌|❌|Available (add-on)|✅|✅|
|**Technical Account Manager (TAM)**|❌|❌|❌|✅ (pooled)|✅ (dedicated)|
|**Response Time — General guidance**|N/A|24 hrs|24 hrs / 12 hrs / 4 hrs (by severity)|Faster tiers|Faster tiers|
|**Response Time — Production system impaired**|N/A|N/A|4 hours|4 hours|1 hour|
|**Response Time — Production system down**|N/A|N/A|1 hour|1 hour|15 minutes|
|**Response Time — Business-critical system down**|N/A|N/A|1 hour|30 minutes|**15 minutes**|

> ⚠️ Note: Exact numeric response-time SLAs are updated periodically by AWS and go slightly beyond core CCP depth — but the **relative ordering and the fastest tier (Enterprise = fastest, ~15 min for business-critical down)** is a well-known CCP exam pattern worth remembering conceptually.

### Plan-by-Plan Breakdown

#### 🔹 Basic Support — ★★★★★

- **Definition:** Free tier of support, included automatically with every AWS account.
- **Includes:** 24/7 access to customer service (account & billing only, NOT technical), AWS Trusted Advisor (7 core checks), AWS Support Forums (re:Post), AWS Personal Health Dashboard.
- **Hinglish analogy:** Jaise naya phone kharidne pe basic warranty milta hai — free but limited.
- **When NOT to use:** Any production business workload — no technical support included.

#### 🔹 Developer Support — ★★★☆☆

- **Definition:** Entry-level paid plan for people **testing/experimenting** in AWS.
- **Includes:** Everything in Basic + ability to **email** AWS Cloud Support directly with a **~24 hour response time** (business hours only, one contact).
- **Real-world scenario:** A solo developer building an MVP/side project wants a safety net for technical questions.
- **Exam trap:** ⚠️ Developer plan = **single contact, business-hours email only** — NOT 24/7 phone.

#### 🔹 Business Support — ★★★★★

- **Definition:** Designed for customers running **production workloads** on AWS.
- **Includes:** Everything in Developer + **24/7 phone/chat/email**, **Full Trusted Advisor** (all checks), unlimited contacts, response time as fast as **1 hour** for production-down issues, optional Infrastructure Event Management (for planned high-risk events like a big sale).
- **Real-world scenario:** An e-commerce company with a live production website needs guaranteed fast support if checkout breaks.

#### 🔹 Enterprise On-Ramp — ★★★☆☆

- **Definition:** A middle-tier plan bridging Business and Enterprise — for growing organizations with **increasing dependence on AWS** for critical workloads, not yet needing full Enterprise-scale support.
- **Includes:** Everything in Business + a **pool of TAMs** (Technical Account Managers) — not one dedicated, but shared access to TAM expertise, faster response for business-critical down (30 min).

#### 🔹 Enterprise Support — ★★★★★

- **Definition:** The top-tier plan for **business/mission-critical** workloads.
- **Includes:** Everything in Business + a **dedicated Technical Account Manager (TAM)**, Concierge support team, fastest response time (**15 minutes** for business-critical system down), proactive guidance (Well-Architected reviews, operations reviews).
- **Real-world scenario:** A large bank or streaming platform (Netflix-scale) where 1 minute of downtime = massive financial loss.

### ⚠️ Common Exam Traps — Support Plans

- Basic Support's 24/7 customer service is **account and billing support only**, NOT technical support — huge trap.
- A **Technical Account Manager (TAM)** is exclusive to **Enterprise (dedicated)** and **Enterprise On-Ramp (pooled)** — NOT Business.
- **AWS Trusted Advisor**: only **7 core checks** free on Basic/Developer; **Full Trusted Advisor** (all checks across cost, performance, security, fault tolerance, service limits) requires **Business tier or above**.
- The plan pricing is generally **based on a % of your monthly AWS usage** (with a minimum), NOT a flat rate for Business/Enterprise — flat fee only applies to Developer.

### 30-Second Revision — Support Plans

- **Definition:** 4 tiers (+1 sub-tier) of AWS customer support, from free to dedicated TAM
- **Use Case:** Match business criticality → correct support tier
- **Alternative:** N/A — this is AWS's own support ladder
- **Pricing:** Free (Basic) → Flat fee (Developer) → % of usage (Business/On-Ramp/Enterprise)
- **Common Trap:** Basic ≠ technical support; TAM only on On-Ramp (pooled) & Enterprise (dedicated)
- **Exam Importance:** ★★★★★

---

## 5️⃣ AWS MARKETPLACE ★★★☆☆

### Definition

A **curated digital catalog** to find, test, buy, deploy, and manage **third-party software** that runs on AWS infrastructure.

### Why AWS provides this

Reduces **Total Cost of Ownership (TCO)** and accelerates innovation — customers don't need to build common software from scratch (e.g., a WAF, a BI tool, an ML model) when a vetted third-party solution already exists.

### Categories Available

|Category|Examples|
|---|---|
|**SaaS**|Project management tools, marketing/customer engagement platforms, file-sharing/collaboration tools|
|**ML & AI**|Prebuilt models (image recognition, NLP), custom-training algorithms|
|**Data & Analytics**|BI/visualization platforms, data integration tools|

### Key Benefits

- Flexible pricing: **pay-as-you-go** and **annual subscription** options
- Reduces procurement complexity
- Purchases can be **consolidated into your existing AWS bill**

### 🧠 What AWS is REALLY testing

AWS isn't testing whether you know Marketplace sells software. AWS is testing whether you know it lets you **buy third-party ISV software with billing folded into your AWS invoice** — a key value prop question.

### 30-Second Revision — AWS Marketplace

- **Definition:** Digital storefront for third-party software on AWS
- **Use Case:** Buy vetted software instead of building in-house
- **Pricing:** Pay-as-you-go or annual subscription, billed via AWS invoice
- **Common Trap:** Marketplace software ≠ AWS-built service; it's from Independent Software Vendors (ISVs)
- **Exam Importance:** ★★★☆☆

---

## 6️⃣ AWS PARTNER NETWORK (APN) ★★☆☆☆

### Definition

A **global community/program** for technology and consulting businesses that use AWS to build solutions and services for customers.

### Why it exists

AWS is heavily invested in **customer success** — APN connects customers to specialized partners (e.g., a retail company hosting on AWS partnering with an analytics/ML specialist partner for personalization).

### Key Partner Benefits

|Benefit|What it means|
|---|---|
|**Funding Benefits**|Credits/discounts to help partners build, market, sell on AWS|
|**AWS Partner Events**|Webinars, workshops, in-person networking with AWS experts|
|**AWS Partner Training & Certification**|Specialized upskilling tracks for partner organizations|

### Hinglish Analogy

Jaise ek real estate builder (AWS) apne trusted interior designers/contractors (Partners) ka network banata hai jinhe customer ko refer kar sake.

### 30-Second Revision — APN

- **Definition:** Global program connecting AWS with consulting/tech partner companies
- **Use Case:** Customers needing specialized implementation help; companies wanting to build a business around AWS
- **Common Trap:** APN is about **partner ecosystem**, not a support plan — don't confuse with TAM/Enterprise Support
- **Exam Importance:** ★★☆☆☆

---

## 7️⃣ AWS RE:POST & TRUST AND SAFETY CENTER ★★★☆☆

|Service|Definition|Analogy|
|---|---|---|
|**AWS re:Post**|Community-driven Q&A platform where users seek help, share knowledge, find solutions|"Reddit for AWS users" — free, community-powered|
|**AWS Trust and Safety Center**|Central place to **report abusive activity** happening on AWS (e.g., phishing, malware hosted on AWS resources)|AWS ka "complaint/police station" for platform abuse|

⚠️ **Exam Trap:** re:Post is **free and community-driven** (not an official guaranteed-response support channel) — it supplements, but does NOT replace, paid Support Plans.

---

## 📊 MODULE-END SUMMARY

### Quick Summary Table

|Category|Key Services|One-Line Purpose|
|---|---|---|
|Pricing Philosophy|Pay-as-you-go, Commit & Save, Pay-less-by-more|How AWS charges conceptually|
|Billing Models|Single Account, Consolidated Billing|How many invoices you get|
|Governance|AWS Organizations|Manage multiple accounts centrally|
|Tracking|Billing & Cost Mgmt Console|View invoices/credits|
|Prevention|AWS Budgets|Alerts before overspend|
|Analysis|AWS Cost Explorer|Visualize past + forecast|
|Optimization|AWS Compute Optimizer|Rightsizing recommendations|
|Estimation|AWS Pricing Calculator|Pre-purchase cost estimate|
|Human Help|Support Plans (Basic→Enterprise)|Technical/account support tiers|
|Marketplace|AWS Marketplace|Buy 3rd-party software|
|Ecosystem|AWS Partner Network (APN)|Consulting/tech partner community|
|Community|AWS re:Post|Free peer Q&A|
|Abuse Reporting|Trust & Safety Center|Report platform abuse|

### 🔤 Acronym Cheat Sheet

- **APN** – AWS Partner Network
- **TAM** – Technical Account Manager
- **TCO** – Total Cost of Ownership
- **SCP** – Service Control Policy (Organizations governance, not billing)
- **ISV** – Independent Software Vendor
- **SLA** – Service Level Agreement

### 🏆 Top 20 Revision Points

1. Pay-as-you-go = no commitment, usage-based
2. Save when you commit = 1yr/3yr commitment discount
3. Pay less by using more = volume discount
4. Inbound data transfer = FREE; only outbound is charged
5. Single account billing = isolated invoice
6. Consolidated Billing = feature of AWS Organizations → one invoice for many accounts
7. Consolidated Billing shares volume discounts, does NOT share access/security
8. AWS Organizations also provides SCPs for governance (separate from billing)
9. Billing Console = view/download invoices, monitor credits/discounts
10. AWS Budgets = proactive, alerts before overspend
11. AWS Cost Explorer = reactive, historical analysis + forecasting
12. AWS Compute Optimizer = ML-based rightsizing recommendations
13. AWS Pricing Calculator = pre-purchase cost estimation (free tool)
14. Basic Support = free, account/billing support only, NO technical support
15. Developer Support = single contact, business-hours email, ~24hr response
16. Business Support = 24/7 phone/chat/email, Full Trusted Advisor, 1hr response for production-down
17. Enterprise On-Ramp = pooled TAM access, faster response tiers
18. Enterprise Support = dedicated TAM, fastest response (~15 min business-critical down)
19. AWS Marketplace = buy third-party ISV software, billed via AWS invoice
20. AWS re:Post = free community Q&A; Trust & Safety Center = report abuse

### 🎯 Common CCP Question Patterns

- "A company wants ONE invoice for 5 AWS accounts" → **Consolidated Billing (AWS Organizations)**
- "A company wants to be ALERTED before exceeding a budget" → **AWS Budgets**
- "A company wants to estimate cost BEFORE launching a new architecture" → **AWS Pricing Calculator**
- "A company wants to see WHERE money was spent last quarter" → **AWS Cost Explorer**
- "A company wants recommendations to reduce EC2 costs based on usage" → **AWS Compute Optimizer**
- "A startup wants FREE support with basic guidance" → **Basic Support Plan**
- "A production e-commerce site needs guaranteed 1-hour response if down" → **Business Support**
- "A mission-critical bank system needs a dedicated point of contact" → **Enterprise Support (TAM)**
- "A company wants to buy a third-party firewall/WAF that runs on AWS" → **AWS Marketplace**
- "A company needs a consulting partner to help migrate" → **AWS Partner Network (APN)**

### 🧭 Final Decision Matrix

|Need|Correct Answer|
|---|---|
|One bill, many accounts|AWS Organizations → Consolidated Billing|
|Prevent overspend|AWS Budgets|
|Analyze past spend|AWS Cost Explorer|
|Estimate future spend|AWS Pricing Calculator|
|Rightsizing advice|AWS Compute Optimizer|
|Free support|Basic|
|Solo dev / experimenting|Developer|
|Production workload|Business|
|Growing critical workload|Enterprise On-Ramp|
|Mission-critical, dedicated TAM|Enterprise|
|Buy 3rd-party software|AWS Marketplace|
|Need implementation partner|APN|
|Free community help|re:Post|
|Report platform abuse|Trust and Safety Center|

### 🔗 Cross-Links to Related Modules

- **Module: Cloud Fundamentals** → CapEx vs OpEx ties directly into "why pricing models exist"
- **Module: Global Infrastructure** → Data transfer pricing depends on Regions/AZs (inter-region transfer cost)
- **Module: Security/IAM** → AWS Organizations SCPs (governance side, distinct from billing side)
- **Module: Compute (EC2)** → Reserved Instances / Savings Plans = the practical implementation of "save when you commit"

---

_BIBLE Notes — Module 11: Pricing and Support | AWS CCP (CLF-C02) | Compiled 16 July_