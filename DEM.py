import math
import tkinter as tk
import time
from random import randint
import threading
from math import pow
from tkinter import filedialog
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Point_list = []  #点的列表
Line_list = []   #边的列表
Triangle_list = []  #三角形的列表
file_path = ' ' #存储文件路径
file_text = '' #存储读取文件
name = [] #临时存储点名
id = [] #临时存储id
line_name = []#临时存放边名
arc = [] #临时存放边
Eqpointlists = [] #存放等高线点
Eqline = [] #存放等高线边
Eqline2 = [] #存储光滑的等高线边
zlist = [] #用于存储高程阶梯


# 点类
class Point:
    def __init__(self,id = -2,pointname = ' ',x = 0.0,y = 0.0,z = 0.0):
        self.id = id
        self.PointName = pointname
        self.X = x
        self.Y = y
        self.Z = z
        self.s_plist = []
    def Cal_Distans(self,other):
        return math.sqrt((self.X - other.X)**2+(self.Y - other.Y)**2)
    def __eq__(self, other):
        if(self.id == other.id):
            return 1
        else:
            return 0
# 线类
class Line:
    def __init__(self,point_b = (' ',' ',0,0,0),point_e = (' ',' ',0,0,0)):
        self.BeginPoint = point_b
        self.EndPoint = point_e
        self.Belonging_Triangle = []
        self.id = 0
    def __eq__(self, other):
        if(self.BeginPoint.id == other.EndPoint.id and self.EndPoint.id ==other.BeginPoint.id):
            return 1
        elif(self.BeginPoint.id ==other.BeginPoint.id and self.EndPoint.id == other.EndPoint.id):
            return 1
        else:
            return 0
# 三角形类
class Triangle:
    def __init__(self,point_b,point_e,point_s,id=0):
        self.BaseLine=Line(point_b,point_e)
        self.newLine1=Line(point_b,point_s)
        self.newLine2=Line(point_s,point_e)
        self.point=[point_b,point_e,point_s]
        self.id=id
    def __eq__(self, other):#重载==
        if(self.BaseLine==other.BaseLine and self.newLine1==other.newLine1 and self.newLine2==other.newLine2):
            return 1
        elif(self.BaseLine==other.BaseLine and self.newLine1==other.newLine2 and self.newLine2==other.newLine1):
            return 1
        elif(self.BaseLine==other.newLine1 and self.newLine1==other.newLine2 and self.newLine2==other.BaseLine):
            return 1
        elif(self.BaseLine==other.newLine1 and self.newLine1==other.BaseLine and self.newLine2==other.newLine2):
            return 1
        elif(self.BaseLine==other.newLine2 and self.newLine1==other.newLine1 and self.newLine2==other.BaseLine):
            return 1
        elif(self.BaseLine==other.newLine2 and self.newLine1==other.BaseLine and self.newLine2==other.newLine1):
            return 1
        else:
            return 0

# 数据读取 将数据组织到已经封装的点类 再用列表将所有点线性连接在一起 方便调用
def ReadDataTXT():
    global Point_list
    global file_text
    global file_path
    file_path = filedialog.askopenfilename(title='选择文件', filetypes=[('TXT', '*.txt'), ('All Files', '*')],initialdir='C:/')
    bool = 1
    if file_path is not None:
        with open(file = file_path) as file:
            file_text = file.readlines()
        for f in file_text:
            str = f.rstrip().split(',')
            try:
                new_point = Point(int(str[0]),str[1],float(str[2]),float(str[3]),float(str[4]))
            except (IndexError,ValueError):
                Point_list = []
                bool = 0
                dianwindow()
            else:
                Point_list.append(new_point)
            if bool == 0:
                break
    txt1.set(file_path)

# 查询数据边界
def XYMinMax():
    xmax = 0.00000001
    xmin = 100000000
    ymax = 0.00000001
    ymin = 10000000
    for point in Point_list:
        if (point.X < xmin):
            xmin = point.X
        elif (point.X > xmax):
            xmax = point.X
        if (point.Y < ymin):
            ymin = point.Y
        elif (point.Y > ymax):
            ymax = point.Y
    return xmin, xmax, ymin, ymax

# 点数据坐标转化，使其适应画布大小
def GaussToScreenCor(XYMinMax_List,Gx,Gy):
    dxmax=(XYMinMax_List[1] - XYMinMax_List[0]) * 1.2
    dymax=(XYMinMax_List[3] - XYMinMax_List[2]) * 1.2
    xscale=dxmax/750
    yscale=dymax/600
    Sx=int((Gx-XYMinMax_List[0])/xscale) + dxmax*0.01
    Sy=int((XYMinMax_List[3]-Gy)/yscale) + dymax*0.01
    return Sx,Sy

# 解算右三角形余弦值
def Solve_Triangle_cos(line,p):
    c = line.BeginPoint.Cal_Distans(line.EndPoint)
    b = line.EndPoint.Cal_Distans(p)
    a = line.BeginPoint.Cal_Distans(p)
    cos = (a*a+b*b-c*c)/(2*a*b)
    return cos

