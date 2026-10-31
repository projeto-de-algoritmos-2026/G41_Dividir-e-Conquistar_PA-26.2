# Space Rescue

Jogo visual em Pygame para localizar os dois sinais de emergencia mais proximos
em um mapa espacial. A busca usa o algoritmo de dividir e conquistar
implementado no projeto.

## Executar

Na raiz do repositorio, instale a dependencia e inicie o jogo:

```bash
python -m pip install -r requirements.txt
python src/main.py
```

No Windows, tambem e possivel criar e ativar um ambiente virtual antes de
instalar as dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\main.py
```

## Controles

- **Novo mapa** ou **N**: gera outro mapa com a mesma quantidade de sinais.
- **Buscar par mais proximo** ou **Espaco**: executa a busca e destaca os dois
  sinais mais proximos, a linha entre eles e a distancia calculada.
- **Reiniciar** ou **R**: restaura o mapa inicial.
- **Esc**: fecha o jogo.

Os sinais sao gerados dentro do setor de resgate e identificados por numeros.
