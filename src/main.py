"""
Main entry point for the Job CV Customization System.
This demonstrates how to use the CrewAI-based system to customize CVs.
"""

import os
from dotenv import load_dotenv
from crew import JobCVCrew
from utils import JobPostingMocker, CVParser
from pathlib import Path


def setup_environment():
    """Load environment variables and verify API keys"""
    load_dotenv('config/.env')
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠ Warning: ANTHROPIC_API_KEY not set in .env file")
        print("Please set your API key to run the full crew")
    
    # Create output directory
    Path("outputs").mkdir(exist_ok=True)


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print(" Job CV Customization System - Proof of Concept")
    print("="*70 + "\n")
    
    # Setup
    setup_environment()
    
    # Initialize the crew with base CV and template
    print("1. Initializing Crew with base CV and template...")
    crew = JobCVCrew(cv_path="inputs/base_cv.yaml")
    
    
    # Get a sample job posting
    print("\n2. Loading sample job posting...")
    sample_postings = JobPostingMocker.get_sample_postings()
    
    # Choose which job posting to customize for
    job_key = "data_scientist"  # Can be changed to "backend_engineer" or "full_stack_engineer"
    job_posting = sample_postings[job_key]
    
    print(f"   Selected job: {job_key}")
    print(f"   Preview: {job_posting[:100]}...")
    
    # Run the customization workflow
    print("\n3. Starting CV customization workflow...")
    print("-" * 70)
    
    try:
        customized_cv = crew.customize_cv_for_job(job_posting)

        print("-" * 70)
        print("\n4. Saving customized CV...")
        yaml_path = crew.save_customized_cv(customized_cv)

        print("\n5. Generating DOCX resume...")
        docx_path = crew.generate_docx(yaml_path)

        print("\n" + "="*70)
        print(" ✓ Workflow Complete!")
        print("="*70)
        print(f"\nOutputs generated:")
        print(f"  YAML CV: {yaml_path}")
        print(f"  DOCX Resume: {docx_path}")
        print("\nNext steps:")
        print("- Review the customized CV")
        print("- Submit the DOCX resume to job applications")
        print("- Test with different job postings")
        
    except Exception as e:
        print(f"\n✗ Error during workflow: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify ANTHROPIC_API_KEY is set in .env")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Ensure base_cv.yaml exists in the inputs/ directory")
        print(f"4. Error details: {str(e)}")


def test_cv_loading():
    """Test basic CV loading functionality"""
    print("\n" + "="*70)
    print(" Testing CV Loading")
    print("="*70 + "\n")
    
    try:
        cv = CVParser.load_cv("inputs/base_cv.yaml")
        print("✓ Successfully loaded base CV")
        print(f"  Name: {cv['personal_info']['name']}")
        print(f"  Email: {cv['personal_info']['email']}")
        print(f"  Skills: {len(cv['skills'])} categories")
        print(f"  Experience: {len(cv['experience'])} positions")
        print(f"  Education: {len(cv['education'])} entries")
        return True
    except Exception as e:
        print(f"✗ Error loading CV: {e}")
        return False


def test_job_postings():
    """Test job posting mocking"""
    print("\n" + "="*70)
    print(" Testing Job Postings")
    print("="*70 + "\n")
    
    postings = JobPostingMocker.get_sample_postings()
    print(f"✓ Available sample postings: {len(postings)}")
    
    for key, posting in postings.items():
        print(f"\n  {key}:")
        print(f"    Length: {len(posting)} characters")
        print(f"    Preview: {posting.split(chr(10))[0]}")


if __name__ == "__main__":
    # Run tests first
    if not test_cv_loading():
        print("\n⚠ CV loading test failed. Please check inputs/base_cv.yaml")
    
    test_job_postings()
    
    # Then run main workflow
    print("\n")
    main()