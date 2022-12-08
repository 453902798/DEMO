# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
import csv
import os
os.chdir(r"D:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/1ball")#�޸Ĺ���Ŀ¼��������󱣴�inp�ļ�
filePath = "D:/ABAQUS/ABAQUS_practice/GraduateDesign/2_60/data/1ball/"#odb·����Ӣ�Ĳ�������

for num in range(1,101): #��������
    Mdb()
    num=str(num)#intתΪstr
    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']

    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb)
    p = mdb.models['Model-1'].parts['PIPE-1']
    odb.close()
    #��������ǰ��
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['PIPE-1']
    a.Instance(name='PIPE-1-1', part=p, dependent=ON)
    #ʵ����

    mdb.Job(name='M'+num+'_1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=DOUBLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
        numDomains=1, activateLoadBalancing=False, multiprocessingMode=DEFAULT, 
        numCpus=1, numGPUs=0)

    mdb.jobs['M'+num+'_1'].writeInput(consistencyChecking=OFF)
    #����job��д��inp



    session.openOdb(filePath+num+'.odb')
    odb = session.odbs[filePath+num+'.odb']
    p = mdb.models['Model-1'].PartFromOdb(name='PIPE-1', instance='PIPE-1', 
        odb=odb, shape=DEFORMED, step=0, frame=-1)
    p = mdb.models['Model-1'].parts['PIPE-1']
    odb.close()
    #�����������
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    
    mdb.jobs.changeKey(fromName='M'+num+'_1', toName='M'+num+'_2')
    mdb.jobs['M'+num+'_2'].writeInput(consistencyChecking=OFF)
    #��job����д��inp



#mdb.saveAs(pathName='G:/pipe_abaqus/pipe_shell_batch/20210507_copper/singlecopperodb/txt/odbreadercopper')#mdb�ļ�����·�����ļ���

print 'End of programm'


