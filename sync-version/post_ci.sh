#!/bin/bash

set -x
set -e

git config --global url."https://${GITHUB_TOKEN}:x-oauth-basic@github.com/".insteadOf "https://github.com/"
git config --global user.email "chenpeng@pingcap.com"
git config --global user.name "ChenPeng2013"

export YAML_PATH="/home/jenkins/agent/workspace/test-plan/compute/sqlfeature/"

git checkout $BEFORE
python -m cases.cli case list --case-meta > test.log

git checkout master
python -m cases.cli ci plan --old-cases test.log
python -m cases.cli case list --case-meta > test2.log

PRECASES=$(wc -l test.log | awk '{print $1}')
CURCASES=$(wc -l test2.log | awk '{print $1}')
CASES=$[CURCASES - PRECASES]
if [ $CASES -eq 0 ]; then
	echo "don't have new cases"
	exit 0
fi

# generater new yaml, if it is tidb issue cases, add affects-branch label
FILENAME="utf-master.yaml"

if [ -f "$FILENAME" ]; then
        rm "$FILENAME"
fi

python -m cases.cli ci one_shot --old-cases test.log

set +e
grep caseName $FILENAME | grep -E "TIBUG-|GH-TIDB-"
CODE=$?
set -e

if [ $CODE == 0 ]; then
  # github issue cases
  LINK=$(/root/tcctl run --token $TCMS_TOKEN -m /home/jenkins/agent/workspace/test-plan/compute/release -f $FILENAME 2>&1)
  LINK=${LINK%%) will run later*}
  TRIGGERID=${LINK##*ID=}
  # add label to tidb issue
  python /root/sync-version/main.py sync --trigger-id $TRIGGERID --trigger-type branch github
fi

set +e
grep caseName $FILENAME | grep "TIBUG-"
CODE=$?
set -e

if [ $CODE == 0 ]; then
  # tibug cases
  LINK=$(/root/tcctl run --token $TCMS_TOKEN -m /home/jenkins/agent/workspace/test-plan/compute/affected-versions -f $FILENAME 2>&1)
  LINK=${LINK%%) will run later*}
  TRIGGERID=${LINK##*ID=}
  # add label to tidb issue
  python /root/sync-version/main.py sync --trigger-id $TRIGGERID --trigger-type version tibug
fi


cd /home/jenkins/agent/workspace/test-plan

set +e
git remote add upstream https://github.com/ChenPeng2013/test-plan.git
set -e

BRANCH="utf-"$(date +%Y%m%d-%H%M)
git checkout -b ${BRANCH}
git add compute/sqlfeature/*.yaml
git commit -m "add cases"
git push upstream ${BRANCH}

YAMLS=$(git diff origin/main... --stat | grep yaml | awk '{print $1}')
ONESHOT=""
for NAME in $(echo $YAMLS); do
  echo "  resourcePool: sql-coverage" >> $NAME
	LINK=$(/root/tcctl run --token $TCMS_TOKEN -m /home/jenkins/agent/workspace/test-plan/meta.yaml -f $NAME 2>&1)
	git checkout $NAME
	LINK=${LINK%% to open*}
	LINK=${LINK##*click}
	ID=${LINK##*plan/}
	URL="https://tcms.pingcap.net/api/v1/plan-executions?offset=0&count=20&ids="${ID}
	ONESHOT=${ONESHOT}" "${LINK}
	while true; do
		sleep 10
		STATUS=$(curl $URL |  python3 -c "import json; import sys; print(json.load(sys.stdin)['data'][0]['status'])")
		if [ "${STATUS}" = "FAILURE" ]; then
			break
		elif [ "${STATUS}" = "PENDING" ]; then
			continue
		elif [ "${STATUS}" = "RUNNING" ]; then
			continue
		elif [ "${STATUS}" = "PREPARING" ]; then
			continue
		elif [ "${STATUS}" = "SUCCESS" ]; then
			echo $NAME" success"
			break
		else
			echo "unknown status "${STATUS}
			exit 1
		fi
	done
done

/root/gh pr create --base main --title "add cases" --body "${ONESHOT}" -H ChenPeng2013:${BRANCH} --repo pingcap/test-plan

sleep 10

PRID=$(/root/gh pr list --repo pingcap/test-plan --author "@me" | grep "utf-2022" | awk 'BEGIN{FS="\t"}{print $1}')
URL="https://github.com/pingcap/test-plan/pull/${PRID}"

curl -X POST -H "Content-Type: application/json" -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"add ${CASES} cases ${URL}\"}}" https://open.feishu.cn/open-apis/bot/v2/hook/73c3d201-09e6-47dd-8cf3-55ec106ef007

set +e
set +x