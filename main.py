import os

from dotenv import load_dotenv

ENV_PATH = os.path.abspath('./.env')
load_dotenv(dotenv_path=ENV_PATH)

KEYWORD_BLOCKLIST = [x.strip() for x in os.getenv('KEYWORD_BLOCKLIST').split(',')]
#ESSENCE_DIR = os.getenv('ESSENCE_DIR')
ESSENCE_DIR = './test/EssenceCatalog'
CONJURE_DIR = os.getenv('CONJURE_DIR')
CONJURE_BIN = os.path.join(CONJURE_DIR, 'conjure')

if __name__ == "__main__":
    stats = get_essence_stats