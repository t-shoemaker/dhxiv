from datetime import datetime, timedelta


def _get_first(metadata, key, default=None):
    """Safely get the first element from a metadata list.

    Parameters
    ----------
    metadata : dict
        Metadata dictionary
    key : str
        Key to retrieve
    default : any, optional
        Default value if key is missing or empty, by default None

    Returns
    -------
    any
        First element of the list at metadata[key], or default if not found
    """
    values = metadata.get(key, [])
    return values[0] if values else default


def get_date_range(years=5):
    """Get range of dates from now to `year` back.

    Parameters
    ----------
    years : int
        Number of years back to scrape

    Returns
    -------
    tuple[str, str]
        Date range 'from' to 'until'

    Raises
    ------
    ValueError
        If years is not positive
    """
    if years <= 0:
        raise ValueError(f"Years must be positive, got {years}")

    until_ = datetime.now()
    from_ = until_ - timedelta(days=years * 365)

    return from_.strftime("%Y-%m-%d"), until_.strftime("%Y-%m-%d")


def parse_authors(metadata):
    """Parse author lists from metadata.

    Parameters
    ----------
    metadata : dict
        Record metadata

    Returns
    -------
    list[str]
        List of author names
    """
    keynames = metadata.get("keyname", [])
    forenames = metadata.get("forenames", [])

    if not keynames:
        return []

    authors = []
    for i, keyname in enumerate(keynames):
        forename = forenames[i] if i < len(forenames) else ""
        if forename:
            authors.append(f"{forename} {keyname}")
        else:
            authors.append(keyname)

    return authors


def format_record(metadata):
    """Format a record into a dictionary.

    Parameters
    ----------
    metadata : dict
        Record metadata

    Returns
    -------
    dict
        Formatted record with keys: id, title, authors, abstract, categories,
        created, updated
    """
    return {
        "id": _get_first(metadata, "id"),
        "title": _get_first(metadata, "title"),
        "authors": parse_authors(metadata),
        "abstract": _get_first(metadata, "abstract"),
        "categories": metadata.get("categories", []),
        "created": _get_first(metadata, "created"),
        "updated": _get_first(metadata, "updated"),
    }
