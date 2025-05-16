"""
Script para preparar la base de conocimientos a partir de archivos CSV.
Convierte los datos de productos y FAQs en documentos Markdown para vectorización.
"""
import os
import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

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
        
        # Leer el CSV con manejo especial para texto con comas
        try:
            # Intentar primero leer con comillas dobles para campos con comas
            df = pd.read_csv(FAQS_PATH, quotechar='"', escapechar='\\')
        except Exception as e:
            logger.warning(f"Error con primer método de lectura: {str(e)}")
            try:
                # Segundo intento con parámetros más permisivos
                df = pd.read_csv(FAQS_PATH, sep=',', quotechar='"', doublequote=True, 
                                 escapechar='\\', engine='python')
            except Exception as e2:
                logger.warning(f"Error con segundo método de lectura: {str(e2)}")
                # Último intento: abrir el archivo manualmente y procesarlo línea por línea
                with open(FAQS_PATH, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                # Obtener encabezados de la primera línea
                headers = lines[0].strip().split(',')
                data = []
                
                # Procesar cada línea manualmente
                for line in lines[1:]:
                    # Dividir cada línea en sus campos, respetando comillas
                    fields = []
                    field = ""
                    in_quotes = False
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                            field += char
                        elif char == ',' and not in_quotes:
                            fields.append(field.strip())
                            field = ""
                        else:
                            field += char
                    
                    # Añadir el último campo
                    if field:
                        fields.append(field.strip())
                    
                    # Asegurarse de que hay al menos 2 campos (pregunta y respuesta)
                    if len(fields) >= 2:
                        row_data = {}
                        for i, header in enumerate(headers[:min(len(headers), len(fields))]):
                            row_data[header] = fields[i]
                        data.append(row_data)
                
                # Crear DataFrame desde los datos procesados manualmente
                df = pd.DataFrame(data)
        
        # Verificar las columnas disponibles en el CSV
        columns = df.columns.tolist()
        logger.info(f"Columnas detectadas en el CSV de FAQs: {columns}")
        
        # Identificar las columnas principales
        pregunta_col = [col for col in columns if 'pregunta' in col.lower()][0] if any('pregunta' in col.lower() for col in columns) else columns[0]
        respuesta_col = [col for col in columns if 'respuesta' in col.lower()][0] if any('respuesta' in col.lower() for col in columns) else columns[1]
        
        # Columnas opcionales
        categoria_col = next((col for col in columns if 'categor' in col.lower()), None)
        etapa_col = next((col for col in columns if 'etapa' in col.lower()), None)
        objetivo_col = next((col for col in columns if 'objetivo' in col.lower()), None)
        siguiente_paso_col = next((col for col in columns if 'siguiente' in col.lower() or 'paso' in col.lower()), None)
        
        for idx, row in df.iterrows():
            # Crear un documento por cada FAQ
            categoria = row[categoria_col] if categoria_col and pd.notna(row[categoria_col]) else "General"
            filename = f"faq_{idx:03d}_{categoria.lower().replace(' ', '_')}.md"
            filepath = os.path.join(FAQS_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {row[pregunta_col]}\n\n")
                f.write(f"{row[respuesta_col]}\n\n")
                
                # Agregar información adicional si está disponible
                if categoria_col and pd.notna(row[categoria_col]):
                    f.write(f"**Categoría:** {row[categoria_col]}\n")
                
                if etapa_col and pd.notna(row[etapa_col]):
                    f.write(f"**Etapa:** {row[etapa_col]}\n")
                
                if objetivo_col and pd.notna(row[objetivo_col]):
                    f.write(f"\n**Objetivo:** {row[objetivo_col]}\n")
                
                if siguiente_paso_col and pd.notna(row[siguiente_paso_col]):
                    f.write(f"\n**Siguiente paso sugerido:** {row[siguiente_paso_col]}\n")
            
        logger.info(f"Se procesaron {len(df)} FAQs")
    
    except Exception as e:
        logger.error(f"Error al procesar FAQs: {str(e)}")
        logger.exception(e)


def clean_value(value):
    """Limpia un valor para asegurar que sea una cadena de texto."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def process_catalogo():
    """Procesa el archivo CSV del catálogo y crea documentos por categorías y productos."""
    try:
        logger.info(f"Procesando catálogo desde {CATALOGO_PATH}")
        
        # Leer el archivo CSV con manejo especial para delimitadores y comillas
        try:
            # Intentar primero con parámetros para manejar campos con comas
            df = pd.read_csv(CATALOGO_PATH, quotechar='"', escapechar='\\')
        except Exception as e:
            logger.warning(f"Error con primer método de lectura: {str(e)}")
            try:
                # Segundo intento con parámetros más permisivos
                df = pd.read_csv(CATALOGO_PATH, sep=',', quotechar='"', doublequote=True, 
                                 escapechar='\\', engine='python')
            except Exception as e2:
                logger.warning(f"Error con segundo método de lectura: {str(e2)}")
                # Último intento: abrir el archivo manualmente y procesarlo línea por línea
                with open(CATALOGO_PATH, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                # Obtener encabezados de la primera línea
                headers = lines[0].strip().split(',')
                data = []
                
                # Procesar cada línea manualmente
                for line in lines[1:]:
                    # Dividir cada línea en sus campos, respetando comillas
                    fields = []
                    field = ""
                    in_quotes = False
                    
                    for char in line:
                        if char == '"':
                            in_quotes = not in_quotes
                            field += char
                        elif char == ',' and not in_quotes:
                            fields.append(field.strip())
                            field = ""
                        else:
                            field += char
                    
                    # Añadir el último campo
                    if field:
                        fields.append(field.strip())
                    
                    # Crear un diccionario con encabezados y valores
                    if fields:
                        row_data = {}
                        for i, header in enumerate(headers[:min(len(headers), len(fields))]):
                            row_data[header] = fields[i]
                        data.append(row_data)
                
                # Crear DataFrame desde los datos procesados manualmente
                df = pd.DataFrame(data)
        
        # Verificar las columnas disponibles
        columns = df.columns.tolist()
        logger.info(f"Columnas detectadas en el CSV de catálogo: {columns}")
        
        # Identificar columnas principales
        producto_col = next((col for col in columns if 'producto' in col.lower() or 'nombre' in col.lower()), columns[0])
        descripcion_col = next((col for col in columns if 'descrip' in col.lower()), columns[1] if len(columns) > 1 else None)
        precio_col = next((col for col in columns if 'precio' in col.lower()), columns[2] if len(columns) > 2 else None)
        categoria_col = next((col for col in columns if 'categor' in col.lower()), None)
        
        # Crear un archivo por producto 
        for idx, row in df.iterrows():
            producto = clean_value(row[producto_col])
            if not producto:
                continue  # Saltamos filas sin nombre de producto
                
            # Generar nombre de archivo seguro
            filename = f"producto_{idx:03d}_{producto.lower().replace(' ', '_').replace('/', '_')}.md"
            filepath = os.path.join(PRODUCTOS_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Título y detalles principales
                f.write(f"# {producto}\n\n")
                
                # Categoría si existe
                if categoria_col and pd.notna(row[categoria_col]):
                    categoria = clean_value(row[categoria_col])
                    f.write(f"**Categoría:** {categoria}\n\n")
                
                # Descripción
                if descripcion_col and pd.notna(row[descripcion_col]):
                    descripcion = clean_value(row[descripcion_col])
                    f.write(f"## Descripción\n\n{descripcion}\n\n")
                
                # Precio
                if precio_col and pd.notna(row[precio_col]):
                    precio = clean_value(row[precio_col])
                    f.write(f"## Precio\n\n**Precio:** ${precio}\n\n")
                
                # Otras características si existen (columnas adicionales)
                f.write("## Características\n\n")
                for col in columns:
                    if col not in [producto_col, descripcion_col, precio_col, categoria_col] and pd.notna(row[col]):
                        f.write(f"**{col}:** {clean_value(row[col])}\n\n")
        
        # También crear archivos por categoría si existe la columna de categoría
        if categoria_col:
            categorias = {}
            for idx, row in df.iterrows():
                if pd.notna(row[categoria_col]):
                    categoria = clean_value(row[categoria_col])
                    if categoria not in categorias:
                        categorias[categoria] = []
                    
                    producto_info = {
                        "nombre": clean_value(row[producto_col]),
                        "descripcion": clean_value(row[descripcion_col]) if descripcion_col and pd.notna(row[descripcion_col]) else "",
                        "precio": clean_value(row[precio_col]) if precio_col and pd.notna(row[precio_col]) else ""
                    }
                    
                    categorias[categoria].append(producto_info)
            
            # Crear un archivo por categoría
            for categoria, productos in categorias.items():
                if not categoria or not productos:
                    continue
                    
                filename = f"categoria_{categoria.lower().replace(' ', '_').replace('/', '_')}.md"
                filepath = os.path.join(PRODUCTOS_DIR, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# Categoría: {categoria}\n\n")
                    
                    for producto in productos:
                        f.write(f"## {producto['nombre']}\n\n")
                        
                        if producto['descripcion']:
                            f.write(f"{producto['descripcion']}\n\n")
                        
                        if producto['precio']:
                            f.write(f"**Precio:** ${producto['precio']}\n\n")
                        
                        f.write("---\n\n")
        
        logger.info(f"Se procesaron {len(df)} productos en {len(categorias) if 'categorias' in locals() else 0} categorías")
    
    except Exception as e:
        logger.error(f"Error al procesar catálogo: {str(e)}")
        logger.exception(e)


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

    # Procesar datos de la web solo si la URL está definida en .env
    try:
        # Obtener URL de la web del negocio desde variable de entorno (.env)
        web_url = os.environ.get("WEB_URL")
        if web_url:
            logger.info(f"URL de web encontrada en .env: {web_url}")
            process_web_to_markdown(
                url=web_url,
                output_path=os.path.join(PRODUCTOS_DIR, "productos_web.md")
            )
        else:
            logger.info("No se encontró la variable WEB_URL en .env, omitiendo procesamiento web")
    except Exception as e:
        logger.warning(f"Error al procesar datos de la web: {str(e)}. Continuando con el resto del proceso.")

    # Procesar FAQs y catálogo desde CSV
    process_faqs()
    process_catalogo()
    logger.info("Preparación de la base de conocimientos completada")


if __name__ == "__main__":
    main()
