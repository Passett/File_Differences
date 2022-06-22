#Import dependencies
import pandas as pd
import datetime
import numpy as np
import os
import shutil

#Paths for files and destination
old=r'C:\Users\richardp\Desktop\Old_EMMIE_File'
new=r'C:\Users\richardp\Desktop\New_EMMIE_File'

#Combine two daily files
FL_4337=r'C:\Users\richardp\Desktop\EMMIE Docs\FIDA_34992_PA_FL_4337_STATE_Mod_2_NONPII.csv'
FL_non_4337=r'C:\Users\richardp\Desktop\EMMIE Docs\FIDA_34992_PA_FL_Non4337_STATE_NONPII.csv'

def differences(old_path, new_path):
    #Combine daily EMMIE files into one data frame and do some prep work to the file
    df_A=pd.read_csv(FL_4337)
    df_B=pd.read_csv(FL_non_4337)
    combined=[df_A,df_B]
    df_C=pd.concat(combined)
    df_C['Disaster Number'].replace('', np.nan, inplace=True)
    df_C.dropna(subset=['Disaster Number'], inplace=True)
    df_C['Version Number']=df_C['Version Number'].astype(int)
    df_C.sort_values(['Version Number'], inplace=True)
    filename=("combinedFile_"+datetime.date.today().strftime("%Y%m%d")+".csv")
    old_file_name="Holding spot for this variable, which will be updated in a for loop below"

    #Delete files from Old_EMMIE_File folder
    for file in os.scandir(old_path):
        os.remove(file.path)

    #Move yesterday's file to Old_EMMIE_File folder
    for file in os.listdir(new_path):
        current_path=new_path+"/"+file
        shutil.copy2(current_path, old_path) #Copy CSVs
        os.remove(current_path) #Delete original files

    #set variable to path of yesterday's full file
    for item in os.listdir(old_path):
        if item.startswith("combinedFile"):
            old_file_name=old_path+"/"+item

    #get differences between yesterday and today's files, sort by Version Number, and save in "new" folder as defined above
    df_C.to_csv(new_path+"\\"+filename, index=False)
    df_Old=pd.read_csv(old_file_name)
    df_New=df_C
    df_Differences=df_New[~df_New.astype(str).apply(tuple, 1).isin(df_Old.astype(str).apply(tuple, 1))]
    df_Differences['Version Number']=df_Differences['Version Number'].astype(int)
    df_Differences.sort_values(['Version Number'], inplace=True)
    filename2=("New_or_Changed_Records_"+datetime.date.today().strftime("%Y%m%d")+".csv")
    df_Differences.to_csv(new_path+"\\"+filename2, index=False)
    print("complete")

differences(old, new)