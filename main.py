import os
from pathlib import Path

from dotenv import load_dotenv

from stats.essence_stats import EssenceStats
from web.table_generator.html import generate_html_table

ENV_PATH = Path("./.env").resolve()
load_dotenv(dotenv_path=ENV_PATH)

KEYWORD_BLOCKLIST = [x.strip() for x in os.getenv("KEYWORD_BLOCKLIST").split(",")]
ESSENCE_DIR = os.getenv("ESSENCE_DIR")
CONJURE_DIR = os.getenv("CONJURE_DIR")
ESSENCE_EXAMPLES_REPO = os.getenv("ESSENCE_EXAMPLES_REPO")
CONJURE_BIN = Path(CONJURE_DIR) / "conjure"
TEMPLATE_DIR = Path("web/templates")

if __name__ == "__main__":
    stats = EssenceStats(
        ESSENCE_DIR,
        CONJURE_BIN,
        ESSENCE_EXAMPLES_REPO,
        blocklist=KEYWORD_BLOCKLIST,
    )
    table_html = generate_html_table(stats, TEMPLATE_DIR)

    path = Path("table.html")
    with path.open("w") as f:
        f.write(table_html)

    # test
