# Investigación técnica revisada — Proyecto Júpiter

## 1. Enfoque general

**Proyecto Júpiter** será una aplicación móvil basada en IA generativa que recogerá información autorizada del usuario para construir una memoria personal digital.

### Fuentes principales de datos

- Uso de aplicaciones.
- Ubicación.
- Google Calendar.
- Posiblemente Gmail.
- Texto introducido por el usuario.
- Audio / notas de voz.

### Objetivo inicial del MVP

- Generar un resumen semanal de la actividad del usuario.
- Permitir conversar con esa memoria mediante un chat.

El enfoque inicial será **Android**, por ser más flexible que iOS para permisos, estadísticas de uso, ubicación y procesos en segundo plano.

---

## 2. Uso de aplicaciones en Android

Android tiene una funcionalidad similar a **Tiempo de Uso** de iOS llamada **Bienestar Digital**.

Nuestra app no accedería directamente a Bienestar Digital, sino a una fuente similar mediante la API `UsageStatsManager`.

Esta API permite obtener:

- Apps utilizadas.
- Tiempo de uso por aplicación.
- Eventos de apertura/cierre.
- Horarios aproximados de actividad.
- Desbloqueos del dispositivo.

Esto permitiría construir una línea temporal básica del día del usuario.

### Limitación importante

Podemos saber que el usuario ha usado una app, pero no necesariamente qué ha hecho dentro de ella.

### Permiso necesario

Para acceder a estas estadísticas, la app necesita el permiso `android.permission.PACKAGE_USAGE_STATS`.

Este permiso debe activarse manualmente desde:

> Ajustes > Acceso a datos de uso > activar permiso para nuestra app

---

## 3. Ubicación del usuario en Android

La recogida de ubicación en Android es posible, pero es una de las partes más delicadas del proyecto porque Android restringe mucho los procesos de localización en segundo plano.

No basta con crear una app que “pida la ubicación” y ya está. Si queremos recibir coordenadas de forma periódica y fiable, hay que usar una arquitectura específica.

### 3.1. Fused Location Provider

Para obtener la ubicación se utilizaría **Fused Location Provider**, una API de localización de Google Play Services.

Esta API no depende únicamente del GPS. Combina varias fuentes de ubicación del dispositivo:

- GPS.
- WiFi.
- Antenas móviles.
- Sensores del dispositivo.

Su ventaja es que permite pedir ubicación con distintos niveles de precisión y consumo de batería. Por ejemplo, podemos configurar si queremos máxima precisión o una localización más aproximada pero menos costosa.

En nuestro caso, serviría para obtener coordenadas periódicas del usuario y convertirlas después en contexto útil para la memoria personal:

- Casa.
- Trabajo.
- Universidad.
- Gimnasio.
- Desplazamientos.
- Rutinas semanales.

### 3.2. Foreground Service

Android no permite que una app cualquiera esté recogiendo ubicación constantemente en segundo plano como si nada.

Para hacer una operación continuada de localización, habría que usar un **Foreground Service**.

Un Foreground Service es un servicio que Android considera activo, visible e importante para el usuario.

Esto no significa necesariamente que la pantalla de la app tenga que estar abierta todo el tiempo. Lo que significa es que el sistema muestra una notificación permanente indicando que la app está realizando una tarea en primer plano.

Ejemplo de notificación:

> Proyecto Júpiter está registrando ubicación para construir tu memoria semanal.

Esto le indica al sistema Android que no debe tratar ese proceso como una tarea oculta cualquiera que puede cerrar fácilmente para ahorrar batería.

En el caso de la ubicación, habría que declarar el servicio en el `AndroidManifest.xml` con el tipo específico:

```xml
android:foregroundServiceType="location"
```

Esto indica que el servicio en primer plano se va a utilizar específicamente para localización.

### 3.3. Permisos necesarios

Para obtener ubicación en primer plano se puede usar:

- `ACCESS_FINE_LOCATION`, si queremos ubicación precisa.
- `ACCESS_COARSE_LOCATION`, si basta con ubicación aproximada.

Para obtener ubicación cuando el usuario no está interactuando directamente con la app, sería necesario:

- `ACCESS_BACKGROUND_LOCATION`

