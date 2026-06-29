# Guia de Migração: Python para JavaScript (Node.js)

Este documento descreve as diretrizes técnicas para a migração do motor de simulação de Python para JavaScript (ES6+ / Node.js).

## 1. Mapeamento de Tipos

| Tipo Python | Tipo JavaScript / TypeScript | Notas |
| :--- | :--- | :--- |
| `int` | `number` | JS não diferencia inteiros de decimais nativamente. |
| `float` | `number` | |
| `bool` | `boolean` | `True` -> `true`, `False` -> `false`. |
| `str` | `string` | |
| `list` | `Array` | Ex: `[]`. |
| `dict` | `Object` ou `Map` | Use `Map` se as chaves forem dinâmicas ou não-strings. |
| `tuple` | `Array` (Readonly) | JS não possui tuplas nativas imutáveis. |
| `set` | `Set` | Útil para `allowStrategies` no `Entity`. |
| `None` | `null` ou `undefined` | Recomendado `null` para ausência intencional de valor. |

## 2. Tradução de Estruturas de Dados

### Listas e Dicionários
*   **Listas:** O `list` do Python mapeia diretamente para `Array` em JS. Use `push()` em vez de `append()`.
*   **Dicionários:** Para o `GridSystem.occupants`, onde a chave é uma tupla `(x, y)`, em JS um `Object` ou `Map` não aceita arrays como chaves únicas por valor. Recomenda-se converter a coordenada em uma string chave: ``const key = `${x},${y}`;``.
*   **DefaultDict:** O `defaultdict(list)` usado no `EventBus` deve ser substituído por um `Map` com lógica de inicialização:
    ```javascript
    if (!this.subscribers.has(eventType)) {
        this.subscribers.set(eventType, []);
    }
    this.subscribers.get(eventType).push(callback);
    ```

### Sets (Conjuntos)
*   Utilizados para `allowStrategies`. Em JS: `new Set(['STRATEGY_A', 'STRATEGY_B'])`. Use `has()` para verificação.

### Heapq (Filas de Prioridade)
*   O Python utiliza `heapq` para o algoritmo A*. JavaScript não possui uma fila de prioridade nativa. É necessário utilizar uma biblioteca externa (ex: `datastructures-js/priority-queue`) ou implementar um Binary Heap manual.

## 3. Gerenciamento de Assincronismo

Embora o código atual seja síncrono, a migração para Node.js permite o uso de padrões assíncronos para I/O ou processamento paralelo futuro.

*   **Async/Await:** Substitua `def func()` assíncronos por `async function func()`.
*   **Promises:** Utilize `Promise.all()` se houver necessidade de inicializar múltiplos serviços em paralelo no `bootstrap`.
*   **Event Loop:** O "Game Loop" em JS pode ser implementado com um `while` simples (como no Python) para simulações CLI, ou `setImmediate()` / `requestAnimationFrame()` em ambientes de interface.

## 4. Dependências e Bibliotecas

| Biblioteca Python | Equivalente NPM | Finalidade |
| :--- | :--- | :--- |
| `heapq` | `datastructures-js/priority-queue` | Algoritmo A* (Pathfinding). |
| `collections.defaultdict` | Implementação manual com `Map` | Gerenciamento de eventos no `EventBus`. |
| `abc.ABC / abstractmethod` | TypeScript `abstract class` ou erro em runtime | Interfaces de Estratégias e Logics. |
| `enum.IntEnum` | `enum` (TS) ou `Object.freeze()` (JS) | Prioridades do sistema. |

## 5. Considerações de Escopo e Contexto

### `this` vs `self`
*   No Python, `self` é passado explicitamente. No JS, `this` é implícito mas seu contexto pode mudar.
*   **Atenção:** Ao passar callbacks (ex: no `EventBus` ou `subscribe`), use **Arrow Functions** `() => this.method()` para preservar o contexto de `this`, ou utilize `.bind(this)`.

### Manipulação de Erros
*   Substitua blocos `try/except` por `try/catch`.
*   Em vez de `raise ValueError("msg")`, utilize `throw new Error("msg")`.

### Construtores e Herança
*   `__init__` torna-se `constructor`.
*   `super().__init__(...)` torna-se `super(...)`.

### Keyword Arguments (`**kwargs`)
*   JS não suporta `**kwargs` nativamente da mesma forma. Utilize **Object Destructuring**:
    ```javascript
    // Python
    def func(self, name, **kwargs): ...

    // JS
    func(name, { opt1, opt2 } = {}) { ... }
    ```

## 6. Fluxo de Execução (Guia de Portabilidade)

Para portar o código, siga esta sequência lógica:

1.  **Core Foundation:**
    *   Implemente o `EventBus` (Pub/Sub).
    *   Implemente o `ServiceContainer` (Gerenciador de Injeção de Dependência e DAG para Tags).
    *   Implemente o `GridSystem` (incluindo o A*).

2.  **Strategy Framework:**
    *   Crie a classe abstrata `StrategyBase`.
    *   Implemente o `StrategyKernel` para gerenciar a criação dinâmica de estratégias via `ServiceContainer`.

3.  **Modules:**
    *   Porte as entidades (`NpcAgent`, `BuildingEntity`) garantindo que as propriedades `allowStrategies` e `strategyStart` sejam respeitadas.
    *   Porte os sistemas (`NpcSystem`, `BuildingSystem`, `TaskManager`).

4.  **Service Providers:**
    *   Crie os providers que encapsulam a fase de `register` (registro de instâncias) e `boot` (ligação de dependências).

5.  **Main Loop:**
    *   Implemente o bootstrap no `main.js`.
    *   Execute o loop de ticks invocando o `SystemManager.updateAll(deltaTime)`.

6.  **Validação:**
    *   O sucesso da migração é atingido quando o log do `main.js` reflete o ciclo: NPC se move -> NPC executa construção no prédio -> Prédio completa transição de `BLUEPRINT` para `FACTORY`.
