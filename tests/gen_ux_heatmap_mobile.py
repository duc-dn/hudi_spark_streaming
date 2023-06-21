from faker import Faker
from kafka import KafkaProducer
import json, time
import random
import string

device_os = ["IOS", "Android", "Windows", "Linux"]
timestamp = [1677635068577, 1676942837, 1677549864335]
class Producer:
    def __init__(self):
        pass 

    def init_producer(self):
        producer = KafkaProducer(
            bootstrap_servers=['broker:9092'],
            value_serializer=self.json_serializer
        )
        return producer

    def generate_dummy_data(self, id: int):
        return {
            "device_id": str(id),
            "vc_class_name": "HomepageViewController",
            "screenX": random.randint(500, 1000),
            "screenY": random.randint(500, 1000),
            "device_os": device_os[random.randint(0, len(device_os) - 1)],
            "device_model_name": "iPhone 13 Pro Max",
            "screen_size": "Small",
            "timestamp": timestamp[random.randint(0, len(timestamp) - 1)],
            "file_path": "63dc729ad09feb313fae7a85/image.jpg",
            "bucket": "63dc729ad09feb313fae7a85",
            "_id": str(id)
        }

    @staticmethod
    def id_generator(
            size=24, chars=string.ascii_lowercase + string.digits
    ):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def json_serializer(data):
        return json.dumps(data).encode('utf-8')

    def generate_ux_data(self, init_index: int, topic: str, time_sleep: int):
        producer = self.init_producer()
        i = init_index
        while True:
            i += 1
            data = self.generate_dummy_data(i)
            print("============================================================")
            print(data)
            producer.send(topic=topic, value=data)
            time.sleep(time_sleep)

if __name__ == '__main__':
    producer = Producer()

    index = 0
    topic = "ux_data_heatmap_mobile_images6360d6562306ead972691199"
    time_sleep = 1
    producer.generate_ux_data(index, topic, time_sleep)