# 生成基线
def BaseLine(Point):
    d = 100000000
    index = 0
    for i in Point_list:
        if(i == Point):
            continue
        else:
            if(Point.Cal_Distans(i) < d):
                d = Point.Cal_Distans(i)
                index = i.id
    line = Line(Point,Point_list[int(index)])
    return line,index

# 判断寻找点是否在基线边右侧
def Judge_Right(BaseLine,Point):
    dx = BaseLine.EndPoint.X-BaseLine.BeginPoint.X
    dy = BaseLine.EndPoint.Y-BaseLine.BeginPoint.Y
    d = math.sqrt(dx*dx+dy*dy)
    cos = 0
    sin = 0
    if(d != 0):
        cos = dx/d
        sin = dy/d
    #旋转平移变换 三角形顺时针旋转基线方向与X正轴重合
    y=-(Point.X-BaseLine.BeginPoint.X)*sin+(Point.Y-BaseLine.BeginPoint.Y)*cos
    if(y<0):
        return 1
    else:
        return 0

# 判断边是否添加重复，重复则删除并返回1
def Judge_Line():
    global Line_list
    line = Line_list[-1]
    for i in range(0,len(Line_list)-1):
        if(Line_list[i] == line):
            del Line_list[-1]
            return 1
    return 0

# 判断栈是否添加重复，重复则删除
def Judge_Base(base):
    line = base[-1]
    for i in range(0,len(base)-1):
        if(base[i] == line):
            del base[-1]
            return base
    return base

# 判断三角形是否添加重复，重复则删除
def Judge_Tria():
    global Triangle_list
    t = Triangle_list[-1]
    for i in range(0, len(Triangle_list) - 1):
        if (Triangle_list[i] == t):
            del Triangle_list[-1]
            return 1
    return 0

# 由基线生成三角形
def CreatTria(line):
    cos = 1.0
    index = -1
    s = 0
    for p in Point_list:
        if (p == line.BeginPoint or p == line.EndPoint):
            continue
        elif (Judge_Right(line, p)):
            if(Solve_Triangle_cos(line,p) < cos ):
                s = 0
                cos = Solve_Triangle_cos(line,p)
                index = p.id

        if(s == len(Point_list)):
            index = randint(0, len(Point_list) - 1)
            return index,1
        s = s + 1
    return index,0

# 建立边与三角形间的索引
def EdgeIndexTri():
    global Line_list
    global Triangle_list
    for i in range(0,len(Triangle_list)):
        for j in Line_list:
            if(Triangle_list[i].BaseLine == j):
                j.Belonging_Triangle.append([i, 0])
            if(Triangle_list[i].newLine1 == j):
                j.Belonging_Triangle.append([i, 0])
            if(Triangle_list[i].newLine2 == j):
                j.Belonging_Triangle.append([i, 0])
    for i in range(len(Triangle_list)):
        for j in range(len(Triangle_list)):
            if (i == j):
                continue
            else:
                if (Triangle_list[i].BaseLine == Triangle_list[j].BaseLine or Triangle_list[i].BaseLine == Triangle_list[j].newLine1 or Triangle_list[i].BaseLine == Triangle_list[j].newLine2):
                    Triangle_list[i].BaseLine.Belonging_Triangle.append(Triangle_list[j])
                if (Triangle_list[i].newLine1 == Triangle_list[j].BaseLine or Triangle_list[i].newLine1 == Triangle_list[j].newLine1 or Triangle_list[i].newLine1 == Triangle_list[j].newLine2):
                    Triangle_list[i].newLine1.Belonging_Triangle.append(Triangle_list[j])
                if (Triangle_list[i].newLine2 == Triangle_list[j].BaseLine or Triangle_list[i].newLine2 == Triangle_list[j].newLine1 or Triangle_list[i].newLine2 == Triangle_list[j].newLine2):
                    Triangle_list[i].newLine2.Belonging_Triangle.append(Triangle_list[j])

# 生成TIN三角网

