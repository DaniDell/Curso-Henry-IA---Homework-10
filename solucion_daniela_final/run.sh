#!/bin/bash
# Script para preparar y ejecutar el Asistente Virtual de CASA DEL MUEBLE

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Asistente Virtual CASA DEL MUEBLE - Iniciando... ===${NC}\n"

# 1. Verificar entorno virtual
echo -e "${YELLOW}Verificando entorno virtual...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python -m venv venv
    source venv/bin/activate
    pip install -r solucion_daniela/requirements.txt
else
    source venv/bin/activate
fi
echo -e "${GREEN}Entorno virtual activado.${NC}\n"

# 2. Preparar la base de conocimientos
echo -e "${YELLOW}Preparando base de conocimientos...${NC}"
python -m solucion_daniela.prepare_knowledge_base
echo -e "${GREEN}Base de conocimientos preparada.${NC}\n"

# 3. Ejecutar el indexador
echo -e "${YELLOW}Indexando base de conocimientos...${NC}"
python -m solucion_daniela.indexer
echo -e "${GREEN}Indexación completada.${NC}\n"

# 4. Iniciar el asistente
echo -e "${YELLOW}Iniciando el asistente virtual...${NC}\n"
python -m solucion_daniela.main