Este permiso es especialmente sensible. En versiones modernas de Android, el usuario normalmente debe activarlo manualmente desde los ajustes del sistema, seleccionando una opción tipo:

> Permitir todo el tiempo

### 3.4. Flujo correcto de permisos

El flujo recomendable sería:

1. Pedir primero permiso de ubicación en primer plano.
2. Explicar al usuario para qué se usará la ubicación.
3. Si la funcionalidad lo requiere, pedir después ubicación en segundo plano.
4. Dirigir al usuario a los ajustes de Android para activar “Permitir todo el tiempo”.
5. Mostrar una notificación permanente mientras el Foreground Service esté activo.
6. Permitir que el usuario pause o desactive este seguimiento desde la app.

### 3.5. Limitaciones importantes

Aunque usemos un Foreground Service, Android puede seguir aplicando restricciones de batería.

Por eso se pueden estudiar medidas adicionales como:

- Pedir al usuario que excluya la app de la optimización de batería.
- Usar `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`.
- Usar `WakeLock` solo en casos justificados, para evitar que la CPU se duerma mientras se procesan o envían coordenadas.

Estas opciones deben usarse con cuidado porque aumentan el consumo de batería y pueden generar rechazo en el usuario.

### 3.6. Recomendación para el MVP

Para el MVP no conviene plantear un rastreo agresivo 24/7.

Lo más razonable sería usar ubicación de forma limitada y transparente:

- Ubicación periódica.
- Detección aproximada de lugares relevantes.
- Registro de rutinas generales.
- Posibilidad de desactivar la función.
- Explicación clara de qué se guarda y para qué.

La idea no debe ser “vigilar al usuario”, sino añadir contexto a su memoria personal.

Ejemplo de uso en el resumen semanal:

> El lunes por la mañana estuviste en la universidad, después pasaste por el gimnasio y por la tarde estuviste en casa trabajando con el ordenador.

---

## 4. APIs de Google

Las integraciones de Google pueden aportar mucho valor, pero conviene priorizar.

### 4.1. Google Calendar

Es la integración más clara para el MVP.

Permite obtener:

- Eventos.
- Fechas.
- Horarios.
- Títulos.
- Descripciones.
- Lugares.

Encaja muy bien con la memoria semanal.

### 4.2. Gmail

Gmail puede aportar contexto real de trabajo, gestiones y comunicaciones importantes.

Sin embargo, es mucho más sensible que Calendar.

Para el MVP puede investigarse, pero sería mejor dejarlo como integración avanzada.

### 4.3. Google Keep / notas

Queda pendiente confirmar si existe una vía oficial, estable y sencilla para integrarlo.

---

## 5. Configuración de APIs de Google

Pasos generales:

1. Crear proyecto en Google Cloud Console.
2. Activar Gmail API y Google Calendar API.
3. Crear credenciales OAuth.
4. Vincular el SHA-1 de la app Android.
5. Integrar Google Identity Services.
6. Solicitar scopes concretos.
7. Obtener token de acceso.
8. Consultar las APIs desde la app o desde el backend.

En producción habría que superar la verificación de Google si se accede a datos sensibles.

---

## 6. Desarrollo móvil con Expo / React Native

Para el desarrollo móvil se utilizará inicialmente **Expo + React Native**.

### Ventajas

- Desarrollo rápido.
- Uso de JavaScript / TypeScript.
- No requiere empezar directamente con Kotlin o Swift.
- Permite probar la app en el móvil escaneando un QR.
- Gran parte del código puede reutilizarse para Android e iOS.

### Matiz técnico importante

Expo/React Native no traduce literalmente JavaScript a Kotlin o Swift.

La app incorpora un motor JavaScript, normalmente **Hermes**, que ejecuta el código JS/TS dentro del dispositivo.

React Native conecta ese código con componentes nativos de Android/iOS.

La experiencia de desarrollo es parecida a un “Live Server” para móvil: escaneas un QR y ves los cambios directamente en el teléfono durante el desarrollo.

### Limitación

Para funcionalidades avanzadas como `UsageStatsManager`, Foreground Services o permisos especiales, puede hacer falta usar:

- Expo Development Builds.
- Config plugins.
- Código nativo Android.

---

## 7. Modelos de lenguaje candidatos

### 7.1. DeepSeek V3

Candidato interesante por coste y rendimiento.