def CreatTIN():
    global Triangle_list
    global Line_list
    global ID
    Triangle_list = []
    Line_list = []
    base_stack = []  #建立一个存放边的栈
    ID = 1  # 设置一个计数器（相当于静态变量）
    beginpoint = randint(0,len(Point_list)-1)
    i1 = Point_list[beginpoint].id
    [l,i2] = BaseLine(Point_list[beginpoint])
    Line_list.append(l)
    Line_list[-1].id = len(Line_list) - 1
    base_stack.append(l)

    while(len(base_stack)):
        sign = 0
        line = base_stack[-1]
        i1 = line.BeginPoint.id
        i2 = line.EndPoint.id
        del base_stack[-1]
        [index,key] = CreatTria(line)
        if(index != -1):
            if(key == 0):
                Line_list.append(Line(Point_list[int(i1)],Point_list[int(index)]))
            if(Judge_Line()):
                sign = sign+1
            if(key == 0):
                Line_list.append(Line(Point_list[int(index)],Point_list[int(i2)]))
            if(Judge_Line()):
                sign = sign+1
            if(sign == 0 ):
                Line_list[-1].id = len(Line_list) - 1
                Line_list[-2].id = len(Line_list) - 2
                base_stack.append(Line_list[-1])
                base_stack = Judge_Base(base_stack)
                base_stack.append(Line_list[-2])
                base_stack = Judge_Base(base_stack)
                Triangle_list.append(Triangle(line.BeginPoint, line.EndPoint, Point_list[int(index)], ID))
                ID = ID + 1
            elif(sign == 1):
                Line_list[-1].id = len(Line_list) - 1
                base_stack.append(Line_list[-1])
                base_stack = Judge_Base(base_stack)
                Triangle_list.append(Triangle(line.BeginPoint, line.EndPoint, Point_list[int(index)], ID))
                ID = ID +1
            elif(sign == 2):
                Triangle_list.append(Triangle(line.BeginPoint, line.EndPoint, Point_list[int(index)], ID))
                ID = ID +1
                Judge_Tria()
    if(len(Line_list) < 2):
        CreatTIN()
        EdgeIndexTri()
        return 0
    EdgeIndexTri()

# 画出数据点
def Draw_Point():
    xyminmax=XYMinMax()
    for point in Point_list:
        gxgy=GaussToScreenCor(xyminmax,point.X,point.Y)
        canvas.create_oval(gxgy[0]-3, gxgy[1]-3, gxgy[0]+3, gxgy[1]+3, fill = 'blue')

# 显示点名
def Name():
    global name
    xyminmax = XYMinMax()
    if (b5['text'] == '显示点名'):
        b5['text'] = '关闭点名'
        if(b4['text'] == '关闭点ID'):
            b4['text'] = '显示点ID'
            for j in range(len(id)):
                old_string = canvas.itemcget(id[j], 'text')
                canvas.itemconfig(id[j], text=' ')
        for point in Point_list:
            gxgy = GaussToScreenCor(xyminmax, point.X, point.Y)
            name.append(canvas.create_text(gxgy[0] + 16, gxgy[1] - 7, text = point.PointName))
    else:
        b5['text'] = '显示点名'
        for j in range(len(name)):
            old_string = canvas.itemcget(name[j], 'text')
            canvas.itemconfig(name[j], text=' ')

#显示边号
def Line_Name():
    global line_name
    xyminmax = XYMinMax()
    if (b8['text'] == '显示边号'):
        b8['text'] = '关闭边号'
        for line in Line_list:
            gxgy = GaussToScreenCor(xyminmax, (line.BeginPoint.X+line.EndPoint.X)/2, (line.BeginPoint.Y+line.EndPoint.Y)/2)
            line_name.append(canvas.create_text(gxgy[0], gxgy[1], text = line.id))
    else:
        b8['text'] = '显示边号'
        for j in range(len(line_name)):
            old_string = canvas.itemcget(line_name[j], 'text')
            canvas.itemconfig(line_name[j], text=' ')

#显示点ID
def ID():
    global name
    xyminmax = XYMinMax()
    if b4['text'] == '显示点ID':
        b4['text'] = '关闭点ID'
        if(b5['text'] == '关闭点名'):
            b5['text'] = '显示点名'
            for j in range(len(name)):
                old_string = canvas.itemcget(name[j], 'text')
                canvas.itemconfig(name[j], text=' ')
        for point in Point_list:
            gxgy = GaussToScreenCor(xyminmax, point.X, point.Y)
            id.append(canvas.create_text(gxgy[0] + 16, gxgy[1] - 7, text = point.id))
    else:
        b4['text'] = '显示点ID'
        for j in range(len(id)):
            old_string = canvas.itemcget(id[j], 'text')
            canvas.itemconfig(id[j], text=' ')

#实现延迟输出TIN
def run_Draw_TIN():
    t = threading.Thread(target = Draw_TIN)
    t.start()

# 画出TIN网
def Draw_TIN():
    global arc
    xyminmax=XYMinMax()
    if b3['text'] == '显示TIN':
        b3['text'] = '关闭TIN'
        for line in Line_list:
            gxgy1 = GaussToScreenCor(xyminmax,line.BeginPoint.X,line.BeginPoint.Y)
            gxgy2 = GaussToScreenCor(xyminmax,line.EndPoint.X,line.EndPoint.Y)
            Line = canvas.create_line(gxgy1[0],gxgy1[1],gxgy2[0],gxgy2[1])
            time.sleep(0.005)
            arc.append(Line)
    else:
        b3['text'] = '显示TIN'
        for j in range(len(arc)):
            canvas.delete(arc[j])

