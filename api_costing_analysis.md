# NexaVoice API Costing Analysis (Monthly Projection)

> [!NOTE]
> **Operating Assumptions:**
> - **Total Calls Per Day:** 1,000 calls 
> - **Days Per Month:** 30 days
> - **Total Calls Per Month:** 30,000 calls
> - **Average Call Duration:** 4 minutes (240 seconds)
> - **Total Monthly Call Minutes:** 120,000 minutes
> - **Concurrency:** 10 concurrent active calls
> 
> *As requested, the granular per-call and per-minute breakdowns have been abstracted to focus entirely on the aggregate Monthly Operational Cost.*

---

## 1. Deepgram (Speech-to-Text Engine)
Deepgram is used to transcribe the customer's live speech into text.
- **Model:** Nova-2 (Standard conversational AI model)
- **Billing Metric:** Per minute of audio processed.
- **Volume:** 120,000 total minutes/month.
- **Rate:** ~$0.0043 per minute.
- **Estimated Monthly Cost:** **$516.00**

## 2. ElevenLabs (Text-to-Speech Engine)
ElevenLabs is used to generate the ultra-realistic human voice for the AI.
- **Billing Metric:** Per 1,000 characters generated.
- **Usage Estimate:** Assuming a balanced 4-minute conversation where the AI speaks 50% of the time, the AI will output roughly 250-300 words (~1,500 characters) per call.
- **Volume:** 30,000 calls × 1,500 characters = 45,000,000 characters/month.
- **Rate:** ~$0.18 per 1,000 characters (Enterprise / Scale tier).
- **Estimated Monthly Cost:** **$8,100.00** 
*(Note: ElevenLabs is the most expensive premium component. Consider switching to Deepgram Aura TTS or Play.ht if cost-reduction is needed in the future).*

## 3. Google Gemini (Conversational LLM)
Gemini handles the intent extraction, CRM updates, and conversation generation.
- **Model:** Gemini 1.5 Flash (or 2.0 Flash)
- **Billing Metric:** Per 1 Million Tokens (Input/Output).
- **Usage Estimate:** A 4-minute call will have around 10 conversational turns. With the system prompt and conversation history, a single call will consume roughly `5,000 Input Tokens` and `500 Output Tokens`.
- **Volume:** 
  - Input: 30,000 calls × 5,000 = 150 Million Tokens.
  - Output: 30,000 calls × 500 = 15 Million Tokens.
- **Rate:** $0.075 per 1M Input Tokens / $0.30 per 1M Output Tokens.
- **Estimated Monthly Cost:** **$15.75**

## 4. Tata Smartflo / Telephony (SIP Trunk)
The telephony provider handling the actual phone network routing (PSTN).
- **Billing Metric:** Per minute of outbound/inbound calling.
- **Volume:** 120,000 minutes/month.
- **Rate:** Assuming standard Indian outbound rates of ~₹1.50 INR ($0.018) per minute.
- **Estimated Monthly Cost:** **$2,160.00**

## 5. AWS S3 (Call Recording Storage)
AWS is used for storing the generated audio logs and MP3 recordings.
- **Billing Metric:** Per GB of storage.
- **Volume:** A compressed 4-minute MP3 audio file is ~1 MB. 30,000 calls = ~30 GB/month.
- **Rate:** $0.023 per GB (S3 Standard).
- **Estimated Monthly Cost:** **$0.69**

---

## 📊 Total Monthly Cost Summary

| API / Service | Core Function | Monthly Cost (USD) | Monthly Cost (INR Approx)* |
| :--- | :--- | :--- | :--- |
| **ElevenLabs** | Voice Generation (TTS) | $8,100.00 | ₹6,72,000 |
| **Tata Smartflo** | Phone Network | $2,160.00 | ₹1,80,000 |
| **Deepgram** | Speech Transcription | $516.00 | ₹42,800 |
| **Google Gemini** | AI Brain / LLM | $15.75 | ₹1,300 |
| **AWS** | Storage / Logs | $0.69 | ₹57 |
| **TOTAL** | | **$10,792.44** | **~₹8,96,157 / month** |

> [!WARNING]
> **Cost Optimization Alert**
> ElevenLabs accounts for nearly **75%** of your total monthly infrastructure cost. If scaling beyond 1,000 calls/day, you should strongly evaluate migrating the Text-to-Speech engine to **Deepgram Aura** or **Amazon Polly**, which would reduce the TTS monthly cost from $8,100 down to roughly $1,800.
