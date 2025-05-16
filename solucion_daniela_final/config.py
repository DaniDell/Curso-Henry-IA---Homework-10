import os

# Define the base directory for the knowledge base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, 'knowledge_base')

# Paths to the CSV files
CATALOGO_PATH = os.path.join(KNOWLEDGE_DIR, 'catalogo.csv')
FAQS_PATH = os.path.join(KNOWLEDGE_DIR, 'FAQs.csv')

# Define the directory for the FAISS index
INDEX_DIR = os.path.join(BASE_DIR, 'faiss_index')

# Define the embedding model name
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

# Define error messages
ERROR_MESSAGES = {
    'csv_error': 'Error al procesar los datos del catálogo.',
    'file_not_found': 'No se pudo encontrar el archivo especificado.',
    'network_error': 'Error de red al conectar con el servicio.',
    'general_error': 'Ha ocurrido un error inesperado.',
    'no_data': 'No se encontraron datos que coincidan con tu búsqueda.'
}
