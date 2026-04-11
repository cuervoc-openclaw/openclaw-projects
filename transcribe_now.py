#!/usr/bin/env python3
# Script simple para transcribir audio inmediato

import subprocess
import json
import os
import sys

# Ruta del audio
audio_path = "/home/cuervoc/.openclaw/media/inbound/588c97cf-e3f1-4303-9f16-bb6dde65043b.ogg"
model_path = "/home/cuervoc/vosk-models/vosk-model-small-es-0.42"

print("🎤 TRANSCRIBIENDO AUDIO...")
print(f"📁 Audio: {audio_path}")
print(f"🤖 Modelo: {model_path}")

# 1. Convertir OGG a WAV
print("1. 🔄 Convirtiendo OGG → WAV...")
wav_path = "/tmp/audio_temp.wav"

try:
    # Usar ffmpeg para convertir
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-ar", "16000",      # 16kHz sample rate
        "-ac", "1",          # mono
        "-y",                # sobrescribir
        wav_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error ffmpeg: {result.stderr}")
        sys.exit(1)
    
    print("✅ Conversión completada")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# 2. Verificar si el archivo WAV existe
if not os.path.exists(wav_path):
    print("❌ Archivo WAV no creado")
    sys.exit(1)

print(f"✅ WAV creado: {wav_path} ({os.path.getsize(wav_path)} bytes)")

# 3. Transcribir con Vosk
print("2. 🤖 Transcribiendo con Vosk...")

try:
    import vosk
    import wave
    
    # Cargar modelo
    if not os.path.exists(model_path):
        print(f"❌ Modelo Vosk no encontrado en: {model_path}")
        sys.exit(1)
    
    model = vosk.Model(model_path)
    
    # Abrir archivo WAV
    wf = wave.open(wav_path, "rb")
    
    # Verificar formato
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
        print("❌ Formato WAV no compatible: debe ser mono, 16-bit, 16kHz")
        sys.exit(1)
    
    # Crear reconocedor
    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    
    # Transcribir
    transcription = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'text' in result and result['text']:
                transcription += result['text'] + " "
    
    # Resultado final
    final_result = json.loads(rec.FinalResult())
    if 'text' in final_result and final_result['text']:
        transcription += final_result['text']
    
    wf.close()
    
    # Limpiar transcripción
    transcription = transcription.strip()
    
    if transcription:
        print("\n" + "="*50)
        print("📝 TRANSCRIPCIÓN COMPLETADA:")
        print("="*50)
        print(f"\n{transcription}\n")
        print("="*50)
        
        # Guardar en archivo
        with open("/tmp/transcripcion.txt", "w") as f:
            f.write(transcription)
        print(f"\n💾 Guardado en: /tmp/transcripcion.txt")
        
    else:
        print("❌ No se pudo transcribir (audio silencioso o muy corto)")
    
except ImportError:
    print("❌ Vosk no instalado. Instala con: pip install vosk")
except Exception as e:
    print(f"❌ Error en transcripción: {e}")

# 4. Limpiar archivo temporal
if os.path.exists(wav_path):
    os.remove(wav_path)
    print(f"\n🧹 Archivo temporal eliminado: {wav_path}")