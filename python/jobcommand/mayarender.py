import logging

from . import command

LOG = logging.getLogger(__name__)

class MayaRenderCommand(command.Command):
    
    def _get_arg_from_list(self, arg):
        
        cmd_list = self.cmd.split()
        
        if arg not in cmd_list:
            raise command.CommandError("Arguments missing in the command. Unable to find the argument '{}' in '{}'".format(arg, self.cmd))
        
        arg_index = cmd_list.index(arg) + 1
        
        LOG.debug("Found arg {} at index {}: '{}'".format(arg, arg_index, cmd_list[arg_index]))
        
        return cmd_list[arg_index]        

    def get_output_path(self):
        return self._get_arg_from_list("-rd")
    
    def get_scene_path(self):        
        cmd_list = self.cmd.split()
        print "-------------------{}----------------{}----".format(cmd_list[-1], type(cmd_list[-1]))
        return cmd_list[-1].replace('"', '')
    
    def get_project_path(self):
        return self._get_arg_from_list("-proj")
    
    def get_end_frame(self):
        return int(self._get_arg_from_list("-e"))
    
    def get_start_frame(self):
        return int(self._get_arg_from_list("-s"))
    
    def get_frame_step(self):
        return int(self._get_arg_from_list("-b"))

    @classmethod
    def is_valid(cls, cmd):
        
        if 'Render' in cmd:
            return True