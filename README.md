# Stack Archaeologist

> An AI-powered tool that excavates and analyzes abandoned GitHub repositories, generating detailed archaeological reports about their history, cause of abandonment, salvageable components, and revival potential.

## What It Does

- Clones any public GitHub repository
- Analyzes git history, commit patterns, file structure
- Uses IBM Bob AI to generate 4-section report:
  - **Architecture Analysis** - Understanding the codebase structure and design
  - **Cause of Death** - Identifying why the project was abandoned
  - **Salvageable Components** - Finding reusable code and patterns
  - **Revival Plan** - Estimating effort and steps needed to revive the project
- Generates a beautiful self-contained HTML report with modern UI

## Built With

- **IBM Bob IDE** - AI-assisted development environment
- **IBM Bob AI** - Intelligent analysis powered by IBM's AI platform
- **Python 3.8+** - Backend runtime
- **FastAPI** - Modern web framework
- **GitPython** - Git repository analysis

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd ibm_bob_hackathon
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and add your BOB_API_KEY
```

Get your IBM Bob API key from the IBM Bob IDE platform.

### 4. Run the application

```bash
python run.py
```

Visit http://localhost:8000 in your browser.

## How to Use

1. Open http://localhost:8000 in your web browser
2. Paste any public GitHub repository URL (e.g., `https://github.com/user/repo`)
3. Click "Analyze Repository"
4. Wait 15-30 seconds for the analysis to complete
5. View results summary on the landing page
6. Click "View Full Report" to see the detailed archaeological report

## Environment Variables

```env
BOB_API_KEY=your_bob_api_key_here
APP_HOST=127.0.0.1
APP_PORT=8000
DEBUG=True
```

## Project Structure

```
stack-archaeologist/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── core/
│   │   └── config.py                # Configuration management
│   ├── services/
│   │   ├── git_analyzer.py          # Git repository analysis
│   │   ├── mock_watsonx_service.py  # AI analysis service
│   │   └── report_generator.py      # HTML report generation
│   ├── templates/
│   │   └── landing_page.html        # Frontend interface
│   └── static/                      # Static assets
├── reports/                         # Generated HTML reports
├── temp_repos/                      # Temporary repository clones
├── requirements.txt                 # Python dependencies
├── run.py                          # Application entry point
├── .env.example                    # Environment template
└── README.md                       # This file
```

## Features

### Modern UI Design
- Clean, professional indigo/purple color scheme
- Responsive design that works on desktop and mobile
- Self-contained HTML reports (no external dependencies)
- Smooth user experience with loading states

### Intelligent Analysis
- Detects technology stack from dependency files and file extensions
- Analyzes commit patterns to identify abandonment causes
- Calculates severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Estimates revival effort and provides actionable recommendations

### Git Analysis
- Total commits and contributor analysis
- Last commit date and days since abandonment
- Warning commit detection (bug fixes, TODOs, WIP)
- Branch analysis and file structure examination

## Architecture

The application follows a clean service-oriented architecture:

1. **FastAPI Backend** - Handles HTTP requests and orchestrates services
2. **Git Analyzer** - Clones and analyzes repository structure and history
3. **AI Service** - Generates intelligent insights using IBM Bob AI
4. **Report Generator** - Creates beautiful HTML reports with inline CSS
5. **Frontend** - Modern single-page interface for user interaction

## Hackathon

Built for the **IBM Bob Hackathon 2026**.

**Theme:** Turn idea into impact faster.

This project was developed entirely using **IBM Bob IDE** as the AI development partner, demonstrating how AI-assisted development can accelerate the creation of complex applications. The entire codebase, from backend services to frontend UI, was built with IBM Bob's intelligent assistance.

## Key Achievements

- ✅ Full-stack application built in record time
- ✅ Modern, professional UI with consistent design system
- ✅ Intelligent AI-powered analysis using IBM Bob AI
- ✅ Self-contained HTML reports with no external dependencies
- ✅ Clean, maintainable codebase with proper separation of concerns

## License

MIT License - feel free to use this project for your own repository archaeology needs!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

---

**Made with IBM Bob IDE** 🤖 | **Powered by IBM Bob AI** 🚀