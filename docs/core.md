# Core Systems Documentation

O domínio `core` contém a fundação do simulador, fornecendo ferramentas de comunicação, gestão espacial e injeção de dependências.

## EventBus (`event_bus.py`)
Implementa o padrão Publish/Subscribe.
- **Função**: Roteador global de mensagens que desacopla os sistemas.
- **Principais Métodos**:
  - `subscribe(event_type, callback)`: Registra um interessado em um tipo de evento.
  - `publish(event_type, **kwargs)`: Dispara o evento para todos os inscritos.

## GridSystem (`grid_system.py`)
Gerencia a malha matemática do mundo.
- **Função**: Controla colisões, ocupação de células e navegação.
- **Navegação**: Implementa o algoritmo **A*** para busca de caminhos (Pathfinding).
- **Métodos**:
  - `is_walkable(x, y)`: Valida se uma célula está livre e dentro dos limites.
  - `find_path(start, end)`: Retorna uma lista de coordenadas para deslocamento.

## Strategy Framework (`core/strategy/`)
O coração comportamental do simulador. Centraliza a definição de capacidades e comportamentos.

- **StrategyBase (`strategy/base.py`)**: Interface abstrata que define o contrato para todas as estratégias (NPCs e Edifícios).
- **StrategyKernel (`kernel.py`)**: O gerenciador central que valida se uma entidade suporta uma estratégia (`allowStrategies`) e injeta as dependências (`EventBus`, `GridSystem`) na instanciação.
- **Configuração Declarativa**: Entidades definem quais estratégias suportam via `allowStrategies` e qual sua lógica inicial via `strategyStart`.
- **Hot-Swapping**: Permite trocar a estratégia de uma entidade em tempo de execução sem necessidade de reinstanciação.

Para mais detalhes, veja a [Documentação do Strategy Framework](./strategy_framework.md).

## ServiceContainer e Orquestração (`service_container.md`)
Para detalhes sobre o novo sistema de Injeção de Dependência (DI) e o Grafo de Execução (DAG), consulte a [Documentação do Service Container](./service_container.md).
