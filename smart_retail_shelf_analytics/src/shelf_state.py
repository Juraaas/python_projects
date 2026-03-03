class ShelfStateManager:
    def __init__(self,
                 shelf_bbox: tuple,
                 grid_rows: int = 2,
                 grid_cols: int = 4):
        self.shelf_bbox = shelf_bbox
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

        self.slot_width = (shelf_bbox[2] - shelf_bbox[0]) / grid_cols
        self.slot_height = (shelf_bbox[3] - shelf_bbox[1]) / grid_rows
        self.total_slots = grid_rows * grid_cols
    
    def _get_slot_index(self, center_x: float, center_y: float):
        x1, y1, x2, y2 = self.shelf_bbox

        if not (x1 <= center_x <= x2 and y1 <= center_y <= y2):
            return None
        
        col = int((center_x - x1) / self.slot_width)
        row = int((center_y - y1) / self.slot_height)

        if col >= self.grid_cols:
            col = self.grid_cols - 1
        if row >= self.grid_rows:
            row = self.grid_rows - 1

        return row * self.grid_cols + col
    
    def update(self, objects: list) -> dict:
        """
        :param objects: stabilized objects (with bbox)
        :returns shelf_state dict
        """
        occupied_slots = set()

        for obj in objects:
            if "bbox" not in obj:
                continue

            x1, y1, x2, y2 = obj["bbox"]
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            slot_index = self._get_slot_index(center_x, center_y)

            if slot_index is not None:
                occupied_slots.add(slot_index)

        occupancy_map = [
            1 if i in occupied_slots else 0
            for i in range(self.total_slots)
        ]

        return {
            "occupied_slots": len(occupied_slots),
            "total_slots": self.total_slots,
            "occupancy_ratio": len(occupied_slots) / self.total_slots,
            "occupancy_map": occupancy_map,
        }