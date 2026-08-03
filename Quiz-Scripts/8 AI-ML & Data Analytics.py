#!/usr/bin/env python3
"""
AWS Certified Cloud Practitioner (CLF-C02)
MODULE 8 — AI/ML & Data Analytics — Practice MCQ Quiz

Exam-mode behavior:
  - No per-question feedback (correct/incorrect) is shown during the quiz.
  - Answers are recorded silently ("Answer recorded.") exactly like the real exam.
  - Full results (score, topic-wise breakdown, weak-topic flags, missed-question
    review) are only revealed after the entire quiz is submitted.
  - Final report is auto-exported to a text file.
"""

import random
import sys
import os
from collections import defaultdict
from datetime import datetime

MODULE_NAME = "8-AIML-DataAnalytics"

# ---------------------------------------------------------------------------
# QUESTIONS
# Each tuple: (topic, question_text, [options], correct_answer, explanation)
#   correct_answer -> single 0-based int for single-select
#   correct_answer -> list/tuple of 0-based ints for multi-select
# ---------------------------------------------------------------------------

QUESTIONS = [

    # ===================== 8.0 AI -> ML -> DL -> Gen AI =====================
    ("AI-ML-DL-GenAI Hierarchy",
     "Which statement correctly describes the relationship between AI, ML, and Deep Learning?",
     [
         "ML is a subset of Deep Learning, which is a subset of AI",
         "AI is a subset of ML, which is a subset of Deep Learning",
         "ML is a subset of AI, and Deep Learning is a subset of ML",
         "AI, ML, and Deep Learning are three separate, unrelated fields"
     ],
     2,
     "The correct nesting is AI ⊃ ML ⊃ DL ⊃ Gen AI — each concept is a more specialized subset of the one before it."),

    ("AI-ML-DL-GenAI Hierarchy",
     "What is the primary characteristic that distinguishes Generative AI from traditional Machine Learning?",
     [
         "Generative AI only works with numeric data",
         "Generative AI creates new content rather than just predicting or classifying based on patterns",
         "Generative AI does not require any training data",
         "Generative AI cannot be accessed through an API"
     ],
     1,
     "Traditional ML finds patterns to predict or classify, while Generative AI uses those learned patterns to produce brand-new text, images, audio, or code."),

    ("AI-ML-DL-GenAI Hierarchy",
     "What is a Foundation Model (FM)?",
     [
         "A small model trained only on a single company's private dataset",
         "A massive, pre-trained model trained on broad data that can be adapted to many downstream tasks",
         "A rule-based expert system with no training data",
         "A database schema used to store ML training data"
     ],
     1,
     "Foundation Models are large, pre-trained on broad datasets, and can be adapted (fine-tuned or prompted) for many different tasks without training from scratch."),

    ("AI-ML-DL-GenAI Hierarchy",
     "A Machine Learning model is best described as:",
     [
         "A fixed set of if-else rules written by a developer",
         "The output produced after training on data, used to make predictions on new/unseen data",
         "A type of database used only for storing structured data",
         "A hardware chip designed only for graphics rendering"
     ],
     1,
     "ML works by feeding large volumes of data into an algorithm that finds patterns, producing a model which is then applied to new, unseen data to predict or decide."),

    # ===================== 8.1 AWS AI/ML Stack =====================
    ("AWS AI-ML Stack",
     "A company has no in-house data scientists but wants to quickly add sentiment analysis to their app. Which layer of the AWS AI/ML stack should they use?",
     [
         "ML Frameworks & Infrastructure",
         "ML Services (SageMaker)",
         "AI Services",
         "Amazon EC2 with custom-installed libraries"
     ],
     2,
     "AI Services are pre-trained and ready to use with no ML expertise required, making them ideal when a company lacks data science skills but needs a fast, standard capability."),

    ("AWS AI-ML Stack",
     "Which statement about the three layers of the AWS AI/ML stack is correct?",
     [
         "The lower the layer, the less control and the less expertise required",
         "The higher the layer, the more customization and the more expertise required",
         "The lower the layer, the more control you get but the more expertise you need",
         "All three layers require the same level of ML expertise"
     ],
     2,
     "Moving down the stack (AI Services → ML Services → ML Frameworks/Infrastructure) trades ease-of-use for greater control, and requires progressively deeper ML expertise."),

    ("AWS AI-ML Stack",
     "A team of data scientists wants to build and train a completely custom fraud-detection model using their own proprietary data. Which layer fits best?",
     [
         "AI Services",
         "ML Services (Amazon SageMaker)",
         "Amazon Polly",
         "Amazon Kendra"
     ],
     1,
     "When a business need requires a custom model built from proprietary data rather than an off-the-shelf capability, SageMaker (ML Services layer) is the appropriate choice."),

    # ===================== 8.2 AI Services =====================
    ("AI Services",
     "Which AWS service converts text into lifelike speech?",
     ["Amazon Transcribe", "Amazon Polly", "Amazon Translate", "Amazon Lex"],
     1,
     "Amazon Polly performs Text-to-Speech conversion, turning written text into natural-sounding audio."),

    ("AI Services",
     "Which AWS service converts spoken audio into written text?",
     ["Amazon Polly", "Amazon Comprehend", "Amazon Transcribe", "Amazon Kendra"],
     2,
     "Amazon Transcribe performs Speech-to-Text conversion, the reverse direction of Polly."),

    ("AI Services",
     "A company has scanned invoices with tables and handwritten notes and needs to extract the data automatically. Which service should they use?",
     ["Amazon Rekognition", "Amazon Textract", "Amazon Comprehend", "Amazon Personalize"],
     1,
     "Amazon Textract is purpose-built to detect and extract typed and handwritten text, tables, and forms from documents, unlike Rekognition which analyzes objects/scenes in images and video."),

    ("AI Services",
     "Which service identifies objects, people, and activities within images and videos?",
     ["Amazon Textract", "Amazon Rekognition", "Amazon Kendra", "Amazon Lex"],
     1,
     "Amazon Rekognition analyzes visual content (images/video) for objects, faces, and activities, whereas Textract focuses specifically on extracting text."),

    ("AI Services",
     "EXAM TRAP: A scanned image contains a printed order form with a table of items. Which service is the CORRECT choice — Rekognition or Textract?",
     ["Amazon Rekognition, because it processes images", "Amazon Textract, because it extracts text/tables from documents", "Both work identically for this use case", "Amazon Comprehend, because it processes documents"],
     1,
     "Even though the input is an image, the goal is text/table extraction from a document — that is Textract's specific job, not Rekognition's (which handles object/scene recognition)."),

    ("AI Services",
     "Which service allows end users to ask natural-language questions and get answers by searching your enterprise document repository?",
     ["Amazon Comprehend", "Amazon Kendra", "Amazon Translate", "Amazon Polly"],
     1,
     "Amazon Kendra is an intelligent enterprise search service that answers natural-language questions by searching across your documents, unlike Comprehend which only analyzes text you feed it."),

    ("AI Services",
     "What is the key difference between Amazon Comprehend and Amazon Kendra?",
     [
         "Comprehend analyzes/extracts meaning from text you provide; Kendra lets users search and ask questions across a document repository",
         "Comprehend is a chatbot builder; Kendra is a translation service",
         "They are the same service with different names",
         "Kendra only works with audio, while Comprehend only works with images"
     ],
     0,
     "Comprehend performs NLP analysis (sentiment, key phrases, entities) on text you supply, while Kendra is a search/Q&A engine over your document repository."),

    ("AI Services",
     "Which service is used to build conversational chatbots and voice assistants, and also powers Amazon Alexa?",
     ["Amazon Lex", "Amazon Kendra", "Amazon Personalize", "Amazon Rekognition"],
     0,
     "Amazon Lex provides the conversational interface (speech and text) used to build chatbots and voice assistants, and is the same technology that powers Alexa."),

    ("AI Services",
     "A retail company wants to generate personalized product recommendations for each customer based on historical browsing and purchase data. Which service fits best?",
     ["Amazon Personalize", "Amazon Textract", "Amazon Translate", "Amazon Transcribe"],
     0,
     "Amazon Personalize builds real-time personalized recommendations using historical customer interaction data, similar to the technology behind Amazon.com's recommendation engine."),

    ("AI Services",
     "SCENARIO: A bank wants to automatically transcribe customer service calls and then flag calls where the customer sounded angry. Select the TWO services required.",
     ["Amazon Transcribe", "Amazon Rekognition", "Amazon Comprehend", "Amazon Polly"],
     [0, 2],
     "Amazon Transcribe converts the call audio into text, and Amazon Comprehend then performs sentiment analysis on that text to detect negative/angry sentiment."),

    ("AI Services",
     "Which of the following are AI Services that require NO ML expertise to use? (Select THREE)",
     ["Amazon Rekognition", "Amazon SageMaker AI", "Amazon Translate", "Amazon Polly", "AWS Glue"],
     [0, 2, 3],
     "Rekognition, Translate, and Polly are all pre-trained, plug-and-play AI Services; SageMaker requires ML expertise to build custom models, and Glue is an ETL tool, not an AI service."),

    # ===================== 8.3 ML Services =====================
    ("ML Services-SageMaker",
     "What is the primary purpose of Amazon SageMaker AI?",
     [
         "To provide pre-built, ready-to-use AI APIs with no customization",
         "To fully manage the infrastructure needed to build, train, and deploy custom ML models",
         "To act only as a data warehouse for structured data",
         "To translate text between languages"
     ],
     1,
     "SageMaker AI is a fully managed service that removes the burden of managing infrastructure so data scientists can build, train, and deploy their own custom ML models."),

    ("ML Services-SageMaker",
     "What does Amazon SageMaker JumpStart provide?",
     [
         "A completely from-scratch model-building environment only",
         "A hub of pre-trained, open-source ML solutions that can be deployed with a few clicks and then fine-tuned",
         "A marketplace for buying third-party datasets",
         "A managed Apache Kafka streaming cluster"
     ],
     1,
     "SageMaker JumpStart offers pre-trained, open-source models you can deploy quickly and optionally fine-tune, sitting between fully pre-built AI Services and building entirely from scratch."),

    ("ML Services-SageMaker",
     "A company wants a middle ground: they want a pre-trained model as a starting point but also want the ability to fine-tune it further. Which option fits best?",
     ["Amazon Polly", "SageMaker JumpStart", "AWS Glue", "Amazon Redshift"],
     1,
     "SageMaker JumpStart is designed exactly for this middle ground — pre-trained models you can deploy quickly and then customize further, unlike a fully pre-built AI Service."),

    ("ML Services-SageMaker",
     "When should a company AVOID using Amazon SageMaker and instead use a pre-built AI Service?",
     [
         "When they need full control over model architecture",
         "When an off-the-shelf AI Service (e.g., Rekognition, Comprehend) already solves the exact business problem",
         "When they have a team of expert data scientists",
         "When they need to train on petabytes of custom data"
     ],
     1,
     "Building a custom SageMaker model when a pre-built AI Service already solves the problem wastes both time and cost — always check if an AI Service fits first."),

    ("ML Services-SageMaker",
     "Which best describes the difference between SageMaker AI (from scratch) and SageMaker JumpStart?",
     [
         "SageMaker AI gives full control by building on empty infrastructure; JumpStart provides a semi-ready, pre-trained starting point",
         "They are identical services with different names",
         "JumpStart is only for image recognition tasks",
         "SageMaker AI cannot be used to deploy models, only train them"
     ],
     0,
     "SageMaker AI (from scratch) is like building a custom house from empty land — full control and effort — while JumpStart is like a semi-furnished apartment, offering a pre-trained head start."),

    # ===================== 8.4 ML Frameworks & Infrastructure =====================
    ("ML Frameworks-Infrastructure",
     "Which AWS layer provides raw compute, open-source frameworks like TensorFlow/PyTorch, and purpose-built ML chips such as Trainium and Inferentia?",
     ["AI Services", "ML Services", "ML Frameworks & Infrastructure", "Data Analytics"],
     2,
     "The ML Frameworks & Infrastructure layer is the foundational layer, offering raw compute, open-source frameworks, and custom AWS silicon for organizations with deep ML expertise."),

    ("ML Frameworks-Infrastructure",
     "Which organizations should typically use the ML Frameworks & Infrastructure layer?",
     [
         "Organizations with no ML experience needing a quick chatbot",
         "Organizations with deep in-house ML expertise needing maximum control and cost-efficiency at scale",
         "Small businesses needing only translation services",
         "Marketing teams building BI dashboards"
     ],
     1,
     "This lowest layer requires the deepest ML expertise and is reserved for organizations that need maximum control over frameworks and hardware at scale."),

    # ===================== 8.5 Generative AI Services =====================
    ("Gen AI Services",
     "What does Amazon Bedrock provide?",
     [
         "A fully managed data warehouse for structured analytics",
         "API access to foundation models from Amazon and leading third-party AI companies, without managing infrastructure",
         "A service to physically ship large datasets to AWS",
         "A managed Apache Kafka cluster"
     ],
     1,
     "Amazon Bedrock gives serverless API access to multiple foundation models (from Amazon and third parties such as Anthropic and Meta) so companies can experiment without managing GPU infrastructure."),

    ("Gen AI Services",
     "A company wants to fine-tune and integrate a foundation model into their app without managing any GPU infrastructure or negotiating with multiple vendors. Which service is the best fit?",
     ["Amazon Bedrock", "Amazon EMR", "AWS Glue", "Amazon MSK"],
     0,
     "Amazon Bedrock is designed exactly for this scenario — a single managed API to access, fine-tune, and integrate foundation models without provisioning infrastructure."),

    ("Gen AI Services",
     "What is the difference between Amazon Q Developer and Amazon Q Business?",
     [
         "Q Developer is for coding assistance; Q Business answers questions using a company's internal data",
         "Q Developer is a data warehouse; Q Business is a data lake",
         "They are identical products marketed differently",
         "Q Business is only for image recognition"
     ],
     0,
     "Amazon Q Developer focuses on coding recommendations and accelerating development, while Amazon Q Business acts as a general assistant that answers questions using a company's internal data repositories."),

    ("Gen AI Services",
     "EXAM TRAP: A company wants an AI assistant that answers employee questions using their internal company documents. Which is generally the BEST described fit — Amazon Q Business or Amazon Kendra?",
     [
         "Amazon Kendra, because it is a conversational assistant",
         "Amazon Q Business, because it is built as a conversational assistant over your company's internal data, while Kendra is primarily a search + Q&A engine",
         "Both are unrelated and neither fits",
         "Amazon Bedrock, because it trains models from scratch"
     ],
     1,
     "Amazon Q Business and Kendra are related but distinct — Q Business is framed as a conversational business assistant, while Kendra is an enterprise search/Q&A engine; AWS exam scenarios often test this distinction."),

    ("Gen AI Services",
     "Does Amazon Bedrock train foundation models from scratch?",
     [
         "Yes, Bedrock always trains new models from the ground up",
         "No, Bedrock provides access to existing foundation models for fine-tuning and integration, not ground-up training",
         "Bedrock only works with structured tabular data",
         "Bedrock is only used for image storage"
     ],
     1,
     "A common exam trap is assuming Bedrock trains models from scratch — it actually provides API access to already pre-trained foundation models that you can fine-tune or integrate."),

    ("Gen AI Services",
     "Which service would a software development team use to get AI-powered code recommendations and accelerate development?",
     ["Amazon Q Developer", "Amazon Q Business", "Amazon Kendra", "Amazon Personalize"],
     0,
     "Amazon Q Developer is the variant of Amazon Q specifically focused on coding-related assistance and accelerating software development."),

    ("Gen AI Services",
     "Which of the following best distinguishes AI Services from Amazon Bedrock?",
     [
         "AI Services provide pre-built, task-specific capabilities; Bedrock provides access to foundation models for broader Generative AI use cases",
         "AI Services and Bedrock are the exact same offering",
         "Bedrock is only for storage, while AI Services are only for compute",
         "AI Services require more ML expertise than Bedrock"
     ],
     0,
     "AI Services (like Polly or Rekognition) solve narrow, pre-defined tasks, while Bedrock provides access to general-purpose foundation models that power flexible Generative AI applications like chat and content generation."),

    ("Gen AI Services",
     "Select the TWO Generative AI-related AWS offerings from the list below.",
     ["Amazon Bedrock", "Amazon Redshift", "Amazon Q Developer", "Amazon EMR"],
     [0, 2],
     "Amazon Bedrock (foundation model access) and Amazon Q Developer (Gen AI coding assistant) are both Generative AI offerings, while Redshift and EMR belong to the data analytics side of AWS."),

    # ===================== 8.6 Data Lakes vs Warehouses / Data Exchange =====================
    ("Data Lakes vs Warehouses",
     "Which AWS service is most commonly used to build a Data Lake for raw, unstructured data?",
     ["Amazon Redshift", "Amazon S3", "Amazon RDS", "AWS Glue"],
     1,
     "Amazon S3 is the primary AWS service used as a Data Lake, storing vast amounts of raw or semi-structured data cheaply before it's structured for analysis."),

    ("Data Lakes vs Warehouses",
     "Which AWS service is the primary choice for a Data Warehouse holding structured, cleaned data for fast SQL analytics?",
     ["Amazon S3", "Amazon Redshift", "Amazon Kinesis", "AWS Data Exchange"],
     1,
     "Amazon Redshift is AWS's managed data warehouse service, built for fast, complex SQL analytics on structured, curated business data."),

    ("Data Lakes vs Warehouses",
     "EXAM TRAP: Which pairing is CORRECT?",
     [
         "Data Lake = Redshift, Data Warehouse = S3",
         "Data Lake = S3, Data Warehouse = Redshift",
         "Data Lake = Athena, Data Warehouse = Glue",
         "Data Lake = QuickSight, Data Warehouse = OpenSearch"
     ],
     1,
     "A classic exam trap swaps these two: S3 is the Data Lake for raw/unstructured storage, and Redshift is the Data Warehouse for structured, curated data."),

    ("Data Lakes vs Warehouses",
     "What is the purpose of AWS Data Exchange?",
     [
         "To let companies find, subscribe to, and use third-party datasets delivered directly into their AWS environment",
         "To store a company's own internal structured data",
         "To perform real-time ETL transformations",
         "To build BI dashboards for internal teams"
     ],
     0,
     "AWS Data Exchange acts as a marketplace connecting data providers with data consumers, letting companies subscribe to external third-party datasets instead of collecting that data themselves."),

    ("Data Lakes vs Warehouses",
     "A logistics company needs years of historical weather data for an ML model but has no way to collect it themselves. What should they use?",
     ["Amazon Redshift", "AWS Data Exchange", "Amazon Kinesis Data Streams", "AWS Glue"],
     1,
     "AWS Data Exchange is designed exactly for this situation — subscribing to ready-made third-party datasets (like historical weather data) instead of building a collection pipeline from scratch."),

    # ===================== 8.7 ETL vs ELT =====================
    ("ETL vs ELT",
     "What does the ETL process stand for, and in what order?",
     [
         "Extract, Load, Transform",
         "Extract, Transform, Load",
         "Transform, Extract, Load",
         "Load, Extract, Transform"
     ],
     1,
     "ETL stands for Extract, Transform, Load — data is pulled from sources, cleaned/converted into a usable format, and then loaded into the destination."),

    ("ETL vs ELT",
     "How does ELT differ from ETL?",
     [
         "ELT loads raw data first and transforms it later, often on-demand in a data lake",
         "ELT never transforms data at all",
         "ELT and ETL are exactly the same process",
         "ELT only applies to streaming data, never batch data"
     ],
     0,
     "ELT swaps the order of the last two steps — raw data is loaded first, then transformed later, which is common in modern data lake architectures."),

    ("ETL vs ELT",
     "Why might a modern data lake architecture favor ELT over ETL?",
     [
         "Because raw data can be stored cheaply and quickly first, with transformation happening later, on-demand, as needed",
         "Because ELT eliminates the need to ever extract data",
         "Because ELT requires no storage at all",
         "Because ELT is only compatible with relational databases"
     ],
     0,
     "ELT lets a data lake ingest raw data immediately and defer transformation until it's actually needed for a specific analysis, offering more flexibility than the rigid ETL approach."),

    # ===================== 8.8 Data Pipeline (Collect/Ingest/Process/Analyze/Visualize) =====================
    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "What are the five stages of the AWS data pipeline, in order?",
     [
         "Ingest → Collect → Process → Visualize → Analyze",
         "Collect → Ingest → Process → Analyze → Visualize",
         "Process → Collect → Analyze → Ingest → Visualize",
         "Collect → Analyze → Ingest → Process → Visualize"
     ],
     1,
     "The standard AWS data pipeline flow is Collect → Ingest → Process → Analyze → Visualize, turning raw data into actionable business insight."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which ingestion service is best for real-time data where MULTIPLE applications need to consume the same stream simultaneously?",
     ["Amazon Data Firehose", "Amazon Kinesis Data Streams", "AWS Glue", "Amazon Athena"],
     1,
     "Kinesis Data Streams supports low-latency, real-time ingestion where multiple consumer applications can read from the same stream at the same time."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which ingestion service automatically batches, compresses, and encrypts data before delivering it to a destination like S3 or Redshift, with no consumer application to manage?",
     ["Amazon Kinesis Data Streams", "Amazon Data Firehose", "Amazon MSK", "Amazon EMR"],
     1,
     "Amazon Data Firehose is fully managed and delivers data directly to a fixed destination with built-in batching, compression, and encryption — requiring the least management of the ingestion options."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "EXAM TRAP: Which ingestion service requires the LEAST amount of management from the user?",
     ["Amazon Kinesis Data Streams", "Amazon Data Firehose", "Amazon MSK", "Amazon EMR"],
     1,
     "Kinesis Data Streams requires you to build and manage a consumer application (and shards), while Firehose is fully managed and simply delivers data to its destination — a frequently tested distinction."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "A company already has an existing Apache Kafka-based streaming pipeline and wants to migrate to AWS without re-architecting it. Which service should they use?",
     ["Amazon Kinesis Data Streams", "Amazon MSK", "Amazon Data Firehose", "AWS Glue"],
     1,
     "Amazon MSK (Managed Streaming for Apache Kafka) lets teams keep using their existing Kafka tools and APIs while AWS manages the operational overhead of running Kafka clusters."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which service is a fully managed, low-code ETL service that also maintains a centralized metadata catalog of your data?",
     ["Amazon EMR", "AWS Glue", "Amazon Athena", "Amazon QuickSight"],
     1,
     "AWS Glue is a fully managed ETL service with visual, code-free job creation, and it uses the Glue Data Catalog to track metadata about what data exists and where."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which service is best suited for large-scale big-data processing using open-source frameworks like Apache Spark or Hadoop?",
     ["AWS Glue", "Amazon EMR", "Amazon Athena", "Amazon Kendra"],
     1,
     "Amazon EMR is designed for large-scale, complex big-data processing with frameworks like Spark and Hadoop, offering more power and flexibility than Glue but requiring more expertise."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "A company wants to run occasional, ad-hoc SQL queries directly on data sitting in S3 without provisioning any infrastructure. Which service fits best?",
     ["Amazon Redshift", "Amazon Athena", "Amazon EMR", "AWS Glue"],
     1,
     "Amazon Athena is serverless and lets you run SQL queries directly on data in place (e.g., in S3), paying only per query, with zero infrastructure setup."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which service is better suited for frequent, complex, high-performance BI queries on structured data loaded into a managed cluster?",
     ["Amazon Athena", "Amazon Redshift", "AWS Data Exchange", "Amazon OpenSearch"],
     1,
     "Amazon Redshift is a provisioned (or serverless-option) data warehouse built for frequent, complex, high-performance SQL analytics, unlike Athena which is meant for ad-hoc queries on data in place."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which service provides interactive BI dashboards that scale to tens of thousands of users, for both technical and non-technical audiences?",
     ["Amazon QuickSight", "Amazon OpenSearch Service", "Amazon Kendra", "AWS Glue"],
     0,
     "Amazon QuickSight is AWS's BI dashboard service, designed to scale to large numbers of users and serve both technical and business audiences."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "Which service is best for real-time keyword or NLP-style search and monitoring over data (e.g., log analytics)?",
     ["Amazon QuickSight", "Amazon OpenSearch Service", "Amazon Athena", "Amazon Redshift"],
     1,
     "Amazon OpenSearch Service is designed for real-time search, monitoring, and analysis using keyword or NLP-style search, commonly used for log and operational analytics."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "SCENARIO: An e-commerce company collects raw clickstream data from its app, needs it ingested in real time, cleaned and cataloged, then queried ad-hoc, then visualized for marketing. Select the THREE services that best match: ingest, process, and analyze stages.",
     ["Amazon Kinesis Data Streams", "AWS Glue", "Amazon Athena", "Amazon QuickSight", "Amazon Redshift"],
     [0, 1, 2],
     "Kinesis Data Streams handles real-time ingestion, AWS Glue handles cleaning/cataloging (process), and Athena handles ad-hoc SQL queries (analyze) directly on S3 data — QuickSight would be the visualize stage, not one of the three requested."),

    ("Data Pipeline-Ingest-Process-Analyze-Visualize",
     "A company needs a fully managed real-time dashboard for live IoT sensor data. Which combination of services best supports this end-to-end?",
     [
         "Amazon Redshift (ingest) + AWS Glue (visualize)",
         "Amazon Kinesis Data Streams (ingest) + Amazon QuickSight (visualize)",
         "Amazon Athena (ingest) + Amazon MSK (visualize)",
         "AWS Data Exchange (ingest) + Amazon EMR (visualize)"
     ],
     1,
     "Kinesis Data Streams provides real-time ingestion of IoT sensor data, and QuickSight provides the dashboard visualization layer — matching each service to its correct pipeline stage."),

]

