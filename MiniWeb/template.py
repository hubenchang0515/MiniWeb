#! /usr/bin/env python3

import re 

class Template(object) :

    def openHtml(self,path) :
        fp = open(path, 'r')
        self.__html = fp.read()
        fp.close
        
    def render(self,**cmd) :
        for key in cmd :
            name = re.compile(r'<%\s*' + key + r'\s*%>')
            self.__html , n = name.subn(cmd[key],self.__html)
            
    def html(self) :
        return [self.__html.encode('utf-8')]

    
if __name__ == '__main__' : 
    t = Template()
    t.openHtml('index.html')
    t.render(name = 'Hello World')
    
    print(t.html())
