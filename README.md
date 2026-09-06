> **این README به دو زبان فارسی و انگلیسی نوشته شده است. | This README is available in both Persian and English.**

# Persian Resume Analyzer

An AI-assisted system for analyzing and improving **Persian-language resumes**. The project combines PDF text extraction, text normalization, rule-based evaluation, LLM-based text repair, structured information extraction, resume analysis, and quality assessment in a modular Streamlit application.

The main goal is not simply to generate a score, but to build a multi-stage pipeline that turns an unstructured Persian resume PDF into structured information and actionable feedback.

---

## Overview

Persian resumes introduce several practical challenges for automated processing, especially when the source document is a PDF. Text extraction can introduce broken words, incorrect spacing, misplaced line breaks, and RTL/LTR ordering problems.

This project addresses those problems through a staged workflow:

```text
PDF Resume
    ↓
Text Extraction
    ↓
Text Cleaning / Normalization
    ↓
Rule-Based Pre-Check
    ↓
AI Text Repair
    ↓
Structured Resume Extraction
    ↓
┌───────────────────────────────┐
│ AI Resume Analysis            │
│ Resume Quality Assessment     │
└───────────────────────────────┘
    ↓
Actionable Feedback
```

The application is implemented as a modular Python project with separate services, prompts, utilities, and Streamlit views.

---

## Key Features

- 📄 Persian PDF resume text extraction
- 🧹 Text cleaning and normalization
- 🔎 Rule-based resume pre-check
- 📊 Structured resume information extraction
- ✨ AI-assisted repair of PDF extraction artifacts
- 🧠 LLM-based professional resume analysis
- 🔍 Dedicated resume quality assessment
- 🤖 ATS-oriented evaluation
- 💼 Technical career and recruiter-oriented analysis
- 🔗 Detection of professional profiles such as LinkedIn and GitHub
- 📈 Rule-based score breakdown across multiple resume dimensions
- 🔄 Modular LLM provider architecture
- 🛟 Automatic fallback from Gemini to OpenRouter for selected temporary service failures
- 🌐 Interactive Streamlit interface

---

## Analysis Pipeline

### 1. PDF Text Extraction

The uploaded PDF is processed page by page and its text is extracted before any analysis takes place.

The project uses **PyMuPDF** for this stage.

### 2. Text Cleaning and Normalization

Extracted Persian PDF text may contain character inconsistencies and formatting artifacts. The processing stage normalizes common Persian/Arabic character differences, digits, invisible characters, spaces, and selected PDF extraction errors.

The rule-based analyzer also contains targeted repairs for examples such as broken Persian section titles and words produced incorrectly by PDF extraction.

### 3. Rule-Based Pre-Check

Before sending the resume through the deeper AI stages, a deterministic rule-based analyzer performs an initial evaluation.

The current analyzer evaluates categories including:

- Contact information
- Professional links
- Resume structure
- Achievements
- Writing quality
- Content

It also produces:

- A rule-based score
- Category-level score breakdown
- Detected contact information
- Professional profile detection
- Structural analysis
- Achievement analysis
- Writing/content checks
- A list of issues with severity and suggestions

The rule-based layer is intentionally separate from the LLM analysis so that explicit, deterministic checks can be performed independently.

### 4. AI Text Repair

PDF extraction is not always reliable for Persian documents. Instead of immediately analyzing potentially corrupted text, the application can send the cleaned text to an LLM specifically for **text reconstruction**.

The repair stage is instructed to:

- Repair broken Persian words
- Fix unnecessary line breaks
- Normalize spacing where appropriate
- Repair obvious RTL/LTR extraction artifacts
- Preserve English technical terminology
- Preserve names, dates, numbers, organizations, and project names
- Preserve the original content
- Avoid adding, removing, summarizing, or professionally rewriting information

This stage is designed as **reconstruction**, not content enhancement.

### 5. Structured Resume Extraction

The repaired resume text is converted into structured JSON data.

The current schema includes:

```text
Personal Information
├── Name
├── Phone
├── Email
├── Location
├── Marital Status
└── Birth Date

Education
Work Experience

Skills
├── Programming Languages
├── Libraries / Frameworks
├── AI / ML Topics
└── Computer Skills

Languages
Certificates
Projects
```

The extraction prompt explicitly requires the model to use only information present in the resume and to return `null` for unavailable fields.

### 6. AI Resume Analysis

Once the resume has been structured, a separate analysis stage evaluates it from a professional perspective.

The current analysis considers:

