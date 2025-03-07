import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from function import DataAnalysis
sns.set(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("../Data/all_data.csv")
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)


for column in datetime_cols:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Mohamad Baskoro Aji")

    # Logo Image
    st.image("logo.png")

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

function = DataAnalysis(main_df)

sum_order_items_df = function.create_sum_order_items_df()
monthly_orders_df = function.create_monthly_orders_df()
cust_state_df, most_common_state = function.create_cust_state_df()
rating_category_product = function.product_review_df()
payment_method_customer, most_popular_payment = function.customer_payment_method_df()
rfm_df = function.rfm_analysis()

# Title
st.header("E-Commerce Dashboard")

# Monthly Orders
st.subheader("Monthly Orders")

# col1= st.columns(2)

# with col1:
#     total_order = monthly_orders_df["order_count"].sum()
#     st.markdown(f"Total Order: **{total_order}**")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    monthly_orders_df["order_approved_at"],
    monthly_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["order_id"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df.iloc[0]["product_category_name_english"]
    st.markdown(f"Top Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_id", y="product_category_name_english", hue="product_category_name_english" , data=sum_order_items_df.head(5), palette=colors, ax=ax[0], legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="order_id", y="product_category_name_english",hue="product_category_name_english", data=sum_order_items_df.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1], legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# Review Score
st.subheader("Review Score")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = rating_category_product["review_score"].mean().round(1)
    st.markdown(f"Average Review Score: **{avg_review_score}**")
    
with col2:
    top_items = rating_category_product.iloc[0]["product_category_name_english"]
    st.markdown(f"Highest Review Score Product Cateogry: **{top_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="review_score", y="product_category_name_english", hue="product_category_name_english" , data=rating_category_product.head(5), palette=colors, ax=ax[0], legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk paling tinggi rating", loc="center", fontsize=18)
ax[0].tick_params(axis ='y', labelsize=15)

sns.barplot(x="review_score", y="product_category_name_english",hue="product_category_name_english", data=rating_category_product.sort_values(by="review_score", ascending=True).head(5), palette=colors, ax=ax[1], legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling rendah rating", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")

most_popular_payment = payment_method_customer.payment_type.value_counts().index[0]
st.markdown(f"Most Popular Payment Type: **{most_popular_payment}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=payment_method_customer.payment_type.value_counts().index,
            y=payment_method_customer.transaction.values,
            data=payment_method_customer,
            palette=["#880808" if state == most_popular_payment else "#068DA9" for state in payment_method_customer.payment_type.value_counts().index],
            legend=False
            )

plt.title("Number customers from State", fontsize=15)
plt.xlabel("State")
plt.ylabel("Number Customers")
plt.xticks(fontsize=10)

st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Dempgraphic")

most_common_state = cust_state_df.customer_state.value_counts().index[0]
st.markdown(f"Most Common State: **{most_common_state}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=cust_state_df.customer_state.value_counts().index,
            y=cust_state_df.customer_count.values,
            data=cust_state_df,
            palette=["#880808" if state == most_common_state else "#068DA9" for state in cust_state_df.customer_state.value_counts().index],
            legend=False
            )

plt.title("Number customers from State", fontsize=15)
plt.xlabel("State")
plt.ylabel("Number Customers")
plt.xticks(fontsize=10)

st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)
 
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
 
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

