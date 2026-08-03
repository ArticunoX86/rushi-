import os
import subprocess
import sys

# Ensure reportlab is installed
try:
    import reportlab
except ImportError:
    print("Installing reportlab...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_pdf(filename="AI_Audio_Streaming_Methodology_and_Cost_Analysis.pdf"):
    # Target page width/height details for margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom color palette (Hex Colors)
    primary_color = colors.HexColor("#1E3A8A")  # Deep Blue
    secondary_color = colors.HexColor("#0D9488")  # Teal
    neutral_dark = colors.HexColor("#1F2937")  # Charcoal
    neutral_light = colors.HexColor("#F9FAFB")  # Off-white
    border_color = colors.HexColor("#E5E7EB")  # Light gray

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=neutral_dark,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeaderText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=neutral_dark
    )

    story = []

    # Title Page/Header
    story.append(Paragraph("AI Audio Streaming: Methodology & Cost Analysis", title_style))
    story.append(Paragraph("Technical Evaluation of Calling Platform Architectures", subtitle_style))
    story.append(Spacer(1, 10))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "This report provides a comparative study of the primary architectures for implementing real-time conversational "
        "AI calling systems. It outlines the implementation methodology and detailed cost structures for four approaches: "
        "the Mobile App Gateway, Twilio Media Streams, WebRTC via LiveKit, and Managed Voice APIs (Vapi/Retell).",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Approach 1
    story.append(Paragraph("Approach 1: Mobile App Gateway (Current Architecture)", h1_style))
    story.append(Paragraph("Methodology:", h2_style))
    story.append(Paragraph("• <b>App Transport:</b> The mobile device acts as an audio transceiver. Dart code establishes WebSocket live loops and requests native phone call routing via MethodChannels.", bullet_style))
    story.append(Paragraph("• <b>Mic Stream:</b> Native Kotlin handles AudioRecord mono microphone capturing (16kHz PCM), chunking it into byte arrays sent over WebSockets to the Python backend.", bullet_style))
    story.append(Paragraph("• <b>Audio Playback:</b> Incoming ElevenLabs audio bytes are downloaded on the mobile client, written to a temporary MP3 file, and played in real time using the Android MediaPlayer.", bullet_style))
    story.append(Paragraph("• <b>Transcription & AI:</b> Python server pipes PCM bytes into Deepgram SDK's live stream. The transcription result triggers Gemini LLM generation, which synthesizes audio via ElevenLabs TTS.", bullet_style))
    
    story.append(Paragraph("Cost Breakdown:", h2_style))
    story.append(Paragraph("• <b>Deepgram STT:</b> ~$0.0043 to $0.0150 per minute (depending on Tier/Volume).", bullet_style))
    story.append(Paragraph("• <b>Gemini LLM:</b> ~$0.00015 per 1K input tokens + $0.0006 per 1K output tokens (extremely low).", bullet_style))
    story.append(Paragraph("• <b>ElevenLabs TTS:</b> ~$0.15 to $0.24 per 1,000 characters (avg. ~$0.08 per conversational minute).", bullet_style))
    story.append(Paragraph("• <b>Telephony (SIM):</b> Cost of the mobile carrier plan (usually flat-rate or standard cellular billing).", bullet_style))
    story.append(Paragraph("• <b>Total Estimated Cost:</b> <b>~$0.10 to $0.15 per conversation minute</b>.", bullet_style))
    story.append(Spacer(1, 15))

    # Approach 2
    story.append(Paragraph("Approach 2: Twilio Media Streams (Direct Telephony)", h1_style))
    story.append(Paragraph("Methodology:", h2_style))
    story.append(Paragraph("• <b>SIP Integration:</b> A phone call is initiated via Twilio API. Twilio's XML instruction (<font face='Courier'>&lt;Stream&gt;</font>) directs it to connect bi-directionally to the backend's WebSocket url.", bullet_style))
    story.append(Paragraph("• <b>Audio Packets:</b> Twilio streams raw audio payload (8kHz Mu-law PCM) formatted in JSON envelopes containing base64 encoded audio strings.", bullet_style))
    story.append(Paragraph("• <b>Speech Translation:</b> Python backend decodes Mu-law bytes, upsamples them to 16kHz mono, and routes them to Deepgram.", bullet_style))
    story.append(Paragraph("• <b>Voice Generation:</b> Gemini output is sent to ElevenLabs. The resulting audio is downsampled to 8kHz Mu-law PCM, base64 encoded, wrapped in a Twilio JSON envelope, and sent back.", bullet_style))
    
    story.append(Paragraph("Cost Breakdown:", h2_style))
    story.append(Paragraph("• <b>Twilio Voice:</b> $0.0130 to $0.0140 per minute (Standard SIP/PSTN inbound/outbound rates).", bullet_style))
    story.append(Paragraph("• <b>Deepgram STT + Gemini LLM + ElevenLabs TTS:</b> Same as Approach 1 (approx. ~$0.09 per minute).", bullet_style))
    story.append(Paragraph("• <b>Total Estimated Cost:</b> <b>~$0.11 to $0.17 per conversation minute</b>.", bullet_style))
    story.append(Spacer(1, 15))

    story.append(PageBreak())  # Move to Page 2 for structural neatness

    # Approach 3
    story.append(Paragraph("Approach 3: WebRTC via LiveKit (App/Web Native Agent)", h1_style))
    story.append(Paragraph("Methodology:", h2_style))
    story.append(Paragraph("• <b>UDP Media Server:</b> Set up an open-source LiveKit Media Server (SFU) running in Docker. The client app connects to LiveKit Room using WebRTC.", bullet_style))
    story.append(Paragraph("• <b>Media Pipeline:</b> LiveKit handles high-quality bi-directional audio tracking using UDP/SRTP protocols (extremely resilient to network drops, sub-100ms transport latency).", bullet_style))
    story.append(Paragraph("• <b>Agent Integration:</b> LiveKit Agents Framework running in Python acts as a participant in the room, intercepting client voice tracks and piping synthesized responses directly back as a track.", bullet_style))
    
    story.append(Paragraph("Cost Breakdown:", h2_style))
    story.append(Paragraph("• <b>LiveKit Hosting:</b> Free (Self-hosted on AWS EC2/DigitalOcean) or LiveKit Cloud (Free tier, then $0.0035/minute).", bullet_style))
    story.append(Paragraph("• <b>Deepgram STT + Gemini LLM + ElevenLabs:</b> Same as Approach 1 (approx. ~$0.09 per minute).", bullet_style))
    story.append(Paragraph("• <b>Total Estimated Cost:</b> <b>~$0.09 to $0.11 per conversation minute</b>.", bullet_style))
    story.append(Spacer(1, 15))

    # Approach 4
    story.append(Paragraph("Approach 4: Managed Voice APIs (Vapi / Retell AI)", h1_style))
    story.append(Paragraph("Methodology:", h2_style))
    story.append(Paragraph("• <b>One-API Setup:</b> No custom WebSockets, audio buffering, resamplings, or SDK synchronization is written.", bullet_style))
    story.append(Paragraph("• <b>Configuration:</b> An agent config is created via API specifying: System Prompt, Deepgram Model, ElevenLabs Voice ID, and Webhook URLs.", bullet_style))
    story.append(Paragraph("• <b>Execution:</b> Call Vapi/Retell API to dial. Their infrastructure coordinates the entire STT-LLM-TTS stream, providing highly optimized sub-second conversational latency.", bullet_style))
    
    story.append(Paragraph("Cost Breakdown:", h2_style))
    story.append(Paragraph("• <b>Platform Fee:</b> $0.15 per conversation minute (includes platform overhead + built-in standard STT/TTS pricing).", bullet_style))
    story.append(Paragraph("• <b>Premium Voice Add-on (ElevenLabs):</b> Custom ElevenLabs key usage billed at cost (~$0.08 per minute).", bullet_style))
    story.append(Paragraph("• <b>Total Estimated Cost:</b> <b>~$0.20 to $0.25 per conversation minute</b>.", bullet_style))
    story.append(Spacer(1, 20))

    # Cost Comparison Summary Table
    story.append(Paragraph("Cost & Architecture Comparison Table", h1_style))
    
    headers = [
        Paragraph("<b>Architecture Approach</b>", table_header_style),
        Paragraph("<b>Telephony / Media Cost</b>", table_header_style),
        Paragraph("<b>AI Services (STT/LLM/TTS)</b>", table_header_style),
        Paragraph("<b>Total Est. Cost/Min</b>", table_header_style),
        Paragraph("<b>Development Complexity</b>", table_header_style)
    ]
    
    row1 = [
        Paragraph("<b>1. Mobile App Gateway</b>", table_cell_style),
        Paragraph("SIM Carrier Cost (Flat-rate)", table_cell_style),
        Paragraph("~$0.09 / min", table_cell_style),
        Paragraph("<b>~$0.10 - $0.15</b>", table_cell_style),
        Paragraph("Medium (Requires Native OS Kotlin/Swift bridges)", table_cell_style)
    ]

    row2 = [
        Paragraph("<b>2. Twilio Media Streams</b>", table_cell_style),
        Paragraph("~$0.0135 / min (Twilio SIP)", table_cell_style),
        Paragraph("~$0.09 / min", table_cell_style),
        Paragraph("<b>~$0.11 - $0.17</b>", table_cell_style),
        Paragraph("High (Requires complex socket payload encoding)", table_cell_style)
    ]

    row3 = [
        Paragraph("<b>3. WebRTC via LiveKit</b>", table_cell_style),
        Paragraph("Self-hosted ($0) or Cloud ($0.0035)", table_cell_style),
        Paragraph("~$0.09 / min", table_cell_style),
        Paragraph("<b>~$0.09 - $0.11</b>", table_cell_style),
        Paragraph("High (Requires WebRTC media server setup)", table_cell_style)
    ]

    row4 = [
        Paragraph("<b>4. Managed Voice APIs</b>", table_cell_style),
        Paragraph("Included in fee", table_cell_style),
        Paragraph("Platform fee + custom TTS (~$0.23)", table_cell_style),
        Paragraph("<b>~$0.20 - $0.25</b>", table_cell_style),
        Paragraph("Low (Single HTTP call config setup)", table_cell_style)
    ]

    data = [headers, row1, row2, row3, row4]
    
    col_widths = [1.5 * inch, 1.6 * inch, 1.4 * inch, 1.1 * inch, 1.4 * inch]
    
    summary_table = Table(data, colWidths=col_widths)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('BACKGROUND', (0,1), (-1,1), neutral_light),
        ('BACKGROUND', (0,3), (-1,3), neutral_light),
    ]))
    
    story.append(summary_table)

    # Build the document
    doc.build(story)
    print("PDF Report generated successfully!")

if __name__ == "__main__":
    create_pdf()
