import os
import sys
from loguru import logger
    
def setup_logging():
    # 1. Definir la ruta de la carpeta de logs
    LOG_DIR = "logs"
    
    # 2. CREAR LA CARPETA AUTOMÁTICAMENTE (Esto es lo que preguntabas)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"Carpeta '{LOG_DIR}' creada con éxito.")

    # 3. Limpiar configuraciones previas para no duplicar logs
    logger.remove()

    # 4. Configurar el log de CONSOLA (lo que ves en la terminal)
    logger.add(sys.stderr, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")

    # 5. Configurar el archivo de AUDITORÍA (Acciones de usuario)
    logger.add(
        os.path.join(LOG_DIR, "audit.log"),
        filter=lambda record: "audit" in record["extra"],
        format="{time:YYYY-MM-DD HH:mm:ss} | {extra[user]} | {message}",
        rotation="10 MB",  # Cuando llegue a 10MB, crea uno nuevo
        retention="1 month" # Borra logs de más de un mes
    )

    # 6. Configurar el archivo de ERRORES (Solo errores del sistema)
    logger.add(
        os.path.join(LOG_DIR, "errors.log"),
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
        backtrace=True, # Muestra el error completo para debuguear
        diagnose=True
    )

    return logger