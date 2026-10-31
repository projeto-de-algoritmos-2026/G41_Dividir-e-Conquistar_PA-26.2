import random
import sys

import pygame

from algoritmos import dividir_conquistar
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


def _desenhar_painel(tela, pontos, resultado, fonte, fonte_pequena, mouse_posicao):
	pygame.draw.rect(
		tela, COR_PAINEL, pygame.Rect(752, 112, 260, 560), border_radius=18
	)
	painel_titulo = fonte.render("CENTRAL DE COMANDO", True, COR_CIANO)
	tela.blit(painel_titulo, (774, 138))
	instrucao = fonte_pequena.render(
		f"{len(pontos)} sinais no setor", True, COR_TEXTO_SUAVE
	)
	tela.blit(instrucao, (774, 174))

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
			"Pronto para procurar o sinal.", True, COR_TEXTO_SUAVE
		)
		tela.blit(estado, (774, 416))
	else:
		tela.blit(
			fonte.render("PAR MAIS PROXIMO", True, COR_DESTAQUE), (774, 410)
		)
		distancia = fonte.render(f"Distancia: {resultado[2]:.2f}", True, COR_TEXTO)
		tela.blit(distancia, (774, 444))
		for indice, ponto in enumerate(resultado[:2], start=1):
			coordenadas = fonte_pequena.render(
				f"Sinal {indice}: ({ponto[0]}, {ponto[1]})",
				True,
				COR_TEXTO_SUAVE,
			)
			tela.blit(coordenadas, (774, 476 + (indice - 1) * 26))

	ajuda = fonte_pequena.render("ESC: sair", True, COR_TEXTO_SUAVE)
	tela.blit(ajuda, (774, 630))


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
	mapa_inicial = gerar_pontos(10)
	pontos = list(mapa_inicial)
	resultado = None
	botoes = (
		(BOTAO_NOVO_MAPA, "novo"),
		(BOTAO_BUSCAR, "buscar"),
		(BOTAO_REINICIAR, "reiniciar"),
	)

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
					pontos = gerar_pontos(len(pontos))
					resultado = None
				elif evento.key == pygame.K_SPACE:
					resultado = dividir_conquistar(pontos)
				elif evento.key == pygame.K_r:
					pontos = list(mapa_inicial)
					resultado = None
			if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
				for retangulo, acao in botoes:
					if retangulo.collidepoint(evento.pos):
						if acao == "novo":
							pontos = gerar_pontos(len(pontos))
							resultado = None
						elif acao == "buscar":
							resultado = dividir_conquistar(pontos)
						else:
							pontos = list(mapa_inicial)
							resultado = None
						break

		tela.fill(COR_FUNDO)
		_desenhar_estrelas(tela, estrelas)
		titulo = fonte_titulo.render("SPACE RESCUE", True, COR_CIANO)
		tela.blit(titulo, (28, 24))
		subtitulo = fonte.render(
			"Encontre o sinal de emergencia mais proximo", True, COR_TEXTO_SUAVE
		)
		tela.blit(subtitulo, (30, 65))
		_desenhar_mapa(tela, pontos, resultado, fonte, fonte_pequena)
		_desenhar_painel(
			tela, pontos, resultado, fonte, fonte_pequena, pygame.mouse.get_pos()
		)

		pygame.display.flip()
		relogio.tick(60)


if __name__ == "__main__":
	main()
