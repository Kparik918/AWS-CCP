# MODULE 8 — AI/ML & Data Analytics (CLF-C02) — BIBLE Notes

---

## 8.0 The Big Picture — AI → ML → DL → Gen AI

```
        ┌─────────────────────────────────────────┐
        │  ARTIFICIAL INTELLIGENCE (AI)             │
        │  "Machine karna chahti hai insaan jaisa   │
        │   sochna" — replicate human cognition      │
        │  ┌───────────────────────────────────┐    │
        │  │  MACHINE LEARNING (ML)             │    │
        │  │  Trains on data → finds patterns   │    │
        │  │  ┌─────────────────────────────┐   │    │
        │  │  │  DEEP LEARNING (DL)          │   │    │
        │  │  │  Neural networks, layers     │   │    │
        │  │  │  ┌───────────────────────┐   │   │    │
        │  │  │  │  GENERATIVE AI        │   │   │    │
        │  │  │  │  Creates NEW content  │   │   │    │
        │  │  │  └───────────────────────┘   │   │    │
        │  │  └─────────────────────────────┘   │    │
        │  └───────────────────────────────────┘    │
        └─────────────────────────────────────────┘
```

**AI** — Branch of computer science that makes machines perform tasks needing human cognition (reasoning, perception, decision-making). Outcomes AWS cares about: **Precision, Accuracy, Speed**.

**ML** — Subset of AI. Feed it large volumes of data → it finds patterns/relationships → produces a **model** → model is applied to new/unseen data to predict or decide.

**NLP** — Branch of AI that lets machines understand, interpret, and generate human language (text/speech).

**Gen AI** — Gen AI ka matlab: AI jo naya content banaata hai — text, image, video, audio, code — kuch bhi. Powered by **Foundation Models (FMs)**: massive, pre-trained ML models trained on huge, broad datasets, adaptable to many downstream tasks (chat, summarization, image generation, code-gen) without training from scratch.

**Hinglish Analogy — The Restaurant**

- **AI** = the entire restaurant's promise ("we'll cook you a great meal exactly how you like it")
- **ML** = the chef who learns from thousands of past orders which spices work for which customer
- **DL** = a master chef with years of layered experience (neural "layers") who can handle very complex dishes
- **Gen AI** = a chef who doesn't just cook known dishes — he **invents a brand-new dish** on the spot based on what he's learned

★★★★★ **Exam Importance: Critical** — AWS loves asking "which layer is this: AI, ML, or Gen AI?"

---

## 8.1 AWS AI/ML Stack — Three Layers

```
┌───────────────────────────────────────────┐
│ Layer 3: AI SERVICES                      │  ← No ML expertise needed
│   Pre-trained, ready-to-use, plug & play  │
├───────────────────────────────────────────┤
│ Layer 2: ML SERVICES                      │  ← Some ML expertise
│   Build/train/deploy YOUR OWN models      │
├───────────────────────────────────────────┤
│ Layer 1: ML FRAMEWORKS & INFRASTRUCTURE   │  ← Deep ML expertise
│   Raw compute + frameworks (TensorFlow,   │
│   PyTorch) + AWS silicon (Trainium/Inferentia)│
└───────────────────────────────────────────┘
```

**Rule of thumb (exam trap magnet):** The lower the layer, the more control you get — but the more expertise you need. The higher the layer, the faster you ship — but less customization.

### What AWS is REALLY testing

AWS isn't testing whether you can name AI services. AWS is testing whether you know **which layer** fits a business need: "I have no data scientists, I just want sentiment analysis" → AI Services. "I have data scientists who want to build a custom fraud model" → ML Services (SageMaker). "I want to train massive custom models with full control over chips/frameworks" → ML Frameworks & Infrastructure.

---

## 8.2 AI Services (Layer 3) — Pre-built, Managed, No ML Skill Needed

★★★★★ Exam Importance: Critical — This is the **most tested table** in the entire module. Memorize the verb attached to each service.

