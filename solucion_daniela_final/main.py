"""
Chatbot RAG para Casa Mueble
Este script implementa un chatbot basado en recuperación aumentada de generación (RAG)
que utiliza una base de conocimientos vectorizada para responder preguntas sobre productos
y servicios de Casa Mueble.
"""
import os
import sys
import logging
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI  # For fallback to OpenAI
from langchain_community.llms import HuggingFaceHub  # For local LLM

from config import KNOWLEDGE_DIR, INDEX_DIR, EMBEDDING_MODEL_NAME


# Cargar variables de entorno desde .env si existe
load_dotenv(override=True)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prompt template para el chatbot
SYSTEM_TEMPLATE = """
Eres un asistente virtual de Casa Mueble, una empresa especializada en muebles de alta calidad. Tu objetivo es ayudar a los clientes a encontrar productos, resolver dudas sobre la empresa y brindar una experiencia personalizada.

INSTRUCCIONES CRÍTICAS SOBRE ALUCINACIONES:
- NUNCA, BAJO NINGUNA CIRCUNSTANCIA, debes inventar o fabricar información que no esté explícitamente en el contexto proporcionado.
- SOLO menciona productos que existan explícitamente en el contexto. La lista completa de productos es: Camastro Leonor, Camastro Clara, Camastro Delfina, Sillón Clemente, Kit Barral Simple Completo, Kit Barral Doble Completo, Fogonero Perikles, Fogonero Efesto, Fogonero con Media Parrilla, Media Parrilla, Estaca Asador, Mesa Brisa 100x50 cm, Juego de Mesas Nido Redondas.
- NUNCA menciones productos genéricos como "Mesa de Comedor Extensible" si no están explícitamente en el contexto.
- NUNCA inventes precios. Si un precio no está explícitamente en el contexto, simplemente di que no tienes esa información.
- Si encuentras una pregunta que requiere información no disponible en el contexto, simplemente admite que no tienes esa información específica.

INSTRUCCIONES GENERALES:
1. Sé amable, profesional y conciso en tus respuestas.
2. MUY IMPORTANTE: SIEMPRE que el contexto incluya información de productos, muestra primero las opciones concretas (nombre, categoría, características, precio, etc.) relevantes a la consulta del cliente, ANTES de hacer preguntas o pedir aclaraciones.
3. Si hay varios productos relevantes, muestra una lista breve y clara con nombre, categoría y precio (si está disponible), y luego ofrece ampliar detalles si el cliente lo desea.
4. CRUCIAL: ANTES de indicar que no tienes información sobre un producto específico, BUSCA CUIDADOSAMENTE en todo el contexto proporcionado, prestando especial atención a nombres similares, variaciones ortográficas o productos de la misma categoría.
5. Para datos específicos como precios, dimensiones o disponibilidad, cita la fuente de donde obtienes la información.
6. Mantén una conversación fluida, reconociendo y recordando lo que el cliente ya mencionó previamente, pero NO retrases la presentación de productos con preguntas innecesarias.
7. Evita repetir información que ya has proporcionado anteriormente.
8. Si te piden un precio específico y no está en el contexto, NUNCA inventes un precio. En su lugar, di: "Lo siento, no tengo información sobre el precio de este producto en particular. Para obtener el precio actualizado, te recomiendo contactar directamente con Casa Mueble a través de su página web o número de atención al cliente."
9. Si tras una búsqueda cuidadosa no encuentras información sobre un producto específico, NO INVENTES que el producto existe o tiene ciertas características. Di claramente que no tienes información sobre ese producto.

CONTEXTO RELEVANTE (Esta es tu única fuente de información para responder):
{context}

HISTORIAL DE CONVERSACIÓN:
{chat_history}

PREGUNTA ACTUAL DEL CLIENTE:
{question}

Tu respuesta debe ser útil, relevante y amigable, mostrando primero las opciones concretas de productos o información relevante, y solo después, si es necesario, hacer preguntas para personalizar la atención.
"""

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
        sys.exit(1)

def load_vector_db(embeddings: HuggingFaceEmbeddings) -> FAISS:
    """
    Carga la base de datos vectorial FAISS.
    
    Args:
        embeddings (HuggingFaceEmbeddings): Modelo de embeddings
        
    Returns:
        FAISS: Base de datos vectorial cargada
    """
    logger.info(f"Cargando índice FAISS desde: {INDEX_DIR}")
    
    try:
        if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
            logger.error(f"No se encontró el índice FAISS en: {INDEX_DIR}")
            logger.info("Ejecuta 'python manage_knowledge_base.py rebuild' para crear el índice")
            sys.exit(1)
            
        vector_db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        logger.info("Índice FAISS cargado exitosamente")
        
        return vector_db
    
    except Exception as e:
        logger.error(f"Error al cargar índice FAISS: {str(e)}")
        sys.exit(1)

