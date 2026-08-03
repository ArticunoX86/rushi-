import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

def build_pdf(filename="NexaVoice_Project_Status_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=12,
        textColor=colors.HexColor('#1C1C2E'),
        alignment=1 # Center
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=14,
        textColor=colors.HexColor('#1B8B4B'), # Emerald Green
        alignment=1 # Center
    )
    
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor('#1C1C2E')
    )
    
    h3_style = ParagraphStyle(
        'H3Style',
        parent=styles['Heading3'],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#1B8B4B')
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leading=16
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        leading=16
    )

    story = []
    
    # 1. Title Section
    story.append(Paragraph("NexaVoice (Salesforce AI Calling Agent)", title_style))
    story.append(Paragraph("Project Completion & Status Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceBefore=10, spaceAfter=20))
    
    # 2. Executive Summary
    story.append(Paragraph("Executive Summary", h2_style))
    summary_text = (
        "The NexaVoice project is currently estimated to be <b>85% - 90% complete</b>. "
        "The core structural foundations across both the frontend mobile application (Flutter) and the AI/Backend (FastAPI) are fully implemented. "
        "The application has been successfully rebranded, the AI processing pipelines (Deepgram + Gemini) are functional, and the DevOps configurations (Docker) are ready for deployment. "
        "The project is now entering its final integration phase, requiring live credentials and end-to-end network testing over the public internet."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))
    
    # 3. Completed Work
    story.append(Paragraph("Section 1: Work Completed (100%)", h2_style))
    
    # Frontend
    story.append(Paragraph("1.1 Frontend App & Branding (Flutter)", h3_style))
    story.append(Paragraph("• Executed complete NexaVoice rebranding using the Emerald Green (#1B8B4B) & Charcoal color palette.", bullet_style))
    story.append(Paragraph("• Integrated the official NexaVoice app icon and logo assets.", bullet_style))
    story.append(Paragraph("• Redesigned the Login Screen with smooth animations and premium UI cards.", bullet_style))
    story.append(Paragraph("• Upgraded Dashboard, Transcripts, and Call Job cards with gradient pills and priority visualization.", bullet_style))
    story.append(Paragraph("• Built the Supervisor Console for seamlessly syncing leads from Salesforce to the local database.", bullet_style))
    
    # Backend
    story.append(Paragraph("1.2 AI Engine & Backend (FastAPI)", h3_style))
    story.append(Paragraph("• Integrated Deepgram Live API for real-time speech-to-text transcription.", bullet_style))
    story.append(Paragraph("• Integrated Google Gemini AI to handle intelligent call scripting and dynamic conversations.", bullet_style))
    story.append(Paragraph("• Created the Call Orchestrator logic to manage bidirectional audio streaming between the caller and the AI.", bullet_style))
    story.append(Paragraph("• Developed telephony API endpoints mapping out Exotel, Airtel SIP, and Twilio integration architectures.", bullet_style))
    
    # Database & DevOps
    story.append(Paragraph("1.3 Database & DevOps Architecture", h3_style))
    story.append(Paragraph("• Defined complete PostgreSQL database schema via Alembic for Users, Leads, Calls, and Devices.", bullet_style))
    story.append(Paragraph("• Created Dockerfile and docker-compose.yml for production-ready AWS deployment.", bullet_style))
    story.append(Paragraph("• Completed detailed Telephony Provider Cost Analysis predicting rates as low as ₹1.39/min (Airtel SIP).", bullet_style))
    story.append(Spacer(1, 10))
    
    story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceBefore=10, spaceAfter=20))
    
    # 4. Remaining Work
    story.append(Paragraph("Section 2: Pending Work (The Final 10% - 15%)", h2_style))
    
    story.append(Paragraph("2.1 Salesforce Production Credentials", h3_style))
    pending_sf = (
        "<b>Current Status:</b> The backend uses mock fallback data for testing.<br/>"
        "<b>Action Required:</b> Input live Salesforce API credentials (Client ID, Secret, Username, Password) into the backend environment variables so real leads can be synced."
    )
    story.append(Paragraph(pending_sf, body_style))
    
    story.append(Paragraph("2.2 Live Telephony Testing (Exotel / Airtel)", h3_style))
    pending_tel = (
        "<b>Current Status:</b> The endpoints for SIP routing are structurally built but await live network access.<br/>"
        "<b>Action Required:</b> Acquire a live Exotel Account (or Airtel SIP Trunk), configure the API keys, and perform end-to-end live testing over the public internet to ensure audio streams successfully flow into Deepgram and Gemini."
    )
    story.append(Paragraph(pending_tel, body_style))
    
    story.append(Paragraph("2.3 App Offline/Network Resilience", h3_style))
    pending_res = (
        "<b>Current Status:</b> The Flutter app assumes the backend is always reachable. If the backend goes down, the app hangs with an infinite loading spinner.<br/>"
        "<b>Action Required:</b> Update the frontend networking logic (DioClient & Providers) to catch connection errors and gracefully display a 'Backend Offline' UI overlay instead of crashing."
    )
    story.append(Paragraph(pending_res, body_style))
    
    story.append(Paragraph("2.4 Gradle & Build Upgrades", h3_style))
    pending_gradle = (
        "<b>Current Status:</b> The Android APK builds successfully but triggers deprecation warnings from older Gradle/Kotlin plugins.<br/>"
        "<b>Action Required:</b> Upgrade Gradle to version 8.14.0 and resolve plugin warnings to ensure long-term App Store compliance and maintainability."
    )
    story.append(Paragraph(pending_gradle, body_style))
    
    story.append(Paragraph("2.5 AWS / Cloud Deployment", h3_style))
    pending_aws = (
        "<b>Current Status:</b> Docker files are prepared, but the app is currently only running on localhost/Wi-Fi.<br/>"
        "<b>Action Required:</b> Spin up an AWS EC2 instance, deploy the Docker containers, configure Nginx + SSL, and update the Flutter AppConfig to point to the new public domain name."
    )
    story.append(Paragraph(pending_aws, body_style))
    
    doc.build(story)
    print(f"Generated {filename}")

if __name__ == "__main__":
    build_pdf()