#插值函数
def Interpolation(line,n,i):
    Zmax = Point()
    Zmin = Point()
    if(line.BeginPoint.Z>line.EndPoint.Z):
        Zmax = line.BeginPoint
        Zmin = line.EndPoint
    elif(line.BeginPoint.Z<line.EndPoint.Z):
        Zmin = line.BeginPoint
        Zmax = line.EndPoint
    if (n>Zmin.Z and n<Zmax.Z):
        dy = Zmax.Y-Zmin.Y
        dx = Zmax.X-Zmin.X
        linescale = (n-Zmin.Z)/(Zmax.Z-Zmin.Z)
        x = Zmin.X+linescale*dx
        y = Zmin.Y+linescale*dy
        name = "{0}--{1}".format(n,i)
        eqpoint = Point(-1,name,x,y,n)
        return eqpoint
    else:
        return Point()

# 边界边列表
def BorderTri():
    Border_list = []
    for i in range(0, len(Line_list)):
        if (len(Line_list[i].Belonging_Triangle) == 1):
            Border_list.append(Line_list[i])
    return Border_list

#一个三角形内生成等值线
def Grow_Eq(triangle,line,n):
    edges = [triangle.BaseLine,triangle.newLine1,triangle.newLine2]
    for edge in edges:
        if(edge == line):
            continue
        else:
            point = Interpolation(edge,n,edge.id)
            if(point.id != -2):
                for i in range(0, len(Line_list)):
                    if (Line_list[i] == edge):
                        return i, point
    return -2,-2

#查找等值点 输出等值线序列点
def Equivalent_point(n):
    global Line_list
    for L in Line_list:
        for l in L.Belonging_Triangle:
            l[1] = 0
    eqlinelist = []
    Border_list = BorderTri()
    index = -1
    for i in Border_list:
        point = Interpolation(i,n,i.Belonging_Triangle[0][0])
        if(point.id != -2):
            eqlinelist.append(point)
            q = 0
            for edge in Line_list:
                if(i == edge):
                    Line_list[q].Belonging_Triangle[0][1] = 1
                    index = Line_list[q].id
                    break
                q = q+1
            break
    T_index = Line_list[index].Belonging_Triangle[0][0]
    [index2,point] = Grow_Eq(Triangle_list[T_index],Line_list[index],n)
    if(index2 == -2):
        return []
    eqlinelist.append(point)
    if(Line_list[index2].Belonging_Triangle[0][0] == T_index and Line_list[index2].Belonging_Triangle[0][1] == 0):
        Line_list[index2].Belonging_Triangle[0][1] = 1
        if(len(Line_list[index2].Belonging_Triangle) == 2):
            T_index = Line_list[index2].Belonging_Triangle[1][0]
    elif(Line_list[index2].Belonging_Triangle[1][0] == T_index and Line_list[index2].Belonging_Triangle[1][1] == 0):
        Line_list[index2].Belonging_Triangle[1][1] = 1
        if (len(Line_list[index2].Belonging_Triangle) == 2):
            T_index = Line_list[index2].Belonging_Triangle[0][0]

    while(len(Line_list[index2].Belonging_Triangle) == 2):
        [index2, point] = Grow_Eq(Triangle_list[T_index], Line_list[index2], n)
        eqlinelist.append(point)
        if(len(Line_list[index2].Belonging_Triangle) == 2):
            if (Line_list[index2].Belonging_Triangle[0][0] == T_index and Line_list[index2].Belonging_Triangle[0][1] == 0):
                Line_list[index2].Belonging_Triangle[0][1] = 1
                T_index = Line_list[index2].Belonging_Triangle[1][0]
            elif (Line_list[index2].Belonging_Triangle[1][0] == T_index and Line_list[index2].Belonging_Triangle[1][1] == 0):
                Line_list[index2].Belonging_Triangle[1][1] = 1
                T_index = Line_list[index2].Belonging_Triangle[0][0]
    return eqlinelist

# 全局等高线
def Contour_Line(d):
    global Eqpointlists
    Zmax = -10000.0
    Zmin = 10000.0
    for p in Point_list:
        if(p.Z>Zmax):
            Zmax=p.Z
        if(p.Z<Zmin):
            Zmin=p.Z
    n = Zmin+d
    while(n < Zmax):
        eqlinlist = Equivalent_point(n)
        eqlinlist.append(n)
        Eqpointlists.append(eqlinlist)
        n = n + d
    if(len(Eqpointlists) < int((Zmax - Zmin)/d)):
        Contour_Line(d)

def run_Draw1():
    t = threading.Thread(target = Draw_Equivalent_line1)
    t.start()

