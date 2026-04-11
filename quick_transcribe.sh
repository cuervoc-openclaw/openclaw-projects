#!/bin/bash
# Script rápido para transcribir audio

echo "🎤 SISTEMA STT - TRANSCRIPCIÓN RÁPIDA"
echo "===================================="

AUDIO_PATH="/home/cuervoc/.openclaw/media/inbound/588c97cf-e3f1-4303-9f16-bb6dde65043b.ogg"
MODEL_PATH="/home/cuervoc/vosk-models/vosk-model-small-es-0.42"
WAV_PATH="/tmp/audio_transcribe.wav"

# 1. Verificar archivo
echo "1. 🔍 Verificando audio..."
if [ ! -f "$AUDIO_PATH" ]; then
    echo "   ❌ Audio no encontrado: $AUDIO_PATH"
    exit 1
fi
echo "   ✅ Audio encontrado: $(ls -lh "$AUDIO_PATH" | awk '{print $5}')"

# 2. Verificar modelo Vosk
echo "2. 🤖 Verificando modelo Vosk..."
if [ ! -d "$MODEL_PATH" ]; then
    echo "   ❌ Modelo Vosk no encontrado: $MODEL_PATH"
    echo "   💡 Descarga con: wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
    exit 1
fi
echo "   ✅ Modelo encontrado"

# 3. Convertir OGG → WAV
echo "3. 🔄 Convirtiendo OGG → WAV..."
if command -v ffmpeg > /dev/null 2>&1; then
    ffmpeg -i "$AUDIO_PATH" -ar 16000 -ac 1 -y "$WAV_PATH" 2>/dev/null
    
    if [ $? -eq 0 ] && [ -f "$WAV_PATH" ]; then
        echo "   ✅ Conversión exitosa: $(ls -lh "$WAV_PATH" | awk '{print $5}')"
    else
        echo "   ❌ Error en conversión"
        exit 1
    fi
else
    echo "   ❌ ffmpeg no instalado"
    exit 1
fi

# 4. Mostrar información del audio
echo "4. 📊 Información del audio:"
echo "   Formato: OGG → WAV (16kHz, mono)"
echo "   Ruta original: $AUDIO_PATH"
echo "   Ruta WAV: $WAV_PATH"

# 5. Intentar transcripción con Python si está disponible
echo -e "\n5. 📝 INTENTANDO TRANSCRIPCIÓN..."
if command -v python3 > /dev/null 2>&1; then
    echo "   Python3 disponible"
    
    # Crear script Python temporal
    cat > /tmp/transcribe_temp.py << 'EOF'
import sys
import json
import wave

try:
    import vosk
    has_vosk = True
except ImportError:
    has_vosk = False
    print("Vosk no instalado")

if has_vosk:
    model_path = "/home/cuervoc/vosk-models/vosk-model-small-es-0.42"
    wav_path = "/tmp/audio_transcribe.wav"
    
    try:
        model = vosk.Model(model_path)
        wf = wave.open(wav_path, "rb")
        
        rec = vosk.KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        
        transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if 'text' in result and result['text']:
                    transcription += result['text'] + " "
        
        final_result = json.loads(rec.FinalResult())
        if 'text' in final_result and final_result['text']:
            transcription += final_result['text']
        
        wf.close()
        
        transcription = transcription.strip()
        if transcription:
            print("TRANSCRIPCIÓN:")
            print("=" * 40)
            print(transcription)
            print("=" * 40)
        else:
            print("No se pudo transcribir (audio silencioso)")
            
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Instala Vosk: pip install vosk")
EOF
    
    # Ejecutar transcripción
    echo "   Ejecutando transcripción Python..."
    python3 /tmp/transcribe_temp.py
    
    # Limpiar
    rm -f /tmp/transcribe_temp.py
else
    echo "   ❌ Python3 no disponible"
fi

# 6. Limpiar
echo -e "\n6. 🧹 Limpiando..."
rm -f "$WAV_PATH"
echo "   ✅ Archivos temporales eliminados"

echo -e "\n🎯 TRANSCRIPCIÓN COMPLETADA"
echo "💡 Para transcripciones automáticas, usa el script transcribe_audio.py"