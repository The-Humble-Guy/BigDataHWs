## Запуск окружения

### Добавляем переменные окружения:

```bash
source envs.sh
```

### Запускаем ZooKeeper и Kafka, создаем топик Kafka при необходимости:

```bash
bash bootstrap.sh
```

### Устанавливаем Python пакеты

```bash
pip install -r requirements.txt
```

### В трех отдельных терминалах сначала добавляем переменные окружения (см. выше), потом выполняем эти команды (по одной в каждом терминале):

```bash
bash run.sh console-consumer
bash run.sh spark-streamer
bash run.sh kafka-producer
```

## Примеры логов

### Логи bootstrap.sh

```bash
(my-conda-env) ubuntu@localhost:~/Documents/BigDataHWs/hw3$ bash bootstrap.sh 
==== Start Zookeeper ====
Starting ZooKeeper...
[sudo] password for ubuntu: 
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /home/ubuntu/BigData/zookeeper/conf/zoo.cfg
Starting zookeeper ... STARTED
ZooKeeper started successfully.
==== Start Kafka ====
Starting Kafka...
Kafka started successfully.
==== Create Kafka topic  ====
Topic 'telegram-messages' not found. Creating...
Created topic telegram-messages.
```

### Логи Kafka Producer

```bash
(my-conda-env) ubuntu@localhost:~/Documents/BigDataHWs/hw3$ ./run.sh spark-streamer
Output directory exists. Deleting...
Output directory is empty. Creating...
Ivy Default Cache set to: /home/ubuntu/.ivy2/cache
The jars for the packages stored in: /home/ubuntu/.ivy2/jars
:: loading settings :: url = jar:file:/home/ubuntu/BigData/spark/jars/ivy-2.4.0.jar!/org/apache/ivy/core/settings/ivysettings.xml
org.apache.spark#spark-streaming-kafka-0-8_2.11 added as a dependency
:: resolving dependencies :: org.apache.spark#spark-submit-parent-cc7862d7-e22a-43b0-b57b-8c28636d45dd;1.0

...

2025-12-07 10:46:35,424 INFO yarn.Client: Submitting application application_1765104260346_0001 to ResourceManager
2025-12-07 10:46:35,553 INFO impl.YarnClientImpl: Submitted application application_1765104260346_0001
2025-12-07 10:46:35,554 INFO cluster.SchedulerExtensionServices: Starting Yarn extension services with app application_1765104260346_0001 and attemptId None
2025-12-07 10:46:36,560 INFO yarn.Client: Application report for application_1765104260346_0001 (state: ACCEPTED)
2025-12-07 10:46:36,562 INFO yarn.Client: 
	 client token: N/A
	 diagnostics: AM container is launched, waiting for AM container to Register with RM
	 ApplicationMaster host: N/A
	 ApplicationMaster RPC port: -1
	 queue: dev
	 start time: 1765104395491
	 final status: UNDEFINED
	 tracking URL: http://localhost:8088/proxy/application_1765104260346_0001/
	 user: ubuntu
2025-12-07 10:46:37,565 INFO yarn.Client: Application report for application_1765104260346_0001 (state: ACCEPTED)
2025-12-07 10:46:38,567 INFO yarn.Client: Application report for application_1765104260346_0001 (state: ACCEPTED)
2025-12-07 10:46:39,197 INFO cluster.YarnClientSchedulerBackend: Add WebUI Filter. org.apache.hadoop.yarn.server.webproxy.amfilter.AmIpFilter, Map(PROXY_HOSTS -> localhost, PROXY_URI_BASES -> http://localhost:8088/proxy/application_1765104260346_0001), /proxy/application_1765104260346_0001
2025-12-07 10:46:39,276 INFO cluster.YarnSchedulerBackend$YarnSchedulerEndpoint: ApplicationMaster registered as NettyRpcEndpointRef(spark-client://YarnAM)
2025-12-07 10:46:39,571 INFO yarn.Client: Application report for application_1765104260346_0001 (state: RUNNING)
2025-12-07 10:46:39,571 INFO yarn.Client: 
	 client token: N/A
	 diagnostics: N/A
	 ApplicationMaster host: 192.168.122.130
	 ApplicationMaster RPC port: -1
	 queue: dev
	 start time: 1765104395491
	 final status: UNDEFINED
	 tracking URL: http://localhost:8088/proxy/application_1765104260346_0001/
	 user: ubuntu
2025-12-07 10:46:39,572 INFO cluster.YarnClientSchedulerBackend: Application application_1765104260346_0001 has started running.
2025-12-07 10:46:39,577 INFO util.Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 34493.
2025-12-07 10:46:39,577 INFO netty.NettyBlockTransferService: Server created on linux:34493
2025-12-07 10:46:39,578 INFO storage.BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
2025-12-07 10:46:39,588 INFO storage.BlockManagerMaster: Registering BlockManager BlockManagerId(driver, linux, 34493, None)
2025-12-07 10:46:39,594 INFO storage.BlockManagerMasterEndpoint: Registering block manager linux:34493 with 366.3 MB RAM, BlockManagerId(driver, linux, 34493, None)
2025-12-07 10:46:39,596 INFO storage.BlockManagerMaster: Registered BlockManager BlockManagerId(driver, linux, 34493, None)
2025-12-07 10:46:39,596 INFO storage.BlockManager: Initialized BlockManager: BlockManagerId(driver, linux, 34493, None)
2025-12-07 10:46:39,682 INFO ui.JettyUtils: Adding filter org.apache.hadoop.yarn.server.webproxy.amfilter.AmIpFilter to /metrics/json.
2025-12-07 10:46:39,687 INFO handler.ContextHandler: Started o.s.j.s.ServletContextHandler@a85350f{/metrics/json,null,AVAILABLE,@Spark}
2025-12-07 10:46:39,750 INFO scheduler.EventLoggingListener: Logging events to file:/home/ubuntu/BigData/tmp/spark/application_1765104260346_0001
2025-12-07 10:46:41,909 INFO cluster.YarnSchedulerBackend$YarnDriverEndpoint: Registered executor NettyRpcEndpointRef(spark-client://Executor) (192.168.122.130:55242) with ID 1
2025-12-07 10:46:41,996 INFO storage.BlockManagerMasterEndpoint: Registering block manager localhost:42269 with 93.3 MB RAM, BlockManagerId(1, localhost, 42269, None)
2025-12-07 10:46:43,688 INFO cluster.YarnSchedulerBackend$YarnDriverEndpoint: Registered executor NettyRpcEndpointRef(spark-client://Executor) (192.168.122.130:55262) with ID 2
2025-12-07 10:46:43,765 INFO cluster.YarnClientSchedulerBackend: SchedulerBackend is ready for scheduling beginning after reached minRegisteredResourcesRatio: 0.8
2025-12-07 10:46:43,783 INFO storage.BlockManagerMasterEndpoint: Registering block manager localhost:42795 with 93.3 MB RAM, BlockManagerId(2, localhost, 42795, None)
Saved 2025-12-07 10:50:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104600.txt
Saved 2025-12-07 10:51:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104660.txt
Saved 2025-12-07 10:52:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104720.txt
Saved 2025-12-07 10:53:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104780.txt
Saved 2025-12-07 10:54:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104840.txt
Saved 2025-12-07 10:55:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104900.txt
Saved 2025-12-07 10:56:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765104960.txt
Saved 2025-12-07 10:57:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765105020.txt
Saved 2025-12-07 10:58:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765105080.txt
Saved 2025-12-07 10:59:00: file:///home/ubuntu/Documents/BigDataHWs/hw3/output/result_1765105140.txt

...
```

