def main() {
    def tag = params.TAG
    if (tag == "") {
        tag = params.BRANCH.replaceAll("/", "-")
        if (params.FORK != "pingcap") { tag = "${params.FORK}__${tag}".toLowerCase() }
    }

    stage("Checkout") {
        container("python") { sh("chown -R 1000:1000 ./")}
        checkout(changelog: false, poll: false, scm: [
            $class           : "GitSCM",
            branches         : [[name: params.BRANCH]],
            userRemoteConfigs: [[url: "https://github.com/${params.FORK}/test-plan.git",
                                 refspec: params.REFSPEC, credentialsId: "github-sre-bot"]],
            extensions       : [[$class: 'PruneStaleBranch'], [$class: 'CleanBeforeCheckout']],
        ])
    }

    stage("Test") {
        container("python") {
            withCredentials([string(credentialsId: "cp-jira-pwd", variable: 'JIRA_PASSWORD'),string(credentialsId: "cp-github-token", variable: 'GITHUB_TOKEN'),]) {
                sh("""
                python /root/sync-version/main.py check tibug --yaml-file compute/sqlfeature/utf-affectversion-auto.yaml
                python /root/sync-version/main.py check yaml --dir compute/affected-versions --type version
                python /root/sync-version/main.py check yaml --dir compute/release --type branch
                python /root/sync-version/main.py check github --days 1
                python /root/sync-version/main.py check case
                """)
            }
        }
    }
}

def run(label, image, Closure main) {
    podTemplate(name: label, label: label, instanceCap: 5, idleMinutes: 60, containers: [
        containerTemplate(name: 'python', image: image, alwaysPullImage: true, ttyEnabled: true, command: 'cat'),
    ]) { node(label) { dir("test-plan") { main() } } }
}

catchError {
    run('utf-jira-field', 'hub-new.pingcap.net/chenpeng/sync-version:latest') { main() }
}
