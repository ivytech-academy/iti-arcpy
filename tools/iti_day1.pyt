# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox        
        self.tools = [SimpleBufferTool]



class SimpleBufferTool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Simple Buffer"
        self.description = "This is a description for my tools"
        #self.category = "Extract\\Main"

    def getParameterInfo(self):
        """Define the tool parameters."""
        
        #Define Input feature param
        in_fc = arcpy.Parameter(displayName="Input Feature Layer",
                                  name="in_buffer_fc",
                                  datatype="GPFeatureLayer",
                                  parameterType="Required",
                                  direction="Input")
        
        #Define distance parametr
        in_distance = arcpy.Parameter(displayName="Set Buffer Distance",
                                      name="in_buffer_distance",
                                      datatype="GPDouble",
                                      parameterType="Optional",
                                      direction="Input")
        in_distance.value = 200
        
        out_fc = arcpy.Parameter(displayName="Output Buffer",
                                 name="out_buffer",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",
                                 direction="Output") 
        
        parameter_list = [in_fc, in_distance, out_fc]
        return parameter_list

    
    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.AddMessage("Reading input parameters...")
        
        in_fc = parameters[0].value
        buffer_distance = parameters[1].value
        out_buffer_fc = parameters[2].valueAsText
            
        #Validate Optional parameters
        if not buffer_distance or buffer_distance == 0:
            buffer_distance = 500 
        
        arcpy.AddMessage("Create buffer at {0} with {1} Meter".format(out_buffer_fc, buffer_distance))
        
        #Create buffer
        arcpy.AddMessage("Creating buffer...")
        
        arcpy.analysis.Buffer(in_features=in_fc,
                              out_feature_class=out_buffer_fc, 
                              buffer_distance_or_field="{0} Meters".format(buffer_distance))
        
        arcpy.AddMessage("Buffer created successfully...")
        
        
        return

    


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Select"
        self.description = "This is a description for my tools"
        

    def getParameterInfo(self):
        """Define the tool parameters."""
        params = None
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return