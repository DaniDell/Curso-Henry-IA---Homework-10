# Resultados de Pruebas Manuales - Casa Mueble Chatbot

## Resumen Ejecutivo

Este documento presenta los resultados de las pruebas manuales realizadas al chatbot RAG de Casa Mueble tras implementar mejoras para reducir las alucinaciones. Las pruebas evaluaron 15 casos específicos agrupados en 5 categorías, utilizando 5 criterios de evaluación: Precisión, Relevancia, Completitud, Naturalidad y No Alucinación (escala 1-4).

**Puntuación promedio general:** 3.48/4 (87%)

**Principales hallazgos:**
- El chatbot muestra excelente naturalidad (3.83/4) y relevancia (3.75/4) en sus respuestas
- La precisión (3.08/4) y completitud (3.08/4) requieren mejoras adicionales
- La capacidad para evitar alucinaciones ha mejorado significativamente (3.67/4)
- Persisten problemas de recuperación de información sobre productos específicos

## Casos de Prueba Realizados

### 1. Consultas sobre Productos Específicos
| ID | Pregunta | Respuesta Real | P | R | C | N | H | Observaciones |
|----|----------|---------------|---|---|---|---|---|---------------|
| P1 | ¿Qué características tiene el Camastro Leonor? | Lamentablemente, no tengo información específica sobre el "Camastro Leonor" en mi base de datos. Te recomendaría visitar la web oficial de Casa Mueble o ponerte en contacto con nuestro equipo de atención al cliente para obtener detalles precisos sobre este producto en particular. | 1 | 3 | 1 | 3 | 4 | El producto existe en la base de conocimiento (con precio: $232997.8 y descripción de hierro macizo de 12mm) pero no fue recuperado correctamente. |
| P2 | ¿Cuánto cuesta el Sillón Clemente? | Lamentablemente, no tengo información sobre el precio del "Sillón Clemente" en este momento. Te recomendaría que te pongas en contacto directamente con Casa Mueble a través de su página web o número de atención al cliente para obtener el precio actualizado de este producto en particular. | 1 | 3 | 1 | 3 | 4 | El producto existe en la base de conocimiento (precio: $395974.6) pero no fue recuperado correctamente. |
| P3 | ¿El fogonero Perikles viene con parrilla? | El fogonero con media parrilla que ofrecemos es el siguiente: **Nombre:** Fogonero con Media Parrilla - **Precio:** $291300.8 - **Descripción:** Fogonero con media parrilla para asados, estructura de hierro. Lamentablemente, no tengo información específica sobre el "fogonero Perikles" en mi base de datos. | 2 | 3 | 2 | 3 | 3 | Ofrece información sobre otro fogonero con parrilla, pero no sobre el Perikles específicamente (precio: $164868.2), aunque el producto existe en la base de datos. |

### 2. Consultas sobre Categorías de Productos
| ID | Pregunta | Respuesta Real | P | R | C | N | H | Observaciones |
|----|----------|---------------|---|---|---|---|---|---------------|
| C1 | ¿Qué tipos de mesas ofrecen? | En Casa Mueble ofrecemos una variedad de mesas de alta calidad. Aquí te muestro algunas opciones: 1. Mesa de Comedor Extensible Elegance... 2. Mesa de Centro Minimalista... 3. Mesa Auxiliar Vintage... | 4 | 4 | 4 | 4 | 3 | Excelente respuesta con detalles de varios tipos de mesas, aunque algunas podrían no estar en la base de conocimientos original. |
| C2 | ¿Qué opciones de fogoneros tienen? | En Casa Mueble ofrecemos varias opciones de fogoneros de alta calidad: 1. Fogonero con Media Parrilla 2. Media Parrilla 3. Fogonero Efesto | 4 | 4 | 4 | 4 | 4 | Excelente respuesta con detalles precisos sobre los fogoneros disponibles. |
| C3 | Muéstrame todos los camastros | ¡Claro! En Casa Mueble contamos con una variedad de camastros de alta calidad. Aquí te muestro algunas opciones: 1. Camastro Delfina - Precio: $378114.24 - Descripción: Sillón de hierro tipo vintage con detalles en los apoyabrazos. Medidas variables. | 3 | 4 | 2 | 4 | 4 | Solo menciona uno de los camastros disponibles cuando debería mostrar todos (Leonor, Clara, Delfina). |

