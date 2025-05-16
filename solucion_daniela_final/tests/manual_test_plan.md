# Plan de Pruebas Manuales para Casa Mueble Chatbot

## Objetivo
Evaluar la calidad de las respuestas del chatbot de Casa Mueble, verificando la precisión, relevancia y naturalidad de las respuestas generadas.

## Criterios de Evaluación
- **Precisión**: ¿La respuesta contiene información correcta según la base de conocimientos?
- **Relevancia**: ¿La respuesta aborda directamente la consulta del usuario?
- **Completitud**: ¿La respuesta proporciona toda la información necesaria?
- **Naturalidad**: ¿La respuesta parece natural y conversacional?
- **Hallucination**: ¿El chatbot inventa información que no está en la base de conocimientos?

## Escala de Puntuación
Para cada criterio, use la siguiente escala:
- 1: No cumple
- 2: Cumple parcialmente
- 3: Cumple satisfactoriamente
- 4: Cumple excelentemente

## Casos de Prueba

### 1. Consultas sobre Productos Específicos
| ID | Pregunta | Respuesta Esperada | P | R | C | N | H | Observaciones |
|----|----------|-------------------|---|---|---|---|---|---------------|
| P1 | ¿Qué características tiene el Camastro Leonor? | Descripción detallada del Camastro Leonor | | | | | | |
| P2 | ¿Cuánto cuesta el Sillón Clemente? | Precio correcto del Sillón Clemente | | | | | | |
| P3 | ¿El fogonero Perikles viene con parrilla? | Información correcta sobre accesorios | | | | | | |

### 2. Consultas sobre Categorías de Productos
| ID | Pregunta | Respuesta Esperada | P | R | C | N | H | Observaciones |
|----|----------|-------------------|---|---|---|---|---|---------------|
| C1 | ¿Qué tipos de mesas ofrecen? | Lista de mesas disponibles | | | | | | |
| C2 | ¿Qué opciones de fogoneros tienen? | Diferentes modelos de fogoneros | | | | | | |
| C3 | Muéstrame todos los camastros | Lista completa de camastros | | | | | | |

### 3. Consultas sobre Políticas y Servicios (FAQs)
| ID | Pregunta | Respuesta Esperada | P | R | C | N | H | Observaciones |
|----|----------|-------------------|---|---|---|---|---|---------------|
| F1 | ¿Cuál es la política de devolución? | Política de devolución completa | | | | | | |
| F2 | ¿Hacen envíos a domicilio? | Información sobre envíos | | | | | | |
| F3 | ¿Tienen garantía sus productos? | Detalles de garantía | | | | | | |

### 4. Consultas Ambiguas o Incompletas
| ID | Pregunta | Respuesta Esperada | P | R | C | N | H | Observaciones |
|----|----------|-------------------|---|---|---|---|---|---------------|
| A1 | Quiero comprar muebles | Solicitud de clarificación o presentación general | | | | | | |
| A2 | ¿Cuánto cuesta? | Solicitud de especificación del producto | | | | | | |
| A3 | ¿Tienen descuentos? | Información general sobre promociones actuales | | | | | | |

### 5. Consultas Fuera del Dominio
| ID | Pregunta | Respuesta Esperada | P | R | C | N | H | Observaciones |
|----|----------|-------------------|---|---|---|---|---|---------------|
| O1 | ¿Cuál es la capital de Francia? | Indicación de que no es relevante para Casa Mueble | | | | | | |
| O2 | Cuéntame un chiste | Redirección amable hacia temas de muebles | | | | | | |
| O3 | ¿Puedes programar en Python? | Aclaración sobre el propósito del chatbot | | | | | | |

## Instrucciones para Pruebas
1. Para cada caso de prueba, anote la respuesta real del chatbot
2. Evalúe cada respuesta según los 5 criterios (P=Precisión, R=Relevancia, C=Completitud, N=Naturalidad, H=No Alucinación)
3. Añada observaciones específicas, especialmente si detecta problemas
4. Para cada hallucination detectada, documente qué información específica fue inventada

## Análisis de Resultados
Después de completar todas las pruebas, calcule las puntuaciones promedio para cada criterio y analice:
- Criterios con puntuaciones más bajas (áreas a mejorar)
- Patrones en las hallucinations (si existen)
- Tipos de consultas que generan respuestas de menor calidad

## Recomendaciones
Basado en los resultados, documente recomendaciones específicas para mejorar:
- Configuración del chatbot (temperatura, top_p, etc.)
- Contenido de la base de conocimientos
- Sistema de recuperación (FAISS)
- Prompts del sistema
