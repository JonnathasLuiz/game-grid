# Grid-Based Economic and Logistic Simulator

## Visão Geral
Este projeto é um simulador econômico e logístico baseado em malha (grid-based). O sistema simula um ecossistema onde NPCs se deslocam fisicamente pelo mapa para realizar tarefas de forma autônoma, como construção e transporte.

## Arquitetura
A aplicação segue uma arquitetura estritamente desacoplada utilizando:
- **Event-Driven Architecture (Event Bus)**: Toda a comunicação entre sistemas é feita via eventos.
- **Strategy Pattern**: O comportamento de NPCs e Edifícios é definido por classes de lógica injetadas em tempo de execução.
- **Kernel/Registry**: Um componente central que atua como fábrica e injetor de dependências (EventBus e GridSystem).

### Principais Sistemas
- **Core Systems**: EventBus, GridSystem (A* Pathfinding), e KernelRegistry.
- **NpcSystem**: Gerencia agentes NPCs e seus comportamentos (Behaviors).
- **BuildingSystem**: Gerencia edifícios e suas lógicas internas (Logics).
- **TaskManager**: Realiza o matchmaking entre demandas e ordens.

## Como Executar

### Simulação
Para rodar a demonstração básica da simulação (fluxo de construção):
```bash
python3 main.py
```

### Testes
Para executar os testes automatizados:
```bash
PYTHONPATH=. python3 tests/test_simulation.py
```

## Documentação Detalhada
A documentação específica de cada módulo pode ser encontrada na pasta `/docs`:
- [Core Systems](./docs/core.md)
- [Strategy Framework](./docs/strategy_framework.md)
- [Service Container & DI](./docs/service_container.md)
- [NPC System](./docs/npc.md)
- [Building System](./docs/building.md)
- [Task Management](./docs/task.md)
