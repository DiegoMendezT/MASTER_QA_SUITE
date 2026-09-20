# Entrega del Consejo Interno: hoja de ruta para la demo de Baterias + UI + API

## Resumen ejecutivo

Esta demo debe demostrar que la suite de QA puede ejecutar un escenario real de cliente en tres capas, todo en una misma corrida coherente:

1. Rastreo del sitio de Super Baterias y recopilación de evidencia
2. Flujos de verificación de UI
3. Flujos de verificación de API

El objetivo no es una demo genérica de automatización. La intención es una demostración más humana, clara y basada en evidencia, que muestre cómo la plataforma visita las landing pages reales de Super Baterias, valida el recorrido del usuario, confirma el comportamiento del backend y presenta los resultados en una sola experiencia de runner e informe.

La condición clave es simple: la demo debe verse limpia, explicable y confiable. La audiencia no va a aceptar capturas, textos o resultados viejos, genéricos, mal etiquetados o ajenos a la corrida seleccionada.

---

## Objetivo de negocio

La demo debe mostrar que la plataforma puede:

- Validar la experiencia del cliente en Baterias en páginas de inicio y de productos
- Probar que el contenido se sirve correctamente en español cuando se selecciona el caso de Baterias
- Ejecutar validaciones de UI en paralelo con la captura de evidencia de páginas de producto
- Revisar APIs como un flujo separado pero integrado dentro de la misma historia
- Presentar la evidencia en una sola vista sin mezclar por accidente artefactos de Trinus, Baterias, UI o API
- Soportar un modelo realista de ejecución paralela para dar confianza en la presentación final

---

## Alcance

### Incluido

- Página de inicio y landing pages de Super Baterias
- Rastreo de múltiples páginas con evidencia de captura hasta el footer
- Casos de validación de UI con capturas de evidencia
- Casos de validación de API con resúmenes estructurados
- Lógica de selección del runner que filtra la evidencia por los markers elegidos
- Reportes ordenados y empaquetado reproducible de evidencias
- Salida en español solo para el escenario de Super Baterias

### Fuera de alcance para esta demo

- Automatización del envío de correos
- Paneles históricos a largo plazo
- Configuración de despliegue empresarial más allá de la demo local
- Validación de otros sitios distintos a Baterias
- Instrumentación SEO o analítica profunda

---

## Evaluación del estado actual

### Lo que ya funciona

- El crawl de Baterias ya está implementado y puede capturar varias páginas de productos
- El proyecto puede generar evidencia de UI y API dentro del mismo flujo
- El runner de la app cuenta con lógica por markers para ejecuciones dirigidas
- La corrida puede ejecutarse con workers en paralelo para reforzar la demo
- Las rutas de artefactos de reportes y capturas ya están generando archivos reales en disco

### Lo que todavía exige disciplina

- La UI no debe mostrar artefactos viejos de una ejecución anterior
- El reporte debe reflejar la última corrida, no una iteración pasada
- El visor de evidencia debe filtrar por timestamp de la corrida y por markers seleccionados
- Solo el caso activo debe mostrar su resumen en español
- La demo debe evitar salidas accidentales del flujo default de Trinus
- El runner debe comunicar con claridad cuál es la selección activa y quiénes son sus evidencias

---

## Secuencia recomendada de la demo

### 1. Selección del runner

El usuario debe elegir uno o varios casos en una sola pantalla del runner. Un ejemplo de configuración sería:

- Super Baterias
- conjunto de UI
- conjunto de API
- Trinus solo si se selecciona explícitamente

El runner no debe incluir Trinus silenciosamente por defecto.

### 2. Modo de ejecución

La demo debe correr en un modo limpio y paralelo, acorde con el objetivo operativo.

- Preferir workers en paralelo para la ejecución combinada de UI y API
- Mantener la ejecución acotada a los markers pedidos
- Asegurar que la evidencia esté scopeada solo a esa corrida

### 3. Generación de evidencia

El sistema debe generar:

