"""
Enhanced Personalized Study Plan Generator using LangChain
with OpenRouter LLM Support - Simplified Version
"""
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import os
import json
import argparse
from datetime import datetime
import yaml
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='study_plan_generator.log'
)
logger = logging.getLogger(__name__)

# Initialize rich console for better CLI presentation
console = Console()

# Define an enhanced PromptTemplate for personalized study plans
personalized_study_plan_template = PromptTemplate(
    input_variables=[
        "student_name",
        "grade_level",
        "subjects",
        "academic_performance", 
        "learning_style",
        "extracurricular_activities",
        "goals",
        "challenges",
        "available_study_time",
        "upcoming_exams",
        "preferred_resources",
        "additional_info",
        "special_considerations"
    ],
    template="""
# EXPERT EDUCATIONAL CONSULTANT ROLE
You are a highly experienced educational consultant with expertise in curriculum design, educational psychology, and personalized learning. Your specialty is creating individualized study plans that maximize student potential through evidence-based learning strategies tailored to each student's unique profile.

# STUDENT PROFILE COMPREHENSIVE ANALYSIS
## Personal Information
- Name: {student_name}
- Grade Level: {grade_level}

## Academic Profile
- Subjects: {subjects}
- Current Academic Performance: {academic_performance}
- Primary Learning Style: {learning_style}

## Personal Context
- Extracurricular Activities & Commitments: {extracurricular_activities}
- Personal & Academic Goals: {goals}
- Learning Challenges & Obstacles: {challenges}
- Available Study Time Distribution: {available_study_time}
- Upcoming Assessments & Deadlines: {upcoming_exams}
- Preferred Learning Resources & Tools: {preferred_resources}
- Additional Contextual Information: {additional_info}
- Special Considerations or Accommodations: {special_considerations}

# COMPREHENSIVE STUDY PLAN DEVELOPMENT FRAMEWORK

## 1. Cognitive Profile Analysis
- Analyze the student's subject-specific cognitive strengths and areas for development
- Map learning style preferences to appropriate teaching and study methodologies
- Identify potential cognitive obstacles and corresponding compensatory strategies
- Connect learning preferences to specific study techniques for each subject

## 2. Time-Energy Management Assessment
- Calculate optimal study duration for different subjects based on difficulty and student energy patterns
- Create a balanced distribution of subjects that accounts for cognitive load
- Factor in extracurricular commitments when designing study blocks
- Incorporate research-based break intervals (e.g., Pomodoro technique, spaced repetition)
- Identify peak cognitive performance periods and match with challenging subjects

## 3. Subject-Specific Strategy Development
For each subject the student is studying:
- Design customized study approaches that align with both subject requirements and learning preferences
- Identify subject-specific resources that match their learning style and address knowledge gaps
- Create progressive difficulty sequences that build confidence while addressing weaknesses
- Develop subject connections to personal interests and goals to enhance intrinsic motivation
- Incorporate retrieval practice and application exercises tailored to the subject matter

## 4. Holistic Progress Framework
- Design a comprehensive tracking system with specific, measurable milestones
- Create balanced self-assessment tools for each subject area
- Incorporate metacognitive reflection prompts to develop learning awareness
- Establish adaptive feedback mechanisms to refine strategies as the student progresses
- Include both knowledge and skill development metrics appropriate to each subject

## 5. Challenge-Specific Intervention Design
- Develop targeted interventions for each identified learning challenge
- Create remediation sequences for specific knowledge or skill gaps
- Design anxiety management protocols for assessments if needed
- Incorporate confidence-building progression paths
- Include subject-specific memory and retention techniques

## 6. Exam Preparation Architecture
- Create subject-specific exam preparation timelines
- Design practice assessment sequences with increasing authenticity
- Develop customized review protocols based on learning style
- Incorporate stress management and performance optimization techniques
- Create pre-exam routines that maximize cognitive performance

## 7. Wellness Integration Framework
- Incorporate physical activity breaks that enhance cognitive function
- Design stress management techniques appropriate to the student's age and preferences
- Include sleep hygiene recommendations to optimize learning consolidation
- Develop sustainable study habits that prevent burnout
- Create reward systems aligned with student interests and goals

# FORMAT OF YOUR RESPONSE

## 1. Executive Summary
Provide a concise overview of the student's profile and the key strategic elements of their personalized study plan.

## 2. Comprehensive Student Analysis
Offer detailed insights into the student's learning profile, identifying specific strengths to leverage and challenges to address.

## 3. Weekly Master Schedule
Create a detailed hour-by-hour schedule that optimally distributes subjects, incorporates breaks, and accounts for extracurricular commitments. Include specific time blocks for each subject with clear objectives.

## 4. Subject-Specific Action Plans
For each subject, provide:
- Customized study methodologies aligned with learning style
- Specific resources with direct links or references where possible
- Targeted exercises addressing identified areas for improvement
- Content-specific memory techniques
- Real-world connections to enhance relevance and retention
- Progressive challenge sequence

## 5. Adaptive Progress Monitoring System
Detail specific metrics and tracking methods for each subject area, including:
- Weekly self-assessment protocols
- Milestone achievements with verification methods
- Adjustment triggers and responsive strategies
- Digital or physical tracking tools recommendation

## 6. Exam Success Strategies
For each upcoming exam, provide:
- Detailed preparation timeline with specific milestones
- Subject-specific review methodologies
- Practice assessment schedule with increasing complexity
- Performance optimization strategies for exam day
- Post-exam review protocol

## 7. Challenge Mitigation Strategies
Address each identified challenge with:
- Specific intervention techniques
- Progress indicators
- Alternative approaches if initial strategies prove ineffective
- Research-backed methodologies appropriate to the specific challenge

## 8. Wellbeing and Sustainability Framework
Provide practical strategies for:
- Maintaining motivation during difficult subjects
- Balancing academic demands with personal wellbeing
- Managing stress during high-pressure periods
- Ensuring physical wellbeing supports cognitive performance
- Creating sustainable study habits that prevent burnout

## 9. Implementation Guidance
Offer clear direction on:
- How to begin implementing the plan effectively
- Adapting the plan as needs and circumstances change
- Troubleshooting common obstacles
- When and how to seek additional support

## 10. Resource Appendix
Compile a comprehensive list of all recommended resources, tools, and materials organized by subject.

Your plan should be evidence-based, practical for implementation, and specifically tailored to {student_name}'s unique profile. Each recommendation should have a clear rationale connected to aspects of their learning profile and supported by educational best practices.
"""
)

