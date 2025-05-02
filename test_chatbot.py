import pytest
from src.chatbot import get_response

def test_get_response():
    response = get_response("What is the forecast for next month?")
    assert isinstance(response, str)
    assert len(response) > 0
