import csv
import os
from typing import List, Dict, Optional, Tuple, Any

class GestorNotas:
    def __init__(self, archivo_activos="notas.csv", archivo_eliminados="notas_eliminadas.csv"):
        self.archivo_activos = archivo_activos
        self.archivo_eliminados = archivo_eliminados
        self.encabezados = ["ID", "Nombre", "Apellido", "Asignatura", "Nota"]
        
        # Crear archivos si no existen
        self._inicializar_archivos()
    
    def _inicializar_archivos(self):
        """Inicializa los archivos CSV si no existen."""
        for archivo in [self.archivo_activos, self.archivo_eliminados]:
            if not os.path.exists(archivo):
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.encabezados)
                    writer.writeheader()
    
    def _obtener_proximo_id(self) -> int:
        """Obtiene el próximo ID disponible."""
        registros = self.obtener_registros()
        if not registros:
            return 1
        return max(int(registro["ID"]) for registro in registros) + 1
    
    def obtener_registros(self) -> List[Dict[str, str]]:
        """Obtiene todos los registros activos."""
        try:
            with open(self.archivo_activos, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Error al leer los registros: {e}")
            return []
    
    def obtener_registros_eliminados(self) -> List[Dict[str, str]]:
        """Obtiene todos los registros eliminados."""
        try:
            with open(self.archivo_eliminados, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"Error al leer los registros eliminados: {e}")
            return []
    
    def agregar_registro(self, nombre: str, apellido: str, asignatura: str, nota: str) -> bool:
        """Agrega un nuevo registro."""
        try:
            id_nuevo = self._obtener_proximo_id()
            nuevo_registro = {
                "ID": str(id_nuevo),
                "Nombre": nombre,
                "Apellido": apellido,
                "Asignatura": asignatura,
                "Nota": nota
            }
            
            registros = self.obtener_registros()
            registros.append(nuevo_registro)
            
            with open(self.archivo_activos, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.encabezados)
                writer.writeheader()
                writer.writerows(registros)
            
            return True
        except Exception as e:
            print(f"Error al agregar registro: {e}")
            return False
    
    def buscar_registros(self, criterio: str, valor: str) -> List[Dict[str, str]]:
        """Busca registros por un criterio específico."""
        registros = self.obtener_registros()
        resultados = []
        
        for registro in registros:
            # Búsqueda parcial (contiene)
            if criterio in registro and valor.lower() in registro[criterio].lower():
                resultados.append(registro)
        
        return resultados
    
    def obtener_registro_por_id(self, id_registro: str) -> Optional[Dict[str, str]]:
        """Obtiene un registro específico por su ID."""
        registros = self.obtener_registros()
        for registro in registros:
            if registro["ID"] == id_registro:
                return registro
        return None
    
    def actualizar_registro(self, id_registro: str, datos: Dict[str, str]) -> bool:
        """Actualiza un registro existente."""
        registros = self.obtener_registros()
        actualizado = False
        
        for i, registro in enumerate(registros):
            if registro["ID"] == id_registro:
                # Preservar el ID original
                datos["ID"] = id_registro
                registros[i] = datos
                actualizado = True
                break
        
        if actualizado:
            try:
                with open(self.archivo_activos, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.encabezados)
                    writer.writeheader()
                    writer.writerows(registros)
                return True
            except Exception as e:
                print(f"Error al actualizar registro: {e}")
        
        return False
    
    def eliminar_registro(self, id_registro: str) -> bool:
        """Mueve un registro a la lista de eliminados."""
        registros = self.obtener_registros()
        registro_eliminado = None
        
        # Buscar y remover el registro
        for i, registro in enumerate(registros):
            if registro["ID"] == id_registro:
                registro_eliminado = registros.pop(i)
                break
        
        if registro_eliminado:
            try:
                # Actualizar archivo de registros activos
                with open(self.archivo_activos, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.encabezados)
                    writer.writeheader()
                    writer.writerows(registros)
                
                # Añadir a registros eliminados
                registros_eliminados = self.obtener_registros_eliminados()
                registros_eliminados.append(registro_eliminado)
                
                with open(self.archivo_eliminados, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.encabezados)
                    writer.writeheader()
                    writer.writerows(registros_eliminados)
                
                return True
            except Exception as e:
                print(f"Error al eliminar registro: {e}")
        
        return False
    
    def exportar_eliminados(self, ruta_destino: str) -> bool:
        """Exporta los registros eliminados a un archivo CSV externo."""
        registros_eliminados = self.obtener_registros_eliminados()
        
        try:
            with open(ruta_destino, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.encabezados)
                writer.writeheader()
                writer.writerows(registros_eliminados)
            return True
        except Exception as e:
            print(f"Error al exportar registros eliminados: {e}")
            return False
    
    def ordenar_registros(self, criterio: str, ascendente: bool = True) -> List[Dict[str, str]]:
        """Ordena los registros según un criterio."""
        registros = self.obtener_registros()
        
        # Función de ordenamiento
        def clave_ordenamiento(registro):
            valor = registro[criterio]
            # Si es numérico, convertir para comparación numérica
            if criterio == "ID" or criterio == "Nota":
                return int(valor)
            # Si es texto, ordenar alfabéticamente
            return valor.lower()
        
        return sorted(registros, key=clave_ordenamiento, reverse=not ascendente)
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas básicas de los registros activos."""
        registros = self.obtener_registros()
        total_estudiantes = len(registros)
        
        if total_estudiantes == 0:
            return {
                "total_estudiantes": 0,
                "promedio_general": 0.0,
                "nota_maxima": 0,
                "nota_minima": 0
            }
        
        # Calcular estadísticas
        notas = [int(reg["Nota"]) for reg in registros]
        promedio = sum(notas) / len(notas) if notas else 0
        
        return {
            "total_estudiantes": total_estudiantes,
            "promedio_general": round(promedio, 2),
            "nota_maxima": max(notas) if notas else 0,
            "nota_minima": min(notas) if notas else 0
        }