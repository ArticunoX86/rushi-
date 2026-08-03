import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

def build_pdf(filename="Project_Codebase_Telephony_Integration_and_Costing_Guide.pdf"):
    pdf_path = os.path.join(os.path.dirname(__file__), filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#0F172A")   # Slate 900
    SECONDARY = colors.HexColor("#2563EB") # Royal Blue
    DARK_TEXT = colors.HexColor("#334155") # Slate 700
    LIGHT_BG = colors.HexColor("#F8FAFC")  # Slate 50
    ACCENT = colors.HexColor("#059669")    # Emerald Green
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=6
    )

    story = []

    # Title & Executive Header
    story.append(Paragraph("Codebase Telephony Integration & Costing Implementation Guide", title_style))
    story.append(Paragraph("Connecting Exotel, Airtel SIP, and Twilio directly into salesforce-ai-calling-agent/backend | 100 Calls/Day (12,000 Mins/Month)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    # Executive Overview
    story.append(Paragraph("1. Overview & Codebase Architecture Map", h1_style))
    overview_text = (
        "This guide outlines how to integrate three PSTN cloud telephony providers into our active FastAPI backend "
        "(<code>c:\\Internship\\Backup\\salesforce-ai-calling-agent\\backend</code>). "
        "Each approach allows customer calls to be answered directly on their regular phone receiver with <b>zero application installed on the customer's device</b>."
    )
    story.append(Paragraph(overview_text, body_style))

    # Codebase Structure Table
    codebase_table = [
        [Paragraph("<b>Target Backend File</b>", body_style), Paragraph("<b>Function & Integration Role</b>", body_style)],
        [Paragraph("<code>app/api/call_dispatch.py</code>", body_style), Paragraph("Triggers outbound PSTN call dispatch via Telephony Provider API", body_style)],
        [Paragraph("<code>app/services/call_dispatcher.py</code>", body_style), Paragraph("Orchestrates call dispatch queuing and database status update", body_style)],
        [Paragraph("<code>app/services/call_orchestrator.py</code>", body_style), Paragraph("Manages Deepgram STT, Gemini LLM, and ElevenLabs/Aura TTS audio streams", body_style)],
        [Paragraph("<code>app/main.py</code>", body_style), Paragraph("Registers new Telephony API routers (Exotel / Airtel / Twilio)", body_style)]
    ]
    t_codebase = Table(codebase_table, colWidths=[180, 340])
    t_codebase.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_codebase)
    story.append(Spacer(1, 8))

    # Comprehensive Costing Table
    story.append(Paragraph("2. Itemized Monthly Costing Matrix (100 Calls/Day = 12,000 Mins/Month)", h1_style))
    
    cost_table_data = [
        [
            Paragraph("<b>Cost Component</b>", body_style),
            Paragraph("<b>Approach 1: Exotel Cloud (Rec.)</b>", body_style),
            Paragraph("<b>Approach 2: Airtel SIP Trunk</b>", body_style),
            Paragraph("<b>Approach 3: Twilio Voice API</b>", body_style)
        ],
        [
            Paragraph("Telephony Outbound Rate", body_style),
            Paragraph("₹0.60 / min ($0.0071)", body_style),
            Paragraph("₹0.30 / min ($0.0036)", body_style),
            Paragraph("₹1.52 / min ($0.0180)", body_style)
        ],
        [
            Paragraph("Monthly Trunk / License Fee", body_style),
            Paragraph("₹2,000 ($23.80)", body_style),
            Paragraph("₹2,500 ($30.00)", body_style),
            Paragraph("₹97 ($1.15)", body_style)
        ],
        [
            Paragraph("<b>Total Telephony Cost</b>", body_style),
            Paragraph("<b>₹9,200 INR ($109.50)</b>", body_style),
            Paragraph("<b>₹6,100 INR ($72.60)</b>", body_style),
            Paragraph("<b>₹18,241 INR ($217.15)</b>", body_style)
        ],
        [
            Paragraph("Deepgram STT (Nova-2)", body_style),
            Paragraph("₹4,334 INR ($51.60)", body_style),
            Paragraph("₹4,334 INR ($51.60)", body_style),
            Paragraph("₹4,334 INR ($51.60)", body_style)
        ],
        [
            Paragraph("Google Gemini 2.5 Flash LLM", body_style),
            Paragraph("₹300 INR ($3.57)", body_style),
            Paragraph("₹300 INR ($3.57)", body_style),
            Paragraph("₹300 INR ($3.57)", body_style)
        ],
        [
            Paragraph("TTS (Deepgram Aura / 11Labs)", body_style),
            Paragraph("₹6,000 INR ($71.42)", body_style),
            Paragraph("₹6,000 INR ($71.42)", body_style),
            Paragraph("₹6,000 INR ($71.42)", body_style)
        ],
        [
            Paragraph("AWS S3 Storage (3k Wavs)", body_style),
            Paragraph("₹25 INR ($0.30)", body_style),
            Paragraph("₹25 INR ($0.30)", body_style),
            Paragraph("₹25 INR ($0.30)", body_style)
        ],
        [
            Paragraph("<b>TOTAL MONTHLY COST</b>", body_style),
            Paragraph("<b>₹19,859 INR ($236.40)</b>", body_style),
            Paragraph("<b>₹16,759 INR ($199.50)</b>", body_style),
            Paragraph("<b>₹28,900 INR ($344.05)</b>", body_style)
        ],
        [
            Paragraph("<b>Cost Per 4-Min Call</b>", body_style),
            Paragraph("<b>₹6.61 INR ($0.078)</b>", body_style),
            Paragraph("<b>₹5.58 INR ($0.066)</b>", body_style),
            Paragraph("<b>₹9.63 INR ($0.114)</b>", body_style)
        ],
        [
            Paragraph("<b>Effective Per Minute Cost</b>", body_style),
            Paragraph("<b>~₹1.65 INR / min</b>", body_style),
            Paragraph("<b>~₹1.39 INR / min</b>", body_style),
            Paragraph("<b>~₹2.40 INR / min</b>", body_style)
        ]
    ]

    t_cost = Table(cost_table_data, colWidths=[140, 126, 126, 128])
    t_cost.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor("#ECFDF5")),
    ]))
    story.append(t_cost)
    story.append(Spacer(1, 10))

    # Detailed Code Implementation Section
    story.append(Paragraph("3. Step-by-Step Codebase Integration for Each Approach", h1_style))

    # Approach 1: Exotel
    story.append(Paragraph("Approach 1: Exotel Voice Stream API Integration (Recommended)", h2_style))
    exotel_details = (
        "<b>New Backend File</b>: <code>app/api/exotel.py</code><br/>"
        "1. Modify <code>app/services/call_dispatcher.py</code> to trigger Exotel outbound call API:<br/>"
        "2. Exotel dials customer phone number over PSTN.<br/>"
        "3. When customer answers, Exotel connects to WebSocket endpoint <code>/exotel/stream/{call_id}</code>.<br/>"
        "4. <code>exotel.py</code> receives 8kHz mulaw audio chunks, converts to PCM, passes to <code>CallOrchestrator</code>, and streams AI speech back."
    )
    story.append(Paragraph(exotel_details, body_style))
    story.append(Paragraph("""# app/api/exotel.py (New File)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.call_orchestrator import CallOrchestrator

router = APIRouter(prefix="/exotel", tags=["Exotel Telephony"])

@router.websocket("/stream/{call_id}")
async def exotel_stream(websocket: WebSocket, call_id: str):
    await websocket.accept()
    orchestrator = CallOrchestrator(call_id=call_id)
    await orchestrator.start()
    try:
        while True:
            data = await websocket.receive_bytes()
            await orchestrator.process_audio_chunk(data)
    except WebSocketDisconnect:
        await orchestrator.close()""", code_style))

    # Approach 2: Airtel SIP + FreeSWITCH
    story.append(Paragraph("Approach 2: Airtel SIP Trunk + FreeSWITCH / LiveKit Gateway", h2_style))
    airtel_details = (
        "<b>New Backend File</b>: <code>app/services/freeswitch_service.py</code><br/>"
        "1. Deploy FreeSWITCH Docker container listening on Airtel SIP IP.<br/>"
        "2. <code>call_dispatcher.py</code> sends ESL socket command to FreeSWITCH.<br/>"
        "3. FreeSWITCH dials customer phone number over Airtel SIP trunk.<br/>"
        "4. FreeSWITCH pipes RTP audio stream directly into <code>webrtc_agent.py</code> using LiveKit SIP or ESL stream."
    )
    story.append(Paragraph(airtel_details, body_style))
    story.append(Paragraph("""# app/services/freeswitch_service.py (New File)
import httpx
async def trigger_airtel_sip_call(phone_number: str, call_id: str):
    # Sends ESL Originate command to FreeSWITCH Docker Container
    url = "http://localhost:8081/freeswitch/originate"
    payload = {"destination": phone_number, "call_id": call_id, "gateway": "airtel_sip"}
    async with httpx.AsyncClient() as client:
        return await client.post(url, json=payload)""", code_style))

    # Approach 3: Twilio Voice Media Stream
    story.append(Paragraph("Approach 3: Twilio Voice Media Stream Integration", h2_style))
    twilio_details = (
        "<b>New Backend File</b>: <code>app/api/twilio.py</code><br/>"
        "1. Modify <code>call_dispatcher.py</code> to use <code>twilio.rest.Client</code>.<br/>"
        "2. Twilio fetches TwiML XML returning <code><Connect><Stream url='wss://domain.com/twilio/stream'/></Connect></code>.<br/>"
        "3. Twilio streams base64 8kHz mulaw audio chunks to FastAPI WebSocket."
    )
    story.append(Paragraph(twilio_details, body_style))
    story.append(Paragraph("""# app/api/twilio.py (New File)
from fastapi import APIRouter, Response, WebSocket

router = APIRouter(prefix="/twilio", tags=["Twilio Telephony"])

@router.post("/voice")
async def twilio_voice():
    xml = '<?xml version="1.0"?><Response><Connect><Stream url="wss://domain.com/twilio/stream"/></Connect></Response>'
    return Response(content=xml, media_type="application/xml")""", code_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("4. Integration Summary & Next Steps", h1_style))
    summary_text = (
        "• <b>Exotel</b> is recommended for fastest implementation into <code>salesforce-ai-calling-agent/backend</code> with zero hardware setup (<b>~₹1.65/min total</b>).<br/>"
        "• <b>Airtel SIP</b> is recommended for maximum scale at lowest per-minute cost (<b>~₹1.39/min total</b>).<br/>"
        "• All three approaches route audio <b>directly to the customer's phone ear receiver</b> without requiring any mobile app on their device."
    )
    story.append(Paragraph(summary_text, body_style))

    doc.build(story)
    print(f"Project Integration PDF Report generated successfully at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
