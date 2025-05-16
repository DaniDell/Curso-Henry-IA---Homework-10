"""
Herramienta para gestionar la base de conocimientos de CASA DEL MUEBLE.
Permite agregar, actualizar o eliminar información y reconstruir el índice.
"""
import os
import sys
import shutil
import logging
import argparse
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rutas importantes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge_base")
FAQS_DIR = os.path.join(KNOWLEDGE_DIR, "faqs")
PRODUCTOS_DIR = os.path.join(KNOWLEDGE_DIR, "productos")


def list_knowledge_files():
    """Lista todos los archivos en la base de conocimiento."""
    logger.info("Archivos en la base de conocimientos:")
    
    # Listar FAQs
    logger.info("\nFAQs:")
    for file in sorted(os.listdir(FAQS_DIR)):
        if file.endswith(".md"):
            logger.info(f"  - {file}")
    
    # Listar productos
    logger.info("\nProductos:")
    for file in sorted(os.listdir(PRODUCTOS_DIR)):
        if file.endswith(".md"):
            logger.info(f"  - {file}")


def delete_knowledge_file(filename):
    """Elimina un archivo de la base de conocimientos."""
    # Buscar en directorio de FAQs
    faq_path = os.path.join(FAQS_DIR, filename)
    if os.path.exists(faq_path):
        os.remove(faq_path)
        logger.info(f"Archivo eliminado: {faq_path}")
        return True
        
    # Buscar en directorio de productos
    product_path = os.path.join(PRODUCTOS_DIR, filename)
    if os.path.exists(product_path):
        os.remove(product_path)
        logger.info(f"Archivo eliminado: {product_path}")
        return True
        
    logger.error(f"No se encontró el archivo: {filename}")
    return False


def rebuild_index():
    """Reconstruye el índice de la base de conocimientos."""
    logger.info("Reconstruyendo el índice...")
    
    # Importar indexer y ejecutar main
    try:
        # Primero ejecutamos prepare_knowledge_base si existe
        if os.path.exists(os.path.join(BASE_DIR, "prepare_knowledge_base.py")):
            logger.info("Ejecutando prepare_knowledge_base.py...")
            import prepare_knowledge_base
            prepare_knowledge_base.main()
        
        # Luego reconstruimos el índice
        logger.info("Ejecutando indexer.py...")
        import indexer
        indexer.main()
        return True
    except Exception as e:
        logger.error(f"Error al reconstruir el índice: {str(e)}")
        return False


def update_csv_file(csv_type, file_path=None):
    """Actualiza un archivo CSV de origen y regenera los archivos markdown."""
    if csv_type not in ["faqs", "catalogo"]:
        logger.error("Tipo de CSV no válido. Debe ser 'faqs' o 'catalogo'")
        return False
        
    target_file = "FAQs.csv" if csv_type == "faqs" else "catalogo.csv"
    target_path = os.path.join(KNOWLEDGE_DIR, target_file)
    
    if file_path and os.path.exists(file_path):
        # Hacer backup del archivo original
        backup_path = target_path + ".backup"
        if os.path.exists(target_path):
            shutil.copy2(target_path, backup_path)
            logger.info(f"Backup creado: {backup_path}")
        
        # Copiar nuevo archivo
        shutil.copy2(file_path, target_path)
        logger.info(f"Archivo actualizado: {target_path}")
        
        # Regenerar base de conocimiento
        return rebuild_index()
    else:
        logger.error(f"Archivo de origen no encontrado: {file_path}")
        return False


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Gestor de la base de conocimientos")
    
    # Definir comandos
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # Comando list
    subparsers.add_parser("list", help="Lista todos los archivos en la base de conocimientos")
    
    # Comando delete
    delete_parser = subparsers.add_parser("delete", help="Elimina un archivo de la base de conocimientos")
    delete_parser.add_argument("filename", help="Nombre del archivo a eliminar")
    
    # Comando update-csv
    update_parser = subparsers.add_parser("update-csv", help="Actualiza un archivo CSV y regenera la base de conocimientos")
    update_parser.add_argument("type", choices=["faqs", "catalogo"], help="Tipo de CSV a actualizar")
    update_parser.add_argument("file_path", help="Ruta del archivo CSV de origen")
    
    # Comando rebuild
    subparsers.add_parser("rebuild", help="Reconstruye el índice de la base de conocimientos")
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Ejecutar comando correspondiente
    if args.command == "list":
        list_knowledge_files()
    elif args.command == "delete":
        success = delete_knowledge_file(args.filename)
        if success:
            rebuild_index()
    elif args.command == "update-csv":
        update_csv_file(args.type, args.file_path)
    elif args.command == "rebuild":
        rebuild_index()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
