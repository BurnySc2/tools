from test.base_test import test_client  # noqa: F401
from unittest.mock import Mock, patch

import pytest
from litestar.status_codes import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_503_SERVICE_UNAVAILABLE
from litestar.testing import TestClient
from pytest_httpx import HTTPXMock

from routes.login_logout import COOKIES, GithubUser, UserCache, get_github_user


@pytest.mark.asyncio
async def test_get_github_user_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://api.github.com/user",
        json={"id": 123, "login": "Abc"},
    )
    result = await get_github_user("test_access_token")
    assert result is not None
    assert result.id == 123
    assert result.login == "Abc"


@pytest.mark.asyncio
async def test_get_github_user_from_cache():
    mock_user = GithubUser(id=123, login="Abc")
    mock_get = Mock(return_value=mock_user)
    with patch.object(UserCache, "__getitem__", mock_get):
        result = await get_github_user("test_access_token")
        assert result is not None
        assert result.id == 123
        assert result.login == "Abc"


@pytest.mark.asyncio
async def test_get_github_user_no_access_token():
    result = await get_github_user()
    assert result is None


@pytest.mark.asyncio
async def test_route_github_login_already_logged_in(test_client: TestClient, httpx_mock: HTTPXMock) -> None:  # noqa: F811
    # User needs to have the github cookie to be linked to an account
    test_client.cookies[COOKIES["github"]] = "valid_access_token"
    # Get request needs to return the user data
    httpx_mock.add_response(
        url="https://api.github.com/user",
        json={"id": 123, "login": "Abc"},
    )
    response = test_client.get("/login/github")
    assert response.status_code == HTTP_200_OK
    assert response.url.path == "/login"
    # Make sure cookie remains unchanged
    assert test_client.cookies[COOKIES["github"]] == "valid_access_token"


@pytest.mark.asyncio
async def test_route_github_login_code_given_success(test_client: TestClient, httpx_mock: HTTPXMock) -> None:  # noqa: F811
    """
    This test case checks the behavior of the application when the Github API returns the access token
    successfully using a code.
    """
    # Post request needs to return the access token
    httpx_mock.add_response(
        url="https://github.com/login/oauth/access_token",
        json={"access_token": "myaccesstoken"},
    )
    # Once access token has been optained, valid user data needs to be returned
    httpx_mock.add_response(
        url="https://api.github.com/user",
        json={"id": 123, "login": "Abc"},
    )
    # Make sure cookie was not set before
    assert COOKIES["github"] not in test_client.cookies
    # Github api returns a parameter "code=somevalue" which can be used to fetch the access token
    response = test_client.get("/login/github?code=mycode")
    assert response.status_code == HTTP_200_OK
    assert response.url.path == "/login"
    # Make sure cookie has been set
    assert test_client.cookies[COOKIES["github"]] == "myaccesstoken"


@pytest.mark.asyncio
async def test_route_github_login_code_given_but_service_down(test_client: TestClient, httpx_mock: HTTPXMock) -> None:  # noqa: F811
    """
    This test case checks the behavior of the application when the Github API is down
    while trying to fetch the access token using a code.
    """
    httpx_mock.add_response(
        url="https://github.com/login/oauth/access_token",
        status_code=503,
    )
    response = test_client.get("/login/github?code=mycode")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.asyncio
async def test_route_github_login_code_given_but_error(test_client: TestClient, httpx_mock: HTTPXMock) -> None:  # noqa: F811
    """
    This test case checks the behavior of the application when the Github API returns an error
    while trying to fetch the access token using a code.
    """
    httpx_mock.add_response(
        url="https://github.com/login/oauth/access_token",
        json={"error": "some_error_message"},
    )
    response = test_client.get("/login/github?code=mycode")
    assert response.status_code == HTTP_409_CONFLICT
