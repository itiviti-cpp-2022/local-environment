import sys
from . import env, run_with_stdout, format_template, error


def run_docker(path, act, volumes=[]):
  return run_with_stdout(format_template(
      "docker run --volume={{path}}:{{container_repo_path}} " +
      "".join(["--volume=" + v + " " for v in volumes]) +
      "cpp-env:1.0 {{act}}",
      {{**env.variables, "act": act, "path": path}})) == 0