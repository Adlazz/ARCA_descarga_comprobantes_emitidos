# ARCA Automatización - Descarga de Comprobantes Emitidos (Ex AFIP)

Este script automatiza la descarga de comprobantes emitidos desde el portal de ARCA (Agencia de Recaudación y Control Aduanero) de Argentina.

## Descripción

El script realiza las siguientes tareas de forma automática:
- Inicio de sesión en el portal de ARCA
- Navegación hasta la sección de comprobantes emitidos
- Ingreso del rango de fechas especificado por el usuario
- Descarga de los comprobantes en formato Excel
- Todo el proceso se realiza de manera automatizada utilizando Selenium WebDriver

## Requisitos Previos

### 1. Instalación de Python
Si aún no tienes Python instalado:
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, asegúrate de marcar la casilla "Add Python to PATH"

### 2. Instalación de Dependencias

**Usando CMD (Símbolo del Sistema):**
```cmd
python -m pip install selenium webdriver-manager keyboard
```

**Usando bash:**
```bash
pip install selenium webdriver-manager keyboard
```

## Configuración

En el archivo `main.py`, necesitarás configurar:
- CUIT del contribuyente
- Contraseña de ARCA

## Uso

1. Ejecutar el script:
```bash
python main.py
```

2. El programa solicitará:
   - Fecha desde (formato: DD/MM/YYYY)
   - Fecha hasta (formato: DD/MM/YYYY)

3. El proceso se ejecutará automáticamente y descargará el archivo Excel con los comprobantes

4. Para finalizar el proceso, presionar la tecla 'Esc'

## Características

- Validación de formato de fechas
- Manejo automático del navegador Chrome
- Rotación de User Agents para evitar bloqueos
- Captura de pantalla automática en caso de errores
- Logs detallados del proceso
- Interfaz de línea de comandos simple

## Notas

- El script utiliza Chrome WebDriver. Asegúrese de tener Google Chrome instalado
- Los archivos Excel se descargarán en la carpeta de descargas predeterminada de su navegador
- En caso de error, se generarán capturas de pantalla para facilitar la resolución de problemas

## Escalabilidad

Este script puede ser adaptado para manejar múltiples contribuyentes de forma simultánea o secuencial, permitiendo la automatización masiva de descargas de comprobantes para diferentes CUITs. Para personalizaciones específicas o implementaciones a medida, no dude en contactarnos.

## Advertencia

Este script es para uso personal y debe utilizarse de manera responsable y dentro de los términos de servicio de ARCA.

## Contacto

Para consultas sobre personalizaciones o implementaciones específicas:
- Email: adrianlazzarini@gmail.com
- Telefono: +54 3704085579
