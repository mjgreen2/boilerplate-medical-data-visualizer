import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.DataFrame(pd.read_csv(filepath_or_buffer = "medical_examination.csv"))

# Add 'overweight' column. To determine if a person is overweight, first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.

df['overweight'] = 10000 *(df['weight']/(df['height'] * df['height']))

for row in range(0, df['overweight'].size):
    if df.loc[row, 'overweight'] > 25:
        df.loc[row, 'overweight'] = 1      
    else:
        df.loc[row, 'overweight'] = 0

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

column_list = ['cholesterol', 'gluc']
for col in range(0, 2):
    for row in range(0, df['overweight'].size):
        if df.loc[row, column_list[col]] == 1:
            df.loc[row, column_list[col]] = 0      
        elif df.loc[row, column_list[col]] > 1:
            df.loc[row, column_list[col]] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.

    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    
    df_cat['total'] = 'NaN'
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()

    # Draw the catplot with 'sns.catplot()'
    fig, ax = plt.subplots(figsize=(11, 5))
    
    fig = sns.catplot(data = df_cat, kind = "bar", x = "variable", y = "total", hue = "value", col = "cardio").fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    #Clean the data. Filter out the following patient segments that represent incorrect data:
    #- diastolic pressure is higher than systolic (Keep the correct data with `(df['ap_lo'] <= df['ap_hi'])`)

    #- height is less than the 2.5th percentile and more than the 97.5th percentile (Keep the correct data with `(df['height'] >= df['height'].quantile(0.025))`)
 
    #- weight is less than the 2.5th percentile and more than the 97.5th percentile
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
    (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure (11inch x 9inch)
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask=mask, annot=True, fmt="^.1f", center=0, 
    vmax=0.3, cbar_kws={"shrink": .50, "ticks":[-0.08, 0, 0.08, 0.16, 0.24]})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
