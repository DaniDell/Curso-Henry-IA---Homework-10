# Plan de migración: Integración de Supabase para Casa del Mueble

## Objetivo

- Subir la base de conocimiento (productos y FAQs) a Supabase para que el chatbot la consulte desde allí, en vez de archivos locales.
- Guardar el historial de conversaciones del chatbot en Supabase para trazabilidad y análisis.

---

## 1. Evaluación de riesgos

- **Exposición de datos sensibles:**
  - Usar solo la API Key pública para lectura desde el chatbot.
  - Limitar permisos de escritura solo a endpoints necesarios (conversaciones).
- **Costos y límites:**
  - Revisar límites de almacenamiento y requests de Supabase (plan gratuito vs. pago).
- **Latencia:**
  - Consultas a Supabase pueden ser más lentas que FAISS local, pero ganan en centralización y acceso multiusuario.
- **Disponibilidad:**
  - Si Supabase cae, el chatbot no podrá responder ni guardar conversaciones.
- **Consistencia:**
  - Asegurar que la base de conocimiento en Supabase esté sincronizada con la local durante la transición.

---

## 2. Pasos de migración

### 2.1. Modelado y creación de tablas en Supabase
- Crear tablas para productos, FAQs y conversaciones.
- Definir esquemas y tipos de datos.
- Otorgar permisos adecuados (lectura pública, escritura restringida).

### 2.2. Carga inicial de datos
- Exportar productos y FAQs a CSV/JSON.
- Usar el panel de Supabase o scripts para importar los datos.
- Validar integridad y formato.

### 2.3. Refactorización del chatbot
- Modificar el pipeline para consultar productos/FAQs desde Supabase vía REST API.
- Mantener fallback a FAISS local durante pruebas.
- Implementar guardado de conversaciones en Supabase.

### 2.4. Pruebas y validación
- Probar recuperación de productos y FAQs desde Supabase.
- Probar guardado y consulta de conversaciones.
- Medir latencia y comparar con FAISS local.

### 2.5. Despliegue y monitoreo
- Hacer backup de la base local antes de migrar.
- Habilitar logs y alertas en Supabase.
- Documentar endpoints y credenciales.

---

## 3. Reversibilidad
- Mantener la base local y el pipeline FAISS como respaldo durante la transición.
- Documentar cómo revertir a la versión anterior si hay problemas.

---

## 4. Notas
- No subir claves privadas ni datos sensibles a Supabase.
- Revisar compliance y privacidad según el uso de datos de clientes.
- Considerar paginación y filtros en las consultas para eficiencia.

---

## 5. Próximos pasos
- [ ] Crear esquemas SQL para las tablas.
- [ ] Escribir scripts de importación/exportación.
- [ ] Refactorizar el chatbot para consumir Supabase.
- [ ] Probar y documentar todo el flujo.
