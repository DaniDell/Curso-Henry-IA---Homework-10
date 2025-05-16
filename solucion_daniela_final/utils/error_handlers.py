"""
Utilidades para manejar errores en la aplicación.
"""
import logging
import functools
from typing import Callable, Any

logger = logging.getLogger(__name__)

def error_handler(func: Callable) -> Callable:
    """
    Decorador para manejar excepciones en funciones y registrarlas.
    
    Args:
        func (Callable): La función a decorar
        
    Returns:
        Callable: Función decorada con manejo de excepciones
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {str(e)}", exc_info=True)
            return None
            
    return wrapper