|Service|One-line Definition|Key Verb to Remember|
|---|---|---|
|**Amazon Polly**|Converts text → lifelike speech|"Polly **speaks**" (Text-to-Speech)|
|**Amazon Transcribe**|Converts speech/audio → text|"Transcribe **listens**" (Speech-to-Text)|
|**Amazon Translate**|Translates text between languages|"Translate **converts languages**"|
|**Amazon Comprehend**|NLP — extracts insights, sentiment, key phrases, entities from text|"Comprehend **understands feelings/meaning**"|
|**Amazon Kendra**|Intelligent enterprise search — answers natural-language questions from your documents|"Kendra **answers questions**"|
|**Amazon Rekognition**|Identifies objects, people, text, activities in **images and videos**|"Rekognition **sees**"|
|**Amazon Textract**|Detects & extracts typed/handwritten text, tables, forms from documents|"Textract **reads documents**"|
|**Amazon Lex**|Builds conversational chatbots/voice assistants (powers Alexa)|"Lex **talks/chats**"|
|**Amazon Personalize**|Builds real-time personalized product/content recommendations from historical data|"Personalize **recommends**"|

### ⚠️ Common Exam Traps

- **Rekognition vs Textract** — Both deal with images, but **Rekognition = objects/scenes/faces**, **Textract = TEXT extraction (forms, tables, handwriting)**. AWS loves a question showing a scanned invoice and asking "which service?" → Textract, NOT Rekognition.
- **Transcribe vs Translate vs Polly** — Direction matters:
    - Speech → Text = **Transcribe**
    - Text → Text (different language) = **Translate**
    - Text → Speech = **Polly**
- **Comprehend vs Kendra** — Comprehend analyzes/extracts meaning FROM text you feed it. Kendra lets END USERS ask natural-language QUESTIONS and searches your document repository for the answer. Comprehend = analysis; Kendra = search engine.
- **Lex vs Kendra** — Lex builds the chatbot interface; Kendra is the enterprise search brain. They can be combined but are NOT the same service.

### Real AWS Scenario

A bank wants to auto-transcribe customer service calls, detect negative sentiment, and flag angry customers for review → **Transcribe** (call → text) + **Comprehend** (sentiment analysis on that text).

### 30-Second Revision — AI Services

- **Definition:** Managed, pre-trained AI models, no ML expertise required
- **Use case:** Fast time-to-market business features (chatbots, search, translation, moderation)
- **Alternative:** SageMaker (if you need a custom model instead)
- **Pricing:** Pay-per-use/API call (no infra to manage)
- **Common Trap:** Rekognition (images) vs Textract (text-in-images) confusion
- **Exam Importance:** ★★★★★

---

## 8.3 ML Services (Layer 2) — Build Your Own Models

### Amazon SageMaker AI

**Definition:** Fully managed service to **build, train, and deploy your own ML models** without managing underlying infrastructure.

**Why AWS provides it:** Data scientists need compute, notebooks, training pipelines, and deployment endpoints — SageMaker bundles all of it so teams don't manage servers.

**When to use:** You have custom data and need a model tailored exactly to your business problem (not solved by an off-the-shelf AI Service).

**When NOT to use:** If a pre-built AI service (e.g., Rekognition, Comprehend) already solves your problem — building custom is wasted effort/cost.

### Amazon SageMaker JumpStart

**Definition:** A hub of **pre-trained, open-source ML solutions** (computer vision, NLP, tabular data models) you can deploy with a few clicks, then fine-tune further if needed — a middle ground between "fully pre-built AI Service" and "build entirely from scratch in SageMaker."

**Hinglish Analogy — The Apartment**

- **AI Services** = renting a fully furnished flat (move in today, no customization)
- **SageMaker JumpStart** = renting a semi-furnished flat (basic setup exists, you add your own touches)
- **SageMaker AI (from scratch)** = buying empty land and constructing your own house (full control, full effort)

