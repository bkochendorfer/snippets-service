@Library('github.com/mozmeao/jenkins-pipeline@20170315.1')
def stage_deployed = false
def config
def docker_image

conduit {
  node {
    stage("Prepare") {
      checkout scm
      setGitEnvironmentVariables()

      try {
        config = readYaml file: "jenkins.yml"
      }
      catch (e) {
        config = []
      }
      println "config ==> ${config}"

      if (!config || (config && config.pipeline && config.pipeline.enabled == false)) {
        println "Pipeline disabled."
      }
    }

    docker_image = "${config.project.docker_name}:${GIT_COMMIT_SHORT}"

    stage("Build") {
      if (!dockerImageExists(docker_image)) {
        sh "echo 'ENV GIT_SHA ${GIT_COMMIT}' >> Dockerfile"
        dockerImageBuild(docker_image, ["pull": true])
      }
      else {
        echo "Image ${docker_image} already exists."
      }
    }

    stage("Test") {
      parallel "Lint": {
        dockerRun(docker_image, "flake8 snippets")
      },
      "Unit Test": {
        def db_name = "postgres-${env.GIT_COMMIT_SHORT}-${BUILD_NUMBER}"
        def args = [
          "docker_args": ("--name ${db_name} " +
                          "-e POSTGRES_PASSWORD=snippets " +
                          "-e POSTGRES_USER=snippets " +
                          "-e POSTGRES_DB=snippets "),
        ]

        dockerRun("postgres:11-alpine", args) {
          args = [
            "docker_args": ("--link ${db_name}:db " +
                            "-e CHECK_PORT=5432 " +
                            "-e CHECK_HOST=db")
          ]
          // Takis waits for mysql to come online
          dockerRun("giorgos/takis", args)

          args = [
            "docker_args": ("--link ${db_name}:db " +
                            "-e 'DEBUG=False' " +
                            "-e 'ALLOWED_HOSTS=*' " +
                            "-e 'SECRET_KEY=foo' " +
                            "-e 'DATABASE_URL=postgres://snippets:snippets@db/snippets' " +
                            "-e 'SITE_URL=http://localhost:8000' " +
                            "-e 'CACHE_URL=dummy://' " +
                            "-e 'ENABLE_ADMIN=True' " +
                            "-e 'SECURE_SSL_REDIRECT=False'"),
            "cmd": "coverage run ./manage.py test --parallel"
          ]
          dockerRun(docker_image, args)
        }
      }
    }

    stage("Upload Images") {
      dockerImagePush(docker_image, "mozjenkins-docker-hub")
    }
  }

  milestone()

  def deployDev = false
  def deployStage = false
  def deployProd = false

  node {
    onBranch("master") {
       deployDev = true
    }
    onBranch("staging") {
       deployStage = true
    }
    onBranch("production") {
       deployProd = true
    }
  }

  if (deployDev) {
    for (deploy in config.deploy.dev) {
      stage ("Deploying to ${deploy.name}") {
        node {
          lock("push to ${deploy.name}") {
            deis_executable = deploy.deis_executable ?: "deis"
            deisLogin(deploy.url, deploy.credentials, deis_executable) {
              deisPull(deploy.app, docker_image, null, deis_executable)
            }
            newRelicDeployment(deploy.newrelic_app, env.GIT_COMMIT_SHORT,
                               "jenkins", "newrelic-api-key")
          }
        }
      }
      stage ("Acceptance tests against ${deploy.name}") {
        node {
          lock("push to ${deploy.name}") {
            sh "bin/acceptance-tests.sh ${deploy.app_url}"
          }
        }
      }
    }
  }
  if (deployStage) {
    for (deploy in config.deploy.stage) {
      stage ("Deploying to ${deploy.name}") {
        node {
          lock("push to ${deploy.name}") {
            deis_executable = deploy.deis_executable ?: "deis"
            deisLogin(deploy.url, deploy.credentials, deis_executable) {
              deisPull(deploy.app, docker_image, null, deis_executable)
            }
            newRelicDeployment(deploy.newrelic_app, env.GIT_COMMIT_SHORT,
                               "jenkins", "newrelic-api-key")
          }
        }
      }
      stage ("Acceptance tests against ${deploy.name}") {
        node {
          lock("push to ${deploy.name}") {
            sh "bin/acceptance-tests.sh ${deploy.app_url}"
          }
        }
      }
    }
  }
  if (deployProd) {
    for (deploy in config.deploy.prod) {
      stage ("Deploying to ${deploy.name}") {
        node {
          lock("push to ${deploy.name}") {
            deis_executable = deploy.deis_executable ?: "deis"
            deisLogin(deploy.url, deploy.credentials, deis_executable) {
              deisPull(deploy.app, docker_image, null, deis_executable)
            }
            newRelicDeployment(deploy.newrelic_app, env.GIT_COMMIT_SHORT,
                               "jenkins", "newrelic-api-key")
          }
        }
      }
      stage ("Acceptance tests against ${deploy.name}") {
        node {
          lock("push to ${deploy.name}") {
            sh "bin/acceptance-tests.sh ${deploy.app_url}"
          }
        }
      }
    }
  }
}
