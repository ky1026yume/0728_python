# %%
import pandas as pd
member_df = pd.read_csv("Member_Data.csv")
sales_df = pd.read_csv("Sales_Data.csv")

# %%
sales_df.query("(Store_ID == 1 or Store_ID == 3) and Amount >= 5000").head()

# %%
sales_df.query("Product_ID == 10 or Product_ID == 20 or Product_ID == 30").head()

# %%
print(sales_df["Product_ID"].dtype)


# %%
sales_df.query("Product_ID not in [10,20,30] ").head()

# %%
sales_saihinti = sales_df["Quantity"].mode()[0]
sales_df.query("Quantity == @sales_saihinti and Store_ID == 3").head()

# %%
sales_saihinti = sales_df["Quantity"].mode()[0]
print(sales_saihinti)

# %%
q1 = sales_df["Amount"].quantile(0.25)
q3 = sales_df["Amount"].quantile(0.75)
print(q1)
print(q3)
sales_df.query("@q1 <= Amount <= @q3")

# %%
print(sales_df["Product_ID"].nunique())
print(sales_df["Store_ID"].nunique())

# %%
sales_df.groupby("Product_ID")["Amount"].sum().head()

# %%
sales_df.groupby("Product_ID")["Quantity"].median().head()

# %%
sales_df.groupby("Store_ID")["Amount"].mean().head()

# %%
member_df.head()

# %%
print(member_df.groupby("Gender")["Age"].mean())

# %%
sales_df.groupby("Member_ID")["Amount"].mean().head()

# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Date_Only"] = sales_df["Transaction_Date"].dt.date
sales_df.groupby("Transaction_Date_Only")["Amount"].sum().head()

# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Date_Only"] = sales_df["Transaction_Date"].dt.date
sales_df.groupby("Transaction_Date_Only")["Amount"].sum().reset_index().sort_values(by = "Amount").head()

# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Month_Only"] = sales_df["Transaction_Date"].dt.month
sales_df.groupby("Transaction_Month_Only")["Amount"].sum().reset_index().head()

# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Month_Only"] = sales_df["Transaction_Date"].dt.to_period("M")
print(sales_df["Transaction_Month_Only"].reset_index())
sales_amount_df = sales_df.groupby("Transaction_Month_Only")["Amount"].sum().reset_index()
sales_amount_df["Amount"].diff().abs().reset_index()


# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Week_Only"] = sales_df["Transaction_Date"].dt.weekday
print(sales_df["Transaction_Week_Only"].reset_index())
sales_df.groupby("Transaction_Week_Only")["Amount"].sum().reset_index().head()

# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Week2_Only"] = sales_df["Transaction_Date"].dt.to_period("W")
print(sales_df["Transaction_Week2_Only"].reset_index())
sales_df.groupby("Transaction_Week2_Only")["Amount"].sum().reset_index().head()

# %%
sales_df["Transaction_Date"] = pd.to_datetime(sales_df["Transaction_Date"])
sales_df["Transaction_Week2_Only"] = sales_df["Transaction_Date"].dt.to_period("W")
print(sales_df["Transaction_Week2_Only"].reset_index())
weekly_sales = sales_df.groupby("Transaction_Week2_Only")["Amount"].sum().reset_index()
(weekly_sales["Amount"].pct_change()*100).head()

# %%


# %%
sales_df["Transaction_Week_Only2"] = pd.to_datetime(sales_df["Transaction_Date"])
print(sales_df.head(1))
sales_df = sales_df.drop("Transaction_Week_Only2",axis=1)
print(sales_df.head(1))


# %%
sales_ooguti_df = sales_df.query("Amount >= 1000")
sales_ooguti_df.head()
sales_ooguti_df.groupby(["Store_ID","Product_ID"])["Amount"].sum().reset_index().head()

# %%
sales_sore_df = sales_df.groupby("Store_ID")["Amount"].sum().reset_index()
sales_sore_df.query("Amount >= 300000")

# %%
sales_member_df = sales_df.groupby("Member_ID")["Transaction_ID"].count()
sales_member_df.head()