- Professional profile quality
- Education relevance
- Work experience impact
- Technical skill positioning
- Project presentation
- Achievement measurement
- ATS optimization
- Readiness for technical roles

The analysis is instructed to distinguish existing information from missing information and to provide specific, actionable recommendations rather than generic advice.

### 7. Resume Quality Assessment

A separate quality-analysis pipeline evaluates the structured resume from three perspectives:

1. **ATS compatibility**
2. **Professional resume structure**
3. **Recruiter first impression**

It produces separate assessments for overall quality, ATS, structure, experience quality, technical profile, recruiter perspective, and priority improvements.

This separation allows the project to distinguish between **content analysis** and **resume quality/presentation analysis**.

---

## Rule-Based Analysis vs. LLM Analysis

One of the main design decisions in the project is keeping deterministic checks and semantic analysis as separate stages.

| Layer | Purpose |
|---|---|
| Rule-Based Analysis | Deterministic checks, structural signals, contact/profile detection, scoring, and explicit issues |
| Text Repair LLM | Reconstruction of corrupted PDF-extracted text without changing its meaning |
| Structured Extraction LLM | Conversion of resume text into a consistent JSON representation |
| Resume Analysis LLM | Deeper professional and career-oriented evaluation |
| Quality Analysis LLM | ATS, structure, recruiter perspective, and prioritized improvements |

This architecture makes each stage responsible for a specific task instead of asking a single prompt to perform the entire workflow.

---

## LLM Provider Architecture

The project uses a small provider abstraction through `services/llm_service.py`.

### Primary Provider: Gemini

Gemini is used as the primary LLM provider.

### Fallback Provider: OpenRouter

If Gemini fails because of selected temporary conditions such as quota exhaustion, rate limiting, or temporary service unavailability, the application attempts to use OpenRouter as a fallback provider.

Other errors are not silently redirected to another provider, which helps avoid hiding configuration or programming problems.

```text
                 ┌───────────────┐
                 │  LLM Request  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │    Gemini     │
                 │    Primary    │
                 └───────┬───────┘
                         │
                temporary failure?
                         ↓
                 ┌───────────────┐
                 │  OpenRouter   │
                 │    Fallback   │
                 └───────────────┘
```

---

## Project Architecture

The project separates application responsibilities into several modules:

```text
Persian-resume-analyzer/
│
├── assets/
│   └── fonts/
│
├── prompts/
│   ├── analysis_prompt.py
│   ├── quality_analysis_prompt.py
│   ├── repair_prompt.py
│   └── structured_resume_prompt.py
│
├── services/
│   ├── gemini_service.py
│   ├── llm_service.py
│   ├── openrouter_service.py
│   ├── resume_analyzer.py
│   ├── resume_quality_analyzer.py
│   ├── rule_based_analyzer.py
│   └── structured_extractor.py
│
├── utils/
│   ├── pdf_reader.py
│   └── text_cleaner.py
│
├── views/
│   ├── analysis_view.py
│   ├── precheck_view.py
│   ├── quality_view.py
│   └── structured_view.py
│
├── app.py
├── style.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Module Responsibilities

- **`app.py`** — Streamlit application flow and session-state management
- **`services/`** — AI providers and resume-analysis logic
- **`prompts/`** — Dedicated prompts for each LLM task
- **`utils/`** — PDF extraction and text-processing utilities
- **`views/`** — Presentation of pre-check, structured data, analysis, and quality results
- **`assets/`** — Project assets such as fonts

---

## Technologies

- **Python**
- **Streamlit**
- **PyMuPDF**
- **Regular Expressions (Regex)**
- **JSON**
- **Large Language Models (LLMs)**
- **Google Gemini**
- **OpenRouter**
- **Requests**

The repository also includes a pinned Python dependency environment in `requirements.txt`.

---

## Running the Application

### 1. Clone the repository

```bash
git clone https://github.com/sarahshakeri/Persian-resume-analyzer.git
cd Persian-resume-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it according to your operating system.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

The LLM services read their API keys from environment variables.

```text
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

Do not commit API keys or other secrets to the repository.

### 5. Run the application

```bash
streamlit run app.py
```

Then upload a Persian resume in PDF format and follow the analysis stages through the interface.

---

## Typical User Workflow

```text
Upload PDF
   ↓
Review extracted text
   ↓
Review cleaned text
   ↓
Run initial rule-based evaluation
   ↓
Repair extracted text with AI
   ↓
Extract structured resume information
   ↓
Run AI resume analysis
   ↓
