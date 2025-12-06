#!/bin/bash
echo "==== Start Zookeeper ===="

if [ ! -f "$ZOOKEEPER_HOME/conf/zoo.cfg" ]; then
    echo "It seems that ZooKeeper config file is missing. Create from default"
    cp "$ZOOKEEPER_HOME/conf/zoo_sample.cfg" "$ZOOKEEPER_HOME/conf/zoo.cfg"
fi

if nc -z localhost 2181 2>/dev/null; then
    echo "ZooKeeper is already running on port 2181. Skipping start."
else
    echo "Starting ZooKeeper..."
    sudo "$ZOOKEEPER_HOME/bin/zkServer.sh" --config "$ZOOKEEPER_HOME/conf" start
    sleep 5
    if nc -z localhost 2181 2>/dev/null; then
        echo "ZooKeeper started successfully."
    else
        echo "Failed to start ZooKeeper."
        exit 1
    fi
fi

echo "==== Start Kafka ===="

if [ ! -f "$KAFKA_HOME/config/server.properties" ]; then
    echo "Kafka config is missing. Creating default configuration..."
    mkdir -p "$KAFKA_HOME/config"
    mkdir -p /tmp/kafka-logs

    cat > "$KAFKA_HOME/config/server.properties" << 'EOF'
broker.id=0
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
log.dirs=/tmp/kafka-logs
num.partitions=1
num.recovery.threads.per.data.dir=1
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000
zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=18000
group.initial.rebalance.delay.ms=0
EOF
fi

if nc -z localhost 9092 2>/dev/null; then
    echo "Kafka is already running on port 9092. Skipping start."
else
    echo "Starting Kafka..."
    sudo "$KAFKA_HOME/bin/kafka-server-start.sh" -daemon "$KAFKA_HOME/config/server.properties"
    sleep 5
    if nc -z localhost 9092 2>/dev/null; then
        echo "Kafka started successfully."
    else
        echo "Failed to start Kafka."
        exit 1
    fi
fi

echo "==== Create Kafka topic  ===="

if ! $KAFKA_HOME/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -q "^$KAFKA_TOPIC$"; then
  echo "Topic '$KAFKA_TOPIC' not found. Creating..."
  $KAFKA_HOME/bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic "$KAFKA_TOPIC" \
    --partitions 1 \
    --replication-factor 1
else
  echo "Topic '$KAFKA_TOPIC' already exists. Skipping creation."
fi
