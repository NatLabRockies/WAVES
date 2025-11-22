import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_GPRA_data(fig_name, target, actuals):
    # Unpack target data
    target_values, target_years = zip(*target)
    # Unpack actuals data
    actual_values, actual_years = zip(*actuals)
    
    # Combine all values to find the maximum value for setting the y-axis limit
    all_values = list(target_values) + list(actual_values)
    max_value = max(all_values)
    
    # Determine the full range of years
    min_year = min(target_years + actual_years)
    max_year = max(target_years + actual_years)
    all_years = list(range(min_year, max_year + 1))
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(9, 4))
    
    # Factor depending on max value
    factor = max_value / 40
    
    # Plot target data without markers for the line
    plt.plot(target_years, target_values, color='royalblue', linestyle='--', linewidth=2, marker='o', markeredgecolor='black', markerfacecolor='black', label='GPRA Target', zorder=10)
    
    # Add markers only for the first and last points
    plt.plot(target_years[0], target_values[0], marker='o', markersize=5, color='royalblue', markeredgecolor='black', markerfacecolor='black', zorder=10)
    plt.plot(target_years[-1], target_values[-1], marker='o', markersize=5, color='royalblue', markeredgecolor='black', markerfacecolor='black', zorder=10)
    
    # Add text annotations for target data
    for year, value in zip(target_years, target_values):
        plt.text(year, value + factor * 0.9, f'{value:.0f}', fontsize=9, color='black', ha='center', va='bottom')
    
    # Plot actuals data with smaller diamond marker
    plt.scatter(actual_years, actual_values, marker='D', s=30, edgecolor='black', color='black', linewidth=2, label='Actuals', zorder=100)
    
    # Add text annotations for actuals data
    #for year, value in zip(actual_years, actual_values):
    #    plt.text(year, value + factor * 0.9, f'{value:.0f}', fontsize=9, color='black', ha='center', va='bottom')
    
    # Plot old_target data with diamond marker
    #old_target_value, old_target_year = old_target
    #plt.plot(old_target_year, old_target_value, color='black', marker='x', markersize=12, markeredgecolor='black', markerfacecolor='black', linewidth=0, label=text_old_target)
    
    # Add text annotation for old_target data
    #plt.text(old_target_year, old_target_value + factor * 0.9, f'{old_target_value:.0f}', fontsize=9, color='black', ha='center', va='bottom')
    
    # Set axis labels
    plt.xlabel('Fiscal Year')
    plt.ylabel('Levelized Cost of Energy (2022$/MWh)')
    
    # Set y-axis limit: bottom is 0 and top is 10 more than the max value
    plt.ylim(bottom=0, top=max_value + 10)
    
    # Ensure every year from min_year to max_year is shown on the x-axis
    plt.xticks(all_years)
    
    # Define y-ticks based on max_value
    if max_value <= 50:
        new_ticks = np.arange(0, max_value + 10, 5)
    else:
        new_ticks = np.arange(0, max_value + 20, 10)
    
    plt.yticks(new_ticks)
    
    # Add a legend
    plt.legend()
    
    # Show only horizontal gridlines
    plt.grid(axis='y')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    plt.savefig("Figures/" + fig_name + '.png', format='png', dpi=300)
    
    # Show plot
    plt.show()
    
    
