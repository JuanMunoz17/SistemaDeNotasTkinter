import re
from typing import Tuple, Optional

class Validador:
    @staticmethod
    def validar_texto_alfabetico(texto: str) -> bool:
        """Valida que el texto contenga solo caracteres alfabéticos y espacios."""
        if not texto or not texto.strip():
            return False
        
        # Permitir letras, espacios y caracteres acentuados
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
        return bool(re.match(patron, texto))
    
    @staticmethod
    def validar_alfanumerico(texto: str) -> bool:
        """Valida que el texto contenga caracteres alfanuméricos, espacios y algunos símbolos."""
        if not texto or not texto.strip():
            return False
        
        # Permitir letras, números, espacios y algunos símbolos comunes
        patron = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-_.,]+$'
        return bool(re.match(patron, texto))
    
    @staticmethod
    def validar_nota(texto: str) -> Tuple[bool, Optional[str]]:
        """Valida que el texto sea un número entero entre 0 y 50."""
        if not texto or not texto.strip():
            return False, "La nota no puede estar vacía"
            
        try:
            nota = int(texto)
            if 0 <= nota <= 50:
                return True, None
            else:
                return False, "La nota debe estar entre 0 y 50"
        except ValueError:
            return False, "La nota debe ser un número entero"
    
    @staticmethod
    def validar_campos_estudiante(nombre: str, apellido: str, asignatura: str, nota: str) -> Tuple[bool, str]:
        """Valida todos los campos de un estudiante."""
        # Validar nombre
        if not nombre or not nombre.strip():
            return False, "El nombre no puede estar vacío"
        if not Validador.validar_texto_alfabetico(nombre):
            return False, "El nombre solo puede contener letras y espacios"
        
        # Validar apellido
        if not apellido or not apellido.strip():
            return False, "El apellido no puede estar vacío"
        if not Validador.validar_texto_alfabetico(apellido):
            return False, "El apellido solo puede contener letras y espacios"
        
        # Validar asignatura
        if not asignatura or not asignatura.strip():
            return False, "La asignatura no puede estar vacía"
        if not Validador.validar_alfanumerico(asignatura):
            return False, "La asignatura contiene caracteres no permitidos"
        
        # Validar nota
        es_valida, mensaje = Validador.validar_nota(nota)
        if not es_valida:
            return False, mensaje
            
        return True, "Todos los campos son válidos"