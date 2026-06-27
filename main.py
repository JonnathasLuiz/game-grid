from game.core.engine import GameEngine
from game.models.structures import Building, Enterprise, Agent, Recipe, ResourceType
from game.models.enums import BuildingType, AgentState
import time

def run_simulation():
    print("Iniciando Simulação de Jogo de Malha...")
    engine = GameEngine(20, 20)

    # 1. Configurar Infraestrutura
    # Criar uma "floresta" (custo alto) no caminho direto entre casa e fábricas
    from game.models.enums import TerrainType
    for x in range(5, 8):
        for y in range(2, 8):
            engine.grid_controller.set_terrain(x, y, TerrainType.GRASS, 10) # Custo alto

    # Criar uma "estrada" (custo baixo) contornando a floresta
    for x in range(2, 11):
        engine.grid_controller.set_road(x, 1)
    for y in range(1, 11):
        engine.grid_controller.set_road(10, y)

    # Residência
    home = Building(id="casa_1", type=BuildingType.RESIDENCE, anchor_x=2, anchor_y=2, entrance_cell=(2,2))
    engine.add_building(home)

    # Fábrica de Madeira (Serraria)
    sawmill = Building(id="serraria", type=BuildingType.FACTORY, anchor_x=10, anchor_y=10, entrance_cell=(10,10))
    engine.add_building(sawmill)

    # Receita: Produz 1 Madeira (sem insumos para simplificar o início da cadeia)
    recipe_wood = Recipe(inputs=[], outputs=[{"type": ResourceType.WOOD, "qty": 1}])
    ent_sawmill = Enterprise(building_id="serraria", recipe=recipe_wood)
    engine.add_enterprise(ent_sawmill)

    # Fábrica de Móveis
    furniture_factory = Building(id="fabrica_moveis", type=BuildingType.FACTORY, anchor_x=15, anchor_y=5, entrance_cell=(15,5))
    engine.add_building(furniture_factory)

    # Receita: 2 Madeiras -> 1 Móvel
    recipe_furniture = Recipe(
        inputs=[{"type": ResourceType.WOOD, "qty": 2}],
        outputs=[{"type": ResourceType.FURNITURE, "qty": 1}]
    )
    ent_furniture = Enterprise(building_id="fabrica_moveis", recipe=recipe_furniture)
    engine.add_enterprise(ent_furniture)

    # 2. Criar NPCs
    # Trabalhador da Serraria
    worker1 = Agent(id="npc_joao", name="João", home_building_id="casa_1", work_building_id="serraria",
                    logical_cell=(2,2), movement_speed=0.5)
    engine.add_agent(worker1)

    # Trabalhador da Fábrica de Móveis
    worker2 = Agent(id="npc_maria", name="Maria", home_building_id="casa_1", work_building_id="fabrica_moveis",
                    logical_cell=(3,2), movement_speed=0.5)
    engine.add_agent(worker2)

    # Transportador (Logística)
    carrier = Agent(id="npc_pedro", name="Pedro", home_building_id="casa_1", work_building_id=None,
                    logical_cell=(2,2), movement_speed=0.8)
    engine.add_agent(carrier)

    print("Mundo configurado. Iniciando loop temporal...")

    # 3. Loop de Simulação (Simular 24 horas de jogo)
    # 24 horas * 10 ticks/hora = 240 ticks
    for t in range(240):
        engine.tick()
        status = engine.get_status()

        # Logar eventos interessantes
        current_time = status["time"]

        # O sistema de logística agora cria ordens automaticamente via matchmaking!
        # Vamos apenas logar quando novas ordens aparecerem.
        if t % 20 == 0:
            print(f"--- Hora: {current_time} ---")
            for aid, data in status["agents"].items():
                print(f"  NPC {aid}: {data['state']} em {data['pos']}")
            print(f"  Produção Serraria: {status['production']['serraria']:.1f}% | Estoque: {sawmill.inventory.get_quantity(ResourceType.WOOD)} Wood")
            print(f"  Produção Móveis: {status['production']['fabrica_moveis']:.1f}% | Estoque: {furniture_factory.inventory.get_quantity(ResourceType.WOOD)} Wood, {furniture_factory.inventory.get_quantity(ResourceType.FURNITURE)} Furniture")

    print("--- Simulação Finalizada ---")
    print(f"Estoque Final Serraria: {sawmill.inventory.items}")
    print(f"Estoque Final Fábrica de Móveis: {furniture_factory.inventory.items}")

if __name__ == "__main__":
    run_simulation()