def plot_capex_donut(technology, df, start_angle, width, height):
    # Calculate the total value
    total_value = df['Value ($/kW)'].sum()

    # Add a new column with the percentage of the total value for each category
    df['% of Total'] = (df['Value ($/kW)'] / total_value) * 100

    # Calculate total percentage per category
    category_totals = df.groupby('Category')['% of Total'].sum()

    # Plotting the donut chart
    fig, ax = plt.subplots(figsize=(width, height))

    # Extract data for plotting
    sizes = df['% of Total']
    labels = df['Component']
    categories = df['Category']
    colors = df['Color']

    # Create the donut chart with black borders and specified colors
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, colors=colors, autopct='', startangle=start_angle, pctdistance=0.85,
        wedgeprops=dict(width=0.3, edgecolor='black', linewidth=1.5)  # Black border with width 1.5
    )

    # Draw the center circle for the donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # Check the number of "Components" per "Category"
    components_per_category = df.groupby('Category')['Component'].count()

    # Add labels with lines pointing to the wedges if there is more than one component per category
    label_offset = 1.25  # Adjusts the distance of the label from the chart
    for i, (pct, wedge, category) in enumerate(zip(df['% of Total'], wedges, categories)):
        if components_per_category[category] > 1:
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = np.cos(np.radians(angle))
            y = np.sin(np.radians(angle))

            horizontalalignment = {-1: 'right', 1: 'left'}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(angle)

            # Add component labels outside the donut
            ax.annotate(labels[i],
                        xy=(x, y),
                        xytext=(label_offset*np.sign(x), label_offset*y),
                        horizontalalignment=horizontalalignment,
                        weight='bold',
                        arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle, color='gray'),
                        fontsize=12)

            # Add percentage labels inside the donut
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = np.cos(np.radians(angle)) * 0.85  # Adjusted position inside the donut
            y = np.sin(np.radians(angle)) * 0.85  # Adjusted position inside the donut
            ax.text(x, y, f'{pct:.1f}%', ha='center', va='center', fontsize=10, color='white', weight='bold')

    # Add radial lines to separate categories
    unique_categories = df['Category'].unique()
    category_angles = []

    for category in unique_categories:
        # Calculate the angle range for each category
        category_size = df[df['Category'] == category]['% of Total'].sum()
        end_angle = start_angle + (category_size / 100) * 360
        category_angles.append((start_angle, end_angle))
        start_angle = end_angle

    # Draw radial lines for category divisions
    for start_angle, end_angle in category_angles:
        # Convert angles to radians
        start_rad = np.radians(start_angle)
        end_rad = np.radians(end_angle)

        # Calculate the line endpoints
        x_start = np.cos(start_rad)
        y_start = np.sin(start_rad)
        x_end = np.cos(end_rad)
        y_end = np.sin(end_rad)

        # Plot the radial lines
        ax.plot([0, x_start], [0, y_start], color='black', linestyle='--', linewidth=1.5)
        ax.plot([0, x_end], [0, y_end], color='black', linestyle='--', linewidth=1.5)

    # Add labels with category names and total percentages centered inside the donut
    for category, angle_range in zip(unique_categories, category_angles):
        # Find the midpoint of the angle range
        angle = (angle_range[0] + angle_range[1]) / 2
        x = np.cos(np.radians(angle)) * 0.33 # Adjusted position inside the donut
        y = np.sin(np.radians(angle)) * 0.35  # Adjusted position inside the donut

        # Get the total percentage for the category
        total_percentage = category_totals[category]

        # Add the label inside the donut
        ax.text(x, y, f'{category}\n{total_percentage:.1f}%', ha='center', va='center', fontsize=13, weight='bold', color='black')

    # Add a legend for Categories
    category_labels = df['Category'].unique()
    category_colors = plt.cm.viridis(np.linspace(0, 1, len(category_labels)))

    for i, category in enumerate(category_labels):
        plt.scatter([], [], color=category_colors[i], label=category)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    if "DW" in technology:
        if "20" in technology:
            plt.title("Residential (20 kW)", fontsize = 16)
        if "100" in technology:
            plt.title("Commercial (100 kW)", fontsize = 16)
        if "1500" in technology:
            plt.title("Large (1,500 kW)", fontsize = 16)
    ax.axis('equal')
    plt.tight_layout()
    plt.savefig("Figures/" + technology + '_capex_donut.png', format='png', dpi=300)
    plt.show()

