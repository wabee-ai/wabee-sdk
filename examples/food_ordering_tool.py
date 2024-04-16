from __future__ import annotations

import json
import logging
from asyncio import AbstractEventLoop, get_event_loop
from functools import partial
from typing import Any, Awaitable
from uuid import UUID

from semantix_agent_tools import (
    SemantixAgentTool,
    SemantixAgentToolConfig,
    SemantixAgentToolInput,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: \t  %(message)s")


class FoodOrderingToolConfig(SemantixAgentToolConfig):
    api_url: str
    api_token: str


class Item(SemantixAgentToolInput):
    product_id: UUID
    quantity: int


class FoodOrderingToolInput(SemantixAgentToolInput):
    customer_id: UUID
    restaurant_id: UUID
    items: list[Item]


def _create_tool(**kwargs: Any) -> SemantixAgentTool:
    return FoodOrderingTool.create(FoodOrderingToolConfig(**kwargs))


class HTTPClient:
    url: str
    headers: dict[str, Any]

    def __init__(self, url: str, headers: dict[str, Any]) -> None:
        self.url = url
        self.headers = headers

    def post(self, body: dict[str, Any]) -> dict[str, Any]:
        request = {
            "url": self.url,
            "headers": self.headers,
            "body": body,
            "method": "POST",
        }
        return {"status_code": 201, "response": {"body": body}, "request": request}


class FoodOrderingTool(SemantixAgentTool):
    http_client: HTTPClient

    def execute(self, query: str) -> str:
        food_ordering_tool_input = FoodOrderingToolInput.query_to_tool_input(query)
        http_client_response = self.http_client.post(
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

    async def execute_async(self, query: str) -> Awaitable[str]:
        async def run(
            *args: Any,
            loop: AbstractEventLoop | None = None,
            executor: Any = None,
            **kwargs: Any,
        ):
            if loop is None:
                loop = get_event_loop()
            pfunc = partial(self.execute, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)

        return await run(query)

    @classmethod
    def create(
        cls, food_ordering_tool_config: FoodOrderingToolConfig
    ) -> FoodOrderingTool:
        http_client = HTTPClient(
            url=food_ordering_tool_config.api_url,
            headers={"Authorization": f"Bearer {food_ordering_tool_config.api_token}"},
        )
        return cls(
            name=food_ordering_tool_config.name,
            description=food_ordering_tool_config.description,
            http_client=http_client,
        )


def main() -> None:
    food_ordering_tool_config = {
        "name": "food_ordering_tool",
        "description": "tool that orders food online",
        "api_url": "https://any-food-ordering-app/orders",
        "api_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImFueV9uYW1lIiwiaWF0IjoxNTE2MjM5MDIyfQ.eYA3Of5-3JqE-_kyhB74_hLt1K_htykH47dHoluJgic",
    }
    food_ordering_tool = _create_tool(**food_ordering_tool_config)
    logging.info(f"Creating FoodOrderingTool with config: {food_ordering_tool_config}")

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

    food_ordering_tool_output = food_ordering_tool._run(food_ordering_tool_query)
    logging.info(f"FoodOrderingTool returned output: {food_ordering_tool_output}")

    logging.info(f"Calling FoodOrderingTool with query: {food_ordering_tool_query}")

    food_ordering_tool_output = food_ordering_tool._run(food_ordering_tool_query)
    logging.info(f"FoodOrderingTool returned output: {food_ordering_tool_output}")
