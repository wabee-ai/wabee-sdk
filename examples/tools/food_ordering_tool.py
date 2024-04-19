from __future__ import annotations

import json
import logging
from asyncio import AbstractEventLoop, get_event_loop, run
from functools import partial
from typing import Any, Awaitable, Type
from uuid import UUID

from langchain_community.llms.fake import FakeListLLM

from semantix_agents.tools import (
    SemantixAgentTool,
    SemantixAgentToolConfig,
    SemantixAgentToolInput,
    SemantixAgentToolInputField,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: \t  %(message)s")


class FoodOrderingToolConfig(SemantixAgentToolConfig):
    api_url: str
    api_token: str


class Item(SemantixAgentToolInput):
    product_id: UUID = SemantixAgentToolInputField(
        name="product_id",
        description="product unique identifier",
        example="0f09c33f-51d1-46df-91dd-dd7c2ba89a20",
    )
    quantity: int = SemantixAgentToolInputField(
        name="quantity", description="product quantity", example=4
    )


class FoodOrderingToolInput(SemantixAgentToolInput):
    customer_id: UUID = SemantixAgentToolInputField(
        name="customer_id",
        description="customer unique identifier",
        example="47b30ed0-d4cc-436c-a21b-08a9115e9373",
    )
    restaurant_id: UUID = SemantixAgentToolInputField(
        name="restaurant_id",
        description="restaurant unique identifier",
        example="bdeffffd-c6e6-4ff7-acf9-5cc7b1ba8f34",
    )
    items: list[Item] = SemantixAgentToolInputField(
        name="items",
        description="order items",
        example=[Item.props()],
    )


def _create_tool(**kwargs: Any) -> SemantixAgentTool:
    return FoodOrderingTool.create(FoodOrderingToolConfig(**kwargs))


class HTTPClient:
    url: str
    headers: dict[str, Any]

    def __init__(self, url: str, headers: dict[str, Any]) -> None:
        self.url = url
        self.headers = headers

    async def post(self, body: dict[str, Any]) -> Awaitable[dict[str, Any]]:
        async def run_as_async(
            *args: Any,
            loop: AbstractEventLoop | None = None,
            executor: Any = None,
            **kwargs: Any,
        ):
            if loop is None:
                loop = get_event_loop()
            pfunc = partial(
                lambda: {"status_code": 201, "message": "created"}, *args, **kwargs
            )
            return await loop.run_in_executor(executor, pfunc)

        return await run_as_async()


class FoodOrderingTool(SemantixAgentTool):
    args_schema: Type[SemantixAgentToolInput] = FoodOrderingToolInput
    http_client: HTTPClient

    async def execute_async(
        self, food_ordering_tool_input: FoodOrderingToolInput
    ) -> Awaitable[str]:
        http_client_response = await self.http_client.post(
            {
                "customer_id": food_ordering_tool_input.customer_id,
                "restaurant_id": food_ordering_tool_input.restaurant_id,
                "items": [
                    {"product_id": item.product_id, "quantity": item.quantity}
                    for item in food_ordering_tool_input.items
                ],
            }
        )
        return str(http_client_response["status_code"])

    @classmethod
    def create(
        cls, food_ordering_tool_config: FoodOrderingToolConfig
    ) -> FoodOrderingTool:
        http_client = HTTPClient(
            url=food_ordering_tool_config.api_url,
            headers={"Authorization": f"Bearer {food_ordering_tool_config.api_token}"},
        )
        return cls(
            name="food_ordering_tool",
            description="tool that orders food online",
            llm=food_ordering_tool_config.llm,
            http_client=http_client,
        )


def main() -> None:
    food_ordering_tool_config = {
        "api_url": "https://any-food-ordering-app/orders",
        "api_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImFueV9uYW1lIiwiaWF0IjoxNTE2MjM5MDIyfQ.eYA3Of5-3JqE-_kyhB74_hLt1K_htykH47dHoluJgic",
        "_llm": FakeListLLM(responses=["any_response"]),
    }
    food_ordering_tool = _create_tool(**food_ordering_tool_config)
    logging.info(f"Creating FoodOrderingTool with config: {food_ordering_tool_config}")

    logging.info("Displaying tool information:")
    print(f"name: {food_ordering_tool.name}")
    print(f"description: {food_ordering_tool.description}")
    print(f"args: {food_ordering_tool.args}")

    food_ordering_tool_query = json.dumps(
        {
            "customer_id": "47b30ed0-d4cc-436c-a21b-08a9115e9373",
            "restaurant_id": "bdeffffd-c6e6-4ff7-acf9-5cc7b1ba8f34",
            "items": [
                {"product_id": "0f09c33f-51d1-46df-91dd-dd7c2ba89a20", "quantity": 1},
                {"product_id": "26440bb5-5a79-4be4-a5b2-22c277d1ecaf", "quantity": 2},
            ],
        }
    )
    logging.info(f"Calling FoodOrderingTool with query: {food_ordering_tool_query}")

    food_ordering_tool_output = run(food_ordering_tool.arun(food_ordering_tool_query))
    logging.info(f"FoodOrderingTool returned output: {food_ordering_tool_output}")
