# Building System Documentation

O domínio `building` gerencia as estruturas e fábricas presentes no mapa.

## BuildingEntity (`entity.py`)
A representação de um edifício.
- **Propriedades**: `id`, `type`, `anchor_x`, `anchor_y`, `entrance_cell`, `logic`.
- **Entrance Cell**: Ponto obrigatório fora do centro onde os NPCs devem estar para interagir com o prédio.

## BuildingSystem (`system.py`)
Gestor de todos os edifícios.
- **Função**: Escuta eventos de progresso e os encaminha para a lógica interna da entidade correta.

## Logics (`logics/`)
Define a mecânica interna do edifício seguindo o padrão **Strategy**.

- **LogicBase (Abstract)**: Classe base abstrata que define a interface para todas as lógicas de edifícios. Garante que todos os edifícios implementem o método `execute` e fornece uma interface padrão para receber progresso via `receive_progress`.
- **LogicBlueprint**: Gerencia o estado de construção. Ao atingir 100% de progresso, solicita ao Kernel a "transmutação" para uma lógica funcional. Implementa o método `receive_progress` para acumular trabalho dos NPCs.
- **LogicFactory**: Lógica de uma fábrica operante (pode produzir recursos, etc).
