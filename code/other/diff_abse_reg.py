import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson
import os

abs_errors = pd.read_csv('data/output/errors.csv')

# Convert the "date" column to datetime if not already in datetime format
abs_errors['date'] = pd.to_datetime(abs_errors['date'])
sample_size = 0 # set to 48 if you want to start with year 1995 Q1
ss_q = int(sample_size/4)

# Now retain only the annual forecasts/actual changes and the date column
data = abs_errors.iloc[sample_size:, [1] + list(range(-6, 0))] 

# Create a constant term for the regression
data['Constant'] = 1

# List of squared error column names to perform regressions on
diff_abse_cols = ["diff_error_unemp","diff_error_cons"]

# Extract year and quarter as separate variables
data['Year'] = data['date'].dt.year
# Demean the year column
year_avg = data['Year'].mean()
data['Year_d'] = data['Year'] - year_avg

# Create a 1x2 grid of plots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
output_dir = 'results'
summary_text = ""

# Loop through the squared error columns
for i, diff_abse_col in enumerate(diff_abse_cols):
    model = sm.OLS(data[diff_abse_col], data[['Constant', 'Year_d']])
    results = model.fit(cov_type="HC3")

    print(f"Regression Summary for {diff_abse_col}:")
    print(results.summary())
    print("\n")

    summary_text += f"Regression Summary for {diff_abse_col}:\n"
    summary_text += results.summary().as_text() + "\n"

    # Calculate the residuals
    residuals = results.resid

    # Compute the Mean Squared Error (MSE)
    mse = (residuals ** 2).mean()
    print(f"Mean Squared Error for {diff_abse_col}: {mse:.4f}")
    summary_text += f"Mean Squared Error for {diff_abse_col}: {mse:.4f}\n"

    # Perform the Durbin-Watson test
    durbin_watson_statistic = durbin_watson(residuals)
    print(f"Durbin-Watson Statistic for {diff_abse_col}: {durbin_watson_statistic}")
    summary_text += f"Durbin-Watson Statistic for {diff_abse_col}: {durbin_watson_statistic}\n"

    # Predict values based on the regression model
    predicted_values = results.predict(data[['Constant', 'Year_d']])

    # Plot the predicted values with time on the x-axis in the corresponding subplot
    ax = axes[i]
    ax.plot(data['Year'], predicted_values, label=f'Predicted {diff_abse_col}', color="red")
    ax.bar(data['Year'], data[diff_abse_col], label=f'Actual {diff_abse_col}', color="black", alpha=0.7)
    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title(f"{diff_abse_col} Over Time")
    ax.legend()

    min_y = data[diff_abse_cols].min().min()
    max_y = data[diff_abse_cols].max().max()
    for ax in axes.flat:
        ax.set_ylim(min_y, max_y)

# Save all regression summaries to a single text file
summary_file_path = os.path.join(output_dir, f"diff_abse_reg_{1983+ss_q}.txt")
with open(summary_file_path, 'w') as summary_file:
    summary_file.write(summary_text)

# Ensure proper spacing between subplots
plt.tight_layout()
if ss_q == 0:
    save_path = "figures/diff_abse_reg_1983.png" 
else:
    save_path = "figures/diff_abse_reg_1995.png"
plt.savefig(save_path, format='png')
plt.show()