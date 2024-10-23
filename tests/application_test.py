import os
import pytest
from pathlib import Path
import json
import time

from application import application

@pytest.fixture
def client():
    with application.app_context():
        yield application.test_client()  # tests run here

def test_real_news(client):
    rv = client.post(
        "/check",
        data=dict(text="U.S. launches effort to reduce reliance on imports or critical minerals"),
        follow_redirects=True,
    )
    assert b"It's Not Fake News :)" in rv.data

    rv = client.post(
        "/check",
        data=dict(text="Trump on Twitter (Dec 21) - Tax Cuts, Home sales"),
        follow_redirects=True,
    )
    assert b"It's Not Fake News :)" in rv.data

def test_fake_news(client):
    rv = client.post(
        "/check",
        data=dict(text="Fresh Off The Golf Course, Trump Lashes Out At FBI Deputy Director And James Comey"),
        follow_redirects=True,
    )
    assert b"It's Fake News!" in rv.data

    rv = client.post(
        "/check",
        data=dict(text="Racist Alabama Cops Brutalize Black Boy While He Is In Handcuffs (GRAPHIC IMAGES)"),
        follow_redirects=True,
    )
    assert b"It's Fake News!" in rv.data