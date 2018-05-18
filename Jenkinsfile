pipeline {
    
    agent any
    
    stages {
        
        stage ('Build') {
            
            agent { label 'master' }
            tools { maven 'Maven352' }
            
                steps {
                    checkout scm
                    sh 'mvn package'
                    sh 'aws s3 cp target/spring*.jar s3://vmerh/spring.jar'
                }
        }

        stage('Provision') {
                
                stage ('Database') {
                    
                    agent { label 'database' }
                    
                        steps {
                            sh 'wget https://raw.githubusercontent.com/MrNight7/spring-petclinic/master/database.yml'
                            sh 'wget https://raw.githubusercontent.com/MrNight7/spring-petclinic/master/my.cnf'
                            ansiblePlaybook(
                                    playbook: 'database.yml')
                               }
                }

                stage ('Application') {
                    
                    agent { label 'application' }
                    
                        steps {
                            sh 'wget https://raw.githubusercontent.com/MrNight7/spring-petclinic/master/application.yml'
                                ansiblePlaybook(
                                    playbook: 'application.yml')
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
