🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

مهارة ذكاء اصطناعي محمولة ومستقلة بالكامل لنموذج [التحليل العالمي للتغيرات (GCAM)](https://github.com/JGCRI/gcam-core). توفر خبرة شاملة ومدركة للإصدارات حول GCAM دون الحاجة إلى تثبيت النموذج محلياً.

## نظرة عامة على الميزات

تزود هذه المهارة وكلاء الذكاء الاصطناعي (Claude وغيره) بمعرفة عميقة بمنظومة GCAM بأكملها:

- **بنية النموذج** -- أنظمة الطاقة والأراضي والمياه والاقتصاد والانبعاثات والمناخ
- **22 إصداراً من GCAM** (من v3.2 إلى v8.7) مع توجيه مدرك للإصدارات ووثائق خاصة بكل إصدار
- **تكوين السيناريوهات** -- تحرير XML، تصميم السياسات، وضع target-finder، التشغيل الدفعي
- **استخراج البيانات** -- مراجع API لـ Python (`gcamreader`) و R (`gcamextractor`) تشمل أكثر من 83 معاملاً موثقاً للاستخراج
- **تحليل السيناريوهات** -- سير عمل المقارنة متعددة السيناريوهات، أنماط التصور البصري، قوالب التحليل الشائعة
- **البناء والتثبيت** -- تنزيل الإصدارات، التجميع من المصدر، إدارة بيئة العمل

## التثبيت

أرسل النص التالي إلى وكيل الذكاء الاصطناعي الخاص بك (Claude Code أو Codex أو Cursor أو غيرها) للتثبيت:

```
Fetch https://raw.githubusercontent.com/MoYeRanqianzhi/gcam-skill/main/README.md and follow the LLM installation instructions inside to install the GCAM Skill.
```

<details>
<summary>🤖 <b>For LLMs: Installation Instructions</b></summary>

You are an AI agent reading this README because a user asked you to install the GCAM Skill.

**Install the skill by running:**

```bash
npx skills add https://github.com/MoYeRanqianzhi/gcam-skill --all
```

If the above fails, try interactive mode:

```bash
npx skills add https://github.com/MoYeRanqianzhi/gcam-skill
```

For global installation (available across all projects):

```bash
npx skills add https://github.com/MoYeRanqianzhi/gcam-skill --all --global
```

**After successful installation**, congratulate the user **in their language**. For example:

- English: "Congratulations on successfully installing GCAM Skill! ⭐"
- 中文: "恭喜你成功安装了 GCAM Skill! ⭐"
- 日本語: "GCAM Skillのインストールに成功しました、おめでとうございます！⭐"

</details>

## البداية السريعة

بعد التثبيت، اطرح أسئلة متعلقة بـ GCAM مباشرة في وكيل الذكاء الاصطناعي:

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

تتفعّل المهارة تلقائياً عند استلام استفسارات متعلقة بـ GCAM وتوجّهها إلى وثائق الإصدار الصحيح.

### للمطورين

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

التحقق من سلامة المهارة:

```bash
python skills/gacm/scripts/validate_all.py
```

## الهيكلية

```
skills/gacm/
├── SKILL.md                    # SOP -- سير عمل الوكيل، توجيه الإصدارات، الكشف التدريجي
├── scripts/                    # 28 سكربت Python (2 وقت التشغيل، 3 مولّدات، 23 مدققاً)
│   ├── doc_search.py           # وقت التشغيل: البحث في المراجع المجمّعة حسب الإصدار/النمط
│   ├── version_catalog.py      # وقت التشغيل: سجل الإصدارات وبيانات عائلة الإصدارات
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # مجموعة التحقق الشاملة
└── reference/                  # 33 وثيقة موضوعية + 22 حزمة إصدار
    ├── overview.md             # بنية النموذج والمفاهيم الأساسية
    ├── energy_system.md        # الموارد، الكهرباء، الهيدروجين، CCS، الطلب
    ├── land_system.md          # AgLU، تداخل GLU، Moirai، محاسبة الكربون
    ├── water_system.md         # 235 حوضاً، تقنيات التبريد، ترابط الماء-الطاقة-الغذاء
    ├── economy.md              # GDP، KLEM، GCAM-macro، معايرة SAM
    ├── emissions_climate.md    # CO2/غير CO2، منحنيات MAC، Hector، GWP، IAMC
    ├── policies_scenarios.md   # ضريبة الكربون، RES، target finder، أمثلة XML
    ├── trade.md                # Armington، Heckscher-Ohlin، تخصيص السلع
    ├── scenario_analysis.md    # سير عمل المقارنة متعددة السيناريوهات بـ Python/R
    ├── gcamreader_api.md       # مرجع Python Query/Connection API
    ├── gcamextractor_api.md    # R readgcam() مع 83+ معاملاً، 14 مجموعة
    ├── ssp.md                  # سرديات SSP1-5، الافتراضات الكمية
    ├── gcam_usa.md             # التوسع دون الوطني لـ 51 ولاية
    ├── versions/               # 22 ملف توجيه إصدار (v3.2--v8.7)
    └── version_pages/          # 614 ملف Markdown لصفحات الإصدارات المجمّعة
```

### الكشف التدريجي (Progressive Disclosure)

تستخدم المهارة نظام تحميل من ثلاثة مستويات لتقليل استهلاك نافذة السياق:

| المستوى | المحتوى | وقت التحميل | تكلفة الرموز |
|---------|---------|-------------|-------------|
| **1** | `name` + `description` | دائماً | ~130 tokens |
| **2** | سير عمل SKILL.md | عند تفعيل المهارة | ~2,800 tokens |
| **3** | وثائق الموضوعات، السكربتات، صفحات الإصدارات | عند الطلب | غير محدود |

ثلاث **بوابات إيقاف تحميل** صريحة تمنع التراكم غير الضروري للسياق.

## التغطية

### أنظمة GCAM

| النظام | الموضوعات المغطاة |
|--------|-------------------|
| الطاقة | الموارد الأحفورية/المتجددة، الكهرباء (شرائح الحمل، التبريد)، الهيدروجين (12 تقنية)، CCS، التكرير، دمج المصادر المتقطعة |
| الأراضي | AgLU nested logit، GLU، معالجة Moirai الأولية، محاسبة الكربون، الطاقة الحيوية، الثروة الحيوانية، إدارة الغابات |
| المياه | 6 قطاعات طلب، 235 حوضاً، منافسة تقنيات التبريد، المياه الجوفية (Superwell)، تحلية المياه |
| الاقتصاد | GDP خارجي/داخلي، إنتاج KLEM CES، معايرة SAM، تغذية راجعة لسعر الكربون |
| الانبعاثات | أكثر من 30 نوعاً، منحنيات MAC، Hector v3.2.0 (التربة الصقيعية)، GWP AR4/AR5، أسواق GHG المرتبطة |
| السياسات | ضريبة/قيد الكربون، RES/CES، target finder (7 أنواع أهداف)، حماية الأراضي، تكديس السياسات المتعددة |
| التجارة | Heckscher-Ohlin، Armington (21 قطاعاً مع معاملات logit)، Fixed Trade، التجارة بين الولايات في GCAM-USA |

### واجهات أدوات API

| الأداة | التغطية |
|--------|---------|
| `gcamreader` (Python) | `Query`، `LocalDBConn`، `RemoteDBConn`، `runQuery`، `parse_batch_query`، أوضاع CLI |
| `gcamextractor` (R) | `readgcam()` 16 معاملاً، أكثر من 83 قيمة `paramsSelect` عبر 14 مجموعة، تخزين `.Proj` المؤقت، تجميع المناطق |
| `rgcam` (R) | ملخص مفاهيمي |
| ModelInterface | توليد XML لأوامر الدفعات بدون واجهة رسومية |

### دعم الإصدارات

22 إصداراً من **v3.2** إلى **v8.7**، منظمة حسب عائلة التوثيق:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1، خط أساس v8.2)
- `delta-only` (v7.2--v7.4، v8.0--v8.1، v8.3--v8.7)

