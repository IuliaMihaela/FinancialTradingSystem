import configparser
config = configparser.ConfigParser()

# Add the structure to the file we will create
config.add_section('queue')
config.set('queue', 'queue_limit', '100')

# Write the new structure to the new file
with open(r"/MessageQueuesService/configfile.ini", 'w') as configfile:
    config.write(configfile)