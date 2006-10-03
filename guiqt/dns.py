# -*- coding: utf-8 -*-

from qt import *
from shared_fnc import *
import _dns

class ccregWindow(_dns.ccregWindow):

    def __init__(self,parent = None,name = None,fl = 0):
        _dns.ccregWindow.__init__(self,parent,name,fl)
        self.addr.horizontalHeader().resizeSection(0,300)
        self._addr_item = None

    def addr_current_changed(self,r,c):
        self._addr_item = table_current_changed(self.addr, r, c)

    def addr_value_changed(self,r,c):
        table_value_changed(self.addr, self._addr_item, r, c)


if __name__ == '__main__':
    app = QApplication([])
    form = ccregWindow()
    form.show()
    app.setMainWidget(form)
    app.exec_loop()