"""Conversor de códigos de capacitor a faradios.

Convierte códigos de tres dígitos con tolerancia (por ejemplo 104K, 2n2, 47p) a faradios y de faradios al código, incluyendo la carta de tolerancias y validación de dígitos.
"""
from __future__ import annotations

TOLERANCIAS = {"B": 0.1, "C": 0.25, "D": 0.5, "F": 1.0, "G": 2.0,
               "J": 5.0, "K": 10.0, "M": 20.0}
PREFIJOS = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3}


def a_faradios(codigo):
    """Convierte '104K', '2n2' o '47p' en (faradios, tolerancia %).

    El código de tres dígitos está **siempre en picofaradios**: ``104`` son
    10·10^4 pF = 100 nF, no 10 µF. La forma con prefijo (``2n2``, ``4u7``) sí
    lleva la unidad escrita.
    """
    texto = codigo.strip().replace(" ", "")
    if not texto:
        raise ValueError("código vacío")
    letra_tol = texto[-1].upper() if texto[-1].upper() in TOLERANCIAS else None
    cuerpo = texto[:-1] if letra_tol else texto
    tolerancia = TOLERANCIAS[letra_tol] if letra_tol else None
    if any(p in cuerpo for p in PREFIJOS):
        prefijo = next(p for p in PREFIJOS if p in cuerpo)
        entero, _, decimal = cuerpo.partition(prefijo)
        if not (entero.isdigit() or entero == "") or not (decimal.isdigit() or decimal == ""):
            raise ValueError(f"código inválido: {codigo}")
        if entero == "" and decimal == "":
            raise ValueError(f"código inválido: {codigo}")
        valor = float(f"{entero or 0}.{decimal or 0}") * PREFIJOS[prefijo]
        return valor, tolerancia
    if len(cuerpo) == 3 and cuerpo.isdigit():
        digitos = int(cuerpo[:2])
        multiplicador = int(cuerpo[2])
        # dos cifras significativas por 10^multiplicador, en picofaradios; el
        # literal decimal evita el error de redondeo de 10**-12 en coma flotante
        return float(f"{digitos}e{multiplicador - 12}"), tolerancia
    raise ValueError(f"código inválido: {codigo}")


def a_codigo(faradios, tolerancia="K"):
    """Devuelve el código de tres dígitos (en picofaradios) para un valor."""
    if faradios <= 0:
        raise ValueError("la capacitancia debe ser positiva")
    if tolerancia not in TOLERANCIAS:
        raise ValueError(f"tolerancia no soportada: {tolerancia}")
    pico = faradios / 1e-12
    if pico < 1:
        raise ValueError("valor por debajo de 1 pF: no cabe en tres dígitos")
    exponente = 0
    while pico >= 100:
        pico /= 10
        exponente += 1
    if pico >= 10:
        cifras = int(round(pico))          # dos cifras significativas
        if cifras == 100:                  # 99,6 pF redondea a 100 pF
            cifras, exponente = 10, exponente + 1
    else:
        cifras = int(round(pico))          # 1..9 pF: "05" = 5 pF
    if exponente > 9:
        raise ValueError("valor fuera del rango de tres dígitos (1 pF a 99 mF)")
    return f"{cifras:02d}{exponente}{tolerancia}"


def formatear(faradios):
    for prefijo, factor in (("µF", 1e-6), ("nF", 1e-9), ("pF", 1e-12)):
        if faradios >= factor * 0.999:
            return f"{faradios / factor:g} {prefijo}"
    return f"{faradios:g} F"


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Conversor de códigos de capacitor a faradios")
    p.add_argument("codigo", nargs="?", help="código como 104K, 2n2 o 47p")
    p.add_argument("--faradios", type=float, help="valor a codificar")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.codigo:
        valor, tol = a_faradios(a.codigo)
        print(f"{a.codigo} -> {formatear(valor)}" + (f" ±{tol:g}%" if tol else ""))
        return 0
    if a.faradios:
        print(a_codigo(a.faradios))
        return 0
    if a.demo:
        for codigo in ("104K", "2n2", "47p", "4u7M"):
            valor, tol = a_faradios(codigo)
            extra = f" ±{tol:g}%" if tol else " sin tolerancia declarada"
            print(f"{codigo:5s} -> {formatear(valor):>10s}{extra}")
        print(f"a_codigo(100 nF) = {a_codigo(100e-9)}")
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
