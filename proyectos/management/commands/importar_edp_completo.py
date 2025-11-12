from django.core.management.base import BaseCommand
from empresas.models import Empresa
from proyectos.models import Proyecto, CuadroControl
from actividades.models import Actividad
from users.models import User
from datetime import datetime
import pandas as pd
import os

class Command(BaseCommand):
    help = "Importa datos desde Ejemplo EDP completo.xlsx (una sola hoja consolidada)"

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Ruta al archivo Excel EDP completo')
        parser.add_argument('--codigo', type=str, default='EDP_COMPLETO', help='Código del proyecto')
        parser.add_argument('--nombre', type=str, default='Proyecto consolidado EDP completo', help='Nombre del proyecto')

    def handle(self, *args, **options):
        ruta = options['archivo']

        if not os.path.exists(ruta):
            self.stderr.write(self.style.ERROR(f'No se encontró el archivo: {ruta}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Leyendo archivo: {ruta}'))
        
        try:
            df = pd.read_excel(ruta, sheet_name=0)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al leer el archivo: {e}'))
            return

        # Detectar columnas automáticamente
        columnas = list(df.columns)
        self.stdout.write(f"Columnas detectadas: {', '.join(columnas)}")
        
        # Mostrar primeras 3 filas para diagnóstico
        self.stdout.write(self.style.WARNING('\nPrimeras 3 filas del archivo:'))
        self.stdout.write(str(df.head(3)))

        # Crear empresa y usuario
        empresa, created = Empresa.objects.get_or_create(nombre='Cliente Genérico')
        if created:
            self.stdout.write(self.style.SUCCESS('Empresa creada: Cliente Genérico'))
        
        responsable = User.objects.filter(is_superuser=True).first()
        if not responsable:
            self.stderr.write(self.style.ERROR('No se encontró un usuario superusuario. Crea uno primero.'))
            return

        # Crear proyecto base
        codigo_proyecto = options['codigo']
        nombre_proyecto = options['nombre']
        
        proyecto, created = Proyecto.objects.get_or_create(
            codigo=codigo_proyecto,
            defaults={
                'nombre': nombre_proyecto,
                'cliente': empresa,
                'responsable': responsable,
                'fecha_inicio': datetime.today(),
                'estado': 'en_ejecucion'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Proyecto creado: {codigo_proyecto}'))
        else:
            self.stdout.write(self.style.WARNING(f'Proyecto existente: {codigo_proyecto}. Se agregarán actividades.'))

        total = 0
        errores = 0
        
        for idx, fila in df.iterrows():
            try:
                # Obtener descripción de la columna ITEM
                descripcion = ''
                if 'ITEM' in fila and pd.notna(fila['ITEM']):
                    descripcion = str(fila['ITEM']).strip()
                
                # Saltar filas sin descripción o filas de encabezado
                if not descripcion or descripcion.lower() in ['item', 'descripción', 'actividad']:
                    continue

                # Obtener número de item (Nº)
                item = ''
                if 'Nº' in fila and pd.notna(fila['Nº']):
                    item = str(fila['Nº']).strip()

                # Calcular avance basado en las columnas ODS (sumar valores numéricos)
                avance = 0
                total_ods = 0
                cantidad_ods = 0
                
                # Buscar columnas ODS
                ods_cols = [col for col in df.columns if col.startswith('ODS')]
                for col in ods_cols:
                    if col in fila and pd.notna(fila[col]):
                        try:
                            val = float(fila[col])
                            if val > 0:
                                total_ods += val
                                cantidad_ods += 1
                        except:
                            pass
                
                # Obtener total si existe
                total_col = 0
                if 'TOTALES' in fila and pd.notna(fila['TOTALES']):
                    try:
                        total_col = float(fila['TOTALES'])
                    except:
                        pass
                
                # Obtener cantidad planificada
                cantidad_planificada = 0
                if 'Cantidad' in fila and pd.notna(fila['Cantidad']):
                    try:
                        cantidad_planificada = float(fila['Cantidad'])
                    except:
                        pass
                
                # Calcular avance: (total ejecutado / cantidad planificada) * 100
                if cantidad_planificada > 0 and total_col > 0:
                    avance = min((total_col / cantidad_planificada) * 100, 100)
                elif total_ods > 0:
                    # Si no hay cantidad planificada, usar promedio de ODS
                    avance = min(total_ods / max(cantidad_ods, 1), 100)
                else:
                    avance = 0

                # Determinar estado basado en avance
                if avance >= 100:
                    estado = 'completada'
                elif avance > 0:
                    estado = 'en_ejecucion'
                else:
                    estado = 'pendiente'

                # Construir observaciones con datos adicionales
                observaciones_parts = []
                if 'U' in fila and pd.notna(fila['U']):
                    observaciones_parts.append(f"Unidad: {fila['U']}")
                if cantidad_planificada > 0:
                    observaciones_parts.append(f"Cantidad: {cantidad_planificada}")
                if 'PU' in fila and pd.notna(fila['PU']):
                    observaciones_parts.append(f"PU: {fila['PU']}")
                if total_col > 0:
                    observaciones_parts.append(f"Total: {total_col}")
                
                observaciones = ' | '.join(observaciones_parts)

                # Crear actividad
                Actividad.objects.create(
                    proyecto=proyecto,
                    item=item[:20] if item else '',
                    descripcion=descripcion,
                    responsable=responsable,
                    fecha_programada=None,  # No hay fechas en este formato
                    fecha_real=None,
                    avance=round(avance, 2),
                    observaciones=observaciones,
                    estado=estado
                )
                total += 1

            except Exception as e:
                errores += 1
                self.stderr.write(self.style.WARNING(f'Error en fila {idx + 2}: {e}'))

        # Actualizar cuadro de control
        try:
            control, _ = CuadroControl.objects.get_or_create(proyecto=proyecto)
            control.actualizar()
            self.stdout.write(self.style.SUCCESS(f'Cuadro de control actualizado: {control.avance_global}%'))
        except Exception as e:
            self.stderr.write(self.style.WARNING(f'Error al actualizar cuadro de control: {e}'))

        # Resumen
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Importación completada'))
        self.stdout.write(self.style.SUCCESS(f'Proyecto: {proyecto.codigo} - {proyecto.nombre}'))
        self.stdout.write(self.style.SUCCESS(f'Actividades importadas: {total}'))
        if errores > 0:
            self.stdout.write(self.style.WARNING(f'Errores encontrados: {errores}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
