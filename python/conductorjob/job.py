import logging
import os
import json
import math

import tractor.api.query
import conductor.lib.conductor_submit as conductor_submit

import jobcommand
from __builtin__ import True

LOG = logging.getLogger(__name__)

class ConductorJobError(Exception):
    pass

class ConductorJob(object):
    
    def __init__(self):
    
        self.upload_paths = []
        self.software_packages_ids = []
        self.owner = 'bob'
        self.priority = 5
        self.location = ""
        self.instance_type = "n1-standard-8"
        self.metadata = {}
        self.local_upload = True
        self.auto_retry_policy = {}
        self.preemptible = True
        self.chunk_size = 1
        self.project = "default"
        self.output_path = ""
        self.job_title = ""
        self._dependencies = None
        
        self._dependency_scan_enabled = True
        self.conductor_job_id = None
                
    def _get_task_data(self):
        pass
    
    def _get_frame_range(self):
        pass
    
    def _get_environment(self):
        pass
    
    def get_output_path(self):
        return self.output_path
    
    def scan_for_dependencies(self):
        return []
    
    def get_dependencies(self):
        
        if self._dependencies is None and self._dependency_scan_enabled:            
            self._dependencies = self.scan_for_dependencies()
            
        return self._dependencies + self.upload_paths

    def submit_job(self):
        
        data = { "upload_paths": self.get_dependencies(),
                 "software_package_ids": self.software_packages_ids, 
                 "tasks_data": self._get_task_data(), 
                 "owner": self.owner, 
                 "frame_range": self._get_frame_range(),
                 "environment": self._get_environment(), 
                 "priority": self.priority,
                 "location": self.location, 
                 "instance_type": self.instance_type, 
                 "preemptible": self.preemptible, 
                 "metadata": self.metadata, 
                 "local_upload": self.local_upload, 
                 "autoretry_policy": self.auto_retry_policy,
                 "chunk_size": self.chunk_size, 
                 "project": self.project,
                 "output_path": self.get_output_path(), 
                 "job_title": self.job_title}
        
        for key, value in os.environ.items():
            if key.startswith("CONDUCTOR_JOBPARM_"):
                job_parm_key = key.replace("CONDUCTOR_JOBPARM_", "")
                
                if value.lower() == "true":
                    value = True
                
                elif value.lower() == "false":
                    value = False
                    
                try:
                    value = int(value)
                except ValueError:
                    pass
                    
                data[job_parm_key.lower()] = value
        
        print data
        
        submitter = conductor_submit.Submit(data)
        
        response, response_code = submitter.main()
        LOG.debug("Response Code: %s", response_code)
        LOG.debug("Response: %s", response)
         
        if response_code in [201, 204]:
            LOG.info("Submission Complete")
 
        else:
            LOG.error("Submission Failure. Response code: %s", response_code)
            raise ConductorJobError("Submission Failure. Response code: %s", response_code)
 
        self.conductor_job_id = response['jobid']
         
        return self.conductor_job_id
    
    @classmethod
    def get_klass(cls, cmd):
        '''
        A factory helper method to choose the appropriate child class based on
        the provided command.
        
        :param cmd: The command to get the corresponding class for
        :type cmd: str
        
        :retrun: The ConductorJob that matches the given command
        :rtype: A child class of :class: `ConductorJob`
        '''
        
        from . import MayaRenderJob
        
        if "Render" in cmd:
            return MayaRenderJob
        
        else:
            raise ConductorJobError("Unable to match the command '{}' to an appropriate class".format(cmd))
    
    @classmethod
    def create_from_tractor_job(cls, job_id):
        '''
        A factory method for creating a ConductorJob from a Tractor Job
        
        :param job_id: A Tractor Job ID (jid)
        :type job_id: int
        
        :return: A ConductorJob object that is built from the parameters of the job_id
        :rtype: :class: `ConductorJob`        
        '''
        
        # Get the command entities from Tractor
        search_query = "jid = {}".format(job_id)
        columns = ['jid', 'tid', 'envkey', 'argv', 'Job.title', 'Job.owner', 'Job.envkey']
        LOG.debug("Using Tractor Query: '{}'".format(search_query))
        commands = tractor.api.query.commands(search=search_query, columns=columns)
        LOG.debug("Found {} Tractor Commands for Job {}".format(len(commands), job_id))
        
        for envkey in commands[0]['Job.envkey']:
            
            if envkey.lower().startswith("conductor_jobparm_"):
                key, value = envkey.split("=")
                os.environ[key.upper()] = value

        base_command = None
        start_frame = None
        end_frame = None
        chunks = 0
        
        # Parse all the commands to find the start, end frame and number of chunks
        # for the entire job.        
        for cmd in commands:
            cmd_str = " ".join(cmd['argv'])
    
            if jobcommand.Command.is_valid(cmd_str):
                base_command = jobcommand.Command.create(cmd_str)
                
                start_frame_seq = (start_frame, base_command.get_start_frame())
                start_frame = min(f for f in  start_frame_seq if f is not None)
                
                end_frame_seq = (end_frame, base_command.get_end_frame())
                end_frame = max(f for f in  end_frame_seq if f is not None)
                
                chunks += 1
                
        if base_command is None:
            raise Exception("Can't find an appropriate Tractor command to submit to Conductor")
        
        # Construct the ConductorJob object
        klass = cls.get_klass(base_command.cmd)
        new_job = klass(base_command.get_scene_path(), base_command.get_project_path())
        new_job.output_path = base_command.get_output_path()
        new_job.start_frame = start_frame        
        new_job.end_frame = end_frame
        new_job.frame_step = base_command.get_frame_step()
        
        dependency_sidecar_path = "{}.cdepends".format(base_command.get_scene_path())
        
        with open(dependency_sidecar_path, 'r') as fh:
            dependencies = json.load(fh)
            
        LOG.debug("Using dependencies: {}".format(dependencies))
        
        new_job.upload_paths.extend(dependencies['dependencies'])
        
        # Conductor needs to know the number of frames in a chunk - not the
        # number of chunks
        new_job.chunk_size = int(math.ceil((end_frame - start_frame + 1) / float(chunks)))
        new_job.job_title = commands[0]['Job.title']
        
        # The owner will only be properly propogated to Conductor if the same
        # users exist. Otherwise it will be submitted as the current user
        new_job.owner = commands[0]['Job.owner']
        
        return new_job    
