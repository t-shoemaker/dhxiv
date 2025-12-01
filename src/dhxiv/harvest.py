import logging

from sickle import Sickle

from .io import JSONLWriter
from .utils import get_date_range, format_record

LOGGER = logging.getLogger(__name__)
CONN = Sickle("https://oaipmh.arxiv.org/oai")


def harvest_records(
    output_dir, years=5, field="cs", size=10_000, prefix="records"
):
    """Harvest records from arXiv.

    Parameters
    ----------
    output_dir : Path or Str
        Output directory for JSONL shards
    years : int
        Years back to harvest
    field : str
        arXiv field identifier
    size : int
        Records per shard
    prefix : str
        Prefix for shard filenames
    """
    from_, until_ = get_date_range(years=years)
    params = {
        "metadataPrefix": "arXiv",
        "set": field,
        "from": from_,
        "until": until_,
    }

    LOGGER.info(
        "Harvesting arXiv paper records from %s. Dates: %s to %s",
        field,
        from_,
        until_,
    )

    count = 0
    errors = 0
    with JSONLWriter(output_dir, size, prefix) as writer:
        for record in CONN.ListRecords(**params):
            try:
                if not record.metadata:
                    LOGGER.debug("Skipping %s, no metadata", str(record))
                    continue

                paper = format_record(record.metadata)
                writer.write(paper)

                count += 1
                if count % 1_000 == 0:
                    LOGGER.info("Harvested %d records", count)

            except Exception as e:
                errors += 1
                LOGGER.warning(
                    "Error processing record %s: %s", str(record), e
                )

    LOGGER.info("Total records harvested: %d. Errors: %d", count, errors)
