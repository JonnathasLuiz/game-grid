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
Define a mecânica interna do edifício.
- **LogicBlueprint**: Gerencia o estado de construção. Ao atingir 100% de progresso, solicita ao Kernel a "transmutação" para uma lógica funcional.
- **LogicFactory**: Lógica de uma fábrica operante (pode produzir recursos, etc).