Run quality assessment
   ↓
Review strengths, weaknesses,
quality findings, and recommendations
```

The application keeps the intermediate results in Streamlit session state so that the different stages can be displayed without losing previously generated results during the current session.

---

## Design Principles

### Preserve information

The extraction and repair prompts explicitly instruct the LLM not to invent missing resume information.

### Separate extraction from evaluation

The system first extracts structured information and only then evaluates it. This reduces the risk of mixing factual extraction with subjective analysis.

### Use deterministic checks where possible

Information that can be checked explicitly—such as the presence of contact information, professional links, or recognizable resume sections—is handled by the rule-based layer rather than relying entirely on an LLM.

### Make feedback actionable

The analysis prompts require explanations of why an issue matters and what practical improvement can be made.

### Keep AI providers replaceable

LLM access is centralized behind a service layer so that the rest of the application does not need to know how a specific provider is called.

---

## Current Scope and Limitations

This project is designed primarily for **Persian-language resumes provided as PDF documents**.

Because PDF extraction quality depends on the source document, the extracted text may sometimes contain artifacts that require reconstruction. The project addresses common cases through deterministic normalization and an optional LLM-based repair stage, but no PDF extraction pipeline can guarantee perfect reconstruction for every document layout.

LLM-generated analysis is also dependent on the information successfully extracted from the resume and on the availability and behavior of the selected model provider.

The project does not claim that an AI-generated score is an objective measure of a candidate's professional ability. Scores and recommendations should be treated as automated assistance rather than a replacement for human review.

---

## Future Improvements

Possible directions for further development include:

- More robust Persian PDF layout and reading-order reconstruction
- Expanded rule-based checks
- More comprehensive Persian NLP processing
- Additional LLM providers
- More structured evaluation metrics
- Automated testing with a curated set of Persian resumes
- Better visualization of analysis results
- Support for additional resume document formats

---

## Reference Architecture

The project follows a staged architecture rather than a single end-to-end prompt:

```text
                ┌────────────────────┐
                │   Streamlit UI     │
                └─────────┬──────────┘
                          │
                          ↓
                ┌────────────────────┐
                │   PDF Extraction   │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Text Normalization │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Rule-Based Checks  │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │    LLM Repair      │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Structured JSON    │
                └──────┬───────┬─────┘
                       │       │
              ┌────────┘       └────────┐
              ↓                         ↓
      ┌───────────────┐       ┌────────────────┐
      │ Resume        │       │ Quality        │
      │ Analysis      │       │ Assessment     │
      └───────┬───────┘       └───────┬────────┘
              └──────────┬────────────┘
                         ↓
                ┌────────────────────┐
                │ Actionable Results │
                └────────────────────┘
```

---

## فارسی

# تحلیل‌گر هوشمند رزومه فارسی

یک سیستم هوشمند برای **تحلیل، ارزیابی و بهبود رزومه‌های فارسی** که ترکیبی از استخراج متن PDF، پاک‌سازی و نرمال‌سازی متن، تحلیل مبتنی بر Rule، پردازش با مدل‌های زبانی بزرگ، استخراج اطلاعات ساختاریافته و ارزیابی کیفیت رزومه را در قالب یک برنامه Streamlit ارائه می‌دهد.

هدف پروژه فقط تولید یک امتیاز نیست؛ بلکه یک pipeline چندمرحله‌ای ساخته شده است که رزومه PDF و متن نامنظم آن را به اطلاعات ساختاریافته و در نهایت به تحلیل و پیشنهادهای قابل‌استفاده تبدیل می‌کند.

---

## قابلیت‌های اصلی

- 📄 استخراج متن رزومه فارسی از PDF
- 🧹 پاک‌سازی و نرمال‌سازی متن
- 🔎 ارزیابی اولیه مبتنی بر Rule
- 📊 استخراج اطلاعات ساختاریافته رزومه
- ✨ اصلاح خطاهای ناشی از استخراج PDF با کمک AI
- 🧠 تحلیل حرفه‌ای رزومه با LLM
- 🔍 ارزیابی اختصاصی کیفیت رزومه
- 🤖 بررسی جنبه‌های مرتبط با ATS
- 💼 تحلیل با تمرکز بر مسیرهای شغلی فنی و دیدگاه Recruiter
- 🔗 شناسایی اطلاعات تماس و لینک‌های حرفه‌ای مانند LinkedIn و GitHub
- 📈 امتیازدهی و breakdown مبتنی بر قواعد برای چند بخش رزومه
- 🔄 معماری ماژولار برای سرویس‌های LLM
- 🛟 استفاده از OpenRouter به‌عنوان fallback در برخی خطاهای موقت Gemini
- 🌐 رابط کاربری تعاملی با Streamlit

---

## روند کامل پردازش

```text
رزومه PDF
   ↓
