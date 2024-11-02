# Streamlit Dashboard for Interactive Data Visualization of Census and General Data
This is an interactive and user-friendly dashboard where users can upload their data files in either CSV or Excel format and interactively generate different types of charts like bar charts, pie charts, scatter plots, and choropleth maps (for displaying state-wise data in India).

# Problem  Statement

This project involves creating an interactive dashboard using Streamlit that allows users to visualize census and general datasets in various customizable chart formats. It provides a user-friendly interface where users can upload their data files in either CSV or Excel format and interactively generate different types of charts, including bar charts, pie charts, scatter plots, and choropleth maps (for displaying state-wise data in India). The aim is to make data exploration more accessible by offering dynamic filtering, flexible axis selection, and visualization customization, especially useful for non-technical users.



# User Manual

Below is a step-by-step guide for using the Streamlit dashboard:

  # a. Launching the Dashboard: 
  Run the script demo_interface.py in a Streamlit-compatible environment by executing streamlit run demo_interface.py in the terminal. 
  
  # b. Uploading a Dataset:  
  Select “Upload a file” and upload a CSV or Excel file. Ensure the file is either .csv, .xlsx, or .xls.
    
  # c. Dataset Display:
  Use the "Display Dataset" checkbox to view the uploaded dataset in a table format. This step 	helps verify data structure before charting.
  
  
  # d. Selecting Chart Types: 
  Check the “Display Charts” box in the sidebar to reveal options for different visualizations. 
  Choose from Bar, Pie, Scatter, and Choropleth Map charts by selecting corresponding checkboxes.

  
  # e. Configuring Axes for Charts: 
  Select columns for the X and Y axes. Ensure selections are compatible with the chosen chart type:
  Bar and pie charts require a categorical column for either one of the axes and a  numeric column for the other axis.
  Scatter plots require both X and Y axes to be numeric.
  
  
  # f. Applying Data Filters (Optional): 
  Enable “Apply Filters” to reveal sliders and dropdowns for selecting ranges for numeric columns or specific values for categorical columns.
  Numeric Range filters are provided for Numeric columns and Multiselectbox filters are provided for Categorical columns.
  Use filters to display only relevant data points within charts.
  Since column filters cannot be applied to choropleth maps, if the user select to apply filters while also selecting the option for choropleth maps or vice-versa, then the column filters won’t be applicable to any of the visualizations as long as the user does not deselect either of the options in the sidebar.  
  
  
  # g. Map Visualization:
  Ensure the dataset includes a state name column and a relevant numeric column like population or area for the choropleth map.
  Select the map visualization for state-wise data representation on India’s map.
  
  # h.Customization:
  
  Add titles for each chart and select colors from predefined options to personalize the visuals.
  
# Tutorial for navigating through our dashboard: 

Tutorial Video_Streamlit dashboard.mp4