def plot_LCOE_sensitivity(technology, df, width=10, height=6, x_min=None, x_max=None): 
    import matplotlib.pyplot as plt
    import numpy as np

    # Reverse the dataframe for proper y-axis ordering
    df = df[::-1]

    fig, ax = plt.subplots(figsize=(width, height))

    # Plot min to base LCOE bars with a higher zorder to ensure they are in front of gridlines
    ax.barh(df['Key Parameters for LCOE Sensitivity Analysis'], 
            df['base LCOE'] - df['min LCOE'], 
            left=df['min LCOE'], 
            color=df['color'], 
            edgecolor='none', zorder=3)

    # Plot base to max LCOE bars with a higher zorder to ensure they are in front of gridlines
    ax.barh(df['Key Parameters for LCOE Sensitivity Analysis'], 
            df['max LCOE'] - df['base LCOE'], 
            left=df['base LCOE'], 
            color=df['color'], 
            edgecolor='none', zorder=3)

    # Calculate the mean base LCOE for the reference line
    reference_LCOE = df['base LCOE'].mean()
    
    # Add a vertical white line for the base LCOE
    reference_line = ax.axvline(x=reference_LCOE, color='white', linewidth=2, zorder=4)
    
    # Adding a legend for the reference LCOE line with a grey background
    ax.legend([reference_line], [f"Reference LCOE = ${reference_LCOE:,.0f}/MWh"], 
              loc='best', fontsize=8, frameon=True, facecolor='lightgrey')

    # Adding the min, base, and max values next to their respective bars in reverse order
    for index in range(len(df)-1, -1, -1):
        row = df.iloc[index]

        # Format the numbers dynamically based on the input, include commas and remove trailing .0
        min_value = f"{row['min value']:,.2f}".rstrip('0').rstrip('.')
        base_value = f"{row['base value']:,.2f}".rstrip('0').rstrip('.')
        max_value = f"{row['max value']:,.2f}".rstrip('0').rstrip('.')

        # Min value label
        ax.text(row['min LCOE'] - 0.5, index, min_value, 
                ha='right', va='center', color='black', fontsize=8)
        
        # Calculate the differences
        diff_max_base = row['max LCOE'] - row['base LCOE']
        diff_base_min = row['base LCOE'] - row['min LCOE']

        # Base value label positioning
        if diff_max_base > diff_base_min:
            ax.text(row['base LCOE'] + 0.2, index, base_value, 
                    ha='left', va='center', color='white', fontsize=8, weight="bold")
        else:
            ax.text(row['base LCOE'] - 0.5, index, base_value, 
                    ha='right', va='center', color='white', fontsize=8, weight="bold")

        # Max value label
        ax.text(row['max LCOE'] + 0.5, index, max_value, 
                ha='left', va='center', color='black', fontsize=8)

    # Define the x-axis range for separation lines
    min_xlim = df['min LCOE'].min() - 10 if x_min is None else x_min
    max_xlim = df['max LCOE'].max() + 10 if x_max is None else x_max

    # Add horizontal separation lines between bars
    for index in range(len(df)):
        ax.hlines(y=index - 0.5, xmin=min_xlim, xmax=max_xlim, color='grey', linestyle='--', linewidth=0.7, zorder=2)

    # Add separation lines before the first bar and after the last bar
    ax.hlines(y=-0.5, xmin=min_xlim, xmax=max_xlim, color='grey', linestyle='--', linewidth=0.7, zorder=2)
    ax.hlines(y=len(df) - 0.5, xmin=min_xlim, xmax=max_xlim, color='grey', linestyle='--', linewidth=0.7, zorder=2)

    # Set x-axis limits with an optional buffer
    ax.set_xlim(min_xlim, max_xlim)

    # Adding grid and labels, with gridlines behind the bars
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.7, zorder=0)
    ax.set_xlabel('LCOE ($/MWh)')
    ax.set_ylabel('Key Parameters for LCOE Sensitivity Analysis')

    # Remove box lines around the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.savefig("Figures/" + technology + '_LCOE_sensitivity.png', format='png', dpi=300)
    plt.show()
    
