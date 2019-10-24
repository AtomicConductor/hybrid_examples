import time
import subprocess
import json
import sys
import logging
import os

import conductor.lib.api_client as conductor_api
import conductor.lib.conductor_submit as conductor_submit
import conductor.lib.downloader2

LOG_FORMAT = "%(name)s [%(levelname)s] - %(asctime): %(message)s"

LOG = logging.getLogger("conductor_poll")
LOG.setLevel(10)
logging.basicConfig(format=LOG_FORMAT)



def get_job_status(job_id, task_id=None):
    
    api = conductor_api.ApiClient()

    uri = "https://api.conductortech.com/api/v1/tasks?filter=jobLabel_eq_{},taskLabel_eq_{}".format(job_id, task_id)
    response, response_code = api.make_request(uri_path=uri, verb="GET", raise_on_error=False,
                                               use_api_key=True)

    return response

def get_task_log(job_id, task_id, first_line):
    
    api = conductor_api.ApiClient()
    
    uri = "get_log_file?job={job_id}&task={task_id}&num_lines%5B%5D={line_num}".format(job_id=job_id, task_id=task_id, line_num=first_line)
    response, response_code = api.make_request(uri_path=uri, verb="GET", raise_on_error=False,
                                               use_api_key=True)
    
    return response

def poll_job(job_label, task_label='000'):
        
    first_log_line = 0
    poll_interval = 10
    task_url = "https://dashboard.conductortech.com/jobs/{}/{}/log".format(job_label, task_label)
    
    # The log can be (partially) downloaded if any of these statuses is true
    TASK_LOG_READY_STATUSES = ['running', 'success', 'downloaded', 'failed']
    
    # These statuses indicate the task has sucesfully complete
    TERMINATE_STATUSES = ['success', 'downloaded'] 
    
    while True:
        
        # Get the Task status
        response = json.loads(get_job_status(job_label, task_label))
        task = response['data'][0]
        task_status = task['status']        
        LOG.info("Conductor Job #{}, Task #{} ({}) status: {}".format(job_label, task_label, task_url, task_status))
        
        if task_status in TASK_LOG_READY_STATUSES:
            
            # Get any new lines in the log
            json_response = get_task_log( job_id=job_label, 
                                          task_id=task_label, 
                                          first_line=first_log_line)
            
            log_response = json.loads(json_response)
            
            try:
                first_log_line += int(log_response['new_num_lines'][0]) 
                print "\n".join(log_response['logs'][0]['log'])
                                
            # Don't fail if there's an issue with the log
            except Exception, errMsg: 
                LOG.warning(str(errMsg))
                continue
            
        if task_status in TERMINATE_STATUSES:
            break
        
        # If the Task failed, there's nothing left to do.
        if task_status in ['failed']:
            raise Exception("Job failed")
        
        time.sleep(poll_interval)
    
    LOG.info("Render complete")

def download_job_cmd(job_label, task_label=None, project='default'):

    if sys.platform == "win32":
        cmd = [sys.executable, r'C:\Program Files (x86)\Conductor Technologies\Conductor\bin\conductor']
        
    else:
        cmd = ['/home/jlehrman/workspace/conductor_client/bin/conductor']

    cmd.extend(["downloader", "--job_id", job_id, "--project", project])
    
    if task_label is not None:
        cmd.extend(['--task_id', task_label])
        
    LOG.debug("Running ({}) {}".format(sys.platform, " ".join(cmd)))
        
    p = subprocess.Popen(cmd, shell=False)
    p.communicate()
    
    if p.returncode != 0:
        raise Exception("The download returned with a code of {}".format(p.returncode))
    
def download_job(job_label, task_label=None, project='default'):
    
    conductor.lib.downloader2.Downloader.download_jobs(job_ids=job_label, task_id=task_label)    
            
if __name__ == "__main__":
    
    job_id = os.environ['CONDUCTOR_JID']
    task_id = os.environ['CONDUCTOR_TID']

    poll_job(job_label=job_id, task_label=task_id)
    download_job(job_label=job_id, task_label=task_id)

    exit(0)