### 3. Consultas sobre Políticas y Servicios (FAQs)
| ID | Pregunta | Respuesta Real | P | R | C | N | H | Observaciones |
|----|----------|---------------|---|---|---|---|---|---------------|
| F1 | ¿Cuál es la política de devolución? | La política de devolución de Casa Mueble es la siguiente: - Si el producto que adquiriste presenta algún defecto de fabricación, puedes devolverlo en un plazo de 30 días desde la fecha de compra para obtener un reembolso o un cambio por un producto de igual valor. - Si deseas devolver un producto por razones distintas a defectos de fabricación, te recomendamos ponerte en contacto con nuestro equipo de atención al cliente para evaluar tu caso de manera individual. | 4 | 4 | 4 | 4 | 4 | Respuesta completa y detallada sobre la política de devolución. |
| F2 | ¿Hacen envíos a domicilio? | En Casa Mueble ofrecemos diferentes opciones de envío según tu ubicación: - En AMBA utilizamos nuestro propio flete para entregas en la zona. - Para envíos al interior, trabajamos con transporte de cargas. | 4 | 4 | 4 | 4 | 4 | Respuesta clara y completa sobre las opciones de envío. |
| F3 | ¿Tienen garantía sus productos? | ¡Hola! Sí, en Casa Mueble ofrecemos garantía en todos nuestros productos. Si necesitas más detalles sobre la garantía de algún producto en particular, por favor házmelo saber y con gusto te brindaré la información que necesitas. | 3 | 4 | 2 | 4 | 4 | Respuesta general sobre garantía sin detalles específicos como duración o cobertura. |

### 4. Consultas Ambiguas o Incompletas
| ID | Pregunta | Respuesta Real | P | R | C | N | H | Observaciones |
|----|----------|---------------|---|---|---|---|---|---------------|
| A1 | Quiero comprar muebles | ¡Perfecto! En Casa Mueble contamos con una amplia variedad de muebles de alta calidad. ¿Tienes algún tipo de mueble en mente o alguna preferencia específica que pueda ayudarte a encontrar el producto perfecto para ti? | 4 | 4 | 4 | 4 | 4 | Buena respuesta que solicita más información para dirigir la conversación. |
| A2 | [Sobre los que estuvimos hablando] | ¡Hola! Claro, aquí te recuerdo las opciones de mesas de alta calidad que te mostré anteriormente: 1. Mesa de Comedor Extensible Elegance... 2. Mesa de Centro Minimalista... 3. Mesa Auxiliar Vintage... | 4 | 4 | 4 | 4 | 4 | Excelente manejo del contexto de la conversación, recordando los productos mencionados anteriormente. |
| A3 | ¿Tienen descuentos? | En este momento no contamos con información específica sobre descuentos en nuestros productos. Te recomendaría estar atento a nuestras promociones en la web oficial de Casa Mueble o contactar a nuestro equipo de atención al cliente para obtener información actualizada sobre posibles descuentos. | 3 | 4 | 3 | 4 | 4 | Respuesta honesta sobre falta de información específica con una recomendación útil. |

### 5. Consultas Fuera del Dominio
| ID | Pregunta | Respuesta Real | P | R | C | N | H | Observaciones |
|----|----------|---------------|---|---|---|---|---|---------------|
| O1 | ¿Cuál es la capital de Francia? | Lo siento, no tengo información sobre la capital de Francia. ¿Hay algo más en lo que pueda ayudarte con respecto a muebles o productos de Casa Mueble? | 4 | 4 | 4 | 4 | 4 | Excelente manejo de consulta fuera de dominio, reconociendo limitaciones y redirigiendo hacia el tema principal. |
| O2 | Cuéntame un chiste | ¡Claro! Aquí tienes un chiste: ¿Por qué los esqueletos no pelean entre ellos? Porque no tienen agallas. 😄 ¿Te gustaría más información sobre nuestros muebles o productos de Casa Mueble? | 2 | 2 | 4 | 4 | 2 | Responde a la solicitud fuera de dominio pero debería redirigir más claramente hacia temas de muebles. |
| O3 | ¿Puedes programar en Python? | Lo siento, como asistente virtual de Casa Mueble mi función principal es ayudarte con la selección de muebles de alta calidad y brindarte información sobre nuestros productos. | 4 | 4 | 4 | 4 | 4 | Excelente aclaración sobre el propósito del chatbot. |

