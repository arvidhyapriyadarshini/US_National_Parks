# US_National_Parks
Data Science Projects - Data Visualization

The Dashboard can be accessed at: https://usnationalparks-arvidhya.streamlit.app

Dataset:

The dataset used for this project is from Kaggle: https://www.kaggle.com/datasets/thedevastator/the-united-states-national-parks
This dataset contains comprehensive information about national parks across the country. It includes details such as the state where each park is situated, the date of establishment, the park's total area, the annual count of recreation visitors, and a description highlighting the key features of each park.

Data Cleansing:

To clean the dataset and create a clean file suitable for visualization, the following data-cleaning steps were performed:

1. Remove duplicate records: Check for null values, and remove any duplicate rows in the dataset to ensure data integrity.
2. Handle missing values: Check for null values and handle them. 
3. Convert data types: Ensure each column has the correct type. For example, dates should be in the DateTime format, numeric columns should be numeric, and categorical columns should be appropriately labeled.
4. Standardize and clean text data and Remove any leading or trailing whitespace.
5. Perform feature engineering: Create new derived columns or features useful for visualization or analysis, such as extracting the year date column, State details, and Latitude and longitude details. 
6. Remove irrelevant columns: Identify columns that are not necessary for visualization purposes and remove them to reduce clutter and improve performance.
7. Once the data cleaning steps are completed, the cleaned dataset is saved to a new file in a format suitable for visualization, such as a CSV. 