Puntos clave:

- Ventana de contexto de 128k tokens.
- Buen razonamiento lógico.
- Buen análisis de datos.
- Coste bajo frente a modelos propietarios grandes.
- Útil para resumir, clasificar y conversar con la memoria.

Pendiente:

- Verificar licencia exacta.
- Confirmar precios actuales.
- Comprobar condiciones de uso comercial y privacidad.

---

### 7.2. Llama 3.1 / 3.3

Candidato interesante si queremos mayor control de infraestructura.

Puntos clave:

- Ventana de contexto amplia.
- Posibilidad de ejecución en servidor propio o nube privada.
- Mayor control sobre datos del usuario.
- Mejor encaje potencial con RGPD.

Matices:

- No toda la familia Llama es multimodal.
- Llama 3.3 es principalmente texto.
- La licencia no es open-source pura tipo MIT/Apache, sino una licencia propia de Meta.

---

### 7.3. Qwen 2.5 / Qwen 2.5-Audio / Qwen2.5-Omni

Qwen es una familia de modelos interesante por sus capacidades abiertas y multimodales.

Qwen 2.5 puede servir como modelo general de texto.

Qwen2.5-Audio / Qwen2.5-Omni resultan especialmente interesantes porque pueden procesar audio directamente.

Esto significa que no solo trabajan con una transcripción escrita, sino que pueden interpretar señales acústicas del habla:

- Tono.
- Ritmo.
- Pausas.
- Intensidad.
- Voz temblorosa.
- Posible llanto.
- Contradicciones entre lo que se dice y cómo se dice.

Ejemplo:

Si un usuario dice “estoy bien” llorando, un modelo audio-multimodal podría detectar que el contenido verbal y la expresión vocal no encajan.

Podría interpretar algo como:

> El usuario afirma estar bien, pero la voz sugiere tristeza, tensión o angustia.

Esto sería muy útil para una memoria personal más rica, porque permitiría analizar no solo el contenido de una nota de voz, sino también el estado emocional aparente.

### Limitación importante

Estas inferencias no deben tratarse como verdades absolutas ni como diagnóstico emocional.

Son señales probabilísticas y pueden fallar por:

- Ruido.
- Acento.
- Mala calidad de audio.
- Contexto.
- Diferencias individuales en la forma de expresarse.

Para el MVP, lo más simple sería:

> Audio → transcripción → LLM

Y dejar el análisis directo de audio como mejora avanzada.

---

## 8. Arquitectura recomendada para el MVP

### 8.1. App móvil

Construida con Expo / React Native.

Funciones principales:

- Login.
- Chat con la memoria.
- Pantalla de resumen semanal.
- Ajustes de permisos.
- Entrada manual de texto/audio.
- Visualización básica de datos recogidos.

### 8.2. Backend

Responsable de:

- Recibir datos del móvil.
- Guardar eventos.
- Procesar información.
- Enviar datos al modelo de IA.
- Generar resúmenes.
- Responder preguntas del usuario.

### 8.3. Base de datos

Se recomienda combinar:

- Base de datos relacional para datos estructurados.
- Base de datos vectorial para recuerdos, notas, resúmenes y búsqueda semántica.

### Datos estructurados

- Uso de apps.
- Eventos de calendario.
- Ubicación.
- Fechas.
- Horarios.

### Datos semánticos

- Notas.
- Audios transcritos.
- Resúmenes.
- Recuerdos generados por IA.

---

## 9. Recomendación para el MVP

Para no sobredimensionar el proyecto, el MVP debería demostrar valor con pocas fuentes bien elegidas.

### Prioridad recomendada

1. Expo / React Native.
2. Google Calendar.
3. Uso de apps con `UsageStatsManager`.
4. Entrada manual de texto.
5. Entrada de audio con transcripción.
6. Resumen semanal generado por IA.
7. Chat con la memoria personal.

### Dejar para una fase posterior

- Gmail.
- Ubicación constante.
- Análisis emocional directo del audio.
- Qwen2.5-Omni en producción.
- Despliegue propio de modelos.
- App iOS completa.
- Auditorías avanzadas.

## Idea clave

No construir desde el principio una IA que lo sabe todo del usuario, sino una memoria semanal útil, autorizada, consultable y técnicamente viable.
