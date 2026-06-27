import { GridController } from './Grid';
import { Vector2 } from '../types';

interface Node {
  x: number;
  y: number;
  g: number;
  h: number;
  f: number;
  parent: Node | null;
}

export class Pathfinding {
  constructor(private gridController: GridController) {}

  public findPath(start: Vector2, end: Vector2): Vector2[] | null {
    const startNode: Node = { x: start.x, y: start.y, g: 0, h: this.heuristic(start, end), f: 0, parent: null };
    startNode.f = startNode.h;

    const openList: Node[] = [startNode];
    const closedList: Set<string> = new Set();

    while (openList.length > 0) {
      // Sort to get the node with the lowest f value
      openList.sort((a, b) => a.f - b.f);
      const currentNode = openList.shift()!;

      if (currentNode.x === end.x && currentNode.y === end.y) {
        return this.reconstructPath(currentNode);
      }

      closedList.add(`${currentNode.x},${currentNode.y}`);

      const neighbors = this.getNeighbors(currentNode);
      for (const neighbor of neighbors) {
        if (closedList.has(`${neighbor.x},${neighbor.y}`)) continue;

        const cell = this.gridController.getCell(neighbor.x, neighbor.y);
        if (!cell || cell.movement_cost === Infinity) continue;

        const tentativeG = currentNode.g + cell.movement_cost;

        let neighborInOpen = openList.find(n => n.x === neighbor.x && n.y === neighbor.y);

        if (!neighborInOpen) {
          const newNode: Node = {
            x: neighbor.x,
            y: neighbor.y,
            g: tentativeG,
            h: this.heuristic(neighbor, end),
            f: 0,
            parent: currentNode,
          };
          newNode.f = newNode.g + newNode.h;
          openList.push(newNode);
        } else if (tentativeG < neighborInOpen.g) {
          neighborInOpen.g = tentativeG;
          neighborInOpen.f = neighborInOpen.g + neighborInOpen.h;
          neighborInOpen.parent = currentNode;
        }
      }
    }

    return null; // No path found
  }

  private heuristic(a: Vector2, b: Vector2): number {
    return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
  }

  private getNeighbors(node: Node): Vector2[] {
    const neighbors: Vector2[] = [];
    const dirs = [
      { x: 0, y: -1 }, { x: 0, y: 1 },
      { x: -1, y: 0 }, { x: 1, y: 0 },
    ];

    for (const dir of dirs) {
      const x = node.x + dir.x;
      const y = node.y + dir.y;
      if (x >= 0 && x < this.gridController.getWidth() && y >= 0 && y < this.gridController.getHeight()) {
        neighbors.push({ x, y });
      }
    }

    return neighbors;
  }

  private reconstructPath(node: Node): Vector2[] {
    const path: Vector2[] = [];
    let current: Node | null = node;
    while (current) {
      path.push({ x: current.x, y: current.y });
      current = current.parent;
    }
    return path.reverse();
  }
}
