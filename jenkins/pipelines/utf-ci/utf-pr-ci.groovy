def runUTFGo(args) {

    def ok = true

    def run = { suite ->
        stage("Run $suite") {
            try {
                build(job: 'utf-go-build', parameters: [
                    string(name: "SUITE", value: suite),
                    string(name: "TAG", value: "alpha1"),
                ])
                build(job: 'utf-go-test', parameters: [
                    string(name: 'SUITE', value: suite),
                    string(name: "TAG", value: "alpha1"),
                    string(name: 'EXTRA_ARGS', value: args),
                    booleanParam(name: 'REPORT', value: true),
                ])
            } catch (e) {
                println("Error: $e")
                ok = false
            }
        }
    }

    parallel(
        'Group 1': {
            run('clustered_index')
            run('temporary_table')
        },
        'Group 2': {
            run('ticdc')
            run('rowformat')
        },
        'Group 3': {
            run('regression')
        },
    )

    assert ok
}

def runUTFPy(args) {
    build(job: 'utf-py-build', parameters: [
        string(name: 'BRANCH', value: "pr/"+params.ghprbPullId),
    ])
    tag = "pr-"+params.ghprbPullId
    build(job: 'utf-py-batch-test-newest', parameters: [
        string(name: 'EXTRA_ARGS', value: args),
        string(name: 'IMAGE', value: "hub-new.pingcap.net/qa/utf-python:${tag}"),
        booleanParam(name: 'REPORT', value: true),
    ])
}

catchError {
    def args = params.EXTRA_ARGS
    args += " --annotation jenkins.trigger=$BUILD_URL"
    parallel(
        'Run UTF Go': { runUTFGo(args) },
        'Run UTF Py': { runUTFPy(args) },
    )
}