def create_sample_student_profile():
    """Create a sample student profile with enhanced details to demonstrate the prompt template"""
    return {
        "student_name": "Alex Johnson",
        "grade_level": "11th Grade (High School Junior)",
        "subjects": "Advanced Placement (AP) Calculus AB, Honors Physics, AP English Literature, Modern World History, AP Computer Science A (Java)",
        "academic_performance": "AP Calculus AB (B+, strong in derivatives, struggles with integration techniques), Honors Physics (C+, understands theory but has difficulty with problem application), AP English Literature (A-, excels in analysis but needs improvement in timed writing), Modern World History (B, strong in memorization but weaker in connecting historical themes), AP Computer Science A (A, particularly strong in algorithms and data structures)",
        "learning_style": "Primary: Visual-spatial and kinesthetic learner who benefits from diagrams, color-coding, videos, and hands-on activities. Secondary: Moderate auditory processing with preference for discussion over lecture. Learns best through concrete examples before abstract concepts. Retention improves significantly when material connects to personal interests.",
        "extracurricular_activities": "Varsity basketball team (practice Monday, Wednesday, Friday 3:30-5:30 PM, games on alternate Tuesdays and Thursdays 4:00-7:00 PM), Coding Club (Thursdays 3:00-4:30 PM), Part-time job at the local tech store (Saturdays 9:00 AM-3:00 PM, Sundays 12:00-5:00 PM)",
        "goals": "Short-term: Improve Physics grade to at least a B before end of semester, achieve a score of at least 1350 on the upcoming SAT. Medium-term: Qualify for AP Physics next year, develop a competitive programming portfolio. Long-term: Gain admission to a top-50 computer science program, possibly with academic scholarship opportunities.",
        "challenges": "1) Difficulty connecting theoretical concepts in Physics to mathematical problem-solving. 2) Test anxiety, particularly in timed assessments, leading to careless errors in math-based subjects. 3) Time management struggles due to multiple commitments and occasional procrastination. 4) Inconsistent study habits with tendency to cram before deadlines rather than distribute practice. 5) Difficulty sustaining focus during long reading assignments.",
        "available_study_time": "Weekdays: Approximately 2-3 hours after school (6:00-9:00 PM) with highest energy/focus from 7:00-8:30 PM. Weekends: 4-5 hours on Saturday evenings (5:00-10:00 PM) and Sunday mornings (9:00 AM-12:00 PM). Can wake up 45 minutes earlier on critical study days. Most mentally alert in the early evening, experiences focus dips mid-afternoon.",
        "upcoming_exams": "SAT scheduled for March 12th (8 weeks from now), Physics midterm on February 3rd (3 weeks from now) covering mechanics and thermodynamics, Calculus project on integration applications due February 15th, AP practice exams beginning in April",
        "preferred_resources": "Interactive simulations and visual models for STEM subjects, video tutorials under 15 minutes, collaborative study groups for discussing concepts, practice problems with step-by-step solutions, spaced repetition software for memorization tasks, educational apps that gamify learning, prefers physical textbooks for deep reading but digital resources for practice and review",
        "additional_info": "Has access to school tutoring center (open Tuesday/Thursday after school). Parents willing to hire a subject tutor if needed. School provides access to online learning platforms including Khan Academy Pro and AP Classroom. Has diagnosed mild ADHD (primarily inattentive type) but prefers non-medication management strategies. History of success with Pomodoro technique when consistently applied.",
        "special_considerations": "Processes information more slowly than peers but with higher retention when given adequate time. Benefits from movement breaks during study sessions. Slight auditory processing delay means recorded lectures work better than live ones because they can be paused/replayed. Strong preference for visual organization systems."
    }

