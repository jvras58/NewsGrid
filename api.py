from fastapi import FastAPI
import pika
import json
import uuid

app = FastAPI()

def send_to_queue(queue_name, data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('user', 'password'))
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()

@app.post("/analyze")
async def request_analysis(topic: str):
    task_id = str(uuid.uuid4())
    payload = {"task_id": task_id, "topic": topic}
    
    send_to_queue('queue_research', payload)
    
    return {"status": "Processing initiated", "task_id": task_id}