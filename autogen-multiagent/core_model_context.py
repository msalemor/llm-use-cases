from dataclasses import dataclass

from autogen_core import AgentId, MessageContext, RoutedAgent, SingleThreadedAgentRuntime, message_handler
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import AssistantMessage, ChatCompletionClient, SystemMessage, UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from common import get_model_client


@dataclass
class Message:
    content: str


class SimpleAgentWithContext(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A simple agent")
        self._system_messages = [SystemMessage(
            content="You are a helpful AI assistant.")]
        self._model_client = model_client
        self._model_context = BufferedChatCompletionContext(buffer_size=5)

    @message_handler
    async def handle_user_message(self, message: Message, ctx: MessageContext) -> Message:
        # Prepare input to the chat completion model.
        user_message = UserMessage(content=message.content, source="user")
        # Add message to model context.
        await self._model_context.add_message(user_message)
        # Generate a response.
        response = await self._model_client.create(
            self._system_messages + (await self._model_context.get_messages()),
            cancellation_token=ctx.cancellation_token,
        )
        # Return with the model's response.
        assert isinstance(response.content, str)
        # Add message to model context.
        await self._model_context.add_message(AssistantMessage(content=response.content, source=self.metadata["type"]))
        return Message(content=response.content)


async def main():
    runtime = SingleThreadedAgentRuntime()
    await SimpleAgentWithContext.register(
        runtime,
        "simple_agent_context",
        lambda: SimpleAgentWithContext(
            model_client=get_model_client()
        ),
    )
    # Start the runtime processing messages.
    runtime.start()
    agent_id = AgentId("simple_agent_context", "default")

    # First question.
    message = Message("Hello, what are some fun things to do in Seattle?")
    print(f"Question: {message.content}")
    response = await runtime.send_message(message, agent_id)
    print(f"Response: {response.content}")
    print("-----")

    # Second question.
    message = Message("What was the first thing you mentioned?")
    print(f"Question: {message.content}")
    response = await runtime.send_message(message, agent_id)
    print(f"Response: {response.content}")

    # Stop the runtime processing messages.
    await runtime.stop()
    await runtime.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