استخراج متن
   ↓
پاک‌سازی و نرمال‌سازی
   ↓
ارزیابی اولیه مبتنی بر Rule
   ↓
اصلاح متن با AI
   ↓
استخراج اطلاعات ساختاریافته
   ↓
┌───────────────────────────────┐
│ تحلیل رزومه با AI             │
│ ارزیابی کیفیت رزومه           │
└───────────────────────────────┘
   ↓
تحلیل و پیشنهادهای قابل‌اقدام
```

### ۱. استخراج متن از PDF

فایل PDF صفحه‌به‌صفحه پردازش شده و متن آن استخراج می‌شود. این مرحله با استفاده از **PyMuPDF** انجام می‌شود.

### ۲. پاک‌سازی و نرمال‌سازی

به‌دلیل مشکلات رایج استخراج متن فارسی از PDF، سیستم برخی تفاوت‌های کاراکتری، ارقام فارسی و عربی، کاراکترهای نامرئی، فاصله‌ها و خطاهای مشخص استخراج را اصلاح می‌کند.

### ۳. ارزیابی اولیه مبتنی بر Rule

قبل از تحلیل عمیق‌تر، یک تحلیل‌گر deterministic رزومه را بررسی می‌کند. این بخش مواردی مانند اطلاعات تماس، لینک‌های حرفه‌ای، ساختار رزومه، دستاوردها، کیفیت نگارش و محتوا را بررسی کرده و امتیاز و فهرست مشکلات را تولید می‌کند.

### ۴. اصلاح متن با AI

هدف این مرحله **بازسازی متن استخراج‌شده** است، نه بازنویسی حرفه‌ای رزومه.

مدل برای اصلاح کلمات شکسته، line breakهای نامناسب، برخی مشکلات RTL/LTR و فاصله‌گذاری هدایت می‌شود و در عین حال موظف است اطلاعات اصلی، نام‌ها، تاریخ‌ها، اعداد، سازمان‌ها و اصطلاحات فنی را حفظ کند و اطلاعات جدیدی اضافه نکند.

### ۵. استخراج اطلاعات ساختاریافته

متن اصلاح‌شده به یک ساختار JSON تبدیل می‌شود که شامل اطلاعات شخصی، تحصیلات، سوابق کاری، مهارت‌ها، زبان‌ها، گواهینامه‌ها و پروژه‌هاست.

### ۶. تحلیل هوشمند رزومه

رزومه ساختاریافته از جنبه‌هایی مانند کیفیت پروفایل حرفه‌ای، ارتباط تحصیلات، تأثیر سوابق کاری، نحوه ارائه مهارت‌های فنی، کیفیت ارائه پروژه‌ها، دستاوردهای قابل‌اندازه‌گیری، ATS و آمادگی برای موقعیت‌های فنی بررسی می‌شود.

### ۷. ارزیابی کیفیت رزومه

این بخش به‌صورت جداگانه سه دیدگاه را بررسی می‌کند:

1. سازگاری با ATS
2. ساختار حرفه‌ای رزومه
3. برداشت اولیه Recruiter

همچنین برای مشکلات، دلیل اهمیت و پیشنهاد بهبود ارائه می‌شود و اولویت‌بندی بهبودها نیز در خروجی وجود دارد.

---

## تفاوت تحلیل Rule-Based و LLM

یکی از تصمیم‌های معماری مهم پروژه، جدا نگه‌داشتن بررسی‌های deterministic از تحلیل معنایی است.

| لایه | وظیفه |
|---|---|
| Rule-Based | بررسی‌های قطعی، ساختار، اطلاعات تماس، لینک‌ها، امتیازدهی و مشکلات مشخص |
| LLM Text Repair | بازسازی متن آسیب‌دیده ناشی از استخراج PDF |
| Structured Extraction | تبدیل متن به ساختار JSON مشخص |
| Resume Analysis | تحلیل حرفه‌ای و شغلی رزومه |
| Quality Analysis | بررسی ATS، ساختار، دیدگاه Recruiter و بهبودهای اولویت‌دار |

---

## معماری سرویس‌های LLM

Gemini سرویس اصلی پروژه است و OpenRouter در صورت بروز برخی خطاهای موقت مانند quota، rate limit یا unavailable بودن موقت سرویس به‌عنوان fallback استفاده می‌شود.

این منطق در یک لایه سرویس مرکزی قرار گرفته تا بخش‌های مختلف برنامه مستقیماً به پیاده‌سازی یک provider وابسته نباشند.

---

## ساختار پروژه

```text
Persian-resume-analyzer/
│
├── assets/
│   └── fonts/
│
├── prompts/
│   ├── analysis_prompt.py
│   ├── quality_analysis_prompt.py
│   ├── repair_prompt.py
│   └── structured_resume_prompt.py
│
├── services/
│   ├── gemini_service.py
│   ├── llm_service.py
│   ├── openrouter_service.py
│   ├── resume_analyzer.py
│   ├── resume_quality_analyzer.py
│   ├── rule_based_analyzer.py
│   └── structured_extractor.py
│
├── utils/
│   ├── pdf_reader.py
│   └── text_cleaner.py
│
├── views/
│   ├── analysis_view.py
│   ├── precheck_view.py
│   ├── quality_view.py
│   └── structured_view.py
│
├── app.py
├── style.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## اصول طراحی

