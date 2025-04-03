#!groovy
import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

// Criar usuário admin automaticamente
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount('admin', 'admin')
instance.setSecurityRealm(hudsonRealm)

// Permitir que usuários autenticados façam qualquer coisa
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
instance.setAuthorizationStrategy(strategy)

instance.save()
