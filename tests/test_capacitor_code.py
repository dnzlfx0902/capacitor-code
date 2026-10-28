import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import capacitor_code as m


class Decodificar(unittest.TestCase):
    def test_codigos_de_tres_digitos(self):
        self.assertEqual(m.a_faradios("104K"), (100e-9, 10.0))
        self.assertEqual(m.a_faradios("473J"), (47e-9, 5.0))

    def test_tres_digitos_son_picofaradios(self):
        # 01·10^0 pF = 1 pF y 47·10^5 pF = 4,7 µF
        self.assertEqual(m.a_faradios("010")[0], 1e-12)
        self.assertEqual(m.a_faradios("475")[0], 4.7e-6)

    def test_codigos_con_prefijo(self):
        self.assertAlmostEqual(m.a_faradios("2n2")[0], 2.2e-9)
        self.assertAlmostEqual(m.a_faradios("47p")[0], 47e-12)
        self.assertAlmostEqual(m.a_faradios("4u7M")[0], 4.7e-6)

    def test_invalidos(self):
        for codigo in ("", "abc", "1x4", "99"):
            with self.subTest(codigo=codigo), self.assertRaises(ValueError):
                m.a_faradios(codigo)


class Codificar(unittest.TestCase):
    def test_ida_y_vuelta(self):
        for faradios in (100e-9, 47e-9, 2.2e-9, 4.7e-6, 1e-12):
            codigo = m.a_codigo(faradios)
            self.assertAlmostEqual(m.a_faradios(codigo)[0], faradios, places=15)

    def test_codigo_concreto(self):
        self.assertEqual(m.a_codigo(100e-9), "104K")
        self.assertEqual(m.a_codigo(4.7e-6), "475K")
        self.assertEqual(m.a_codigo(2.2e-9, "J"), "222J")

    def test_formato(self):
        self.assertEqual(m.formatear(100e-9), "100 nF")
        self.assertEqual(m.formatear(4.7e-6), "4.7 µF")


if __name__ == "__main__":
    unittest.main()