- Evidencia visual de la home de Baterias y páginas relevantes de productos
- Evidencia visual de ejecuciones UI exitosas
- Evidencia textual o de logs para validaciones API
- Una sección resumen breve con el estado de cada escenario

### 4. Capa de presentación

La UI de Streamlit debe mostrar:

- los markers seleccionados
- el resumen de la corrida
- capturas de Baterias en galería o por bloques
- capturas de UI para los casos activos
- tarjetas o logs de resumen de API
- sin dropdowns duplicados, sin defaults ocultos y sin bloques viejos

---

## Criterios funcionales de aceptación

### Caso Super Baterias

- Se visita y captura la home
- Se incluyen las landing pages raíz de productos
- Se capturan páginas relevantes de categorías
- Se toman capturas de pantalla a pantalla completa, incluyendo zonas bajas y footer
- El resumen en español solo aparece cuando se selecciona Super Baterias
- El resumen refleja el contenido real de Super Baterias y no un boilerplate de Trinus

### Caso UI

- Se capturan evidencias UI cuando las pruebas pasan
- La evidencia de UI es visible solo en la corrida activa
- No se muestran capturas viejas de ejecuciones anteriores
- Los resultados reflejan el escenario realmente seleccionado

### Caso API

- Las salidas de API se resumen con claridad en la UI o en el reporte
- La información de API es visible junto con la corrida seleccionada
- Los resultados no se mezclan con las capturas de UI

### Corrida combinada

- Los markers selectivos producen evidencia selectiva
- Las corridas mixtas muestran solo lo relevante
- La plataforma sigue siendo fácil de leer durante la demo en vivo

---

## Narrativa de la demo

### Historia sugerida para el equipo

"Esta demo muestra un único flujo de QA que cubre la tienda de Baterias, un flujo de validación de UI y otro de verificación de API, todo generado desde el mismo runner. Estamos mostrando evidencia real, no placeholders sintéticos. Las capturas muestran las páginas y la estructura que el cliente vería en la práctica. La capa de UI confirma el recorrido del front-end y la capa de API confirma el comportamiento de los contratos y endpoints."

Ese es el mensaje que queremos que la audiencia escuche.

---

## Riesgos y bloqueadores

### 1. Problema de evidencia stale

Riesgo: la UI muestra capturas o resultados viejos aunque ya hubo una nueva corrida.

Mitigación:

- Limpiar las carpetas de evidencia antes de cada corrida
- Filtrar por timestamp de inicio de la corrida
- Mostrar solo archivos del run activo

### 2. Contaminación entre casos

Riesgo: aparece salida de Trinus aunque se haya seleccionado Baterias, o viceversa.

Mitigación:

- Hacer de la selección de markers la fuente única de verdad
- Mantener los resúmenes por contenido bloqueados según el caso activo
- Separar las secciones por origen del escenario

### 3. Drift del reporte

Riesgo: el HTML del reporte no se refresca en el navegador aunque el archivo haya cambiado en disco.

Mitigación:

- Recargar la pestaña del navegador o abrir una nueva
- Verificar que la app se lanzara desde el punto de entrada correcto del repo
- Asegurarse de que el runner no esté sirviendo sesión vieja

### 4. Sobrecarga de la demo

Riesgo: mostrar demasiada información hace que la demo pierda claridad.

Mitigación:

- Mantener la demo default enfocada en Baterias + UI + API
- Mostrar solo los artefactos seleccionados para la corrida activa
- Usar resúmenes breves y capturas claras

---

## Hoja de ruta hacia la demo lista

### Fase 1: estabilidad y control

- Confirmar un arranque limpio desde el repo raíz
- Evitar problemas de puerto y estado stale de la app
- Mantener una sola página de runner explícita
- Quitar Trinus accidental o controles duplicados

### Fase 2: integridad de evidencia

- Limpiar capturas viejas antes de cada ejecución
- Filtrar la evidencia mostrada por hora de inicio y markers seleccionados
- Validar que el set de capturas de Baterias incluya varias páginas y no solo footer

