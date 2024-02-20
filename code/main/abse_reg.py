import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import durbin_watson
import os
import numpy as np
from matplotlib.font_manager import FontProperties

abs_errors = pd.read_csv('data/output/abs_errors.csv')

# Convert the "date" column to datetime if not already in datetime format
abs_errors['date'] = pd.to_datetime(abs_errors['date'])
sample_size = 0 # set to 48 if you want to start with year 1995 Q1
ss_q = int(sample_size/4)

# Now retain only the annual forecasts/actual changes and the date column
data = abs_errors.iloc[sample_size:, [1] + list(range(-6, 0))] 

# Create a constant term for the regression
data['Constant'] = 1

# List of squared error column names to perform regressions on
abse_cols = ['GB_error_unemp', 'SPF_error_unemp', 'GB_error_cons', 'SPF_error_cons']

# Extract year and quarter as separate variables
data['Year'] = data['date'].dt.year

# Demean the year column
year_avg = data['Year'].mean()
data['Year_d'] = data['Year'] - year_avg

# Create a 2x2 grid of plots for the first two rows
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig2, ax2 = plt.subplots(1, 1, figsize=(6, 4))
fig3, ax3 = plt.subplots(1, 1, figsize=(6, 4))

# Create tables for the two figures (HARD-CODE DEPENDING ON FULL SAMPLE OR 1995 START!!!)
table_data_GB = [
    ['Trend:  -0.04 (p=.000)'],
    ['MSE:     0.59         '],
    ['Abs err: 1.02         ']]
table_GB = ax2.table(cellText=table_data_GB, loc='upper right', cellLoc='right', edges="open")
table_GB.auto_set_font_size(False)
table_GB.set_fontsize(8)

# Change the font properties to use a monospace font
monospace_font = FontProperties(family='monospace', size=8)
for i, j in zip(range(3), [0, 0, 0]):
    cell = table_GB.get_celld()[i, j]
    cell.get_text().set_fontproperties(monospace_font)

table_GB.scale(.5, .750)  # Adjust the table size if needed

table_data_SPF = [
    ['Trend:  -0.03 (p=.000)'],
    ['MSE:     0.69         '],
    ['Abs err: 1.10         ']]
table_SPF = ax3.table(cellText=table_data_SPF, loc='upper right', cellLoc='right', edges="open")
table_SPF.auto_set_font_size(False)
table_SPF.set_fontsize(8)

# Change the font properties to use a monospace font
for i, j in zip(range(3), [0, 0, 0]):
    cell = table_SPF.get_celld()[i, j]
    cell.get_text().set_fontproperties(monospace_font)

table_SPF.scale(.5, .750)

# Directory and filename for saving regression summaries
output_dir = 'results'
summary_text = ""

# Loop through the squared error columns
for i, abse_col in enumerate(abse_cols):
    model = sm.OLS(data[abse_col], data[['Constant', 'Year_d']])
    
    # Fit the regression model and specify the covariance type for robust standard errors
    results = model.fit(cov_type='HC3')  # You can choose 'HC4' or other options as well
    
    print(f"Regression Summary for {abse_col}:")
    print(results.summary())
    print("\n")

    summary_text += f"Regression Summary for {abse_col}:\n"
    summary_text += results.summary().as_text() + "\n"

    # Calculate the residuals
    residuals = results.resid

    # Compute the Mean Squared Error (MSE)
    mse = (residuals ** 2).mean()
    print(f"Mean Squared Error for {abse_col}: {mse:.4f}")
    summary_text += f"Mean Squared Error for {abse_col}: {mse:.4f}\n"

    # Perform the Durbin-Watson test
    durbin_watson_statistic = durbin_watson(residuals)
    print(f"Durbin-Watson Statistic for {abse_col}: {durbin_watson_statistic}")
    summary_text += f"Durbin-Watson Statistic for {abse_col}: {durbin_watson_statistic}\n"

    # Predict values based on the regression model
    predicted_values = results.predict(data[['Constant', 'Year_d']])

    # Calculate the min and max values for each row
    if i < 2:  # First row
        min_y = data[abse_cols].iloc[:, :2].min().min()
        max_y = data[abse_cols].iloc[:, :2].max().max()
    else:  # Second row
        min_y = data[abse_cols].iloc[:, 2:].min().min()
        max_y = data[abse_cols].iloc[:, 2:].max().max()
    
    # Plot the predicted values with time on the x-axis in the corresponding subplot for the first two rows
    row, col = divmod(i, 2)  # Calculate row and column for the subplot
    ax = axes[row, col]
    ax.plot(data['Year'], predicted_values, color="red")
    ax.bar(data['Year'], data[abse_col], color="black", alpha=0.7)
    ax.set_xlabel("Year")
    ax.set_ylabel("Values")
    ax.set_title(f"{abse_col} Over Time")

    # If it's the last row, plot in the first separate figure (fig2)
    if i == 2:
        ax2.plot(data['Year'], predicted_values, color="red", linewidth=3.0)
        ax2.bar(data['Year'], data[abse_col], color="black", alpha=0.7)
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Values")
        ax2.set_title(f"Fed Error Over Time", fontdict={'family': 'monospace'})

    # If it's the last row, plot in the second separate figure (fig3)
    elif i == 3:
        ax3.plot(data['Year'], predicted_values, color="red",linewidth=3.0)
        ax3.bar(data['Year'], data[abse_col], color="black", alpha=0.7)
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Values")
        ax3.set_title(f"SPF Error Over Time", fontdict={'family': 'monospace'})

    # Set the same y-axis limits for the same row
    for subplot in axes[row, :]:
        subplot.set_ylim(min_y, max_y)

# Set the same y-limits for the last two figures
y_min = min(0, 5)  # Change this if you want a custom range
y_max = max(0, 5)  # Change this if you want a custom range
ax2.set_ylim(y_min, y_max)
ax3.set_ylim(y_min, y_max)

# Save all regression summaries to a single text file
summary_file_path = os.path.join(output_dir, f"abse_reg_{1983+ss_q}.txt")
with open(summary_file_path, 'w') as summary_file:
    summary_file.write(summary_text)

# Ensure proper spacing between subplots
plt.tight_layout()
plt.show()


# Degenerate code. Easier to save them yourself once the graphs pop up. For now.
# Save both figures
#if sample_size == 0:
#    save_path = "figures/abse_reg_1983.png" 
#    save_path2 = "figures/abse_reg_1983_GB_cons_only.png"
#    save_path3 = "figures/abse_reg_1983_SPF_cons_only.png"
#else:
#    save_path = "figures/abse_reg_1995.png"
#    save_path2 = "figures/abse_reg_1995_GB_cons_only.png"
#    save_path3 = "figures/abse_reg_1995_SPF_cons_only.png"

#plt.savefig(save_path, format='png')
#plt.savefig(save_path2, format='png', bbox_inches='tight')
#plt.savefig(save_path3, format='png', bbox_inches='tight')


