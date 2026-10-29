import pygame
from math import sqrt


pontos = [
	(100, 150),
	(180, 200),
	(300, 100),
	(350, 280),
]


def distancia_euclidiana(ponto1, ponto2):
	x1, y1 = ponto1
	x2, y2 = ponto2
	return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def mostrar_mapa(pontos, largura=36, altura=15):
	if not pontos:
		print("Nenhum ponto para mostrar no mapa.")
		return

	grade = [[" " for _ in range(largura)] for _ in range(altura)]
	menor_x = min(x for x, _ in pontos)
	maior_x = max(x for x, _ in pontos)
	menor_y = min(y for _, y in pontos)
	maior_y = max(y for _, y in pontos)
	faixa_x = maior_x - menor_x or 1
	faixa_y = maior_y - menor_y or 1
	identificadores = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	for indice, (x, y) in enumerate(pontos):
		coluna = round((x - menor_x) / faixa_x * (largura - 1))
		linha = round((y - menor_y) / faixa_y * (altura - 1))
		marcador = identificadores[indice] if indice < len(identificadores) else "*"
		grade[linha][coluna] = marcador

	print("Resgate Espacial")
	print("Mapa espacial: cada marcador representa um ponto")
	print("+" + "-" * largura + "+")
	for linha in grade:
		print("|" + "".join(linha) + "|")
	print("+" + "-" * largura + "+")
	for indice, ponto in enumerate(pontos):
		marcador = identificadores[indice] if indice < len(identificadores) else "*"
		print(f"{marcador}: {ponto}")


mostrar_mapa(pontos)
