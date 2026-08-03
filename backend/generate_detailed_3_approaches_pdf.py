import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

def build_pdf(filename="Detailed_3_PSTN_Telephony_Approaches_Guide.pdf"):
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
    
    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")   # Slate 900
    SECONDARY = colors.HexColor("#2563EB") # Royal Blue
    TEAL = colors.HexColor("#0D9488")      # Teal Accent
    DARK_TEXT = colors.HexColor("#1E293B") # Slate 800
    LIGHT_BG = colors.HexColor("#F8FAFC")  # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")   # Slate 100
    BORDER_COLOR = colors.HexColor("#CBD5E1")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
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
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    diagram_style = ParagraphStyle(
        'Diagram',
        parent=styles['Code'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E3A8A"),
        backColor=colors.HexColor("#EFF6FF"),
        borderColor=colors.HexColor("#BFDBFE"),
        borderWidth=1,
        borderPadding=8,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=6
    )

    story = []

    # Title & Header
    story.append(Paragraph("Comprehensive Guide to 3 PSTN Telephony Approaches for AI Calling", title_style))
    story.append(Paragraph("Detailed Architecture, Step-by-Step Code Integration, and Cost Analysis for Delivering AI Voice Directly into Customer Phone Ear Receivers", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=12))

    # Core Problem & Solution Statement
    story.append(Paragraph("1. Executive Summary & Hardware Realities", h1_style))
    exec_summary = (
        "When placing automated AI sales calls, <b>Device B (the customer's phone) must hear the AI's synthesized voice crystal clear in their ear</b> without needing to install any application. "
        "Because physical Android smartphones physically block third-party apps from inserting digital audio files into standard SIM card phone calls, "
        "the industry standard solution is to connect your Python FastAPI backend directly to a <b>PSTN Telephony Infrastructure</b>."
    )
    story.append(Paragraph(exec_summary, body_style))
    story.append(Spacer(1, 6))

    # APPROACH 1: EXOTEL CLOUD TELEPHONY
    story.append(Paragraph("2. Approach 1: Exotel Cloud Telephony Voice Stream API (Recommended for India)", h1_style))
    exotel_overview = (
        "<b>Overview</b>: Exotel is India's leading enterprise cloud communications platform. It provides direct Indian virtual numbers, "
        "low per-minute tariffs, and native bi-directional WebSockets (Exotel Voice Stream API)."
    )
    story.append(Paragraph(exotel_overview, body_style))
    
    exotel_diagram = """[FastAPI Backend (app/services/call_dispatcher.py)]
      │  1. HTTP POST Call Request (Exotel REST API)
      ▼
[Exotel Cloud Telephony Engine]
      │  2. Dials Customer Phone Number via Indian Telecom Network
      ▼
[Customer's Mobile Phone] (Answers Call)
      │  3. Exotel Opens Bi-directional WebSocket to FastAPI
      ▼
[FastAPI /exotel/stream (WebSocket Receiver)] ◄──► [Deepgram STT ➔ Gemini LLM ➔ ElevenLabs TTS]"""
    story.append(Paragraph(exotel_diagram, diagram_style))

    story.append(Paragraph("How It Works technically:", h2_style))
    story.append(Paragraph("• <b>Outbound Dialing</b>: Your backend calls Exotel's REST API `POST /v1/Accounts/{SID}/Calls/connect.json` specifying the customer's phone number.", bullet_style))
    story.append(Paragraph("• <b>WebSocket Handshake</b>: When the customer picks up, Exotel connects via WebSockets to `wss://your-domain.com/exotel/stream/{call_id}`.", bullet_style))
    story.append(Paragraph("• <b>Audio Exchange</b>: Exotel streams 8kHz mulaw audio chunks. Python FastAPI converts these to 16kHz PCM, passes them to Deepgram/Gemini, and returns the ElevenLabs AI voice back over WebSocket.", bullet_style))

    story.append(Paragraph("FastAPI Integration Code (app/api/exotel.py):", h2_style))
    story.append(Paragraph("""# app/api/exotel.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.call_orchestrator import CallOrchestrator

router = APIRouter(prefix="/exotel", tags=["Exotel Telephony"])

@router.websocket("/stream/{call_id}")
async def exotel_voice_stream(websocket: WebSocket, call_id: str):
    await websocket.accept()
    orchestrator = CallOrchestrator(call_id=call_id)
    await orchestrator.start()
    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            await orchestrator.process_audio_chunk(audio_chunk)
    except WebSocketDisconnect:
        await orchestrator.close()""", code_style))

    story.append(Spacer(1, 10))

    # APPROACH 2: AIRTEL CORPORATE SIP TRUNK
    story.append(Paragraph("3. Approach 2: Airtel Corporate SIP Trunking + FreeSWITCH / LiveKit Gateway", h1_style))
    airtel_overview = (
        "<b>Overview</b>: Bharti Airtel provisions a dedicated enterprise digital SIP channel trunk into your server infrastructure via a Session Border Controller (SBC). "
        "We host an open-source <b>FreeSWITCH Docker container</b> or <b>LiveKit SIP Gateway</b> to handle the telephony channel."
    )
    story.append(Paragraph(airtel_overview, body_style))

    airtel_diagram = """[FastAPI Backend (app/services/call_dispatcher.py)]
      │  1. Triggers ESL Command to FreeSWITCH Container
      ▼
[FreeSWITCH Docker / LiveKit SIP Gateway (SBC Container)]
      │  2. Dials Customer via Airtel Enterprise SIP Channel
      ▼
[Customer's Mobile Phone] (Answers Call)
      │  3. FreeSWITCH Bridges Live RTP Audio Stream to Python AI Agent
      ▼
[Python AI Voice Agent (webrtc_agent.py)] ◄──► [Deepgram STT ➔ Gemini LLM ➔ ElevenLabs/Aura TTS]"""
    story.append(Paragraph(airtel_diagram, diagram_style))

    story.append(Paragraph("How It Works technically:", h2_style))
    story.append(Paragraph("• <b>SIP Trunk Connection</b>: Airtel routes raw SIP signaling to your FreeSWITCH server IP over a dedicated IP pipe.", bullet_style))
    story.append(Paragraph("• <b>RTP Media Relay</b>: FreeSWITCH handles G.711 / G.722 RTP audio packet decoding natively and pipes the raw PCM stream directly into Python `webrtc_agent.py`.", bullet_style))
    story.append(Paragraph("• <b>Lowest Cost at Scale</b>: Since you own the FreeSWITCH container, call rates are just ₹0.30/min flat rate with zero platform middleman fees.", bullet_style))

    story.append(Paragraph("FreeSWITCH Trigger Code (app/services/freeswitch_service.py):", h2_style))
    story.append(Paragraph("""# app/services/freeswitch_service.py
import httpx

async def trigger_airtel_sip_call(phone_number: str, call_id: str):
    url = "http://freeswitch-container:8081/api/originate"
    payload = {
        "gateway": "airtel_sip_trunk",
        "destination": phone_number,
        "call_id": call_id
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=payload)
        return res.json()""", code_style))

    story.append(Spacer(1, 10))

    # APPROACH 3: TWILIO VOICE API
    story.append(Paragraph("4. Approach 3: Twilio Voice TwiML Media Streams", h1_style))
    twilio_overview = (
        "<b>Overview</b>: Twilio is the global leader in cloud communications. It provides worldwide phone numbers and TwiML WebSockets (`<Connect><Stream>`) "
        "to stream phone call audio directly into Python WebSockets."
    )
    story.append(Paragraph(twilio_overview, body_style))

    twilio_diagram = """[FastAPI Backend (app/services/call_dispatcher.py)]
      │  1. HTTP POST Call Request (Twilio REST API)
      ▼
[Twilio Global Voice Cloud]
      │  2. Dials Customer Phone Number
      ▼
[Customer's Mobile Phone] (Answers Call)
      │  3. Twilio Fetches TwiML & Opens WebSockets to FastAPI
      ▼
[FastAPI /twilio/stream (WebSocket Endpoint)] ◄──► [Deepgram STT ➔ Gemini LLM ➔ ElevenLabs TTS]"""
    story.append(Paragraph(twilio_diagram, diagram_style))

    story.append(Paragraph("How It Works technically:", h2_style))
    story.append(Paragraph("• <b>TwiML Webhook</b>: Twilio calls your `/twilio/voice` HTTP endpoint, which responds with TwiML XML instructions to open a WebSockets media stream.", bullet_style))
    story.append(Paragraph("• <b>Audio Format</b>: Twilio streams base64-encoded 8kHz mulaw audio frames inside JSON payload messages.", bullet_style))

    story.append(Paragraph("Twilio Integration Code (app/api/twilio.py):", h2_style))
    story.append(Paragraph("""# app/api/twilio.py
from fastapi import APIRouter, Response, WebSocket

router = APIRouter(prefix="/twilio", tags=["Twilio Telephony"])

@router.post("/voice")
async def twilio_voice():
    twiml_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Connect>
            <Stream url="wss://your-domain.com/twilio/stream" />
        </Connect>
    </Response>'''
    return Response(content=twiml_xml, media_type="application/xml")""", code_style))

    story.append(Spacer(1, 10))

    # 5. COST COMPARISON & COMPARATIVE ANALYSIS
    story.append(Paragraph("5. Comprehensive Pricing & Feature Comparison Matrix", h1_style))
    story.append(Paragraph("Cost modeled for <b>100 calls/day × 30 days = 3,000 calls / 12,000 call minutes per month</b>:", body_style))

    comparison_data = [
        [
            Paragraph("<b>Feature / Metric</b>", body_style),
            Paragraph("<b>Approach 1: Exotel Cloud</b>", body_style),
            Paragraph("<b>Approach 2: Airtel SIP Trunk</b>", body_style),
            Paragraph("<b>Approach 3: Twilio Voice</b>", body_style)
        ],
        [
            Paragraph("Target Market", body_style),
            Paragraph("India (Native Cloud)", body_style),
            Paragraph("India Enterprise", body_style),
            Paragraph("Global / International", body_style)
        ],
        [
            Paragraph("Telephony Rate / Min", body_style),
            Paragraph("₹0.60 / min ($0.0071)", body_style),
            Paragraph("<b>₹0.30 / min ($0.0036)</b>", body_style),
            Paragraph("₹1.52 / min ($0.0180)", body_style)
        ],
        [
            Paragraph("Monthly Infrastructure", body_style),
            Paragraph("₹2,000 / mo", body_style),
            Paragraph("₹2,500 / mo", body_style),
            Paragraph("₹97 / mo", body_style)
        ],
        [
            Paragraph("Total Telephony (12k Mins)", body_style),
            Paragraph("₹9,200 INR ($109.50)", body_style),
            Paragraph("<b>₹6,100 INR ($72.60)</b>", body_style),
            Paragraph("₹18,241 INR ($217.15)", body_style)
        ],
        [
            Paragraph("AI Pipeline (STT+LLM+TTS)", body_style),
            Paragraph("₹10,634 INR ($126.60)", body_style),
            Paragraph("₹10,634 INR ($126.60)", body_style),
            Paragraph("₹10,634 INR ($126.60)", body_style)
        ],
        [
            Paragraph("<b>TOTAL MONTHLY COST</b>", body_style),
            Paragraph("<b>₹19,859 INR ($236.40)</b>", body_style),
            Paragraph("<b>₹16,759 INR ($199.50)</b>", body_style),
            Paragraph("<b>₹28,900 INR ($344.05)</b>", body_style)
        ],
        [
            Paragraph("<b>Effective Per Min Cost</b>", body_style),
            Paragraph("<b>~₹1.65 INR / min</b>", body_style),
            Paragraph("<b>~₹1.39 INR / min</b>", body_style),
            Paragraph("<b>~₹2.40 INR / min</b>", body_style)
        ],
        [
            Paragraph("Setup Complexity", body_style),
            Paragraph("Low (Pure API)", body_style),
            Paragraph("Medium (FreeSWITCH)", body_style),
            Paragraph("Low (Pure API)", body_style)
        ]
    ]

    t_comp = Table(comparison_data, colWidths=[120, 134, 134, 134])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#ECFDF5")),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # Final Summary Recommendation
    story.append(Paragraph("6. Final Recommendation", h1_style))
    final_rec = (
        "1. <b>Recommended Primary Option for Indian Market</b>: <b>Exotel Cloud Telephony</b>. "
        "It provides the ideal balance of zero telephony hardware maintenance, fast FastAPI WebSocket integration, and a low cost of <b>₹1.65/min total</b>.<br/>"
        "2. <b>Recommended Option for Maximum Scaling & Lowest Rate</b>: <b>Airtel Corporate SIP Trunk + FreeSWITCH</b> (<b>₹1.39/min total</b>)."
    )
    story.append(Paragraph(final_rec, body_style))

    doc.build(story)
    print(f"Detailed PDF Report generated successfully at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
