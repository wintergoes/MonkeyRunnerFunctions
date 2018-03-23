#coding:utf-8

'''
************************************************************************************************************************
*
*	Created By: liuderu
*	Email: wintergoes@163.com
*	Description: Functions for test android apps with MonkeyRunner
*
************************************************************************************************************************
'''

from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice 
from com.android.monkeyrunner.easy import By

class Point:
	def __init__(self,x_init,y_init):
		self.x = x_init
		self.y = y_init
		
	def __str__(self):
		return str(self.x) + ", " + str(self.y)
		
class ViewRect:
	def __init__(self,x_init,y_init, width_init, height_init):
		self.x = x_init
		self.y = y_init
		self.width = width_init
		self.height = height_init
		
	def __str__(self):
		return str(self.x) + ", " + str(self.y)		

def log(logstr):
    print logstr

def isViewExist(device, viewid):
	hierachy_view = device.getHierarchyViewer()
	view_node = hierachy_view.findViewById('id/' + viewid)
	if view_node==None:
		return False
	else:
		return True

def safeTouch(easydevice, viewid, touchtype, maxtrycount):
	if viewid.startswith('id/'):
		log('viewid starts with "id/", please correct it...')
		
	trycount = 0
	while True:
		try:
			easydevice.touch(By.id('id/' + viewid),MonkeyDevice.DOWN_AND_UP)	
			break
		except:
			print "Failed to touch " + viewid + " " + str(trycount) + " times"
			trycount=trycount+1
			MonkeyRunner.sleep(1.0)
			
		if trycount >= maxtrycount:
			break

# 			
def safeType(easydevice, viewid, typevalue, maxtrycount):
	if viewid.startswith('id/'):
		log('viewid starts with "id/", please correct it...')

	trycount = 0
	while True:
		try:
			easydevice.type(By.id('id/' + viewid), typevalue)	
			break
		except:
			print "Failed to type " + viewid + ", value: " + typevalue + ", " + str(trycount) + " times"
			trycount=trycount+1
			MonkeyRunner.sleep(1.0)
			
		if trycount >= maxtrycount:
			break	
	
def clickTopLeft(device, viewid):
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + viewid)
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    device.touch(viewpoint.x + 5, viewpoint.y + 5, MonkeyDevice.DOWN_AND_UP)
	
def longClickTopLeft(device, viewid):
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + viewid)
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    device.touch(viewpoint.x + 5, viewpoint.y + 5, MonkeyDevice.DOWN)	
    MonkeyRunner.sleep(2.0)
    device.touch(viewpoint.x + 5, viewpoint.y + 5, MonkeyDevice.UP)	
	
#获取View的左上、右下角的坐标值	
def getViewRect(device, viewid):
	hierachy_view = device.getHierarchyViewer()
	view_node = hierachy_view.findViewById('id/' + viewid)
	viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
	centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
	width=(centerpoint.x - viewpoint.x) * 2
	height=(centerpoint.y - viewpoint.y) * 2
	r = ViewRect(viewpoint.x, viewpoint.y, viewpoint.x + width, viewpoint.y + height)
	return r
	
def getDialogPos(device, dlg_root_view_id):
    displaywidth=device.getProperty("display.width")
    displayheight=device.getProperty("display.height")
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + dlg_root_view_id)	
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)	
    width=(centerpoint.x - viewpoint.x) * 2
    height=(centerpoint.y - viewpoint.y) * 2
    dlgpos = Point(int((int(displaywidth) - width) / 2), int((int(displayheight) - height) / 2))
    return dlgpos
	
def clickViewOnDlg(device, dlg_root_view_id, viewid):
	dlgpos = getDialogPos(device, dlg_root_view_id)
	hierachy_view = device.getHierarchyViewer()
	view_node = hierachy_view.findViewById('id/' + viewid)
	if view_node == None:
		log('clickViewOnDlg did not find view')
		return
	centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)	
	print centerpoint
	device.touch(dlgpos.x + centerpoint.x, dlgpos.y + centerpoint.y, MonkeyDevice.DOWN_AND_UP)
	
def getViewText(device, viewid):
	hierachy_view = device.getHierarchyViewer()
	view_node = hierachy_view.findViewById('id/' + viewid)
	if view_node == None:
		return "View IS NOT EXIST"
	else:
		return hierachy_view.getText(view_node)
	
#横纵向按比例点击某个位置，xpos、ypos为小于1的小数	
def clickRelativePos(device, viewid, xpos, ypos):	
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + viewid)
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
    height=(centerpoint.y - viewpoint.y) * 2
    width=(centerpoint.x - viewpoint.x) * 2
    print viewpoint.x + int(xpos * width)
    print viewpoint.y + int(ypos * height)
    device.touch(viewpoint.x + int(xpos * width), viewpoint.y + int(ypos * height), MonkeyDevice.DOWN_AND_UP)

#横纵向按比例点击某个位置，xpos、ypos为小于1的小数	
def clickRelativePosWithOffset(device, viewid, xpos, ypos, xoffset, yoffset):	
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + viewid)
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
    height=(centerpoint.y - viewpoint.y) * 2
    width=(centerpoint.x - viewpoint.x) * 2
    device.touch(viewpoint.x + int(xpos * width) + xoffset, viewpoint.y + int(ypos * height) + yoffset, MonkeyDevice.DOWN_AND_UP)	

#向左滑动
def dragLeft(device, viewid, interval):
	hierachy_view = device.getHierarchyViewer()
	view_node = hierachy_view.findViewById('id/' + viewid)
	viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
	centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
	width=(centerpoint.x - viewpoint.x) * 2
	device.drag((viewpoint.x + width - 10, centerpoint.y), (viewpoint.x + 10, centerpoint.y), interval, 10)
	MonkeyRunner.sleep(0.2)
	
#向右滑动
def dragRight(device, viewid, interval):
	hierachy_view = device.getHierarchyViewer()
	view_node = hierachy_view.findViewById('id/' + viewid)
	viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
	centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
	width=(centerpoint.x - viewpoint.x) * 2
	device.drag((viewpoint.x + 10, centerpoint.y), (viewpoint.x + width - 10, centerpoint.y), interval, 10)
	MonkeyRunner.sleep(0.2)	

#向上滑动
def dragTop(device, viewid, interval):
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + viewid)
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
    height=(centerpoint.y - viewpoint.y) * 2
    device.drag((viewpoint.x, viewpoint.y + height - 10), (viewpoint.x, viewpoint.y + 10), interval, 10)
    MonkeyRunner.sleep(0.2)

#向下滑动
def dragBottom(device, viewid, interval):
    hierachy_view = device.getHierarchyViewer()
    view_node = hierachy_view.findViewById('id/' + viewid)
    viewpoint = hierachy_view.getAbsolutePositionOfView(view_node)
    centerpoint = hierachy_view.getAbsoluteCenterOfView(view_node)
    height=(centerpoint.y - viewpoint.y) * 2
    device.drag((viewpoint.x, viewpoint.y + 10), (viewpoint.x, viewpoint.y + height - 10), interval, 10)
    MonkeyRunner.sleep(0.2)
