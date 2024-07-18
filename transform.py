#Import modules
import pandas as pd
import numpy as np

#Define lists
bachelorlist = ["bachelor","Bachelor","B.A.","BA","Bsc","BSc","BSoc","LLB","LL.B","LL.B"]
masterlist = ["master","Master","Postgraduate","Post-graduate","Post-Graduate","Msc","MSc","LMM","PGDE","MA","LPC","PGCE"]
phdlist = ["PhD","Doctor","Ph.D"]
#Load Excel
xlsx = pd.ExcelFile("C:/Users/tobia/Desktop/Personal/ZIGLA/Parliamentors/DB/LinkedInAlumniData.xlsx")

#Read Experience Sheet
df = pd.read_excel(xlsx, "experience")

#Column 'current job'
df["current_job"] = "No" 
df["date"].fillna("NaN", inplace = True)
df.loc[df.date.str.contains("Present"), "current_job"] = "Yes"
df.loc[df.date.str.contains("actualidad"), "current_job"] = "Yes"

#Column 'remained_time'
df[['date', 'remained_time']] = df.date.str.split("·", expand = True)

#Export to Excel
df.to_excel("experience.xlsx")
"""
"""
#Read Education Sheet
df1 = pd.read_excel(xlsx, "education")

#Create binary columns
df1[["bachelor", "master", "phd"]] = "No" 
df1["max_education"] = "Secondary school"
df1.title.fillna("NaN", inplace = True)
#Assign 'Yes' cases for Binaries Columns "bachelor", "master", "phd"
for term in bachelorlist:
    print(list(df1.loc[df1.title.str.contains(term), "title"]))
    df1.loc[df1.title.str.contains(term), "bachelor"] = "Yes"
for term in masterlist:
    df1.loc[df1.title.str.contains(term), "master"] = "Yes"
for term in phdlist:
    df1.loc[df1.title.str.contains(term), "phd"] = "Yes"

#Assign max_education values row by row (even for same person)
df1.loc[df1["phd"]=="Yes", "max_education"] = "PhD"
df1.loc[(df1["phd"]!="Yes") & (df1["master"]=="Yes"), "max_education"] = "Master"
df1.loc[(df1["phd"]!="Yes") & (df1["master"]!="Yes") & (df1["bachelor"] == "Yes"), "max_education"] = "Bachelor"

#Filter by person and assign correctly maxeducation
for person in pd.unique(df1.url.values):
    dfperson = df1.loc[df1.url==person, :]
    if np.isin("Yes", dfperson["phd"].values):
        df1.loc[df1.url==person, "max_education"] = "PhD"
        df1.loc[df1.url==person, "phd"] = "Yes"
    elif  np.isin("Yes", dfperson["master"].values):
        df1.loc[df1.url==person, "max_education"] = "Master"
        df1.loc[df1.url==person, "master"] = "Yes"
    elif  np.isin("Yes", dfperson["bachelor"].values):
        df1.loc[df1.url==person, "max_education"] = "Bachelor"
        df1.loc[df1.url==person, "bachelor"] = "Yes"
    else:
        df1.loc[df1.url==person, "max_education"].max_education = "Secondary School"

#Export to Excel
df1.to_excel("education.xlsx")
"""
"""
#Read General Sheet to 
df = pd.read_excel(xlsx, "general")
df["Any volunteering experience"] = "Yes"
df.loc[(df.volunteering_experience.str.contains("error")) | (df.volunteering_experience.str.contains("No posee")),"Any volunteering experience"] = "No"
df.to_excel("general.xlsx")
"""
"""
#Company transformation
df = pd.read_excel("PATH_TO_FILE")
df.fillna("NaN", inplace = True)
df["active_years"] = "NaN"
df.loc[df["Founded"]!="NaN","active_years"] = df.loc[df["Founded"]!="NaN","Founded"].apply(lambda x: 2023 - int(x))
df.to_excel("compdata.xlsx")