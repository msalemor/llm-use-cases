from autogen_core import DefaultTopicId, TopicId, TypeSubscription, default_subscription
from autogen_core import RoutedAgent, message_handler, type_subscription
from autogen_core import AgentId, MessageContext, RoutedAgent, SingleThreadedAgentRuntime, message_handler
from dataclasses import dataclass


@dataclass
class TextMessage:
    content: str
    source: str


@dataclass
class ImageMessage:
    url: str
    source: str


@dataclass
class Message:
    content: str


@type_subscription(topic_type="default")
class ReceivingAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: Message, ctx: MessageContext) -> None:
        print(f"Received a message: {message.content}")


class BroadcastingAgent(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: Message, ctx: MessageContext) -> None:
        await self.publish_message(
            Message("Publishing a message from broadcasting agent!"),
            topic_id=TopicId(type="default", source=self.id.key),
        )


async def main():
    runtime = SingleThreadedAgentRuntime()

    # Option 1: with type_subscription decorator
    # The type_subscription class decorator automatically adds a TypeSubscription to
    # the runtime when the agent is registered.
    await ReceivingAgent.register(runtime, "receiving_agent", lambda: ReceivingAgent("Receiving Agent"))

    # Option 2: with TypeSubscription
    await BroadcastingAgent.register(runtime, "broadcasting_agent", lambda: BroadcastingAgent("Broadcasting Agent"))
    await runtime.add_subscription(TypeSubscription(topic_type="default", agent_type="broadcasting_agent"))

    # Start the runtime and publish a message.
    runtime.start()
    await runtime.publish_message(
        Message("Hello, World! From the runtime!"), topic_id=TopicId(type="default", source="default")
    )
    await runtime.stop_when_idle()


@default_subscription
class BroadcastingAgentDefaultTopic(RoutedAgent):
    @message_handler
    async def on_my_message(self, message: Message, ctx: MessageContext) -> None:
        # Publish a message to all agents in the same namespace.
        await self.publish_message(
            Message("Publishing a message from broadcasting agent!"),
            topic_id=DefaultTopicId(),
        )


async def main_default_topic():
    runtime = SingleThreadedAgentRuntime()
    await BroadcastingAgentDefaultTopic.register(
        runtime, "broadcasting_agent", lambda: BroadcastingAgentDefaultTopic(
            "Broadcasting Agent")
    )
    await ReceivingAgent.register(runtime, "receiving_agent", lambda: ReceivingAgent("Receiving Agent"))
    runtime.start()
    await runtime.publish_message(Message("Hello, World! From the runtime!"), topic_id=DefaultTopicId())
    await runtime.stop_when_idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    asyncio.run(main_default_topic())
