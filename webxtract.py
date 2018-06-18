import sys 
import os
import re
from packet import * 

repl_chars = [('\\n','\n'),('\\r','\r'),('\\t','\t')]

def replace_chars(s):
    for t in repl_chars:
        s=s.replace(t[0],t[1])
    return s
def create_dir(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        if not os.path.isdir(dirname):
            raise ValueError("{} exists and is not a directory".format(dirname))

def analyze_frame(frame,path,queue,files):
    packet = Packet(frame)
    request_uri=packet.http.get_request_uri()
    if request_uri!=None:
        queue.append(request_uri)
    else:
        html = packet.http.get_data()
        status_code = packet.http.get_status_code()
        if html!=None and status_code == 200:
            req=queue.pop()
            dirs = os.path.dirname(req)
            filename=os.path.basename(req)
            complete_path=path+dirs
            create_dir(complete_path)
            filename='{}/{}'.format(complete_path,filename) 
            html = replace_chars(html)
            files.append((filename,html))
def main():
    content = None
    path = '{}/output'.format(os.path.dirname(sys.argv[1]))
    create_dir(path)
    with open(sys.argv[1]) as f:
        content = f.read()
    if content != None:
        content = re.split(Packet.regex,content)
    queue=[]
    files=[]
    for frame in content:
        analyze_frame(frame,path,queue,files)
    tosub=[]
    newfiles=[]
    for f in files:
       filename,html = f
       if not filename.endswith('.html'):
           basename = os.path.basename(filename)
           newbase = re.sub('.[a-z]+$','.html',basename)
           newfiles.append((os.path.dirname(filename)+'/'+newbase,html))
           tosub.append((basename,newbase))
       else:
           newfiles.append(f)
    newnewfiles=[]
    for s in tosub:
        oldbase,newbase = s
        for f in newfiles:
            filename,html = f
            newhtml = re.sub(oldbase,newbase,html)
            newnewfiles.append((filename,newhtml))
        newfiles = newnewfiles
        newnewfiles=[]
    for f in newfiles:
        name,html = f
        h = open(name,'w')
        h.write(html)

if __name__=="__main__":
    main()
