import os
import re
from db import *

import time
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom



global RxMessageObject
global ListTemp
global MessageFound
global RxMessageFound 
global TxMessageFound 
global Nodes

def LoadDatabase():
   
   global  RxMessageObject
   global  ListTemp
   DbPath = r'C:\Projects\PythonWorkspace\Python\ParseFile\MS1_CAN_P702_GASDHEV_MY21_V05.dbc' 

   dtabase = open(DbPath,'r')
   lines = dtabase.readlines()


   RxMessageObject = []
   NoneTxMessage = []
   NoneTxMessageID= []
   ListTemp = []
   MessageFound =False
   TxMessageFound = False

   for line in lines:
      if "BU_:" in line:
         db().node = line.split()
         del db().node[0]



   for line in lines:

      if "BU_:" in line:
         db().node = line.split()
         del db().node[0]

      #if "VAL_TABLE_" in line:
      #   db().ValueTable.append(line)
      
      elif " SG_ " in line:

         if line.split()[0] == "SG_" and MessageFound == True and TxMessageFound == False:
            #db().signal.append(line.split()[1])
            #print(line.split()[7])
            if findClimateNode(line):
              # RxMessageObject.append(InitRxMessage())
              # RxMessageObject[-1].RxSignal.append(line.split()[1])
              db().RxMessageSignal.append(line.split()[1])
              ListTemp.append(line.split()[1])
              

         elif line.split()[0] == "SG_" and MessageFound == True and TxMessageFound == True:
            db().TxMessageSignal.append(line.split()[1])
         else:
            TxMessageFound = False
            MessageFound = False

      elif "BO_ " in line:
         
         '''Find message'''
         if line.split()[0] == "BO_":
            MessageFound = True
            TxMessageFound = False
            '''Find climate node related Tx message'''
            if line.split()[4] == "HVAC_RCCM":
               TxMessageFound = True
               '''Get Message message ID'''
               temp = line.split()[2]
               temp = list(temp)
               del temp[-1]
               temp = ''.join(temp) +'(' + str(hex(int(line.split()[1]))).upper() +  ')'
               db().TxMessageID.append(str(hex(int(line.split()[1]))).upper())
               db().TxMessageWithID.append(temp)
               '''Get Normal Message name'''
               db().TxMessageSignal.append(line.split()[2])
               db().TxMessageIndex.append(db().TxMessageSignal.index(line.split()[2]))

            else:
               NoneTxMessage.append(line.split()[2])
               NoneTxMessageID.append(line.split()[1])

      else:
         TxMessageFound = False
         MessageFound = False

      if MessageFound == False:
         if len(ListTemp):
            '''Get Message message ID'''
            temp = NoneTxMessage[-1]
            temp = list(temp)
            del temp[-1]
            temp = ''.join(temp) +'(' + str(hex(int(NoneTxMessageID[-1]))).upper() +  ')'
            db().RxMessageWithID.append(temp)
            db().RxMessageID.append(str(hex(int(NoneTxMessageID[-1]))).upper())
            '''Get Normal Message name'''
            db().RxMessageSignal.append(NoneTxMessage[-1])
            db().RxMessageIndex.append(db().RxMessageSignal.index(NoneTxMessage[-1]))
            ListTemp.clear()         

def findClimateNode(str):
   bFound = False
  # pattern = re.compile("?:HVAC_RCCM|FCIM")
   res1 = re.findall(r'(?:TesterPhysicalReqHVAC_RCCM)',str)
   if res1:
      pass
   else:
      res = re.findall(r'(?:HVAC_RCCM|FCIM )',str)

      if res:
         bFound = True
      else:
         return False

   return bFound

def HandleHVAC_RCCM():
   GetTxMessageName()
   #db().RxMessageSignal.reverse()
   GetRxMessageName()
   db().TxMessageToID = dict(zip(db().TxMessage, db().TxMessageID))
   db().RxMessageToID = dict(zip(db().RxMessage, db().RxMessageID))

def GetTxMessageName():
   for i in db().TxMessageIndex:
      temp = list(db().TxMessageSignal[i])
      del temp[-1]
      temp = ''.join(temp)
      db().TxMessageSignal[i] = ''.join(temp)
      db().TxMessage.append(temp)




