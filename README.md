# Web Scraper Notas UNSA
- ![Web Scraper](/webscrapper.png)

Este proyecto es un scraper web diseñado para extraer las notas de los estudiantes de la página de Notas UNSA. El scraper realiza una solicitud HTTP a la página, extrae los datos relevantes y muestra cuántas notas tiene el usuario.

## Estructura del Proyecto

```
web-scraper-notas-unsa
├── src
│   ├── scraper.py         # Punto de entrada del scraper
│   └── utils
│       └── __init__.py    # Funciones auxiliares para el scraper
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación del proyecto
```
- ![Web Main](/webscrappermain.png)
## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd web-scraper-notas-unsa
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar el scraper, utiliza el siguiente comando:

```
python src/scraper.py
```

Asegúrate de tener acceso a la página de Notas UNSA y de que la estructura de la página no haya cambiado, ya que esto podría afectar la funcionalidad del scraper.