def load_llm():
    """
    Carga el modelo de lenguaje a utilizar.
    
    Returns:
        El modelo de lenguaje cargado o None si ocurre un error
    """
    logger.info("Cargando modelo de lenguaje")    # Primera opción: probar con OpenAI si hay API key disponible
    if os.environ.get("OPENAI_API_KEY"):
        try:
            logger.info("Usando OpenAI como modelo de lenguaje")
            return ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
        except Exception as e:
            logger.warning(f"Error al cargar OpenAI: {str(e)}")
    
    # Segunda opción: probar con HuggingFace Hub
    if os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
        try:
            logger.info("Usando HuggingFace Hub como modelo de lenguaje")
            return HuggingFaceHub(
                repo_id="google/flan-t5-base",
                model_kwargs={"temperature": 0.1, "max_length": 512}
            )
        except Exception as e:
            logger.warning(f"Error al cargar HuggingFace Hub: {str(e)}")
    
    # Si llegamos aquí, advertir que no hay modelo disponible
    logger.warning("No se pudo cargar ningún modelo de lenguaje. El sistema funcionará con formato de plantilla simple.")
    return None

def expand_query(query: str, chat_history: List[Dict[str, str]] = None) -> str:
    """
    Expande la consulta del usuario para mejorar la búsqueda vectorial.
    
    Args:
        query (str): Consulta original del usuario
        chat_history (List[Dict[str, str]], optional): Historial de la conversación
        
    Returns:
        str: Consulta expandida y mejorada
    """
    expanded_query = query
    
    # Añadir contexto del historial de chat si está disponible
    if chat_history and len(chat_history) > 0:
        # Tomar las últimas 2 interacciones para contexto
        recent_context = chat_history[-4:] if len(chat_history) > 4 else chat_history
        context = " ".join([entry["content"] for entry in recent_context])
        
        # Construir una consulta expandida con el contexto
        expanded_query = f"{query}. Contexto adicional de la conversación: {context}"
    
    # Expandir nombres de productos específicos
    product_specific_mappings = {
        "camastro": ["camastro", "tumbona", "reposera", "sillón reclinable", "leonor", "clara", "delfina"],
        "sillón": ["sillón", "sillon", "sofá", "sofa", "butaca", "clemente"],
        "fogonero": ["fogonero", "brasero", "parrilla", "asador", "perikles", "efesto"],
        "mesa": ["mesa", "escritorio", "mueble", "mesita", "brisa"],
        "kit": ["kit", "conjunto", "set", "barral"]
    }
    
    # Comprobar si la consulta contiene palabras clave de productos específicos
    for product_type, synonyms in product_specific_mappings.items():
        if any(term.lower() in query.lower() for term in synonyms):
            # Si se encuentra un tipo de producto, añadir todos sus sinónimos a la consulta expandida
            additional_terms = " ".join([term for term in synonyms if term.lower() not in expanded_query.lower()])
            expanded_query = f"{expanded_query} {additional_terms}"
            
            # Si la consulta menciona un nombre específico, reforzarlo
            for potential_name in ["leonor", "clara", "delfina", "clemente", "perikles", "efesto", "brisa"]:
                if potential_name.lower() in query.lower():
                    expanded_query = f"{expanded_query} producto {potential_name} específico"
                    break
    
    # Añadir términos específicos para mejorar la búsqueda
    product_keywords = [
        "mesa", "silla", "mueble", "fogonero", "estante", "rack", 
        "biblioteca", "perchero", "espejo", "camastro", "sillón"
    ]
    
    for keyword in product_keywords:
        if keyword in query.lower() and keyword not in expanded_query.lower():
            expanded_query = f"{expanded_query} {keyword}"
    
    # Si la consulta menciona dimensiones o colores, enfatizarlos
    dimension_pattern = r'\d+\s*(?:cm|mts?|metros?|centimetros?)'
    dimensions = re.findall(dimension_pattern, query.lower())
    colors = ["negro", "blanco", "verde", "oxido", "oxidado"]
    
    dimension_terms = " ".join(dimensions)
    color_terms = " ".join([color for color in colors if color in query.lower()])
    
    if dimension_terms:
        expanded_query = f"{expanded_query} con dimensiones {dimension_terms}"
    if color_terms:
        expanded_query = f"{expanded_query} de color {color_terms}"
    
    return expanded_query

