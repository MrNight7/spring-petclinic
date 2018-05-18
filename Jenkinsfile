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
}
