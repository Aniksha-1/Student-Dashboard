import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Students and AI readiness",page_icon=":chart_with_upwards_trend:",layout="wide")
st.title(":chart_with_upwards_trend: Students and AI readiness")
st.markdown("<style>div.block-container{padding-top:2 rem;}</style>",unsafe_allow_html=True)
fl=st.file_uploader(":file_folder:Upload your file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
 filename=fl.name
 st.write(filename)
 df=pd.read_excel(fl)
else:
 df=pd.read_excel("Student_AI_Readiness_Dataset.xlsx")

st.sidebar.header("Choose your filter:")
department=st.sidebar.multiselect(
   "Department",
    df["Department"].unique()
)
year=st.sidebar.multiselect(
   "Year",
   df["Year"].unique()
)
level=st.sidebar.multiselect(
   "Readiness Level",
    df["Readiness_Level"].unique()
      )
 

df = pd.read_excel("Student_AI_Readiness_Dataset.xlsx")


st.title("📊 Overview")
total_students=len(df)
average_score=df["AI_Readiness_Score"].mean()
high=len(df[df["Readiness_Level"]=="High"])
medium=len(df[df["Readiness_Level"]=="Medium"])

low=len(df[df["Readiness_Level"]=="Low"])

col1,col2,col3,col4,col5=st.columns(5)
col1.metric("Students",total_students)
col2.metric("Average Score",average_score)
col3.metric("High",high)
col4.metric("Medium",medium)
col5.metric("LoW",low)
filtered_df=df.copy()
if department:
 filtered_df=df[df["Department"].isin(department)]
if year:
 filtered_df=df[df["Year"].isin(year)]
if level:
 filtered_df=filtered_df[filtered_df["Readiness_Level"].isin(level)]
dep_count=filtered_df.groupby("Department").size().reset_index(name="Count")

col6,col7=st.columns(2)
with col6:
 st.subheader("Students by Department")
fig = px.bar(
    dep_count,
    x="Department",
    y="Count",
    color="Department",
    text="Count",
    template="seaborn"
)
st.plotly_chart(fig,use_container_width=True)

level = filtered_df["Readiness_Level"].value_counts().reset_index()

level.columns = ["AI_Readiness", "Count"]

fig1 = px.pie(
    level,
    names="AI_Readiness",
    values="Count",
    hole=0.5,
    title="AI Readiness Level")
with col7:
  st.plotly_chart(fig1, use_container_width=True)
col8=st.columns(1)
skills = filtered_df[
    [
        "Python_Skill",
        "SQL_Skill",
        "AI_Knowledge",
        "Ethics_Awareness",
        "Interest_Level"
    ]
].mean()

col8,col9,col10=st.columns(3)

skills = skills.reset_index()

skills.columns = ["Skill", "Average"]
fig2 = px.bar(
    skills,
    x="Skill",
    y="Average",
    color="Average",
    text_auto=".2f",
    title="Average Skill Levels"
)
with col8:
 st.plotly_chart(fig2, use_container_width=True)
dept_skill = filtered_df.groupby("Department")["Python_Skill"].mean()

dept_skill = dept_skill.reset_index()
fig3 = px.bar(
    dept_skill,
    x="Department",
    y="Python_Skill",
    color="Department",
    title="Average Python Skill by Department",
    text_auto=".2f"
)
with col9:
 st.plotly_chart(fig3, use_container_width=True)
top = filtered_df.sort_values(
    "AI_Readiness_Score",
    ascending=False
).head(10)

st.subheader(" Top 10 AI Ready Students")

st.dataframe(top)
df=pd.read_excel("Student_AI_Readiness_Dataset.xlsx")
usage_count=df["ChatGPT_Usage"].value_counts().reset_index()
usage_count.columns =["Usage","Students"]
fig4=px.bar(
 usage_count,
 x='Usage',
 y='Students',
 color='Usage',
 text='Students',
 title='AI Usage Among Students'
 )
fig4.update_layout(
 xaxis_title="Usage Frequency",
 yaxis_title="Number of Students"
)
with col10:
 st.plotly_chart(fig4,use_container_width=True)
 
 
st.subheader("🔍 Key Insights")

st.success("✔ Most students use AI tools weekly")

st.info("✔ Python skill is higher than SQL skill.")

st.warning("✔ AI Certification completion is low.")

st.success("✔ AI&DS students have the highest readiness score.")


