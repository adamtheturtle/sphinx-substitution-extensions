"""
Release the next version.
"""

import datetime
import os
from pathlib import Path

from github import Github
from github.ContentFile import ContentFile
from github.Repository import Repository


def get_version(github_repository: Repository) -> str:
    """
    Return the next version.
    This is today’s date in the format ``YYYY.MM.DD.MICRO``.
    ``MICRO`` refers to the number of releases created on this date,
    starting from ``0``.
    """
    utc_now = datetime.datetime.utcnow()
    date_format = '%Y.%m.%d'
    date_str = utc_now.strftime(date_format)
    tag_labels = [tag.name for tag in github_repository.get_tags()]
    today_tag_labels = [
        item for item in tag_labels if item.startswith(date_str)
    ]
    micro = int(len(today_tag_labels))
    new_version = f'{date_str}.{micro}'
    return new_version


def update_changelog(version: str, github_repository: Repository) -> None:
    """
    Add a version title to the changelog.
    """
    changelog_path = Path('CHANGELOG.rst')
    branch = 'master'
    changelog_content_file = github_repository.get_contents(
        path=str(changelog_path),
        ref=branch,
    )
    # ``get_contents`` can return a ``ContentFile`` or a list of
    # ``ContentFile``s.
    assert isinstance(changelog_content_file, ContentFile)
    changelog_bytes = changelog_content_file.decoded_content
    changelog_contents = changelog_bytes.decode('utf-8')
    new_changelog_contents = changelog_contents.replace(
        'Next\n----',
        f'Next\n----\n\n{version}\n------------',
    )
    github_repository.update_file(
        path=str(changelog_path),
        message=f'Update for release {version}',
        content=new_changelog_contents,
        sha=changelog_content_file.sha,
    )


def main() -> None:
    """
    Perform a release.
    """
    github_token = os.environ['GITHUB_TOKEN']
    github_repository_name = os.environ['GITHUB_REPOSITORY']
    github_client = Github(github_token)
    github_repository = github_client.get_repo(
        full_name_or_id=github_repository_name,
    )
    version_str = get_version(github_repository=github_repository)
    update_changelog(version=version_str, github_repository=github_repository)
    github_repository.create_git_tag_and_release(
        tag=version_str,
        tag_message='Release ' + version_str,
        release_name='Release ' + version_str,
        release_message='See CHANGELOG.rst',
        type='commit',
        object=github_repository.get_commits()[0].sha,
    )


if __name__ == '__main__':
    main()
