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

