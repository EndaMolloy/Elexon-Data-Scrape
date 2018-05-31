from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
ELEXON_API_KEY = os.getenv("ELEXON_API_KEY")
DB_CONN_STRING = os.getenv("DB_CONN_STRING")
