import dj_database_url
from decouple import config

DATABASE = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}