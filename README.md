# MiniWeb
A simple Web Server Framework based on WSGI.  

# class Web(pi = "" , port = 8000)
Class of web server,default port is 8000.
```
# create a server listen to 2333 port
web  = Web(port=2333)
```
## GET(self,url)
Decorator to bind url and function in GET method.  
```
# call index() while visit '/' by GET metohd
@web.GET('/')
def index(request,response) :
    pass
```
## POST(self,url)
Decorator to bind url and function in POST method.  
```
# call login() while visit '/login' by POST method
@web.POST('/login')
def login(request,response) :
    pass
```
## getKeys(self)
return all keys(form name) of GET parameters.  
```
# get keys list of GET
keys = web.getKeys()
```
## postKeys(self)
return all keys(form name) of POST parameters.  
```
# get key list of POST
keys = web.postKeys()
```
## getParam(self,key)
return the value of GET parameter index by key(form name).  
```
# get value of GET
id = web.getParam('id')
```
## postParam(self,key)
return the value of POST parameter index by key(form name).  
```
# get value of POST
username = web.postParam('username')
```
## filename(self,key)
return the filename of POST upload index by key(form name).
```
# get file name of POST
filename = web.filename('picture')
```  
## file(self,key)
return a file-like object of POST upload index by key(form name).
```
# get file of POST
file = web.file('picture')
```  
## exec(self)
execute server.
```
web.exec()
```

# class Template()
Class of template, template variable in HTML file is <% name %>.
```
# create a Template to render HTML
template = Template()
```
## openHtml(self,path)
read a HTML file  
```
# open a HTML file
template.openHtml('index.html')
```
## render(self,**cmd)
render the HTML data  
```
# change <% value %> to Welcome
template.render(value =  'Welcome')
```
## html(self)
return the rendered HTML data
```
html = template.html()
```


# Example
## HTML file index.html
```
<html>
    <head>
        <meta charset='utf-8'/>
        <title><% title %></title>
    </head>
    <body>
        <p><% article %></p>
    </body>
</html>
```
## Python file
```
#! /usr/bin/env python3
import MiniWeb

web = MiniWeb.Web() # create web server,listen to default port 8000

@web.GET('/')
def index(request,response) :
    t = MiniWeb.Template()
    response('200 ok',[('Content-Type','text/html')])
    t.openHtml('index.html')
    t.render(title = 'Home Page')
    t.render(article = 'Welcome')
    return t.html()
    
web.exec()
```
Visit localhost:8000 in broswer.  
![](https://github.com/hubenchang0515/MiniWeb/blob/master/readme.png?raw=true)
