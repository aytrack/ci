import os


class Config:
    # for jira
    user = 'sre-bot@pingcap.com'
    pwd = os.getenv("JIRA_PASSWORD")
    affect_version_field = 'versions'
    fix_version_field = 'fixVersions'

    # for tcms, default get token from $HOME/.tcctl
    tcms_token = os.getenv("TCMS_TOKEN")

    # for github
    github_token = os.getenv("GITHUB_TOKEN")





