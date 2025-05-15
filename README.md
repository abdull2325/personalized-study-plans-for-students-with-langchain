</div>
An intelligent, LLM-powered application that generates highly personalized study plans for students by analyzing their unique academic profile, learning style, and personal circumstances. The tool leverages educational psychology principles and evidence-based learning strategies to create comprehensive, actionable study plans.
<p align="center">
  <img src="https://github.com/username/enhanced-study-plan-generator/raw/main/assets/study_plan_example.png" alt="Study Plan Example" width="600">
</p>
✨ Features

🧠 Personalized Analysis: Evaluates learning style, strengths, challenges, and goals
📚 Subject-Specific Strategies: Custom approaches for each course based on student needs
⏰ Intelligent Scheduling: Creates optimal study timetables accounting for energy levels
📊 Progress Monitoring: Built-in tracking systems with achievable milestones
🔄 Adaptive Planning: Strategies for exam preparation and challenge mitigation
📱 Multiple AI Models: Access GPT-4, Claude, Gemini, and more through OpenRouter
📈 Data Visualization: Generate visual study schedule representations
💻 Interactive CLI: Rich command-line interface with user-friendly prompts

🛠️ Installation
bash# Clone the repository
git clone https://github.com/yourusername/enhanced-study-plan-generator.git
cd enhanced-study-plan-generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
📋 Requirements
langchain>=0.1.0
langchain_openai>=0.0.5
pyyaml>=6.0
rich>=13.0.0
matplotlib>=3.7.0
numpy>=1.24.0
⚙️ Configuration
The application uses a config.yaml file for configuration. If not present, it will be created with default values on first run.
yamldefault_model: "gpt-4-turbo"
temperature: 0.7
output_dir: "study_plans"
openrouter_api_base: "https://openrouter.ai/api/v1"
🚀 Usage
Basic Usage
bashpython study_plan_generator.py
Follow the interactive prompts to:

Select an AI model
Set temperature for response creativity
Enter student information or use a sample profile
Generate the personalized study plan
Save and visualize the plan

Command-line Options
bash# Use a specific model with custom temperature
python study_plan_generator.py --model "claude-3-sonnet" --temp 0.8

# Use the sample profile
python study_plan_generator.py --sample

# Specify API key directly
python study_plan_generator.py --api-key "your-api-key"
📊 Example Output
The generator creates comprehensive study plans with sections including:

Executive Summary
Student Analysis
Weekly Master Schedule
Subject-Specific Action Plans
Progress Monitoring System
Exam Success Strategies
Challenge Mitigation Strategies
Implementation Guidance

<details>
<summary>Example Study Plan (Click to expand)</summary>
# PERSONALIZED STUDY PLAN FOR ALEX JOHNSON

## EXECUTIVE SUMMARY

Alex is an 11th-grade student with strong analytical abilities who faces challenges with physics problem-solving and time management. This plan leverages Alex's visual-spatial learning style and programming strengths while addressing test anxiety and focus difficulties through structured schedules and specialized techniques.

## WEEKLY MASTER SCHEDULE

### Monday
- 6:00-6:45 AM: Physics concept review using visual simulations
- 3:30-5:30 PM: Basketball practice
- 6:30-7:15 PM: Calculus integration practice
- 7:30-8:15 PM: English Literature reading with annotation
- 8:30-9:00 PM: Daily review and next-day preparation

### Tuesday
...
</details>
🧠 Student Profile Elements
For best results, include detailed information in these areas:

Academic Information: Subjects, grades, strengths/weaknesses
Learning Style: Visual, auditory, kinesthetic preferences
Schedule & Commitments: Extracurricular activities, jobs
Goals: Short-term and long-term academic objectives
Challenges: Learning obstacles, time management issues
Study Time: Available hours and peak productivity periods
Exams & Deadlines: Upcoming assessments and due dates
Resources: Preferred learning tools and resources
Special Considerations: Learning differences, accommodations

🌐 Supported AI Models
The application uses OpenRouter to access various language models:
ProviderModelsBest ForOpenAIGPT-3.5-Turbo, GPT-4-TurboDetailed analysis, reasoningAnthropicClaude-3-Haiku, Claude-3-SonnetThoughtful educational plansGoogleGemini-ProMultilingual content supportMistral AIMistral-Large, Mixtral-8x7bFast generation, efficiencyMetaLlama-2-70b-chatOpen source alternativeMicrosoftPhi-2Lightweight, efficient plans
📊 Visualization
The tool can generate visualizations of weekly study schedules using matplotlib:
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
⭐ Star History
Show Image

<p align="center">
  <a href="https://github.com/abdull2325">Created with ❤️ by Your Name</a>
</p>
