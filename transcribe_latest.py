#!/usr/bin/env python3
"""
Transcripción del último audio recibido
"""

import os
import subprocess
import json
import tempfile

def convert_ogg_to_wav(ogg_path, wav_path):
    """Convertir OGG a WAV usando ffmpeg"""
    try:
        cmd = [
            'ffmpeg',
            '-i', ogg_path,
            '-ar', '16000',
            '-ac', '1',
            '-y',
            wav_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception:
        return False

def transcribe_wav(wav_path):
    """Transcribir WAV usando Vosk"""
    try:
        from vosk import Model, KaldiRecognizer
        import wave
        
        model_path = "/home/cuervoc/vosk-models/vosk-model-small-es-0.42"
        model = Model(model_path)
        
        wf = wave.open(wav_path, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        
        transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                transcription += result.get('text', '') + " "
        
        final = json.loads(rec.FinalResult())
        transcription += final.get('text', '')
        
        wf.close()
        return transcription.strip()
    except Exception:
        return None

def main():
    # Último audio recibido
    audio_path = "/home/cuervoc/.openclaw/media/inbound/bcb40f84-51c2-491c-bcdf-aa77a91d7612.ogg"
    
    if not os.path.exists(audio_path):
        print("❌ Audio no encontrado")
        return
    
    print(f"🎤 Audio: {os.path.basename(audio_path)} ({os.path.getsize(audio_path)/1024:.1f} KB)")
    
    # Crear WAV temporal
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name
    
    try:
        # Convertir
        print("🔄 Convirtiendo...")
        if not convert_ogg_to_wav(audio_path, wav_path):
            print("❌ Error en conversión")
            return
        
        # Transcribir
        print("📝 Transcribiendo...")
        text = transcribe_wav(wav_path)
        
        if text:
            print("\n" + "="*50)
            print("📝 TRANSCRIPCIÓN:")
            print("="*50)
            print(f"\n{text}")
            print("\n" + "="*50)
            
            # Guardar
            with open("/home/cuervoc/.openclaw/workspace/ultima_transcripcion.txt", "w") as f:
                f.write(text)
        else:
            print("❌ No se pudo transcribir")
            
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)

if __name__ == "__main__":
    main()