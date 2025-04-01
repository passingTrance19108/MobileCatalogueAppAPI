import configparser
import os

def get_database_uri(config_file='config.properties'):
    # Check if DATABASE_URI is provided as an environment variable.
    env_db_uri = os.environ.get('DATABASE_URI')
    if env_db_uri:
        return env_db_uri

    # Fallback to reading from the properties file.
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['database']['uri']

# Example usage:
if __name__ == '__main__':
    db_uri = get_database_uri()
    print("Database URI:", db_uri)
