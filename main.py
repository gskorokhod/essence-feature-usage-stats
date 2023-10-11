import os
from pprint import pprint

from dotenv import load_dotenv

from stats.essence_stats import EssenceStats
from web.table_generator.html import generate_html_table

ENV_PATH = os.path.abspath('./.env')
load_dotenv(dotenv_path=ENV_PATH)

KEYWORD_BLOCKLIST = [x.strip() for x in os.getenv('KEYWORD_BLOCKLIST').split(',')]
#ESSENCE_DIR = os.getenv('ESSENCE_DIR')
ESSENCE_DIR = './test/EssenceCatalog'
CONJURE_DIR = os.getenv('CONJURE_DIR')
ESSENCE_EXAMPLES_REPO = os.getenv('ESSENCE_EXAMPLES_REPO')
CONJURE_BIN = os.path.join(CONJURE_DIR, 'conjure')
TEMPLATE_DIR = 'web/templates'

if __name__ == "__main__":
    stats = EssenceStats(ESSENCE_DIR, CONJURE_BIN, ESSENCE_EXAMPLES_REPO, blocklist=KEYWORD_BLOCKLIST)
    # pprint(stats.as_json())
    table_html = generate_html_table(stats, TEMPLATE_DIR)
    with open('table.html', 'w') as f:
        f.write(table_html)
