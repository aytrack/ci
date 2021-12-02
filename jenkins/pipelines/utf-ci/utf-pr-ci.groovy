def runUTFGo(args) {

    def ok = true

    def run = { suite ->
        stage("Run $suite") {
            try {
                build(job: 'utf-go-build', parameters: [
                    string(name: "SUITE", value: suite),
                    string(name: "TAG", value: "alpha1"),
                ])
            } catch (e) {
                println("Error: $e")
                ok = false
            }
        }
    }

    assert ok
}


def main(tag, branch) {
    stage("Checkout") {
        container("python") { sh("chown -R 1000:1000 ./")}
        checkout(changelog: false, poll: false, scm: [
            $class           : "GitSCM",
            branches         : [[name: branch]],
            userRemoteConfigs: [[url: "https://github.com/pingcap/automated-tests.git",
                                 refspec: "+refs/heads/*:refs/remotes/origin/* +refs/pull/*/head:refs/remotes/origin/pr/*", credentialsId: "github-sre-bot"]],
            extensions       : [[$class: 'PruneStaleBranch'], [$class: 'CleanBeforeCheckout']],
        ])
    }

    stage("Test") {
        container("python") {
            sh("""
            pip install ./framework
            git checkout origin/master
            python -m cases.cli case list --case-meta > test.log
            git checkout origin/$branch
            python -m cases.cli ci one_shot --old-cases test.log
            """)
        }
    }
}

def runUTFPy(args) {
    build(job: 'utf-py-build', parameters: [
        string(name: 'BRANCH', value: "pr/"+params.ghprbPullId),
    ])
    tag = "pr-"+params.ghprbPullId
    // try to create one_shot

    podTemplate(name: "utf-one-shot", label: "utf-one-shot", instanceCap: 5, idleMinutes: 60, containers: [
        containerTemplate(name: 'python', image: 'hub-new.pingcap.net/chenpeng/python:3.8', alwaysPullImage: true, ttyEnabled: true, command: 'cat'),
    ]) { node("utf-one-shot") { dir("automated-tests") { main(tag, "pr/"+params.ghprbPullId) } } }
}

catchError {
    def args = params.EXTRA_ARGS
    args += " --annotation jenkins.trigger=$BUILD_URL"
    parallel(
        'Run UTF Go': { runUTFGo(args) },
        'Run UTF Py': { runUTFPy(args) },
    )
}

