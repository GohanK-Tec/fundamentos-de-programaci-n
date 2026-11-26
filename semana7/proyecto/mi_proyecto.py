"""
Proyecto: KLUU FOOD SERVICES — Control de Despachos e Inventario con Archivos
Curso: Fundamentos de Programación (Semana 7 - Entrega Final)
Descripción: Gestiona despachos de lotes de insumos alimentarios validando
             stock disponible (0 a 500), cantidad (1 a 500 y <= stock),
             precio (> 0 y <= $1000), descuentos por volumen (0%, 5%, 10%, 15%)
             e IVA del 16%, guardando registros en archivos .txt con fecha
             en tupla (año 2026).
"""

import os
import time


# Carpeta donde está guardado este archivo .py (con respaldo si se corre sin __file__)
try:
    CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
except NameError:
    CARPETA_PROYECTO = os.path.abspath(".")

# Menú principal en matriz [opcion, descripcion]
MENU_KLUU = [
    ["1", "Registrar despacho"],
    ["2", "Ver resumen"],
    ["3", "Ver / Leer / Crear archivos .txt"],
    ["4", "Salir"],
]


def ruta_completa(nombre_archivo):
    """Une la carpeta del proyecto con el nombre del archivo .txt."""
    return os.path.join(CARPETA_PROYECTO, nombre_archivo)


def pantalla_carga(segundos=2):
    """Muestra una barra de carga animada en consola (máximo 5 segundos)."""
    if segundos > 5:
        segundos = 5
    elif segundos <= 0:
        segundos = 1

    pasos = 10
    pausa = segundos / pasos
    print("\nCargando KLUU FOOD SERVICES...", flush=True)
    for paso in range(1, pasos + 1):
        barra = "#" * paso + "." * (pasos - paso)
        print(f"[{barra}] {paso * 10}%", flush=True)
        time.sleep(pausa)
    print("Listo.\n", flush=True)


def solicitar_usuario_bienvenida():
    """Pide el nombre o nickname del usuario y muestra un saludo dinámico."""
    while True:
        nombre = input("Ingresa tu nombre o nickname: ").strip()
        if nombre != "":
            nombre_formateado = nombre.title()
            break
        print("Advertencia: el nombre no puede estar vacío.", flush=True)

    bienvenida = (
        "\n==========================================\n"
        f"Bienvenid@, {nombre_formateado.upper()} — KLUU FOOD SERVICES\n"
        f"Operador activo: {nombre_formateado}\n"
        f"Carpeta de trabajo: {CARPETA_PROYECTO}\n"
        "=========================================="
    )
    print(bienvenida, flush=True)
    return nombre_formateado


def simular_inactividad():
    """Simula 10 minutos de inactividad con for y valida respuesta si/no."""
    print("\nNo ingresaste opción. Simulando 10 minutos de inactividad...", flush=True)
    for minuto in range(1, 11):
        print(f"Minuto {minuto} de inactividad...", flush=True)
        time.sleep(0.15)

    while True:
        respuesta = input("¿Deseas continuar en el menú? (si/no): ").strip().lower()
        if respuesta == "si":
            return True
        if respuesta == "no":
            return False
        print("Advertencia: escribe exactamente 'si' o 'no'.", flush=True)


def pedir_fecha_tupla():
    """Solicita fecha dd/mm/aaaa (solo año 2026, mes 1-12, día 1-31) y retorna tupla."""
    while True:
        texto_fecha = input("Ingresa la fecha de operación en 2026 (dd/mm/2026): ").strip()
        partes = texto_fecha.split("/")
        if len(partes) != 3:
            print("Advertencia: formato inválido. Usa dd/mm/2026 (ejemplo: 25/11/2026).", flush=True)
            continue

        try:
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])

            if anio != 2026:
                print("Advertencia: solo está permitido el año 2026.", flush=True)
                continue
            if mes < 1 or mes > 12:
                print("Advertencia: el mes no puede ser menor a 1 ni mayor a 12.", flush=True)
                continue
            if dia < 1 or dia > 31:
                print("Advertencia: el día no puede ser menor a 1 ni mayor a 31.", flush=True)
                continue
            if mes in (4, 6, 9, 11) and dia > 30:
                print("Advertencia: ese mes tiene máximo 30 días.", flush=True)
                continue
            if mes == 2 and dia > 28:
                print("Advertencia: febrero de 2026 tiene máximo 28 días.", flush=True)
                continue

            Fecha = dia, mes, anio
            return Fecha
        except ValueError:
            print("Advertencia: día, mes y año deben ser números enteros.", flush=True)


