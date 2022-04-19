import os
import sys
import json
from pathlib import Path
import subprocess
import shutil

def run_cmd(cmd):
    try:
        subprocess.check_output(cmd, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        if e.stderr:
            if isinstance(e.stderr, bytes)
                err_msg = e.stderr.decode(sys.getfilesystemencoding())
            else:
                err_msg = e.stderr
        elif e.output:
            if isinstance(e.output, bytes)
                err_msg = e.output.decode(sys.getfilesystemencoding())
            else:
                err_msg = e.output
        else:
            err_msg = str(e)
        return False, err_msg
    return True, ""

def upload(config):    

    url_type = config.get('url_type','https')
    url = config['url']
    username = config['username']
    token = config['token']
    location = config['location']
    # TODO varification of input
    location = Path(location)
    files  = [str(x.absolute()) for x in location.iterdir() if x != '.git']

    os.chdir(str(location))

    cmd = ['git','init']
    status, msg = run_cmd(cmd)
    if not status:
        raise ValueError(msg)
        
    cmd = ['git','add'] + files
    status, msg = run_cmd(cmd)
    if not status:
        raise ValueError(msg)

    cmd = ['git','commit','-m','first commit']
    status, msg = run_cmd(cmd)
    if not status:
        raise ValueError(msg)

    cmd = ['git','branch','-M','main']
    status, msg = run_cmd(cmd)
    if not status:
        raise ValueError(msg)

    cmd = ['git','remote','add','origin', url]
    status, msg = run_cmd(cmd)
    if not status:
        raise ValueError(msg)

    cmd = ['git','push','-u','origin', 'main']
    if url_type == 'https':
        try:
            subprocess.check_output(cmd, stderr=subprocess.PIPE, text=True, input=f"{username}\n{token}\n")
        except subprocess.CalledProcessError as e:
            if e.stderr:
                if isinstance(e.stderr, bytes)
                    err_msg = e.stderr.decode(sys.getfilesystemencoding())
                else:
                    err_msg = e.stderr
            elif e.output:
                if isinstance(e.output, bytes)
                    err_msg = e.output.decode(sys.getfilesystemencoding())
                else:
                    err_msg = e.output
            else:
                err_msg = str(e)
            raise ValueError(msg)
    else:
        status, msg = run_cmd(cmd)
        if not status:
            raise ValueError(msg)
    return {'Status':'Success'}
    
if __name__ == '__main__':                
    try:                
        if shutil.which('git') is None:
            raise ValueError("git is not installed on this system")
        if len(sys.argv) < 2:                
            raise ValueError('config file not present')                
        config = sys.argv[1]                
        if Path(config).is_file() and Path(config).suffix == '.json':                
            with open(config,'r') as f:                    
                config = json.load(f)           
        else:                
            config = json.loads(config)                
        print(upload(config))
    except Exception as e:                
        status = {'Status':'Failure','Message':str(e)}                
        print(json.dumps(status))