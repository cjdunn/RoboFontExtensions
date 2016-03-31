from mojo.UI import CurrentSpaceCenter
from mojo.events import addObserver, removeObserver

class disableDragObserver(object):
    
    def __init__(self):
        addObserver(self, 'spaceCenterOpenCallback', 'spaceCenterWillOpen')
        addObserver(self, 'spaceCenterCloseCallback', 'spaceCenterWillClose')
        
    def deactivateModule(self):
        removeObserver(self, 'spaceCenterDidOpen')
        removeObserver(self, 'fontDidOpen')
        print 'disableDrag deactivated'
        
    def spaceCenterOpenCallback(self, info):
        sp = CurrentSpaceCenter()
        sp.disableDrag(True)
        print 'disableDrag activated'
        
    def spaceCenterCloseCallback(self, info):
        self.deactivateModule()
        
    
disableDragObserver()