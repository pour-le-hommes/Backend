import pytest
import os

@pytest.Function
def remove_docs():
    assert os.getenv("Show_Docs")==False