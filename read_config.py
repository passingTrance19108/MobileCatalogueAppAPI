import configparser

def get_database_uri(config_file='config.properties'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['database']['uri']

# Example usage:
if __name__ == '__main__':
    db_uri = get_database_uri()
    print("Database URI:", db_uri)
