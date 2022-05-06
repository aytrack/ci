#!/bin/bash
set -x
set -e

PRID=$1
FILENAME="utf-pr-$PRID.yaml"

if [ -f "$FILENAME" ]; then
        rm "$FILENAME"
fi

python -m cases.cli ci one_shot --old-cases test.log

if [ ! -f "$FILENAME" ]; then
  # don't generate new cases
	exit 0
fi

set +e
grep caseName $FILENAME | grep -E "TIBUG-|GH-TIDB-"
CODE=$?
set -e

if [ $CODE == 0 ]; then
  # github issue cases
  LINK=$(/root/tcctl run --token $TCMS_TOKEN -m /home/jenkins/agent/workspace/test-plan/compute/release -f $FILENAME 2>&1)
  LINK=${LINK%%) will run later*}
  TRIGGERID=${LINK##*ID=}
  python /root/sync-version/main.py sync --trigger-id $TRIGGERID --trigger-type branch pr --pr-id $PRID

  set +e
  grep caseName $FILENAME | grep "TIBUG-"
  CODE=$?
  set -e
  if [ $CODE == 0 ]; then
    # tibug cases
    LINK=$(/root/tcctl run --token $TCMS_TOKEN -m /home/jenkins/agent/workspace/test-plan/compute/affected-versions -f $FILENAME 2>&1)
    LINK=${LINK%%) will run later*}
    TRIGGERID=${LINK##*ID=}
    python /root/sync-version/main.py sync --trigger-id $TRIGGERID --trigger-type version pr --pr-id $PRID
  fi
  exit 0
fi

LINK=$(/root/tcctl run --token $TCMS_TOKEN -m /home/jenkins/agent/workspace/test-plan/compute/meta.yaml -f $FILENAME 2>&1)
LINK=${LINK%% to open*}
LINK=${LINK##*click}
ID=${LINK##*plan/}
URL="https://tcms.pingcap.net/api/v1/plan-executions?offset=0&count=20&ids="${ID}
curl -s -H "Authorization: token ${GITHUB_TOKEN}" -X POST -d "{\"body\": \"one_shot ${LINK}\"}"  "https://api.github.com/repos/pingcap/automated-tests/issues/$PRID/comments"

while true; do
	sleep 10
	STATUS=$(curl ${URL} |  python3 -c "import json; import sys; print(json.load(sys.stdin)['data'][0]['status'])")
	if [ "${STATUS}" = "FAILURE" ]; then
		exit 1
	elif [ "${STATUS}" = "PENDING" ]; then
		continue
	elif [ "${STATUS}" = "RUNNING" ]; then
		continue
	elif [ "${STATUS}" = "PREPARING" ]; then
		continue
	elif [ "${STATUS}" = "SUCCESS" ]; then
		echo "success"
		break
	else
		echo "unknown status "${STATUS}
		exit 1
	fi
done

set +e