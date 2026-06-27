class BuildingEntity:
    def __init__(self, building_id, b_type, x, y, entrance_x, entrance_y):
        self.id = building_id
        self.type = b_type
        self.anchor_x = x
        self.anchor_y = y
        self.entrance_cell = (entrance_x, entrance_y)
        self.inventory = {}
        self.logic = None

    def update(self):
        if self.logic:
            self.logic.execute()
