import logging

LOG = logging.getLogger(__name__)

class CommandError(Exception):
    pass

class Command(object):

    def __init__(self, cmd):
        
        self.cmd = cmd        
        self._match_obj = None
    
    def _get_match_obj(self):
        
        if self._match_obj is None:
            self._match_obj = self.RX.search()
        
        return self._match_obj
    
    def _parse(self):
        pass
    
    @classmethod
    def create(cls, cmd):
        from . import mayarender
        return mayarender.MayaRenderCommand(cmd)

    @classmethod
    def is_valid(cls, cmd):
        from . import mayarender
        return mayarender.MayaRenderCommand.is_valid(cmd)