def formatear_fecha(fecha):
    """Convierte la tupla (dia, mes, anio) a texto dd/mm/aaaa."""
    dia, mes, anio = fecha
    return f"{dia:02d}/{mes:02d}/{anio}"


def asegurar_archivo_base(nombre_archivo, fecha):
    """Crea un archivo .txt base con la fecha en tupla si aún no existe."""
    destino = ruta_completa(nombre_archivo)
    if not os.path.exists(destino):
        try:
            with open(destino, "w", encoding="utf-8") as archivo:
                archivo.write(f"Fecha: {formatear_fecha(fecha)} | Fecha={fecha}\n")
                archivo.write("Bitácora de despachos KLUU FOOD SERVICES\n")
        except OSError as error:
            print(f"Error al crear '{nombre_archivo}': {error}", flush=True)


def listar_archivos_txt():
    """Muestra y devuelve los archivos .txt en la carpeta del proyecto."""
    try:
        archivos = [
            nombre for nombre in os.listdir(CARPETA_PROYECTO)
            if nombre.endswith(".txt") and os.path.isfile(ruta_completa(nombre))
        ]
        archivos.sort()
        print(f"\n--- Archivos .txt en {CARPETA_PROYECTO} ---", flush=True)
        if len(archivos) == 0:
            print("No hay archivos .txt en esta carpeta.", flush=True)
        else:
            for indice, nombre in enumerate(archivos, start=1):
                print(f"{indice}. {nombre}", flush=True)
        return archivos
    except PermissionError:
        print("Error: sin permisos para leer la carpeta.", flush=True)
        return []
    except OSError as error:
        print(f"Error al listar archivos: {error}", flush=True)
        return []


