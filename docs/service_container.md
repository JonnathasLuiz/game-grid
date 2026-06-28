# Service Container e Injeção de Dependência

Este documento descreve o sistema de Injeção de Dependência (DI) e o Grafo de Execução (DAG) introduzidos na versão 3.0 da arquitetura.

## ServiceContainer (`game/core/service_container.py`)
O `ServiceContainer` é o cofre central de dependências. Ele gerencia instâncias (Singletons), associa tags a serviços e resolve a ordem de execução.

### Principais Funcionalidades:
- **Singleton**: Garante uma instância única para um serviço.
- **Tagging**: Agrupa serviços sob uma etiqueta (ex: `gameplay_update`).
- **DAG (Topological Sort)**: Resolve dependências entre tags para garantir que sistemas base rodem antes de sistemas dependentes.
- **Micro-Order (Prioridade)**: Ordena serviços dentro de uma mesma tag usando `SystemPriority`.

## Gestão de Tags e Dependências

### Tags de Execução
As tags permitem agrupar sistemas que devem ser executados em fases específicas do loop.
- `container.tag(tag_name, [service_names], priority)`: Associa serviços a uma tag com uma prioridade específica.

### Micro-Ordem (SystemPriority)
Dentro de uma mesma tag, os sistemas são executados em ordem crescente de prioridade.
- Ex: Se `Physics` tem prioridade 100 e `AI` tem 500, ambos na tag `gameplay_update`, o `Physics` rodará primeiro.

### Macro-Ordem (Dependências de Tags)
As tags podem depender umas das outras, criando um Grafo Direcionado Acíclico (DAG).
- `container.add_tag_dependency(tag, depends_on)`: Garante que `tag` só execute APÓS `depends_on`.
- Ex: `container.add_tag_dependency("gameplay_update", depends_on="core_update")` garante que os sistemas de gameplay só rodem após os sistemas de core estarem prontos.

### Exemplo de Uso:
```python
container = ServiceContainer()
container.singleton("MyService", MyService())
container.tag("core_update", ["MyService"], priority=SystemPriority.CORE_ENGINE)
```

## Service Providers (`game/modules/providers/`)
Módulos responsáveis por configurar o container. Cada provider deve implementar `IServiceProvider`.

### Ciclo de Vida:
1. **register(container)**: Instancia serviços e define tags. Não deve acessar outros serviços.
2. **boot(container)**: Configura dependências entre serviços e define regras de precedência de tags (`add_tag_dependency`).

## SystemManager (`game/core/system_manager.py`)
Orquestrador do Loop de Jogo. Ele solicita ao container a lista de sistemas resolvidos por tags e os executa na ordem correta.

### Como utilizar no Main:
```python
app_container = ServiceContainer()
providers = [CoreServiceProvider(), MyServiceProvider(), SystemServiceProvider()]

for p in providers: p.register(app_container)
for p in providers: p.boot(app_container)

manager = app_container.resolve("SystemManager")
while True:
    manager.update_all(delta_time)
```

## SystemPriority (`game/core/system_priority.py`)
Enum que define a ordem interna de execução dentro de uma tag, evitando números mágicos.
- `INPUT`: 0
- `CORE_ENGINE`: 100
- `ECONOMY_SYSTEMS`: 300
- `LOGISTICS`: 400
- `AI_DECISION`: 500
- `RENDER`: 1000
