import os
from github import Github, Auth
from mcp.server.fastmcp import FastMCP

# Initialize
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)
mcp = FastMCP("JM Portfolio MCP Server")


@mcp.tool()
def list_repos(username: str) -> str:
    """List public repositories for a GitHub user."""
    user = gh.get_user(username)
    repos = user.get_repos()
    result = []
    for repo in repos:
        result.append(
            f"- {repo.name}: {repo.description or 'No description'} "
            f"(⭐ {repo.stargazers_count}, {repo.language or 'No language'})"
        )
    return "\n".join(result) if result else "No repos found."


@mcp.tool()
def get_repo(username: str, repo_name: str) -> str:
    """Get detailed information about a specific GitHub repository."""
    repo = gh.get_repo(f"{username}/{repo_name}")
    return (
        f"Name: {repo.name}\n"
        f"Description: {repo.description or 'None'}\n"
        f"Language: {repo.language or 'None'}\n"
        f"Stars: {repo.stargazers_count}\n"
        f"Forks: {repo.forks_count}\n"
        f"Open issues: {repo.open_issues_count}\n"
        f"Created: {repo.created_at}\n"
        f"Last updated: {repo.updated_at}\n"
        f"URL: {repo.html_url}"
    )


@mcp.tool()
def list_repo_contents(username: str, repo_name: str, path: str = "") -> str:
    """List files and directories in a GitHub repository at a given path."""
    repo = gh.get_repo(f"{username}/{repo_name}")
    contents = repo.get_contents(path)
    result = []
    for item in contents:
        result.append(f"[{item.type}] {item.path}")
    return "\n".join(result) if result else "Empty directory."


if __name__ == "__main__":
    mcp.run()
