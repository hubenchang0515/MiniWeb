#! /usr/bin/env python3

import MiniWeb
import cgi


web = MiniWeb.Web()
template = MiniWeb.Template()


@web.GET('/')
def index(request,response) :
    response('200 ok',[('Content-Type','text/html')])
    template.openHtml('demo.html')
    template.render(username = '')
    return template.html()
    
@web.POST('/')
def index(request,response) :
    response('200 ok',[('Content-Type','text/html')])    
    username = web.postParam('username')
    template.openHtml('demo.html')
    template.render( username = '<center><h1>' + username + '</h1></center>' )
    return template.html()
    
web.exec()