def plot_LCOE_sensitivity_percentage(technology, df, width=10, height=6, x_min=None, x_max=None):
    import matplotlib.pyplot as plt
    import numpy as np

    # Reverse the dataframe for proper y-axis ordering
    df = df[::-1].copy()

    # Calculate the mean base LCOE for the reference line
    reference_LCOE = df['base LCOE'].mean()

    # Convert LCOE values to percentage change relative to reference
    df['min_pct'] = (df['min LCOE'] - reference_LCOE) / reference_LCOE * 100
    df['base_pct'] = (df['base LCOE'] - reference_LCOE) / reference_LCOE * 100
    df['max_pct'] = (df['max LCOE'] - reference_LCOE) / reference_LCOE * 100

    fig, ax = plt.subplots(figsize=(width, height))

    # Plot min to base percentage bars
    ax.barh(df['Key Parameters for LCOE Sensitivity Analysis'], 
            df['base_pct'] - df['min_pct'], 
            left=df['min_pct'], 
            color=df['color'], 
            edgecolor='none', zorder=3)

    # Plot base to max percentage bars
    ax.barh(df['Key Parameters for LCOE Sensitivity Analysis'], 
            df['max_pct'] - df['base_pct'], 
            left=df['base_pct'], 
            color=df['color'], 
            edgecolor='none', zorder=3)

    # Add a vertical white line at 0% (reference LCOE)
    reference_line = ax.axvline(x=0, color='white', linewidth=2, zorder=4)
    
    # Adding a legend for the reference LCOE line with a grey background
    ax.legend([reference_line], [f"Reference LCOE = ${reference_LCOE:,.0f}/MWh"], 
              loc='best', fontsize=8, frameon=True, facecolor='lightgrey')

    # Adding the min, base, and max values next to their respective bars in reverse order
    for index in range(len(df)-1, -1, -1):
        row = df.iloc[index]

        # Format the numbers dynamically based on the input
        min_value = f"{row['min value']:,.2f}".rstrip('0').rstrip('.')
        base_value = f"{row['base value']:,.2f}".rstrip('0').rstrip('.')
        max_value = f"{row['max value']:,.2f}".rstrip('0').rstrip('.')

        # Min value label
        ax.text(row['min_pct'] - 0.5, index, min_value, 
                ha='right', va='center', color='black', fontsize=8)
        
        # Calculate the differences
        diff_max_base = row['max_pct'] - row['base_pct']
        diff_base_min = row['base_pct'] - row['min_pct']

        # Base value label positioning
        if diff_max_base > diff_base_min:
            ax.text(row['base_pct'] + 0.2, index, base_value, 
                    ha='left', va='center', color='white', fontsize=8, weight="bold")
        else:
            ax.text(row['base_pct'] - 0.5, index, base_value, 
                    ha='right', va='center', color='white', fontsize=8, weight="bold")

        # Max value label
        ax.text(row['max_pct'] + 0.5, index, max_value, 
                ha='left', va='center', color='black', fontsize=8)

    # Define the x-axis range for separation lines
    min_xlim = df['min_pct'].min() - 10 if x_min is None else x_min
    max_xlim = df['max_pct'].max() + 10 if x_max is None else x_max

    # Add horizontal separation lines between bars
    for index in range(len(df)):
        ax.hlines(y=index - 0.5, xmin=min_xlim, xmax=max_xlim, color='grey', linestyle='--', linewidth=0.7, zorder=2)

    # Add separation lines before the first bar and after the last bar
    ax.hlines(y=-0.5, xmin=min_xlim, xmax=max_xlim, color='grey', linestyle='--', linewidth=0.7, zorder=2)
    ax.hlines(y=len(df) - 0.5, xmin=min_xlim, xmax=max_xlim, color='grey', linestyle='--', linewidth=0.7, zorder=2)

    # Set x-axis limits with an optional buffer
    ax.set_xlim(min_xlim, max_xlim)

    # Adding grid and labels
    ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.7, zorder=0)
    ax.set_xlabel('Percentage Change with respect to Reference LCOE (%)')
    ax.set_ylabel('Key Parameters for LCOE Sensitivity Analysis')

    # Remove box lines around the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.savefig("Figures/" + technology + '_LCOE_sensitivity_percentage.png', format='png', dpi=300)
    plt.show()

