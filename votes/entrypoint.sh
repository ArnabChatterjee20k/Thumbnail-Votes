#!/bin/bash

python consumer.py &

# Execute the command passed to the script
exec "$@"