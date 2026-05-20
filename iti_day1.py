import arcpy
import time
import os

#print("arcpy loaded")
#print(arcpy.GetInstallInfo())


def write_to_file(content):
    file_path = r"C:\Data\tmp_files\report.txt"
    with open(file_path, "a+") as f:
        f.writelines("\n")
        f.writelines(content)
        


def list_all_fc(in_workspace):
    #Set workspace
    arcpy.env.workspace = in_workspace    
    all_fc = []    
    #List root fcs
    fc_list = arcpy.ListFeatureClasses()    
    #list datasets
    ds_list = arcpy.ListDatasets()
    for ds in ds_list:
        ds_fc = arcpy.ListFeatureClasses(feature_dataset=ds)
        all_fc += ds_fc
    
    all_fc += fc_list
     
    return all_fc
        


#Get count of features
def count_features(in_fc):    
    count = arcpy.management.GetCount(in_fc)
    
    return count


def log_message(message=None, message_type=None, message_list=None):    
     
    in_table_path = "process_log"
    fields = ["message", "message_type", "creation_date"]
    
    with arcpy.da.InsertCursor(in_table_path, fields) as ins_cursor:
        if message_list:
            for msg in message_list:
                ins_cursor.insertRow(msg)
        else:                    
            ins_cursor.insertRow((message, message_type, time.strftime("%d/%m/%y %H:%M:%S")))
    
    print("Message Logged successfully")
    
    
def log_message_list(msg_list):    
     
    in_table_path = "process_log"
    fields = ["message", "message_type", "creation_date"]
    
    with arcpy.da.InsertCursor(in_table_path, fields) as ins_cursor:        
        for msg in msg_list:
            ins_cursor.insertRow(msg)
    
    print("Message Logged successfully")


def copy_cp_to_new_fc():
    #declare variables
    in_cp_fc = r"C:\Data\code\py\maps\ITI\ITI.gdb\reference\ref_point"

    # Input polygon feature class
    in_sector_fc = r"C:\Data\code\py\maps\ITI\ITI.gdb\reference\sectors"

    # Output feature class
    output_cp_fc = r"C:\Data\code\py\maps\ITI\ITI.gdb\new_ref_point"

    # Polygon field that contains the polygon name/type
    sector_name_field = "Name"

    # Target sector value value to filter
    sector_value = "Sector-1"
    
    
    #Make layer from Sector feature class
    sector_filter = "Upper({0}) = '{1}'".format(sector_name_field, sector_value.upper())
    
    #sector_filter = "Upper(Name) = 'SECTOR-2'"
    
    #Select Sector feature with Name=Sector-2    
    # sector_layer = arcpy.MakeFeatureLayer_management(in_sector_fc, "sector_lyr",
    #                                                  where_clause=sector_filter)
    
    # cp_layer = arcpy.MakeFeatureLayer_management(in_cp_fc, "cp_lyr")
    
    #Select CP points inside Sector-2
    # arcpy.SelectLayerByLocation_management(
    #     in_layer=cp_layer,
    #     overlap_type="WITHIN", 
    #     select_features=sector_layer,
    #     selection_type="NEW_SELECTION",
    #     invert_spatial_relationship="INVERT")
    
    # arcpy.SelectLayerByLocation_management(
    #     in_layer=cp_layer,
    #     selection_type="SWITCH_SELECTION")
            
    #Get number of selcted features
    # seclcted_count = arcpy.GetCount_management(cp_layer)
    # print("Selected CP:" + str(seclcted_count))
    
    #Copy selected Cp features to new feature class
    # arcpy.env.overwriteOutput = True
    # arcpy.management.CopyFeatures(cp_layer, output_cp_fc)
    
    #1-Get Target Sector features (Searcch cursor)
    target_sector = []
    with arcpy.da.SearchCursor(in_sector_fc, ["OBJECTID", "SHAPE@"], sector_filter) as sec_cur:
        for row in sec_cur:
            target_sector.append(row[1])
                
    #2-Get CP features that are within the retrieved Sector (from step1)
    cp_to_be_insert = []
    with arcpy.da.SearchCursor(in_cp_fc, ["SHAPE@", "code"]) as cp_cur:        
        for row in cp_cur:
            for sector_geom in target_sector:
                if sector_geom.contains(row[0]):
                    cp_to_be_insert.append(row)

    for cp in cp_to_be_insert:
        print(cp[1])
                                                
    #3- Create new feature calss    
    output_cp_fc = r"C:\Data\code\py\maps\ITI\ITI.gdb\new_ref_point3"
    out_path = os.path.dirname(output_cp_fc)
    fc_name = os.path.basename(output_cp_fc)

    cp_info = arcpy.Describe(in_cp_fc)
    spatial_ref = cp_info.spatialReference

    arcpy.management.CreateFeatureclass(
        out_path,
        fc_name,
        "POINT",
        template=in_cp_fc,
        spatial_reference=spatial_ref
    )
    
    field_list = arcpy.ListFields(in_cp_fc)
    cp_field_names = []
    for f in field_list:
        if f.type not in ("OID"):
            cp_field_names.append(f.name)
    
    #4-Loop over matching CP features and insert into new feature class
    with arcpy.da.InsertCursor(output_cp_fc, cp_field_names) as ins_cur:
        for cp_row in cp_to_be_insert:
            ins_cur.insertRow(cp_row)
        
    print("CP Inserted successfully")
    
    
    
    
if __name__ == "__main__":
    write_to_file("From Main")
    
    workspace = r"C:\Data\code\py\maps\ITI\ITI.gdb"
    
    fc_list = list_all_fc(workspace)
    print(type(fc_list))
    
    #print("List of Feature Classes:")
    # for fc in fc_list:
    #     result = count_features(fc)
    #     print("Feature Class {0} has ({1}) records/features".format(fc, result))
        
    arcpy.env.workspace = workspace
    #log_message("Careful! Sytanx error Trying InsertCursor", "Warning")
    
    messages = [
        ("This is error!", "Error", time.strftime("%d/%m/%y %H:%M:%S")),
        ("This is Info", "Info", time.strftime("%d/%m/%y %H:%M:%S")),
        ("This is Warning!", "Warning", time.strftime("%d/%m/%y %H:%M:%S"))        
    ]
    
    #log_message(message_list=messages)
    
    copy_cp_to_new_fc()