# websocket_server.py
import asyncio
import websockets
import openai
import tempfile
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

async def handle_audio(websocket, path):
    while True:
        try:
            # クライアントからの音声データを受信
            audio_data = await websocket.recv()
            
            # 一時ファイルとして保存
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_data)
                audio_path = tmp_file.name

            try:
                # WhisperAPIに送信
                with open(audio_path, "rb") as audio_file:
                    transcript = openai.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="ja"
                    )
                
                if transcript.text.strip():
                    await websocket.send(transcript.text)
                
            finally:
                # 一時ファイルを削除
                if os.path.exists(audio_path):
                    os.unlink(audio_path)
            
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error: {e}")
            await websocket.send(f"Error: {str(e)}")

async def main():
    print("Starting WebSocket server...")
    async with websockets.serve(handle_audio, "0.0.0.0", 8765, ping_interval=None):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())