def plot_LCOE_waterfall(technology, df, width, height, y_min=None, y_max=None):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    df_final = df

    # Extract the final components, values, and categories
    components = df_final['Component']
    values = df_final['Value ($/MWh)']
    categories = df_final['Category']

    # Calculate total LCOE
    total_lcoe = values.sum()

    # Append 'Total LCOE' to components and values
    components = pd.concat([components, pd.Series('LCOE')], ignore_index=True)
    values = pd.concat([values, pd.Series(total_lcoe)], ignore_index=True)
    categories = pd.concat([categories, pd.Series('Total')], ignore_index=True)

    # Setup the figure and axes
    fig, ax = plt.subplots(figsize=(width, height))

    # Initial bar is set at 0
    bar_positions = np.arange(len(values))
    bar_values = values.tolist()
    bar_labels = components.tolist()

    # Waterfall plot values
    cumulative_values = np.cumsum([0] + bar_values[:-1])
    base = cumulative_values

    # Define color map for categories
    category_colors = {
        'Turbine': 'olivedrab',
        'Balance of System CapEx': 'dodgerblue',
        'Financial CapEx': 'purple',
        'OpEx': 'yellow',
        'Total': 'darkblue'
    }

    # Plotting the bars
    for i in range(len(bar_values)):
        color = category_colors.get(categories[i], 'grey')
        if i == len(bar_values) - 1:
            # Total LCOE bar is fully visible and dark blue
            ax.bar(bar_positions[i], bar_values[i], bottom=0, color=category_colors["Total"], edgecolor='black', label='LCOE', zorder=3)
        else:
            # Invisible base bar for intermediate bars
            ax.bar(bar_positions[i], base[i], bottom=0, color='white', edgecolor='white', zorder=1)
            # Intermediate bars
            ax.bar(bar_positions[i], bar_values[i], bottom=base[i], color=color, edgecolor='black', zorder=3)

    # Labeling bars with values
    for i, (pos, val) in enumerate(zip(bar_positions, bar_values)):
        alignment = 'center' if val > 0 else 'top'
        if i == len(bar_values) - 1:
            # Round total LCOE to integer for display
            ax.text(pos, val + 0.5, f'{int(round(val))}', ha='center', va='bottom', color='black', zorder=4)
        else:
            ax.text(pos, base[i] + val + 0.5, f'{val:.1f}', ha='center', va='bottom', color='black', zorder=4)

    # Add labels for each category above the bars
    category_positions = {}
    for i, (pos, val) in enumerate(zip(bar_positions, bar_values)):
        category = categories[i]
        if category not in category_positions:
            category_positions[category] = []
        category_positions[category].append((pos, val))

    # Determine a consistent height for the category labels
    label_y_position = base[2] * 0.6  # Default height for categories
    first_category_label_y_position = None

    for category, positions in category_positions.items():
        if category == 'Total':
            continue
        # Check if the technology string contains "DW"
        if "DW" in technology and len(positions) == 1:
            continue
        # Calculate the range for the category
        min_pos = min(pos for pos, _ in positions)
        max_pos = max(pos for pos, _ in positions)
        total_percentage = sum(val for _, val in positions)
        pct_of_total = (total_percentage / total_lcoe) * 100
        text_label = f'{category}\n({pct_of_total:.1f}%)'
        
        # Get the color of the current category and set text box background color
        color = category_colors.get(category, 'grey')
        bbox_props = dict(boxstyle="square,pad=0.3", edgecolor="black", facecolor=color)

        # Determine the height for the label
        if first_category_label_y_position is None:
            first_category_label_y_position = base[max_pos] + 1.75 * bar_values[max_pos]  # 20% above the height of the last bar in the first category
            y_position = first_category_label_y_position
        else:
            y_position = label_y_position
        
        # Place the label above the bars for this category at the determined height
        if color == "yellow":
            ax.text((min_pos + max_pos) / 2, y_position, text_label, ha='center', va='center', color='black', bbox=bbox_props, zorder=4)
        else:
            ax.text((min_pos + max_pos) / 2, y_position, text_label, ha='center', va='center', color='white', bbox=bbox_props, zorder=4)

    # Add horizontal grid lines behind the bars
    ax.yaxis.grid(True, linestyle='--', linewidth=0.7, zorder=0)

    # Add a grey horizontal line at the height of the total value
    ax.axhline(total_lcoe, color='grey', linestyle='--', linewidth=1, zorder=1)

    # Add vertical grey lines to separate the bars from different categories
    if "DW" not in technology:
        category_boundaries = []
        last_category = categories[0]

        for i in range(1, len(categories)):
            if categories[i] != last_category:
                category_boundaries.append(i - 0.5)
                last_category = categories[i]

        for boundary in category_boundaries:
            ax.axvline(boundary, color='grey', linewidth=1.2, zorder=1)

    # Setting labels and title
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right')
    ax.set_ylabel('Levelized Cost of Energy (2023$/MWh)')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    if "DW" in technology:
        if "20" in technology:
            plt.title("Single-Turbine\nResidential (20 kW)", fontsize=16)
        if "100" in technology:
            plt.title("Single-Turbine\nCommercial (100 kW)", fontsize=16)
        if "1500" in technology:
            plt.title("Single-Turbine\nLarge (1,500 kW)", fontsize=16)

    # Set y-axis limits if specified
    if y_min is not None:
        ax.set_ylim(bottom=y_min)
    if y_max is not None:
        ax.set_ylim(top=y_max)

    # Tight layout for better spacing
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig("Figures/" + technology + '_LCOE_waterfall.png', format='png', dpi=300)
    plt.show()

