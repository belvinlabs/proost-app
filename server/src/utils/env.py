import os


def is_local():
  return os.getenv('GAE_APPLICATION') is None
