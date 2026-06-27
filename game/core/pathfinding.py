import heapq
from typing import List, Tuple, Optional, Dict
from .grid import GridController

class AStarPathfinding:
    """
    Implementação do algoritmo A* para navegação na malha do jogo.
    Leva em conta o custo de movimento de cada célula e permite alcançar a célula de destino
    mesmo que esta esteja marcada como ocupada (necessário para entradas de edifícios).
    """
    def __init__(self, grid_controller: GridController):
        self.gc = grid_controller

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Calcula a distância de Manhattan entre dois pontos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Retorna os vizinhos acessíveis de uma célula, incluindo o objetivo se estiver ocupado."""
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            cell = self.gc.get_cell(nx, ny)
            if cell and cell.movement_cost < float('inf'):
                # Permite mover para células não ocupadas ou para o objetivo exato
                if not cell.is_occupied or (nx, ny) == goal:
                    neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Encontra o caminho mais curto entre start e goal usando A*.
        Retorna uma lista de coordenadas (x, y).
        """
        if start == goal:
            return [start]

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        cost_so_far: Dict[Tuple[int, int], float] = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next_node in self.get_neighbors(current, goal):
                cell = self.gc.get_cell(next_node[0], next_node[1])
                new_cost = cost_so_far[current] + cell.movement_cost

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from:
            return []

        # Reconstrói o caminho
        path = []
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path
