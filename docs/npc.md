# NPC System Documentation

O domínio `npc` gerencia os agentes autônomos que operam no simulador.

## NpcAgent (`agent.py`)
A representação física do NPC.
- **Conceito**: Uma "casca" (shell) sem lógica intrínseca.
- **Propriedades**: `id`, `state`, `logical_cell`, `inventory`, `behavior`.
- **Funcionamento**: O método `.update()` delega a execução para o objeto `behavior` injetado.

## NpcSystem (`system.py`)
O gestor da população de NPCs.
- **Função**: Escuta ordens do `EventBus` (`ORDEM_CRIADA`) e as atribui a NPCs ociosos.
- **Matchmaking**: Atualmente utiliza uma lógica simples de "primeiro disponível".

## Behaviors (`behaviors/`)
Onde reside a inteligência dos NPCs, agora integrados ao **Strategy Framework**.

- **BehaviorGeneric**: Interface base para todos os comportamentos de NPCs, herdando de `StrategyBase`.
- **BehaviorBuild**: Implementa a lógica de construção. O NPC caminha até a entrada do edifício e emite eventos de `PROGRESSO_GERADO` a cada tick.