def search_knowledge_base(query: str, vector_db: FAISS, k: int = 3, chat_history: List[Dict[str, str]] = None) -> List[str]:
    """
    Busca en la base de conocimientos utilizando la consulta del usuario.
    
    Args:
        query (str): Consulta del usuario
        vector_db (FAISS): Base de datos vectorial
        k (int, optional): Número de documentos a recuperar. Default es 3.
        chat_history (List[Dict[str, str]], optional): Historial de la conversación
        
    Returns:
        List[str]: Documentos relevantes encontrados
    """
    try:
        # Detectar si la consulta es sobre un producto específico
        product_specific = False
        product_keywords = ["camastro", "sillón", "fogonero", "mesa", "parrilla", "kit", "barral", "estaca"]
        for keyword in product_keywords:
            if keyword.lower() in query.lower():
                product_specific = True
                break
        
        # Ajustar k si la consulta es sobre un producto específico
        if product_specific:
            k = 5  # Aumentar el número de resultados para consultas de productos específicos
        
        # Expand query to improve search
        expanded_query = expand_query(query, chat_history)
        logger.info(f"Consulta original: '{query}' -> Expandida: '{expanded_query}'")
        
        # Realizar la búsqueda de similitud con la consulta expandida
        documents = vector_db.similarity_search(expanded_query, k=k)
        
        # Búsqueda adicional con la consulta original para no perder resultados directos
        original_documents = vector_db.similarity_search(query, k=k)
        
        # Para productos específicos, realizar una búsqueda adicional con palabras clave exactas
        if product_specific:
            # Extraer posibles nombres de productos de la consulta
            words = query.lower().split()
            for word in words:
                if len(word) > 3 and word not in ["que", "cual", "como", "donde", "quien", "tiene", "para"]:
                    # Buscar documentos que contengan exactamente esa palabra
                    exact_documents = vector_db.similarity_search(word, k=3)
                    original_documents.extend(exact_documents)
        
        # Combinar resultados y eliminar duplicados
        all_docs = []
        doc_contents = set()
        
        for doc_list in [documents, original_documents]:
            for doc in doc_list:
                if doc.page_content not in doc_contents:
                    all_docs.append(doc)
                    doc_contents.add(doc.page_content)
        
        # Formatear resultados con fuentes
        contexts = []
        max_results = k + 2 if product_specific else k  # Más resultados para productos específicos
        for doc in all_docs[:max_results]:  # Limitar a max_results después de combinar
            # Extraer metadata o nombre de archivo como fuente
            source = doc.metadata.get('source', 'Unknown source') if hasattr(doc, 'metadata') else 'Unknown source'
            
            # Formatear el contenido con la fuente
            formatted_content = f"{doc.page_content}\n[Fuente: {source}]"
            contexts.append(formatted_content)
        
        return contexts
    
    except Exception as e:
        logger.error(f"Error al buscar en la base de conocimientos: {str(e)}")
        return []

def format_chat_history(history: List[Dict[str, str]]) -> str:
    """
    Formatea el historial de chat para incluirlo en el prompt.
    
    Args:
        history (List[Dict[str, str]]): Lista de mensajes con claves 'role' y 'content'
        
    Returns:
        str: Historial de chat formateado
    """
    if not history:
        return "No hay historial previo."
        
    formatted_history = ""
    for message in history:
        role = "Cliente" if message["role"] == "user" else "Asistente"
        formatted_history += f"{role}: {message['content']}\n\n"
        
    return formatted_history.strip()