def mostrar_contenido_archivo(nombre):
    """Lee e imprime en pantalla el contenido de un archivo .txt."""
    if not nombre.endswith(".txt"):
        nombre = nombre + ".txt"

    try:
        with open(ruta_completa(nombre), "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print(f"\n=== Contenido de {nombre} ===", flush=True)
        print(contenido if contenido.strip() != "" else "(Archivo vacío)", flush=True)
        print("===============================", flush=True)
    except FileNotFoundError:
        print(f"Error: el archivo '{nombre}' no existe en {CARPETA_PROYECTO}.", flush=True)
    except PermissionError:
        print(f"Error: permiso denegado para abrir '{nombre}'.", flush=True)
    except IsADirectoryError:
        print(f"Error: '{nombre}' es una carpeta, no un archivo.", flush=True)
    except OSError as error:
        print(f"Error al leer '{nombre}': {error}", flush=True)


def gestionar_archivos(fecha):
    """Permite leer un archivo existente o crear uno nuevo con la fecha en tupla."""
    archivos = listar_archivos_txt()
    accion = input("Escribe 'L' para leer un archivo o 'C' para crear uno nuevo: ").strip().upper()

    if accion == "L":
        if len(archivos) == 0:
            return
        seleccion = input("Escribe el número o el nombre del archivo a leer: ").strip()
        if seleccion == "":
            print("Advertencia: debes indicar un archivo.", flush=True)
            return

        if seleccion.isdigit():
            indice = int(seleccion) - 1
            if 0 <= indice < len(archivos):
                mostrar_contenido_archivo(archivos[indice])
            else:
                print("Advertencia: número de archivo fuera de rango.", flush=True)
        else:
            mostrar_contenido_archivo(seleccion)

    elif accion == "C":
        nombre = input("Nombre del nuevo archivo .txt: ").strip()
        if nombre == "":
            print("Advertencia: el nombre no puede estar vacío.", flush=True)
            return
        if not nombre.endswith(".txt"):
            nombre = nombre + ".txt"

        if os.path.exists(ruta_completa(nombre)):
            print(f"Advertencia: el archivo '{nombre}' ya existe en {CARPETA_PROYECTO}.", flush=True)
            return

        nota = input("Encabezado o descripción inicial: ").strip()
        if nota == "":
            nota = "Registro KLUU FOOD SERVICES"

        try:
            with open(ruta_completa(nombre), "w", encoding="utf-8") as archivo:
                archivo.write(f"Fecha: {formatear_fecha(fecha)} | Fecha={fecha}\n")
                archivo.write(f"Descripción: {nota}\n")
            print(f"Guardado en: {ruta_completa(nombre)}", flush=True)
        except PermissionError:
            print(f"Error: sin permisos para crear '{nombre}'.", flush=True)
        except IsADirectoryError:
            print(f"Error: '{nombre}' es una carpeta.", flush=True)
        except OSError as error:
            print(f"Error al crear '{nombre}': {error}", flush=True)
    else:
        print("Advertencia: opción no válida. Escribe 'L' o 'C'.", flush=True)


def anexar_registro(nombre_archivo, texto_registro, fecha):
    """Agrega un registro al final de un archivo existente con la fecha en tupla."""
    try:
        with open(ruta_completa(nombre_archivo), "a", encoding="utf-8") as archivo:
            archivo.write(f"[{formatear_fecha(fecha)} | Fecha={fecha}] {texto_registro}\n")
        return True
    except FileNotFoundError:
        print(f"Error: el archivo '{nombre_archivo}' no existe.", flush=True)
        return False
    except PermissionError:
        print(f"Error: sin permisos para escribir en '{nombre_archivo}'.", flush=True)
        return False
    except IsADirectoryError:
        print(f"Error: '{nombre_archivo}' es una carpeta.", flush=True)
        return False
    except OSError as error:
        print(f"Error al guardar en '{nombre_archivo}': {error}", flush=True)
        return False


def calcular_importe_despacho(precio, cantidad):
    """Calcula subtotal, descuento por volumen, IVA (16%) y total neto."""
    subtotal = precio * cantidad

    if cantidad >= 100:
        descuento = subtotal * 0.15
    elif cantidad >= 50:
        descuento = subtotal * 0.10
    elif cantidad >= 25:
        descuento = subtotal * 0.05
    else:
        descuento = 0.0

    subtotal_con_descuento = subtotal - descuento
    iva = subtotal_con_descuento * 0.16
    total_venta = subtotal_con_descuento + iva
    return subtotal, descuento, iva, total_venta


def pedir_precio_valido():
    """Bloquea el avance hasta ingresar un precio > 0 y <= 1000."""
    while True:
        try:
            precio = float(input("Ingresa el precio del producto (máx. $1000): "))
        except ValueError:
            print("Advertencia: ingresa un número válido para el precio.", flush=True)
            continue

        if precio <= 0:
            print("Advertencia: el precio debe ser mayor a $0. Intenta de nuevo.", flush=True)
            continue

        if precio > 1000:
            print("No contamos con productos de más de $1000 para su venta individual", flush=True)
            continue

        return precio


def pedir_stock_valido():
    """Bloquea el avance hasta ingresar un stock entero entre 0 y 500."""
    while True:
        try:
            stock = int(input("Ingresa el stock disponible (0 a 500 lotes): "))
        except ValueError:
            print("Advertencia: el stock debe ser un número entero entre 0 y 500.", flush=True)
            continue

        if stock < 0 or stock > 500:
            print("Advertencia: el stock no puede ser menor a 0 ni mayor a 500. Intenta de nuevo.", flush=True)
            continue

        return stock


def pedir_cantidad_valida(stock):
    """Bloquea el avance hasta ingresar una cantidad entre 1 y 500 que no supere el stock."""
    if stock == 0:
        print("Advertencia: no hay stock disponible (0 lotes). No se puede despachar.", flush=True)
        return None

    while True:
        try:
            cantidad = int(input(f"Ingresa la cantidad que deseas comprar (1 a {min(stock, 500)} lotes): "))
        except ValueError:
            print("Cantidad fuera del rango o no disponible", flush=True)
            continue

        if cantidad <= 0 or cantidad > 500 or cantidad > stock:
            print("Cantidad fuera del rango o no disponible", flush=True)
            continue

        if cantidad > 0 and cantidad <= 500 and cantidad <= stock:
            return cantidad


def registrar_despacho(fecha, usuario):
    """Solicita precio, stock y cantidad bloqueando datos inválidos, calcula y guarda."""
    precio = pedir_precio_valido()
    stock = pedir_stock_valido()
    cantidad = pedir_cantidad_valida(stock)

    if cantidad is None:
        print("Despacho cancelado por falta de stock. No se registró nada.", flush=True)
        return None, None

    if cantidad > 0 and cantidad <= stock and cantidad <= 500 and stock <= 500 and precio > 0 and precio <= 1000:
        subtotal, descuento, iva, total_venta = calcular_importe_despacho(precio, cantidad)
        stock_restante = stock - cantidad

        print(f"Subtotal: ${round(subtotal, 2)}", flush=True)
        print(f"Descuento: -${round(descuento, 2)}", flush=True)
        print(f"IVA (16%): +${round(iva, 2)}", flush=True)
        print(f"El total a pagar: ${round(total_venta, 2)}", flush=True)
        print(f"Stock restante: {stock_restante} lotes", flush=True)

        archivos = listar_archivos_txt()
        destino = input("Archivo .txt donde guardar (Enter = despachos.txt): ").strip()
        if destino == "":
            destino = "despachos.txt"
        elif destino.isdigit() and 1 <= int(destino) <= len(archivos):
            destino = archivos[int(destino) - 1]
        elif not destino.endswith(".txt"):
            destino = destino + ".txt"

        detalle = (
            f"Operador: {usuario} | Cant: {cantidad} | Precio: ${precio:.2f} | "
            f"Desc: ${descuento:.2f} | IVA: ${iva:.2f} | "
            f"Total: ${total_venta:.2f} | StockRest: {stock_restante}"
        )

        if not os.path.exists(ruta_completa(destino)):
            try:
                with open(ruta_completa(destino), "w", encoding="utf-8") as archivo:
                    archivo.write(f"Fecha: {formatear_fecha(fecha)} | Fecha={fecha}\n")
                if anexar_registro(destino, detalle, fecha):
                    print(f"Creado y guardado en: {ruta_completa(destino)}", flush=True)
            except OSError as error:
                print(f"Error al crear '{destino}': {error}", flush=True)
        else:
            if anexar_registro(destino, detalle, fecha):
                print(f"Guardado en: {ruta_completa(destino)}", flush=True)

        return total_venta, destino

    print("Advertencia: datos inválidos. El despacho no se registró.", flush=True)
    return None, None


def mostrar_resumen(usuario, fecha, total, registro, ultimo_archivo):
    """Muestra el resumen de la sesión y despliega en pantalla el archivo guardado."""
    print("\n================ RESUMEN DE OPERACIÓN ================", flush=True)
    print(f"Operador: {usuario}", flush=True)
    print(f"Fecha activa (tupla): {fecha}", flush=True)
    print(f"Total de despachos en sesión: {registro}", flush=True)
    print(f"Monto acumulado en sesión: ${round(total, 2)}", flush=True)
    print(f"Carpeta: {CARPETA_PROYECTO}", flush=True)
    print("======================================================", flush=True)

    archivos = listar_archivos_txt()
    if len(archivos) > 0:
        ver = input(f"Número o nombre de archivo a ver (Enter = {ultimo_archivo}): ").strip()
        if ver == "":
            elegido = ultimo_archivo
        elif ver.isdigit() and 1 <= int(ver) <= len(archivos):
            elegido = archivos[int(ver) - 1]
        else:
            elegido = ver
        mostrar_contenido_archivo(elegido)


def dibujar_menu():
    """Recorre la matriz MENU_KLUU y muestra las opciones en consola."""
    print("\n=== KLUU FOOD SERVICES ===", flush=True)
    for fila in MENU_KLUU:
        print(f"{fila[0]}. {fila[1]}", flush=True)


def main():
    """Controla el flujo principal del programa."""
    while True:
        pantalla_carga(2)
        usuario = solicitar_usuario_bienvenida()
        Fecha = pedir_fecha_tupla()
        asegurar_archivo_base("despachos.txt", Fecha)

        total = 0.0
        registro = 0
        ultimo_archivo = "despachos.txt"

        while True:
            dibujar_menu()
            opcion = input("Elige una opción (1-4) o presiona Enter: ").strip()

            if opcion == "":
                if simular_inactividad():
                    continue
                break

            if opcion == "1":
                monto, archivo_usado = registrar_despacho(Fecha, usuario)
                if monto is not None:
                    total += monto
                    registro += 1
                    if archivo_usado is not None:
                        ultimo_archivo = archivo_usado

            elif opcion == "2":
                mostrar_resumen(usuario, Fecha, total, registro, ultimo_archivo)

            elif opcion == "3":
                gestionar_archivos(Fecha)

            elif opcion == "4":
                print("Gracias por usar KLUU FOOD SERVICES. ¡Hasta luego!", flush=True)
                return

            else:
                print("Advertencia: por favor elige una opción válida (1-4).", flush=True)


if __name__ == "__main__":
    main()