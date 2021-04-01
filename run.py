#!/usr/bin/env python3
import argparse
import os
import sys
from util import env, run_with_stdout, format_template, assert_requirements


def init_argparser():
  parser = argparse.ArgumentParser(
    description="Compile + test your project before submitting it to github.\n"
                "Before running this, make sure you ran build.py in order to "
                "create the required docker container.",
    epilog="By @renbou with <3",
    formatter_class=argparse.RawTextHelpFormatter
  )
  parser.add_argument("repo", help="Path to repository containing the project")
  parser.add_argument("-b", "--build", help="Run only build, without actually"
                                            " testing the project",
                      dest="only_build", action="store_true")
  return parser


def run_image(args):
  """Run docker container with local repository path
  mapped to the actual container path.
  """
  path = os.path.realpath(args.repo)
  if not os.path.exists(path):
    print("Specified repository path doesn't exist.")
    sys.exit(1)

  action = "build" if args.only_build else "test"

  if run_with_stdout(format_template(
    "docker run --volume={{path}}:{{container_repo_path}} cpp-env:1.0 {{act}}",
      {**env.variables, "path": path, "act": action})) != 0:
    print("Running failed :(")


if __name__ == '__main__':
  assert_requirements(env.requirements)
  parser = init_argparser()
  run_image(parser.parse_args())
