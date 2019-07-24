from TrEnvHandler import TrEnvHandler
import logging

class ConductorEnvHandler(TrEnvHandler):
    
    def updateEnvironment(self, cmd, env, envkeys):
    
        self.logger.debug("ConductorEnvHandler.updateEnvironment: %s" % repr(envkeys))
        self.logger.debug("ConductorEnvHandler.updateEnvironment: %s" % repr(env))
        
        for envkey in envkeys:
            if envkey.startswith("conductor_"):
                key, value = envkey.split("=")
                env[key.upper()] = value
    
        return TrEnvHandler.updateEnvironment(self, cmd, env, envkeys)

    def remapCmdArgs(self, cmdinfo, launchenv, thisHost):
        self.logger.debug("ConductorEnvHandler.remapCmdArgs: %s" % self.name)
        argv = ["python", "/data/tractor/bin/conductor_poll.py"]
        
        return argv
