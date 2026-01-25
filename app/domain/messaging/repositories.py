from abc import ABC, abstractmethod


class IMessageBroker(ABC):
    @abstractmethod
    def send_to_queue(self, queue_name: str, data: dict) -> None:
        """Envia uma mensagem para a fila especificada."""
        pass
