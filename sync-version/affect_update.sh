#!/bin/bash

set -x
set -e

FILENAME="compute/sqlfeature/utf-affectversion-auto.yaml"

if [ "${TRIGGERID}" != "" ]; then
  python /root/sync-version/main.py sync --trigger-id $TRIGGERID --trigger-type $TRIGGERTYPE $SYNCTYPE
  exit 0
fi

for NAME in $(echo $FILENAME); do
  if [ $TRIGGERTYPE = "branch" ]; then
    LINK=$(/root/tcctl run --token $TCMS_TOKEN -m compute/release -f $NAME 2>&1)
  fi

  if [ $TRIGGERTYPE = "version" ]; then
    LINK=$(/root/tcctl run --token $TCMS_TOKEN -m compute/affected-versions -f $NAME 2>&1)
  fi
  git checkout $NAME

  LINK=${LINK%%) will run later*}
  TRIGGERID=${LINK##*ID=}
  python /root/sync-version/main.py sync --trigger-id $TRIGGERID --trigger-type $TRIGGERTYPE $SYNCTYPE
done

set +e
set +x