### Fase 3: preparación del caso Baterias

- Incluir la home y las landing root de productos
- Agregar captura hasta el footer en las páginas relevantes
- Garantizar que el resumen en español aparezca solo cuando se selecciona Baterias
- Validar que el contenido corresponda al caso de Baterias y no a una plantilla genérica

### Fase 4: integración de UI y API

- Confirmar que la evidencia de UI es visible para la corrida activa
- Confirmar que la evidencia de API está agrupada y visible
- Probar selecciones mixtas: Baterias + UI + API
- Confirmar que no queda output stale de corridas anteriores

### Fase 5: pulido de la demo

- Revisión final de la distribución y legibilidad de la evidencia
- Preparar un script limpio con los outputs esperados
- Validar la corrida en una sesión nueva del navegador antes de la revisión de liderazgo

---

## Definición de hecho para la demo

La demo está lista cuando:

- la app arranca sin problemas desde el punto de entrada correcto
- el conjunto de markers seleccionados controla la salida
- Baterias muestra el resumen correcto en español y evidencia multi-página
- la evidencia de UI está presente y visualmente clara
- la evidencia de API está presente y legible
- no se filtran capturas ni reportes viejos en la demo
- la corrida final puede mostrarse en vivo y explicarse en menos de 5 minutos

---

## Preguntas para revisión del Consejo Interno

El Consejo Interno debería revisar antes de aprobar:

1. ¿El caso de Baterias es claramente la historia principal y más fuerte de esta demo?
2. ¿El conjunto de evidencia prueba una ejecución real a lo largo del recorrido del cliente?
3. ¿Los problemas de artefactos stale quedaron resueltos o siguen siendo una fuente de confusión?
4. ¿El runner está lo suficientemente limpio para una demo en vivo sin defaults ocultos ni controles duplicados?
5. ¿La evidencia de UI y API está integrada de manera que la historia sea clara?
6. ¿El requisito de idioma español fortalece la demo o corre el riesgo de complicar demasiado la localización?

---

## Revisión simulada del Consejo Interno

### Resumen de la revisión

"El Consejo aprueba la dirección de la demo, con un requisito claro: estabilizar antes de presentarla. La preocupación principal es la integridad de la evidencia: el sistema debe mostrar solo la corrida activa y el escenario seleccionado. El equipo debe reforzar la lógica de gating, limpiar artefactos viejos y asegurar que cada bloque de evidencia pueda vincularse claramente a una selección concreta."

### Acciones requeridas

- Corregir la fuga de evidencia vieja y filtrar por timestamp de la corrida
- Mantener Super Baterias como un escenario distinto y en español
- Conservar una lógica de selección centralizada para Trinus, Super Baterias, UI y API
- Confirmar que toda la evidencia de capturas incluye navegación más allá del footer
- Demostrar una corrida limpia de Streamlit en una sesión nueva del navegador

---

## Lectura de vuelta para el equipo Agile

"El Consejo Interno coincide con la dirección, pero pone el foco explícito en la calidad de la evidencia y la disciplina de la demo. Lo más importante no es solo que las pruebas pasen; es que el runner y la presentación de evidencias sean confiables durante una demo en vivo. El caso de Baterias debe ser claramente distinto, en español, multi-página y guiado por los markers seleccionados. Los casos de UI y API deben verse y estar correctamente acotados. El equipo debe limpiar artefactos viejos, evitar defaults ocultos y validar la app en una sesión nueva del navegador antes de la demo final."

---

## Postura recomendada para el próximo sprint

Esto debería tratarse como un sprint de estabilización para preparación de demo, con énfasis en:

- confiabilidad
- integridad de evidencia
- claridad narrativa
- confianza del usuario
- lógica limpia de selección

El objetivo final no es solo probar que la automatización funciona, sino demostrar que la historia del cliente es visible, creíble y presentable en tiempo real.

