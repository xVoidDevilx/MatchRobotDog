#!/bin/bash

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -port|--port)
            PORT="$2"
            export PORT  # Export the PORT environment variable
            shift
            ;;
        *)
            echo "Unknown parameter passed: $1"
            exit 1
            ;;
    esac
    shift
done

# Run your Flask app with the specified port
python app.py --host 0.0.0.0 --port $PORT
