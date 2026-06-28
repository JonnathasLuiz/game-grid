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

## KernelRegistry (`kernel.py`)
O catálogo e fábrica do sistema.
- **Função**: Centraliza o registro de classes de comportamento e lógica, injetando as dependências necessárias (`EventBus` e `GridSystem`) no momento da instanciação.
- **Injeção de Dependência**: Garante que os comportamentos não precisem de imports circulares ou referências globais.

## ServiceContainer e Orquestração (`service_container.md`)
Para detalhes sobre o novo sistema de Injeção de Dependência (DI) e o Grafo de Execução (DAG), consulte a [Documentação do Service Container](./service_container.md).
