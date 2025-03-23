from autogen_core import SingleThreadedAgentRuntime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from common import get_model_client


@dataclass
class MyMessageType:
    content: str


class MyAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("MyAgent")

    @message_handler
    async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
        print(f"{self.id.type} received message: {message.content}")


class MyAssistant(RoutedAgent):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._delegate = AssistantAgent(name, model_client=get_model_client())

    @message_handler
    async def handle_my_message_type(self, message: MyMessageType, ctx: MessageContext) -> None:
        print(f"{self.id.type} received message: {message.content}")
        response = await self._delegate.on_messages(
            [TextMessage(content=message.content, source="user")
             ], ctx.cancellation_token
        )
        print(f"{self.id.type} responded: {response.chat_message.content}")


async def main():
    # Create a runtime and register the agents
    runtime = SingleThreadedAgentRuntime()
    await MyAgent.register(runtime, "my_agent", lambda: MyAgent())
    await MyAssistant.register(runtime, "my_assistant", lambda: MyAssistant("my_assistant"))

    runtime.start()  # Start processing messages in the background.
    await runtime.send_message(MyMessageType("Hello, World!"), AgentId("my_agent", "default"))
    await runtime.send_message(MyMessageType("What is the speed of light?"), AgentId("my_assistant", "default"))
    # await runtime.stop()  # Stop processing messages in the background.
    await runtime.stop_when_idle()
    await runtime.close()  # Close the runtime when done.

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
