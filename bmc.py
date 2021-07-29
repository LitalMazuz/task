# -*- coding: utf-8 -*-
"""
@author: lital mazuz
"""

import sys
import threading
import paramiko

lock = threading.Lock()

def connectHostnameAndPrint(hostname, rootDir): 
    '''
    Parameters
    ----------
    hostname : TYPE: string, DESCRIPTION: the “remote” hostname
    rootDir : TYPE: string, DESCRIPTION: root directory name.
    '''
    with lock:
        client.connect(hostname, username='cs205848914', password='shir205848914')   
    stdin, stdout, stderr = client.exec_command('ls '+rootDir) #prints the sub folders & files for the requested directory.
    lines = stdout.readlines()
    lines=[(r.split('\n')[0]) for r in lines]
    print('thread ID: '+ str(threading.get_ident()) +' - '+str(lines))
        
        
def getArgv():
    '''
    Returns
    -------
    hostnames : TYPE: dictionary, DESCRIPTION: list of the “remote” hostname   
    root_dir : TYPE: dictionary, DESCRIPTION: list of the root directory 
    argv_len : TYPE: int, DESCRIPTION: number of parameters (less than 1 - file name)
    '''
    argv_len=len(sys.argv)
    if argv_len==1:
        print("Please enter arguments")
        sys.exit()
    argv = sys.argv[1:]
    argv_len-=1
    hostnames={}
    root_dir={}
    for i in range (0,argv_len):
        hosts_dir=argv[i].split('|')
        hostnames[i]=hosts_dir[0]
        root_dir[i]=hosts_dir[1]
    return hostnames,root_dir,argv_len   


if __name__ == "__main__":
    hostname,root_dir,arg_len=getArgv()
    threads=list()
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
    for i in range(0,arg_len):
        thread=threading.Thread(target=connectHostnameAndPrint,args=(hostname[i],root_dir[i]))
        threads.append(thread) 
    try:  #start the thread's activity  
        for j in threads: 
            j.start()   
    except:
        print("Error: unable to start thread")  
    for j in threads:
        j.join()
      
    client.close()
    
    
    
    
    
    
    