def Draw_Equivalent_line1():
    global Eqline
    global Eqline2
    global zlist
    global Eqpointlists
    sign = 0
    if(b7['text'] == '显示等高线'):
        if (b72['text'] == '关闭平滑等高线'):
            Eqpointlists = []
            b72['text'] = '显示平滑等高线'
            for i in range(len(Eqline2)):
                canvas.delete(Eqline2[i])
        color()
        Eqline = []
        b7['text'] = '关闭等高线'
        a = txt2.get()
        try:
            b = float(a)
        except(ValueError):
            b = 50  # 默认等高线间距50m
            denggaowindow()
        Contour_Line(b)
        xyminmax=XYMinMax()
        for eqpointlist in Eqpointlists:
            for i in range(0,len(eqpointlist)-1):
                gxgy1=GaussToScreenCor(xyminmax,eqpointlist[i].X,eqpointlist[i].Y)
                if(eqpointlist[-2].X != eqpointlist[i].X):
                    gxgy2=GaussToScreenCor(xyminmax,eqpointlist[i+1].X,eqpointlist[i+1].Y)
                    Eqline.append(canvas.create_line(gxgy1[0],gxgy1[1],gxgy2[0],gxgy2[1],fill = get_color(eqpointlist[-1])))
                 #   time.sleep(0.3)
            if (sign % 3 == 0):
                g = GaussToScreenCor(xyminmax, eqpointlist[0].X, eqpointlist[0].Y)
                text = Reserve(eqpointlist[-1], 2)
                Eqline.append(canvas.create_text(g[0] + 30, g[1], text=[str(text),'m']))
            sign = sign + 1
        zlist = []
    else:
        Eqpointlists = []
        b7['text'] = '显示等高线'
        for i in range(len(Eqline)):
            canvas.delete(Eqline[i])

def run_Draw2(): #延迟输出
    t = threading.Thread(target = Draw_Equivalent_line2)
    t.start()

def Reserve(x,n): #保留指定有效位,n为位数
    y = 10**n
    x = (int(x*y + 0.5)) / y
    return x


def Draw_Equivalent_line2():  #平滑等高线
    global Eqline
    global Eqline2
    global zlist
    global Eqpointlists
    if(b72['text'] == '显示平滑等高线'):
        if(b7['text'] == '关闭等高线'):
            b7['text'] = '显示等高线'
            Eqpointlists = []
            for i in range(len(Eqline)):
                canvas.delete(Eqline[i])
        color()
        Eqline2 = []
        b72['text'] = '关闭平滑等高线'
        Contour_Line(float(e2.get()))
        xyminmax=XYMinMax()
        x = []
        y = []
        Px = []
        Py = []
        sign = 0
        for eqpointlist in Eqpointlists:
            x.append(eqpointlist[0].X)
            x.append(eqpointlist[0].X)
            y.append(eqpointlist[0].Y)
            y.append(eqpointlist[0].Y)
            for i in range(len(eqpointlist)-1):
                x.append(eqpointlist[i].X)
                y.append(eqpointlist[i].Y)
            x.append(eqpointlist[-2].X)
            x.append(eqpointlist[-2].X)
            y.append(eqpointlist[-2].Y)
            y.append(eqpointlist[-2].Y)
            Px.append(x[0])
            Py.append(y[0])
            Range = []
            t = 0
            for i in range(0,10):
                t = t + 0.1
                Range.append(t)

            for i in range(1, len(x)-4):
                for t in Range:
                    Px.append((pow(1 - t, 3) * x[i] + (3 * pow(t, 3) - 6 * pow(t, 2) + 4) * x[i + 1] + (-3 * pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1) * x[i + 2] + pow(t, 3) * x[i + 3]) / 6)
                    Py.append((pow(1 - t, 3) * y[i] + (3 * pow(t, 3) - 6 * pow(t, 2) + 4) * y[i + 1] + (-3 * pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1) * y[i + 2] + pow(t, 3) * y[i + 3]) / 6)

            Px.append(x[-1])
            Py.append(y[-1])
            for i in range(0, len(Px)):
                gxgy1 = GaussToScreenCor(xyminmax, Px[i], Py[i])

                if (Px[-1] != Px[i]):
                    gxgy2 = GaussToScreenCor(xyminmax, Px[i + 1], Py[i + 1])
                    Eqline2.append(canvas.create_line(gxgy1[0], gxgy1[1], gxgy2[0], gxgy2[1], fill=get_color(eqpointlist[-1])))

            if(sign%3 == 0):
                g = GaussToScreenCor(xyminmax, eqpointlist[0].X, eqpointlist[0].Y)
                text = Reserve(eqpointlist[-1], 2)
                Eqline2.append(canvas.create_text(g[0] + 30, g[1] , text = [str(text),'m']))
            x = []
            y = []
            Px = []
            Py = []
            sign = sign+1
        zlist = []

    else:
        Eqpointlists = []
        b72['text'] = '显示平滑等高线'
        for i in range(len(Eqline2)):
            canvas.delete(Eqline2[i])

def Draw_eqPoint():
    xyminmax=XYMinMax()
    for point1 in Eqpointlists:
        for point2 in point1:
            gxgy=GaussToScreenCor(xyminmax,point2.X,point2.Y)
            oval = canvas.create_oval(gxgy[0]-1.7, gxgy[1]-1.7, gxgy[0]+1.7, gxgy[1]+1.7)


