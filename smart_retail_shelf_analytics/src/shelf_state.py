class ShelfStateManager:
    def __init__(self,
                 shelf_bbox: tuple,
                 grid_rows: int = 1,
                 grid_cols: int = 4,
                 presence_threshold: int = 3,
                 absence_threshold: int = 5):
        self.shelf_bbox = shelf_bbox
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols

        self.slot_width = (shelf_bbox[2] - shelf_bbox[0]) / grid_cols
        self.slot_height = (shelf_bbox[3] - shelf_bbox[1]) / grid_rows
        self.total_slots = grid_rows * grid_cols

        self.presence_threshold = presence_threshold
        self.absence_threshold = absence_threshold

        self.presence_counters = [0] * self.total_slots
        self.absence_counters = [0] * self.total_slots
        self.occupancy_map = [0] * self.total_slots
        self.prev_occupancy_map = [0] * self.total_slots
        self.slot_flip_counts = [0] * self.total_slots
        self.total_frames = 0
    
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
        detected_slots = set()

        for obj in objects:
            if "bbox" not in obj:
                continue

            x1, y1, x2, y2 = obj["bbox"]
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            slot_index = self._get_slot_index(center_x, center_y)

            if slot_index is not None:
                detected_slots.add(slot_index)
        
        for i in range(self.total_slots):
            if i in detected_slots:
                self.presence_counters[i] += 1
                self.absence_counters[i] = 0

                if self.presence_counters[i] >= self.presence_threshold:
                    self.occupancy_map[i] = 1
            else:
                self.absence_counters[i] += 1
                self.presence_counters[i] = 0

                if self.absence_counters[i] >= self.absence_threshold:
                    self.occupancy_map[i] = 0
            
        for i in range(self.total_slots):
            if self.occupancy_map[i] != self.prev_occupancy_map[i]:
                self.slot_flip_counts += 1
        
        self.prev_occupancy_map = self.occupancy_map.copy()
        self.total_frames += 1

        total_flips = sum(self.slot_flip_counts)

        if self.total_frames > 0:
            slot_flip_rate = total_flips / (self.total_frames * self.total_slots)
        else:
            slot_flip_rate = 0.0

        occupied_slots = sum(self.occupancy_map)

        return {
            "occupied_slots": occupied_slots,
            "total_slots": self.total_slots,
            "occupancy_ratio": occupied_slots / self.total_slots,
            "occupancy_map": self.occupancy_map.copy(),
            "slot_flip_rate": slot_flip_rate,
            "slot_flip_counts": self.slot_flip_counts.copy(),
        }