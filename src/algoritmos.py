from collections import Counter
from math import hypot


def distancia_euclidiana(ponto1, ponto2):
	x1, y1 = ponto1
	x2, y2 = ponto2
	return hypot(x2 - x1, y2 - y1)


def _forca_bruta(pontos):
	melhor_par = (None, None, float("inf"))

	for indice, ponto1 in enumerate(pontos):
		for ponto2 in pontos[indice + 1:]:
			distancia = distancia_euclidiana(ponto1, ponto2)
			if distancia < melhor_par[2]:
				melhor_par = (ponto1, ponto2, distancia)

	return melhor_par


def forca_bruta(pontos):
	if len(pontos) < 2:
		return None
	return _forca_bruta(pontos)


def dividir_conquistar(pontos):
	if len(pontos) < 2:
		return None

	pontos_x = sorted(pontos, key=lambda ponto: (ponto[0], ponto[1]))
	pontos_y = sorted(pontos, key=lambda ponto: (ponto[1], ponto[0]))

	def resolver(pontos_ordenados_x, pontos_ordenados_y):
		quantidade = len(pontos_ordenados_x)
		if quantidade <= 3:
			return _forca_bruta(pontos_ordenados_x)

		meio = quantidade // 2
		esquerda_x = pontos_ordenados_x[:meio]
		direita_x = pontos_ordenados_x[meio:]
		linha_divisoria = direita_x[0][0]

		contagem_esquerda = Counter(esquerda_x)
		esquerda_y = []
		direita_y = []
		for ponto in pontos_ordenados_y:
			if contagem_esquerda[ponto] > 0:
				esquerda_y.append(ponto)
				contagem_esquerda[ponto] -= 1
			else:
				direita_y.append(ponto)

		melhor_esquerda = resolver(esquerda_x, esquerda_y)
		melhor_direita = resolver(direita_x, direita_y)
		melhor_par = min(melhor_esquerda, melhor_direita, key=lambda par: par[2])
		menor_distancia = melhor_par[2]

		faixa = [
			ponto
			for ponto in pontos_ordenados_y
			if abs(ponto[0] - linha_divisoria) < menor_distancia
		]

		for indice, ponto1 in enumerate(faixa):
			indice_seguinte = indice + 1
			while (
				indice_seguinte < len(faixa)
				and faixa[indice_seguinte][1] - ponto1[1] < menor_distancia
			):
				ponto2 = faixa[indice_seguinte]
				distancia = distancia_euclidiana(ponto1, ponto2)
				if distancia < menor_distancia:
					melhor_par = (ponto1, ponto2, distancia)
					menor_distancia = distancia
				indice_seguinte += 1

		return melhor_par

	return resolver(pontos_x, pontos_y)