def capex_dataframe_dw(df_20kW, df_100kW, df_1500kW):
    # Initialize the DataFrame structure
    parameters = ['Wind Turbine CapEx', 'BOS CapEx', 'Total CapEx', 'OpEx']
    units = ['2023$/kW', '2023$/kW', '2023$/kW', '2023$/kW/yr']
    
    # Define the DataFrame for the result
    result_df = pd.DataFrame(columns=['Parameter', 'Residential', 'Commercial', 'Large', 'Units'])
    result_df['Parameter'] = parameters
    result_df['Units'] = units

    # Define a helper function to get the values for each DataFrame
    def get_capex_values(df, component):
        if 'Value ($/kW)' in df.columns:
            return df[df['Component'] == component]['Value ($/kW)'].sum()
        else:
            raise KeyError("Column 'Value ($/kW)' not found in DataFrame")

    

    def get_opex_value(df):
        if 'Value ($/kW-yr)' in df.columns:
            return df[df['Component'] == 'OpEx']['Value ($/kW-yr)'].sum()
        else:
            raise KeyError("Column 'Value ($/kW-yr)' not found in DataFrame")

    # Fill the DataFrame with the required values
    try:
        result_df.loc[result_df['Parameter'] == 'Wind Turbine CapEx', 'Residential'] = get_capex_values(df_20kW, 'Wind Turbine CapEx')
        result_df.loc[result_df['Parameter'] == 'BOS CapEx', 'Residential'] = get_capex_values(df_20kW, 'BOS CapEx')
        result_df.loc[result_df['Parameter'] == 'OpEx', 'Residential'] = get_opex_value(df_20kW)
    
        result_df.loc[result_df['Parameter'] == 'Wind Turbine CapEx', 'Commercial'] = get_capex_values(df_100kW, 'Wind Turbine CapEx')
        result_df.loc[result_df['Parameter'] == 'BOS CapEx', 'Commercial'] = get_capex_values(df_100kW, 'BOS CapEx')
        result_df.loc[result_df['Parameter'] == 'OpEx', 'Commercial'] = get_opex_value(df_100kW)

        result_df.loc[result_df['Parameter'] == 'Wind Turbine CapEx', 'Large'] = get_capex_values(df_1500kW, 'Wind Turbine CapEx')
        result_df.loc[result_df['Parameter'] == 'BOS CapEx', 'Large'] = get_capex_values(df_1500kW, 'BOS CapEx')
        result_df.loc[result_df['Parameter'] == 'OpEx', 'Large'] = get_opex_value(df_1500kW)
    
        # Calculate Total CapEx for each category
        result_df.loc[result_df['Parameter'] == 'Total CapEx', 'Residential'] = result_df.loc[result_df['Parameter'].isin(['Wind Turbine CapEx', 'BOS CapEx']), 'Residential'].sum()
        result_df.loc[result_df['Parameter'] == 'Total CapEx', 'Commercial'] = result_df.loc[result_df['Parameter'].isin(['Wind Turbine CapEx', 'BOS CapEx']), 'Commercial'].sum()
        result_df.loc[result_df['Parameter'] == 'Total CapEx', 'Large'] = result_df.loc[result_df['Parameter'].isin(['Wind Turbine CapEx', 'BOS CapEx']), 'Large'].sum()

        # Round the values to the nearest whole number and format with commas
        def format_with_commas(x):
            if pd.notnull(x):
                return "{:,}".format(round(x))
            return x

        result_df[['Residential', 'Commercial', 'Large']] = result_df[['Residential', 'Commercial', 'Large']].applymap(format_with_commas)
    
    except KeyError as e:
        print(f"Error: {e}")
    
    return result_df



def capex_dataframe(df):
    summary = []

    for category in df["Category"].unique()[::-1]:
        category_df = df[df["Category"] == category]
        total_value = category_df["Value ($/kW)"].sum()
        summary.append({"Parameter": f"Total {category}", "Value ($/kW)": total_value})
        summary.extend(category_df[["Component", "Value ($/kW)"]].rename(columns={"Component": "Parameter"}).to_dict("records"))

    total_capex = df["Value ($/kW)"].sum()
    summary.append({"Parameter": "Total CapEx", "Value ($/kW)": total_capex})

    summary_df = pd.DataFrame(summary)

    summary_df["Value ($/kW)"] = summary_df["Value ($/kW)"].round().astype(int).apply(lambda x: f"{x:,}")

    return summary_df

