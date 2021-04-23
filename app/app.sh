#!/bin/bash

cnt=1

check_file () {
  if [[ ! -f $1 ]]; then
    echo "[^] $1 file is missing, cannot continue"
    exit 1
  fi
}

# Create build files
run_cmake () {
  check_file "$REPO_PATH/CMakeLists.txt"
  mkdir "$1"
  cmake -S "$REPO_PATH" -B "$1" "${@:2}"
  status=$?
  if [[ ! $status -eq 0 ]]; then
    echo "[^] Error running cmake"
    exit 1
  fi
}

# Build after running cmake
run_make () {
  make -C "$1"
  status=$?
  if [[ ! $status -eq 0 ]]; then
    echo "[^] Error while building"
    exit 1
  fi
}

# Run unit tests after building
run_test () {
  cd "$1"
  "$1/test/runUnitTests"
  status=$?
  if [[ ! $status -eq 0 ]]; then
    echo "[^] Tests failed"
    exit 1
  fi
  cd "$OLDPWD"
}

build () {
  if [[ -z $REPO_PATH || ! -d $REPO_PATH ]]; then
    echo "Can't find repository, quitting"
    exit 1
  fi

  echo "[$cnt] Generating build files with cmake"
  run_cmake "$1" "${@:2}"
  echo "[+] Cmake success"
  (( cnt++ ))

  echo "[$cnt] Building with make"
  run_make "$1"
  echo "[+] Make success"
  (( cnt++ ))

  echo "[+] Successfully built the project!"
}

tests () {
  echo "[$cnt] Running normal tests"
  run_test /build
  echo "[+] Normal test success"
  (( cnt++ ))

  echo "[$cnt] Running tests with ASAN (Address Sanitizer)"
  build /build_asan -DCMAKE_BUILD_TYPE=ASAN
  run_test /build_asan
  echo "[+] ASAN test success"
  (( cnt++ ))

  echo "[$cnt] Running tests with USAN (Undefined Behaviour Sanitizer)"
  build /build_usan -DCMAKE_BUILD_TYPE=USAN
  run_test /build_usan
  echo "[+] USAN test success"
  (( cnt++ ))

  echo "[+] Test success! Woohoo! Go ahead and submit this badboi to github :)"
}

format () {
  if [[ -z $REPO_PATH || ! -d $REPO_PATH ]]; then
    echo "Can't find repository, quitting"
    exit 1
  fi

  # find matching files for clang-format
  file_list="$(find "$REPO_PATH" -regextype posix-extended -regex '.*\.(cpp|h)' -not -regex '.*(test|debug|cmake).*')"

  # format using specified clang-format settings (directory with .clang-format)
  cd "$1"
  if [[ "$2" == "grep" ]]; then
    clang-format "${@:3}" $file_list 1>/tmp/clang-format 2>&1
    status=$?
    cat /tmp/clang-format | grep -v "Formatting"
  else
    clang-format "${@:3}" $file_list
    status=$?
  fi
  cd "$OLDPWD"
  return $status
}

help () {
  cat << EOF
usage: $0 [action]
action:
  build - just try to run build and linter on the repo
  test - run the build action and then run tests as well
EOF
}

if [[ $# -lt 1 || $0 == "-h" || $0 == "--help" ]]; then
  help
fi

case $1 in
  build)
    build /build -DUSE_CLANG_TIDY=TRUE -DPATH_TO_ICA=/env/libica-plugin.so
    ;;

  test)
    build /build -DUSE_CLANG_TIDY=TRUE -DPATH_TO_ICA=/env/libica-plugin.so
    tests
    ;;

  check_format)
    format "${2:-$REPO_PATH}" grep --dry-run --Werror --verbose -i -style=file
    status=$?
    if [[ $status -eq 0 ]]; then
      echo "[+] Formatting is correct for all files!"
    else
      echo "[^] Wrong formatting in some files..."
    fi
    ;;

  format)
    format "${2:-$REPO_PATH}" nogrep --verbose -i -style=file
    ;;
  *)
    echo -ne "Invalid argument.\n\n"
    help
esac
