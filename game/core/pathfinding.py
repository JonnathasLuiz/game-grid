import heapq
from typing import List, Tuple, Optional, Dict
from .grid import GridController

class AStarPathfinding:
    def __init__(self, grid_controller: GridController):
        self.gc = grid_controller

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            cell = self.gc.get_cell(nx, ny)
            if cell and cell.movement_cost < float('inf'):
                # In our simulation, building cells are occupied but their entrance is accessible.
                # However, usually we don't walk THROUGH buildings.
                # If it's occupied by a building, only the entrance should be accessible if it's the target.
                # For simplicity, we just check movement_cost and is_occupied.
                if not cell.is_occupied:
                    neighbors.append((nx, ny))
                # Note: This might need refinement for "entering" buildings.
        return neighbors

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
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

            for next_node in self.get_neighbors(current):
                cell = self.gc.get_cell(next_node[0], next_node[1])
                new_cost = cost_so_far[current] + cell.movement_cost

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from:
            # Maybe the goal is occupied (like an entrance cell that is actually walkable but marked differently)
            # Special case for building entrances: if goal is occupied but it's our target,
            # we should allow it.
            # Let's adjust get_neighbors or find_path to allow goal even if occupied.
            pass

        # Reconstruct path
        path = []
        curr = goal
        if goal not in came_from:
            # Check if any neighbor of goal is reachable
            return [] # No path found

        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path

    # Refined neighbors to allow target cell even if occupied
    def get_neighbors_refined(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            cell = self.gc.get_cell(nx, ny)
            if cell and cell.movement_cost < float('inf'):
                if not cell.is_occupied or (nx, ny) == goal:
                    neighbors.append((nx, ny))
        return neighbors

    def find_path_refined(self, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        if start == goal:
            return [start]

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal: break

            for next_node in self.get_neighbors_refined(current, goal):
                cell = self.gc.get_cell(next_node[0], next_node[1])
                new_cost = cost_so_far[current] + cell.movement_cost
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

        if goal not in came_from: return []
        path = []
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path
