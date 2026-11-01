import random
import time
from math import isclose

import pygame

from algoritmos import distancia_euclidiana, dividir_conquistar, forca_bruta
from pontos import ALTURA_MAPA, LARGURA_MAPA, gerar_pontos


LARGURA_JANELA = 1040
ALTURA_JANELA = 720
AREA_MAPA = pygame.Rect(28, 112, 700, 560)

COR_FUNDO = (7, 12, 31)
COR_PAINEL = (14, 23, 49)
COR_GRADE = (28, 43, 76)
COR_TEXTO = (225, 235, 255)
COR_TEXTO_SUAVE = (139, 158, 194)
COR_CIANO = (74, 222, 230)
COR_ROXO = (166, 123, 255)
COR_DESTAQUE = (255, 207, 92)

BOTAO_NOVO_MAPA = pygame.Rect(774, 230, 216, 44)
BOTAO_BUSCAR = pygame.Rect(774, 286, 216, 44)
BOTAO_REINICIAR = pygame.Rect(774, 342, 216, 44)
BOTAO_DIMINUIR = pygame.Rect(774, 190, 38, 28)
BOTAO_AUMENTAR = pygame.Rect(974, 190, 38, 28)
QUANTIDADE_MINIMA = 2
QUANTIDADE_MAXIMA = 500


def _posicao_na_tela(ponto):
	x, y = ponto
	margem = 22
	area_util = AREA_MAPA.inflate(-2 * margem, -2 * margem)
	pos_x = area_util.left + x / LARGURA_MAPA * area_util.width
	pos_y = area_util.bottom - y / ALTURA_MAPA * area_util.height
	return round(pos_x), round(pos_y)


def _desenhar_estrelas(tela, estrelas):
	for x, y, brilho in estrelas:
		cor = (brilho, brilho, min(brilho + 24, 255))
		pygame.draw.circle(tela, cor, (x, y), 1 if brilho < 180 else 2)


def _desenhar_mapa(tela, pontos, resultado, fonte, fonte_pequena):
	pygame.draw.rect(tela, COR_PAINEL, AREA_MAPA, border_radius=18)
	pygame.draw.rect(tela, COR_GRADE, AREA_MAPA, width=1, border_radius=18)

	for divisao in range(1, 5):
		x = AREA_MAPA.left + divisao * AREA_MAPA.width // 5
		y = AREA_MAPA.top + divisao * AREA_MAPA.height // 5
		pygame.draw.line(
			tela, COR_GRADE, (x, AREA_MAPA.top + 1), (x, AREA_MAPA.bottom - 1)
		)
		pygame.draw.line(
			tela, COR_GRADE, (AREA_MAPA.left + 1, y), (AREA_MAPA.right - 1, y)
		)

	if resultado is not None:
		posicao1 = _posicao_na_tela(resultado[0])
		posicao2 = _posicao_na_tela(resultado[1])
		pygame.draw.line(tela, COR_DESTAQUE, posicao1, posicao2, 3)

	for indice, ponto in enumerate(pontos):
		posicao = _posicao_na_tela(ponto)
		if resultado is not None and ponto in resultado[:2]:
			cor = COR_DESTAQUE
			pygame.draw.circle(tela, COR_DESTAQUE, posicao, 13, width=2)
		else:
			cor = COR_CIANO if indice % 2 == 0 else COR_ROXO
		pygame.draw.circle(tela, cor, posicao, 7)
		pygame.draw.circle(tela, (245, 250, 255), posicao, 3)
		rotulo = fonte_pequena.render(str(indice + 1), True, COR_TEXTO)
		tela.blit(rotulo, (posicao[0] + 10, posicao[1] - 14))

	titulo = fonte.render("SETOR DE RESGATE", True, COR_TEXTO)
	tela.blit(titulo, (AREA_MAPA.left, 76))
	legenda = fonte_pequena.render(
		f"{len(pontos)} sinais de emergencia", True, COR_TEXTO_SUAVE
	)
	tela.blit(legenda, (AREA_MAPA.right - legenda.get_width(), 80))


def _desenhar_botao(tela, retangulo, rotulo, fonte, mouse_posicao):
	hover = retangulo.collidepoint(mouse_posicao)
	cor_fundo = (33, 54, 91) if hover else (23, 38, 69)
	cor_borda = COR_CIANO if hover else COR_GRADE
	pygame.draw.rect(tela, cor_fundo, retangulo, border_radius=10)
	pygame.draw.rect(tela, cor_borda, retangulo, width=1, border_radius=10)
	texto = fonte.render(rotulo, True, COR_TEXTO)
	tela.blit(texto, texto.get_rect(center=retangulo.center))


