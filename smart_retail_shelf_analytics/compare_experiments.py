import os
from src.evaluation import ShelfEvaluator

def summarize(path):
    evaluator = ShelfEvaluator(path)
    report = evaluator.generate_report()

    summary = {
        "experiment": os.path.basename(path).replace(".csv", ""),
        "avg_fps": report["fps"]["avg_fps"],
        "max_fps": report["fps"]["max_fps"],
        "avg_count": report["basic"]["avg_count"],
        "alert_activations": report["alerts"]["alert_activations"],
        "alert_ratio": report["alerts"]["alert_ratio"],
        "avg_count_change": report["stability"]["avg_count_change"],
        "max_count_jump": report["stability"]["max_count_jump"],
        "avg_slot_flip_rate": report["slot_stability"]["avg_slot_flip_rate"],
    }
    return summary

def compare(paths):
    summaries = [summarize(p) for p in paths]

    print("\n=========== EXPERIMENT COMPARISON ============\n")
    
    for s in summaries:
        flip = s["avg_slot_flip_rate"]
        flip_str = f"{flip:.6f}" if flip is not None else "N/A"
        print(f"Experiment: {s['experiment']}")
        print(f"Avg FPS: {s['avg_fps']:.2f}")
        print(f"Avg Count: {s['avg_count']:.2f}")
        print(f"Alert Activations: {s['alert_activations']}")
        print(f"Alert Ratio: {s['alert_ratio']:.3f}")
        print(f"Avg Count Change: {s['avg_count_change']:.3f}")
        print(f"Max Count Jump: {s['max_count_jump']}")
        print(f"Avg Slot Flip Rate: {flip_str}")

        print("-" * 40)

def main():
    experiments = [
        os.path.join("logs", f)
        for f in os.listdir("logs")
        if f.endswith(".csv")
    ]

    compare(experiments)

if __name__ == "__main__":
    main()