'----------颜色部分----------------'

def color():
    global zlist
    Zmax = -10000.0
    Zmin = 10000.0

    for p in Point_list:
        if (p.Z > Zmax):
            Zmax = p.Z
        if (p.Z < Zmin):
            Zmin = p.Z
    dz = Zmax - Zmin
    d =dz/7
    zlist.append(Zmin)
    for i in range(0,6):
        Zmin = Zmin+d
        zlist.append(Zmin)
    zlist.append(Zmax)

def get_color(h):
    color1 = ['#3b38ff', '#5c2fe6', '#7c25cc', '#9d1cb3', '#be1399', '#de0980', '#ff0066','#ff0019']
    color2 = [ '#8838ff', '#9c2fd9', '#b025b2', '#c41c8c', '#d71366', '#eb093f', '#ff0019']
    for i in range(len(zlist)-1):
        if(h>zlist[i] and h<=zlist[i+1]):
            return color2[i]


'-----------查询部分--------------'
#查找一条线的起点ID
def Search_beginID():
    for l in Line_list:
        if(l.id == int(ent1.get())):
            txt7.set(l.BeginPoint.id)
            return 0
    txt7.set('无此边！')

#查找一个三角形的邻接三角形中第三点ID
def Search_ThridPoint():
    p_list = []
    for t in Triangle_list:
        if(t.id == int(ent2.get())):
            a = t.BaseLine
            b = t.newLine1
            c = t.newLine2
            line_list = [a,b,c]
            for j in line_list:
                if(len(j.Belonging_Triangle)==1):
                    if(t == j.Belonging_Triangle[0]):
                        continue
                    else:
                        t2 = j.Belonging_Triangle[0]
                        for i in t2.point:
                            if (i == j.BeginPoint or i == j.EndPoint):
                                continue
                            else:
                                p_list.append(i.id)
                                break
                if(len(p_list)==3):
                    txt8.set(p_list)
                    return 0
    txt8.set('无此三角形！')

#查询边界边
def Search_Border():
    list = BorderTri()
    l = []
    for i in list:
        l.append(i.id)
    txt9.set(l)









'------------3DTIN部分----------------'

def zhu():
    global Point_list
    global Line_list
    global Eqpointlists
    fig = plt.figure()
    ax = Axes3D(fig)
    X = []
    Y = []
    Z = []
    for i in range(len(Point_list)):
        X.append(Point_list[i].X)
        Y.append(Point_list[i].Y)
        Z.append(Point_list[i].Z)
    ax.scatter3D(X, Y, Z)
    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.axes.zaxis.set_ticklabels([])
    for i in range(len(Line_list)):
        xx = [Line_list[i].BeginPoint.X,Line_list[i].EndPoint.X]
        yy = [Line_list[i].BeginPoint.Y,Line_list[i].EndPoint.Y]
        zz = [Line_list[i].BeginPoint.Z,Line_list[i].EndPoint.Z]
        ax.plot(xx,yy,zz,color = 'green',linewidth= 0.5)

    color()
    x = []
    y = []
    z = []
    Px = []
    Py = []
    Pz = []
    sign = 0
    for eqpointlist in Eqpointlists:
        x.append(eqpointlist[0].X)
        x.append(eqpointlist[0].X)
        y.append(eqpointlist[0].Y)
        y.append(eqpointlist[0].Y)
        z.append(eqpointlist[0].Z)
        z.append(eqpointlist[0].Z)
        for i in range(len(eqpointlist) - 1):
            x.append(eqpointlist[i].X)
            y.append(eqpointlist[i].Y)
            z.append(eqpointlist[i].Z)
        x.append(eqpointlist[-2].X)
        x.append(eqpointlist[-2].X)
        y.append(eqpointlist[-2].Y)
        y.append(eqpointlist[-2].Y)
        z.append(eqpointlist[-2].Z)
        z.append(eqpointlist[-2].Z)
        Px.append(x[0])
        Py.append(y[0])
        Pz.append(z[0])
        Range = []
        d = 0
        for i in range(0, 10):
            d = d + 0.1
            Range.append(d)

        for i in range(1, len(x) - 4):
            for t in Range:
                Px.append((pow(1 - t, 3) * x[i] + (3 * pow(t, 3) - 6 * pow(t, 2) + 4) * x[i + 1] + (
                -3 * pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1) * x[i + 2] + pow(t, 3) * x[i + 3]) / 6)
                Py.append((pow(1 - t, 3) * y[i] + (3 * pow(t, 3) - 6 * pow(t, 2) + 4) * y[i + 1] + (
                -3 * pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1) * y[i + 2] + pow(t, 3) * y[i + 3]) / 6)
                Pz.append((pow(1 - t, 3) * z[i] + (3 * pow(t, 3) - 6 * pow(t, 2) + 4) * z[i + 1] + (
                -3 * pow(t, 3) + 3 * pow(t, 2) + 3 * t + 1) * z[i + 2] + pow(t, 3) * z[i + 3]) / 6)
        Px.append(x[-1])
        Py.append(y[-1])
        Pz.append(z[-1])
        for i in range(len(Px)-1):
            xx = [Px[i], Px[i+1]]
            yy = [Py[i], Py[i+1]]
            zz = [Pz[i], Pz[i+1]]
            ax.plot(xx, yy, zz, color=get_color(zz[0]), linewidth=0.7)
        x = []
        y = []
        z = []
        Px = []
        Py = []
        Pz = []
        sign = sign + 1
    plt.show()


