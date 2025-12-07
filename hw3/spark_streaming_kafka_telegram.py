import json
import os
import re
import sys
import time

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# Spark settings
SPARK_APP_NAME = "ProperNounsKafkaTelegram"
SPARK_CHECKPOINT_DIR="checkpoint_telegram"
SPARK_LOG_LEVEL = "ERROR"
SPARK_BATCH_INTERVAL = 60       # 1 min
WINDOW_LENGTH = 30 * 60         # 30 min
SLIDE_INTERVAL = 60             # window size in seconds

OUTPUT_DIR = os.environ.get("OUTPUT_DIR")
if not OUTPUT_DIR:
    print("Error: environment variable OUTPUT_DIR is not set")
    sys.exit(1)

OUTPUT_DIR = f"file://{OUTPUT_DIR}"

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")
if not KAFKA_TOPIC:
    print("Error: environment variable KAFKA_TOPIC is not set")
    sys.exit(1)


# Regex for extracting proper names
proper_noun_pattern = re.compile(r"\b[А-ЯЁ][а-яё]+\b")

# Regex for removing vowels and the letter 'й' at the end of a word
vowels_remove_pattern = re.compile(r"[аеёиоуыэюяй]+$", re.IGNORECASE)

# Stop words 
STOP_WORDS_FILE = os.environ.get("STOP_WORDS_FILE")

if STOP_WORDS_FILE:
    with open(STOP_WORDS_FILE, "r", encoding="utf-8") as file:
        stop_words = { line.strip() for line in file if line.strip()  }


latest_top10 = []

def clean_and_filter(message):
    try:
        parsed = json.loads(message)
        text = parsed.get("message", "")
        # For debug
        # text = message
    except json.JSONDecodeError:
        return []

    if not text:
        return []

    candidates = proper_noun_pattern.findall(text)
    result = []
    for w in candidates:
        if w.lower() in stop_words:
            continue
        w = vowels_remove_pattern.sub("", w)
        result.append(w)
    return result

def process_rdd(time_stamp, rdd):
    global latest_top10
    if not rdd.isEmpty():
        sorted_rdd = rdd.sortBy(lambda x: -x[1])
        ts = int(time_stamp.timestamp())
        path = f"{OUTPUT_DIR}/result_{ts}.txt"
        lines = sorted_rdd.map(lambda x: f"{x[0]}, {x[1]}")
        lines.saveAsTextFile(path)
        # save top 10 words in Spark driver 
        latest_top10 = sorted_rdd.take(10)
        print(f"Saved {time_stamp}: {path}")

def main():
    sc = SparkContext(appName=SPARK_APP_NAME)
    sc.setLogLevel(SPARK_LOG_LEVEL)
    ssc = StreamingContext(sc, SPARK_BATCH_INTERVAL)
    ssc.checkpoint(SPARK_CHECKPOINT_DIR)

    kafka_stream = KafkaUtils.createDirectStream(
        ssc,
        topics=[KAFKA_TOPIC],
        kafkaParams={"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
    ).map(lambda x: x[1])

    words = kafka_stream.flatMap(clean_and_filter).map(lambda w: (w, 1))

    windowed_counts = words.reduceByKeyAndWindow(
        lambda a, b: a + b,
        lambda a, b: a - b,
        WINDOW_LENGTH,
        SLIDE_INTERVAL
    )

    # Save results every minute
    windowed_counts.foreachRDD(process_rdd)

    # Start with timeout
    ssc.start()
    ssc.awaitTerminationOrTimeout(WINDOW_LENGTH + 60)

    # Print results
    if latest_top10:
        print("\n Top 10 proper names:")
        for w, c in latest_top10:
            print(f"{w}, {c}")

    ssc.stop(stopSparkContext=True, stopGraceFully=True)

if __name__ == "__main__":
    main()

