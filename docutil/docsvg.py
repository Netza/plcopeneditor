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

import wx, os, subprocess

def get_inkscape_path():
    """ Return the Inkscape path """
    import _winreg
    svgexepath = _winreg.QueryValue(_winreg.HKEY_LOCAL_MACHINE,
                 'Software\\Classes\\svgfile\\shell\\Inkscape\\command')
    svgexepath = svgexepath.replace('"%1"', '')
    return svgexepath.replace('"', '')

def open_win_svg(svgexepath, svgfile):
    """ Open Inkscape on Windows platform """
    popenargs = [svgexepath]
    if svgfile is not None :
        popenargs.append(svgfile)
    subprocess.Popen(popenargs).pid

def open_lin_svg(svgexepath, svgfile):
    """ Open Inkscape on Linux platform """
    if os.path.isfile("/usr/bin/inkscape"):
        os.system("%s %s &"%(svgexepath , svgfile))
    
def open_svg(svgfile):
    """ Generic function to open SVG file """
    if wx.Platform == '__WXMSW__' :
        svgexepath = get_inkscape_path()
        try:
            open_win_svg(svgexepath , svgfile)
        except:
            wx.MessageBox("Inkscape is not found or installed !")
            return None
    else:
        svgexepath = os.path.join("/usr/bin","inkscape")
        if(os.path.isfile(svgexepath)):
            open_lin_svg(svgexepath, svgfile)
        else:
            wx.MessageBox("Inkscape is not found or installed !")
            return None

