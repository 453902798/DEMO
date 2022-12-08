# -*- coding: mbcs -*-
import math
from abaqus import *
from abaqusConstants import *
from caeModules import *
import csv
import os

##############################################################################
#####说明：本程序为通过在.csv文件中设置参数，批量完成建模、接触、边界等设置，最终完成批量前处理
##############################################################################

os.chdir(r"D:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/2ball")#修改工作目录，用于最后保存odb文件
filePath = "DD:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/2ball/"#cvs文件路径
fr = open(filePath+"graduatedesign_2_3.csv",'r')#csv文件名
reader = csv.reader(fr)
paralist=list(reader)
PARALISTindex=range(len(paralist)-2)
mdb.models.changeKey(fromName='Model-1', toName='Model-0')
for i in PARALISTindex:
    print (paralist[i+2])
    diameter=float(paralist[i+2][1])# 管材外径
    thickness=float(paralist[i+2][2])# 壳模型壁厚
    radius=float(paralist[i+2][3])# 弯曲半径
    frictionofbending=float(paralist[i+2][4])# 管材与弯曲模摩擦系数fb
    frictionofpressure=float(paralist[i+2][5])# 管材与压模摩擦系数fp
    frictionofwiper=float(paralist[i+2][6])# 管材与防皱模摩擦系数fw
    frictionofclamp=float(paralist[i+2][7])# 管材与夹紧模摩擦系数fc
    gapofbending=float(paralist[i+2][8])# 弯曲模间隙（0-0.25）
    gapofpressure=float(paralist[i+2][9])# 压模间隙（0-0.25）
    gapofwiper=float(paralist[i+2][10])# 防皱模间隙（0-0.25）
    gapofclamp=float(paralist[i+2][11])# 夹紧模间隙（0.1）
    #boosterdistanceofpressure=float(paralist[i+2][12])
    diffvelocityofpressure=float(paralist[i+2][12])# 助推速度差dVp
    initialpositionofpressure=float(paralist[i+2][13])# 助推块初始位置Lp0
    angularvelocity=float(paralist[i+2][14])# 弯曲模进给角速度（0.1745-1.0472rad/s）
    timeofstep1=float(paralist[i+2][16])# step时间
    frictionofboosterblock=float(paralist[i+2][17])# 助推块摩擦系数
    diameterofmandrel=float(paralist[i+2][18])# 芯棒直径
    widthofmandrel=float(paralist[i+2][19])# 芯棒宽度
    spacingofmandrel=float(paralist[i+2][20])# 芯棒间距
    lengthofshank=float(paralist[i+2][21])# 芯轴长度
    prolongationofshank=float(paralist[i+2][22])# 芯轴初始伸长量
    radiusofMandrelfillet=float(paralist[i+2][23])# 芯轴圆角半径
    massscaling=float(paralist[i+2][24])# 质量缩放系数
    lengthofclamp=0.8*radius# 夹紧模长度
    lengthofpressure=2.5*radius# 压模长度
    lengthofwiper=1.5*radius# 防皱模长度
    widthofbending=diameter+50
    lengthofpipe=angularvelocity*timeofstep1*radius+lengthofclamp+200
    boostervelocityofpressure=(angularvelocity+diffvelocityofpressure)*radius
    frictionofgeneral=0.05