class StudyPlanGenerator:
    def __init__(self):
        self.config = self._load_config()
        self.console = Console()
        # Force OpenRouter configuration for this simplified version
        self.config["default_model"] = "gpt-4-turbo"
        self.config["openrouter_api_base"] = "https://openrouter.ai/api/v1"
    
    def _load_config(self):
        """Load configuration from config file if exists, otherwise use defaults"""
        config_path = Path("config.yaml")
        default_config = {
            "default_model": "gpt-4-turbo",
            "temperature": 0.7,
            "output_dir": "study_plans",
            "openrouter_api_base": "https://openrouter.ai/api/v1"
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return default_config
        else:
            # Create default config file
            try:
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    yaml.dump(default_config, f)
            except Exception as e:
                logger.error(f"Error creating config file: {e}")
            
            return default_config
    
    def _setup_llm(self, api_key, model=None, temperature=None):
        """Set up the language model for OpenRouter"""
        if temperature is None:
            temperature = self.config.get("temperature", 0.7)
            
        if not model:
            model = self.config.get("default_model", "gpt-4-turbo")
            
        return ChatOpenAI(
            api_key=api_key,
            base_url=self.config.get("openrouter_api_base", "https://openrouter.ai/api/v1"),
            model=model,
            temperature=temperature,
            default_headers={
                "HTTP-Referer": "https://study-plan-generator.app",
                "X-Title": "Personalized Study Plan Generator"
            }
        )
    
    def display_available_models(self):
        """Display available models on OpenRouter"""
        table = Table(title="Available Models on OpenRouter")
        table.add_column("Number", justify="right", style="cyan")
        table.add_column("Model", style="green")
        table.add_column("Provider", style="yellow")
        table.add_column("Description", style="magenta")
        
        models = [
            ("1", "gpt-3.5-turbo", "OpenAI", "Balanced performance and cost"),
            ("2", "gpt-4-turbo", "OpenAI", "Advanced reasoning capabilities"),
            ("3", "claude-3-haiku", "Anthropic", "Fast and efficient assistant"),
            ("4", "claude-3-sonnet", "Anthropic", "Strong reasoning and helpfulness"),
            ("5", "gemini-pro", "Google", "Strong at multilingual content"),
            ("6", "mistral-large", "Mistral AI", "Excellent open model performance"),
            ("7", "llama-2-70b-chat", "Meta", "Powerful open source model"),
            ("8", "mixtral-8x7b", "Mistral AI", "Excellent for diverse tasks"),
            ("9", "phi-2", "Microsoft", "Lightweight model with good performance")
        ]
        
        for model in models:
            table.add_row(*model)
                
        console.print(table)
    
    def get_model_selection(self):
        """Get model selection from user for OpenRouter"""
        self.display_available_models()
        
        model_choice = console.input("[bold yellow]Select a model (enter number or full model name, default: 2 for gpt-4-turbo): [/bold yellow]")
        
        # Map model choices
        models_map = {
            "1": "gpt-3.5-turbo",
            "2": "gpt-4-turbo",
            "3": "claude-3-haiku",
            "4": "claude-3-sonnet",
            "5": "gemini-pro",
            "6": "mistral-large",
            "7": "llama-2-70b-chat",
            "8": "mixtral-8x7b",
            "9": "phi-2",
            "": "gpt-4-turbo"  # Default if empty
        }
        return models_map.get(model_choice, model_choice)
    
    def get_api_key(self):
        """Get OpenRouter API key"""
        env_var_key = "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"
        if os.environ.get(env_var_key):
            api_key = os.environ.get(env_var_key)
            console.print("[bold green]Using OpenRouter API key from environment variable[/bold green]")
            return api_key
            
        # For this specific implementation, use the provided key
        api_key = "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"
        console.print("[bold green]Using provided OpenRouter API key[/bold green]")
        return api_key
    
    def collect_student_info(self):
        """Collect student information through interactive prompts or use sample"""
        use_sample = console.input("[bold yellow]Would you like to use a sample student profile? (y/n, default: y): [/bold yellow]").lower()
        
        if use_sample.strip() == '' or use_sample == 'y':
            profile = create_sample_student_profile()
            console.print("\n[bold green]Using sample student profile:[/bold green]")
            
            # Display sample profile in a nice format
            for key, value in profile.items():
                formatted_key = key.replace('_', ' ').title()
                console.print(f"[bold cyan]{formatted_key}:[/bold cyan] {value}")
                
            return profile
        
        console.print("\n[bold green]Please enter the student profile information:[/bold green]")
        
        profile = {
            "student_name": console.input("[bold cyan]Student Name: [/bold cyan]"),
            "grade_level": console.input("[bold cyan]Grade Level: [/bold cyan]"),
            "subjects": console.input("[bold cyan]Subjects (include details about each): [/bold cyan]"),
            "academic_performance": console.input("[bold cyan]Academic Performance (include strengths/weaknesses): [/bold cyan]"),
            "learning_style": console.input("[bold cyan]Learning Style (visual, auditory, kinesthetic, etc.): [/bold cyan]"),
            "extracurricular_activities": console.input("[bold cyan]Extracurricular Activities (include schedules): [/bold cyan]"),
            "goals": console.input("[bold cyan]Short and Long-term Goals: [/bold cyan]"),
            "challenges": console.input("[bold cyan]Specific Challenges: [/bold cyan]"),
            "available_study_time": console.input("[bold cyan]Available Study Time (daily/weekly patterns): [/bold cyan]"),
            "upcoming_exams": console.input("[bold cyan]Upcoming Exams and Deadlines: [/bold cyan]"),
            "preferred_resources": console.input("[bold cyan]Preferred Learning Resources: [/bold cyan]"),
            "additional_info": console.input("[bold cyan]Additional Information (optional): [/bold cyan]"),
            "special_considerations": console.input("[bold cyan]Special Considerations (disabilities, accommodations, etc.): [/bold cyan]")
        }
        
        return profile

    def generate_study_plan(self, api_key, model=None, student_profile=None, temperature=0.7):
        """Generate a personalized study plan using the defined PromptTemplate"""
        if not student_profile:
            student_profile = create_sample_student_profile()
        
        # Set up the language model
        llm = self._setup_llm(api_key, model, temperature)
        
        # Create the chain with our prompt template
        with console.status("[bold green]Generating personalized study plan...[/bold green]"):
            study_plan_chain = LLMChain(
                llm=llm,
                prompt=personalized_study_plan_template
            )
            
            # Run the chain to generate the study plan
            study_plan = study_plan_chain.invoke(student_profile)
        
        return study_plan

    def visualize_study_schedule(self, plan_text):
        """Create a simple visualization of the weekly study schedule"""
        try:
            # This is a simple placeholder for visualization
            # In a real implementation, you would parse the study plan to extract the schedule
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            hours = list(range(6, 23))  # 6 AM to 10 PM
            
            # Create a random schedule for demonstration
            np.random.seed(42)  # For reproducibility
            schedule = np.zeros((len(days), len(hours)))
            subjects = ['Math', 'Physics', 'English', 'History', 'CS', 'Break', 'Extracurricular']
            subject_colors = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF', '#CCCCCC', '#99FFFF']
            
            # Randomly assign subjects to time slots
            for i in range(len(days)):
                for j in range(len(hours)):
                    if np.random.random() > 0.7:  # 30% chance of having a scheduled activity
                        schedule[i, j] = np.random.randint(1, len(subjects) + 1)
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(12, 8))
            im = ax.imshow(schedule, cmap='tab10', aspect='auto', vmin=0, vmax=len(subjects))
            
            # Set labels
            ax.set_xticks(np.arange(len(hours)))
            ax.set_yticks(np.arange(len(days)))
            ax.set_xticklabels([f"{h}:00" for h in hours])
            ax.set_yticklabels(days)
            
            # Rotate the tick labels and set their alignment
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
            
            # Create legend
            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor=subject_colors[i], label=subjects[i]) 
                              for i in range(len(subjects))]
            ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Add title and adjust layout
            ax.set_title("Weekly Study Schedule")
            fig.tight_layout()
            
            # Save the figure
            os.makedirs('visualizations', exist_ok=True)
            plt.savefig('visualizations/study_schedule.png')
            plt.close()
            
            return 'visualizations/study_schedule.png'
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return None

    def save_study_plan(self, student_name, study_plan, format_type="txt"):
        """Save the generated study plan to a file"""
        # Create directory if it doesn't exist
        output_dir = self.config.get("output_dir", "study_plans")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename based on student name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join([c if c.isalnum() else "_" for c in student_name])
        filename = f"{output_dir}/{safe_name}_study_plan_{timestamp}.{format_type}"
        
        with open(filename, "w") as f:
          if isinstance(study_plan, dict):
            f.write(json.dumps(study_plan, indent=4))
          else:
            f.write(str(study_plan))
        
        console.print(f"[bold green]Study plan saved to {filename}[/bold green]")
        return filename

    def run(self):
        """Run the study plan generator"""
        console.print(Panel.fit(
            "[bold cyan]Personalized Study Plan Generator[/bold cyan]\n"
            "Using LangChain with OpenRouter",
            title="Welcome",
            border_style="green"
        ))
        
        # Get API key (uses the provided one)
        api_key = self.get_api_key()
        
        # Get model selection
        model = self.get_model_selection()
        
        # Get temperature setting
        temp_input = console.input("[bold yellow]Enter temperature setting (0.0-1.0, default: 0.7): [/bold yellow]")
        try:
            temperature = float(temp_input) if temp_input else 0.7
            if not 0 <= temperature <= 1:
                console.print("[bold red]Invalid temperature value. Using default 0.7.[/bold red]")
                temperature = 0.7
        except ValueError:
            console.print("[bold red]Invalid temperature value. Using default 0.7.[/bold red]")
            temperature = 0.7
        
        # Collect student information
        student_profile = self.collect_student_info()
        
        # Generate the study plan
        study_plan = self.generate_study_plan(
            api_key=api_key,
            model=model,
            student_profile=student_profile,
            temperature=temperature
        )
        
        # Print the study plan
        console.print("\n[bold green]===== PERSONALIZED STUDY PLAN =====[/bold green]\n")
        console.print(study_plan)
        
        # Save options
        save_option = console.input("\n[bold yellow]Would you like to save the study plan? (y/n): [/bold yellow]").lower()
        if save_option == 'y':
            format_options = ["txt", "md", "html"]
            format_choice = console.input(f"[bold yellow]Choose format {format_options} (default: txt): [/bold yellow]").lower()
            
            if format_choice not in format_options:
                format_choice = "txt"
                
            self.save_study_plan(student_profile["student_name"], study_plan, format_choice)
        
        # Visualization option
        viz_option = console.input("\n[bold yellow]Would you like to generate a visual schedule? (y/n): [/bold yellow]").lower()
        if viz_option == 'y':
            viz_path = self.visualize_study_schedule(study_plan)
            if viz_path:
                console.print(f"[bold green]Visualization saved to {viz_path}[/bold green]")

def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Generate personalized study plans using LangChain and OpenRouter")
    parser.add_argument("--model", help="Model name to use")
    parser.add_argument("--api-key", help="API key for OpenRouter")
    parser.add_argument("--sample", action="store_true", help="Use sample student profile")
    parser.add_argument("--temp", type=float, default=0.7, help="Temperature setting (0.0-1.0)")
    
    args = parser.parse_args()
    
    # Create and run the generator
    generator = StudyPlanGenerator()
    generator.run()

if __name__ == "__main__": 
    main()