def _comparar_algoritmos(pontos):
	inicio = time.perf_counter_ns()
	resultado_bruto = forca_bruta(pontos)
	tempo_bruto = (time.perf_counter_ns() - inicio) / 1_000_000

	inicio = time.perf_counter_ns()
	resultado_dividir = dividir_conquistar(pontos)
	tempo_dividir = (time.perf_counter_ns() - inicio) / 1_000_000

	if resultado_bruto is None or resultado_dividir is None:
		return None, tempo_bruto, tempo_dividir
	if not isclose(resultado_bruto[2], resultado_dividir[2]):
		raise RuntimeError("Os algoritmos encontraram distancias minimas diferentes.")
	return resultado_dividir, tempo_bruto, tempo_dividir


def _par_correto(pontos, selecao, distancia_minima):
	if len(selecao) != 2:
		return False
	distancia_selecionada = distancia_euclidiana(
		pontos[selecao[0]], pontos[selecao[1]]
	)
	return isclose(distancia_selecionada, distancia_minima)


def _ponto_clicado(posicao, pontos, selecao):
	mais_proximo = None
	menor_distancia = 14
	for indice, ponto in enumerate(pontos):
		if indice in selecao:
			continue
		dx = _posicao_na_tela(ponto)[0] - posicao[0]
		dy = _posicao_na_tela(ponto)[1] - posicao[1]
		distancia = (dx * dx + dy * dy) ** 0.5
		if distancia < menor_distancia:
			mais_proximo = indice
			menor_distancia = distancia
	return mais_proximo


def _desenhar_painel(
	tela,
	quantidade,
	resultado,
	tempos,
	selecao,
	status,
	pontuacao,
	fonte,
	fonte_pequena,
	mouse_posicao,
):
	pygame.draw.rect(
		tela, COR_PAINEL, pygame.Rect(752, 112, 260, 560), border_radius=18
	)
	painel_titulo = fonte.render("CENTRAL DE COMANDO", True, COR_CIANO)
	tela.blit(painel_titulo, (774, 138))
	tela.blit(
		fonte_pequena.render("Sinais no mapa:", True, COR_TEXTO_SUAVE), (814, 196)
	)
	_desenhar_botao(tela, BOTAO_DIMINUIR, "-", fonte, mouse_posicao)
	_desenhar_botao(tela, BOTAO_AUMENTAR, "+", fonte, mouse_posicao)
	contador = fonte.render(str(quantidade), True, COR_TEXTO)
	tela.blit(contador, contador.get_rect(center=(893, 204)))

	_desenhar_botao(
		tela, BOTAO_NOVO_MAPA, "NOVO MAPA  (N)", fonte_pequena, mouse_posicao
	)
	_desenhar_botao(
		tela,
		BOTAO_BUSCAR,
		"BUSCAR PAR MAIS PROXIMO",
		fonte_pequena,
		mouse_posicao,
	)
	_desenhar_botao(
		tela, BOTAO_REINICIAR, "REINICIAR  (R)", fonte_pequena, mouse_posicao
	)

	if resultado is None:
		estado = fonte_pequena.render(
			"Busque o par mais proximo.", True, COR_TEXTO_SUAVE
		)
		tela.blit(estado, (774, 416))
	else:
		tela.blit(
			fonte.render("PAR MAIS PROXIMO", True, COR_DESTAQUE), (774, 410)
		)
		distancia = fonte.render(f"Distancia: {resultado[2]:.2f}", True, COR_TEXTO)
		tela.blit(distancia, (774, 444))
		linha_tempos = fonte_pequena.render(
			f"Forca bruta: {tempos[0]:.3f} ms", True, COR_TEXTO_SUAVE
		)
		tela.blit(linha_tempos, (774, 478))
		linha_tempos = fonte_pequena.render(
			f"Dividir e conquistar: {tempos[1]:.3f} ms",
			True,
			COR_TEXTO_SUAVE,
		)
		tela.blit(linha_tempos, (774, 500))
		instrucao = fonte_pequena.render(
			"Clique em dois sinais para resgatar.", True, COR_TEXTO_SUAVE
		)
		tela.blit(instrucao, (774, 540))
		if selecao:
			escolhidos = ", ".join(str(indice + 1) for indice in selecao)
			tela.blit(
				fonte_pequena.render(f"Selecionados: {escolhidos}", True, COR_TEXTO),
				(774, 564),
			)
		if status:
			cor_status = COR_CIANO if status.startswith("Resgate") else COR_DESTAQUE
			tela.blit(fonte_pequena.render(status, True, cor_status), (774, 590))

	pontos_texto = fonte.render(f"Resgates: {pontuacao}", True, COR_TEXTO)
	tela.blit(pontos_texto, (774, 620))
	ajuda = fonte_pequena.render("ESC: sair", True, COR_TEXTO_SUAVE)
	tela.blit(ajuda, (926, 624))


