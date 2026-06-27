"""
Grid System module for spatial management and pathfinding.
"""
import heapq

class GridSystem:
    """
    Manages a 2D grid, entity occupancy, and pathfinding.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.occupants = {}  # (x, y) -> entity_id

    def is_walkable(self, x, y):
        """
        Checks if a cell is within bounds and not occupied.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return (x, y) not in self.occupants

    def occupy(self, x, y, entity_id):
        """
        Marks a cell as occupied by an entity.
        """
        self.occupants[(x, y)] = entity_id

    def release(self, x, y):
        """
        Clears occupancy for a cell.
        """
        if (x, y) in self.occupants:
            del self.occupants[(x, y)]

    def find_path(self, start, end):
        """
        Calculates a path from start to end using A* algorithm.
        Returns a list of (x, y) coordinates or None if no path exists.
        """
        if start == end:
            return [start]

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, end)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                # For pathfinding, we allow the 'end' cell even if occupied
                # if it's the target interaction cell.
                if not self.is_walkable(*neighbor) and neighbor != end:
                    continue

                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None # No path found

    def _heuristic(self, a, b):
        """
        Manhattan distance heuristic for A*.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, pos):
        """
        Returns adjacent cells (4-way).
        """
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbors.append((x + dx, y + dy))
        return neighbors

    def _reconstruct_path(self, came_from, current):
        """
        Reconstructs the path from A* data.
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
