# sync tcms results

the repo are written by `Python3`

## prerequisite
environment configuration
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

# jira_password is used to get TIBUG-ID info and update labels
export JIRA_PASSWORD="xxxxxx"
# TCMS_TOKEN is used to get tcms results
export TCMS_TOKEN="xxxxxx"
# GITHUB_TOKEN is used to get tidb issue label and add new labels
export GITHUB_TOKEN="xxxxx"
```

## sync to tibug
update TIBUG-ID affect labels and fix labels
```
python main.py -i trigger_id -t jira
```

## sync to tidb issue
sync all issue labels is a major changes, you must set config.update_all to true or set config.allow_id manually
```
python main.py -i trigger_id -t github
```
