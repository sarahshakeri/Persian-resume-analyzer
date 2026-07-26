import re


# ============================================================

def normalize_resume_text(text):
    """
    Normalize common Persian PDF extraction problems while
    preserving the original line structure as much as possible.
    """

    # --------------------------------------------------------
    # Persian / Arabic digits
    # --------------------------------------------------------

    digit_translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789"
    )

    text = text.translate(digit_translation)


    # --------------------------------------------------------
    # Arabic characters -> Persian characters
    # --------------------------------------------------------

    char_translation = str.maketrans({
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "ۀ": "ه",
        "ة": "ه",
    })

    text = text.translate(char_translation)


    # --------------------------------------------------------
    # Invisible characters
    # --------------------------------------------------------

    text = text.replace("\u200c", " ")
    text = text.replace("\u200f", " ")
    text = text.replace("\u200e", " ")
    text = text.replace("\ufeff", " ")


    # --------------------------------------------------------
    # Normalize spaces
    # --------------------------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )


    # --------------------------------------------------------
    # Common Persian PDF extraction errors
    # --------------------------------------------------------

    extraction_fixes = {

        # سوابق کار ی -> سوابق کاری
        r"\bسوابق\s+کار\s+ی\b":
            "سوابق کاری",

        # سابقه کار ی -> سابقه کاری
        r"\bسابقه\s+کار\s+ی\b":
            "سابقه کاری",

        # مدارک رسم ی -> مدارک رسمی
        r"\bمدارک\s+رسم\s+ی\b":
            "مدارک رسمی",

        # پژوهش های -> پژوهش های
        r"\bپژوهش\s+های\b":
            "پژوهش های",

        # مهارت ها -> مهارت ها
        r"\bمهارت\s+ها\b":
            "مهارت ها",
    }

    for pattern, replacement in extraction_fixes.items():

        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE
        )


    # --------------------------------------------------------
    # Repair section titles split across two lines
    # Example from Persian PDF extraction:
    #
    # تحصیال
    # ت
    #
    # -> تحصیلات
    # --------------------------------------------------------

    text = re.sub(
        r"تحصیال\s*\n\s*ت",
        "تحصیلات",
        text
    )


    # --------------------------------------------------------
    # Remove excessive empty lines
    # --------------------------------------------------------

    text = re.sub(
        r"\n[ \t]*\n[ \t]*\n+",
        "\n\n",
        text
    )

    return text.strip()

# ============================================================
# Helper functions
# ============================================================

def contains_any(text, keywords):
    """
    Return True if any keyword exists in text.
    """
    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def count_keyword_occurrences(text, keywords):
    """
    Count occurrences of achievement/action keywords.

    Longer phrases are checked first and overlapping phrases
    are reduced to avoid excessive double counting.
    """

    count = 0
    working_text = text

    unique_keywords = sorted(
        set(keywords),
        key=len,
        reverse=True
    )

    for keyword in unique_keywords:

        pattern = re.escape(keyword.lower())

        matches = list(
            re.finditer(
                pattern,
                working_text,
                flags=re.IGNORECASE
            )
        )

        count += len(matches)

        if matches:
            working_text = re.sub(
                pattern,
                " ",
                working_text,
                flags=re.IGNORECASE
            )

    return count


def detect_section(text, keywords):
    """
    Detect resume sections using line-level and general-text matching.

    Line-level matching is preferred because resume section titles
    usually appear on separate lines.
    """

    lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip()
    ]

    normalized_keywords = [
        keyword.lower().strip()
        for keyword in keywords
    ]

    # --------------------------------------------------------
    # Strong detection: section-like lines
    # --------------------------------------------------------

    for line in lines:

        clean_line = re.sub(
            r"[:：\-–—|•▪●]+",
            " ",
            line
        )

        clean_line = re.sub(
            r"\s+",
            " ",
            clean_line
        ).strip()

        for keyword in normalized_keywords:

            if clean_line == keyword:
                return True

            # Section titles with small extra text
            if (
                keyword in clean_line
                and len(clean_line.split()) <= 6
            ):
                return True

    # --------------------------------------------------------
    # Fallback detection
    # Useful when PDF extraction destroys line structure
    # --------------------------------------------------------

    for keyword in normalized_keywords:

        if keyword in text:
            return True

    return False


