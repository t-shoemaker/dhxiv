dhxiv
=====

Harvest arXiv paper metadata via OAI-PMH to survey DH contributions.

Usage
-----

1. Install [`pixi`][pixi] if you don't already have it. Don't want to use
   `pixi`? Just ensure you have [`sickle`][sickle] available in a Python
   environment

2. Install the environment with `pixi`

   ```sh
   pixi install
   ```

3. Run a fresh harvest

   ```sh
   pixi run python -m dhxiv -o <output_dir> -y 5 -f cs
   ```

**Harvest Options:**

| Flag           | Description                          | Default    |
|----------------|--------------------------------------|------------|
| `-o, --output` | Output directory for JSONL shards    | (required) |
| `-y, --years`  | Years back to harvest                | `5`        |
| `-f, --field`  | arXiv field: `cs`, `math`, or `stat` | `cs`       |
| `-s, --size`   | Records per shard                    | `10000`    |
| `-p, --prefix` | Prefix for shard filenames           | `records`  |

[pixi]: https://pixi.sh/latest
[sickle]: https://sickle.readthedocs.io/en/latest

Output Format
-------------

Paper records are written to JSONL files in shards. Each line is a JSON object
with the following schema:

```json
{
  "id": "arXiv ID",
  "title": "Paper title",
  "authors": ["Author One", "Author Two", "..."],
  "abstract": "Paper abstract",
  "categories": ["cs.AI", "cs.LG", "..."],
  "created": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD"
}
```

Shard files are named `{prefix}_{shard_num:03d}.jsonl.gz` (e.g.,
`records_001.jsonl.gz`, `records_002.jsonl.gz`).
