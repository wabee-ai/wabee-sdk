import pytest
from langchain_community.llms.fake import FakeListLLM

from wabee.tools.wabee_agent_tool_config import WabeeAgentToolConfig


class TestWabeeAgentToolConfig:
    def test_should_have_llm_as_default_attribute(
        self,
    ) -> None:
        fake_llm = FakeListLLM(responses=["any_response"])
        sut = WabeeAgentToolConfig(_llm=fake_llm)
        assert sut.llm == fake_llm

    def test_should_check_if_llm_belongs_to_allowed_llms_by_langchain(self) -> None:
        class InvalidLLM: ...

        with pytest.raises(ValueError):
            WabeeAgentToolConfig(_llm=InvalidLLM())