### حفظ اطلاعات اصلی

Promptهای استخراج و اصلاح متن صراحتاً مدل را از ساختن اطلاعاتی که در رزومه وجود ندارند منع می‌کنند.

### جداسازی Extraction و Evaluation

ابتدا اطلاعات استخراج و ساختاریافته می‌شوند و سپس تحلیل انجام می‌شود. این جداسازی کمک می‌کند استخراج اطلاعات با قضاوت درباره کیفیت رزومه مخلوط نشود.

### استفاده از Rule در موارد قابل‌بررسی

مواردی که می‌توانند به‌صورت deterministic بررسی شوند، مانند وجود ایمیل، شماره تلفن، لینک LinkedIn یا GitHub و برخی بخش‌های رزومه، در لایه Rule-Based بررسی می‌شوند.

### خروجی قابل‌اقدام

تحلیل LLM فقط به بیان یک مشکل اکتفا نمی‌کند و promptها مدل را ملزم می‌کنند توضیح دهد مشکل چرا اهمیت دارد و چه اقدامی برای بهبود آن می‌توان انجام داد.

### معماری قابل توسعه

دسترسی به مدل‌های زبانی در لایه service قرار گرفته تا تغییر یا اضافه کردن providerهای دیگر، وابستگی بخش‌های اصلی برنامه به یک سرویس خاص را کاهش دهد.

---

## اجرا

```bash
git clone https://github.com/sarahshakeri/Persian-resume-analyzer.git
cd Persian-resume-analyzer
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

کلیدهای API موردنیاز از متغیرهای محیطی خوانده می‌شوند:

```text
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

کلیدهای API نباید در repository قرار بگیرند.

---

## محدودیت‌های فعلی

تمرکز اصلی پروژه روی **رزومه‌های فارسی در قالب PDF** است.

کیفیت استخراج متن به ساختار فایل PDF وابسته است و ممکن است در بعضی فایل‌ها خطاهای مربوط به layout، ترتیب خواندن یا ساختار متن ایجاد شود. پروژه برای برخی از این موارد از نرمال‌سازی و اصلاح متن با AI استفاده می‌کند، اما نمی‌توان بازسازی کامل همه انواع PDF را تضمین کرد.

همچنین تحلیل و امتیازدهی LLM به اطلاعات استخراج‌شده و رفتار و در دسترس بودن سرویس مدل وابسته است. امتیاز تولیدشده نباید به‌عنوان معیار عینی توانایی حرفه‌ای فرد در نظر گرفته شود و بهتر است به‌عنوان یک ابزار کمکی در کنار بررسی انسانی استفاده شود.

---

## مسیرهای توسعه آینده

- بهبود بازسازی layout و ترتیب خواندن PDFهای فارسی
- توسعه Ruleهای بیشتر برای ارزیابی رزومه
- پردازش پیشرفته‌تر NLP فارسی
- اضافه کردن providerهای بیشتر برای LLM
- تعریف معیارهای ارزیابی ساختاریافته‌تر
- ساخت مجموعه‌ای از رزومه‌های فارسی برای تست و ارزیابی سیستم
- بهبود visualization نتایج
- پشتیبانی از فرمت‌های بیشتر رزومه

---

## Author

**Sarah Shakeri**

GitHub: [@sarahshakeri](https://github.com/sarahshakeri)
