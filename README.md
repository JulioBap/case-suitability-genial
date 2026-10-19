# Motor de Suitability — Case I

Projeto em Python que calcula o risco ponderado de uma carteira após uma nova compra e compara o resultado ao limite de alerta do cliente.

## Como executar

É necessário ter Python 3 instalado. No terminal, dentro desta pasta, execute:

```powershell
python main.py
```

O programa lê as informações de `example.json` e imprime a decisão em formato JSON. Para avaliar um arquivo diferente, informe seu nome no comando:

```powershell
python main.py outro_cenario.json
```

Os arquivos JSON devem manter a mesma estrutura:

- `cliente`: perfil e `score_max_risco`;
- `carteira_atual`: ativos com `risco` e `valor_investido`;
- `nova_ordem`: ativo com `risco` e `valor_ordem`.

## Regra implementada

O risco da carteira é a média ponderada pelo valor investido. O risco projetado inclui o valor da nova ordem. Se o risco projetado ultrapassar `110%` do score máximo do cliente, o resultado é `Alerta`; caso contrário, é `Aprovado`.

O enunciado não define o limiar para um desenquadramento severo. Por isso, o código não inventa um corte para `Rejeitado`; essa política precisa ser definida pelo negócio e por Compliance.

## Arquivos

- `suitability.py`: funções de cálculo e decisão;
- `main.py`: leitura dos dados, chamada do motor e impressão do resultado;
- `example.json`: dados de exemplo;
- `case-report.md`: respostas às questões de negócio do case.