# ============================================================
# Main analyzer
# ============================================================

def analyze_resume_rules(text):

    if not text or not text.strip():
        raise ValueError(
            "متن رزومه نمی‌تواند خالی باشد."
        )

    normalized_text = normalize_resume_text(text)
    lower_text = normalized_text.lower()

    result = {
        "rule_based_score": 0,
        "score_breakdown": {},
        "contact_information": {},
        "professional_links": {},
        "structure_analysis": {},
        "achievement_analysis": {},
        "writing_quality": {},
        "content_analysis": {},
        "issues": []
    }

    score_breakdown = {
        "contact": 0,
        "professional_links": 0,
        "structure": 0,
        "achievements": 0,
        "writing": 0,
        "content": 0
    }

    # ========================================================
    # 1. Contact information
    # Maximum score: 15
    # ========================================================

    email_pattern = (
        r"(?<![\w.+-])"
        r"[A-Za-z0-9._%+-]+"
        r"\s*@\s*"
        r"[A-Za-z0-9.-]+"
        r"\s*\.\s*"
        r"[A-Za-z]{2,}"
        r"(?![\w.-])"
    )

    phone_patterns = [
        # Iranian mobile number
        r"(?<!\d)"
        r"(?:\+98|0098|98|0)?"
        r"[\s\-()]*"
        r"9\d{2}"
        r"[\s\-()]*"
        r"\d{3}"
        r"[\s\-()]*"
        r"\d{4}"
        r"(?!\d)",

        # Generic international/mobile style fallback
        r"(?<!\d)"
        r"\+\d{1,3}"
        r"[\s\-()]?"
        r"\d{2,4}"
        r"[\s\-()]?"
        r"\d{3,4}"
        r"[\s\-()]?"
        r"\d{3,4}"
        r"(?!\d)"
    ]

    has_email = bool(
        re.search(
            email_pattern,
            normalized_text,
            flags=re.IGNORECASE
        )
    )

    has_phone = any(
        re.search(pattern, normalized_text)
        for pattern in phone_patterns
    )

    result["contact_information"] = {
        "email_found": has_email,
        "phone_found": has_phone
    }

    if has_email:
        score_breakdown["contact"] += 8

    else:
        result["issues"].append({
            "category": "Contact Information",
            "severity": "High",
            "issue":
                "آدرس ایمیل حرفه‌ای در رزومه شناسایی نشد.",
            "suggestion":
                "یک آدرس ایمیل حرفه‌ای و معتبر به اطلاعات تماس رزومه اضافه کنید."
        })

    if has_phone:
        score_breakdown["contact"] += 7

    else:
        result["issues"].append({
            "category": "Contact Information",
            "severity": "High",
            "issue":
                "شماره تلفن در رزومه شناسایی نشد.",
            "suggestion":
                "یک شماره تلفن معتبر به اطلاعات تماس رزومه اضافه کنید."
        })

    # ========================================================
    # 2. Professional links
    # Maximum score: 10
    # ========================================================

    linkedin_patterns = [
        r"linkedin\.com",
        r"www\.linkedin\.com",
        r"linkedin\s*:",
        r"linkedin"
    ]

    github_patterns = [
        r"github\.com",
        r"www\.github\.com",
        r"github\s*:",
        r"github"
    ]

    linkedin = any(
        re.search(
            pattern,
            lower_text,
            flags=re.IGNORECASE
        )
        for pattern in linkedin_patterns
    )

    github = any(
        re.search(
            pattern,
            lower_text,
            flags=re.IGNORECASE
        )
        for pattern in github_patterns
    )

    result["professional_links"] = {
        "linkedin_found": linkedin,
        "github_found": github
    }

    if linkedin:
        score_breakdown["professional_links"] += 5

    else:
        result["issues"].append({
            "category": "Professional Profile",
            "severity": "Low",
            "issue":
                "پروفایل LinkedIn در رزومه شناسایی نشد.",
            "suggestion": (
                "در صورت داشتن پروفایل حرفه‌ای، لینک LinkedIn خود را "
                "برای تکمیل حضور حرفه‌ای به رزومه اضافه کنید."
            )
        })

    if github:
        score_breakdown["professional_links"] += 5

    else:
        result["issues"].append({
            "category": "Technical Portfolio",
            "severity": "Medium",
            "issue":
                "لینک GitHub یا نمونه‌کار کدنویسی در رزومه شناسایی نشد.",
            "suggestion": (
                "برای موقعیت‌های AI یا Software، در صورت وجود پروژه‌های مرتبط، "
                "لینک مخازن GitHub خود را به رزومه اضافه کنید."
            )
        })

    # ========================================================
    # 3. Resume structure
    # Maximum score: 25
    # ========================================================

    sections = {

        "education": [
            "education",
            "academic background",
            "academic education",
            "تحصیلات",
            "سوابق تحصیلی",
            "سابقه تحصیلی",
            "مدارک تحصیلی",
            "آموزش",
            "دانشگاه"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "work history",
            "سوابق کاری",
            "سابقه کاری",
            "تجارب کاری",
            "تجربیات کاری",
            "تجربه کاری",
            "سوابق شغلی",
            "سابقه شغلی",
            "تجربه حرفه ای",
            "تجربیات حرفه ای"
        ],

        "skills": [
            "skills",
            "technical skills",
            "professional skills",
            "core skills",
            "competencies",
            "مهارت",
            "مهارت ها",
            "مهارتهای تخصصی",
            "مهارت های تخصصی",
            "مهارتهای فنی",
            "مهارت های فنی",
            "توانمندی ها",
            "توانایی ها"
        ],

        "projects": [
            "projects",
            "project",
            "academic projects",
            "personal projects",
            "selected projects",
            "پروژه",
            "پروژه ها",
            "پروژه های دانشگاهی",
            "پروژه های شخصی",
            "پروژه های منتخب",
            "پروژه های انجام شده",
            "پژوهش",
            "پژوهش های علمی",
            "پژوهش های علمی دانشگاهی",
            "فعالیت های پژوهشی",
            "تحقیقات",
            "research",
            "research projects",
            "research experience"

            
        ]
    }

    detected = {}

    for section, keywords in sections.items():

        detected[section] = detect_section(
            lower_text,
            keywords
        )

    result["structure_analysis"] = detected

    section_score = 25 / len(sections)

    section_names = {
        "education": "تحصیلات",
        "experience": "سوابق کاری",
        "skills": "مهارت‌ها",
        "projects": "پروژه‌ها"
    }

    for section, exists in detected.items():

        if exists:
            score_breakdown["structure"] += section_score

        else:
            section_name = section_names.get(
                section,
                section
            )

            result["issues"].append({
                "category": "Structure",
                "severity": "Medium",
                "issue":
                    f"بخش «{section_name}» در رزومه شناسایی نشد.",
                "suggestion": (
                    "برای بخش‌های اصلی رزومه از عنوان‌های واضح و استاندارد "
                    "استفاده کنید تا خوانایی و سازگاری با سیستم‌های ATS بهبود یابد."
                )
            })

    # ========================================================
    # 4. Achievement analysis
    # Maximum score: 20
    # ========================================================

    achievement_keywords = [

        # English
        "achieved",
        "improved",
        "developed",
        "designed",
        "implemented",
        "created",
        "managed",
        "trained",
        "built",
        "optimized",
        "analyzed",
        "led",
        "increased",
        "reduced",
        "launched",
        "delivered",
        "organized",
        "coordinated",
        "automated",
        "generated",
        "completed",
        "conducted",

        # Persian
        "طراحی",
        "طراحی کردم",
        "پیاده سازی",
        "پیاده کردم",
        "توسعه",
        "توسعه دادم",
        "ایجاد",
        "ساختم",
        "ساخت",
        "آموزش",
        "آموزش دادم",
        "تدریس",
        "بهبود",
        "بهبود دادم",
        "مدیریت",
        "مدیریت کردم",
        "تحلیل",
        "تحلیل کردم",
        "بهینه سازی",
        "افزایش",
        "کاهش",
        "راه اندازی",
        "اجرا",
        "اجرا کردم",
        "برنامه نویسی",
        "تولید",
        "تکمیل",
        "هدایت",
        "هماهنگی",
        "پژوهش",
        "تحقیق"
    ]

    action_count = count_keyword_occurrences(
        lower_text,
        achievement_keywords
    )

    # --------------------------------------------------------
    # Quantifiable achievements
    # --------------------------------------------------------

    achievement_context = [

        # English
        "student",
        "students",
        "accuracy",
        "score",
        "percentage",
        "percent",
        "users",
        "clients",
        "hours",
        "performance",
        "projects",
        "customers",
        "participants",
        "revenue",
        "time",
        "days",
        "months",
        "years",
        "increase",
        "decrease",
        "reduced",
        "improved",

        # Persian
        "درصد",
        "دانشجو",
        "دانش آموز",
        "فراگیر",
        "هنرجو",
        "نمره",
        "دقت",
        "ساعت",
        "تعداد",
        "کاربر",
        "عملکرد",
        "مشتری",
        "پروژه",
        "نفر",
        "شرکت کننده",
        "روز",
        "ماه",
        "سال",
        "افزایش",
        "کاهش",
        "بهبود",
        "صرفه جویی"
    ]

    achievement_numbers = 0

    number_matches = list(
        re.finditer(
            r"(?<!\d)"
            r"\d+(?:[.,]\d+)?"
            r"\s*(?:%|درصد)?"
            r"(?!\d)",
            normalized_text
        )
    )

    for match in number_matches:

        start = max(
            0,
            match.start() - 70
        )

        end = min(
            len(normalized_text),
            match.end() + 70
        )

        nearby_text = (
            normalized_text[start:end]
            .lower()
        )

        if contains_any(
            nearby_text,
            achievement_context
        ):
            achievement_numbers += 1

    # Avoid unrealistic inflation caused by repeated extraction
    achievement_numbers = min(
        achievement_numbers,
        10
    )

    # --------------------------------------------------------
    # Action verb score: max 8
    # --------------------------------------------------------

    if action_count >= 8:
        action_score = 8

    elif action_count >= 5:
        action_score = 6

    elif action_count >= 3:
        action_score = 4

    elif action_count >= 1:
        action_score = 2

    else:
        action_score = 0

    # --------------------------------------------------------
    # Measurable achievement score: max 12
    # --------------------------------------------------------

    if achievement_numbers >= 3:
        measurable_score = 12
        achievement_status = "Strong"

    elif achievement_numbers == 2:
        measurable_score = 9
        achievement_status = "Good"

    elif achievement_numbers == 1:
        measurable_score = 5
        achievement_status = "Moderate"

    else:
        measurable_score = 0
        achievement_status = "Weak"

    score_breakdown["achievements"] = (
        action_score + measurable_score
    )

    result["achievement_analysis"] = {
        "action_verbs_detected": action_count,
        "measurable_results_detected": achievement_numbers,
        "status": achievement_status
    }

    if action_count < 3:

        result["issues"].append({
            "category": "Writing Quality",
            "severity": "Low",
            "issue":
                "استفاده از افعال اثرگذار در رزومه محدود است.",
            "suggestion": (
                "برای توضیح سوابق کاری و نقش خود در پروژه‌ها، "
                "بیشتر از افعال فعال و نتیجه‌محور استفاده کنید."
            )
        })

    if achievement_numbers == 0:

        result["issues"].append({
            "category": "Achievements",
            "severity": "High",
            "issue":
                "دستاورد قابل‌اندازه‌گیری مشخصی در رزومه شناسایی نشد.",
            "suggestion": (
                "در صورت امکان، نتایج واقعی و قابل‌اندازه‌گیری مانند "
                "تعداد افراد آموزش‌دیده، درصد بهبود، میزان دقت، نتیجه پروژه "
                "یا زمان صرفه‌جویی‌شده را اضافه کنید."
            )
        })

    # ========================================================
    # 5. Writing quality / Bullet Points
    # Maximum score: 10
    # ========================================================

    bullet_patterns = [
        r"(?m)^\s*[-–—]\s+",
        r"(?m)^\s*[•▪●◦‣⁃]\s*",
        r"(?m)^\s*[✓✔]\s*",
        r"(?m)^\s*\*\s+"
    ]

    bullet_count = sum(
        len(
            re.findall(
                pattern,
                normalized_text
            )
        )
        for pattern in bullet_patterns
    )

    result["writing_quality"] = {
        "bullet_points": bullet_count
    }

    if bullet_count >= 8:
        score_breakdown["writing"] = 10

    elif bullet_count >= 5:
        score_breakdown["writing"] = 8

    elif bullet_count >= 3:
        score_breakdown["writing"] = 5

    elif bullet_count >= 1:
        score_breakdown["writing"] = 2

    else:
        score_breakdown["writing"] = 0

        result["issues"].append({
            "category": "Writing Quality",
            "severity": "Medium",
            "issue":
                "ساختار Bullet Point مناسبی در رزومه شناسایی نشد.",
            "suggestion": (
                "برای توضیح سوابق کاری، دستاوردها و پروژه‌ها از "
                "Bullet Pointهای کوتاه، واضح و خوانا استفاده کنید."
            )
        })

    # ========================================================
    # 6. Content completeness
    # Maximum score: 20
    # ========================================================

    words = re.findall(
        r"[A-Za-z]+(?:['’-][A-Za-z]+)*"
        r"|"
        r"[\u0600-\u06FF]+"
        r"|"
        r"\d+(?:[.,]\d+)?",
        normalized_text
    )

    word_count = len(words)

    result["content_analysis"] = {
        "word_count": word_count
    }

    if word_count >= 250:
        score_breakdown["content"] = 20

    elif word_count >= 180:
        score_breakdown["content"] = 17

    elif word_count >= 120:
        score_breakdown["content"] = 14

    elif word_count >= 80:
        score_breakdown["content"] = 10

    elif word_count >= 50:
        score_breakdown["content"] = 6

    else:
        score_breakdown["content"] = 3

    if word_count < 100:

        result["issues"].append({
            "category": "General",
            "severity": "Medium",
            "issue":
                "محتوای رزومه نسبتاً کوتاه به نظر می‌رسد.",
            "suggestion": (
                "بررسی کنید که آیا سوابق مرتبط، پروژه‌ها، مهارت‌ها "
                "یا دستاوردهای مهمی از رزومه حذف شده‌اند یا خیر."
            )
        })

    # ========================================================
    # Final score
    #
    # Contact             15
    # Professional links  10
    # Structure           25
    # Achievements        20
    # Writing             10
    # Content             20
    # -----------------------
    # Total              100
    # ========================================================

    final_score = round(
        sum(score_breakdown.values())
    )

    result["score_breakdown"] = {

        "contact_information": round(
            score_breakdown["contact"]
        ),

        "professional_links": round(
            score_breakdown["professional_links"]
        ),

        "resume_structure": round(
            score_breakdown["structure"]
        ),

        "achievement_quality": round(
            score_breakdown["achievements"]
        ),

        "writing_quality": round(
            score_breakdown["writing"]
        ),

        "content_completeness": round(
            score_breakdown["content"]
        )
    }

    result["rule_based_score"] = max(
        0,
        min(
            final_score,
            100
        )
    )

    return result