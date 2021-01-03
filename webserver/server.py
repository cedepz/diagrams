import uuid
import os
import re
import sys;
import base64;
import zlib;

from flask import Flask, request, render_template, send_file, send_from_directory
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

import importlib
module = importlib.import_module("diagrams.aws.network")


app = Flask(__name__)

APP_BASE = '/opt/app-root/webserver'

@app.route('/')
def index():
    print("Incoming call")
    return "Hello diagrams world !"

#@app.route('/editor')
#def result():
#    return render_template('index.html')

@app.route('/test')
def test():
    fileid = str(uuid.uuid4())
    code = 'with Diagram("test", show=False, direction="TB"):\n\tELB("lb") >> [EC2("worker1"),\n\tEC2("worker2"),\n\tEC2("worker3")] >> RDS("events")'
    print("origin str:"+code)
    p = re.compile('with[ ]*Diagram\(([^\)]*)\)') 
    codewithfilename = p.sub("with Diagram(\g<1>, filename=\""+APP_BASE+"/generated/"+fileid+"\")",code,1)
    print("modified str:"+codewithfilename)
    exec(codewithfilename)
    res = send_from_directory(APP_BASE+'/generated/', fileid+".png");
    os.remove(APP_BASE+"/generated/"+fileid+".png")
    return res

@app.route('/diagram', methods = ['POST','GET'])
def diagramgen():
    fileid = str(uuid.uuid4())
    code = request.values['code']
    #print("origin str:"+code)
    p = re.compile('with[ ]*Diagram\(([^\)]*)\)') 
    codewithfilename = p.sub("with Diagram(\g<1>, filename=\""+APP_BASE+"/generated/"+fileid+"\")",code,1)
    #print("modified str:"+codewithfilename)
    exec(codewithfilename)
    res = send_from_directory(APP_BASE+'/generated', fileid+".png");    
    os.remove(APP_BASE+"/generated/"+fileid+".png")
    return res

@app.route('/mgdiagram/<string:path>', methods = ['GET'])
def mgdiagramgen(path):
    fileid = str(uuid.uuid4())
    code = str(zlib.decompress(base64.urlsafe_b64decode(path)))
    print("origin str:"+code)
    p = re.compile('with[ ]*Diagram\(([^\)]*)\)') 
    codewithfilename = p.sub("with Diagram(\g<1>, filename=\""+APP_BASE+"/generated/"+fileid+"\")",code,1)
    #print("modified str:"+codewithfilename)
    exec(codewithfilename)
    res = send_from_directory(APP_BASE+'/generated', fileid+".png");    
    os.remove(APP_BASE+"/generated/"+fileid+".png")
    return res

@app.route('/editor/<path:path>')
def send_static(path):
    print("send_static: "+path)
    return send_from_directory(APP_BASE+"/editor", path)

@app.route('/compress', methods = ['POST','GET'])
def compress():
    code = request.values['code']
    compressedCode = zlib.compress(bytes(code, 'utf-8'), 9)
    encodedCode = base64.urlsafe_b64encode(compressedCode)
    return encodedCode

if __name__ == "__main__":
    print("Starting server")
    app.run(host='0.0.0.0', port= 8080, debug= True)
    
