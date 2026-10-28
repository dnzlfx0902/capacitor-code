# Conversor de códigos de capacitor a faradios

Convierte códigos de tres dígitos con tolerancia (por ejemplo 104K, 2n2, 47p) a faradios y de faradios al código, incluyendo la carta de tolerancias y validación de dígitos.

`electronica` · 2026-10-28

## Instalación

```bash
python3 --version   # 3.10 o superior
# sin dependencias: sólo biblioteca estándar
```

## Uso

```bash
python3 capacitor_code.py --demo
python3 capacitor_code.py 104K
python3 capacitor_code.py --faradios 0.0000001
```

Salida real de una corrida de ejemplo:

```text
104K  ->     100 nF ±10%
2n2   ->     2.2 nF sin tolerancia declarada
47p   ->      47 pF sin tolerancia declarada
4u7M  ->     4.7 µF ±20%
a_codigo(100 nF) = 104K
```

## Cómo probar

```bash
python3 -m unittest discover -s tests -v
```

## Estructura

```text
2026-10-28-capacitor-code/
├── .github/
│   └── workflows/
│       └── ci-python.yml
├── .gitignore
├── LICENSE
├── capacitor_code.py
└── tests/
    └── test_capacitor_code.py
```

## Licencia

Distribuido bajo la licencia MIT.
