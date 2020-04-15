import os
import json

def get_env_from_json():
  config_path = os.path.dirname(os.path.realpath(__file__)) + '/../../config.json'
  with open(config_path, 'r') as f:
      env = json.load(f)
      return env

env = get_env_from_json()
