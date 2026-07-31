import os
import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from services.llm import get_ai_response
from services.tts import generate_audio
from deepgram import DeepgramClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for simple session history
sessions = {}

@app.websocket("/ws/interview/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    sessions[client_id] = [] # Reset history
    
    # Initialize Deepgram
    deepgram = DeepgramClient()

    try:
        while True:
            # 1. Receive Audio Blob from Frontend
            data = await websocket.receive_bytes()
            
            # Ignore ridiculously short audio clicks (prevents empty file errors)
            if len(data) < 1000:
                print("Audio too short, ignoring.")
                continue
            
            try:
                # 2. Transcribe using Deepgram
                response = deepgram.listen.v1.media.transcribe_file(
                    request=data,
                    model="nova-2",
                    smart_format=True
                )
                transcript = response.results.channels[0].alternatives[0].transcript
            except Exception as e:
                print(f"Deepgram skipped a bad audio chunk.")
                continue # Keep the connection alive!

            if not transcript or len(transcript) < 2:
                continue
            
            print(f"Candidate said: {transcript}")
            
            # 3. Get LLM Response
            ai_text, updated_history = await get_ai_response(transcript, sessions[client_id])
            sessions[client_id] = updated_history
            
            print(f"AI Response: {ai_text}")

            # 4. Generate Audio (TTS)
            audio_path = await generate_audio(ai_text)
            
            # 5. Send Audio back to Frontend
            with open(audio_path, "rb") as audio_file:
                audio_data = audio_file.read()
                # Send metadata first
                await websocket.send_text(json.dumps({"text": ai_text}))
                # Send audio bytes
                await websocket.send_bytes(audio_data)
            
            os.remove(audio_path) # Cleanup

    except Exception as e:
        print(f"Connection closed: {e}")