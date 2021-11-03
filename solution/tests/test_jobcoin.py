#!/usr/bin/env python
from click.testing import CliRunner
from solution import cli
from unittest.mock import patch
import pytest
import re


@pytest.fixture
def response():
    import requests
    return requests.get('https://jobcoin.gemini.com/')

def test_content(response):
    assert 'Hello!' in str(response.content)


def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(cli.main, input=' \n y')
    assert not result.exception
    assert result.exit_code == 0
    assert 'Welcome to the Jobcoin mixer' in result.output
    

def test_cli_creates_address():
    runner = CliRunner()
    result = runner.invoke(cli.main, input='1234,4321 \n\ny')
    assert not result.exception
    address_create_output = result.output
    print(address_create_output)
    output_re = re.compile(
        r'You may now send Jobcoins to address [0-9a-zA-Z]{32}. '
        'They will be mixed and sent to your destination addresses.'
    )
    assert output_re.search(address_create_output) is not None
