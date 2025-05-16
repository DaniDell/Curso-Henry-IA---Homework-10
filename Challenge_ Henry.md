# Tarea: Sistema de Atención al Cliente Automatizado con LangChain

## Objetivo

Desarrollar una aplicación utilizando LangChain que sea capaz de procesar solicitudes de clientes y decidir el método más apropiado para responder, ya sea consultando una base de datos, una base de conocimientos, o utilizando el conocimiento integrado en un modelo de lenguaje de gran escala (LLM).

## Requerimientos

El sistema debe ser capaz de identificar y enrutar las solicitudes a uno de los siguientes flujos de trabajo:

1. **Consulta de Balance de Cuentas:** Extraer información de un archivo CSV basado en un ID específico proporcionado por el usuario.
   
2. **Información General sobre Procesos Bancarios:** Recuperar y generar respuestas a partir de una base de conocimientos sobre procedimientos bancarios específicos como abrir cuentas o realizar transferencias.

3. **Respuestas Generales:** Utilizar el conocimiento del LLM para responder preguntas generales que no requieren consulta de datos externos.

## Implementación Sugerida

- **Indexación de la Base de Conocimientos:** Utilizar el modelo `sentence-transformers/all-MiniLM-L6-v2` para generar embeddings de la base de conocimientos, que luego pueden ser indexados utilizando FAISS. Esta indexación permite realizar búsquedas eficientes y relevantes dentro de la base de conocimientos para responder consultas específicas.

- **Almacenamiento de Vectores:** Se recomienda almacenar la base de datos de vectores localmente y cargarla mediante FAISS para facilitar el acceso rápido y eficiente durante las consultas de recuperación.

- **LangChain:** Utilizar LangChain para integrar y coordinar las diferentes herramientas y modelos, incluyendo el manejo del modelo de lenguaje, la configuración del retriever, y la ejecución de consultas a la base de datos.

## Archivos y Directorios

- **`knowledge\_base/`:** Debe contener archivos con información detallada sobre diversos procesos bancarios.
- **`saldos.csv`:** Archivo CSV que almacena los balances de cuentas asociados con IDs de cédula específicos.


## Flexibilidad del Lenguaje de Programación

Este proyecto puede ser implementado utilizando JavaScript o Python, según la preferencia del desarrollador. Ambos lenguajes son adecuados para trabajar con LangChain y las herramientas asociadas, y la elección puede depender de la familiaridad del desarrollador con el lenguaje o de requisitos específicos del entorno de ejecución.

## Ejecución y Gestión de la Solución

La solución implementada se encuentra en el directorio `/solucion`. Para probar la solución, puedes ejecutar el comando:

```bash
pipenv shell

python3 solucion/main.py
```

Antes de ejecutar la solución, asegúrate de instalar todas las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

Si necesitas reindexar la base de conocimientos, puedes hacerlo ejecutando el script `indexer.py` que se encuentra en el mismo directorio:

```bash
python3 solucion/indexer.py
```

Este script generará un directorio `index` que contiene la base de datos de vectores FAISS. Esto es útil si has realizado cambios en la base de conocimientos y necesitas actualizar los índices para reflejar esos cambios.

## Entrega

- Código fuente de la aplicación.
- Documentación que describa el diseño del sistema, cómo funciona y cómo se deben ejecutar las pruebas.
- Archivo con pruebas automatizadas.