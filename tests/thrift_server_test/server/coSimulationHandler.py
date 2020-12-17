import hashlib
import sys
# your gen-py dir
sys.path.append('./gen-py')
from ril import *
from ril.ttypes import *
from FileData import FileData

class CoSimulationHandler:

    def __init__(self):
        self.instances= dict()

    def getVersion(self):
        return "0.1"

    def getTypesPlatform(self):
        return "linux64"

    def instanciate(self, instanceName, fmuType, fmuGUID, fmuResourceLocation, visible, loggingOn):
        """
        Parameters:
         - instanceName
         - fmuType
         - fmuGUID
         - fmuResourceLocation
         - visible
         - loggingOn
        """        
       
        componentRef=int(hashlib.sha1(instanceName.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
        self.instances[instanceName]=FileData(instanceName)
        print (f"call: instanciate({instanceName}, {fmuType}, {fmuGUID}, {fmuResourceLocation}, {visible}, {loggingOn})  ==> {componentRef}")
        return Instance(instanceName, componentRef, fmuGUID, ModelState.modelInstantiated)

    def setupExperiment(self, c, toleranceDefined, tolerance, startTime, stopTimeDefined, stopTime):
        """
        Parameters:
         - c
         - toleranceDefined
         - tolerance
         - startTime
         - stopTimeDefined
         - stopTime

        """
        print (f"call: setupExperiment({c}, {toleranceDefined}, {tolerance}, {startTime}, {stopTimeDefined}, {stopTime})")
        return Status.OK

    def enterInitializationMode(self, c):
        """
        Parameters:
         - c

        """
        print (f"call: enterInitializationMode({c})")
        return Status.OK

    def exitInitializationMode(self, c):
        """
        Parameters:
         - c

        """
        print (f"call: exitInitializationMode({c})")
        return Status.OK

    def terminate(self, c):
        """
        Parameters:
         - c

        """
        print (f"call: terminate({c})")
        data = self.instances[c.instanceName]   
        data.dump()   
        return Status.OK

    def reset(self, c):
        """
        Parameters:
         - c

        """
        print (f"call: reset({c})")
        return Status.OK

    def freeInstance(self, c):
        """
        Parameters:
         - c

        """
        print (f"call: freeInstance({c})")
        return Status.OK

    def getReal(self, c, refs):
        """
        Parameters:
         - c
         - refs

        """
        print (f"call: getReal({c}, {refs})")
        data = self.instances[c.instanceName]
        result=[]
        for ref in refs:
            value = data.read(ref)
            if value is None:
                result.append(0.0)
            else:
                result.append(value)        
        print (f"return {result}")
        return result

    def getInteger(self, c, refs):
        """
        Parameters:
         - c
         - refs

        """
        print (f"call: getInteger({c}, {refs})")
        data = self.instances[c.instanceName]
        result=[]
        for ref in refs:
            value = data.read(ref)
            if value is None:
                result.append(0)
            else:
                result.append(value)        
        print (f"return {result}")
        return result

    def getBoolean(self, c, refs):
        """
        Parameters:
         - c
         - refs

        """
        print (f"call: getBoolean({c}, {refs})")
        data = self.instances[c.instanceName]
        result=[]
        for ref in refs:
            value = data.read(ref)
            if (value is None) or (value == 0 ):
                result.append(False)
            else:
                result.append(value)        
        print (f"return {result}")
        return result

    def getString(self, c, refs):
        """
        Parameters:
         - c
         - refs

        """
        #print (f"call: getString({c}, {refs})")
        data = self.instances[c.instanceName]
        result=[]
        for ref in refs:
            value = data.read(ref)
            if value is None:
                result.append("")
            else:
                result.append(value)        
        return result

    def setReal(self, c, ref_values):
        """
        Parameters:
         - c
         - ref_values

        """
        
        data = self.instances[c.instanceName]
        for ref in ref_values:
            data.write(ref, ref_values.get(ref))
        print (f"call: setReal({c}, {ref_values})")
        return Status.OK        

    def setInteger(self, c, ref_values):
        """
        Parameters:
         - c
         - ref_values

        """        
        data = self.instances[c.instanceName]
        for ref in ref_values:
            data.write(ref, ref_values.get(ref))
        print (f"call: setInteger({c}, {ref_values})")
        return Status.OK

    def setBoolean(self, c, ref_values):
        """
        Parameters:
         - c
         - ref_values

        """
        
        data = self.instances[c.instanceName]
        for ref in ref_values:
            data.write(ref, ref_values.get(ref))
        print (f"call: setBoolean({c}, {ref_values})")
        return Status.OK

    def setString(self, c, ref_values):
        """
        Parameters:
         - c
         - ref_values

        """
        
        data = self.instances[c.instanceName]
        for ref in ref_values:
            data.write(ref, ref_values.get(ref))
        print (f"call: setString({c}, {ref_values})")
        return Status.OK

    def setRealInputDerivatives(self, c, ref_orders, ref_values):
        """
        Parameters:
         - c
         - ref_orders
         - ref_values

        """
        print (f"call: setRealInputDerivatives({c}, {ref_orders}, {ref_values})")
        return Status.OK

    def setRealOutputDerivatives(self, c, ref_orders, ref_values):
        """
        Parameters:
         - c
         - ref_orders
         - ref_values

        """
        print (f"call: setRealOutputDerivatives({c}, {ref_orders}, {ref_values})")
        return Status.OK

    def cancelStep(self, c):
        """
        Parameters:
         - c

        """
        print (f"call: cancelStep({c})")
        return Status.OK

    def doStep(self, c, currentCommunicationPoint, communicationStepSize, noSetFMUStatePriorToCurrentPoint):
        """
        Parameters:
         - c
         - currentCommunicationPoint
         - communicationStepSize
         - noSetFMUStatePriorToCurrentPoint

        """
        print (f"call: doStep({c}, {currentCommunicationPoint}, {communicationStepSize}, {noSetFMUStatePriorToCurrentPoint})")
        data = self.instances[c.instanceName]      
        data.doStep()
        return Status.OK

    def getStatus(self, c, s):
        """
        Parameters:
         - c
         - s

        """
        print (f"call: getStatus({c}, {s})")
        return Status.OK

    def getIntegerStatus(self, c, s):
        """
        Parameters:
         - c
         - s

        """
        print (f"call: getIntegerStatus({c}, {s})")
        return 1

    def getRealStatus(self, c, s):
        """
        Parameters:
         - c
         - s

        """
        print (f"call: getRealStatus({c}, {s})")
        return 0.0

    def getBooleanStatus(self, c, s):
        """
        Parameters:
         - c
         - s

        """
        print (f"call: getBooleanStatus({c}, {s})")
        return True

    def getStringStatus(self, c, s):
        """
        Parameters:
         - c
         - s

        """
        print (f"call: getStringStatus({c}, {s})")
        return ""