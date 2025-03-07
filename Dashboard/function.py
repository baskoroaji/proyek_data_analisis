class DataAnalysis:
    def __init__(self, df):
        self.df = df
    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english").order_id.count().sort_values(ascending=False).reset_index()
        return sum_order_items_df
    
    def create_monthly_orders_df(self):
        monthly_orders_df = self.df.resample(rule='ME', on='order_approved_at').agg({
            "order_id": "nunique",
        })
        monthly_orders_df = monthly_orders_df.reset_index()
        monthly_orders_df.rename(columns={
            "order_id": "order_count",
        }, inplace=True)
        
        return monthly_orders_df
    
    def create_cust_state_df(self):
        cust_state_df = self.df.groupby(by="customer_state").customer_id.nunique().reset_index()
        cust_state_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_common_state = cust_state_df.loc[cust_state_df['customer_count'].idxmax(), 'customer_state']
        cust_state_df = cust_state_df.sort_values(by='customer_count', ascending=False)

        return cust_state_df, most_common_state
    
    def product_review_df(self):
        rating_category_product = self.df.groupby(by="product_category_name_english").review_score.mean().round(1).sort_values(ascending=False).reset_index()
        return rating_category_product
    
    def customer_payment_method_df(self):
        payment_method_customer = self.df.groupby("payment_type").order_id.nunique().sort_values(ascending=False).reset_index()
        payment_method_customer.rename(columns={
            "order_id": "transaction"
        }, inplace=True)
        most_popular_payment = payment_method_customer.iloc[0]['payment_type']
        return payment_method_customer, most_popular_payment
    
    def rfm_analysis(self):
        rfm_df = self.df.groupby(by="customer_id", as_index=False).agg({
            "order_purchase_timestamp": "max", 
            "order_id": "nunique", 
            "price": "sum" 
        })
        rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

        rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
        recent_date = self.df["order_purchase_timestamp"].dt.date.max()
        rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
        rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
        
        return rfm_df    
    