# ---------------------------------------------------------------------------
# QUIZ ENGINE (reusable across modules — do not modify per-module)
# ---------------------------------------------------------------------------

def _normalize_correct(correct):
    """Return correct answer(s) as a set of ints, regardless of single/multi format."""
    if isinstance(correct, (list, tuple, set)):
        return set(correct)
    return {correct}


def shuffle_question(question_tuple):
    """Shuffle the options of a single question, remapping the correct answer index/indices."""
    topic, text, options, correct, explanation = question_tuple
    correct_set = _normalize_correct(correct)

    indices = list(range(len(options)))
    random.shuffle(indices)

    new_options = [options[i] for i in indices]
    # map old index -> new index
    old_to_new = {old_i: new_i for new_i, old_i in enumerate(indices)}
    new_correct = {old_to_new[i] for i in correct_set}

    if isinstance(correct, (list, tuple, set)):
        new_correct_out = sorted(new_correct)
    else:
        new_correct_out = next(iter(new_correct))

    return (topic, text, new_options, new_correct_out, explanation)


def ask_question(qnum, total, question_tuple):
    """Presents a single question, collects the user's answer, and returns it.
    Does NOT reveal correctness (exam-mode)."""
    topic, text, options, correct, explanation = question_tuple
    is_multi = isinstance(correct, (list, tuple))

    print(f"\nQuestion {qnum}/{total}  [{topic}]")
    print(text)
    if is_multi:
        n = len(_normalize_correct(correct))
        print(f"(Select {n} answers — enter the numbers separated by commas, e.g. 1,3)")
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")

    while True:
        raw = input("Your answer: ").strip()
        try:
            if is_multi:
                picks = [int(x.strip()) - 1 for x in raw.split(",") if x.strip() != ""]
                if len(picks) == 0 or any(p < 0 or p >= len(options) for p in picks):
                    raise ValueError
                selected = sorted(set(picks))
            else:
                pick = int(raw.strip()) - 1
                if pick < 0 or pick >= len(options):
                    raise ValueError
                selected = pick
            break
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {len(options)}"
                  + (" (comma-separated for multiple)." if is_multi else "."))

    print("Answer recorded.")
    return selected


