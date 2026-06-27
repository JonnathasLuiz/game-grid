export enum TerrainType {
  GRASS = 'GRASS',
  DIRT = 'DIRT',
  WATER = 'WATER',
  ROAD = 'ROAD',
}

export enum OccupantType {
  NONE = 'NONE',
  BUILDING = 'BUILDING',
  DECORATION = 'DECORATION',
  NATURAL_RESOURCE = 'NATURAL_RESOURCE',
}

export interface Cell {
  x: number;
  y: number;
  terrain_type: TerrainType;
  movement_cost: number;
  is_occupied: boolean;
  occupant_type: OccupantType;
  occupant_id: string | null;
  reservation_id: string | null;
}

export enum BuildingType {
  RESIDENCE = 'RESIDENCE',
  FACTORY = 'FACTORY',
  WAREHOUSE = 'WAREHOUSE',
}

export type ResourceType = 'WOOD' | 'FURNITURE' | 'IRON' | 'STEEL' | 'COAL';

export interface InventoryObject {
  [key: string]: number;
}

export interface RecipeItem {
  type: ResourceType;
  qty: number;
}

export interface Recipe {
  inputs: RecipeItem[];
  outputs: RecipeItem[];
}

export enum NPCState {
  IDLE = 'IDLE',
  COMMUTING_TO_WORK = 'COMMUTING_TO_WORK',
  WORKING = 'WORKING',
  COMMUTING_TO_HOME = 'COMMUTING_TO_HOME',
  LOGISTICS_TASK = 'LOGISTICS_TASK',
}

export interface Vector2 {
  x: number;
  y: number;
}

export interface TransportOrder {
  id: string;
  resourceType: ResourceType;
  quantity: number;
  originBuildingId: string;
  destinationBuildingId: string;
  status: 'PENDING' | 'ASSIGNED' | 'PICKED_UP' | 'COMPLETED';
}