# %%
member_transaction_count = sales_df.groupby("Member_ID")["Transaction_ID"].count().reset_index()
member_transaction_count.query("Transaction_ID >= 2")

# %%
age_bin = [min(member_df["Age"])-1,30,50,65,max(member_df["Age"])]
age_labels = ["-30", "31-50", "51-65", "66-"]
member_df["Age_Group"]  = pd.cut(member_df["Age"],bins = age_bin,labels = age_labels) 
member_df.groupby("Age_Group")["Member_ID"].count()

# %%
days_bin = [min(member_df["Days_Since_Registration"])-1,365,710,max(member_df["Days_Since_Registration"])]
days_lebel = ["〜1年","1年〜2年", "2年〜"]
member_df["group_kainin"] = pd.cut(member_df["Days_Since_Registration"],bins=days_bin,labels=days_lebel)
member_df.groupby("group_kainin")["Member_ID"].count().reset_index().head()

# %%


# %%
merge_df = pd.merge(member_df,sales_df,on="Member_ID",how="inner")
merge_df.drop(["Transaction_Week2_Only","Transaction_Week_Only","Transaction_Month_Only","Transaction_Date_Only"],axis=1,inplace=True)
merge_df.head()

# %%
merge_df.groupby("Gender")["Amount"].mean().reset_index()

# %%
merge_df.groupby("Gender")["Quantity"].mean().reset_index()

# %%
merge_df.groupby(["Gender","Store_ID"])["Transaction_ID"].count().reset_index().head()

# %%
merge_Store_df = merge_df.query("Store_ID in [1,5,9]")
merge_Store_df
merge_Store_df.groupby("Store_ID")["Quantity"].sum().head()

# %%
merge_df["Transaction_Date"] = pd.to_datetime(merge_df["Transaction_Date"])
last_10_days = merge_df[merge_df["Transaction_Date"] > merge_df["Transaction_Date"].max() - pd.Timedelta(days=10) ]
last_10_days.groupby("Transaction_Date")["Amount"].sum()

# %%
merge_df.groupby("Member_ID")["Amount"].sum().nlargest(5)

# %%
merge_df.groupby("Member_ID")["Transaction_Date"].max().reset_index().head()

# %%
merge_df.groupby("Member_ID")["Transaction_Date"].min().reset_index().head()

# %%
df_tmp = sales_df.groupby("Member_ID").agg({"Transaction_Date":["max", "min"]}).reset_index()
# df_tmp.head()
df_tmp.columns = ["Member_ID", "Transaction_Date_Max", "Transaction_Date_Min"]
# df_tmp.head()
df_tmp.query("Transaction_Date_Max != Transaction_Date_Min")


# %%
print(merge_df["Member_ID"].dtype)
merge_df["Member_ID"] = merge_df["Member_ID"].astype(str)
print(merge_df["Member_ID"].dtype)
merge_df[merge_df["Member_ID"].str.contains("2")]



# %%
print(merge_df["Product_ID"].dtype)
merge_df["Product_ID"] = merge_df["Product_ID"].astype(str)
print(merge_df["Product_ID"].dtype)
merge_df[merge_df["Product_ID"].str.contains("^1")]

# %%
print(merge_df["Store_ID"].dtype)
merge_df["Store_ID"] = merge_df["Store_ID"].astype(str)
print(merge_df["Store_ID"].dtype)
merge_df[merge_df["Store_ID"].str.contains("5$")]

# %%
print(merge_df["Transaction_ID"].dtype)
merge_df["Transaction_ID"] = merge_df["Transaction_ID"].astype(str)
merge_df[merge_df["Transaction_ID"].str.contains("[1,3,5,7,9]$")].head()

# %%
print(merge_df["Member_ID"].dtype)


# %%
merge_df[merge_df["Member_ID"].str.contains("^¥d{3}$")].head()

# %%
merge_df[merge_df["Member_ID"].str.contains("^13")].head()

# %%
merge_df[merge_df["Member_ID"].str.contains(r"^1\d")].head()

