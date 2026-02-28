from src.evaluation import ShelfEvaluator

def main():
    evaluator = ShelfEvaluator("logs/shelf_events.csv")

    report = evaluator.generate_report()

    print("\n======= SHELF SYSTEM EVALUATION =======\n")

    for section, metrics in report.items():
        print(f"[{section.upper()}]")
        for k, v in metrics.items():
            print(f"{k:25}: {v}")
        print()

if __name__ == "__main__":
    main()
