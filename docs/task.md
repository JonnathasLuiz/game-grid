# Task Management Documentation

O domínio `task` é responsável pela orquestração de demandas econômicas.

## TaskManager (`manager.py`)
Um serviço de matchmaking sem estado físico.
- **Função**: Escuta o `EventBus` para novas tarefas (`NOVA_TAREFA`) e as transforma em ordens executáveis (`ORDEM_CRIADA`).
- **Desacoplamento**: Garante que o sistema que gera a demanda não precise conhecer o NPC que irá executá-la.
