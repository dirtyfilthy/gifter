import os
from enum import Enum

class RunningMode(Enum):
	LOCAL      = 1
	PRODUCTION = 2


MODE = RunningMode.LOCAL
SECRET_KEY="ThisIsASecretKey!!!!"


# if the environment variable "RUNNING_MODE" is set to "PRODUCTION", we are in production mode
# otherwise, we use local mode. Local mode uses a local sqlite database for development

if os.environ.get("RUNNING_MODE", "LOCAL") == "PRODUCTION":
	MODE = RunningMode.PRODUCTION

DB_HOST = None
DB_NAME = None
DB_USER = None
DB_PASS = None

# if in production, get the relevant database connection information from environment variables so
# we don't need to hardcode them in the script

if MODE == RunningMode.PRODUCTION:
	DB_HOST = os.environ["DB_HOST"]
	DB_USER = os.environ["DB_USER"]
	DB_PASS = os.environ["DB_PASS"]
	DB_NAME = os.environ["DB_NAME"]
	SECRET_KEY = os.environ["SECRET_KEY"]


def is_production():
	''' return True if running in production mode '''
	return MODE == RunningMode.PRODUCTION