def wind_ES_summary_table(rating_landbased_MW, rating_offshore_MW):
    # Load data from CSV files
    lbw_df = pd.read_csv("Data/LBW_LCOE.csv")
    fbow_df = pd.read_csv("Data/FBOW_LCOE.csv")
    flow_df = pd.read_csv("Data/FLOW_LCOE.csv")
    dw_20kW_df = pd.read_csv("Data/DW_20kW_LCOE.csv")
    dw_100kW_df = pd.read_csv("Data/DW_100kW_LCOE.csv")
    dw_1500kW_df = pd.read_csv("Data/DW_1500kW_LCOE.csv")

    # Helper function for formatting with commas and rounding
    def format_number(num, decimals=0):
        if decimals == 0:
            return f"{num:,.0f}"
        else:
            return f"{num:,.{decimals}f}"

    # Define the rows of the table
    rows = [
        {"Parameter": "Wind turbine rating", "Units": "MW", 
         "Utility Scale (LBW)": format_number(rating_landbased_MW,1), 
         "Utility Scale (FBOW)": format_number(rating_offshore_MW,1),
         "Utility Scale (FLOW)":format_number(rating_offshore_MW,1), 
         "Residential (DW)": "20 (kW)", "Commercial (DW)": "100 (kW)", "Large (DW)": format_number(1.5,1)},
        {"Parameter": "Capital expenditures (CapEx)", "Units": "$/kW", 
         "Utility Scale (LBW)": format_number(lbw_df['Value ($/kW)'].sum()), 
         "Utility Scale (FBOW)": format_number(fbow_df['Value ($/kW)'].sum()), 
         "Utility Scale (FLOW)": format_number(flow_df['Value ($/kW)'].sum()), 
         "Residential (DW)": format_number(dw_20kW_df['Value ($/kW)'].sum()), 
         "Commercial (DW)": format_number(dw_100kW_df['Value ($/kW)'].sum()), 
         "Large (DW)": format_number(dw_1500kW_df['Value ($/kW)'].sum())},
        {"Parameter": "Fixed charge rate (FCR) (real)", "Units": "%", 
         "Utility Scale (LBW)": format_number(lbw_df['Fixed charge rate (FCR) (real)'].mean() * 100, 2), 
         "Utility Scale (FBOW)": format_number(fbow_df['Fixed charge rate (FCR) (real)'].mean() * 100, 2), 
         "Utility Scale (FLOW)": format_number(flow_df['Fixed charge rate (FCR) (real)'].mean() * 100, 2), 
         "Residential (DW)": format_number(dw_20kW_df['Fixed charge rate (FCR) (real)'].mean() * 100, 2), 
         "Commercial (DW)": format_number(dw_100kW_df['Fixed charge rate (FCR) (real)'].mean() * 100, 2), 
         "Large (DW)": format_number(dw_1500kW_df['Fixed charge rate (FCR) (real)'].mean() * 100, 2)},
        {"Parameter": "Operational expenditures (OpEx)", "Units": "$/kW/yr", 
         "Utility Scale (LBW)": format_number(lbw_df.loc[lbw_df['Category'] == 'OpEx', 'Value ($/kW-yr)'].sum()), 
         "Utility Scale (FBOW)": format_number(fbow_df.loc[fbow_df['Category'] == 'OpEx', 'Value ($/kW-yr)'].sum()), 
         "Utility Scale (FLOW)": format_number(flow_df.loc[flow_df['Category'] == 'OpEx', 'Value ($/kW-yr)'].sum()), 
         "Residential (DW)": format_number(dw_20kW_df.loc[dw_20kW_df['Category'] == 'OpEx', 'Value ($/kW-yr)'].sum()), 
         "Commercial (DW)": format_number(dw_100kW_df.loc[dw_100kW_df['Category'] == 'OpEx', 'Value ($/kW-yr)'].sum()), 
         "Large (DW)": format_number(dw_1500kW_df.loc[dw_1500kW_df['Category'] == 'OpEx', 'Value ($/kW-yr)'].sum())},
        {"Parameter": "Net annual energy production", "Units": "MWh/MW/yr", 
         "Utility Scale (LBW)": format_number(lbw_df['Net AEP (MWh/kW/yr)'][0] * 1000), 
         "Utility Scale (FBOW)": format_number(fbow_df['Net AEP (MWh/kW/yr)'][0] * 1000), 
         "Utility Scale (FLOW)": format_number(flow_df['Net AEP (MWh/kW/yr)'][0] * 1000), 
         "Residential (DW)": format_number(dw_20kW_df['Net AEP (MWh/kW/yr)'][0] * 1000), 
         "Commercial (DW)": format_number(dw_100kW_df['Net AEP (MWh/kW/yr)'][0] * 1000), 
         "Large (DW)": format_number(dw_1500kW_df['Net AEP (MWh/kW/yr)'][0] * 1000)},
        {"Parameter": "Levelized cost of energy (LCOE)", "Units": "$/MWh", 
         "Utility Scale (LBW)": format_number(lbw_df['Value ($/MWh)'].sum()), 
         "Utility Scale (FBOW)": format_number(fbow_df['Value ($/MWh)'].sum()), 
         "Utility Scale (FLOW)": format_number(flow_df['Value ($/MWh)'].sum()), 
         "Residential (DW)": format_number(dw_20kW_df['Value ($/MWh)'].sum()), 
         "Commercial (DW)": format_number(dw_100kW_df['Value ($/MWh)'].sum()), 
         "Large (DW)": format_number(dw_1500kW_df['Value ($/MWh)'].sum())},
    ]

    # Create a DataFrame from the rows
    table_df = pd.DataFrame(rows)

    # Add the multi-index columns
    table_df.columns = pd.MultiIndex.from_tuples([
        ("", "Parameter"), 
        ("", "Units"),
        ("Land-Based", "Utility Scale"),
        ("Offshore", "Utility Scale (Fixed-Bottom)"),
        ("Offshore", "Utility Scale (Floating)"),
        ("Distributed", "Single Turbine (Residential)"),
        ("Distributed", "Single Turbine (Commercial)"),
        ("Distributed", "Single Turbine (Large)")
    ])

    return table_df

