#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected output"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payloadi)
    """Test class for GithubOrgClient methods"""

    def test_public_repos_url(self):
        """Unit-test _public_repos_url property"""
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test-org/repos")


    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos with mocked data"""

        # Payload returned by get_json (mocked API response)
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload

        # Patch the _public_repos_url property to return a fake URL
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"

            # Instantiate client and call method
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Assert the result is a list of repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Ensure mocks were called exactly once
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
            mock_repos_url.assert_called_once()