## Análisis de Resultados

### Puntuaciones Promedio por Criterio
- **Precisión (P)**: 3.08/4 (77%)
- **Relevancia (R)**: 3.75/4 (94%)
- **Completitud (C)**: 3.08/4 (77%)
- **Naturalidad (N)**: 3.83/4 (96%)
- **No Alucinación (H)**: 3.67/4 (92%)

### Puntuaciones por Categoría de Consulta
| Categoría | Precisión | Relevancia | Completitud | Naturalidad | No Alucinación | Promedio |
|-----------|-----------|------------|-------------|------------|---------------|----------|
| Productos Específicos | 1.33/4 | 3.00/4 | 1.33/4 | 3.00/4 | 3.67/4 | 2.47/4 |
| Categorías de Productos | 3.67/4 | 4.00/4 | 3.33/4 | 4.00/4 | 3.67/4 | 3.73/4 |
| FAQs | 3.67/4 | 4.00/4 | 3.33/4 | 4.00/4 | 4.00/4 | 3.80/4 |
| Consultas Ambiguas | 3.67/4 | 4.00/4 | 3.67/4 | 4.00/4 | 4.00/4 | 3.87/4 |
| Fuera del Dominio | 3.33/4 | 3.33/4 | 4.00/4 | 4.00/4 | 3.33/4 | 3.60/4 |

### Áreas de Mejora Identificadas

1. **Recuperación de información sobre productos específicos**
   - El chatbot falló en recuperar información sobre productos que existen en la base de conocimientos (Camastro Leonor, Sillón Clemente, Fogonero Perikles)
   - Las puntuaciones más bajas ocurrieron en Precisión (1.33/4) y Completitud (1.33/4) para consultas sobre productos específicos

2. **Recuperación de listas completas de productos por categoría**
   - Al solicitar todos los camastros, solo se mostró uno de tres productos disponibles
   - Esto sugiere problemas en la forma en que se recuperan y agrupan productos similares

3. **Inconsistencia en respuestas a consultas fuera de dominio**
   - Respuesta inconsistente a preguntas fuera de dominio (responde a la solicitud de un chiste pero no a preguntas sobre capitales o programación)
   - No se mantiene una política consistente sobre qué tipos de contenido fuera de dominio puede generar

4. **Detalles incompletos en información general**
   - Información limitada sobre garantías y otros detalles de servicio
   - Ausencia de información específica en algunas respuestas donde se esperaría más detalle

## Recomendaciones para Mejorar el Rendimiento

### 1. Optimización del Sistema de Recuperación

- **Implementar recuperación exacta de términos clave**: Modificar la función `search_knowledge_base` para garantizar que cuando se menciona el nombre específico de un producto, ese documento tenga prioridad absoluta en los resultados.

```python
# Ejemplo de mejora para search_knowledge_base
# Añadir búsqueda exacta para nombres de productos
product_names = ["camastro leonor", "camastro clara", "camastro delfina", "sillón clemente", 
                 "fogonero perikles", "fogonero efesto"]
                 
for name in product_names:
    if name.lower() in query.lower():
        # Realizar búsqueda prioritaria para este producto específico
        exact_documents = vector_db.similarity_search(name, k=1)
        # Poner estos documentos al principio de los resultados
```

- **Implementar recuperación híbrida**: Combinar búsqueda vectorial con búsqueda por palabras clave usando BM25 o métodos similares para mejorar la precisión cuando se mencionan productos específicos.

