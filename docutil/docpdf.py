#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This file is part of PLCOpenEditor, a library implementing an IEC 61131-3 editor
#based on the plcopen standard. 
#
#Copyright (C) 2007: Edouard TISSERANT and Laurent BESSARD
#
#See COPYING file for copyrights details.
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#General Public License for more details.
#
#You should have received a copy of the GNU General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import wx, os

readerexepath = None
    
def get_acroversion():
    " Return version of Adobe Acrobat executable or None"
    import _winreg
    adobesoft = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'Software\Adobe')
    for index in range(_winreg.QueryInfoKey(adobesoft)[0]):
        key = _winreg.EnumKey(adobesoft, index)
        if "acrobat" in key.lower():
            acrokey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Adobe\\%s' % key)
            for index in range(_winreg.QueryInfoKey(acrokey)[0]):
                numver = _winreg.EnumKey(acrokey, index)
                try:
                    res = _winreg.QueryValue(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Adobe\\%s\\%s\\InstallPath' % (key, numver))
                    return res
                except:
                    pass
    return None

def open_win_pdf(readerexepath, pdffile, pagenum = None):
    if pagenum != None :
        os.spawnl(os.P_DETACH, readerexepath, "AcroRd32.exe", "/A", "page=%d=OpenActions" % pagenum, '"%s"'%pdffile)
    else:
        os.spawnl(os.P_DETACH, readerexepath, "AcroRd32.exe", '"%s"'%pdffile)

def open_lin_pdf(readerexepath, pdffile, pagenum = None):
    if pagenum == None :
        os.system("%s -remote DS301 %s &"%(readerexepath, pdffile))
    else:
    	print "Open pdf %s at page %d"%(pdffile, pagenum)
        os.system("%s -remote DS301 %s %d &"%(readerexepath, pdffile, pagenum))

def open_pdf(pdffile, pagenum = None):
    if wx.Platform == '__WXMSW__' :
        try:
            readerpath = get_acroversion()
        except:
            wx.MessageBox("Acrobat Reader is not found or installed !")
            return None
        
        readerexepath = os.path.join(readerpath, "AcroRd32.exe")
        if(os.path.isfile(readerexepath)):
            open_win_pdf(readerexepath, pdffile, pagenum)
        else:
            return None
    else:
        readerexepath = os.path.join("/usr/bin","xpdf")
        if(os.path.isfile(readerexepath)):
            open_lin_pdf(readerexepath, pdffile, pagenum)
        else:
            wx.MessageBox("xpdf is not found or installed !")
            return None
