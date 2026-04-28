#!/usr/bin/env python3
"""
Transcripción de audio OGG a texto usando Vosk
"""

import os
import subprocess
import json
import tempfile
from pathlib import Path

def convert_ogg_to_wav(ogg_path, wav_path):
    """Convertir OGG a WAV usando ffmpeg"""
    try:
        cmd = [
            'ffmpeg',
            '-i', ogg_path,
            '-ar', '16000',      # 16kHz sample rate
            '-ac', '1',          # mono
            '-y',                # overwrite
            wav_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Error ffmpeg: {result.stderr[:200]}")
            return False
        return True
    except Exception as e:
        print(f"Error en conversión: {e}")
        return False

def transcribe_audio(wav_path):
    """Transcribir audio WAV usando Vosk"""
    try:
        # Importar Vosk (instalado globalmente)
        from vosk import Model, KaldiRecognizer
        
        # Cargar modelo español
        model_path = "/home/cuervoc/vosk-models/vosk-model-small-es-0.42"
        if not os.path.exists(model_path):
            print(f"❌ Modelo Vosk español no encontrado en: {model_path}")
            # Buscar alternativas
            import glob
            models = glob.glob("/home/cuervoc/vosk-models/*")
            print(f"Modelos disponibles: {models}")
            return None
        
        model = Model(model_path)
        
        # Leer audio
        import wave
        wf = wave.open(wav_path, "rb")
        
        # Verificar formato
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
            print(f"❌ Formato no soportado: {wf.getnchannels()} canales, {wf.getsampwidth()} bytes, {wf.getframerate()} Hz")
            return None
        
        # Crear reconocedor
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        
        # Transcribir
        transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if 'text' in result:
                    transcription += result['text'] + " "
        
        # Obtener resultado final
        final_result = json.loads(rec.FinalResult())
        if 'text' in final_result:
            transcription += final_result['text']
        
        wf.close()
        return transcription.strip()
        
    except ImportError:
        print("❌ Vosk no instalado. Instala: pip install vosk")
        return None
    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        return None

def transcribe_file(audio_path):
    """Transcribir un archivo de audio específico"""
    if not os.path.exists(audio_path):
        print(f"❌ Archivo no encontrado: {audio_path}")
        return None
    
    print(f"🎤 Procesando audio: {os.path.basename(audio_path)}")
    print(f"📏 Tamaño: {os.path.getsize(audio_path) / 1024:.1f} KB")
    
    # Crear archivo temporal WAV
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name
    
    try:
        # 1. Convertir OGG → WAV
        print("🔄 Convirtiendo OGG → WAV...")
        if not convert_ogg_to_wav(audio_path, wav_path):
            print("❌ Falló la conversión")
            return None
        
        print(f"✅ Convertido: {os.path.getsize(wav_path) / 1024:.1f} KB")
        
        # 2. Transcribir
        print("📝 Transcribiendo con Vosk...")
        transcription = transcribe_audio(wav_path)
        
        return transcription
        
    finally:
        # Limpiar archivo temporal
        if os.path.exists(wav_path):
            os.unlink(wav_path)

def main():
    # Ruta del audio recibido (último audio)
    audio_path = "/home/cuervoc/.openclaw/media/inbound/bcb40f84-51c2-491c-bcdf-aa77a91d7612.ogg"
    
    if not os.path.exists(audio_path):
        print(f"❌ Archivo no encontrado: {audio_path}")
        return
    
    print(f"🎤 Procesando audio: {os.path.basename(audio_path)}")
    print(f"📏 Tamaño: {os.path.getsize(audio_path) / 1024:.1f} KB")
    
    # Crear archivo temporal WAV
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name
    
    try:
        # 1. Convertir OGG → WAV
        print("🔄 Convirtiendo OGG → WAV...")
        if not convert_ogg_to_wav(audio_path, wav_path):
            print("❌ Falló la conversión")
            return
        
        print(f"✅ Convertido: {os.path.getsize(wav_path) / 1024:.1f} KB")
        
        # 2. Transcribir
        print("📝 Transcribiendo con Vosk...")
        transcription = transcribe_audio(wav_path)
        
        if transcription:
            print("\n" + "="*60)
            print("🎯 TRANSCRIPCIÓN COMPLETA:")
            print("="*60)
            print(f"\n\"{transcription}\"")
            print("\n" + "="*60)
            
            # Guardar transcripción
            transcript_file = "/home/cuervoc/.openclaw/workspace/ultima_transcripcion.txt"
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(transcription)
            print(f"💾 Guardado en: {transcript_file}")
            
            return transcription
        else:
            print("❌ No se pudo transcribir el audio")
            return None
            
    finally:
        # Limpiar archivo temporal
        if os.path.exists(wav_path):
            os.unlink(wav_path)

if __name__ == "__main__":
    main()