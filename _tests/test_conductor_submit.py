import unittest
import re
import sys

sys.path.append("../python")

import conductor_submit



class TestConductorSubmit(unittest.TestCase):
    
    tractor_tasks = [ {u'maxslots': None, u'jid': 25, u'minslots': None, u'resumewhile': [], u'service': u'', u'cid': 2, u'tags': [u'render'], u'retryrcodes': [], u'argv': [u'Render', u'-s', u'3', u'-e', u'4', u'-b', u'1', u'-rl', u'defaultRenderLayer', u'-rd', u'/tmp/render_output/', u'-proj', u'"C:/Users/jlehrman/Documents/maya/projects/conductor/"', u'"/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"'], u'maxrunsecs': 0.0, u'tid': 3, u'envkey': [u'conductor', u'conductorpoll', u'conductor_tid=13', 'conductor_tid=13', 'conductor_jid=13'], u'refersto': u'', u'msg': u'', u'resumepin': False, u'runtype': u'regular', u'metadata': u'', u'local': False, u'id': u'', u'expand': False, u'minrunsecs': 0.0},
                      {u'maxslots': None, u'jid': 25, u'minslots': None, u'resumewhile': [], u'service': u'', u'cid': 3, u'tags': [u'render'], u'retryrcodes': [], u'argv': [u'Render', u'-s', u'5', u'-e', u'5', u'-b', u'1', u'-rl', u'defaultRenderLayer', u'-rd', u'/tmp/render_output/', u'-proj', u'"C:/Users/jlehrman/Documents/maya/projects/conductor/"', u'"/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"'], u'maxrunsecs': 0.0, u'tid': 4, u'envkey': [u'conductor', u'conductorpoll', u'conductor_tid=14', 'conductor_tid=14', 'conductor_jid=14'], u'refersto': u'', u'msg': u'', u'resumepin': False, u'runtype': u'regular', u'metadata': u'', u'local': False, u'id': u'', u'expand': False, u'minrunsecs': 0.0}]
    
    conductor_tasks = [{u'status': u'downloaded', u'timeFinished': 1562351632698867L, u'timeStarted': 1562351495627719L, u'environment': {u'MAYA_PLUG_IN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'MAYA_LOCATION': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6', u'MAYA_LICENSE': u'unlimited', u'PYTHONPATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/Conductor:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'MAYA_DISABLE_CIP': u'1', u'MAYA_SCRIPT_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'solidangle_LICENSE': u'4101@docker_host', u'MAYA_RENDER_DESC_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1.', u'PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/bin:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./bin', u'ARNOLD_PLUGIN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'LD_LIBRARY_PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/xgen/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/bifrost/lib'}, u'jobId': 6439969292025856L, u'priority': u'006', u'jobLabel': u'00764', u'uploadId': 4914522804715520L, u'taskLabel': u'000', u'id': 5175804321595392L, u'command': u'Render  -s 3 -e 4 -b 1 -rl defaultRenderLayer -rd /tmp/render_output/ -proj "C:/Users/jlehrman/Documents/maya/projects/conductor/" "/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"', u'statusDescription': u'', u'selfLink': u'/api/tasks/5175804321595392'},
                       {u'status': u'downloaded', u'timeFinished': 1562351632698867L, u'timeStarted': 1562351495627719L, u'environment': {u'MAYA_PLUG_IN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'MAYA_LOCATION': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6', u'MAYA_LICENSE': u'unlimited', u'PYTHONPATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/Conductor:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'MAYA_DISABLE_CIP': u'1', u'MAYA_SCRIPT_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'solidangle_LICENSE': u'4101@docker_host', u'MAYA_RENDER_DESC_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1.', u'PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/bin:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./bin', u'ARNOLD_PLUGIN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'LD_LIBRARY_PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/xgen/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/bifrost/lib'}, u'jobId': 6439969292025856L, u'priority': u'006', u'jobLabel': u'00764', u'uploadId': 4914522804715520L, u'taskLabel': u'000', u'id': 5175804321595392L, u'command': u'Render  -s 5 -e 5 -b 1 -rl defaultRenderLayer -rd /tmp/render_output/ -proj "C:/Users/jlehrman/Documents/maya/projects/conductor/" "/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"', u'statusDescription': u'', u'selfLink': u'/api/tasks/5175804321595392'}]

    expected_pairing = [ ({u'maxslots': None, u'jid': 25, u'minslots': None, u'resumewhile': [], u'service': u'', u'cid': 2, u'tags': [u'render'], u'retryrcodes': [], u'argv': [u'Render', u'-s', u'3', u'-e', u'4', u'-b', u'1', u'-rl', u'defaultRenderLayer', u'-rd', u'/tmp/render_output/', u'-proj', u'"C:/Users/jlehrman/Documents/maya/projects/conductor/"', u'"/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"'], u'maxrunsecs': 0.0, u'tid': 3, u'envkey': [u'conductor', u'conductorpoll', u'conductor_tid=13', 'conductor_tid=13', 'conductor_jid=13'], u'refersto': u'', u'msg': u'', u'resumepin': False, u'runtype': u'regular', u'metadata': u'', u'local': False, u'id': u'', u'expand': False, u'minrunsecs': 0.0},
                          {u'status': u'downloaded', u'timeFinished': 1562351632698867L, u'timeStarted': 1562351495627719L, u'environment': {u'MAYA_PLUG_IN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'MAYA_LOCATION': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6', u'MAYA_LICENSE': u'unlimited', u'PYTHONPATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/Conductor:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'MAYA_DISABLE_CIP': u'1', u'MAYA_SCRIPT_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'solidangle_LICENSE': u'4101@docker_host', u'MAYA_RENDER_DESC_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1.', u'PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/bin:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./bin', u'ARNOLD_PLUGIN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'LD_LIBRARY_PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/xgen/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/bifrost/lib'}, u'jobId': 6439969292025856L, u'priority': u'006', u'jobLabel': u'00764', u'uploadId': 4914522804715520L, u'taskLabel': u'000', u'id': 5175804321595392L, u'command': u'Render  -s 3 -e 4 -b 1 -rl defaultRenderLayer -rd /tmp/render_output/ -proj "C:/Users/jlehrman/Documents/maya/projects/conductor/" "/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"', u'statusDescription': u'', u'selfLink': u'/api/tasks/5175804321595392'} ),
                          
                          ({u'maxslots': None, u'jid': 25, u'minslots': None, u'resumewhile': [], u'service': u'', u'cid': 3, u'tags': [u'render'], u'retryrcodes': [], u'argv': [u'Render', u'-s', u'5', u'-e', u'5', u'-b', u'1', u'-rl', u'defaultRenderLayer', u'-rd', u'/tmp/render_output/', u'-proj', u'"C:/Users/jlehrman/Documents/maya/projects/conductor/"', u'"/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"'], u'maxrunsecs': 0.0, u'tid': 4, u'envkey': [u'conductor', u'conductorpoll', u'conductor_tid=14', 'conductor_tid=14', 'conductor_jid=14'], u'refersto': u'', u'msg': u'', u'resumepin': False, u'runtype': u'regular', u'metadata': u'', u'local': False, u'id': u'', u'expand': False, u'minrunsecs': 0.0},
                           {u'status': u'downloaded', u'timeFinished': 1562351632698867L, u'timeStarted': 1562351495627719L, u'environment': {u'MAYA_PLUG_IN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'MAYA_LOCATION': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6', u'MAYA_LICENSE': u'unlimited', u'PYTHONPATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/Conductor:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'MAYA_DISABLE_CIP': u'1', u'MAYA_SCRIPT_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./scripts', u'solidangle_LICENSE': u'4101@docker_host', u'MAYA_RENDER_DESC_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1.', u'PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/bin:/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./bin', u'ARNOLD_PLUGIN_PATH': u'/opt/solidangle/arnold-maya/3/arnold-maya-maya2018-3.2.1-1./plug-ins', u'LD_LIBRARY_PATH': u'/opt/autodesk/maya-io/2018/maya-io2018.SP6/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/xgen/lib:/opt/autodesk/maya-io/2018/maya-io2018.SP6/plug-ins/bifrost/lib'}, u'jobId': 6439969292025856L, u'priority': u'006', u'jobLabel': u'00764', u'uploadId': 4914522804715520L, u'taskLabel': u'000', u'id': 5175804321595392L, u'command': u'Render  -s 5 -e 5 -b 1 -rl defaultRenderLayer -rd /tmp/render_output/ -proj "C:/Users/jlehrman/Documents/maya/projects/conductor/" "/Users/jlehrman/Documents/maya/projects/conductor/simple_shapes.ma"', u'statusDescription': u'', u'selfLink': u'/api/tasks/5175804321595392'}   )
                     ]
    
    def test_match_tasks(self):
#         tractor_cmd = self.tractor_tasks[0]['argv']
#         
#         tractor_first_frame = tractor_cmd[tractor_cmd.index("-s")+1]
#         tractor_end_frame = tractor_cmd[tractor_cmd.index("-e")+1]
#         
#         print tractor_first_frame, tractor_end_frame
#         
#         conductor_cmd = self.conductor_tasks[0]['command'].split()
#         print conductor_cmd
#         
#         conductor_first_frame = tractor_cmd[tractor_cmd.index("-s")+1]
#         conductor_end_frame = tractor_cmd[tractor_cmd.index("-e")+1]
#         
#         print conductor_first_frame, conductor_end_frame
#         
        pairing = conductor_submit.match_tractor_commands_to_conductor_tasks(self.tractor_tasks, self.conductor_tasks)
        
        print pairing.keys()
        print pairing.values()[0]
        print pairing.values()[1]      

        
         

if __name__ == "__main__":
    unittest.main()