'------------3D规则网格DEM部分----------------'


New_plist = [] #存放网格点

def Creat_DEM_point(d):
    global New_plist
    [xmin, xmax, ymin, ymax] = XYMinMax()
    dx = xmax - xmin
    dy = ymax - ymin
    nx = int(dx/d)
    ny = int(dy/d)
    x = xmin
    y = ymin
    ylist = []
    for i in range(nx):
        for j in range(ny):
            ylist.append(Point(-1,'{}-{}'.format(i,j),x,y,0))
            y = y+d
        y = ymin
        x = x+d
        New_plist.append(ylist)
        ylist = []
    for i in New_plist:
        for i2 in i:
            for j in Point_list:
                if(i2.Cal_Distans(j)<1400):
                    i2.s_plist.append(j.id)
                    if(len(i2.s_plist) > 6):
                        break
    sum1 = 0
    sum2 = 0
    for i in New_plist:
        for i2 in i:
            for j in i2.s_plist:
                s = i2.Cal_Distans(Point_list[j])
                sum1 = sum1 + Point_list[j].Z/s
                sum2 = sum2 + 1/s
            if(sum2 == 0):
                i2.Z = 0
            else:
                i2.Z = sum1/sum2
            sum1 = 0
            sum2 = 0


def Creat_DEM():
    global New_plist
    color()
    fig = plt.figure()
    ax = Axes3D(fig)
    plt.xlabel('x')
    plt.ylabel('y')
    X=[]
    Y=[]
    Z=[]
    for i in New_plist:
        for i2 in range(len(i)-1):
            if (i[i2].Z != 0 and i[i2+1].Z != 0):
                ax.plot([i[i2].X, i[i2+1].X], [i[i2].Y, i[i2+1].Y], [i[i2].Z, i[i2+1].Z], color=get_color((i[i2].Z+i[i2+1].Z)/2))
    for i in range(len(New_plist[0])):
        for i2 in range(len(New_plist)-1):
            if (New_plist[i2][i].Z != 0 and New_plist[i2+1][i].Z != 0):
                ax.plot([New_plist[i2][i].X, New_plist[i2+1][i].X], [New_plist[i2][i].Y, New_plist[i2+1][i].Y], [New_plist[i2][i].Z, New_plist[i2+1][i].Z], color=get_color((New_plist[i2][i].Z + New_plist[i2+1][i].Z)/2))
    New_plist = []
    plt.show()

def Run_DEM():
    a = float(e1.get())
    print(a)
    Creat_DEM_point(a)
    Creat_DEM()


'--------鲁棒性---------'
def denggaowindow():
    window = tk.Tk()
    window.geometry('250x100')
    window.title("发生错误")
    label = tk.Label(window, font=('楷书', 15), width=18, bd=3, text='您未输入等高线间距').place(x=25, y=15)
    labe2 = tk.Label(window, font=('楷书', 15), width=18, bd=3, text='则默认间距50m').place(x=25, y=45)
    window.mainloop()

def dianwindow():
    window = tk.Tk()
    window.geometry('300x100')
    window.title("发生错误")
    label = tk.Label(window, font=('楷书', 15), width=18, bd=3, text='点数据文件缺失数据').place(x=25, y=15)
    labe2 = tk.Label(window, font=('楷书', 15), width=25, bd=3, text='或者文件未按特定格式存储').place(x=25, y=45)
    window.mainloop()


window = tk.Tk()
window.title('DEM')
window.geometry('1100x800')


# 在窗体上生成一块画布 用于绘制导线图
canvas = tk.Canvas(window, width=750, height=600, bg='white')
canvas.place(x=280, y=150)
canvas2 = tk.Canvas(window, width=280, height=800, bg='lightcyan')
canvas2.place(x=0, y=0)
txt1 = tk.StringVar()
txt2 = tk.StringVar()
txt3 = tk.StringVar(0,200)
txt4 = tk.StringVar()
txt5 = tk.StringVar()
txt6 = tk.StringVar()
txt7 = tk.StringVar()
txt8 = tk.StringVar()
txt9 = tk.StringVar()
ent1 = 0
ent2 = 0
ent3 = 0

