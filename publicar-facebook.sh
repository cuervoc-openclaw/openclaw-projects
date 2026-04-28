#!/bin/bash

# Script para publicar contenido en Facebook sobre servicios de construcción
# Autor: Sistema OpenClaw
# Fecha: $(date)

# Configuración
PAGINA_FACEBOOK="MiEmpresaConstruccion"
TOKEN_ACCESO="TU_TOKEN_DE_ACCESO_AQUI"
TELEFONO_WHATSAPP="+569XXXXXXXX"
CARPETA_IMAGENES="./imagenes_construccion"

# Seleccionar post aleatorio
POSTS=(
    "facebook_post_construccion.txt"
    "facebook_post_construccion_v2.txt" 
    "facebook_post_construccion_v3.txt"
    "facebook_post_construccion_v4.txt"
)

POST_SELECCIONADO=${POSTS[$RANDOM % ${#POSTS[@]}]}

# Leer contenido del post
if [ -f "$POST_SELECCIONADO" ]; then
    CONTENIDO=$(cat "$POST_SELECCIONADO")
    echo "Publicando post: $POST_SELECCIONADO"
else
    echo "Error: No se encontró el archivo $POST_SELECCIONADO"
    exit 1
fi

# Seleccionar imagen aleatoria (si existe la carpeta)
if [ -d "$CARPETA_IMAGENES" ]; then
    IMAGENES=($CARPETA_IMAGENES/*.jpg $CARPETA_IMAGENES/*.png)
    if [ ${#IMAGENES[@]} -gt 0 ]; then
        IMAGEN_SELECCIONADA=${IMAGENES[$RANDOM % ${#IMAGENES[@]}]}
        echo "Imagen seleccionada: $IMAGEN_SELECCIONADA"
    fi
fi

# Reemplazar placeholder de teléfono
CONTENIDO=${CONTENIDO//+56 9 XXXX XXXX/$TELEFONO_WHATSAPP}

# Mostrar contenido a publicar
echo "=== CONTENIDO DEL POST ==="
echo "$CONTENIDO"
echo "=========================="

# Aquí iría la lógica real para publicar en Facebook
# Ejemplo con curl (comentado porque necesita token real):
# curl -X POST \
#   -F "message=$CONTENIDO" \
#   -F "access_token=$TOKEN_ACCESO" \
#   "https://graph.facebook.com/v12.0/$PAGINA_FACEBOOK/feed"

echo ""
echo "✅ Post listo para publicar en Facebook"
echo "📱 Contacto WhatsApp: $TELEFONO_WHATSAPP"
echo "🕐 Publicado el: $(date '+%d/%m/%Y %H:%M')"

# Registrar en log
echo "$(date '+%Y-%m-%d %H:%M:%S') - Post publicado: $POST_SELECCIONADO" >> facebook_posts.log