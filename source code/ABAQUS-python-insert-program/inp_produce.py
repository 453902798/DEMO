# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
import csv
import os
os.chdir(r"D:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/1ball")#修改工作目录，用于最后保存inp文件
filePath = "D:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/1ball/"#odb路径与英文部分名称

for num in range(1,101): #迭代数字
    Mdb()
    num=str(num)#int转为str
    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']

    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb)
    p = mdb.models['Model-1'].parts['PIPE-1']
    odb.close()
    #导入弯曲前的
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['PIPE-1']
    a.Instance(name='PIPE-1-1', part=p, dependent=ON)
    #实例化

    mdb.Job(name='M'+num+'_1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=DOUBLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
        numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
        numCpus=1, numGPUs=0)

    mdb.jobs['M'+num+'_1'].writeInput(consistencyChecking=OFF)
    #创建job并写入inp



    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']
    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb, shape=DEFORMED, step=0, frame=-1)
    p = mdb.models['Model-1'].parts['PIPE-1']
    odb.close()
    #导入弯曲后的
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    
    mdb.jobs.changeKey(fromName='M'+num+'_1', toName='M'+num+'_2')
    mdb.jobs['M'+num+'_2'].writeInput(consistencyChecking=OFF)
    #改job名并写入inp



#mdb.saveAs(pathName='G:/pipe_abaqus/pipe_shell_batch/20210507_copper/singlecopperodb/txt/odbreadercopper')#mdb文件保存路径及文件名

print 'End of programm'


