"""Exceptions raised by the Stage 3 data pipeline."""


class Stage3Error(Exception):
    """Base class for Stage 3 pipeline errors."""


class DatasetValidationError(Stage3Error):
    """Raised when the source dataset fails a blocking validation check."""


class SplitImpossibleError(Stage3Error):
    """Raised when a leakage-free group-aware split cannot be produced."""