### Decision Tree

```
Need ML capability?
   │
   ├── Off-the-shelf model solves it? ──Yes──> Use AI Service (Polly, Rekognition...)
   │
   └── No, need customization
          │
          ├── Want a pre-trained starting point? ──Yes──> SageMaker JumpStart
          │
          └── Need fully custom model, full control ──> SageMaker AI
```

### What AWS is REALLY testing

AWS isn't testing whether you know SageMaker "trains models." AWS is testing whether you know **when to reach for SageMaker instead of an AI service** — i.e., recognizing the business needs customization, not just a ready-made API.

### 30-Second Revision — ML Services

- **Definition:** Managed infra to build/train/deploy custom ML models
- **Use case:** Custom problems that AI Services can't solve
- **Alternative:** AI Services (if pre-built fits) / raw ML frameworks (if you need lower-level control)
- **Pricing:** Pay for compute/storage used during training & hosting (notebook instances, training jobs, endpoints)
- **Common Trap:** Choosing SageMaker when a cheaper, faster AI Service already does the job
- **Exam Importance:** ★★★★☆

---

## 8.4 ML Frameworks & Infrastructure (Layer 1)

**Definition:** The foundational layer — lets ML experts build, train, and deploy models using popular open-source frameworks (TensorFlow, PyTorch) on **AWS purpose-built ML chips** (e.g., AWS Trainium for training, AWS Inferentia for inference) and Deep Learning AMIs/Containers.

**When to use:** Only for organizations with deep in-house ML/data-science expertise needing maximum control and cost-efficiency at scale.

**Exam depth needed:** Recognition only — CLF-C02 just wants you to know this layer **exists** and sits _below_ SageMaker. No need to know chip architecture.

★★☆☆☆ Exam Importance: Recognition Only

---

## 8.5 Generative AI Services

### Amazon Bedrock

**Definition:** Fully managed service giving **API access to foundation models from Amazon AND leading third-party AI companies** (e.g., Anthropic, Meta, Stability AI) — fine-tune and integrate FMs into your apps through a single API, serverless, no infrastructure to manage.

**Why AWS provides it:** Businesses want to experiment with multiple FMs without hosting infrastructure or negotiating with each model provider separately.

**Real-world problem it solves:** "I want to try Claude AND another FM without managing GPUs or separate vendor contracts."

### Amazon Q — Two Flavors

Apne data ko do iss service ko, phir vo banayega apne liye ek virtual assistant/chatbot jo kaam karega apne data ke related sawaalon ke jawaab dene ka.

|Variant|Purpose|
|---|---|
|**Amazon Q Developer**|Coding-related — code recommendations, accelerates development|
|**Amazon Q Business**|General business use — answers questions using YOUR company's internal data/repositories|

### Comparison Table — Bedrock vs SageMaker vs AI Services

|Aspect|AI Services|Amazon Bedrock|SageMaker AI|
|---|---|---|---|
|Model type|Pre-built task-specific|Foundation Models (Gen AI)|Any custom ML model|
|Customization|None/minimal|Fine-tune FMs|Full control|
|Skill needed|None|Low-Medium|Medium-High|
|Best for|Standard tasks (translate, transcribe)|Gen AI apps (chat, content gen)|Custom business ML models|

### ⚠️ Common Exam Traps

- Confusing **Amazon Q Business** (uses your company data to answer questions) with **Amazon Kendra** (enterprise search). Q Business is more "conversational assistant," Kendra is "search + Q&A engine" — they're related but distinct services.
- Assuming Bedrock **trains** models from scratch — it doesn't; it gives access to **existing** FMs for fine-tuning/integration, not ground-up training.

### 30-Second Revision — Gen AI Services