def GetRxMessageName():
   for i in db().RxMessageIndex:
      #temp = db().RxMessageSignal[i]
      #temp = list(temp)
      temp = list(db().RxMessageSignal[i])
      del temp[-1]
      db().RxMessageSignal[i] = ''.join(temp)
      temp = ''.join(temp)
      db().RxMessage.append(temp)

def CreateXml():
   root_name = ET.Element("Database")
   node_HVAC_RCCM = ET.SubElement(root_name, "HVAC_RCCM")
   node_HVAC_RCCM_Tx = ET.SubElement(node_HVAC_RCCM, "TxMessages")
   node_HVAC_RCCM_Rx = ET.SubElement(node_HVAC_RCCM, "RxMessages")

   '''
      Create Tx messages
   '''
   for i in db().TxMessage:
      Message = ET.SubElement(node_HVAC_RCCM_Tx, "MsgName")
      Message.tag = i 
      #print(db().TxMessage)
      k = db().TxMessageSignal.index(i)

      temp = {}
      index = db().TxMessage.index(i)
      #temp[db().TxMessage[index]] = db().TxMessageID[index]
      temp["MessageID"] = db().TxMessageID[index]
      temp["Dir"] = "Tx"
      
      Message.attrib = temp
      #Message.tail = db().TxMessageToID[i]
      
      
      if k != db().TxMessageIndex[-1]:
         j=int(k)
         '''
            Create signals for each message
         '''
         #db().TxMessageIndex[db().TxMessageIndex.index(k)+1]
         while j+1 < db().TxMessageIndex[db().TxMessageIndex.index(k)+1]:
            j += 1
            Signal = ET.SubElement(Message, "SigName")
            Signal.text = db().TxMessageSignal[j]
      else:
         j=int(k)
         '''
            Create signals for each message
         '''
         #db().TxMessageIndex[db().TxMessageIndex.index(k)+1]
         while j < db().TxMessageSignal.index(db().TxMessageSignal[-1]):
            j += 1
            Signal = ET.SubElement(Message, "SigName")
            Signal.text = db().TxMessageSignal[j]
            


   '''
      Create Rx messages
   '''
   for i in db().RxMessage:
      Message = ET.SubElement(node_HVAC_RCCM_Rx, "MsgName")
      Message.tag = i
      #print(db().TxMessage)
      k = db().RxMessageSignal.index(i)

      temp = {}
      index = db().RxMessage.index(i)
      #temp[db().RxMessage[index]] = db().RxMessageID[index]
      temp["MessageID"] = db().RxMessageID[index]
      temp["Dir"] = "Rx"
      
      Message.attrib = temp
     # print(db().RxMessageIndex)
     # print(i)

      if k != db().RxMessageIndex[0]:
         j=int(k)
         '''
            Create signals for each message
         '''
        # print(k)
         #print(db().RxMessageIndex[db().RxMessageIndex.index(k)+1])
         while j-1 > db().RxMessageIndex[db().RxMessageIndex.index(k)-1]:
            j -= 1
            Signal = ET.SubElement(Message, "SigName")
            Signal.text = db().RxMessageSignal[j]
      else:
         j=int(k)
         '''
            Create signals for each message
         '''
         #db().TxMessageIndex[db().TxMessageIndex.index(k)+1]
         while j > db().RxMessageSignal.index(db().RxMessageSignal[0]):
            j -= 1
            Signal = ET.SubElement(Message, "SigName")
            Signal.text = db().RxMessageSignal[j]

   return root_name


def dict_to_xml(input_dict, root_tag, node_tag):
    """ 定义根节点root_tag，定义第二层节点node_tag
    第三层中将字典中键值对对应参数名和值
       return: xml的tree结构 """
    root_name = ET.Element(root_tag)
    for (k, v) in input_dict.items():
        node_name = ET.SubElement(root_name, node_tag)
        for key, val in v.items():
            key = ET.SubElement(node_name, key)
            key.text = val
    return root_name

def out_xml(root):
    """格式化root转换为xml文件"""
    rough_string = ET.tostring(root, 'utf-8')
    reared_content = minidom.parseString(rough_string)
    with open(out_file, 'w+') as fs:
        reared_content.writexml(fs, addindent=" ", newl="\n", encoding="utf-8")
    return True

if __name__ == '__main__':
   
   out_file = r"C:\Projects\PythonWorkspace\Python\ParseFile\database.xml"
   InitDb()
   LoadDatabase()
   HandleHVAC_RCCM()
   root = CreateXml()
   out_xml(root)

