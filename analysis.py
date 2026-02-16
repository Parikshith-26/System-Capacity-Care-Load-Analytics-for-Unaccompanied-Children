import pandas as pd

# Load data
df = pd.read_csv("data/uac_cleaned.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').set_index('Date')

# Create continuous timeline
df = df.asfreq('D')

# Fill values
df[['cbp_custody','hhs_care']] = df[['cbp_custody','hhs_care']].ffill()
df[['apprehended','transferred','discharged']] = df[['apprehended','transferred','discharged']].fillna(0)

# Metrics
df['total_load'] = df['cbp_custody'] + df['hhs_care']
df['net_intake'] = df['transferred'] - df['discharged']
df['growth_rate'] = df['total_load'].pct_change()*100

df['backlog_flag'] = (df['net_intake'] > 0).astype(int)
df['backlog_streak'] = df['backlog_flag'].groupby((df['backlog_flag'] != df['backlog_flag'].shift()).cumsum()).cumsum()

df['volatility'] = df['total_load'].rolling(14).std()
df['discharge_ratio'] = df['discharged']/df['transferred']

threshold = df['volatility'].quantile(0.75)
df['stress_flag'] = ((df['net_intake'] > 0) & (df['volatility'] > threshold))

# Results
print("Max total load:", int(df['total_load'].max()))
print("Avg discharge efficiency:", round(df['discharge_ratio'].mean(),2))
print("Longest backlog streak:", int(df['backlog_streak'].max()))
print("Total stress days:", int(df['stress_flag'].sum()))

# save processed file for dashboard
df.to_csv("processed.csv")