### Логи Kafka Console Consumer
```bash
(my-conda-env) ubuntu@localhost:~/Documents/BigDataHWs/hw3$ ./run.sh console-consumer
{"channel": "ТАСС", "sender_id": 1050820672, "message": "▶️ Выброс солнечной плазмы от ночной вспышки дойдет до Земли в первой половине дня 9 декабря, сообщает лаборатория солнечной астрономии ИКИ РАН.\n\nВидео: Telegram-канал лаборатории солнечной астрономии ИКИ РАН", "date": "2025-12-07 10:49:01+00:00"}
...
```

### Логи Spark Streamer
```bash
(my-conda-env) ubuntu@localhost:~/Documents/BigDataHWs/hw3$ ./run.sh kafka-producer
✅ Connected to channel: Baza
✅ Connected to channel: BBC News | Русская служба
✅ Connected to channel: Mash
✅ Connected to channel: Readovka
✅ Connected to channel: РИА Новости
✅ Connected to channel: SHOT
✅ Connected to channel: ТАСС
✅ Connected to channel: Дептранс Москвы
✅ Connected to channel: 112
✅ Connected to channel: Mash Room
✅ Connected to channel: PRO Hi-Tech
✅ Connected to channel: Топор
✅ Connected to channel: Топор Live
🚀 Waiting messages from Telegram channels ...
📨 The message has been published to Kafka: ТАСС
📨 The message has been published to Kafka: Топор Live
...
```

## Результаты работы

```bash
 Top 10 proper names:
Москв, 6
Подписатьс, 5
Европ, 4
Топор, 4
Росс, 4
Герман, 3
Дептранс, 3
Майданов, 2
Ликсутов, 2
Президент, 2
```