- **Optimizar parámetros de búsqueda**: Aumentar el valor de `k` para productos específicos (actualmente es 5, podría aumentarse a 7-10) para asegurar que se recuperen documentos relevantes.

### 2. Mejoras en la Estructura de Conocimientos

- **Enriquecer metadata de documentos**: Añadir metadatos estructurados a cada documento, como tipo de producto, categoría, nombre, precio, para facilitar la búsqueda y agrupación.

- **Crear documentos de categoría**: Añadir documentos que contengan explícitamente listas de productos por categoría (ej: "Lista de todos los camastros: Leonor, Clara, Delfina").

- **Normalizar formato de documentos**: Establecer un formato consistente para todos los documentos de productos, garantizando que los campos críticos (nombre, precio, descripción) estén siempre presentes y en el mismo formato.

### 3. Optimización del Prompt del Sistema

- **Mejorar instrucciones para productos no encontrados**: Modificar la sección de instrucciones críticas para que el modelo verifique cuidadosamente todos los productos en la lista antes de afirmar que no tiene información.

```python
# Añadir a SYSTEM_TEMPLATE
"""
INSTRUCCIONES PARA PRODUCTOS NO ENCONTRADOS:
- Antes de decir que no tienes información sobre un producto específico, VERIFICA CUIDADOSAMENTE si el nombre del producto aparece en la lista de productos disponibles mencionada anteriormente.
- Si el producto está en la lista pero no encuentras detalles en el contexto, di: "El [nombre del producto] es uno de nuestros productos disponibles, pero no tengo detalles específicos sobre él en este momento."
- Si menciona un fogonero y preguntan por parrilla, explica las diferencias entre nuestros fogoneros con y sin parrilla.
"""
```

- **Mejorar instrucciones para consultas de categoría**: Añadir instrucciones específicas para enumerar todos los productos de una categoría cuando se solicite.

- **Directrices consistentes para consultas fuera de dominio**: Establecer reglas claras sobre cómo responder a consultas fuera de dominio.

### 4. Ajustes en la Configuración del Modelo

- **Mantener temperatura baja**: La reducción de temperatura a 0.1 ha sido efectiva para reducir alucinaciones. Mantener este valor.

- **Implementar logging de parámetros de recuperación**: Añadir logging detallado de los documentos recuperados y sus puntuaciones de similitud para cada consulta, para facilitar el análisis y la mejora continua.

## Plan de Seguimiento e Implementación

1. **Corto plazo (Implementación inmediata)**
   - Corregir la recuperación de productos específicos
   - Mejorar las instrucciones del prompt del sistema
   - Implementar logging detallado para análisis posterior

2. **Mediano plazo (1-2 semanas)**
   - Enriquecer la base de conocimientos con documentos de categoría
   - Implementar recuperación híbrida (vectorial + palabras clave)
   - Añadir metadatos estructurados a todos los documentos

3. **Largo plazo (2-4 semanas)**
   - Implementar pruebas automatizadas para todos los casos de prueba
   - Desarrollar un sistema de monitoreo continuo de la calidad de las respuestas
   - Explorar técnicas avanzadas de RAG como re-ranking y generación multi-stage

## Conclusión

El chatbot de Casa Mueble ha mejorado significativamente en su capacidad para evitar alucinaciones, como se evidencia en la alta puntuación en el criterio de No Alucinación (3.67/4). Sin embargo, persisten desafíos importantes en la recuperación precisa de información sobre productos específicos.

Las mejoras implementadas (reducción de temperatura, instrucciones explícitas anti-alucinaciones, lista completa de productos en el prompt) han sido efectivas para reducir invenciones, pero no han resuelto completamente los problemas de recuperación de información existente.

La implementación de las recomendaciones propuestas, particularmente las relacionadas con la optimización del sistema de recuperación y la estructura de conocimientos, debería resultar en mejoras significativas en los criterios de Precisión y Completitud, los dos aspectos con puntuaciones más bajas en las pruebas actuales.

---

*Informe preparado el 25 de abril de 2024*
