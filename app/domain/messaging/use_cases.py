from app.domain.interfaces.IMessageBroker import IMessageBroker

from app.domain.exceptions import MessageSendError
from app.domain.messaging.entities import Message


class SendMessageUseCase:
    def __init__(self, message_broker: IMessageBroker):
        self.message_broker = message_broker

    def execute(self, message: Message) -> None:
        try:
            self.message_broker.send_to_queue(message.queue_name, message.data)
        except Exception as exc:
            raise MessageSendError(
                f"Erro ao enviar mensagem para {message.queue_name}: {str(exc)}"
            ) from exc
