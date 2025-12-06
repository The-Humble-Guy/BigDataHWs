#!/bin/bash

# Start HDFS and YARN
$HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/sbin/start-yarn.sh

# Start Spark
$SPARK_HOME/sbin/start-history-server.sh

jps

#sudo $ZOOKEEPER_HOME/bin/zkServer.sh --config $ZOOKEEPER_HOME/conf start
#sudo $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
