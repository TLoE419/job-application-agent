"""
Task definitions for the CV customization system.
Each task is assigned to an agent and defines the work to be done.
"""

from crewai import Task
from agents import job_analyzer_agent, cv_matcher_agent, cv_customizer_agent

# =====================================================
# TASK 1: Analyze Job Posting
# =====================================================
analyze_job_task = Task(
    description="""Analyze the following job posting and provide a comprehensive breakdown:
    
    {job_posting}
    
    Your analysis should include:
    1. Job title and company overview
    2. Core responsibilities and duties
    3. Required skills and qualifications
    4. Nice-to-have skills and experience
    5. Implicit requirements (culture, work style, etc.)
    6. Key keywords and phrases that appear frequently
    7. Seniority level and career expectations
    
    Format the output as structured data that can be easily compared with a CV.""",
    agent=job_analyzer_agent,
    expected_output="Comprehensive job analysis with structured requirements and skills breakdown",
)

# =====================================================
# TASK 2: Match CV with Job Requirements
# =====================================================
match_cv_task = Task(
    description="""Compare the candidate's CV with the job requirements and provide a detailed analysis:

    Candidate CV:
    {candidate_cv}

    Use the job analysis from the previous task to understand the requirements.

    Your analysis should include:
    1. Matching skills (what the candidate has that the job requires)
    2. Skill gaps (what the job requires that the candidate doesn't have)
    3. Experience alignment (relevant work experience)
    4. Opportunity areas (where to position strengths)
    5. Potential concerns or misalignments
    6. Overall fit assessment (high/medium/low fit)
    7. Specific recommendations for what to emphasize in the tailored CV

    Be strategic and practical in your assessment.""",
    agent=cv_matcher_agent,
    expected_output="Detailed matching analysis with specific recommendations for CV customization",
    context=[analyze_job_task],  # Use output from previous task
)

# =====================================================
# TASK 3: Generate Customized CV
# =====================================================
customize_cv_task = Task(
    description="""Create a customized YAML CV based on the original CV and the matching analysis:

    Original CV:
    {original_cv}

    Use the matching analysis from the previous task to guide your customization.

    CRITICAL CONSTRAINTS - YOU MUST FOLLOW THESE RULES:

    1. SKILLS INTEGRITY:
       - ONLY use skills, technologies, and tools that are ALREADY in the original CV
       - NEVER add new skills that don't exist in the original CV (e.g., if TensorFlow is not in original, DON'T add it)
       - You can REORDER skills to prioritize relevant ones, but CANNOT invent new ones
       - You can REMOVE less relevant skills, but CANNOT add fabricated ones

    2. TECHNICAL DETAIL PRESERVATION:
       - KEEP all technical details, specific technologies, and version numbers from original
       - DO NOT simplify or generalize technical descriptions
       - PRESERVE all project-specific technologies and implementation details
       - Maintain the depth and specificity of technical achievements

    3. OUTPUT FORMAT:
       - Output ONLY pure YAML content - NO explanatory text before or after
       - NO markdown code blocks (no ```yaml or ```)
       - NO introductory sentences like "Here is the customized CV:"
       - NO concluding remarks or explanations
       - Start directly with YAML (e.g., "personal_info:")
       - End with the last YAML field - nothing else

    4. CUSTOMIZATION APPROACH:
       - Reorganize CV sections to prioritize relevant experience
       - Rewrite bullet points to emphasize relevant achievements using EXISTING skills
       - Reorder skills to highlight those matching job requirements
       - Keep all information truthful and authentic
       - Maintain the same YAML structure as the original
       - Enhance impact and relevance WITHOUT fabricating new information

    Your output must be valid YAML that can be directly parsed by yaml.safe_load() without any preprocessing.""",
    agent=cv_customizer_agent,
    expected_output="Pure YAML content only - no explanatory text, starting with 'personal_info:' and ending with the last YAML field",
    context=[analyze_job_task, match_cv_task],  # Use outputs from previous tasks
)
