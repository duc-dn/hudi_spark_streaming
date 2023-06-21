from faker import Faker
from kafka import KafkaProducer
import json, time
import random
import string

parent = \
    [
        {
            "x": random.uniform(500, 1000),
            "y": random.uniform(500, 1000),
            "width": random.randint(50, 1000),
            "height": random.randint(50, 1000)
        }
    ]

views = ["/dashboard", "/view", "/staff", "/vnface"]

types = ["Desktop1920", "Desktop1366", "Ipad", "Smartphone", "Other"]

y = [None, random.randint(500, 1000)]

timestamp = [None, 1676687547526, 1677549864335]

topic_list = ['click_events62ea35fe235a31ea38e6aa78', 'click_events62fb48262306ead97264144b', 'click_events6361e5072306ead972692121',
         'click_events63bf6538d09feb313fad4a80']

heatmap_mobile_image = ["heatmap_mobile_images63dc729ad09feb313fae7a85", "heatmap_mobile_images63f86cfc4a5a3016008638bb"]

class Producer:
    def __init__(self, parent, views, types, y):
        self.parent = parent
        self.views = views
        self.types = types
        self.y = y

    def init_producer(self):
        producer = KafkaProducer(
            bootstrap_servers=['broker:9092'],
            value_serializer=self.json_serializer
        )
        return producer

    def generate_dummy_data(self, ux_click_id: int):
        data1 = {
            "collection": topic_list[random.randint(0, len(topic_list) - 1)],
            "query": "insert",
            "data": {
                "events": [
                {
                    "key": "[CLY]_action",
                    "count": 1,
                    "segmentation": {
                        "type": "click",
                        "x": random.randint(500, 1000),
                        "y": self.y[random.randint(0, 1)],
                        "width": random.randint(1500, 2000),
                        "height": random.randint(1000, 2000),
                        "view": self.views[random.randint(0, len(views) - 1)],
                        "parent": self.parent[0],
                        "domain": "console-vnface.vnpt.vn"
                    },
                    "timestamp": 34324235233,
                    "hour": random.randint(4, 20),
                    "dow": random.randint(1, 10)
                }
            ],
            "app_key": "5fa32bd8282b2fcdc247b68241faebffcd4ece04",
            "device_id": str(ux_click_id),
            "sdk_name": "javascript_native_web","sdk_version": "22.06.0",
            "t": 1,
            "timestamp": timestamp[random.randint(0, len(timestamp) - 1)],
            "hour": random.randint(4, 20),
            "dow": random.randint(1, 10),
            "raw_html": None,
            "screen_size_type": self.types[random.randint(0, len(types) - 1)],
            "_id": ux_click_id
            }
        }
        data2 = {
            "collection": heatmap_mobile_image[random.randint(0, len(heatmap_mobile_image) - 1)],
            "query": "insert",
            "data": {
                "device_id": "dd1848203bb80cab",
                "vc_class_name": "HistoryActivity",
                "screenX": 1080,
                "screenY": 2312,
                "device_os": "Android",
                "device_model_name": "Samsung SM-A528B",
                "screen_size": "Large",
                "timestamp": timestamp[random.randint(0, len(timestamp) - 1)],
                "file_path": "63dc729ad09feb313fae7a85/HistoryActivity_132.jpg",
                "bucket": "63dc729ad09feb313fae7a85",
                "_id": ux_click_id
            }                
        }
        data = [data1, data2]
        return data[random.randint(0, 1)]
    
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
            ux_click = self.generate_dummy_data(i)
            print("============================================================")
            print(ux_click)
            producer.send(topic=topic, value=ux_click)
            time.sleep(time_sleep)

if __name__ == '__main__':
    producer = Producer(parent, views, types, y)

    index = 0
    topic = "ux_data_exbe"
    time_sleep = 5
    producer.generate_ux_data(index, topic, time_sleep)