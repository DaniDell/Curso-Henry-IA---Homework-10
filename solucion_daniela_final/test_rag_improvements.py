"""
Script para probar las mejoras en el sistema RAG.
"""
import os
import sys
import logging
from dotenv import load_dotenv

from main import load_embeddings, load_vector_db, load_llm, process_query

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv(override=True)

def test_simple_detection():
    """Prueba simple de detección del tipo de consulta."""
    test_queries = [
        "Quiero comprar una mesa de comedor",
        "¿Cuánto cuesta la silla modelo A32?",
        "¿Hacen envíos internacionales?",
        "Necesito información sobre garantías",
        "Me gustaría hablar con alguien",
    ]
    
    print("\n== Probando consultas básicas ==")
    for query in test_queries:
        print(f"\n- Query: '{query}'")

def test_search_processing():
    """Prueba el procesamiento de búsqueda con consultas de ejemplo y verifica que la respuesta contenga información concreta de productos."""
    import re
    # Cargar componentes necesarios
    print("\nCargando embeddings y base de datos vectorial...")
    embeddings = load_embeddings()
    vector_db = load_vector_db(embeddings)
    llm = load_llm()

    # Consultas de prueba
    test_queries = [
        "¿Tienen mesas de comedor de 6 personas?",
        "¿Cuánto cuesta el fogonero grande?",
        "¿Hacen envíos al interior del país?",
        "¿Los productos vienen ensamblados o hay que armarlos?",
        "Necesito una mesa negra para exterior",
    ]
    # Palabras clave típicas de productos y patrón de precio
    product_keywords = [
        "mesa", "silla", "fogonero", "camastro", "barral", "estante", "rack", "biblioteca", "perchero", "espejo", "precio", "categoría", "color", "variante"
    ]
    price_pattern = re.compile(r"\$?\d{2,}[\.,]?\d*")

    print("\n== Probando procesamiento de consultas ==")
    for query in test_queries:
        print(f"\nConsulta: '{query}'")
        try:
            response = process_query(query, vector_db, llm)
            short_response = response[:150] + "..." if len(response) > 150 else response
            print(f"Respuesta: {short_response}")
            # Verificar presencia de información concreta
            found = any(kw in response.lower() for kw in product_keywords) or price_pattern.search(response)
            assert found, f"La respuesta no contiene información concreta de productos: {response}"
        except AssertionError as ae:
            print(f"❌ FALLO: {ae}")
        except Exception as e:
            print(f"Error al procesar consulta: {str(e)}")

if __name__ == "__main__":
    print("\n===== PRUEBA DE MEJORAS RAG =====")
    try:
        test_simple_detection()
        test_search_processing()
        print("\n✅ Pruebas completadas con éxito")
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