def main():
	pygame.init()
	pygame.display.set_caption("Space Rescue | Busca pelo sinal mais proximo")
	tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
	relogio = pygame.time.Clock()
	fonte_titulo = pygame.font.Font(None, 42)
	fonte = pygame.font.Font(None, 22)
	fonte_pequena = pygame.font.Font(None, 18)
	gerador_estrelas = random.Random(7)
	estrelas = [
		(
			gerador_estrelas.randrange(LARGURA_JANELA),
			gerador_estrelas.randrange(ALTURA_JANELA),
			gerador_estrelas.randrange(90, 220),
		)
		for _ in range(100)
	]
	quantidade = 10
	mapa_inicial = gerar_pontos(quantidade)
	pontos = list(mapa_inicial)
	resultado = None
	tempos = (0.0, 0.0)
	selecao = []
	status = ""
	pontuacao = 0
	botoes = (
		(BOTAO_NOVO_MAPA, "novo"),
		(BOTAO_BUSCAR, "buscar"),
		(BOTAO_REINICIAR, "reiniciar"),
		(BOTAO_DIMINUIR, "diminuir"),
		(BOTAO_AUMENTAR, "aumentar"),
	)

	def novo_mapa():
		nonlocal mapa_inicial, pontos, resultado, selecao, status
		mapa_inicial = gerar_pontos(quantidade)
		pontos = list(mapa_inicial)
		resultado = None
		selecao = []
		status = ""

	def buscar_par():
		nonlocal resultado, tempos, selecao, status
		resultado, tempo_bruto, tempo_dividir = _comparar_algoritmos(pontos)
		tempos = (tempo_bruto, tempo_dividir)
		selecao = []
		status = "Clique em dois sinais para vencer."

	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
				return
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					pygame.quit()
					return
				if evento.key == pygame.K_n:
					novo_mapa()
				elif evento.key == pygame.K_SPACE:
					buscar_par()
				elif evento.key == pygame.K_r:
					pontos = list(mapa_inicial)
					resultado = None
					selecao = []
					status = ""
					pontuacao = 0
				elif evento.key in (pygame.K_UP, pygame.K_RIGHT):
					quantidade = min(QUANTIDADE_MAXIMA, quantidade + 1)
					novo_mapa()
				elif evento.key in (pygame.K_DOWN, pygame.K_LEFT):
					quantidade = max(QUANTIDADE_MINIMA, quantidade - 1)
					novo_mapa()
			if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
				for retangulo, acao in botoes:
					if retangulo.collidepoint(evento.pos):
						if acao == "novo":
							novo_mapa()
						elif acao == "buscar":
							buscar_par()
						elif acao == "reiniciar":
							pontos = list(mapa_inicial)
							resultado = None
							selecao = []
							status = ""
							pontuacao = 0
						elif acao == "aumentar":
							quantidade = min(QUANTIDADE_MAXIMA, quantidade + 1)
							novo_mapa()
						elif acao == "diminuir":
							quantidade = max(QUANTIDADE_MINIMA, quantidade - 1)
							novo_mapa()
						break
				else:
					if resultado is not None and not status.startswith("Resgate"):
						indice = _ponto_clicado(evento.pos, pontos, selecao)
						if indice is not None:
							selecao.append(indice)
							if len(selecao) == 2:
								if _par_correto(pontos, selecao, resultado[2]):
									pontuacao += 1
									status = "Resgate confirmado! Voce venceu!"
								else:
									status = "Par incorreto. Tente novamente."
									selecao = []

		tela.fill(COR_FUNDO)
		_desenhar_estrelas(tela, estrelas)
		titulo = fonte_titulo.render("SPACE RESCUE", True, COR_CIANO)
		tela.blit(titulo, (28, 24))
		subtitulo = fonte.render(
			"Encontre o sinal de emergencia mais proximo", True, COR_TEXTO_SUAVE
		)
		tela.blit(subtitulo, (30, 65))
		_desenhar_mapa(
			tela,
			pontos,
			resultado,
			fonte,
			fonte_pequena,
		)
		for indice in selecao:
			posicao = _posicao_na_tela(pontos[indice])
			pygame.draw.circle(tela, (100, 255, 153), posicao, 13, width=2)
		_desenhar_painel(
			tela,
			quantidade,
			resultado,
			tempos,
			selecao,
			status,
			pontuacao,
			fonte,
			fonte_pequena,
			pygame.mouse.get_pos(),
		)

		pygame.display.flip()
		relogio.tick(60)


if __name__ == "__main__":
	main()