def process_query(user_input: str, vector_db: FAISS, llm=None, chat_history: List[Dict[str, str]] = None) -> str:
    """
    Procesa la consulta del usuario y genera una respuesta utilizando solo la base vectorial y el LLM.
    Si no hay información relevante, genera un fallback contextualizado con sugerencia de web y URL personalizada.
    """
    if chat_history is None:
        chat_history = []

    # 1. Expandir la consulta usando historial y sinónimos
    expanded_query = expand_query(user_input, chat_history)

    # 2. Buscar en la base vectorial
    knowledge_base_info = search_knowledge_base(expanded_query, vector_db, k=3, chat_history=chat_history)

    # 3. Si hay resultados, armar contexto y generar respuesta con LLM
    if knowledge_base_info:
        context = "\n\n".join(knowledge_base_info)
        formatted_history = format_chat_history(chat_history)
        prompt = ChatPromptTemplate.from_template(SYSTEM_TEMPLATE)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        response = chain.invoke({
            "context": context,
            "question": user_input,
            "chat_history": formatted_history
        })
        return response    # 4. Si no hay resultados, fallback contextualizado    formatted_history = format_chat_history(chat_history)
    fallback_context = (
        "No se encontró información relevante sobre esta consulta en nuestra base de datos. "
        "IMPORTANTE: Debes indicar claramente al cliente que no dispones de información específica sobre su consulta. "
        "NO inventes productos, características, precios, o cualquier otra información. "
        "La lista completa de productos en nuestra base de conocimientos es: Camastro Leonor, Camastro Clara, Camastro Delfina, Sillón Clemente, "
        "Kit Barral Simple Completo, Kit Barral Doble Completo, Fogonero Perikles, Fogonero Efesto, Fogonero con Media Parrilla, Media Parrilla, "
        "Estaca Asador, Mesa Brisa 100x50 cm, Juego de Mesas Nido Redondas. "
        "Recomienda al cliente visitar la web oficial: https://casamueble.com.ar"
    )
    # Si la consulta es sobre producto, armar URL personalizada
    product_keywords = ["producto", "mueble", "mesa", "silla", "fogonero", "camastro"]
    if any(word in user_input.lower() for word in product_keywords):
        fallback_context += f"\nTambién podés sugerir que busque aquí: https://casamueble.com.ar/search/?q={user_input.replace(' ', '+')}"

    prompt = ChatPromptTemplate.from_template(SYSTEM_TEMPLATE)
    output_parser = StrOutputParser()
    
    # Si estamos usando LLM, utilizar la cadena normal
    if llm:
        chain = prompt | llm | output_parser
        response = chain.invoke({
            "context": fallback_context,
            "question": user_input,
            "chat_history": formatted_history
        })
    else:
        # Si no hay LLM disponible, usar una respuesta predeterminada para evitar hallucinations
        response = (
            "Lo siento, no tengo información específica sobre tu consulta en mi base de datos. "
            "Para obtener información actualizada y precisa, te recomiendo visitar la página web oficial "
            "de Casa Mueble en https://casamueble.com.ar o contactar directamente con el servicio de atención al cliente."
        )
    return response

def save_conversation_log(chat_history, filename="conversation_log.txt"):
    """
    Guarda el historial de la conversación en un archivo de texto.
    Args:
        chat_history (list): Lista de mensajes (dicts con 'role' y 'content')
        filename (str): Nombre del archivo donde guardar el log
    """
    # Crear ruta absoluta para el archivo de log
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n=== Nueva conversación ===\n")
            f.write(f"Fecha y hora: {os.path.basename(__file__)} - {os.path.dirname(os.path.abspath(__file__))}\n")
            for msg in chat_history:
                role = "Usuario" if msg["role"] == "user" else "Asistente"
                f.write(f"{role}: {msg['content']}\n")
            f.write("\n=== Fin de la conversación ===\n\n")
            
        # Imprimir la ubicación del archivo para referencia
        print(f"\n[Log guardado en: {log_path}]")
        
    except Exception as e:
        logger.error(f"Error al guardar el log: {str(e)}")
        print(f"\n[Error al guardar el log: {str(e)}]")

def main():
    """Función principal para ejecutar el chatbot."""
    print("\n===== Bienvenido al Asistente Virtual de Casa Mueble =====")
    print("Escribe 'salir' o 'exit' para terminar la conversación.")
    print("¿En qué puedo ayudarte hoy?\n")
    
    # Cargar embeddings, base de datos vectorial y modelo de lenguaje
    embeddings = load_embeddings()
    vector_db = load_vector_db(embeddings)
    
    # Cargar el modelo de lenguaje una sola vez
    try:
        llm = load_llm()
        logger.info("Modelo de lenguaje cargado correctamente")
    except Exception as e:
        logger.error(f"Error al cargar el modelo de lenguaje: {str(e)}")
        llm = None
        
    # Inicializar historial de conversación
    chat_history = []
    hubo_conversacion = False
    while True:
        # Obtener entrada del usuario
        user_input = input("\n👤 Tú: ")
        
        # Verificar si el usuario quiere salir
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("\n🤖 Asistente: ¡Gracias por utilizar nuestro asistente virtual! ¡Hasta pronto!")
            # Guardar log solo si hubo al menos un intercambio exitoso
            if hubo_conversacion and len(chat_history) > 1:
                save_conversation_log(chat_history)
                print("\n[Conversación registrada en conversation_log.txt]")
            break
        
        # Agregar entrada del usuario al historial
        chat_history.append({"role": "user", "content": user_input})
        
        # Limitar tamaño del historial (último par de intercambios)
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]
        
        # Procesar la consulta y generar respuesta
        try:
            response = process_query(user_input, vector_db, llm, chat_history)
            print(f"\n🤖 Asistente: {response}")
            
            # Agregar respuesta al historial
            chat_history.append({"role": "assistant", "content": response})
            hubo_conversacion = True
        except Exception as e:
            logger.error(f"Error al procesar la consulta: {str(e)}")
            error_msg = "Lo siento, ha ocurrido un error al procesar tu consulta. Por favor, intenta de nuevo."
            print(f"\n🤖 Asistente: {error_msg}")
            
            # También agregar mensaje de error al historial
            chat_history.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
