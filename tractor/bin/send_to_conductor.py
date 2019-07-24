#!/usr/bin/python

import logging
import json
import math
import sys

import tractor.api.query

import conductor.lib.api_client as conductor_api

import jobcommand
import conductorjob

LOG = logging.getLogger(__name__)
logging.root.setLevel(10)
LOG.setLevel(10)

def match_tractor_commands_to_conductor_tasks(tractor_commands, conductor_tasks):
    
    tractor_cmd_dict = {}
    pairing_dict = {}
    
    for tractor_cmd in tractor_commands:
        tractor_cmd_args = tractor_cmd['argv']    

        try:
            tractor_first_frame = tractor_cmd_args[tractor_cmd_args.index("-s")+1]
        except ValueError:
            raise conductorjob.ConductorJobError("Encountered an unexpected command in Tractor ('{}'). Expected a Maya Render command containing a start frame argument (-s)".format(tractor_cmd_args))            
        
        try:
            tractor_end_frame = tractor_cmd_args[tractor_cmd_args.index("-e")+1]
        except ValueError:
            raise conductorjob.ConductorJobError("Encountered an unexpected command in Tractor ('{}'). Expected a Maya Render command containing an end frame argument (-e)".format(tractor_cmd_args))                        
        
        
        tractor_cmd_dict[(tractor_first_frame, tractor_end_frame)] = tractor_cmd
        
    for conductor_task in conductor_tasks:
        conductor_cmd_args = conductor_task['command'].split()

        try:
            conductor_first_frame = conductor_cmd_args[conductor_cmd_args.index("-s")+1]
            
        except ValueError:
            raise conductorjob.ConductorJobError("Encountered an unexpected command in Conductor ('{}'). Expected a Maya Render command containing a start frame argument (-s)".format(conductor_cmd_args))

        try:
            conductor_end_frame = conductor_cmd_args[conductor_cmd_args.index("-e")+1]
            
        except ValueError:
            raise conductorjob.ConductorJobError("Encountered an unexpected command in Conductor ('{}'). Expected a Maya Render command containing an end frame argument (-e)".format(conductor_cmd_args))            
        
        pairing_dict[(conductor_first_frame, conductor_end_frame)] = (tractor_cmd_dict[(conductor_first_frame, conductor_end_frame)],
                                                                      conductor_task)
        
    return pairing_dict

def get_conductor_tasks(job_id):
    
    api = conductor_api.ApiClient()

    uri = "https://api.conductortech.com/api/v1/tasks?filter=jobLabel_eq_{}".format(job_id)
    response, response_code = api.make_request(uri_path=uri, verb="GET", raise_on_error=False,
                                               use_api_key=True)    
    
    LOG.debug("Found {} Conductor Tasks for Job {}".format(len(response), job_id))
    
    return json.loads(response)['data']

def get_tractor_commands(job_id):
    
    search_query = "jid = {}".format(job_id)
    columns = ['jid', 'tid', 'envkey', 'argv', 'Job.title', 'Job.owner']
    commands = tractor.api.query.commands(search=search_query, columns=columns)    
    
    LOG.debug("Found {} Tractor Commands for Job {}".format(len(commands), job_id))
    
    return commands
    
    

def update_tractor_tasks(tractor_job_id, conductor_job_id):
    
    tractor_commands = get_tractor_commands(tractor_job_id)
    conductor_tasks = get_conductor_tasks(conductor_job_id)
    
    for t in conductor_tasks:
        LOG.debug( t.keys())
        
    paired_tasks = match_tractor_commands_to_conductor_tasks(tractor_commands, conductor_tasks)
    
    LOG.debug("Found paired tasks: {}".format(paired_tasks))
    
    for frame_tuple, command_pair in paired_tasks.iteritems():
        
        tractor_command = command_pair[0]
        conductor_task = command_pair[1]

        task_id = tractor_command['tid']
        job_id = tractor_command['jid']
        envkey = tractor_command['envkey']

        envkey.append("conductor_tid={}".format(conductor_task['taskLabel']))
        envkey.append("conductor_jid={}".format(conductor_task['jobLabel']))
    
        tractor.api.query.cattr("jid = {} AND tid = {}".format(job_id, task_id), key='envkey', value=envkey)
    
    jobs = tractor.api.query.jobs("jid={}".format(tractor_job_id), columns=['service'], limit=1)
    LOG.debug( "jobs: {}".format(jobs))    
    service_key = jobs[0]['service']

    service_key = "Conductor".format(service_key)
    
    tractor.api.query.jattr("jid = {}".format(tractor_job_id), key='service', value=service_key)

if __name__ == "__main__":
 
    # Read data that is passed by the Tractor menu command
    jsonData = sys.stdin.read()
    
    if jsonData:
        jobs = json.loads(jsonData)
    
        LOG.debug("Using input: '{}'".format(jobs, type(jobs)))
        
        for job in jobs:
            
            tractor_job_id = job['jid']
            
            submitter = conductorjob.ConductorJob.create_from_tractor_job(job_id=tractor_job_id)
            conductor_job_id = submitter.submit_job()
            
            update_tractor_tasks(tractor_job_id, conductor_job_id)
        
    print "--- DONE ---"