- **Definition:** Managed access to foundation models (Bedrock) + AI assistants built on your data (Amazon Q)
- **Use case:** Chatbots, content generation, coding assistants, internal knowledge Q&A
- **Alternative:** SageMaker JumpStart (deploy an open FM yourself) if Bedrock doesn't offer the model you want
- **Pricing:** Pay per API call/token usage, serverless
- **Common Trap:** Q Business vs Kendra vs Bedrock mix-up
- **Exam Importance:** ★★★★★

---

## 8.6 Data Analytics — Why It Exists

Data har jagah hai — har cheez jo hum internet pe karte hain wo data generate karti hai. Itna saara raw data se seedha kuch nahi milta — patterns, trends, customer choices nikaalne ke liye us data ko **collect → structure → analyze → visualize** karna padta hai. That's the job of a data pipeline.

### Data Lakes vs Data Warehouses

|Aspect|Data Lake|Data Warehouse|
|---|---|---|
|Data type|Raw, unstructured/semi-structured, "as-is"|Structured, cleaned, schema-defined|
|Volume|Vast, virtually limitless|Large but curated|
|Primary AWS service|**Amazon S3**|**Amazon Redshift**|
|Use case|Store everything cheaply now, decide structure later|Fast complex SQL analytics on structured business data|
|Users|Data scientists, ML engineers|Business analysts, BI teams|

**Hinglish Analogy — The Warehouse vs The Library**

- **Data Lake** = ek bada godown jaha sab kuch phenk diya — kabhi bhi sort karke nikaal sakte ho (flexible, messy)
- **Data Warehouse** = ek organized library jaha har kitaab ka fixed shelf number hai (structured, fast to query, but you must "shelve" data properly before storing it)

### ⚠️ Common Exam Traps

- Data Lake = S3 (raw/unstructured). Data Warehouse = Redshift (structured). Swapping these in a question is a classic trap.
- A giant pile of data with NO structure is **useless on its own** — this is why ETL exists.

---

## 8.6.1 AWS Data Exchange

**Definition:** A service that lets you **find, subscribe to, and use third-party data directly from AWS** — instead of generating/collecting the data yourself, you "buy" or subscribe to ready-made datasets from external providers, delivered straight into your AWS environment (e.g., S3).

**Why AWS provides it:** Not every company has (or needs) the resources to collect certain data themselves — e.g., weather data, financial market data, healthcare datasets. Data Exchange acts as a **marketplace** connecting data providers with data consumers, all within AWS.

**Real-world problem it solves:** "We need historical weather data for our logistics ML model, but we have no way to collect years of weather history ourselves." → Subscribe to a weather dataset via AWS Data Exchange instead of building a collection pipeline from scratch.

