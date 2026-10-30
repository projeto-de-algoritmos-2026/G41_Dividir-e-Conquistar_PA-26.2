from random import randint


LARGURA_MAPA = 800
ALTURA_MAPA = 600
MARGEM_PONTO = 10


def gerar_pontos(quantidade):
	if quantidade < 0:
		raise ValueError("A quantidade de pontos nao pode ser negativa.")

	return [
		(
			randint(MARGEM_PONTO, LARGURA_MAPA - MARGEM_PONTO),
			randint(MARGEM_PONTO, ALTURA_MAPA - MARGEM_PONTO),
		)
		for _ in range(quantidade)
	]
