# -*- coding: utf-8 -*-

import arcpy
import os

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox        
        self.tools = [SimpleBufferTool, MultiBufferTool]



class MultiBufferTool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Multi-Distance Buffer"
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
                                      parameterType="Required",
                                      direction="Input",
                                      multiValue=True) #[]
        in_distance.values = [200, 300]
        
        out_fc = arcpy.Parameter(displayName="Output Buffer",
                                 name="out_buffer",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",
                                 direction="Output") 
        
        parameter_list = [in_fc, in_distance, out_fc]
        return parameter_list

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        
        #Add our custom validation    
            
        #Validate selected layer shape
        in_fc = parameters[0] #Get reference to the param object as is
        
        if in_fc and in_fc.value:            
            desc = arcpy.Describe(in_fc.value)
            shape_type = desc.shapeType #Point Plyline Polygon
            
            if shape_type not in ["Point", "Polygon"]:
                in_fc.setErrorMessage("Invalid shape type. Only Point layers are supported")
             
             
        #Validating distance value to make sure its > 0 and < 300
        buffer_distance_param = parameters[1] #"10;20;30"
        
        if buffer_distance_param.valueAsText:
            #distance_as_str = str(buffer_distance_param.valueAsText)
            distance_list = buffer_distance_param.valueAsText.split(";") #[10, 20, 30]
            
            for dist in distance_list: #for dist in [10, 20, 30]
                float_dist = float(dist)
                if float_dist:
                    if float_dist <= 0:
                        buffer_distance_param.setErrorMessage("Buffer distance must be greater than zero")
                        
                    if float_dist > 300:
                        buffer_distance_param.setWarningMessage("Distances greater than 300 might impact tool performance")
               
        
        return
        
        
    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.AddMessage("Reading input parameters...")
        
        in_fc = parameters[0].value
        buffer_distances = parameters[1].valueAsText  #"10;20;30"
        #out_buffer_fc = parameters[2].valueAsText
        
        #Reading Multi-Distance value
        if buffer_distances:            
            distance_list = buffer_distances.split(";") #[10, 20, 30]
            
            for dist in distance_list: #for dist in [10, 20, 30]
                float_dist = float(dist)
                if float_dist: #Create buffer for each distance
                    
                    #Create temp feature class for current budffer distance
                    #for each distance, we need unique fc name   
                    unique_fc_name = arcpy.CreateUniqueName("out_buf", arcpy.env.scratchGDB) #{scratchGDB_path\out_buf_}   
                    #unique_fc_name = create_unique_name("out_buf", arcpy.env.scratchGDB) #{scratchGDB_path\out_buf_}   
                                                        
                    arcpy.AddMessage("Create buffer at {0} with {1} Meter".format(unique_fc_name, float_dist))
                                             
                    arcpy.analysis.Buffer(in_features=in_fc,
                                        out_feature_class=unique_fc_name, 
                                        buffer_distance_or_field="{0} Meters".format(float_dist))
                    
        arcpy.AddMessage("Buffer created successfully...")
        
        
        return


def create_unique_name(base_name, in_worksapce):
    #check if there is a FC with the base_name       
    fc_path = os.path.join(in_worksapce, base_name)
    
    counter = 0
    while arcpy.Exists(fc_path):
        fc_path = os.path.join(in_worksapce, "{0}_{1}".format(base_name, counter))
        counter+= 1
        
    return fc_path


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

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        
        #Add our custom validation    
            
        #Validate selected layer shape
        in_fc = parameters[0] #Get reference to the param object as is
        
        if in_fc and in_fc.value:            
            desc = arcpy.Describe(in_fc.value)
            shape_type = desc.shapeType #Point Plyline Polygon
            
            if shape_type not in ["Point", "Polygon"]:
                in_fc.setErrorMessage("Invalid shape type. Only Point layers are supported")
             
        #Validating distance value to make sure its > 0 and < 300
        buffer_distance = parameters[1]
        
        if buffer_distance.value <=0:
            buffer_distance.setErrorMessage("Buffer distance must be greater than zero")
        
        if buffer_distance.value > 300:
            #Warning messages don't prevent tool from running
            buffer_distance.setWarningMessage("Distances greater than 300 might impact tool performance")     
               
        
        return
        
        
    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.AddMessage("Reading input parameters...")
        
        in_fc = parameters[0].value
        buffer_distance = parameters[1].value
        out_buffer_fc = parameters[2].valueAsText
            
        #Validate Optional parameters
        if not buffer_distance or buffer_distance == 0:
            buffer_distance = 100
        # else: #User set his/her own value
        #     if buffer_distance < 0 or buffer_distance > 300:
        #         arcpy.AddError("Invalid buffer distance {0}. Buffer distance must be between 0 and 300. Exiting...".format(buffer_distance))
        #         #Log error to Table
        #         return
        
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