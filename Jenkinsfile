pipeline {

    agent none
    
    stages {

        stage ('Build') {
            agent { label 'master' }
            tools { maven 'Maven352' }
                steps {
                    checkout scm
                    sh 'mvn package'
                    sh 'aws s3 cp target/spring*.jar s3://vmerh/spring.jar'
//                    sh """aws ec2 terminate-instances --instance-ids \
//                        \$(curl -s http://169.254.169.254/latest/meta-data/instance-id)"""
                }
        }

        stage('All tests') {
            failFast true
            parallel {
                
                stage ('Database Worker') {
                    agent { label 'db' }
                        steps {
                            sh 'curl -O https://raw.githubusercontent.com/MrNight7/spring-petclinic/master/ec2/db-playbook.yml'
                            sh 'curl -O https://raw.githubusercontent.com/MrNight7/spring-petclinic/master/ec2/mysql.cnf.j2'
                            ansiblePlaybook(
                                    playbook: 'db-playbook.yml')
                               }
                }

                stage ('Application Worker') {
                    agent { label 'app' }
                        steps {
                            sh 'curl -O https://raw.githubusercontent.com/MrNight7/spring-petclinic/master/ec2/app-playbook.yml'
                                ansiblePlaybook(
                                    playbook: 'app-playbook.yml')
                            sh 'aws s3 mv s3://vmerh/spring.jar s3://vmerh/spring-${BUILD_ID}-${GIT_COMMIT}.jar'
                        }
                }
            }
        }

        stage ('Terminate instances') {
            agent { label 'master' }
                steps {
                    sh """for i in \$(aws ec2 describe-instances \
                    --filters 'Name=tag:Name,Values=*Worker' \
                    --query 'Reservations[*].Instances[*].InstanceId' \
                    --output=text); do aws ec2 terminate-instances \
                    --instance-ids \$i; done"""
                }
        }
    }
}
