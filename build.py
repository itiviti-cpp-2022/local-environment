#!/usr/bin/env python3
import os
import sys
from util import env, run_with_stdout, format_template_file, assert_dependencies


def preprocess():
  """Format the dockerfile with proper variables like local repository path and what-not.
  """
  format_template_file("app/Dockerfile", "app/Dockerfile.build", env.variables)


def postprocess():
  """Remove the temporary files we created during preprocessing or building
  """
  os.remove("app/Dockerfile.build")


def build_image():
  if run_with_stdout("docker image build . "
                     "--file app/Dockerfile.build --tag cpp-env:1.0") != 0:
    print("Docker build failed.")
    sys.exit(-1)


if __name__ == '__main__':
  # Make sure that our dependencies are satisfied
  assert_dependencies(env.dependencies)
  preprocess()
  build_image()
  postprocess()
