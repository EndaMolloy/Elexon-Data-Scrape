from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os
ELEXON_API_KEY = os.getenv("ELEXON_API_KEY")
