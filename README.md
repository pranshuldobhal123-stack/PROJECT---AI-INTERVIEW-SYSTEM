# PROJECT---AI-INTERVIEW-SYSTEM

A real-time AI interview platform with live voice interaction, automatic question generation, and webcam-based proctoring.

## 🚀 Overview

This project includes:

- **Python backend** using FastAPI and WebSockets
- **Speech transcription** via Deepgram
- **AI response generation** using Groq LLM
- **Text-to-speech** output with Microsoft Edge TTS
- **Next.js frontend** with live microphone input and audio playback
- **Client-side proctoring** using MediaPipe face landmark detection

## 📁 Project structure

The application files are located inside the nested `ai-interview-system/` folder.

- `ai-interview-system/backend/`
  - `main.py` — FastAPI WebSocket server
  - `services/llm.py` — Groq LLM chat integration
  - `services/tts.py` — edge-tts audio generation
  - `.env` — environment variables for Groq API key (not committed)

- `ai-interview-system/frontend/`
  - `app/page.tsx` — landing page and session startup
  - `components/InterviewSession.tsx` — live microphone streaming and WebSocket client
  - `components/ProctorView.tsx` — camera-based face/gaze detection
  - `package.json` — Next.js and frontend dependencies

## ✨ Features

- **Real-time audio interview**: candidate speech is streamed from browser to backend
- **Speech-to-text**: captured audio is transcribed with Deepgram
- **AI interviewer**: prompts are sent to a Groq LLM and conversational replies are generated
- **Text-to-speech feedback**: the backend returns audio for AI responses
- **Proctoring UI**: webcam gaze and face detection via MediaPipe
- **Modern frontend**: built with Next.js 16 and React 19

## 🧠 Architecture

### Frontend

1. User clicks `Initialize Session`
2. Browser captures microphone audio with `MediaRecorder`
3. Audio chunks are streamed to backend WebSocket at `ws://localhost:8000/ws/interview/user1`
4. The frontend receives:
   - JSON text events for transcript and status
   - binary audio blobs for TTS playback
5. The proctoring panel uses MediaPipe face landmark detection to warn on gaze aversion or missing face.

### Backend

1. FastAPI opens a WebSocket on `/ws/interview/{client_id}`
2. Backend receives audio bytes from client
3. Deepgram transcribes audio into text
4. Conversation history is sent to Groq LLM via `services/llm.py`
5. Generated AI text is converted to speech with `edge-tts`
6. Backend streams response text and MP3 audio back to frontend

## ⚙️ Setup

### Backend

```bash
cd ai-interview-system/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Set environment variables in `ai-interview-system/backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key
```

Run the backend server:

```bash
python main.py
```

### Frontend

```bash
cd ai-interview-system/frontend
npm install
npm run dev
```

Open the browser at the port shown by Next.js, then start the interview session.

## 🛡️ Security & notes

- `.env` files should never be committed to source control
- The backend currently accepts `allow_origins=["*"]` for development only
- For production, secure the WebSocket connection and restrict CORS

## 📌 Important

- The repository default branch is `main`
- The root README points to the nested project folder structure
- If you want, I can also help flatten the repository so `backend/` and `frontend/` are at the root level