def create():
    global ent1
    global ent2
    global ent3
    top = tk.Toplevel()
    top.geometry('500x300')
    top.title('查询')

    label1 = tk.Label(top, font=('楷书', 10), width=8, bd=3, text='编号:',bg='white' ).place(x=30, y=60)
    label1 = tk.Label(top, font=('楷书', 10), width=8, bd=3, text='三角形:', bg='white').place(x=30, y=140)

    label1 = tk.Label(top, font=('楷书', 10),  text='通过边号查询起点ID').place(x=30, y=30)
    label1 = tk.Label(top, font=('楷书', 10),  text='查询三角形邻接三角形的第三个点ID').place(x=30, y=110)
    label1 = tk.Label(top, font=('楷书', 10),  text='查询边界边').place(x=30, y=190)

    label1 = tk.Label(top, font=('楷书', 10), width=8, bd=3, text='起点ID' ).place(x=230, y=60)
    label1 = tk.Label(top, font=('楷书', 10), width=8, bd=3, text='第三个点ID').place(x=230, y=140)
    label1 = tk.Label(top, font=('楷书', 10), width=8, bd=3, text='边界边').place(x=100, y=220)


    a1 = tk.Button(top, text='查询', font=('楷书', 10), command = Search_beginID)
    a1.place(x=180, y=60)
    a2 = tk.Button(top, text='查询', font=('楷书', 10), command = Search_ThridPoint)
    a2.place(x=180, y=140)
    a3 = tk.Button(top, text='查询', font=('楷书', 10), command = Search_Border)
    a3.place(x=50, y=220)

    ent1 = tk.Entry(top, font=('楷书', 10), width=8, bd=3, textvariable=txt4)
    ent1.place(x=90, y=60)
    ent2 = tk.Entry(top, font=('楷书', 10), width=8, bd=3, textvariable=txt5)
    ent2.place(x=90, y=140)


    ent4 = tk.Entry(top, font=('楷书', 10), width=16, bd=3, textvariable=txt7)
    ent4.place(x=300, y=60)
    ent5 = tk.Entry(top, font=('楷书', 10), width=16, bd=3, textvariable=txt8)
    ent5.place(x=300, y=140)
    ent6 = tk.Entry(top, font=('楷书', 10), width=32, bd=3, textvariable=txt9)
    ent6.place(x=160, y=220)



b15 = tk.Button(window, text='查询', font=('楷书',18),command=create,bg='white')
b15.place(x=30, y=640)

e1 = 0
def create2():
    global txt3
    global e1
    top = tk.Tk()
    top.geometry('500x200')
    top.title('3D规则网格')
    label1 = tk.Label(top, font=('楷书', 15), width=13, bd=3, text='输入分辨率：', bg='white').place(x=30, y=60)
    e1 = tk.Entry(top,font=('楷书', 15), width=8, bd=3, textvariable=txt3)
    e1.place(x=180, y=60)
    a1 = tk.Button(top, text='生成', font=('楷书', 15),command = Run_DEM)
    a1.place(x=290, y=60)


e1 = tk.Entry(window, font=('楷书', 17), width=30, bd=5, textvariable=txt1).place(x=460, y=35)
e2 = tk.Entry(window, font=('楷书', 17), width=5, bd=3, textvariable=txt2)
e2.place(x=460,y=90)
label1 = tk.Label(window, font=('楷书', 17), width=13, bd=3, text='等高线间距(m):',bg='white').place(x=290,y=90)
b1 = tk.Button(window, text='选择点数据', font=('楷书', 18), command=ReadDataTXT,bg='white').place(x=290, y=30)
b2 = tk.Button(window, text='生成点', font=('楷书', 18), command=Draw_Point,bg='white').place(x=860, y=30)
b3 = tk.Button(window, text='显示TIN', font=('楷书', 18), command=run_Draw_TIN,bg='white')
b3.place(x=30, y=290)
b4 = tk.Button(window, text='显示点ID', font=('楷书', 18), command=ID,bg='white')
b4.place(x=30, y=80)
b5 = tk.Button(window, text='显示点名', font=('楷书', 18), command=Name,bg='white')
b5.place(x=30, y=150)
b6 = tk.Button(window, text='创建TIN', font=('楷书', 18,), command=CreatTIN,bg='white')
b6.place(x=860, y=80)
b7 = tk.Button(window, text='显示等高线', font=('楷书', 18), command=run_Draw1,bg='white')
b7.place(x=30, y=360)
b8 = tk.Button(window, text='显示边号', font=('楷书', 18), command=Line_Name,bg='white')
b8.place(x=30,y=220)
b9 = tk.Button(window, text='显示3D TIN', font=('楷书', 18),bg='white',command = zhu)
b9.place(x=30,y=500)
b9 = tk.Button(window, text='显示3D规则网格', font=('楷书', 18), command=create2,bg='white')
b9.place(x=30,y=570)
b72 = tk.Button(window, text='显示平滑等高线', font=('楷书', 18),bg='white', command=run_Draw2)
b72.place(x=30, y=430)

window.mainloop()


