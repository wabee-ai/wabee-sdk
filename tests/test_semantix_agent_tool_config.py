import pytest
from langchain_community.llms.fake import FakeListLLM

from semantix_agent_tools.semantix_agent_tool_config import SemantixAgentToolConfig


class TestSemantixAgentToolConfig:
    def test_should_have_name_and_description_and_llm_as_default_attributes(
        self,
    ) -> None:
        fake_llm = FakeListLLM(responses=["any_response"])
        sut = SemantixAgentToolConfig(
            name="any_name", description="any_description", llm=fake_llm
        )

        assert sut.name == "any_name"
        assert sut.description == "any_description"
        assert sut.llm == fake_llm

    def test_should_check_if_llm_belongs_to_allowed_llms_by_langchain(self) -> None:
        class InvalidLLM: ...

        with pytest.raises(ValueError):
            SemantixAgentToolConfig(
                name="any_name", description="any_description", llm=InvalidLLM()
            )
