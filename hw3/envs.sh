#!/bin/bash

KAFKA_TOPIC="telegram-messages"
OUTPUT_DIR="${PWD}/output"
STOP_WORDS_FILE="$(realpath stop-words-russian.txt)"

export KAFKA_TOPIC
export OUTPUT_DIR
export STOP_WORDS_FILE

export APP_ID="<APP_ID>"
export API_HASH="<API_HASH>"
