# Jogo de Malha - Simulação Logística e Economia de NPCs

Este projeto é uma implementação em Python de um simulador baseado em malha (grid), focado em logística, produção industrial e comportamento autônomo de NPCs.

## Visão Geral

A simulação apresenta um mundo onde NPCs vivem em residências, trabalham em fábricas durante o expediente e realizam tarefas logísticas para manter a cadeia de suprimentos ativa.

### Principais Sistemas

1.  **Sistema de Malha (Grid Controller)**: Gerencia o terreno, custos de movimento e reservas de células para evitar colisões físicas entre NPCs.
2.  **Navegação A***: Algoritmo de pathfinding ponderado que leva em conta o tipo de terreno (ex: estradas são mais rápidas que grama).
3.  **Inteligência de NPCs**: NPCs possuem rotinas diárias controladas por uma Máquina de Estados (IDLE, Commuting, Working, Logistics).
4.  **Sistema de Produção**: Empresas validam pessoal, insumos e espaço antes de processar receitas e gerar produtos acabados.
5.  **Sistema Logístico**: Gerenciador de oferta e procura que cria ordens de transporte automaticamente e as atribui a NPCs disponíveis.
6.  **Motor de Jogo (Game Engine)**: Orquestra o tempo global, ciclos de produção e atualizações de estado de todas as entidades.

## Estrutura do Projeto

```
game/
├── core/           # Núcleo da simulação (Grid, Pathfinding, Engine)
├── models/         # Definições de dados (Enums, Dataclasses)
└── systems/        # Lógica de sistemas (NPCs, Produção, Logística)
tests/              # Testes unitários para cada módulo
main.py              # Script principal de demonstração
```

## Como Executar

### Pré-requisitos
- Python 3.7+

### Executando a Simulação
Para rodar a demonstração principal que simula um ciclo de 24 horas:
```bash
python3 main.py
```

### Executando os Testes
Para verificar a integridade dos módulos individualmente:
```bash
for f in tests/test_*.py; do python3 $f; done
```

## Arquitetura Técnica

- **Reserva de Célula**: Implementada no `NPCSystem` para garantir que apenas um NPC ocupe ou planeje ocupar uma célula por vez.
- **Célula de Entrada**: NPCs navegam até a `entrance_cell` de um edifício para interagir com ele, simulando a entrada física na estrutura.
- **Matchmaking Logístico**: O `LogisticsSystem` monitora os estoques das empresas e automaticamente cria ordens de transporte quando insumos estão baixos e há oferta disponível em outro local.
