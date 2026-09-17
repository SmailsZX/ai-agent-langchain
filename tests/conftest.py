"""Фикстуры для тестов."""

import pytest


@pytest.fixture
def sample_expression():
    """Пример математического выражения."""
    return "2 + 2 * 3"


@pytest.fixture
def sample_city():
    """Пример города."""
    return "Иркутск"