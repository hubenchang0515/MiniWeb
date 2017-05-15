#! /usr/bin/env python3

if __name__ == '__main__' :
    import type
else :
    from .type import *

from wsgiref.simple_server import make_server

import magic
import os
import re
import cgi

class Web(object) :
    @property
    def port(self) :
        return self.__port
        
    @port.setter
    def port(self,port) :
        assert isinstance(port,int) and port >= 0 and port <= 65535 , 'Port should be an integer in [0,65535].'
        self.__port = port
        
    @property
    def ip(self) :
        return self.__ip
        
    @ip.setter
    def ip(self,ip) :
        assert isinstance(ip,str) , "IP should be a string like '127.0.0.1'."
        self.__ip = ip



    def __init__(self,ip='',port=8000) :
        self.ERROR = {}
        self.__initError()
        self.LIST = { 'GET' : {} , 'POST' : {} }
        self.PARAM = { 'GET' : {} , 'POST' : {} }
        self.ip = ip
        self.port = port
        self.httpd = make_server(ip,port,self.route)



    #decorator of GET
    def GET(self,url) :
        def decorator(func) :
            self.LIST['GET'][url] = func
            return func
        return decorator
     
        
        
    #decorator of POST
    def POST(self,url) :
        def decorator(func) :
            self.LIST['POST'][url] = func
            return func
        return decorator



    # return all keys of GET parameters
    def getKeys(self) :
        keys = [key for key in self.PARAM['GET']]
        return keys
        
        
    
    # return all keys of POST parameters    
    def postKeys(self) :
        keys = [key for key in self.PARAM['POST']]
        return keys
    


    # return the value of GET parameter 
    def getParam(self,key) :
        value = self.PARAM['GET'][key] if key in self.PARAM['GET'] else None
        return value



    # return the value of POST paramter
    def postParam(self,key) :
        value = self.PARAM['POST'][key].value if key in self.PARAM['POST'] else None
        return value
        
        
  
    # return the filename     
    def filename(self,key) : 
        filename = self.PARAM['POST'][key].name if key in self.PARAM['POST'] else None
        return filename
    
    
    
    # return a file-like object of uploaded file
    def file(self,key) : 
        fp = self.PARAM['POST'][key].file if key in self.PARAM['POST'] else None
        return fp
    
    
    
    # choice script to run or response a static file
    def route(self,request,response) : 
        method = request['REQUEST_METHOD'].upper()
        url    = request['PATH_INFO']
        
        if method == 'POST' : 
            self.__setPostParam(request)
        elif method == 'GET' :
            self.__setGetParam(request['QUERY_STRING'])
            
        if url in self.LIST[method] :
            return self.LIST[method][url](request,response)
        elif os.path.isfile(url[1:]) :
            return self.__staticFile(url[1:],request,response)
        else :
            return self.ERROR[404](request,response)
     
     
     
    # execute server
    def exec(self) :
        mPort = '# Excute HTTP server on port : ' + str(self.port) + ' #'
        hr = ''.join(['#' for c in mPort])
        print(hr)
        print(mPort)
        print(hr)
        
        self.httpd.serve_forever()
    
    
    
    # initialize GET parameters
    def __setGetParam(self,query_string) : 
        if '&' in query_string :
            form = re.split(r'&',query_string)
            for sub in form :
                if '=' in sub :
                    key,value = re.split(r'=',sub)
                    self.PARAM['GET'][key] = value   
                    
                    
    # initialize POST parameters
    def __setPostParam(self,request) : 
        self.PARAM['POST'] = get_post_form(request)
    '''
        size = int(request.get('CONTENT_LENGTH'))
        data = request['wsgi.input'].read(size).decode()  
        if '&' in data :
            form = re.split(r'&',data)
            for sub in form :
                if '=' in sub :
                    key,value = re.split(r'=',sub)
                    self.PARAM['POST'][key] = value   
    '''   
                
    




    def __staticFile(self,path,request,response) :
    
        fileType = magic.from_file(path, mime=True)
        
        if fileType == 'text/plain' :
            fileType = MimeType(path)
            
        response('200 ok',[('Content-Type',fileType)])
        fp = open(path,'rb')
        data = fp.read()
        fp.close()
        #data = data.encode('utf-8') or data
        
        return [data]
    


    def __initError(self) :
        def error400(request,response) :
            html = [b'''
                     <html>
                     <head><title>400 Bad Request</title></head>
                     <body bgcolor="white">
                     <center><h1>404 Not Found</h1></center>
                     <hr><center>MiniWeb</center>
                     </body>
                     </html>
                     ''']
            response('400 Bad Request',[('Content-Type','text/html')])
            return html
            
        def error403(request,response) :
            html = [b'''
                     <html>
                     <head><title>403 Forbidden</title></head>
                     <body bgcolor="white">
                     <center><h1>404 Not Found</h1></center>
                     <hr><center>MiniWeb</center>
                     </body>
                     </html>
                     ''']
            response('403 Forbidden',[('Content-Type','text/html')])
            return html
    
        def error404(request,response) :
            html = [b'''
                     <html>
                     <head><title>404 Not Found</title></head>
                     <body bgcolor="white">
                     <center><h1>404 Not Found</h1></center>
                     <hr><center>MiniWeb</center>
                     </body>
                     </html>
                     ''']
            response('404 Not Found',[('Content-Type','text/html')])
        
            return html
            
        self.ERROR[400] = error400    
        self.ERROR[403] = error403
        self.ERROR[404] = error404



        
        

############ These code is copied from http://wsgi.readthedocs.io/##############

def is_post_request(environ):
    if environ['REQUEST_METHOD'].upper() != 'POST':
        return False
    content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
    return (content_type.startswith('application/x-www-form-urlencoded' or content_type.startswith('multipart/form-data')))


class InputProcessed(object):
    def read(self, *args):
        raise EOFError('The wsgi.input stream has already been consumed')
    readline = readlines = __iter__ = read


def get_post_form(environ):
    #assert is_post_request(environ)
    input = environ['wsgi.input']
    post_form = environ.get('wsgi.post_form')
    if (post_form is not None
        and post_form[0] is input):
        return post_form[2]
    # This must be done to avoid a bug in cgi.FieldStorage
    environ.setdefault('QUERY_STRING', '')
    fs = cgi.FieldStorage(fp=input,
                          environ=environ)
    new_input = InputProcessed()
    post_form = (new_input, input, fs)
    environ['wsgi.post_form'] = post_form
    environ['wsgi.input'] = new_input
    return fs

################################### END ########################################

if __name__ == '__main__' :
    web = Web()

    @web.GET('/')
    def index(request,response) :
        response('200 ok',[('Content-Type','text/html')])
        html = b'''
                <html>
                <head>
                    <meta charset='utf-8'/>
                    <title>Welcome to MiniWeb</title>
                </head>
                <body>
                    <center><h1>Welcome to MiniWeb</h1></center>
                </body>
                </html>
               '''
        return [html]

    web.exec()

