import configparser
config = configparser.ConfigParser()

# Add the structure to the file we will create
config.add_section('QUEUE')
config.set('QUEUE', 'queue_limit', '100')

# Write the new structure to the new file
with open("configfile.ini", 'w') as configfile:
    config.write(configfile)


