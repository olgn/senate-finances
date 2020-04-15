from utils import env

# set the instagram url and ensure it exists
SENATE_EFD_URL = env.get('SENATE_EFD_URL')
if SENATE_EFD_URL is None:
    print('You must supply the Senate EFD url in the config file. Exiting')
    exit