def run_quiz():
    print("=" * 70)
    print(f" AWS CCP (CLF-C02) PRACTICE QUIZ — MODULE {MODULE_NAME}")
    print(" EXAM MODE: No feedback will be shown until the quiz is complete.")
    print("=" * 70)

    questions = list(QUESTIONS)
    random.shuffle(questions)
    questions = [shuffle_question(q) for q in questions]

    total = len(questions)
    results = []  # list of dicts: topic, question, options, selected, correct, explanation, is_correct

    for idx, q in enumerate(questions, start=1):
        topic, text, options, correct, explanation = q
        selected = ask_question(idx, total, q)

        correct_set = _normalize_correct(correct)
        selected_set = _normalize_correct(selected) if isinstance(selected, (list, tuple)) else {selected}
        is_correct = selected_set == correct_set

        results.append({
            "topic": topic,
            "question": text,
            "options": options,
            "selected": selected,
            "correct": correct,
            "explanation": explanation,
            "is_correct": is_correct,
        })

    print_results(results)


def _format_answer(options, answer):
    if isinstance(answer, (list, tuple)):
        return "; ".join(f"{i+1}. {options[i]}" for i in answer)
    return f"{answer + 1}. {options[answer]}"


def print_results(results):
    total = len(results)
    correct_count = sum(1 for r in results if r["is_correct"])
    pct = (correct_count / total * 100) if total else 0

    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for r in results:
        topic_stats[r["topic"]]["total"] += 1
        if r["is_correct"]:
            topic_stats[r["topic"]]["correct"] += 1

    lines = []
    lines.append("=" * 70)
    lines.append(" QUIZ RESULTS — MODULE 8: AI/ML & DATA ANALYTICS")
    lines.append("=" * 70)
    lines.append(f"Score: {correct_count}/{total} ({pct:.1f}%)")
    lines.append("")

    lines.append("Topic-wise Breakdown (weakest first):")
    lines.append("-" * 70)
    topic_pcts = []
    for topic, stats in topic_stats.items():
        t_pct = (stats["correct"] / stats["total"] * 100) if stats["total"] else 0
        topic_pcts.append((topic, stats["correct"], stats["total"], t_pct))
    topic_pcts.sort(key=lambda x: x[3])

    for topic, c, t, p in topic_pcts:
        lines.append(f"  {topic:<45} {c}/{t}  ({p:.1f}%)")

    lines.append("")
    weak_topics = [t for t in topic_pcts if t[3] < 70]
    if weak_topics:
        lines.append("⚠ WEAK TOPICS (< 70%) — Review these first:")
        lines.append("-" * 70)
        for topic, c, t, p in weak_topics:
            lines.append(f"  - {topic} ({p:.1f}%)")
    else:
        lines.append("✅ No weak topics — all topics scored 70% or above!")

    lines.append("")
    lines.append("Missed Questions Review:")
    lines.append("-" * 70)
    missed = [r for r in results if not r["is_correct"]]
    if not missed:
        lines.append("  None — perfect score! 🎉")
    else:
        for i, r in enumerate(missed, start=1):
            lines.append(f"\n  {i}. [{r['topic']}] {r['question']}")
            lines.append(f"     Your answer:    {_format_answer(r['options'], r['selected'])}")
            lines.append(f"     Correct answer: {_format_answer(r['options'], r['correct'])}")
            lines.append(f"     Explanation:    {r['explanation']}")

    lines.append("")
    lines.append("=" * 70)
    lines.append(f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)

    report = "\n".join(lines)
    print("\n" + report)

    export_path = f"{MODULE_NAME}-Results.txt"
    try:
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📄 Report exported to: {os.path.abspath(export_path)}")
    except OSError as e:
        print(f"\n⚠ Could not export report: {e}")


if __name__ == "__main__":
    try:
        run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted by user. Exiting.")
        sys.exit(0)