# %%
tep_df = merge_df.groupby("Product_ID")["Quantity"].agg(lambda x : x.mode()[0]).reset_index()
tep_df.query("Quantity >= 3")

# %%
tep_df2 = merge_df.groupby("Product_ID")["Quantity"].agg(lambda x : x.mode()[0]).reset_index()
tep_df2[tep_df2["Quantity"] == tep_df2["Quantity"].max()]

# %%
tep_df3 = merge_df.groupby("Store_ID")["Amount"].var().reset_index().sort_values(by="Amount",ascending=False)
tep_df3.head()

# %%
tep_df4 = merge_df.groupby("Member_ID")["Amount"].std().reset_index()
tep_df4.query("Member_ID > '4000'")

# %%
member_df.groupby("Age")["Member_ID"].count().reset_index().sort_values(by = "Member_ID", ascending=False)

# %%
# print(member_df["Age"].dtype)
age_df = member_df["Age"].median()
# print(age_df)
member_df.query("Age >= @age_df")


# %%
Amount_df = pd.concat([merge_df[["Amount","Transaction_ID"]],merge_df["Amount"].rank(method="first",ascending=False)],axis=1)
Amount_df.columns = ["Amount","Transaction_ID","Ranking"]
Amount_df.sort_values(by="Amount")

# %%
df_member = merge_df.groupby("Member_ID")["Amount"].sum().reset_index()
df_member = pd.concat([df_member[["Member_ID","Amount"]],df_member["Amount"].rank(pct= True)],axis=1)
df_tmp.columns = ["Member_ID", "Amount", "Percentile"]
df_tmp.sort_values(by="Percentile")

# %%
member_df.head()

# %%
pivot_df = merge_df.pivot_table(index="Age_Group",columns="Gender",values="Amount",aggfunc="mean")
pivot_df.head()

# %%
pivot_df.reset_index().melt(id_vars="Age_Group", var_name="Gender", value_name="Average_Amount")

# %%
pivot_df = merge_df.pivot_table(index="Age_Group",columns="Gender",values="Transaction_ID",aggfunc="count")
pivot_df.head()

# %%
merge_df["Amount_flag"] = (merge_df["Amount"] >= 2000).astype(int)
merge_df.head()

# %%
merge_df["Quantity_flag"] = (merge_df["Quantity"] > merge_df["Quantity"].mean()).astype(int)
merge_df.head()

# %%
# merge_df["Amount"] = merge_df["Amount"].astype(int)
# merge_df["Member_ID"] = merge_df["Member_ID"].astype(int)
Amount_df = merge_df.groupby("Member_ID")["Amount"].sum()
q1,q2,q3 = Amount_df.quantile([0.25,0.5,0.75])
labels1 = [1,2,3,4,]
bins = [0,q1,q2,q3,Amount_df.reset_index()["Amount"].max()]

merge_df = merge_df.merge(Amount_df.rename("Total2"),on="Member_ID")
merge_df["Amount_pct"] = pd.cut(merge_df["Total2"],bins=bins,labels=labels1)

# Amount_df.head()

# %%
labels2 = ["Low","Medium","high"]
merge_df["Quantity_label"] = pd.qcut(merge_df["Quantity"],q=3,labels=labels2)
merge_df.head()

# %%
gender_dumi = pd.get_dummies(merge_df["Gender"])
# gender_dumi.head()
merge_df = pd.concat([merge_df,gender_dumi],axis=1)
merge_df.head()

# %%
# pip install scikit-learn
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
merge_df["Amount_Stead"] = scaler.fit_transform(merge_df[["Amount"]])

# %%
sales_df.sample(frac=0.1).head()

# %%
member_df.sample(frac=0.2).head()

# %%
merge_df["Amount"] = merge_df["Amount"].astype(int)
print(merge_df["Amount"].dtype)
merge_df = merge_df.loc[:, ~merge_df.columns.duplicated()]

# print(merge_df.columns)

merge_df.query("Amount >= 5000").sample(n=5)

# %%
merge_df[merge_df["Amount"] >= 5000].sample(n=5)

# %%
merge_df.to_csv("XX.csv", index=False, encoding="utf-8-sig")

# %%



