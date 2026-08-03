import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)

def build_pdf(filename="Telephony_Providers_Comparison_and_Implementation_Report.pdf"):
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
    PRIMARY = colors.HexColor("#1E3A8A")   # Deep Navy Blue
    SECONDARY = colors.HexColor("#0D9488") # Teal
    DARK_TEXT = colors.HexColor("#1F2937") # Slate Dark
    LIGHT_BG = colors.HexColor("#F3F4F6")  # Soft Gray
    ACCENT = colors.HexColor("#3B82F6")    # Bright Blue
    BORDER_COLOR = colors.HexColor("#E5E7EB")

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
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
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1F2937"),
        backColor=colors.HexColor("#F9FAFB"),
        borderColor=colors.HexColor("#D1D5DB"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    story = []

    # Title & Executive Header
    story.append(Paragraph("Telephony Provider Costing & Technical Implementation Analysis", title_style))
    story.append(Paragraph("Comparison of Airtel Corporate SIP Trunking vs. Exotel Cloud Telephony vs. Twilio Voice API for AI Calling Platform | 100 Calls/Day (12,000 Mins/Month)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=12))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    exec_summary_text = (
        "This report evaluates three PSTN telephony integration strategies to deliver AI voice streams directly into a customer's phone ear receiver without requiring any application on the customer's device. "
        "The evaluation models a standard operational load of <b>100 calls/day</b> across <b>30 days/month</b> with an average duration of <b>4 minutes per call</b> (Total volume: <b>3,000 calls / 12,000 call minutes per month</b>)."
    )
    story.append(Paragraph(exec_summary_text, body_style))

    # Key Comparison Table
    story.append(Paragraph("1. Monthly Cost Breakdown Comparison (in INR ₹ & USD $)", h1_style))
    
    table_data = [
        [
            Paragraph("<b>Cost Parameter</b>", body_style),
            Paragraph("<b>Airtel Corporate SIP Trunk</b>", body_style),
            Paragraph("<b>Exotel Cloud Telephony</b>", body_style),
            Paragraph("<b>Twilio Voice API</b>", body_style)
        ],
        [
            Paragraph("Outbound Call Rate / Min", body_style),
            Paragraph("₹0.30 / min ($0.0036)", body_style),
            Paragraph("₹0.60 / min ($0.0071)", body_style),
            Paragraph("₹1.52 / min ($0.0180)", body_style)
        ],
        [
            Paragraph("Monthly Trunk / Rental Fee", body_style),
            Paragraph("₹2,500 ($30.00)", body_style),
            Paragraph("₹2,000 ($23.80)", body_style),
            Paragraph("₹97 ($1.15)", body_style)
        ],
        [
            Paragraph("<b>Telephony Cost (12k Mins)</b>", body_style),
            Paragraph("<b>₹6,100 ($72.60)</b>", body_style),
            Paragraph("<b>₹9,200 ($109.50)</b>", body_style),
            Paragraph("<b>₹18,241 ($217.15)</b>", body_style)
        ],
        [
            Paragraph("AI Pipeline (STT+LLM+TTS)", body_style),
            Paragraph("₹10,634 ($126.60)", body_style),
            Paragraph("₹10,634 ($126.60)", body_style),
            Paragraph("₹10,634 ($126.60)", body_style)
        ],
        [
            Paragraph("<b>Total Monthly Cost (3k Calls)</b>", body_style),
            Paragraph("<b>₹16,734 INR ($199.20)</b>", body_style),
            Paragraph("<b>₹19,834 INR ($236.10)</b>", body_style),
            Paragraph("<b>₹28,875 INR ($343.75)</b>", body_style)
        ],
        [
            Paragraph("<b>Cost Per 4-Min Call</b>", body_style),
            Paragraph("<b>₹5.58 INR ($0.066)</b>", body_style),
            Paragraph("<b>₹6.61 INR ($0.078)</b>", body_style),
            Paragraph("<b>₹9.62 INR ($0.114)</b>", body_style)
        ],
        [
            Paragraph("<b>Effective Cost Per Min</b>", body_style),
            Paragraph("<b>₹1.39 INR / min</b>", body_style),
            Paragraph("<b>₹1.65 INR / min</b>", body_style),
            Paragraph("<b>₹2.40 INR / min</b>", body_style)
        ]
    ]

    t = Table(table_data, colWidths=[130, 130, 130, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#F0FDF4")),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Financial Analysis & Key Insights
    story.append(Paragraph("Key Financial Takeaways:", h2_style))
    story.append(Paragraph("• <b>Airtel Corporate SIP Trunking</b> is the most cost-effective solution for high-volume Indian operations, yielding a total cost of <b>₹1.39/min</b> (~67% cheaper than Twilio).", bullet_style))
    story.append(Paragraph("• <b>Exotel</b> provides the best balance of low Indian call rates (<b>₹1.65/min</b> total) with zero physical server hardware maintenance.", bullet_style))
    story.append(Paragraph("• <b>Twilio Voice API</b> is the most expensive for Indian calling (<b>₹2.40/min</b> total) due to international USD-denominated tariffs, but offers global deployment simplicity.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=4, spaceAfter=10))

    # Implementation Methodology Section
    story.append(Paragraph("2. Technical Implementation Architecture for Each Option", h1_style))

    # Option A: Airtel Corporate SIP Trunking
    story.append(Paragraph("Approach A: Airtel Corporate SIP Trunk (Self-Hosted FreeSWITCH / LiveKit SIP)", h2_style))
    airtel_impl = (
        "<b>Architecture</b>: Airtel provisions a Session Border Controller (SBC) SIP connection directly into your cloud server. "
        "We run an open-source <b>FreeSWITCH</b> container or <b>LiveKit SIP Gateway</b> to accept the SIP trunk.<br/>"
        "<b>Call Flow</b>:<br/>"
        "1. Backend triggers call via FreeSWITCH ESL (Event Socket Library) command.<br/>"
        "2. FreeSWITCH dials customer phone number via Airtel SIP Trunk.<br/>"
        "3. When call answers, FreeSWITCH streams 8kHz/16kHz PCM audio over WebSocket/WebRTC to Python FastAPI.<br/>"
        "4. Python AI Agent processes speech (Deepgram STT ➔ Gemini LLM ➔ ElevenLabs/Aura TTS) and streams voice back to FreeSWITCH."
    )
    story.append(Paragraph(airtel_impl, body_style))
    story.append(Paragraph("""# FreeSWITCH ESL Call Trigger Example (Python)
from ESL import *
con = ESLconnection('127.0.0.1', '8021', 'ClueCon')
cmd = "bgapi originate {sip_auto_answer=true}sofia/gateway/airtel/+919876543210 &socket(127.0.0.1:8086 full)"
e = con.api(cmd)""", code_style))

    # Option B: Exotel Cloud Telephony
    story.append(Paragraph("Approach B: Exotel Voice Stream API (India Cloud Telephony)", h2_style))
    exotel_impl = (
        "<b>Architecture</b>: Exotel exposes a cloud REST API to trigger calls and a bi-directional WebSocket Voice Stream API.<br/>"
        "<b>Call Flow</b>:<br/>"
        "1. FastAPI calls Exotel REST API `POST /v1/Accounts/{SID}/Calls/connect.json`.<br/>"
        "2. Exotel dials customer phone number.<br/>"
        "3. Upon connection, Exotel opens a WebSocket connection to `wss://your-domain.com/exotel/stream`.<br/>"
        "4. Python FastAPI receives audio chunks in 8kHz mulaw format, decodes to PCM, feeds to Gemini/Deepgram, and sends audio replies back."
    )
    story.append(Paragraph(exotel_impl, body_style))
    story.append(Paragraph("""# Exotel Outbound Call Dispatch (Python FastAPI)
import httpx
async def trigger_exotel_call(phone_number: str, call_id: str):
    url = f"https://api.exotel.com/v1/Accounts/{EXOTEL_SID}/Calls/connect.json"
    data = {
        "From": phone_number,
        "CallerId": EXOTEL_VIRTUAL_NUMBER,
        "Url": f"http://your-domain.com/exotel/passthru?call_id={call_id}"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, data=data, auth=(EXOTEL_API_KEY, EXOTEL_TOKEN))
        return res.json()""", code_style))

    # Option C: Twilio Voice API
    story.append(Paragraph("Approach C: Twilio TwiML Voice Media Stream", h2_style))
    twilio_impl = (
        "<b>Architecture</b>: Twilio Voice API using TwiML `<Connect><Stream>` for bi-directional WebSockets.<br/>"
        "<b>Call Flow</b>:<br/>"
        "1. FastAPI calls `twilio_client.calls.create(to=phone_number, from_=twilio_number, url=twiml_url)`.<br/>"
        "2. Twilio dials customer phone number.<br/>"
        "3. When answered, Twilio fetches TwiML XML returning `<Connect><Stream url='wss://your-domain.com/twilio/stream'/></Connect>`.<br/>"
        "4. Twilio opens WebSocket and streams audio payload in base64 mulaw to FastAPI."
    )
    story.append(Paragraph(twilio_impl, body_style))
    story.append(Paragraph("""# Twilio TwiML Router Endpoint (Python FastAPI)
from fastapi import APIRouter, Response

@router.post("/twilio/voice")
async def twilio_voice_webhook():
    xml_response = '''<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Connect>
            <Stream url="wss://your-domain.com/twilio/stream" />
        </Connect>
    </Response>'''
    return Response(content=xml_response, media_type="application/xml")""", code_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Summary Recommendation", h1_style))
    recommendation_text = (
        "1. <b>For Immediate Low-Complexity Indian PSTN (Best Balance)</b>: Implement <b>Exotel Voice Stream API</b>. "
        "It requires zero server telephony hardware, works with standard Indian phone numbers, costs <b>~₹1.65/min total</b>, and plugs directly into Python FastAPI via WebSockets.<br/>"
        "2. <b>For Maximum Scale & Lowest Cost</b>: Deploy <b>Airtel Corporate SIP Trunk + FreeSWITCH</b> in Docker. "
        "This achieves <b>~₹1.39/min total cost</b> with complete infrastructure control.<br/>"
        "3. <b>For International Calling</b>: Use <b>Twilio Voice API</b>."
    )
    story.append(Paragraph(recommendation_text, body_style))

    doc.build(story)
    print(f"PDF Report generated successfully at: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    build_pdf()
