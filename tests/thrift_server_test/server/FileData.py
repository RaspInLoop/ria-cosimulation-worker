import hashlib
import sys
# your gen-py dir
sys.path.append('./gen-py')
from ril.ttypes import *
import json


class FileData():

    def __init__(self, instanceName=None):
        self.inputfilename=f"/var/lib/data-test/{instanceName}_inputs.json"
        self.outputfilename=f"/var/lib/data-test/{instanceName}_outputs.json"
        self.outputs={}
        try:
            with open(self.inputfilename) as f:
                self.inputs = json.load(f)
        except:
            self.inputs ={}
        self.step_idx = 0

    def doStep(self):
        self.step_idx+=1

    def read(self, var_ref):
        if (str(var_ref) in self.inputs):
            var_inputs = self.inputs.get(str(var_ref))
            if (len(var_inputs) > self.step_idx):
                return var_inputs[self.step_idx]
            else:
                return None
        else:
            return None

    def write(self, var_ref, value):
        if (not str(var_ref) in self.outputs):
            self.outputs[str(var_ref)] = []
        var_outputs = self.outputs.get(str(var_ref))
        if (len(var_outputs) <= self.step_idx ):
            var_outputs.append(value)
        else:
            var_outputs[self.step_idx] = value
        
    def dump(self):
        with open(self.outputfilename, 'w') as outfile:
            json.dump( self.outputs, outfile)      
