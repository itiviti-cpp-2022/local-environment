#!/usr/bin/env python3
import argparse
import os
import sys
from util import env, run_with_stdout, format_template, check_file_update


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
  parser.add_argument("-s", "--send", help="Test the project and "
                                           " format+push on success",
                      dest="send", action="store_true")
  parser.add_argument("-cf", "--clang-format", help="Path to your own"
                                                    " clang-format file, which will be used to reformat"
                                                    " the code back to your style after sending.",
                      dest="clang_format")
  return parser


def exec_docker(args, volumes=[]):
  if run_with_stdout(format_template(
      "docker run --volume={{path}}:{{container_repo_path}} " +
      "".join(["--volume=" + v + " " for v in volumes]) +
      "cpp-env:1.0 {{act}}",
      args)) != 0:
    print("Running failed :(")
    sys.exit(1)


def run_image(args):
  """Run docker container with local repository path
  mapped to the actual container path.
  """
  path = os.path.realpath(args.repo)
  if not os.path.exists(path):
    print("Specified repository path doesn't exist.")
    sys.exit(1)

  action = "build" if args.only_build else "test"
  exec_docker({**env.variables, "path": path, "act": action})

  # after running the docker container check if we need to do anything else
  if args.send:
    print("Formatting to remote clang-format")
    exec_docker({**env.variables, "path": path, "act": "format"})

    # temporarily switch to repo
    oldpwd = os.getcwd()
    os.chdir(path)
    print("Committing formatted changes to repo")
    run_with_stdout("git add .")
    run_with_stdout("git commit -m \"(local-env) test and format\"")
    run_with_stdout("git push")
    os.chdir(oldpwd)

    if args.clang_format:
      clang_format_path = os.path.realpath(args.clang_format)
      if not os.path.exists(clang_format_path):
        print("Specified personal clang-format file doesn't exist.")
        sys.exit(1)
      print("Formatting to local clang-format using " + clang_format_path)
      exec_docker({**env.variables, "path": path,
                   "act": "format /format"},
                  [clang_format_path + ":/format/.clang-format"])


if __name__ == '__main__':
  # Check if newer dependencies are available
  for dep in env.dependencies:
    if check_file_update(dep["repo"], dep["path"]):
      print("Update available for dependency {}. Please run build.py."
            .format(os.path.basename(dep["path"])))
      sys.exit(0)
  parser = init_argparser()
  run_image(parser.parse_args())
