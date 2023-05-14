from pathlib import Path
import environ
from dropbox import Dropbox
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

dbx = Dropbox(env('DROPBOX_OAUTH2_TOKEN'))