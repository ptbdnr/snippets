#!/bin/sh
# filepath: postman/newman/run.sh

# Run the Newman tests
newman run ../collections/sample_collection.json -e ../environments/sample_environment.json