**When to use:** You need external, third-party data (not your own company's data) to enrich analytics or train ML models.

**When NOT to use:** For your own internal company data — that belongs in S3/Redshift via your own pipeline, not Data Exchange (Data Exchange is for **external** data sourcing).

**Hinglish Analogy:** Your own data pipeline (S3/Redshift/Glue) is like growing your own vegetables at home. **AWS Data Exchange** is like going to the sabzi mandi (market) to directly buy vegetables someone else already grew — faster, no need to farm it yourself.

### ⚠️ Exam Trap

Don't confuse Data Exchange with a data _storage_ or _processing_ service — it's a **marketplace/subscription** service for acquiring external datasets, not a place you build pipelines in.

★★☆☆☆ Exam Importance: Recognition Only

---

## 8.7 ETL vs ELT

**ETL = Extract → Transform → Load**

1. **Extract** — pull data from various sources
2. **Transform** — clean/convert into a consistent, usable format
3. **Load** — push into destination (data warehouse/analytics platform)

**ELT = Extract → Load → Transform** — load raw data first, transform later (common with modern data lakes where transformation happens on-demand).

**Memory Trick:** "Pehle nikaalo (Extract), phir sudharo (Transform), phir bhejo (Load)" — for ETL. For ELT, just swap Load and Transform order: raw data pehle safe jagah pahucha do, baad me saaf karo.

★★★★☆ Exam Importance: Very Common

---

## 8.8 The Full Data Pipeline — 5 Steps

```
COLLECT → INGEST → PROCESS → ANALYZE → VISUALIZE
```

Data pipelines are **automated assembly lines** that make the ETL process efficient, repeatable, and fast.

### Step 1 — Collect

|Data Type|Storage Service|
|---|---|
|Unstructured (Data Lake)|**Amazon S3**|
|Structured (Data Warehouse)|**Amazon Redshift**|

### Step 2 — Ingest (moving data from source → destination)

|Service|Type|Key Trait|
|---|---|---|
|**Amazon Kinesis Data Streams**|Real-time ingestion|Low latency; multiple consumers can read the same stream simultaneously|
|**Amazon Data Firehose**|Near-real-time / batch ingestion|Batches, compresses, and encrypts data automatically before loading into destination (S3, Redshift, etc.)|

#### Comparison Table — Kinesis Data Streams vs Data Firehose

| Aspect               | Kinesis Data Streams                                          | Amazon Data Firehose                                           |
| -------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| Latency              | Real-time (milliseconds)                                      | Near real-time (seconds, buffered)                             |
| Consumers            | Multiple apps can consume same stream                         | Delivers directly to a fixed destination                       |
| Management           | You manage shards/scaling (or on-demand mode)                 | Fully managed, no shard management                             |
| Transform on the fly | Custom consumer app logic                                     | Built-in batch/compress/encrypt, optional Lambda transform     |
| Best for             | Real-time analytics dashboards, multiple simultaneous readers | Simple "ingest and dump into S3/Redshift/OpenSearch" pipelines |

### ⚠️ Exam Trap

Kinesis Data Streams = you build the real-time consumer application. Firehose = fully managed delivery, **no consumer app needed** — it just lands data in the destination. AWS often tests "which one requires the LEAST management?" → Firehose.

### Amazon MSK (Managed Streaming for Apache Kafka)

**Definition:** A fully managed service to run **Apache Kafka** — a popular open-source tool for real-time data streaming — without manually setting up, patching, or scaling Kafka clusters yourself.

**Why AWS provides it:** Many companies already use Kafka (open-source, industry-standard) for streaming and don't want to rebuild that architecture on Kinesis — MSK lets them keep using Kafka's tools/APIs while AWS manages the operational heavy-lifting (broker setup, patching, scaling, monitoring).

**Real-world problem it solves:** "We already have a Kafka-based streaming pipeline built by our engineering team — we don't want to re-architect it on Kinesis, we just want AWS to manage the Kafka servers for us."

**When to use:** You (or your team) are already invested in the Kafka ecosystem, use Kafka-specific tools, or need Kafka's specific features/compatibility.

**When NOT to use:** Starting fresh with no Kafka dependency — Kinesis Data Streams is usually simpler and more "AWS-native" (deeper out-of-the-box integration with other AWS services).

**Hinglish Analogy:** Kinesis Data Streams is like buying a brand-new AWS-designed delivery bike — simple, works great within the AWS city. MSK is like AWS agreeing to maintain YOUR existing Kafka-brand bike — same familiar vehicle, but someone else now handles the servicing.

#### Comparison Table — Kinesis Data Streams vs Amazon MSK

|Aspect|Kinesis Data Streams|Amazon MSK|
|---|---|---|
|Underlying tech|AWS-native streaming service|Managed **Apache Kafka** (open-source)|
|Best for|New AWS-native pipelines, simplicity|Teams already using/committed to Kafka|
|Ecosystem|AWS SDKs/integrations|Kafka APIs, Kafka Connect, existing Kafka tooling|
|Management|Fully managed, minimal config|Managed, but still Kafka-cluster-aware (brokers, topics)|

### ⚠️ Exam Trap

Don't assume MSK and Kinesis are freely interchangeable. AWS tests **recognition of Kafka** — if the scenario explicitly mentions "Apache Kafka" or "migrating an existing Kafka pipeline," the expected answer is **MSK**, not Kinesis.

★★★☆☆ Exam Importance: Good to Know

### Step 3 — Process

|Service|Role|
|---|---|
|**AWS Glue Data Catalog**|Centralized metadata repository — keeps track of _what_ data exists and _where_ (schema, location)|
|**AWS Glue**|Fully managed **ETL** service; visual, code-free job creation supported; uses the Data Catalog as reference|
|**Amazon EMR**|Large-scale big-data processing using open-source frameworks like Apache Spark/Hadoop — for companies with big-data expertise; more complex, more flexible/powerful|

**Hinglish Analogy — Glue vs EMR**

- **AWS Glue** = ek smart maid jo bina zyada instructions ke ghar clean-and-sort kar deti hai (managed, simple, low-code)
- **Amazon EMR** = ek poori construction crew jo apne tools khud leke aati hai for big, complex jobs (powerful, but you need expertise to run it)

### Step 4 — Analyze

|Service|Role|
|---|---|
|**Amazon Athena**|Serverless, **SQL queries directly on data sitting in S3** (or elsewhere) — no infra, pay only for queries run|
|**Amazon Redshift**|Managed data warehouse — complex, fine-grained SQL analytics on structured data at scale|

#### Comparison Table — Athena vs Redshift

|Aspect|Amazon Athena|Amazon Redshift|
|---|---|---|
|Infrastructure|Serverless, zero setup|Managed cluster (provisioned or serverless option)|
|Data location|Query data **in place** (e.g., directly in S3)|Data must be loaded INTO Redshift|
|Best for|Ad-hoc, occasional queries on data lake data|Frequent, complex, high-performance BI queries|
|Pricing|Pay per query (per TB scanned)|Pay for cluster/compute + storage|

### Step 5 — Visualize

|Service|Role|
|---|---|
|**Amazon QuickSight**|BI dashboards — interactive, scales to tens of thousands of users, for technical AND non-technical users|
|**Amazon OpenSearch Service**|Real-time search, monitoring, and analysis using keyword or NLP-style search over data|

### What AWS is REALLY testing (whole pipeline)

AWS isn't testing whether you can recite 10 service names. AWS is testing whether you can **map a business scenario to the correct stage of the pipeline** — e.g., "I need to run ad-hoc SQL on files sitting in S3 without provisioning anything" → Athena, not Redshift. "I need a fully managed real-time dashboard for live IoT sensor data" → Kinesis Data Streams (ingest) + QuickSight (visualize).

### Full Pipeline Decision Tree

```
Where is my data coming from / going?
   │
   ├── Need to STORE raw data?
   │      ├── Unstructured → S3 (Data Lake)
   │      └── Structured   → Redshift (Data Warehouse)
   │
   ├── Need to MOVE data in?
   │      ├── Real-time, multiple consumers → Kinesis Data Streams
   │      └── Simple, managed, batch delivery → Data Firehose
   │
   ├── Need to CLEAN/PREPARE data?
   │      ├── Simple, managed, low-code ETL → AWS Glue (+ Data Catalog)
   │      └── Massive big-data, Spark/Hadoop needs → Amazon EMR
   │
   ├── Need to QUERY/ANALYZE data?
   │      ├── Ad-hoc SQL on data in S3, no infra → Athena
   │      └── Heavy structured BI workloads → Redshift
   │
   └── Need to VISUALIZE data?
          ├── BI dashboards for business users → QuickSight
          └── Real-time keyword/NLP search & monitoring → OpenSearch
```

### Real AWS Scenario

An e-commerce company in India collects clickstream data from its app (raw, unstructured) → stores in **S3** (lake) → ingests live clicks via **Kinesis Data Streams** → cleans/catalogs with **AWS Glue** → runs ad-hoc SQL to check "which product page had the most drop-offs" via **Athena** → visualizes trends for the marketing team via **QuickSight**.

### 30-Second Revision — Data Pipeline

- **Definition:** Collect → Ingest → Process → Analyze → Visualize
- **Use case:** Turning raw business data into actionable insight
- **Alternative pairs:** S3/Redshift (collect), Kinesis/Firehose (ingest), Glue/EMR (process), Athena/Redshift (analyze), QuickSight/OpenSearch (visualize)
- **Pricing:** Mostly pay-as-you-go / serverless (Athena, Firehose, Glue) except Redshift/EMR clusters (provisioned compute)
- **Common Trap:** Mixing up which service belongs to which pipeline stage
- **Exam Importance:** ★★★★★

---

## MODULE END — QUICK REFERENCE

### Quick Summary Table — All Module 8 Services

|Category|Service|Function|
|---|---|---|
|AI Service|Amazon Polly|Text → Speech|
|AI Service|Amazon Transcribe|Speech → Text|
|AI Service|Amazon Translate|Language translation|
|AI Service|Amazon Comprehend|NLP / sentiment analysis|
|AI Service|Amazon Kendra|Enterprise search / Q&A|
|AI Service|Amazon Rekognition|Image/video object & activity recognition|
|AI Service|Amazon Textract|Extract text from documents|
|AI Service|Amazon Lex|Chatbots / voice assistants|
|AI Service|Amazon Personalize|Personalized recommendations|
|ML Service|Amazon SageMaker AI|Build/train/deploy custom models|
|ML Service|SageMaker JumpStart|Pre-trained models, few-click deploy|
|Gen AI|Amazon Bedrock|API access to foundation models|
|Gen AI|Amazon Q Developer|Coding assistant|
|Gen AI|Amazon Q Business|Business Q&A on internal data|
|Data Collect|Amazon S3|Data lake storage|
|Data Collect|Amazon Redshift|Data warehouse storage & analytics|
|Data Ingest|Kinesis Data Streams|Real-time ingestion|
|Data Ingest|Amazon Data Firehose|Near-real-time batch ingestion|
|Data Ingest|Amazon MSK|Managed Apache Kafka streaming|
|Data Acquisition|AWS Data Exchange|Subscribe to third-party datasets|
|Data Process|AWS Glue / Glue Data Catalog|Managed ETL + metadata catalog|
|Data Process|Amazon EMR|Big-data processing (Spark/Hadoop)|
|Data Analyze|Amazon Athena|Serverless SQL on S3 data|
|Data Visualize|Amazon QuickSight|BI dashboards|
|Data Visualize|Amazon OpenSearch|Real-time search & monitoring|

### Acronym Cheat Sheet

- **AI** — Artificial Intelligence
- **ML** — Machine Learning
- **DL** — Deep Learning
- **NLP** — Natural Language Processing
- **FM** — Foundation Model
- **ETL** — Extract, Transform, Load
- **ELT** — Extract, Load, Transform
- **EMR** — Elastic MapReduce
- **BI** — Business Intelligence

### Top 20 Revision Points

1. AI ⊃ ML ⊃ DL ⊃ Gen AI (each is a subset of the previous)
2. Gen AI runs on Foundation Models (FMs) — pre-trained, adaptable to many tasks
3. AWS AI/ML stack = AI Services → ML Services → ML Frameworks/Infra (top to bottom = less control, more speed)
4. Polly = Text→Speech; Transcribe = Speech→Text; Translate = Text→Text (different language)
5. Rekognition = images/video objects; Textract = text extraction FROM documents/images
6. Comprehend = analyzes text you give it; Kendra = lets users ASK questions, searches your docs
7. Lex = chatbot/voice interface builder (powers Alexa)
8. Personalize = recommendation engine from historical data
9. SageMaker AI = build your own model from scratch, fully managed infra
10. SageMaker JumpStart = pre-trained models, few-click deploy, then fine-tune
11. Amazon Bedrock = single API to access multiple third-party + Amazon FMs, fine-tune, serverless
12. Amazon Q Developer = coding help; Amazon Q Business = company-data Q&A assistant
13. Data Lake (raw, unstructured) → S3; Data Warehouse (structured) → Redshift
14. ETL = Extract→Transform→Load; ELT = Extract→Load→Transform
15. Pipeline order: Collect → Ingest → Process → Analyze → Visualize
16. Kinesis Data Streams = real-time, low latency, multi-consumer; Firehose = near-real-time, fully managed batch delivery
17. Amazon MSK = managed **Apache Kafka** — pick it when the scenario explicitly mentions Kafka or migrating an existing Kafka pipeline
18. AWS Data Exchange = marketplace to subscribe to **third-party/external** datasets — not for your own internal data
19. AWS Glue = managed, low-code ETL + Data Catalog (metadata); EMR = big-data frameworks (Spark/Hadoop), more complex/flexible
20. Athena = serverless SQL directly on S3 data, pay-per-query; Redshift = provisioned warehouse for heavy structured analytics
21. QuickSight = BI dashboards for business users; OpenSearch = real-time keyword/NLP search & monitoring
22. Whenever a scenario says "no infrastructure to manage" + "SQL on S3" → Athena is almost always the answer

### Common CCP Question Patterns

- "A company wants to convert customer service call recordings into text and then detect sentiment. Which two services?" → Transcribe + Comprehend
- "A company wants to extract data from scanned invoices and forms." → Textract
- "A company wants a chatbot answering employee questions using internal company documents." → Amazon Q Business (or Kendra if framed as "search")
- "A company wants to run ad-hoc SQL queries on data sitting in S3 without provisioning servers." → Athena
- "A company needs real-time ingestion of clickstream data with multiple downstream consumers." → Kinesis Data Streams
- "A company wants the simplest way to deliver streaming data into S3/Redshift with minimal management." → Amazon Data Firehose
- "A company wants to fine-tune and access multiple foundation models via one API." → Amazon Bedrock
- "A company already runs Apache Kafka on-premises and wants to move to AWS without rewriting their streaming pipeline." → Amazon MSK
- "A company wants to enrich its analytics with third-party weather/financial data instead of collecting it themselves." → AWS Data Exchange

### Final Decision Matrix

|If the scenario says...|Use...|
|---|---|
|"No ML expertise, just need a ready feature"|AI Services|
|"Custom model, have data scientists"|SageMaker AI|
|"Pre-trained model, quick deploy + fine-tune"|SageMaker JumpStart|
|"Chat with multiple foundation models via API"|Amazon Bedrock|
|"Company-data-aware business assistant"|Amazon Q Business|
|"Coding assistant"|Amazon Q Developer|
|"Store raw/unstructured data cheaply"|S3 (Data Lake)|
|"Store structured data for analytics"|Redshift (Data Warehouse)|
|"Real-time streaming, multiple consumers"|Kinesis Data Streams|
|"Simplest managed delivery to S3/Redshift"|Data Firehose|
|"Already using Apache Kafka / migrating a Kafka pipeline"|Amazon MSK|
|"Need external/third-party datasets (not our own data)"|AWS Data Exchange|
|"Low-code ETL + metadata catalog"|AWS Glue / Glue Data Catalog|
|"Big-data Spark/Hadoop processing"|Amazon EMR|
|"Serverless SQL directly on S3"|Athena|
|"Heavy structured BI SQL analytics"|Redshift|
|"Interactive BI dashboards"|QuickSight|
|"Real-time search/monitoring"|OpenSearch|

### Cross-links to Related Services (other modules)

- **S3** → covered in-depth in Module: Storage
- **Redshift** → also appears in Module: Databases (purpose-built DB discussion)
- **IAM/Security considerations** for all above services → covered in Security modules (least-privilege access to Bedrock/SageMaker/Glue resources)
- **EC2/compute underlying SageMaker/EMR** → Module: Compute

---
