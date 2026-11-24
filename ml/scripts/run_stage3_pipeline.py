"""CLI for the Stage 3 canonical data pipeline.

Usage:
    python ml/scripts/run_stage3_pipeline.py \
        --csv "<path to 600 news with valid hoax label.csv>" \
        --workbook "<path to 600 news labelling process.xlsx>" \
        --output-dir ml/data/processed
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from hoaxscope_ml.data.dedup import DedupConfig  # noqa: E402
from hoaxscope_ml.data.errors import Stage3Error  # noqa: E402
from hoaxscope_ml.data.split import SplitConfig  # noqa: E402
from hoaxscope_ml.pipeline import run_stage3_pipeline, write_reports  # noqa: E402
from hoaxscope_ml.preprocessing.text import PreprocessingConfig  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run HoaxScope Stage 3 data pipeline")
    parser.add_argument("--csv", required=True, help="Path to the approved CSV file")
    parser.add_argument("--workbook", help="Optional workbook for row-order URL audit")
    parser.add_argument(
        "--output-dir",
        default="ml/data/processed",
        help="Local ignored directory for report JSON files",
    )
    parser.add_argument("--seed", type=int, default=20261124)
    parser.add_argument("--shingle-size", type=int, default=5)
    parser.add_argument("--similarity-threshold", type=float, default=0.5)
    parser.add_argument("--min-length-ratio", type=float, default=0.2)
    parser.add_argument("--lowercase", action="store_true")
    parser.add_argument("--tokenize", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = run_stage3_pipeline(
            args.csv,
            workbook_path=args.workbook,
            dedup_config=DedupConfig(
                shingle_size=args.shingle_size,
                similarity_threshold=args.similarity_threshold,
                min_length_ratio=args.min_length_ratio,
            ),
            split_config=SplitConfig(seed=args.seed),
            preprocessing_config=PreprocessingConfig(
                lowercase=args.lowercase,
                tokenize=args.tokenize,
            ),
        )
        written = write_reports(result, args.output_dir)
    except Stage3Error as exc:
        print(f"Stage 3 stopped: {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(f"wrote {path.as_posix()}")

    validation = result.validation
    print(
        "validation: "
        f"passed={validation.passed} records={validation.record_count} "
        f"labels={validation.source_label_counts}"
    )
    if not result.passed:
        print(f"stopped at: {result.stopped_stage or 'unspecified'}")
        for issue in validation.issues:
            print(f"  {issue.code}: {issue.message}")
        return 1

    assert result.dedup is not None
    assert result.split is not None
    print(
        "dedup: "
        f"url_groups={result.dedup.url_duplicate_group_count} "
        f"near_pairs={result.dedup.near_duplicate_candidate_pairs} "
        f"conflict_records={result.dedup.conflict_record_count}"
    )
    print(
        "split: "
        f"records={result.split.record_counts_by_split} "
        f"leakage_checks="
        f"{sum(1 for check in result.split.leakage_checks if check.passed)}"
        f"/{len(result.split.leakage_checks)} passed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
