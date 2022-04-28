image:
	rm -rf build
	mkdir -p build/sync-version
	cp -r plan message source util build/sync-version/
	cp *.py build/sync-version/
	cp requirements.txt build/sync-version/
	cp Dockerfile build/
	cp run.sh build/
	cd ~/test-plan; git checkout main; git pull -r
	cp ~/test-plan/meta.yaml build/
	cp -r ~/test-plan/compute/affected-versions build/
	cp -r ~/test-plan/compute/release build/
	cd ~/test-infra/tools/tcctl; git checkout main; git pull -r; GOOS=linux make build
	cp /Users/chenpeng/test-infra/tools/tcctl/bin/tcctl build/
	docker build -t hub-new.pingcap.net/chenpeng/sync-version:latest build/
