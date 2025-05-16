"""
Script para preparar la base de conocimientos a partir de archivos CSV.
Convierte los datos de productos y FAQs en documentos Markdown para vectorización.
"""
import os
import csv
import pandas as pd
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# Importar configuración desde el mismo directorio
def get_env_var(name, default=None):
    value = os.environ.get(name)
    if value is None:
        if default is not None:
            return default
        raise RuntimeError(f"La variable de entorno {name} no está definida.")
    return value

from config import KNOWLEDGE_DIR, CATALOGO_PATH, FAQS_PATH

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directorios para organizar la base de conocimientos
FAQS_DIR = os.path.join(KNOWLEDGE_DIR, "faqs")
PRODUCTOS_DIR = os.path.join(KNOWLEDGE_DIR, "productos")


def ensure_directories():
    """Crea los directorios necesarios si no existen."""
    os.makedirs(FAQS_DIR, exist_ok=True)
    os.makedirs(PRODUCTOS_DIR, exist_ok=True)
    logger.info(f"Directorios creados: {FAQS_DIR}, {PRODUCTOS_DIR}")


def process_faqs():
    """Procesa el archivo CSV de FAQs y crea documentos markdown individuales."""
    try:
        logger.info(f"Procesando FAQs desde {FAQS_PATH}")
        df = pd.read_csv(FAQS_PATH)
        
        for idx, row in df.iterrows():
            # Crear un documento por cada FAQ
            filename = f"faq_{idx:03d}_{row['Categoría'].lower().replace(' ', '_')}.md"
            filepath = os.path.join(FAQS_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {row['Preguntas del cliente']}\n\n")
                f.write(f"{row['Respuesta optimizada']}\n\n")
                f.write(f"**Categoría:** {row['Categoría']}\n")
                f.write(f"**Etapa:** {row['Etapa del embudo']}\n")
                
                # Agregar información adicional si está disponible
                if 'Objetivo de la respuesta' in row and pd.notna(row['Objetivo de la respuesta']):
                    f.write(f"\n**Objetivo:** {row['Objetivo de la respuesta']}\n")
                
                if 'Siguiente paso sugerido' in row and pd.notna(row['Siguiente paso sugerido']):
                    f.write(f"\n**Siguiente paso sugerido:** {row['Siguiente paso sugerido']}\n")
            
        logger.info(f"Se procesaron {len(df)} FAQs")
    
    except Exception as e:
        logger.error(f"Error al procesar FAQs: {str(e)}")


def clean_value(value):
    """Limpia un valor para asegurar que sea una cadena de texto."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def process_catalogo():
    """Procesa el archivo CSV del catálogo y crea documentos por categorías."""
    try:
        logger.info(f"Procesando catálogo desde {CATALOGO_PATH}")
        
        # Leer el archivo CSV sin headers y definir nombres de columnas según el formato observado
        df = pd.read_csv(CATALOGO_PATH, header=None, dtype=str)
        
        # Agrupar productos por nombre
        products = {}
        current_id = None
        current_name = None
        
        for i, row in df.iterrows():
            # Si las primeras columnas tienen datos, es una entrada principal de producto
            if pd.notna(row[0]) and pd.notna(row[1]):
                current_id = clean_value(row[0])
                current_name = clean_value(row[1])
                
                if current_id not in products:
                    products[current_id] = {
                        "nombre": current_name,
                        "categoria": clean_value(row[2]) if len(row) > 2 else "",
                        "variantes": [],
                        "precios": {}
                    }
            
            # Si la primera columna está vacía pero tenemos un ID actual, es una variante
            elif current_id is not None:
                variante = {}
                for j in range(3, min(9, len(row)), 2):
                    if pd.notna(row[j]) and pd.notna(row[j+1]):
                        prop_name = clean_value(row[j])
                        prop_value = clean_value(row[j+1])
                        variante[prop_name] = prop_value
                
                # Obtener precios si están disponibles
                if len(row) > 9 and pd.notna(row[9]):
                    precios = {
                        "regular": clean_value(row[9]),
                        "cuotas": clean_value(row[10]) if len(row) > 10 and pd.notna(row[10]) else "",
                        "transferencia": clean_value(row[11]) if len(row) > 11 and pd.notna(row[11]) else ""
                    }
                    
                    # Crear una clave única para esta variante basada en sus propiedades
                    variant_key = "_".join([f"{k}_{v}" for k, v in variante.items()])
                    products[current_id]["precios"][variant_key] = precios
                
                if variante:
                    products[current_id]["variantes"].append(variante)
        
        # Agrupar productos por categoría
        categories = {}
        for prod_id, product in products.items():
            cat = product["categoria"]
            if ">" in cat:
                main_cat = cat.split(">")[0].strip()
                sub_cat = cat.split(">")[1].strip() if len(cat.split(">")) > 1 else ""
                cat_key = f"{main_cat}_{sub_cat}" if sub_cat else main_cat
            else:
                cat_key = cat if cat else "Sin_Categoria"
            
            if cat_key not in categories:
                categories[cat_key] = []
            
            categories[cat_key].append((prod_id, product))
        
        # Crear documentos por categoría
        for cat_key, products_list in categories.items():
            filename = f"categoria_{cat_key.lower().replace(' ', '_').replace('/', '_')}.md"
            filepath = os.path.join(PRODUCTOS_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                cat_display = cat_key.replace('_', ' ')
                f.write(f"# Categoría: {cat_display}\n\n")
                
                for prod_id, product in products_list:
                    f.write(f"## {product['nombre']}\n\n")
                    f.write(f"ID: {prod_id}\n\n")
                    
                    if product['categoria']:
                        f.write(f"Categoría: {product['categoria']}\n\n")
                    
                    # Escribir variantes
                    if product['variantes']:
                        f.write("### Variantes disponibles\n\n")
                        for i, variante in enumerate(product['variantes']):
                            if variante:
                                f.write(f"**Variante {i+1}:** ")
                                props = [f"{k}: {v}" for k, v in variante.items()]
                                f.write(", ".join(props))
                                
                                # Añadir precios para esta variante
                                variant_key = "_".join([f"{k}_{v}" for k, v in variante.items()])
                                if variant_key in product['precios']:
                                    precios = product['precios'][variant_key]
                                    f.write("\n\n")
                                    f.write(f"Precio regular: ${precios['regular']}\n")
                                    if precios['cuotas']:
                                        f.write(f"Precio en 6 cuotas sin interés: ${precios['cuotas']}\n")
                                    if precios['transferencia']:
                                        f.write(f"Precio por transferencia: ${precios['transferencia']}\n")
                                
                                f.write("\n\n")
                    
                    f.write("---\n\n")
        
        logger.info(f"Se procesaron {len(products)} productos en {len(categories)} categorías")
    
    except Exception as e:
        logger.error(f"Error al procesar catálogo: {str(e)}")


def process_web_to_markdown(url, output_path):
    """Descarga una página web, la limpia y la convierte a Markdown estructurado."""
    try:
        logger.info(f"Descargando y procesando web: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Puedes ajustar el selector según la estructura de la web
        main_content = soup.find("main") or soup.body
        markdown = md(str(main_content))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"<!-- Fuente: {url} | Fecha: 2025-05-16 -->\n")
            f.write(markdown)
        logger.info(f"Markdown generado en: {output_path}")
    except Exception as e:
        logger.error(f"Error al procesar web {url}: {str(e)}")


def main():
    """Función principal."""
    logger.info("Iniciando preparación de la base de conocimientos")
    ensure_directories()

    # Obtener URL de la web del negocio desde variable de entorno
    web_url = get_env_var("CASAMUEBLE_WEB_URL", "https://casamueble.com.ar/productos")
    process_web_to_markdown(
        url=web_url,
        output_path=os.path.join(PRODUCTOS_DIR, "productos_web.md")
    )

    # Procesar FAQs y catálogo desde CSV
    process_faqs()
    process_catalogo()
    logger.info("Preparación de la base de conocimientos completada")


if __name__ == "__main__":
    main()