def save_technology_tables(df):

    # Split the dataframe into three based on technology
    land_based_df = df.iloc[:, [0, 1, 2]]
    display(land_based_df)
    offshore_df = df.iloc[:, [0, 1, 3, 4]]
    display(offshore_df)
    distributed_df = df.iloc[:, [0, 1, 5, 6, 7]]
    display(distributed_df)
    
    # Save each dataframe as a separate CSV file
    land_based_df.to_csv('Tables/Summary_Table_LBW.csv', index=False)
    offshore_df.to_csv('Tables/Summary_Table_OSW.csv', index=False)
    distributed_df.to_csv('Tables/Summary_Table_DW.csv', index=False)
    
    
def create_offshore_opex_summary_table(fixed_df, floating_df):
    
    # Define a dictionary to hold summary data
    summary = {
        "Parameter": [],
        "Fixed Value ($/kW-yr)": [],
        "Floating Value ($/kW-yr)": []
    }

    # Define categories to summarize
    op_ex_categories = {
        "Maintenance": ["Labor (technicians)", "Materials", "Equipment (vessels)"],
        "Operations": ["Management administration", "Port fees", "Insurance"]
    }

    # Function to get the total value for a given item
    def get_total_value(df, item):
        # Ensure the item is correctly specified
        if 'Component' in df.columns:
            values = df[df['Component'] == item]['Value ($/kW-yr)']
            return values.sum() if not values.empty else 0
        else:
            print("Error: 'Component' column is missing.")
            return 0

    # Add values for Maintenance and Operations
    for category, items in op_ex_categories.items():
        summary["Parameter"].append(category)
        fixed_total = round(sum(get_total_value(fixed_df, item) for item in items))
        floating_total = round(sum(get_total_value(floating_df, item) for item in items))
        summary["Fixed Value ($/kW-yr)"].append(fixed_total)
        summary["Floating Value ($/kW-yr)"].append(floating_total)

        # Add details for each item
        for item in items:
            fixed_value = round(get_total_value(fixed_df, item))
            floating_value = round(get_total_value(floating_df, item))
            summary["Parameter"].append(f"  {item}")
            summary["Fixed Value ($/kW-yr)"].append(fixed_value)
            summary["Floating Value ($/kW-yr)"].append(floating_value)

    # Add total OpEx
    total_fixed_op_ex = round(sum([summary["Fixed Value ($/kW-yr)"][i] for i in range(len(summary["Parameter"])) if summary["Parameter"][i] in op_ex_categories]))
    total_floating_op_ex = round(sum([summary["Floating Value ($/kW-yr)"][i] for i in range(len(summary["Parameter"])) if summary["Parameter"][i] in op_ex_categories]))
    
    summary["Parameter"].append("Total OpEx")
    summary["Fixed Value ($/kW-yr)"].append(total_fixed_op_ex)
    summary["Floating Value ($/kW-yr)"].append(total_floating_op_ex)

    # Create DataFrame from summary
    summary_df = pd.DataFrame(summary)

    return summary_df


def create_landbased_opex_summary_table(df):
    # Strip any leading or trailing spaces from column names
    df.columns = df.columns.str.strip()
    
    # Filter out the row with 'Operational Expenditure'
    operational_expenditures = df[df['Category'] == 'OpEx']
    
    if operational_expenditures.empty:
        raise ValueError("No Operational Expenditure data found in the DataFrame.")
    
    
    # Extract necessary values (check column names here)
    try:
        value = operational_expenditures.iloc[0]['Value ($/kW-yr)']
    except KeyError:
        value = operational_expenditures.iloc[0]['Value ($/kW)']  # Adjust if necessary
    unit = '$/kW/yr'
    
    # Create a new DataFrame with the desired format
    result_df = pd.DataFrame({
        'Parameter': ['Operational Expenditures'],
        'Value': [value.round().astype(int)],
        'Unit': [unit]
    })
    
    return result_df