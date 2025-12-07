#!/bin/env python3

import asyncio
import json
import os
import sys

from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from kafka import KafkaProducer
import kafka.errors

# Fetch all messages from telegram channels
FETCH_ALL = False

# Telegram API credentials
API_ID = os.environ.get("APP_ID")
API_HASH = os.environ.get("API_HASH")

if not all([API_ID, API_HASH]):
    print("Error: API_ID or API_HASH environment variable is not set")
    sys.exit(1)

# Kafka configuration
KAFKA_HOST = "localhost"
KAFKA_PORT = "9092"
TOPIC_NAME = "telegram-messages"

# Note: Telegram channels from task are not available
CHANNELS = [
    "@bazabazon",
    "@bbcrussian",
    "@breakingmash",
    "@readovkanews",
    "@rian_ru",
    "@shot_shot",
    "@tass_agency",
    "https://t.me/DtRoad",
    "https://t.me/ENews112",
    "https://t.me/mashkomnata",
    "https://t.me/prohitec",
    "https://t.me/topor_novostnoy",
    "https://t.me/toporlive",
]


class KafkaCommunicator:
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def send(self, message):
        try:
            self.producer.send(self.topic, message.encode("utf-8"))
            self.producer.flush()
        except Exception as e:
            print(f"Kafka send error: {e}")

    def close(self):
        self.producer.close()


async def main():
    producer = KafkaProducer(bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}")
    communicator = KafkaCommunicator(producer, TOPIC_NAME)

    client = TelegramClient("telegram_kafka_session", API_ID, API_HASH)

    await client.start()

    entities = []

    for ch in CHANNELS:
        try:
            entity = await client.get_entity(ch)
            entities.append(entity)
            await client(JoinChannelRequest(entity))
            print(f"✅ Connected to channel: {entity.title}")
        except Exception as e:
            print(f"❌ Error connecting to channel {ch}: {e}")

    if FETCH_ALL:
        async def fetch_history():
            for ch in entities:
                print(f"⬇️ Loading history from {getattr(ch, 'title', ch)} ...")
                async for message in client.iter_messages(ch, reverse=True):
                    msg_data = {
                        "channel": getattr(ch, "title", "Unknown"),
                        "sender_id": getattr(message.sender_id, "id", None),
                        "message": message.text,
                        "date": str(message.date)
                    }
                    json_data = json.dumps(msg_data, ensure_ascii=False)
                    communicator.send(json_data)
                print(f"✅ History loaded for {getattr(ch, 'title', ch)}")

        await fetch_history()

    # Handle new messages
    # @client.on(events.NewMessage(chats=CHANNELS))
    @client.on(events.NewMessage(chats=entities))
    async def handler(event):
        try:
            msg = event.message.message
            sender = await event.get_sender()
            chat = await event.get_chat()
            msg_data = {
                "channel": getattr(chat, "title", "Unknown"),
                "sender_id": getattr(sender, "id", None),
                "message": msg,
                "date": str(event.message.date)
            }
            json_data = json.dumps(msg_data, ensure_ascii=False)
            communicator.send(json_data)
            print(f"📨 The message has been published to Kafka: {msg_data['channel']}")
        except Exception as e:
            print(f"Message processing error: {e}")

    print("🚀 Waiting messages from Telegram channels ...")
    try:
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        print("🛑 User session termination...")
    finally:
        for ch in CHANNELS:
            try:
                entity = await client.get_entity(ch)
                await client(LeaveChannelRequest(entity))
                print(f"🔌 Disconnected from channel: {entity.title}")
            except Exception:
                pass
        communicator.close()
        await client.disconnect()
        print("✅ Done.")


if __name__ == "__main__":
    asyncio.run(main())
