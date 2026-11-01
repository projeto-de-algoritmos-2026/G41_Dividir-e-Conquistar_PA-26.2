# Space Rescue

Jogo em Pygame para encontrar os dois sinais de emergência mais próximos em um
mapa espacial. Depois de executar a busca, selecione os dois sinais no mapa para
confirmar o resgate e marcar pontos.

## Demonstração

![Space Rescue: busca pelo par mais próximo e resgate concluído](assets/print.png)

## Como executar

Na raiz do repositório, instale as dependências e inicie o jogo:

```bash
python -m pip install -r requirements.txt
python src/main.py
```

No Windows, também é possível usar um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\main.py
```

## Como jogar

1. Ajuste a quantidade de sinais entre 2 e 500 com os botões **-** e **+** ou
   as setas do teclado. A alteração gera um mapa novo.
2. Pressione **Buscar par mais próximo** ou **Espaço** para executar os
   algoritmos. O jogo destaca o par e mostra a distância mínima e o tempo de
   execução de cada algoritmo.
3. Clique nos dois sinais que formam o par mais próximo. Ao acertar, o resgate é
   confirmado e a pontuação aumenta.

Outros controles:

- **Novo mapa** ou **N**: gera outro mapa com a quantidade atual de sinais.
- **Reiniciar** ou **R**: restaura o mapa inicial e zera a pontuação.
- **Esc**: fecha o jogo.

## Testes

Execute os testes dos algoritmos e da validação do par selecionado:

```bash
python -m unittest discover -v
```
