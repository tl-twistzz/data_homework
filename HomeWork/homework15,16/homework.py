import pandas as pd

# 合并数据文件
dfs = []
for i in range(1, 8):
    file_path = f'users_combined_info_500_part_{i}.csv'
    df = pd.read_csv(file_path)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# 数据清洗
# 去除重复数据
combined_df.drop_duplicates(inplace=True)

# 处理缺失值
domain_country_mapping = {
    'google.com': 'United States',
    'microsoft.com': 'United States',
    'alibaba.com': 'China',
    'tencent.com': 'China',
    'infosys.com': 'India'
}

for index, row in combined_df.iterrows():
    if pd.isnull(row['location']) and '@' in row['name']:
        company_domain = row['name'].split('@')[1]
        if company_domain in domain_country_mapping:
            combined_df.at[index, 'location'] = domain_country_mapping[company_domain]

# 人口统计分析

# 国家和地区分布
country_region_counts = combined_df['location'].value_counts()
print("国家和地区分布：")
print(country_region_counts)

# 城市级别分布（假设location列格式为'城市, 国家'）
combined_df['City'] = combined_df['location'].apply(lambda x: x.split(',')[0] if ',' in x else x)
city_counts = combined_df['City'].value_counts()
print("城市级别分布：")
print(city_counts)

# 时区分布（假设已通过某种方式获取了时区信息并存储在event_time列）
# 这里只是简单示例，实际需要更复杂的时区提取逻辑
combined_df['TimeZone'] = combined_df['event_time'].str[-6:]
timezone_counts = combined_df['TimeZone'].value_counts()
print("时区分布：")
print(timezone_counts)

# 协作行为分析

# 提交频率（假设PushEvent的数量代表提交次数，需要根据实际情况调整）
commit_counts = combined_df[combined_df['event_type'] == 'PushEvent'].groupby('user_id')['event_type'].count()
print("提交频率：")
print(commit_counts)

# 公司关联度（假设name列中包含公司邮箱信息，这里只是简单示例，可能不准确）
company_collaboration = combined_df.groupby(combined_df['name'].str.split('@').str[1])['user_id'].apply(lambda x: len(x.unique()))
print("公司关联度：")
print(company_collaboration)

# 邮箱域名与协作活跃度（假设name列中包含邮箱信息）
email_domain_commit = combined_df.groupby(combined_df['name'].str.split('@').str[1])['event_type'].count()
print("邮箱域名与协作活跃度：")
print(email_domain_commit)