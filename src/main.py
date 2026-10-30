from math import isclose

from algoritmos import dividir_conquistar, forca_bruta
from pontos import gerar_pontos


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


def comparar_algoritmos(pontos):
	resultado_forca_bruta = forca_bruta(pontos)
	resultado_dividir_conquistar = dividir_conquistar(pontos)

	if resultado_forca_bruta is None:
		print("Sao necessarios pelo menos dois pontos.")
		return

	print(f"Distancia minima (forca bruta): {resultado_forca_bruta[2]:.2f}")
	print(
		"Distancia minima (dividir e conquistar): "
		f"{resultado_dividir_conquistar[2]:.2f}"
	)

	if isclose(resultado_forca_bruta[2], resultado_dividir_conquistar[2]):
		print("Os algoritmos encontraram a mesma distancia minima.")
	else:
		print("Os algoritmos encontraram distancias diferentes.")
def ler_quantidade_pontos():
	while True:
		try:
			quantidade = int(input("Quantos pontos deseja gerar? "))
		except ValueError:
			print("Digite um numero inteiro.")
			continue

		if quantidade < 2:
			print("Informe pelo menos dois pontos.")
			continue

		return quantidade


def main():
	quantidade = ler_quantidade_pontos()
	pontos = gerar_pontos(quantidade)
	mostrar_mapa(pontos)
	comparar_algoritmos(pontos)


if __name__ == "__main__":
	main()
