"""
main.py — Kenya Smart Agriculture Full Pipeline
================================================
Runs the complete end-to-end pipeline in sequence.

Usage:
    python main.py              # Run full pipeline
    python main.py --step 1    # Run one step only

Steps:
    1 → Extract & validate raw data
    2 → Clean & engineer features
    3 → Merge master dataset
    4 → Train Model 1 (Food Security Classification)
    5 → Train Model 2 (Price Forecasting)
    6 → Train Model 3 (Recommendation System)
"""

import argparse
import sys
import os
import time

def run_step(step_num, step_name, module_path):
    print(f"\n{'█'*55}")
    print(f"  RUNNING STEP {step_num}: {step_name}")
    print(f"{'█'*55}")
    start = time.time()
    try:
        import importlib.util
        spec   = importlib.util.spec_from_file_location("step", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.main()
        elapsed = time.time() - start
        print(f"\n  ✅ Step {step_num} complete ({elapsed:.1f}s)")
        return True
    except Exception as e:
        print(f"\n  ❌ Step {step_num} failed: {e}")
        return False


STEPS = {
    1: ("Extract & Validate Data",     "scripts/extract_data.py"),
    2: ("Clean & Feature Engineering", "scripts/prepare_data.py"),
    3: ("Merge Master Dataset",        "scripts/merge_data.py"),
    4: ("Train Model 1 — IPC Classifier", "scripts/train_model1.py"),
    5: ("Train Model 2 — Price Forecast", "scripts/train_model2.py"),
    6: ("Train Model 3 — Recommendation","scripts/train_model3.py"),
}


def main():
    parser = argparse.ArgumentParser(description="Kenya Agriculture ML Pipeline")
    parser.add_argument("--step", type=int, choices=list(STEPS.keys()),
                        help="Run only one specific step")
    args = parser.parse_args()

    print("\n" + "█"*55)
    print("  KENYA SMART AGRICULTURE PLATFORM")
    print("  End-to-End ML Pipeline")
    print("█"*55)
    print("\n  Steps:")
    for num, (name, _) in STEPS.items():
        print(f"    {num}. {name}")

    results = {}

    if args.step:
        name, path = STEPS[args.step]
        results[args.step] = run_step(args.step, name, path)
    else:
        for num, (name, path) in STEPS.items():
            success = run_step(num, name, path)
            results[num] = success
            if not success:
                print(f"\n  ⚠️  Stopping at step {num}. Fix the error and re-run.")
                break

    # Summary
    print(f"\n{'═'*55}")
    print("  PIPELINE SUMMARY")
    print(f"{'═'*55}")
    for num, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status}  Step {num}: {STEPS[num][0]}")
    print(f"{'═'*55}\n")


if __name__ == "__main__":
    main()
