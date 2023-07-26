#!/bin/sh

command_to_execute="make update-mirrors-without-backup"

while true; do
    $command_to_execute
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "Command exited successfully."
        break
    else
        echo "Command exited with a non-zero exit code. Retrying..."
        sleep 1
    fi
done
