"""
Script para indexar la base de conocimientos de CASA DEL MUEBLE en un índice FAISS.
Vectoriza documentos para la búsqueda semántica de información sobre muebles de hierro.
"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import KNOWLEDGE_DIR, INDEX_DIR, EMBEDDING_MODEL_NAME
from utils.error_handlers import error_handler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_directories() -> bool:
    """
    Verifica que los directorios necesarios existan y crea el directorio de índice si no existe.
    
    Returns:
        bool: True si la validación es exitosa, False en caso contrario
    """
    try:
        # Verificar que el directorio de conocimientos existe
        if not os.path.exists(KNOWLEDGE_DIR):
            logger.error(f"El directorio de conocimientos no existe: {KNOWLEDGE_DIR}")
            return False
        
        # Crear directorio de índice si no existe
        os.makedirs(INDEX_DIR, exist_ok=True)
        
        return True
    
    except Exception as e:
        logger.error(f"Error al validar directorios: {str(e)}")
        return False


def load_documents() -> List[Dict[str, Any]]:
    """
    Carga los documentos desde el directorio de conocimientos.
    
    Returns:
        List[Dict[str, Any]]: Lista de documentos cargados
    """
    logger.info(f"Cargando documentos desde: {KNOWLEDGE_DIR}")
    
    try:
        loader = DirectoryLoader(
            KNOWLEDGE_DIR,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True
        )
        
        documents = loader.load()
        logger.info(f"Se cargaron {len(documents)} documentos")
        
        return documents
    
    except Exception as e:
        logger.error(f"Error al cargar documentos: {str(e)}")
        raise


def split_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Divide los documentos en chunks más pequeños para mejor indexación.
    
    Args:
        documents (List[Dict[str, Any]]): Lista de documentos a dividir
        
    Returns:
        List[Dict[str, Any]]: Lista de documentos divididos
    """
    logger.info("Dividiendo documentos en chunks")
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        split_docs = text_splitter.split_documents(documents)
        logger.info(f"Documentos divididos en {len(split_docs)} chunks")
        
        return split_docs
    
    except Exception as e:
        logger.error(f"Error al dividir documentos: {str(e)}")
        raise


def load_embeddings() -> HuggingFaceEmbeddings:
    """
    Carga el modelo de embeddings.
    
    Returns:
        HuggingFaceEmbeddings: Modelo de embeddings cargado
    """
    logger.info(f"Cargando modelo de embeddings: {EMBEDDING_MODEL_NAME}")
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            cache_folder=os.path.join(os.path.dirname(INDEX_DIR), "models_cache")
        )
        
        return embeddings
    
    except Exception as e:
        logger.error(f"Error al cargar modelo de embeddings: {str(e)}")
        raise


def create_index(documents: List[Dict[str, Any]], embeddings: HuggingFaceEmbeddings) -> Optional[FAISS]:
    """
    Crea un índice FAISS a partir de los documentos y embeddings.
    
    Args:
        documents (List[Dict[str, Any]]): Lista de documentos procesados
        embeddings (HuggingFaceEmbeddings): Modelo de embeddings
        
    Returns:
        Optional[FAISS]: Índice FAISS creado o None si hay un error
    """
    logger.info("Creando índice FAISS")
    
    try:
        db = FAISS.from_documents(documents, embeddings)
        logger.info("Índice FAISS creado exitosamente")
        
        return db
    
    except Exception as e:
        logger.error(f"Error al crear índice FAISS: {str(e)}")
        raise


def save_index(db: FAISS) -> bool:
    """
    Guarda el índice FAISS en el directorio especificado.
    
    Args:
        db (FAISS): Índice FAISS a guardar
        
    Returns:
        bool: True si el guardado es exitoso, False en caso contrario
    """
    logger.info(f"Guardando índice FAISS en: {INDEX_DIR}")
    
    try:
        db.save_local(INDEX_DIR)
        logger.info(f"Índice guardado exitosamente en: {INDEX_DIR}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error al guardar índice: {str(e)}")
        return False


@error_handler
def main() -> None:
    """Función principal para indexar la base de conocimientos."""
    logger.info("Iniciando indexación de la base de conocimientos")

    # Validar directorios
    if not validate_directories():
        logger.error("Falló la validación de directorios")
        return

    # Cargar documentos
    documents = load_documents()

    # Dividir documentos
    split_docs = split_documents(documents)

    # Cargar embeddings
    embeddings = load_embeddings()

    # Crear índice
    db = create_index(split_docs, embeddings)

    # Guardar índice
    if db and save_index(db):
        logger.info("Indexación completada exitosamente")
    else:
        logger.error("Error en el proceso de indexación")

if __name__ == "__main__":
    main()
