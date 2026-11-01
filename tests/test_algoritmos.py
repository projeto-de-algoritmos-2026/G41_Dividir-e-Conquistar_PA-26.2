import random
import unittest
from math import isclose
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from algoritmos import dividir_conquistar, forca_bruta
from main import _comparar_algoritmos, _par_correto


class AlgoritmosTest(unittest.TestCase):
	def assert_algoritmos_concordam(self, pontos):
		resultado_bruto = forca_bruta(pontos)
		resultado_dividir = dividir_conquistar(pontos)
		self.assertIsNotNone(resultado_bruto)
		self.assertIsNotNone(resultado_dividir)
		self.assertTrue(isclose(resultado_bruto[2], resultado_dividir[2]))

	def test_mapa_com_menos_de_dois_pontos(self):
		self.assertIsNone(forca_bruta([]))
		self.assertIsNone(dividir_conquistar([(0, 0)]))

	def test_mapa_pequeno(self):
		self.assert_algoritmos_concordam([(0, 0), (3, 4), (20, 20)])

	def test_pontos_muito_proximos_e_duplicados(self):
		pontos = [(0.0, 0.0), (400.0, 300.0), (0.001, 0.001), (0.0, 0.0)]
		self.assert_algoritmos_concordam(pontos)
		self.assertEqual(dividir_conquistar(pontos)[2], 0)

	def test_mapa_grande(self):
		gerador = random.Random(26)
		pontos = [
			(gerador.randrange(1_000_000), gerador.randrange(1_000_000))
			for _ in range(1200)
		]
		self.assert_algoritmos_concordam(pontos)

	def test_comparacao_retorna_tempos_dos_dois_algoritmos(self):
		resultado, tempo_bruto, tempo_dividir = _comparar_algoritmos(
			[(0, 0), (5, 0), (30, 40)]
		)
		self.assertEqual(resultado[2], 5)
		self.assertGreaterEqual(tempo_bruto, 0)
		self.assertGreaterEqual(tempo_dividir, 0)

	def test_validacao_do_par_selecionado(self):
		pontos = [(0, 0), (3, 4), (30, 40)]
		self.assertTrue(_par_correto(pontos, [0, 1], 5))
		self.assertFalse(_par_correto(pontos, [0, 2], 5))
		self.assertFalse(_par_correto(pontos, [0], 5))


if __name__ == "__main__":
	unittest.main()
