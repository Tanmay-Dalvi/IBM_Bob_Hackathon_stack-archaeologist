"""
HTML Report Generator - Premium Modern Design
Creates self-contained HTML reports with inline CSS
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging
import re
import html

from app.core.config import settings

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates self-contained HTML reports with modern indigo/purple theme.
    Zero emojis, clean professional design.
    """
    
    def __init__(self):
        """Initialize report generator and create output directory"""
        self.output_dir = Path(settings.REPORT_OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"ReportGenerator initialized with output dir: {self.output_dir}")
    
    async def generate_report(
        self,
        repo_name: str,
        git_data: Dict,
        architecture: Dict,
        cause_of_death: Dict,
        salvageable: Dict,
        revival_plan: Dict
    ) -> str:
        """
        Generate a complete HTML archaeological report.
        
        Args:
            repo_name: Name of the repository
            git_data: Raw git analysis data
            architecture: Architecture analysis
            cause_of_death: Abandonment analysis
            salvageable: Salvageable components analysis
            revival_plan: Revival plan
            
        Returns:
            Filename of the generated report
        """
        try:
            # Create filename: repo-name-timestamp.html
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_repo_name = self._sanitize_filename(repo_name)
            filename = f"{safe_repo_name}-{timestamp}.html"
            report_path = self.output_dir / filename
            
            # Generate HTML content
            html_content = self._generate_html(
                repo_name=repo_name,
                git_data=git_data,
                architecture=architecture,
                cause_of_death=cause_of_death,
                salvageable=salvageable,
                revival_plan=revival_plan,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            # Write to file
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Report generated: {report_path}")
            return filename
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            raise
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize repository name for use in filename"""
        name = re.sub(r'[<>:"/\\|?*]', '-', name)
        name = name.strip('. ')
        return name[:50] if name else 'unknown-repo'
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return html.escape(str(text))
    
    def _format_text(self, text: str) -> str:
        """
        Format text by converting markdown-style formatting to HTML.
        Handles **bold**, bullet points, and line breaks.
        """
        if not text:
            return ''
        
        # Escape HTML first
        text = self._escape_html(text)
        
        # Convert **text** to <strong>text</strong>
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #6366F1; font-weight: 600;">\1</strong>', text)
        
        # Convert numbered lists (1. item) to proper HTML
        text = re.sub(
            r'^(\d+)\.\s+(.+)$',
            r'<div style="margin: 12px 0;"><strong style="color: #6366F1;">\1.</strong> \2</div>',
            text,
            flags=re.MULTILINE
        )
        
        # Convert bullet points (- item or * item) to proper HTML
        text = re.sub(
            r'^[-*]\s+(.+)$',
            r'<div style="margin: 10px 0; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: #6366F1;">•</span>\1</div>',
            text,
            flags=re.MULTILINE
        )
        
        # Convert double line breaks to paragraphs
        paragraphs = text.split('\n\n')
        formatted_paragraphs = [f'<p style="margin: 16px 0; line-height: 1.8;">{p.strip()}</p>' for p in paragraphs if p.strip()]
        
        return ''.join(formatted_paragraphs)
    
    def _generate_html(
        self,
        repo_name: str,
        git_data: Dict,
        architecture: Dict,
        cause_of_death: Dict,
        salvageable: Dict,
        revival_plan: Dict,
        timestamp: str
    ) -> str:
        """
        Generate complete self-contained HTML with inline CSS.
        Modern indigo/purple theme, zero emojis.
        """
        
        # Extract data
        total_commits = git_data.get('total_commits', 0)
        last_commit_date = self._format_date(git_data.get('last_commit_date', 'Unknown'))
        days_abandoned = git_data.get('days_since_last_commit', 0)
        top_contributors = git_data.get('top_contributors', [])
        top_contributor = top_contributors[0].get('name', 'Unknown') if top_contributors else 'Unknown'
        
        # Get severity
        severity = cause_of_death.get('severity', 'medium').upper()
        severity_colors = {
            'LOW': '#10B981',
            'MEDIUM': '#F97316',
            'HIGH': '#EF4444',
            'CRITICAL': '#EF4444'
        }
        severity_color = severity_colors.get(severity, '#F97316')
        
        # Build tech stack
        dep_files = git_data.get('dependency_files', [])
        tech_stack = self._build_tech_stack(dep_files, git_data.get('file_extensions', {}))
        
        # Format analysis content
        architecture_html = self._format_text(architecture.get('analysis', 'No analysis available'))
        cause_of_death_html = self._format_text(cause_of_death.get('analysis', 'No analysis available'))
        salvageable_html = self._format_text(salvageable.get('analysis', 'No analysis available'))
        revival_plan_html = self._format_text(revival_plan.get('analysis', 'No plan available'))
        
        # Build HTML
        html_output = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Report - {self._escape_html(repo_name)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: none;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #080B14;
            color: #E2E8F0;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* Navbar */
        .navbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 52px;
            background: #080B14;
            border-bottom: 1px solid #1F2640;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 48px;
            z-index: 100;
        }}
        
        .navbar-brand {{
            font-size: 13px;
            color: #64748B;
            font-weight: 500;
        }}
        
        .navbar-info {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .repo-name {{
            font-size: 13px;
            color: #E2E8F0;
            font-weight: 500;
        }}
        
        .analyzed-date {{
            font-size: 12px;
            color: #64748B;
        }}
        
        /* KPI Strip */
        .kpi-strip {{
            margin-top: 52px;
            background: #0F1320;
            border-bottom: 1px solid #1F2640;
            padding: 24px 48px;
        }}
        
        .kpi-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .kpi-item {{
            flex: 1;
            text-align: center;
            padding: 0 20px;
            border-right: 1px solid #1F2640;
        }}
        
        .kpi-item:last-child {{
            border-right: none;
        }}
        
        .kpi-value {{
            font-size: 28px;
            font-weight: 700;
            color: #E2E8F0;
            margin-bottom: 6px;
        }}
        
        .kpi-label {{
            font-size: 11px;
            font-weight: 500;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        
        /* Tech Stack Row */
        .tech-stack-row {{
            background: #080B14;
            padding: 16px 48px;
            border-bottom: 1px solid #1F2640;
        }}
        
        .tech-stack-container {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .tech-stack-label {{
            font-size: 11px;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 500;
        }}
        
        .tech-pill {{
            background: #1F2640;
            color: #6366F1;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}
        
        /* Main Content */
        .main-content {{
            padding: 32px 48px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .cards-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .report-card {{
            background: #141928;
            border: 1px solid #1F2640;
            border-radius: 12px;
            padding: 28px 32px;
        }}
        
        .card-header {{
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #1F2640;
        }}
        
        .card-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #64748B;
            font-weight: 600;
        }}
        
        .card-body {{
            font-size: 14px;
            line-height: 1.8;
            color: #CBD5E1;
        }}
        
        .card-body strong {{
            color: #6366F1;
            font-weight: 600;
        }}
        
        /* Footer */
        .footer {{
            padding: 32px 48px;
            border-top: 1px solid #1F2640;
            text-align: center;
            margin-top: 40px;
        }}
        
        .footer-brand {{
            font-size: 13px;
            color: #E2E8F0;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        
        .footer-credit {{
            font-size: 12px;
            color: #64748B;
        }}
        
        /* Responsive */
        @media (max-width: 1024px) {{
            .navbar {{
                padding: 0 24px;
            }}
            
            .kpi-strip {{
                padding: 20px 24px;
            }}
            
            .kpi-container {{
                flex-wrap: wrap;
            }}
            
            .kpi-item {{
                flex: 1 1 50%;
                border-right: none;
                border-bottom: 1px solid #1F2640;
                padding: 16px 0;
            }}
            
            .kpi-item:nth-last-child(-n+2) {{
                border-bottom: none;
            }}
            
            .tech-stack-row {{
                padding: 16px 24px;
            }}
            
            .main-content {{
                padding: 24px;
            }}
            
            .cards-grid {{
                grid-template-columns: 1fr;
            }}
            
            .footer {{
                padding: 24px;
            }}
        }}
        
        @media (max-width: 640px) {{
            .navbar {{
                padding: 0 16px;
            }}
            
            .navbar-info {{
                flex-direction: column;
                align-items: flex-end;
                gap: 4px;
            }}
            
            .kpi-strip {{
                padding: 16px;
            }}
            
            .kpi-item {{
                flex: 1 1 100%;
            }}
            
            .tech-stack-row {{
                padding: 12px 16px;
            }}
            
            .main-content {{
                padding: 16px;
            }}
            
            .report-card {{
                padding: 20px 16px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="navbar-brand">Stack Archaeologist</div>
        <div class="navbar-info">
            <div class="repo-name">{self._escape_html(repo_name)}</div>
            <div class="analyzed-date">Analyzed on {self._escape_html(timestamp)}</div>
        </div>
    </nav>
    
    <!-- KPI Strip -->
    <div class="kpi-strip">
        <div class="kpi-container">
            <div class="kpi-item">
                <div class="kpi-value">{days_abandoned}</div>
                <div class="kpi-label">Days Abandoned</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-value">{total_commits}</div>
                <div class="kpi-label">Total Commits</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-value">{self._escape_html(last_commit_date)}</div>
                <div class="kpi-label">Last Commit</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-value" style="color: {severity_color};">{severity}</div>
                <div class="kpi-label">Severity</div>
            </div>
            <div class="kpi-item">
                <div class="kpi-value" style="font-size: 16px;">{self._escape_html(top_contributor)}</div>
                <div class="kpi-label">Top Contributor</div>
            </div>
        </div>
    </div>
    
    <!-- Tech Stack Row -->
    <div class="tech-stack-row">
        <div class="tech-stack-container">
            <span class="tech-stack-label">Detected Stack</span>
            {self._render_tech_pills(tech_stack)}
        </div>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
        <div class="cards-grid">
            <!-- Architecture Analysis -->
            <div class="report-card">
                <div class="card-header">
                    <div class="card-title">Architecture Analysis</div>
                </div>
                <div class="card-body">
                    {architecture_html}
                </div>
            </div>
            
            <!-- Cause of Death -->
            <div class="report-card">
                <div class="card-header">
                    <div class="card-title">Cause of Death</div>
                </div>
                <div class="card-body">
                    {cause_of_death_html}
                </div>
            </div>
            
            <!-- Salvageable Components -->
            <div class="report-card">
                <div class="card-header">
                    <div class="card-title">Salvageable Components</div>
                </div>
                <div class="card-body">
                    {salvageable_html}
                </div>
            </div>
            
            <!-- Revival Plan -->
            <div class="report-card">
                <div class="card-header">
                    <div class="card-title">Revival Plan</div>
                </div>
                <div class="card-body">
                    {revival_plan_html}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="footer-brand">Stack Archaeologist</div>
        <div class="footer-credit">Built using IBM Bob IDE and Google Gemini</div>
    </footer>
</body>
</html>'''
        
        return html_output
    
    def _format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format"""
        try:
            if not date_str or date_str == 'Unknown':
                return 'Unknown'
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        except Exception:
            return str(date_str)[:10]
    
    def _build_tech_stack(self, dep_files: List[str], file_exts: Dict) -> List[str]:
        """Build tech stack list from dependency files and file extensions"""
        tech_stack = []
        
        # Map dependency files to tech names
        tech_map = {
            'package.json': 'Node.js',
            'requirements.txt': 'Python',
            'pom.xml': 'Java',
            'go.mod': 'Go',
            'Gemfile': 'Ruby',
            'Cargo.toml': 'Rust',
            'composer.json': 'PHP',
            'build.gradle': 'Java',
        }
        
        for dep_file in dep_files:
            if dep_file in tech_map:
                tech = tech_map[dep_file]
                if tech not in tech_stack:
                    tech_stack.append(tech)
        
        # If no dependency files, infer from file extensions
        if not tech_stack:
            ext_map = {
                '.py': 'Python',
                '.js': 'JavaScript',
                '.ts': 'TypeScript',
                '.java': 'Java',
                '.go': 'Go',
                '.rb': 'Ruby',
                '.php': 'PHP',
                '.rs': 'Rust',
                '.cpp': 'C++',
                '.c': 'C',
                '.cs': 'C#',
            }
            for ext, count in sorted(file_exts.items(), key=lambda x: x[1], reverse=True)[:3]:
                if ext in ext_map:
                    tech = ext_map[ext]
                    if tech not in tech_stack:
                        tech_stack.append(tech)
        
        return tech_stack if tech_stack else ['Unknown']
    
    def _render_tech_pills(self, tech_stack: List[str]) -> str:
        """Render tech stack pills HTML"""
        pills = []
        for tech in tech_stack:
            pills.append(f'<span class="tech-pill">{self._escape_html(tech)}</span>')
        return '\n'.join(pills)

# Made with Bob