#########################
####### 模型建立 #########
#########################
    #1.1弯曲模建模
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=1000.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(radius, 0.0), point1=(radius, -(diameter/2.0+gapofbending)), point2=(radius, 
        diameter/2.0+gapofbending), direction=CLOCKWISE)#半圆弧
    s.Line(point1=(radius, (diameter/2.0+gapofbending)), point2=(radius, widthofbending/2.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)#线段
    s.Line(point1=(radius, -(diameter/2.0+gapofbending)), point2=(radius, -(widthofbending)/2.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)#线段
    p = mdb.models['Model-0'].Part(name='bending-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['bending-die']
    p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)#旋转拉伸
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    p.ReferencePoint(point=(0.0, 0.0, 0.0))#选择刚体参考点
    mdb.models['Model-0'].parts['bending-die'].features.changeKey(fromName='RP', 
        toName='RP-bending')#重命名参考点
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='bending-die')#建立集合

    #1.2管件建模
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
    sheetSize=1000.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)

    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, diameter/2.0-thickness/2.0))
    p = mdb.models['Model-0'].Part(name='pipe', dimensionality=THREE_D, 
      type=DEFORMABLE_BODY)
    p = mdb.models['Model-0'].parts['pipe']
    p.BaseShellExtrude(sketch=s, depth=lengthofpipe)
    s.unsetPrimaryObject()
    ##del mdb.models['Model-1'].sketches['__profile__']

    p = mdb.models['Model-0'].parts['pipe']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3 ]', ), )
    p.Set(faces=faces, name='pipe')

    #1.3夹紧模
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    s.ArcByCenterEnds(center=(radius, 0.0), point1=(radius, -(diameter/2.0+gapofclamp)), point2=(radius, 
        diameter/2.0+gapofclamp), direction=COUNTERCLOCKWISE)#半圆弧
    s.Line(point1=(radius, (diameter/2.0+gapofclamp)), point2=(radius, widthofbending/2.0))#线段
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.Line(point1=(radius, -(diameter/2.0+gapofclamp)), point2=(radius, -(widthofbending)/2.0))#线段
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    p = mdb.models['Model-0'].Part(name='clamp-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['clamp-die']
    p.BaseShellExtrude(sketch=s, depth=lengthofclamp)#拉伸
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[4], rule=CENTER))#选择刚体参考点
    mdb.models['Model-0'].parts['clamp-die'].features.changeKey(fromName='RP', 
        toName='RP-clamp')#参考点重命名
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='clamp-die')#建立集合

    #1.4压模
    s1 = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -(diameter/2.0+gapofpressure)), point2=(0.0, diameter/2.0+gapofpressure), 
        direction=CLOCKWISE)#半圆弧
    p = mdb.models['Model-0'].Part(name='pressure-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['pressure-die']
    p.BaseShellExtrude(sketch=s1, depth=lengthofpressure)#拉伸
    s1.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v2, e1, d1, n1 = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e1[0], rule=CENTER))#选择刚体参考点
    mdb.models['Model-0'].parts['pressure-die'].features.changeKey(fromName='RP', 
        toName='RP-pressure')#重命名参考点
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='pressure-die')#建立集合

    #1.5防皱模
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, -(diameter/2.0+gapofwiper)), point2=(0.0, diameter/2.0+gapofwiper), 
        direction=CLOCKWISE)#半圆弧
    p = mdb.models['Model-0'].Part(name='wiper-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['wiper-die']
    p.BaseShellExtrude(sketch=s, depth=lengthofwiper)#拉伸
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[2], rule=CENTER))#选择刚体参考点
    mdb.models['Model-0'].parts['wiper-die'].features.changeKey(fromName='RP', 
        toName='RP-wiper')#参考点重命名
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='wiper-die')#建立集合
    #1.6镶块建模
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ArcByCenterEnds(center=(radius, 0.0), point1=(radius, -(diameter/2.0+gapofclamp)), point2=(radius, 
        diameter/2.0+gapofclamp), direction=CLOCKWISE)#半圆弧
    p = mdb.models['Model-0'].Part(name='insert-die', dimensionality=THREE_D, 
        type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['insert-die']
    p.BaseShellExtrude(sketch=s, depth=lengthofclamp)#拉伸
    s.unsetPrimaryObject()
    del mdb.models['Model-0'].sketches['__profile__']
    v1, e, d2, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=p.InterestingPoint(edge=e[0], rule=CENTER))#选择刚体参考点
    mdb.models['Model-0'].parts['insert-die'].features.changeKey(fromName='RP', 
        toName='RP-insert')#参考点重命名
    r = p.referencePoints
    refPoints=(r[2], )
    p.Set(referencePoints=refPoints, name='insert-die')#建立集合

    #芯球1
    s1 = mdb.models['Model-0'].ConstrainedSketch(name='__profile__',
                                                    sheetSize=2000.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -1000.0), point2=(0.0, 1000.0))
    s1.FixedConstraint(entity=g[2])
    s1.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.ConstructionLine(point1=(widthofmandrel/2, 0.0), angle=90.0)
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.ConstructionLine(point1=(-widthofmandrel/2, 0.0), angle=90.0)
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(-widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )), point2=(widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )),
                       direction=CLOCKWISE)
    s1.Line(point1=(-widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )), point2=(-widthofmandrel/2, 0.0))
    s1.VerticalConstraint(entity=g[7], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[3], addUndoState=False)
    s1.Line(point1=(-widthofmandrel/2, 0.0), point2=(widthofmandrel/2, 0.0))
    s1.HorizontalConstraint(entity=g[8], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[4], entity2=g[3], addUndoState=False)
    s1.Line(point1=(widthofmandrel/2, 0.0), point2=(widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )))
    s1.VerticalConstraint(entity=g[9], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[8], entity2=g[9], addUndoState=False)
    s1.sketchOptions.setValues(constructionGeometry=ON)
    s1.assignCenterline(line=g[3])
    p = mdb.models['Model-0'].Part(name='ball1', dimensionality=THREE_D,
                                      type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['ball1']
    p.BaseShellRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-0'].parts['ball1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-0'].sketches['__profile__']
    p = mdb.models['Model-0'].parts['ball1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-0'].parts['ball1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-0'].parts['ball1']
    p.ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models['Model-0'].parts['ball1'].features.changeKey(fromName='RP',toName='RP-ball1')
    p = mdb.models['Model-0'].parts['ball1']
    r = p.referencePoints
    refPoints = (r[2],)
    p.Set(referencePoints=refPoints, name='ball1')
    #: 集 'ball1' 已创建 (1 参考点).
    p = mdb.models['Model-0'].parts['ball1']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#1 ]',), )
    p.Surface(side1Faces=side1Faces, name='ball1')
    #: 表面 'ball1' 已创建 (1 面).

    #芯球2
    s1 = mdb.models['Model-0'].ConstrainedSketch(name='__profile__',
                                                    sheetSize=2000.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -1000.0), point2=(0.0, 1000.0))
    s1.FixedConstraint(entity=g[2])
    s1.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.ConstructionLine(point1=(widthofmandrel/2, 0.0), angle=90.0)
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.ConstructionLine(point1=(-widthofmandrel/2, 0.0), angle=90.0)
    s1.VerticalConstraint(entity=g[5], addUndoState=False)
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(-widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )), point2=(widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )),
                       direction=CLOCKWISE)
    s1.Line(point1=(-widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )), point2=(-widthofmandrel/2, 0.0))
    s1.VerticalConstraint(entity=g[7], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[3], addUndoState=False)
    s1.Line(point1=(-widthofmandrel/2, 0.0), point2=(widthofmandrel/2, 0.0))
    s1.HorizontalConstraint(entity=g[8], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[4], entity2=g[3], addUndoState=False)
    s1.Line(point1=(widthofmandrel/2, 0.0), point2=(widthofmandrel/2, math.sqrt(math.pow((diameterofmandrel/2),2)-math.pow(widthofmandrel/2,2) )))
    s1.VerticalConstraint(entity=g[9], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[8], entity2=g[9], addUndoState=False)
    s1.sketchOptions.setValues(constructionGeometry=ON)
    s1.assignCenterline(line=g[3])
    p = mdb.models['Model-0'].Part(name='ball2', dimensionality=THREE_D,type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['ball2']
    p.BaseShellRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-0'].parts['ball2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-0'].sketches['__profile__']
    p = mdb.models['Model-0'].parts['ball2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-0'].parts['ball2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-0'].parts['ball2']
    p.ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models['Model-0'].parts['ball2'].features.changeKey(fromName='RP',toName='RP-ball2')
    p = mdb.models['Model-0'].parts['ball2']
    r = p.referencePoints
    refPoints = (r[2],)
    p.Set(referencePoints=refPoints, name='ball2')
    #: 集 'ball2' 已创建 (1 参考点).
    p = mdb.models['Model-0'].parts['ball2']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#1 ]',), )
    p.Surface(side1Faces=side1Faces, name='ball2')
    #: 表面 'ball2' 已创建 (1 面).

    

    #芯轴
    s = mdb.models['Model-0'].ConstrainedSketch(name='__profile__',
                                                   sheetSize=2000.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -1000.0), point2=(0.0, 1000.0))
    s.FixedConstraint(entity=g[2])
    
    s.ConstructionLine(point1=(0.0, 0.0), angle=90.0)
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.ConstructionLine(point1=(lengthofshank, 0.0), angle=90.0)
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
    s.HorizontalConstraint(entity=g[5], addUndoState=False)
    s.ConstructionLine(point1=(0.0, diameterofmandrel/2.0), angle=0.0)
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.Line(point1=(0.0, 0.0), point2=(lengthofshank, 0.0))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[7], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
    s.CoincidentConstraint(entity1=v[1], entity2=g[4], addUndoState=False)
    s.Line(point1=(lengthofshank, 0.0), point2=(lengthofshank, diameterofmandrel/2.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s.CoincidentConstraint(entity1=v[2], entity2=g[4], addUndoState=False)
    s.Line(point1=(lengthofshank, diameterofmandrel/2.0), point2=(0.0, diameterofmandrel/2.0))
    s.HorizontalConstraint(entity=g[9], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[8], entity2=g[9], addUndoState=False)
    s.CoincidentConstraint(entity1=v[3], entity2=g[2], addUndoState=False)
    s.Line(point1=(0.0, diameterofmandrel/2.0), point2=(0.0, 0.0))
    s.VerticalConstraint(entity=g[10], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
    s.FilletByRadius(radius=radiusofMandrelfillet, curve1=g[10], nearPoint1=(0,0.01), curve2=g[9],
                     nearPoint2=(0.01,diameterofmandrel/2.0))
    s.sketchOptions.setValues(constructionGeometry=ON)
    s.assignCenterline(line=g[5])
    p = mdb.models['Model-0'].Part(name='shank', dimensionality=THREE_D,type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-0'].parts['shank']
    p.BaseShellRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-0'].parts['shank']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-0'].sketches['__profile__']
    p1 = mdb.models['Model-0'].parts['shank']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-0'].parts['shank']
    p.ReferencePoint(point=(prolongationofshank, 0.0, 0.0))
    mdb.models['Model-0'].parts['shank'].features.changeKey(fromName='RP',toName='RP-shank')
    p = mdb.models['Model-0'].parts['shank']
    r = p.referencePoints
    refPoints = (r[2],)
    p.Set(referencePoints=refPoints, name='shank')
    #: 集 'shank' 已创建 (1 参考点).
    p = mdb.models['Model-0'].parts['shank']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#2 ]',), )
    p.Surface(side1Faces=side1Faces, name='shank')
    #: 表面 'shank' 已创建 (1 面).

    #2.1定义材料
    # mdb.models['Model-0'].Material(name='copper-T1')
    # mdb.models['Model-0'].materials['copper-T1'].Elastic(table=((110000,
    #     0.32), ))
    # mdb.models['Model-0'].materials['copper-T1'].Density(table=((8.9e-09, ), ))
    # mdb.models['Model-0'].materials['copper-T1'].Conductivity(table=((390, ), ))
    # mdb.models['Model-0'].materials['copper-T1'].Plastic(table=((240.0, 0.0), (245.0,
    #     0.01), (250.0, 0.02), (260.0, 0.03), (263.0, 0.04), (
    #     267.0, 0.05), (270.0, 0.06), (267.0, 0.07), (263.0, 0.08),
    #     (260.0, 0.09),(255.0, 0.1)))
    #
    # mdb.models['Model-0'].Material(name='SI_mm113111_6061-T6(GB)')
    # mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Elastic(table=((69000.0006661372,
    #     0.33), ))
    # mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Density(table=((2.7e-09, ), ))
    # mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Conductivity(table=((166.9, ), ))
    # mdb.models['Model-0'].materials['SI_mm113111_6061-T6(GB)'].Plastic(table=((275.0, 0.0), (275.0,
    #     0.004), (275.79029, 0.01), (277.16924, 0.015), (282.68505, 0.02), (
    #     296.47456, 0.03), (310.26408, 0.04), (324.05359, 0.06), (344.73786, 0.08),
    #     (355.76948, 0.09)))
    from material import createMaterialFromDataString

    createMaterialFromDataString('Model-0', 'SI_mm304', '2016',"""{'specificHeat': {'temperatureDependency': OFF, 'table': ((460000000.0,),), 'dependencies': 0, 'law': CONSTANTVOLUME}, 'materialIdentifier': '', 'description': '', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((190000.0, 0.29),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((7.93e-09,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'name': 'SI_mm304', 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((206.807, 0.0), (215.0, 0.0011), (303.6, 0.1176), (376.0, 0.234), (432.5, 0.35), (472.8, 0.47), (479.0, 0.58), (505.0, 0.7)), 'numBackstresses': 1}, 'expansion': {'temperatureDependency': OFF, 'userSubroutine': OFF, 'zero': 0.0, 'dependencies': 0, 'table': ((1.8e-05,),), 'type': ISOTROPIC}, 'conductivity': {'temperatureDependency': OFF, 'table': ((16.3,),), 'dependencies': 0, 'type': ISOTROPIC}}""")
    #: Material 'SI_mm304' has been copied to the current model.

    #2.2定义截面


    mdb.models['Model-0'].HomogeneousShellSection(name='Section-1', 
        preIntegrate=OFF, material='SI_mm304',
        thicknessType=UNIFORM, thickness=thickness, thicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=9)



    #2.3截面指派


    p = mdb.models['Model-0'].parts['pipe']
    region = p.sets['pipe']
    p = mdb.models['Model-0'].parts['pipe']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

    #3组合装配
    #3.1零件实例化
    a = mdb.models['Model-0'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-0'].parts['bending-die']
    a.Instance(name='bending-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['clamp-die']
    a.Instance(name='clamp-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['pipe']
    a.Instance(name='pipe-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['pressure-die']
    a.Instance(name='pressure-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['wiper-die']
    a.Instance(name='wiper-die-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['insert-die']
    a.Instance(name='insert-die-1', part=p, dependent=ON)
    a = mdb.models['Model-0'].rootAssembly
    p = mdb.models['Model-0'].parts['ball1']
    a.Instance(name='ball1-1', part=p, dependent=ON)
    p = mdb.models['Model-0'].parts['ball2']
    a.Instance(name='ball2-1', part=p, dependent=ON)
    
    p = mdb.models['Model-0'].parts['shank']
    a.Instance(name='shank-1', part=p, dependent=ON)
    #3.2旋转操作
    a = mdb.models['Model-0'].rootAssembly
    a.rotate(instanceList=('bending-die-1', 'clamp-die-1','insert-die-1',), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, 1.0), angle=90.0)
    a.rotate(instanceList=('clamp-die-1','insert-die-1',), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 1.0, 0.0), angle=180.0)
    a.rotate(instanceList=('pipe-1', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(
        0.0, 1.0, 0.0), angle=180.0)
    a.rotate(instanceList=('pressure-die-1', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, -1.0), angle=90.0)
    a.rotate(instanceList=('wiper-die-1', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(0.0, 0.0, 1.0), angle=90.0)
    #3.3平移操作
    a = mdb.models['Model-0'].rootAssembly
    a.translate(instanceList=('pipe-1', ), vector=(0.0, radius, lengthofclamp+0.5*lengthofclamp))
    a.translate(instanceList=('clamp-die-1', ), vector=(0.0, 0.0, lengthofclamp))
    a.translate(instanceList=('wiper-die-1', ), vector=(0.0, radius, -lengthofwiper))
    a.translate(instanceList=('pressure-die-1', ), vector=(0.0, radius, -(lengthofpressure+initialpositionofpressure)))
    a.translate(instanceList=('insert-die-1', ), vector=(0.0, 0.0, lengthofclamp))
    #3.4芯棒调整
    a = mdb.models['Model-0'].rootAssembly
    a.rotate(instanceList=('ball1-1', 'ball2-1', 'shank-1'), axisPoint=(
        0.0, 0.0, 0.0), axisDirection=(0.0, 1.0, 0.0), angle=90.0)
    #: The instances were rotated by 90. 度(关于由点 0., 0., 0. 和向量 0., 1., 0. 定义的轴线)
    a = mdb.models['Model-0'].rootAssembly
    a.translate(instanceList=('ball1-1', 'ball2-1', 'shank-1'), vector=(
        0.0, radius, prolongationofshank))
    #: The instances were translated by 0., 弯曲半径, 初始伸长量(相对于装配坐标系)
    a = mdb.models['Model-0'].rootAssembly
    a.translate(instanceList=('ball1-1',), vector=(0.0, 0.0, spacingofmandrel-prolongationofshank))
    #: The instance ball1-1 was translated by 0., 0., 4. (相对于装配坐标系)
    a = mdb.models['Model-0'].rootAssembly
    a.translate(instanceList=('ball2-1',), vector=(0.0, 0.0, 2*spacingofmandrel+widthofmandrel-prolongationofshank))
    #: The instance ball2-1 was translated by 0., 0., 15. (相对于装配坐标系)
    



    #4定义分析步
    mdb.models['Model-0'].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
    timePeriod=timeofstep1, massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, massscaling,
    0.0, None, 0, 0, 0.0, 0.0, 0, None), ))#质量缩放
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models['Model-0'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=36, timeMarks=ON)#均匀时间间隔输出

    mdb.models['Model-0'].historyOutputRequests['H-Output-1'].setValues(
        variables=('ALLIE', 'ALLKE', 'ETOTAL'))
    
    
    #5定义相互作用
    #5.1定义表面

    a = mdb.models['Model-0'].rootAssembly
    s1 = a.instances['pipe-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#3 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='pipe')
    a = mdb.models['Model-0'].rootAssembly
    s1 = a.instances['pipe-1'].faces
    side2Faces1 = s1.getSequenceFromMask(mask=('[#3 ]',), )
    a.Surface(side2Faces=side2Faces1, name='pipe-inside')
    #: 表面 'pipe-inside' 已创建 (2 面).

    s1 = a.instances['bending-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='bending')#创建表面
    s1 = a.instances['clamp-die-1'].faces
    side2Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
    a.Surface(side2Faces=side2Faces1, name='clamp')#创建表面
    s1 = a.instances['pressure-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='pressure')#创建表面
    s1 = a.instances['wiper-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='wiper')#创建表面

    s1 = a.instances['insert-die-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='insert')#创建表面


    #5.2定义接触属性
    mdb.models['Model-0'].ContactProperty('bending')
    mdb.models['Model-0'].interactionProperties['bending'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofbending, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-0'].interactionProperties['bending'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
    #bending接触属性
    mdb.models['Model-0'].ContactProperty('pressure')
    mdb.models['Model-0'].interactionProperties['pressure'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofpressure, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-0'].interactionProperties['pressure'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
    #pressure接触属性
    mdb.models['Model-0'].ContactProperty('wiper')
    mdb.models['Model-0'].interactionProperties['wiper'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofwiper, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-0'].interactionProperties['wiper'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
    #wiper接触属性
    mdb.models['Model-0'].ContactProperty('clamp')
    mdb.models['Model-0'].interactionProperties['clamp'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofclamp, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-0'].interactionProperties['clamp'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
    #clamp接触属性
    mdb.models['Model-0'].ContactProperty('general')
    mdb.models['Model-0'].interactionProperties['general'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF,
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        frictionofboosterblock,),), shearStressLimit=None,maximumElasticSlip=FRACTION,
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-0'].interactionProperties['general'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON,constraintEnforcementMethod=DEFAULT)

    #5.3定义接触

    #: 相互作用 "General" .
    mdb.models['Model-0'].ContactExp(name='General', createStepName='Initial')
    mdb.models['Model-0'].interactions['General'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=ON)
    r21 = mdb.models['Model-0'].rootAssembly.surfaces['bending']
    r22 = mdb.models['Model-0'].rootAssembly.surfaces['pipe']
    r31 = mdb.models['Model-0'].rootAssembly.surfaces['clamp']
    r32 = mdb.models['Model-0'].rootAssembly.surfaces['pipe']
    r41 = mdb.models['Model-0'].rootAssembly.surfaces['insert']
    r42 = mdb.models['Model-0'].rootAssembly.surfaces['pipe']
    r51 = mdb.models['Model-0'].rootAssembly.surfaces['pressure']
    r52 = mdb.models['Model-0'].rootAssembly.surfaces['pipe']
    r61 = mdb.models['Model-0'].rootAssembly.surfaces['wiper']
    r62 = mdb.models['Model-0'].rootAssembly.surfaces['pipe']
    mdb.models['Model-0'].interactions['General'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'general'), (r21, r22,'bending'), (r31, r32, 'clamp'),
        (r41, r42, 'clamp'), (r51, r52,'pressure'), (r61, r62, 'wiper')))

    ## surface to surface
    # a = mdb.models['Model-0'].rootAssembly
    # region1=a.surfaces['bending']
    # region2=a.surfaces['pipe']
    # mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='bending',
    #     createStepName='Step-1', master = region1, slave = region2,
    #     mechanicalConstraint=PENALTY, sliding=FINITE,
    #     interactionProperty='bending', initialClearance=OMIT, datumAxis=None,
    #     clearanceRegion=None)#bending接触
    # region1=a.surfaces['pressure']
    # region2=a.surfaces['pipe']
    # mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='pressure',
    #     createStepName='Step-1', master = region1, slave = region2,
    #     mechanicalConstraint=PENALTY, sliding=FINITE,
    #     interactionProperty='pressure', initialClearance=OMIT, datumAxis=None,
    #     clearanceRegion=None)#pressure接触
    # region1=a.surfaces['wiper']
    # region2=a.surfaces['pipe']
    # mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='wiper',
    #     createStepName='Step-1', master = region1, slave = region2,
    #     mechanicalConstraint=PENALTY, sliding=FINITE,
    #     interactionProperty='wiper', initialClearance=OMIT, datumAxis=None,
    #     clearanceRegion=None)#wiper接触
    #
    # a = mdb.models['Model-0'].rootAssembly
    # region1=a.surfaces['clamp']
    # region2=a.surfaces['pipe']
    # mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='clamp',
    #     createStepName='Initial', master = region1, slave = region2,
    #     mechanicalConstraint=PENALTY, sliding=FINITE, interactionProperty='clamp',
    #     initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
    # #: The interaction "clamp" has been created.
    #
    # a = mdb.models['Model-0'].rootAssembly
    # region1=a.surfaces['insert']
    # region2=a.surfaces['pipe']
    # mdb.models['Model-0'].SurfaceToSurfaceContactExp(name ='insert',
    #     createStepName='Initial', master = region1, slave = region2,
    #     mechanicalConstraint=PENALTY, sliding=FINITE, interactionProperty='clamp',
    #     initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
    # #: The interaction "insert" has been created.


    #5.4定义约束
    #region2=a.surfaces['pipe-front-face']
    #5.5定义连接
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.instances['bending-die-1'].referencePoints#连接点1
    r2 = a.instances['clamp-die-1'].referencePoints#连接点2
    a.WirePolyLine(points=((r1[2], r2[2]), ), mergeType=IMPRINT, meshable=OFF)
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(edges=edges1, name='Wire-1-Set-1')#定义线条特征
    a = mdb.models['Model-0'].rootAssembly
    r11 = a.instances['bending-die-1'].referencePoints
    r12 = a.instances['insert-die-1'].referencePoints
    a.WirePolyLine(points=((r11[2], r12[2]), ), mergeType=IMPRINT, meshable=OFF)
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
    a.Set(edges=edges1, name='Wire-2-Set-1')
    mdb.models['Model-0'].ConnectorSection(name='ConnSect-1', assembledType=BEAM)
    region=a.sets['Wire-1-Set-1']
    csa = a.SectionAssignment(sectionName='ConnSect-1', region=region)#定义连接截面
    mdb.models['Model-0'].ConnectorSection(name='ConnSect-2', assembledType=BEAM)
    region=a.sets['Wire-2-Set-1']
    csa = a.SectionAssignment(sectionName='ConnSect-2', region=region)

################################################
    #芯棒约束设置
################################################
    #创建局部坐标系
    a = mdb.models['Model-0'].rootAssembly
    r11 = a.instances['shank-1'].referencePoints
    a.DatumCsysByThreePoints(origin=r11[2], name='shank', coordSysType=CARTESIAN,
                             line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.instances['ball1-1'].referencePoints
    a.DatumCsysByThreePoints(origin=r1[2], name='ball1', coordSysType=CARTESIAN,
                             line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
    a = mdb.models['Model-0'].rootAssembly
    r11 = a.instances['ball2-1'].referencePoints
    a.DatumCsysByThreePoints(origin=r11[2], name='ball2', coordSysType=CARTESIAN,
                             line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
    #创建RP点
    a = mdb.models['Model-0'].rootAssembly
    v21 = a.instances['ball1-1'].vertices
    a.ReferencePoint(point=v21[1])
    a = mdb.models['Model-0'].rootAssembly
    v11 = a.instances['ball2-1'].vertices
    a.ReferencePoint(point=v11[1])

    #将所创建RP点与芯球RP点形成耦合约束
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[34], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-0'].rootAssembly
    region2=a.instances['ball1-1'].sets['ball1']
    mdb.models['Model-0'].Coupling(name='ball1', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[35], )
    region1=regionToolset.Region(referencePoints=refPoints1)
    a = mdb.models['Model-0'].rootAssembly
    region2=a.instances['ball2-1'].sets['ball2']
    mdb.models['Model-0'].Coupling(name='ball2', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    
#创建连接线
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.instances['shank-1'].referencePoints
    r2 = a.instances['ball1-1'].referencePoints
    a.WirePolyLine(points=((r1[2], r2[2]),), mergeType=IMPRINT, meshable=OFF)
    a = mdb.models['Model-0'].rootAssembly
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]',), )
    a.Set(edges=edges1, name='Wire-3-Set-1')
    a = mdb.models['Model-0'].rootAssembly
    r11 = a.instances['shank-1'].referencePoints
    r12 = a.referencePoints
    a.WirePolyLine(points=((r11[2], r12[34]),), mergeType=IMPRINT, meshable=OFF)
    a = mdb.models['Model-0'].rootAssembly
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]',), )
    a.Set(edges=edges1, name='Wire-4-Set-1')
    a = mdb.models['Model-0'].rootAssembly
    r1 = a.instances['ball1-1'].referencePoints
    r2 = a.instances['ball2-1'].referencePoints
    a.WirePolyLine(points=((r1[2], r2[2]),), mergeType=IMPRINT, meshable=OFF)
    a = mdb.models['Model-0'].rootAssembly
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]',), )
    a.Set(edges=edges1, name='Wire-5-Set-1')
    a = mdb.models['Model-0'].rootAssembly
    r11 = a.instances['ball1-1'].referencePoints
    r12 = a.referencePoints
    a.WirePolyLine(points=((r11[2], r12[35]),), mergeType=IMPRINT, meshable=OFF)
    a = mdb.models['Model-0'].rootAssembly
    e1 = a.edges
    edges1 = e1.getSequenceFromMask(mask=('[#1 ]',), )
    a.Set(edges=edges1, name='Wire-6-Set-1')
    #创建连接
    mdb.models['Model-0'].ConnectorSection(name='ConnSect-3',
    translationalType=LINK, rotationalType=REVOLUTE)
    a = mdb.models['Model-0'].rootAssembly
    region=a.sets['Wire-3-Set-1']
    datum1 = mdb.models['Model-0'].rootAssembly.datums[31]
    csa = a.SectionAssignment(sectionName='ConnSect-3', region=region)
    #: 截面 "ConnSect-3" 已指派给 1 条线或附着线.
    a.ConnectorOrientation(region=csa.getSet(), localCsys1=datum1)
    a = mdb.models['Model-0'].rootAssembly
    region=a.sets['Wire-4-Set-1']
    datum1 = mdb.models['Model-0'].rootAssembly.datums[31]
    csa = a.SectionAssignment(sectionName='ConnSect-3', region=region)
    #: 截面 "ConnSect-3" 已指派给 1 条线或附着线.
    a.ConnectorOrientation(region=csa.getSet(), localCsys1=datum1)
    a = mdb.models['Model-0'].rootAssembly
    region=a.sets['Wire-5-Set-1']
    datum1 = mdb.models['Model-0'].rootAssembly.datums[32]
    csa = a.SectionAssignment(sectionName='ConnSect-3', region=region)
    #: 截面 "ConnSect-3" 已指派给 1 条线或附着线.
    a.ConnectorOrientation(region=csa.getSet(), localCsys1=datum1)
    a = mdb.models['Model-0'].rootAssembly
    region=a.sets['Wire-6-Set-1']
    datum1 = mdb.models['Model-0'].rootAssembly.datums[32]
    csa = a.SectionAssignment(sectionName='ConnSect-3', region=region)
    #: 截面 "ConnSect-3" 已指派给 1 条线或附着线.
    a.ConnectorOrientation(region=csa.getSet(), localCsys1=datum1)




    #5.6定义惯性inertia
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['clamp-die-1'].sets['clamp-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-1', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['insert-die-1'].sets['insert-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-2', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['bending-die-1'].sets['bending-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-3', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)
    a = mdb.models['Model-0'].rootAssembly
    region=a.instances['pressure-die-1'].sets['pressure-die']
    mdb.models['Model-0'].rootAssembly.engineeringFeatures.PointMassInertia(
        name='Inertia-4', region=region, mass=0.001, i11=100.0, i22=100.0, 
        i33=100.0, alpha=0.0, composite=0.0)

    p = mdb.models['Model-0'].parts['ball1']
    region = p.sets['ball1']
    mdb.models['Model-0'].parts['ball1'].engineeringFeatures.PointMassInertia(
        name='ball1', region=region, mass=1E-008, i11=0.0001, i22=0.0001, i33=0.0001,
        alpha=0.0, composite=0.0)
    p = mdb.models['Model-0'].parts['ball2']
    region = p.sets['ball2']
    mdb.models['Model-0'].parts['ball2'].engineeringFeatures.PointMassInertia(
        name='ball2', region=region, mass=1E-008, i11=0.0001, i22=0.0001, i33=0.0001,
        alpha=0.0, composite=0.0)
    #6定义边界
    #6.1定义防皱模边界条件
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['wiper-die-1'].sets['wiper-die']
    mdb.models['Model-0'].EncastreBC(name='wiper', createStepName='Initial', 
        region=region, localCsys=None)
    #6.2定义压模边界条件
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['pressure-die-1'].sets['pressure-die']
    mdb.models['Model-0'].VelocityBC(name='pressure', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=boostervelocityofpressure, vr1=0.0, vr2=0.0, 
        vr3=0.0, amplitude=UNSET, localCsys=None, distributionType=UNIFORM, 
        fieldName='')

    #6.3定义弯曲模边界条件
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['bending-die-1'].sets['bending-die']
    mdb.models['Model-0'].VelocityBC(name='bending', createStepName='Step-1', 
        region=region, v1=0.0, v2=0.0, v3=0.0, vr1=angularvelocity, vr2=0.0, vr3=0.0, 
        amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')
    #6.4固定芯轴
    a = mdb.models['Model-0'].rootAssembly
    region = a.instances['shank-1'].sets['shank']
    mdb.models['Model-0'].EncastreBC(name='shank', createStepName='Initial',
                                        region=region, localCsys=None)
    #7网格划分
    #弯曲模网格划分
    p = mdb.models['Model-0'].parts['bending-die']
    p.seedPart(size=(diameter*3.1415926)/40, deviationFactor=0.1, minSizeFactor=0.1)#全局布种
    p.generateMesh()#网格划分
    #夹紧模网格划分
    p = mdb.models['Model-0'].parts['clamp-die']
    p.seedPart(size=(diameter*3.1415926)/40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #管件划分网格
    p = mdb.models['Model-0'].parts['pipe']
    p.seedPart(size=(diameter*3.1415926)/50, deviationFactor=0.01, minSizeFactor=0.1)
    p.generateMesh()

    #压模划分网格
    p = mdb.models['Model-0'].parts['pressure-die']
    p.seedPart(size=(diameter*3.1415926)/40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #防皱模划分网格
    p = mdb.models['Model-0'].parts['wiper-die']
    p.seedPart(size=(diameter*3.1415926)/40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #镶块网格划分
    p = mdb.models['Model-0'].parts['insert-die']
    p.seedPart(size=(diameter*3.1415926)/40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    #芯棒网络划分
    p = mdb.models['Model-0'].parts['ball1']
    p.seedPart(size=(diameter*3.1415926)/40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    p = mdb.models['Model-0'].parts['ball2']
    p.seedPart(size=(diameter * 3.1415926) /40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    p = mdb.models['Model-0'].parts['shank']
    p.seedPart(size=(diameter * 3.1415926) /40, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()

    mdb.models.changeKey(fromName='Model-0', toName='Model-'+paralist[i+2][0])#修改模型树中模型名
    mdb.Model(name='Model-0', modelType=STANDARD_EXPLICIT)#建立新模型

    mdb.Job(name=paralist[i+2][0], model='Model-'+paralist[i+2][0], description='', type=ANALYSIS,
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
    memoryUnits=PERCENTAGE, explicitPrecision=DOUBLE,
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
    contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
    resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1,
    activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)#创建任务

#mdb.jobs['bending'+paralist[i+2][0]].submit(consistencyChecking=OFF)#提交任务

del mdb.models['Model-0']
mdb.saveAs(pathName='D:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/2ball'+paralist[i+2][0])#mdb文件保存路径及文件名

session.viewports['Viewport: 1'].setValues(displayedObject=None)
print ('End of programm');
    
