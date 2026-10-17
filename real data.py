import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Amazon dataset csv.csv')

df_silver = df.drop_duplicates(subset=['OrderID']).copy()
df_silver['OrderDate'] = pd.to_datetime(df_silver['OrderDate'])
numeric_cols = ['Quantity', 'UnitPrice', 'TotalAmount', 'Discount', 'Tax', 'ShippingCost']
for col in numeric_cols:
    df_silver[col] = pd.to_numeric(df_silver[col], errors='coerce')

df_silver = df_silver.dropna(subset=['TotalAmount', 'Category'])
df_silver.to_csv('silver_amazon_data.csv', index=False)

gold_category_sales = df_silver.groupby('Category')['TotalAmount'].sum().sort_values(ascending=False).reset_index()
gold_category_sales.to_csv('gold_category_sales.csv', index=False)

gold_brand_performance = df_silver.groupby('Brand').agg({
    'TotalAmount': 'sum',
    'OrderID': 'count'
}).rename(columns={'OrderID': 'TotalOrders'}).sort_values(by='TotalAmount', ascending=False).head(10).reset_index()
gold_brand_performance.to_csv('gold_brand_performance.csv', index=False)

gold_payment_report = df_silver.groupby('PaymentMethod')['TotalAmount'].sum().reset_index()
gold_payment_report.to_csv('gold_payment_summary.csv', index=False)

gold_city_sales = df_silver.groupby('City')['TotalAmount'].sum().sort_values(ascending=False).head(10).reset_index()
gold_city_sales.to_csv('gold_city_sales.csv', index=False)

df_silver['YearMonth'] = df_silver['OrderDate'].dt.to_period('M').astype(str)
gold_monthly_trend = df_silver.groupby('YearMonth')['TotalAmount'].sum().reset_index()
gold_monthly_trend.to_csv('gold_monthly_trend.csv', index=False)

fig, axes = plt.subplots(2, 2, figsize=(20, 12))
plt.suptitle('Amazon Gold Layer Analysis Dashboard', fontsize=24, fontweight='bold', color='darkblue')

axes[0, 0].bar(gold_category_sales['Category'], gold_category_sales['TotalAmount'], color='teal')
axes[0, 0].set_title('Revenue by Category', fontsize=15)
axes[0, 0].tick_params(axis='x', rotation=45)

axes[0, 1].bar(gold_city_sales['City'], gold_city_sales['TotalAmount'], color='orange')
axes[0, 1].set_title('Top 10 Cities by Revenue', fontsize=15)
axes[0, 1].tick_params(axis='x', rotation=45)

axes[1, 0].plot(gold_monthly_trend['YearMonth'], gold_monthly_trend['TotalAmount'], marker='o', linewidth=3, color='red')
axes[1, 0].set_title('Monthly Sales Growth', fontsize=15)
axes[1, 0].grid(True, linestyle='--', alpha=0.6)
axes[1, 0].tick_params(axis='x', rotation=45)

axes[1, 1].pie(gold_payment_report['TotalAmount'], labels=gold_payment_report['PaymentMethod'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
axes[1, 1].set_title('Revenue Share by Payment Method', fontsize=15)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('amazon_final_gold_dashboard.png')

print("ETL Process Finished. 5 Gold files and Dashboard generated.")