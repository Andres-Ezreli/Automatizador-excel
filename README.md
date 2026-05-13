# Generador y Asignador de Stickers en Soportes (SAYCO)

Este proyecto automatiza la asignación, estampado de coordenadas (X,Y) y clasificación de documentos PDF y archivos MP3 basados en metadatos de un archivo Excel. Combina macros de VBA con scripts de Python, con soporte nativo para entornos sincronizados en la nube (OneDrive / SharePoint).

## 🚀 Requisitos Previos

El equipo debe tener instalado **Python 3.10+** y las siguientes librerías. Abra la consola (CMD) y ejecute:
`pip install PyMuPDF openpyxl`

## 📂 Estructura del Directorio (Importante)

El sistema utiliza una arquitectura de "ancla" para encontrar el código de Python sin importar dónde esté guardado el Excel. Mantenga esta estructura:

[Carpeta Raíz del Proyecto]
 ├── stamper/               # MOTOR DE PYTHON: Aquí van todos los scripts .py
 ├── Carlos Vives/          # Carpeta de Proyecto 1 (Ejemplo)
 │   ├── INVENTARIO.xlsm      # El Archivo Excel del artista
 │   ├── Input/               # PDFs crudos
 │   └── Output/              # ANCLA: PDFs estampados y MP3s caen aquí
 └── Otro Artista/          # Carpeta de Proyecto 2
     ├── INVENTARIO.xlsm      
     ├── Input/               
     └── Output/              

## ⚙️ Configuración Inicial (¡Muy Importante!)

1. **La Ruta Ancla:** Abra su archivo Excel, vaya a la hoja `STICKERmaker` y haga clic en **Obtener Ruta de Salida**. Seleccione la carpeta `Output` que se encuentra *al lado* de su archivo Excel. 
   *(Nota: El sistema utilizará esta ruta para encontrar mágicamente la carpeta `stamper`, saltándose los errores web de OneDrive).*
2. **Habilitar Macros:** Asegúrese de que Excel tenga habilitada la ejecución de macros.

## 🖨️ Estampado de PDFs (Stickers)

Superpone una imagen generada desde las celdas de Excel hacia un PDF de origen.

- **Posicionamiento Dinámico:** Modifique las columnas `Eje Y` (Distancia vertical) y `Eje X` (Distancia horizontal) en la hoja de Excel. Si los deja en blanco, asume `0.0` (Esquina superior izquierda).
- **Proceso Individual:** Seleccione su PDF con "Examinar" y haga clic en "Pegar Sticker [Tipo]" para procesar un solo documento.
- **Proceso Masivo:** Haga clic en "Pegar Todos Los Stickers" para procesar todo a la vez.

## 🎵 Envío de Fonogramas (MP3)

Para agrupar audios por código de obra sin usar Python (100% nativo en Excel):
1. Haga clic en **Obtener Ruta de Mp3** y seleccione el archivo de audio fuente.
2. Haga clic en **Ruta de Carpeta Fonograma** y seleccione la carpeta padre (ej. `Output/FONOGRAMAS`).
3. Digite el código numérico de la obra en la celda (ej. `12576`).
4. Haga clic en **Enviar Fonogramas**. El sistema creará la subcarpeta y copiará el MP3 allí.