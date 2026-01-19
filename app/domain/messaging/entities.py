from dataclasses import dataclass


@dataclass
class Message:
    queue_name: str
    data: dict
    message_id: str = None

    def to_dict(self) -> dict:
        return {
            "queue_name": self.queue_name,
            "data": self.data,
            "message_id": self.message_id,
        }
