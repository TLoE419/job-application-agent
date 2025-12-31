# Template-Based Resume Generation

## Overview

This system allows you to create a DOCX resume template with placeholders, then automatically fill it with customized CV data.

## How It Works

1. **Create your template** - Design your resume in Word with placeholders
2. **Agent generates YAML** - AI customizes your CV for specific jobs
3. **Fill template** - Automatically replace placeholders with CV data

## Template Placeholder Format

Use `{{FIELD_NAME}}` format in your Word template:

### Personal Info
- `{{Name}}` or `{{NAME}}` - Full name
- `{{LOCATION}}` - Current location
- `{{EMAIL}}` - Email address
- `{{PHONE}}` - Phone number
- `{{GITHUB}}` - GitHub profile
- `{{LINKEDIN}}` - LinkedIn profile

### Education (multiple entries)
- `{{EDU_1_SCHOOL}}` - First school name
- `{{EDU_1_LOCATION}}` - School location
- `{{EDU_1_DEGREE}}` - Degree name
- `{{EDU_1_DATE}}` - Study period
- `{{EDU_1_COURSES}}` - Relevant courses
- `{{EDU_2_SCHOOL}}`, etc. - Second entry

### Experience (multiple entries)
- `{{EXP_1_COMPANY}}` - Company name
- `{{EXP_1_LOCATION}}` - Location
- `{{EXP_1_TITLE}}` - Job title
- `{{EXP_1_DATE}}` - Employment period
- `{{EXP_1_ACHIEVEMENT_1}}` - First bullet point
- `{{EXP_1_ACHIEVEMENT_2}}` - Second bullet point
- `{{EXP_1_ACHIEVEMENT_3}}` - Third bullet point

### Skills
- `{{SKILL_LANGUAGE}}` - Programming languages
- `{{SKILL_FRAME_TOOL}}` - Frameworks and tools

### Projects (multiple entries)
- `{{PROJ_1_NAME}}` - Project name
- `{{PROJ_1_DATE}}` - Project date
- `{{PROJ_1_DESC_1}}` - First description
- `{{PROJ_1_DESC_2}}` - Second description
- `{{PROJ_1_DESC_3}}` - Third description

## Usage

### Full Workflow (CV Customization + DOCX Generation)

```bash
python src/main.py
```

This will:
1. Analyze job posting
2. Customize CV for the job
3. Generate YAML file
4. Generate DOCX resume from template

**Outputs:**
- `outputs/customized_cv.yaml` - Customized CV data
- `outputs/customized_cv.docx` - Final resume

### Manual DOCX Generation

If you already have a YAML file:

```bash
python src/docx_filler.py templates/template.docx outputs/customized_cv.yaml outputs/my_resume.docx
```

## Base CV Structure

Your `inputs/base_cv.yaml` should match your template placeholders:

```yaml
personal_info:
  name: "Your Name"
  location: "City, State"
  email: "you@email.com"
  phone: "(123) 456-7890"
  github: "github.com/username"
  linkedin: "linkedin.com/in/username"

education:
  - institution: "University Name"  # or use "school"
    location: "City, State"
    degree: "Master of Science in Computer Science"
    start_date: "Sep. 2023"
    end_date: "Dec. 2025"
    courses:
      - "Machine Learning"
      - "Algorithms"

experience:
  - company: "Company Name"
    location: "City, State"
    title: "Software Engineer"
    start_date: "Jan. 2023"
    end_date: "Present"
    achievements:
      - "Achievement 1"
      - "Achievement 2"
      - "Achievement 3"

skills:
  languages:
    - "Python"
    - "JavaScript"
  frameworks_and_tools:  # or use "frameworks_tools"
    - "Django"
    - "React"

projects:
  - name: "Project Name"
    date: "2024"
    descriptions:
      - "Description 1"
      - "Description 2"
      - "Description 3"
```

## Features Preserved

When filling the template, the system preserves:

✅ **All formatting** - Fonts, sizes, colors
✅ **Alignment** - Left, right, center, justify
✅ **Lists** - Bullet points and numbering
✅ **Styles** - Paragraph and character styles
✅ **Tables** - Table structure and layout

## Tips

1. **Design in Word first** - Create your ideal resume layout
2. **Replace with placeholders** - Swap actual content with `{{PLACEHOLDERS}}`
3. **Test filling** - Run manual DOCX generation to verify
4. **Keep formatting simple** - Complex formatting may not preserve perfectly

## Troubleshooting

### Placeholder not replaced
- Check spelling: `{{EDU_1_SCHOOL}}` not `{{EDU_1_SHCOOL}}`
- Ensure YAML has matching field
- Field names are case-sensitive

### Formatting lost
- Template may have complex formatting
- Try simplifying the template design
- Check if styles are applied at paragraph level

### Bullets disappeared
- Ensure template uses Word's built-in list styles
- Avoid manual bullet characters

## Example Workflow

1. Create `templates/template.docx` with your design
2. Replace content with placeholders
3. Run: `python src/main.py`
4. Review `outputs/customized_cv.docx`
5. Submit to job application!