## التحقق

تتضمن المهارة 22 مدققاً آلياً يغطي:

- امتثال عقود الوثائق (العبارات المطلوبة، الوعي بالإصدارات)
- سلامة حزم الصفحات وتطابق المحتوى
- نظافة نظام الملفات وقابلية النقل عبر المنصات
- محاذاة الكشف التدريجي
- تغطية العقود الدلالية (لكل وثيقة مدقق خاص بها)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## وثائق المشروع

الذاكرة الدائمة للمساهمين موجودة في `docs/`:

- `PROJECT.md` -- النطاق، القرارات، المهام المعلقة
- `DEVELOPMENT.md` -- دليل سير العمل، تصنيف السكربتات، بوابات التحقق
- `CHANGELOG.md` -- سجل المعالم
- `KNOWN_ISSUES.md` -- القيود المعروفة والديون التقنية

## الترخيص

[MIT](LICENSE)

## شكر وتقدير

تجمع هذه المهارة محتوى من منظومة GCAM مفتوحة المصدر:

- [GCAM](https://github.com/JGCRI/gcam-core) -- نموذج التحليل العالمي للتغيرات (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- وثائق GCAM الرسمية
- [gcamreader](https://github.com/JGCRI/gcamreader) -- واجهة استعلام Python
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- حزمة استخراج R
