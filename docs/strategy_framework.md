# Strategy Framework (Framework de Estratégias)

O **Strategy Framework** é o motor comportamental central do simulador, localizado em `game/core/strategy/`. Ele permite que entidades (como NPCs e Edifícios) tenham seus comportamentos definidos e alterados de forma dinâmica e desacoplada.

## Motivação
Anteriormente, as lógicas de comportamento estavam presas aos seus respectivos módulos. Isso dificultava a reutilização e tornava o sistema rígido. Com o Strategy Framework, centralizamos a execução e padronizamos a interface de todos os comportamentos do jogo.

## Componentes Principais

### 1. StrategyBase (`base.py`)
É a classe base abstrata (interface) para todas as estratégias.
- **`execute(delta_time)`**: Método obrigatório que define o que a estratégia faz a cada tick. O uso de `delta_time` garante que a simulação seja independente da taxa de quadros (framerate).
- **Injeção Automática**: Toda estratégia recebe em seu construtor referências ao `owner` (quem possui a estratégia), `EventBus`, `GridSystem` e o próprio `Kernel`.

### 2. StrategyKernel (`kernel.py`)
O gerenciador e fábrica de estratégias.
- **Registro**: Centraliza todas as classes de comportamento disponíveis.
- **Validação de Capacidades**: Antes de instanciar uma estratégia, o Kernel verifica se a entidade alvo possui permissão para usá-la (através do atributo `allowStrategies`).
- **Instanciação**: Cria a instância da estratégia injetando todas as dependências necessárias de forma agnóstica.

## Configuração Declarativa

As entidades não precisam conhecer os detalhes internos das estratégias, elas apenas declaram suas intenções:

- **`allowStrategies`**: Um conjunto (`set`) que define quais comportamentos aquela classe de entidade suporta. Isso evita, por exemplo, que um NPC tente executar uma lógica de "Fábrica".
- **`strategyStart`**: Define qual estratégia deve ser iniciada automaticamente assim que a entidade é criada.

### Exemplo em `BuildingEntity`:
```python
class BuildingEntity:
    allowStrategies = {"BLUEPRINT", "FACTORY"}
    strategyStart = "BLUEPRINT"
```

## Hot-Swapping (Troca a Quente)

Uma das maiores vantagens deste framework é o suporte a **Hot-Swapping**. Uma entidade pode alterar completamente seu comportamento em tempo de execução sem precisar ser destruída ou recriada.

**Como funciona:**
A entidade possui um método (ex: `set_logic()` ou `set_behavior()`) que substitui a instância da estratégia atual por uma nova, gerada pelo Kernel. Isso permite, por exemplo, que um edifício em construção (`BLUEPRINT`) se transforme instantaneamente em uma fábrica operacional (`FACTORY`) assim que o progresso atinge 100%.

## Benefícios
1. **Desacoplamento Total**: O módulo de construção não precisa saber como a fábrica funciona, apenas que ele pode usar a estratégia "FACTORY".
2. **Reutilização**: Estratégias genéricas podem ser compartilhadas entre diferentes tipos de entidades.
3. **Escalabilidade**: Adicionar novos comportamentos é tão simples quanto criar uma nova classe e registrá-la no Kernel.
