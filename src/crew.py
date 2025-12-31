"""
Main Crew orchestration for the Job CV Customization System.
This coordinates all agents and tasks.
"""

from crewai import Crew
from agents import job_analyzer_agent, cv_matcher_agent, cv_customizer_agent
from tasks import analyze_job_task, match_cv_task, customize_cv_task
import yaml
from pathlib import Path

class JobCVCrew:
    """Orchestrates the entire job CV customization workflow"""

    def __init__(self, cv_path: str = "inputs/base_cv.yaml", template_path: str = "templates/template.docx"):
        """
        Initialize the crew with a base CV and template

        Args:
            cv_path: Path to the base CV in YAML format
            template_path: Path to the DOCX template file
        """
        self.cv_path = cv_path
        self.template_path = template_path
        self.base_cv = self._load_cv()

        # Create the crew with all agents and tasks
        self.crew = Crew(
            agents=[job_analyzer_agent, cv_matcher_agent, cv_customizer_agent],
            tasks=[analyze_job_task, match_cv_task, customize_cv_task],
            verbose=True,
        )
    
    def _load_cv(self) -> dict:
        """Load and parse the base CV from YAML file"""
        try:
            with open(self.cv_path, 'r') as file:
                cv = yaml.safe_load(file)
            print(f"✓ Loaded base CV from {self.cv_path}")
            return cv
        except FileNotFoundError:
            print(f"✗ Error: CV file not found at {self.cv_path}")
            raise
        except yaml.YAMLError as e:
            print(f"✗ Error parsing YAML: {e}")
            raise
    
    def customize_cv_for_job(self, job_posting: str) -> str:
        """
        Main workflow: Takes a job posting and generates customized CV

        Args:
            job_posting: The job posting text to customize CV for

        Returns:
            The customized CV as a YAML string
        """
        print("\n" + "="*60)
        print("Starting CV Customization Workflow")
        print("="*60 + "\n")

        # Format CV as string for the agents
        cv_string = yaml.dump(self.base_cv, default_flow_style=False)

        # Execute the crew with the inputs
        inputs = {
            "job_posting": job_posting,
            "candidate_cv": cv_string,
            "original_cv": cv_string,
        }

        result = self.crew.kickoff(inputs=inputs)

        # Post-process to ensure pure YAML output
        cleaned_result = self._clean_yaml_output(str(result))

        return cleaned_result

    def _clean_yaml_output(self, output: str) -> str:
        """
        Clean the agent output to ensure it's pure YAML

        Args:
            output: The raw output from the agent

        Returns:
            Cleaned YAML string
        """
        
        # Remove markdown code blocks if present
        if "```yaml" in output:
            output = output.split("```yaml")[1].split("```")[0]
        elif "```" in output:
            output = output.split("```")[1].split("```")[0]

        # Remove common introductory phrases
        intro_phrases = [
            "Here is the customized CV:",
            "Here's the customized CV:",
            "Below is the customized CV:",
            "The customized CV is:",
            "Customized CV:",
        ]
        for phrase in intro_phrases:
            if phrase in output:
                output = output.split(phrase, 1)[1]

        # Strip whitespace
        output = output.strip()

        # Validate it's actual YAML
        try:
            yaml.safe_load(output)
            print("✓ YAML validation passed")
        except yaml.YAMLError as e:
            print(f"⚠ Warning: Generated content may not be valid YAML: {e}")

        return output
    
    def save_customized_cv(self, customized_cv: str, output_path: str = None) -> str:
        """
        Save the customized CV to a YAML file

        Args:
            customized_cv: The customized CV content
            output_path: Path to save the file (optional)

        Returns:
            Path to the saved file
        """
        if output_path is None:
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / "customized_cv.yaml"

        with open(output_path, 'w') as file:
            file.write(customized_cv)

        print(f"✓ Customized CV saved to {output_path}")
        return str(output_path)

    def generate_docx(self, yaml_cv_path: str, output_docx_path: str = None) -> str:
        """
        Generate DOCX resume from YAML CV using template

        Args:
            yaml_cv_path: Path to the YAML CV file
            output_docx_path: Path to save the DOCX file (optional)

        Returns:
            Path to the generated DOCX file
        """
        from docx_filler import DOCXFiller

        if output_docx_path is None:
            output_docx_path = yaml_cv_path.replace('.yaml', '.docx')

        print(f"\n📄 Generating DOCX resume from template...")

        # Load CV data
        with open(yaml_cv_path, 'r') as f:
            cv_data = yaml.safe_load(f)

        # Fill template
        result = DOCXFiller.fill_template(self.template_path, cv_data, output_docx_path)

        return result


# Example usage
if __name__ == "__main__":
    # Initialize the crew
    crew = JobCVCrew(cv_path="inputs/base_cv.yaml")
    
    # Example job posting (in real usage, this would be scraped from LinkedIn)
    example_job_posting = """
    Senior AI/ML Engineer
    Company: InnovateTech
    
    We're looking for a Senior AI/ML Engineer to join our growing team!
    
    Responsibilities:
    - Design and implement machine learning pipelines
    - Lead AI/ML initiative for our platform
    - Collaborate with data scientists and engineers
    - Mentor junior engineers on best practices
    - Optimize model performance and deployment
    
    Requirements:
    - 5+ years of experience with Python and machine learning
    - Strong knowledge of TensorFlow or PyTorch
    - Experience with AWS or GCP
    - Proven track record of shipping ML models to production
    - Excellent communication and leadership skills
    
    Nice to Have:
    - Experience with FastAPI or similar frameworks
    - Knowledge of Docker and Kubernetes
    - Open source contributions
    - Experience with distributed systems
    """
    
    # Run the customization workflow
    customized_cv = crew.customize_cv_for_job(example_job_posting)
    
    # Save the result
    crew.save_customized_cv(customized_cv)
    
    print("\n" + "="*60)
    print("✓ Workflow Complete!")
    print("="*60)
    