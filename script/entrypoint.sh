#!/bin/bash
set -e

echo Command is : "$1"
echo Minikube IP is : "$2"

echo "$2" > /tmp/minikube_ip.txt

case "$1" in
  install_dependencies)
    pyb "$1"
    ;;
  run_unit_tests)
    pyb "$1"
    ;;
  run_integration_tests)
    pyb "$1"
    ;;
  *)
    # The command is something like bash, not an pyb subcommand. Just run it in the right environment.
    exec "$@"
    ;;
esac