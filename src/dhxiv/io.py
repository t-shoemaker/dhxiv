import gzip
import json
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)


class JSONLWriter:
    """Write records to JSONL files in shards."""

    def __init__(self, output_dir, size=10_000, prefix="records"):
        """Initialize the writer.

        Parameters
        ----------
        output_dir : Path or str
            Directory to write shards
        size : int
            Number of records per shard
        prefix : str
            Prefix for shared filenames
        """
        self.output_dir = Path(output_dir)
        self.size = size
        self.prefix = prefix

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.shard_num = 1
        self.count_in_shard = 0
        self.current_filename = None
        self.current_file = None
        self._open_shard()

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.close()
        return False

    def _open_shard(self):
        """Open a new shard file."""
        self.current_filename = (
            self.output_dir / f"{self.prefix}_{self.shard_num:03d}.jsonl.gz"
        )
        self.current_file = gzip.open(self.current_filename, "wt")
        self.count_in_shard = 0
        LOGGER.info("Opened shard: %s", self.current_filename.name)

    def write(self, record):
        """Write a record to the current shard.

        Parameters
        ----------
        record : dict
            Record to write
        """
        self.current_file.write(json.dumps(record) + "\n")
        self.count_in_shard += 1

        if self.count_in_shard >= self.size:
            LOGGER.info(
                "Wrote %d records to %s; opening a new shard",
                self.count_in_shard,
                self.current_filename.name,
            )
            self.current_file.close()
            self.shard_num += 1
            self._open_shard()

    def close(self):
        """Close the current shard file."""
        if self.current_file:
            self.current_file.close()
