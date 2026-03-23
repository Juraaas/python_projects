def enrich_event(event, mode):
    if mode == "entry":
        return {
            **event,
            "camera": "entry_cam_1",
        }
    else:
        return {
            **event,
            "type": "vehicle_exit_detected",
            "camera": "exit_cam_1",
        }