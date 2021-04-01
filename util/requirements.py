import importlib.util
import subprocess
import sys

def check(requirements):
  """
  Check that all the requirements are installed
  :param requirements: list of required modules as strings
  :return -1 on failure, 0 on success (all modules are present)
  """
  for r in requirements:
    spec = importlib.util.find_spec(r)
    if spec is None:
      return -1
  return 0


def install(requirements):
  """
  Run pip with current python executable and install the requirements
  :param requirements: list of required libraries as strings
  :return -1 on failure, 0 on success
  """
  for r in requirements:
    try:
      subprocess.check_call([sys.executable, "-m", "pip", "install", r])
    except subprocess.CalledProcessError as e:
      print("Error installing requirement {}: {}".format(r, e))
      return -1
  return 0


def assert_requirements(requirements):
  """
  Check if requirements are present and install if needed. On fail kills the script.
  :param requirements: list of required libraries as strings
  """
  if check(requirements) != 0 and install(requirements) != 0:
    print("Requirements aren't present and unable to install them. Quitting.")
    sys.exit(-1)