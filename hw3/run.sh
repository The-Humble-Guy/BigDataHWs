#!/bin/bash

PROGRAM="${0##*/}"
COMMAND="$1"

cmd_console_consumer() {
    $KAFKA_HOME/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic $KAFKA_TOPIC --from-beginning
}

cmd_console_producer() {
    $KAFKA_HOME/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic $KAFKA_TOPIC
}

cmd_kafka_producer() {
    python telegram_kafka_producer.py
}

cmd_spark_streamer() {
    if [[ -z "$OUTPUT_DIR" ]]; then
        echo "Error: OUTPUT_DIR is not set"
        exit 1
    fi

    if [[ -d "${OUTPUT_DIR}" ]]; then
        echo "Output directory exists. Deleting..."
        rm -rf "${OUTPUT_DIR}"
    fi

    echo "Output directory is empty. Creating..."
    mkdir -p "${OUTPUT_DIR}"
    spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 spark_streaming_kafka_telegram.py
}

cmd_help() {
    cat << EOF
Supported commands:
    kafka-producer: run Kafka producer
    console-consumer: run simple Kafka consumer inside terminal session
    console-producer: run simple Kafka producer inside terminale session
    spark-streamer: run Spark application with Kafka consumer
EOF
}

if [[ -z "$KAFKA_TOPIC" ]]; then
    echo "Error: KAFKA_TOPIC is not set"
    exit 1
fi

case "$COMMAND" in
    kafka-producer)   shift; cmd_kafka_producer "$@" ;;
    console-consumer) shift; cmd_console_consumer "$@" ;;
    console-producer) shift; cmd_console_producer "$@" ;;
    spark-streamer)   shift; cmd_spark_streamer "$@" ;;
    help|*)           shift; cmd_help "$@" ;;
esac

exit 0
