from stats.essence_stats import get_feature_stats
from web.table_generator.html_table_generator import generate_html_table
from dotenv import load_dotenv
import os


ENV_PATH = os.path.abspath('./.env')
load_dotenv(dotenv_path=ENV_PATH)

KEYWORD_BLOCKLIST = [x.strip() for x in os.getenv('KEYWORD_BLOCKLIST').split(',')]
ESSENCE_DIR = os.getenv('ESSENCE_DIR')
CONJURE_DIR = os.getenv('CONJURE_DIR')
CONJURE_BIN = os.path.join(CONJURE_DIR, 'conjure')


if __name__ == "__main__":
    html = generate_html_table(get_feature_stats(ESSENCE_DIR, CONJURE_BIN, path_depth=2, blocklist=KEYWORD_BLOCKLIST))
    with open('../../test.html', 'w') as f:
        f.write(str(html))
        f.close()
