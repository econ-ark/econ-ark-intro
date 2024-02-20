import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson
import os

errors = pd.read_csv('data/output/errors.csv')

# Convert the "date" column to datetime if not already in datetime format
errors['date'] = pd.to_datetime(errors['date'])
sample_size = 0 # set to 48 if you want to start with year 1995 Q1
ss_q = int(sample_size/4)

# Now retain only the annual forecasts/actual changes and the date column
data = errors.iloc[sample_size:, [1] + list(range(-6, 0))] 

# Create a constant term for the regression
data['Constant'] = 1

# List of squared error column names to perform regressions on
sqe_cols = ['GB_error_unemp', 'SPF_error_unemp', 'GB_error_cons', 'SPF_error_cons']

# Extract year and quarter as separate variables
data['Year'] = data['date'].dt.year
# Demean the year column
year_avg = data['Year'].mean()
data['Year_d'] = data['Year'] - year_avg

# Define the start and end dates to exclude
start_date_to_exclude = pd.to_datetime('2008-01-01')
end_date_to_exclude = pd.to_datetime('2011-12-31')

# Filter the data to exclude the observations within the specified date range
data = data[(data['date'] < start_date_to_exclude) | (data['date'] > end_date_to_exclude)]

# Create a 2x2 grid of plots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Directory and filename for saving regression summaries
output_dir = 'results'
summary_text = ""

# Loop through the squared error columns
for i, sqe_col in enumerate(sqe_cols):
    model = sm.OLS(data[sqe_col], data[['Constant', 'Year_d']])
    
    # Fit the regression model and specify the covariance type for robust standard errors
    results = model.fit(cov_type='HC3')  # You can choose 'HC4' or other options as well
    
    print(f"Regression Summary for {sqe_col}:")
    print(results.summary())
    print("\n")

    summary_text += f"Regression Summary for {sqe_col}:\n"
    summary_text += results.summary().as_text() + "\n"

    # Calculate the residuals
    residuals = results.resid

    # Compute the Mean Squared Error (MSE)
    mse = (residuals ** 2).mean()
    print(f"Mean Squared Error for {sqe_col}: {mse:.4f}")
    summary_text += f"Mean Squared Error for {sqe_col}: {mse:.4f}\n"

    # Perform the Durbin-Watson test
    durbin_watson_statistic = durbin_watson(residuals)
    print(f"Durbin-Watson Statistic for {sqe_col}: {durbin_watson_statistic}")
    summary_text += f"Durbin-Watson Statistic for {sqe_col}: {durbin_watson_statistic}\n"

    # Predict values based on the regression model
    predicted_values = results.predict(data[['Constant', 'Year_d']])

    # Calculate the min and max values for each row
    if i < 2:  # First row
        min_y = data[sqe_cols].iloc[:, :2].min().min()
        max_y = data[sqe_cols].iloc[:, :2].max().max()
    else:  # Second row
        min_y = data[sqe_cols].iloc[:, 2:].min().min()
        max_y = data[sqe_cols].iloc[:, 2:].max().max()

    # Plot the predicted values with time on the x-axis in the corresponding subplot
    row, col = divmod(i, 2)  # Calculate row and column for the subplot
    ax = axes[row, col]
    ax.plot(data['Year'], predicted_values, label=f'Predicted {sqe_col}', color="red")
    ax.bar(data['Year'], data[sqe_col], label=f'Actual {sqe_col}', color="black", alpha=0.7)
    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title(f"{sqe_col} Over Time")
    ax.legend()

    # Set the same y-axis limits for the same row
    for subplot in axes[row, :]:
        subplot.set_ylim(min_y, max_y)

# Save all regression summaries to a single text file
summary_file_path = os.path.join(output_dir, f"xGR_sqe_reg_{1983+ss_q}.txt")
with open(summary_file_path, 'w') as summary_file:
    summary_file.write(summary_text)

# Ensure proper spacing between subplots
plt.tight_layout()
if ss_q == 0:
    save_path = "figures/xGR_sqe_reg_1983.png" 
else:
    save_path = "figures/xGR_sqe_reg_1995.png"
plt.savefig(save_path, format='png')
plt.show()