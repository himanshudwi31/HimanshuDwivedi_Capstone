from unittest.mock import AsyncMock, patch
import pytest

from src.pipeline.fake_llm import Question, Answer, FakeLLMError

@pytest.mark.asyncio
async def test_ask_llm_calls_fake_once():

    fake_answer = Answer(
        question="What is RAG?",
        text="Mocked answer.",
        cost_usd=0.0001,
        retries=0,
    )

    with patch(
        "src.pipeline.pipeline.fake_ask_llm",
        AsyncMock(return_value=fake_answer),
    ) as m:
        from src.pipeline.pipeline import ask_llm
        result = await ask_llm(Question(text="What is RAG?"))

    assert m.call_count == 1
    assert result.text == "Mocked answer."


@pytest.mark.asyncio
async def test_retry_three_times_on_failure():
    with patch(
        "src.pipeline.pipeline.fake_ask_llm",
        AsyncMock(side_effect=FakeLLMError("simulated")),
    ) as m_call, patch(
        "src.pipeline.pipeline.asyncio.sleep",
        AsyncMock(),
    ):
        from src.pipeline.pipeline import ask_llm_with_retry
        with pytest.raises(FakeLLMError):
            await ask_llm_with_retry(Question(text="What is RAG?"), tries=3)

    assert m_call.call_count == 3
