# Case I — Relatório de Suitability

## Resumo da solução

O motor calcula o risco da carteira como uma média ponderada pelo valor investido. Para avaliar uma nova compra, inclui o valor e o risco da ordem no cálculo e compara o risco projetado com 110% do score máximo de risco do cliente. O status `Alerta` indica que o limite foi ultrapassado; `Aprovado` indica que ficou dentro do limite.

O motor calcula e informa o resultado. A execução da ordem e o registro de eventual ciência do cliente pertencem aos sistemas que orquestram o fluxo de compra.

## 1. Regulação e negócio: cliente insiste após o alerta

Se a política aprovada permitir que o cliente prossiga após um alerta, a jornada deve apresentar o termo de ciência antes de enviar a ordem para execução. O aceite precisa ser uma ação afirmativa e estar vinculado à ordem e à avaliação que originaram o alerta. Se os dados relevantes da ordem mudarem, o sistema deve recalcular o risco e solicitar nova ciência quando necessário.

Para permitir auditoria posterior, a plataforma deve registrar, de forma protegida e com acesso controlado:

- cliente, ordem, ativo, valores e horário da avaliação;
- carteira e perfil considerados, risco projetado, limite aplicado e resultado;
- versão da regra usada no cálculo;
- versão do termo apresentado, canal, horário e evidência de autenticação do aceite;
- decisão final da ordem e motivo de eventual bloqueio ou falha.

Os registros da avaliação, do aceite e da ordem devem poder ser correlacionados. O processamento também deve evitar ordens duplicadas em caso de reenvio ou falha de comunicação. Sem um aceite válido, a ordem deve permanecer pendente ou ser bloqueada conforme a política definida por Compliance.

Compliance e negócio devem definir o texto e a validade do termo, quais operações podem prosseguir, o tratamento de casos severos, os prazos de retenção e quem pode consultar ou alterar esses dados. O motor não deve presumir o aceite nem decidir sozinho que qualquer alerta pode ser ignorado.

## 2. Desenquadramento passivo e comunicação ao cliente

O motor pode ser reaproveitado por um processo periódico de monitoramento. Esse processo atualiza os valores das posições com dados de mercado, recalcula o risco ponderado e compara o resultado com o perfil e os limites vigentes. Cada avaliação deve guardar a data e hora, os valores e a origem dos dados, o resultado e a versão da regra, para que seja possível explicar o alerta.

O monitoramento deve diferenciar uma carteira dentro do limite de uma avaliação que não pôde ser concluída por dados ausentes ou desatualizados. Para reduzir notificações repetidas, pode deduplicar alertas e aplicar regras de persistência ou escalonamento definidas por negócio e Compliance. Falhas no cálculo ou na atualização dos dados devem gerar um aviso operacional, em vez de serem tratadas como conformidade.

Os canais podem trabalhar em conjunto:

- **Aplicativo:** aviso rápido na área autenticada, com data da avaliação, explicação e próximos passos;
- **E-mail:** resumo durável da comunicação e referência ao aplicativo, evitando expor informações sensíveis desnecessárias;
- **Assessor:** contato em situações persistentes ou relevantes conforme critérios definidos, oferecendo orientação adequada ao cliente.

A escolha e a ordem dos canais devem considerar as preferências do cliente e as regras de comunicação aplicáveis. O sistema deve registrar o envio, a entrega ou a falha da notificação. Receber um aviso não deve ser confundido com aceitar uma operação ou com uma nova ordem de investimento.

## Observação sobre os exemplos do enunciado

Usando os dados fornecidos para a carteira e a nova ordem, o risco atual é aproximadamente `1,6667` e o projetado é `1,8077`. Como o limite de alerta para score máximo `2,5` é `2,75`, esse conjunto de dados resulta em `Aprovado`. A saída ilustrativa de alerta com risco `2,78` não corresponde aos mesmos valores de entrada; essa divergência deve ser esclarecida pelo responsável pelo case.

## Limite não especificado

O enunciado apresenta um caso de rejeição severa, mas não define o corte numérico para separar `Alerta` de `Rejeitado`. Portanto, a implementação atual aplica apenas o limite de alerta especificado. Um limiar de rejeição deve ser definido e aprovado por negócio e Compliance antes de ser adicionado.
