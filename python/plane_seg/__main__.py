import numpy as np

from algorithm import DDPFF, PEAC, CAPE
from metrics import evaluate_metrics
from pathlib import Path

import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", type=str)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output", type=Path, default="labels")
    parser.add_argument(
        "--eval-metric",
        type=str,
        help="may be: {iou, dice, precision-iou, recall-iou, fScore-iou, mean-iou, mean-dice}",
    )
    parser.add_argument(
        "--eval-all-metrics", type=bool, default=False, help="True/False"
    )
    parser.add_argument(
        "--metrics-print-to-console",
        type=bool,
        default=True,
        help="True/False",
    )
    parser.add_argument("--metrics-output-to-file", type=Path)
    parser.add_argument("--ground-truth", type=Path)

    args = parser.parse_args(argv)

    if args.algorithm.startswith("peac"):
        algorithm = PEAC(args.algorithm, args.config, args.data)
    elif args.algorithm.startswith("ddpff"):
        algorithm = DDPFF(args.algorithm, args.config, args.data)
    elif args.algorithm.startswith("cape"):
        algorithm = CAPE(
            args.algorithm,
            args.config,
            args.data,
            calib_path=args.config,
        )
    else:
        raise ValueError("invalid algorithm specified:", args.algorithm)

    labels = algorithm.run()
    np.save(args.output, labels)

    # Evaluating metrics if needed
    if args.eval_metric is not None:
        evaluated_metric = evaluate_metrics(
            labels,
            args.ground_truth,
            args.eval_metric,
            args.metrics_print_to_console,
            args.metrics_output_to_file,
        )
    elif args.eval_all_metrics:
        evaluated_metrics = evaluate_metrics(
            labels,
            args.ground_truth,
            print_to_console=args.metrics_print_to_console,
            output_file=args.metrics_output_to_file,
        )


if __name__ == "__main__":
    main(sys.argv[1:])
