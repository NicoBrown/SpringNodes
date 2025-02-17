#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System
from System.Drawing import Point, Font, Color
from System.Windows.Forms import *
from System import Array, Object
from System.Threading import Thread, ThreadStart

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

def hasInd(l1, i):
	try: l1[i] ; return True
	except: return False

class NameWrap(Object):
	def __init__(self, obj1, name1 = None):
		self.obj = obj1
		if obj1 == None: name1 = "null"
		if name1 == None and obj1 != None: name1 = obj1.ToString()
		self.name = name1
	def ToString(self):
		return self.name

class DragDrop(Form):
	def __init__(self, cm1):
		self.Text = "SpringNodes: Drag and Drop Reorder"
		self.Width = 367
		self.Height = n + 110
		self.ControlBox = False
		self.TopMost = True
		self.BackColor = Color.FromArgb(40,40,40)
		self.FormBorderStyle = FormBorderStyle.FixedDialog
		self.StartPosition = FormStartPosition.CenterScreen
		self.FormClosing += self.DisableForceClose
		self.SafeToClose = False
		
		self.label = Label()
		self.label.Text = cm1
		self.label.Location = Point(5, 5)
		self.label.ForeColor = Color.FromArgb(234,234,234)
		self.label.Font = Font("Calibri", 10)
		self.label.AutoSize = True
		self.Controls.Add(self.label)
		
		self.box1 = ListBox()
		self.box1.Location = Point(5,32)
		self.box1.Width = 350
		self.box1.Height = n
		self.box1.HorizontalScrollBar = True
		self.box1.BackColor = Color.FromArgb(53,53,53)
		self.box1.ForeColor = Color.FromArgb(234,234,234)
		self.box1.Font = Font("Calibri", 11)
		self.box1.BorderStyle = BorderStyle.None
		self.box1.AllowDrop = True
		self.box1.MouseDown += self.Drag1
		self.box1.DragOver += self.Over1
		self.box1.DragDrop += self.Drop1
		self.Controls.Add(self.box1)

		self.button1 = Button()
		self.button1.Text = 'Save Order'
		self.button1.AutoSize = True
		self.button1.Width = 200
		self.button1.ForeColor = Color.FromArgb(234,234,234)
		self.button1.Font = Font("Calibri", 10)
		self.button1.Location = Point(80, n + 35)
		self.button1.Click += self.save
		self.Controls.Add(self.button1)
	
	def add_range(self,l1):
		self.box1.Items.AddRange(l1)
	def save(self, sender, event):
		self.output1 = self.box1.Items
		self.SafeToClose = True
		self.Close()
	def Drag1(self, sender, event):
		if self.box1.SelectedItem == None : pass
		else:
			self.type1 = self.box1.SelectedItem.GetType()
			self.box1.DoDragDrop(self.box1.SelectedItem, DragDropEffects.Move)
	def Over1(self, sender, event):
		event.Effect = DragDropEffects.Move
	def Drop1(self, sender, event):
		pt1 = self.box1.PointToClient(Point(event.X, event.Y))
		ind1 = self.box1.IndexFromPoint(pt1)
		if ind1 < 0 : ind1 = self.box1.Items.Count - 1
		data1 = event.Data.GetData(self.type1)
		self.box1.Items.Remove(data1)
		self.box1.Items.Insert(ind1, data1)
	def DisableForceClose(self, sender, event):
		if not self.SafeToClose : event.Cancel = True
		else: pass

def EnableDrop():
	def thread_proc():
		form = DragDrop(IN[2])
		form.add_range(l1_arr)
		Application.Run(form)
		global out1 
		out1 = form.output1
		Application.Exit()
	t1 = Thread(ThreadStart(thread_proc))
	t1.ApartmentState = System.Threading.ApartmentState.STA
	t1.Start()
	t1.Join()

if IN[0] == None: l1 = []
else: l1 = tolist(IN[0])
if IN[1] == None: names = None
else: names = tolist(IN[1])

n = 22 * len(l1) + 5
if not l1: n = 27
if n > 700 : n = 700
for i in xrange(len(l1)):
	name1 = None
	if hasInd(names, i): name1 = names[i]
	l1[i] = NameWrap(l1[i], name1)
l1_arr = Array[Object](l1)
out1 = None
EnableDrop()
OUT = [i.obj for i in out1]