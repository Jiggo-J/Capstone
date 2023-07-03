#Import the neccessary libraries 

import locale

# Data Manipulation and Analysis
import pandas as pd
import numpy as np

# Visualization
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from branca.colormap import linear
import plotly.graph_objects as go
import altair as alt

# Machine Learning
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression

# Streamlit
import streamlit as st
from streamlit_folium import folium_static

from scipy.stats import ttest_ind, f_oneway, chi2_contingency




# Define the format_number function
def format_number(number):
    if isinstance(number, str):
        return number
    else:
        try:
            formatted_number = "{:,.2f}".format(float(number))
            return formatted_number
        except ValueError:
            return "Invalid Number"

#Define Background function 
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://techbarcelona.com/wp-content/uploads/Esade_RLU-4.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
                background-repeat: no-repeat;
                width: <155px>;
                height: <106px>;
                display: inline-block;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
#######
###########
# Set the background color to gray
page_bg_img = """
    <style>
    [data-testid="stSidebarNav"]{
    background-color: #e5e5f7;
    opacity: 0.6;
    background-image: radial-gradient(#444cf7 0.5px, #e5e5f7 0.5px);
    background-size: 10px 10px;
    }
    </style>
    """
st.markdown(page_bg_img, unsafe_allow_html=True)

#We import the database
#Data Import AWS
df = pd.read_excel('s3://feacapstone/Capstone Database.xlsx')
df_cashflow = pd.read_excel('s3://feacapstone/cashflow_adjusted.xlsx')

#df = pd.read_excel('C:\\Users\\jansc\\Python_Scripts\\Capstone\\Capstone Database.xlsx') 
#df_cashflow = pd.read_excel('C:\\Users\\jansc\\Python_Scripts\\Capstone\\cashflow_adjusted.xlsx')

########## Here we start to develop the App

# Define app layout
st.title('M&A App')

#Add Logos
# Add pictures in the sidebar
from PIL import Image
#Image Import AWS
image1 = Image.open('s3://feacapstone/Esade.png')
image = Image.open('s3://feacapstone/Deloitte.png')

#image1 = Image.open('C:\\Users\\jansc\\Python_Scripts\\Capstone\\Esade.png')
#image = Image.open('C:\\Users\\jansc\\Python_Scripts\\Capstone\\Deloitte.png')

image.thumbnail((200, 200))
image1.thumbnail((200, 200))

st.sidebar.image(image1)
st.sidebar.image(image, caption='Developed by Esade and Deloitte')

# Add sidebar for navigation

menu = ['Home', 'Information Overview', 'Company Financial Efficiency Ratios','Market Analysis', 'Valuation Calculator']
choice = st.sidebar.selectbox('Select an option', menu)


if choice == 'Home':
    st.title("Welcome to the M&A Financial App")
    st.write("""
    The M&A Financial App is a sophisticated tool designed to analyze investment opportunities across diverse sectors and industries. Our mission is to empower users to efficiently identify potential targets for M&A activity through comprehensive financial analysis.
    """)

    st.markdown("### Key Features")
    st.write("""
    - Access an extensive database of companies with comprehensive financial data
    - Calculate crucial financial ratios and metrics for each company
    - Be able to make multiple comparisons fo different companies and variables
    - Ability to make market analysis of different industires
    - A calculator that gives the projected cashflows and gives a valuation for the company
    """)

    st.markdown("### Explore the App")
    st.write("""
    Navigate through different sections of the app using the comprehensive menu on the left, including:
    - **Information Overview**: Gain a high-level summary of the companies in the database
    - **Company Financial Efficiency Ratios**: Analyze the financial ratios and efficiency of individual companies
    - **Market Analysis**: Explore trends and gain valuable insights related to the market and industry
    - **Valuation Calculator**: Calculate the value of any given company
    """)

    st.markdown("### Get Started")
    st.write("Ready to unlock a world of investment opportunities? Seamlessly navigate through the menu on the left to embark on your financial analysis journey!")

    
elif choice == 'Information Overview':

        st.title("Key Information Overview")

        # Sidebar for selecting a country
        country_names = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Select a Country:", country_names)

        # Filter dataframe for the selected country
        country_data = df[df['Country'] == selected_country]

        # Sidebar for selecting a company
        company_names = country_data['Name'].unique()
        selected_company = st.sidebar.selectbox("Select a Company:", company_names)

        # Filter dataframe for the selected company
        company_data = df[df['Name'] == selected_company]

        # Sidebar for selecting a year
        year_list = ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
        selected_year = st.sidebar.selectbox("Select a Year for Information Overview:", year_list)


        filtered_data = company_data[['Name', 'Tax ID', 'City', 'BvD Number', 'Autonomous Community', 'Postal Code', 'Website', 'Province', 'Country', 'Share Capital (thousand EUR)', 'Stock Market Price'] +
                                    ['Operating Revenues (thousand EUR) ' + selected_year,
                                     'EBITDA (thousand EUR) ' + selected_year,
                                     'Gross result (thousand EUR) ' + selected_year,
                                     'Financial income (thousand EUR) ' + selected_year,
                                     'Operating result (thousand EUR) ' + selected_year,
                                     'Financial expenses (thousand EUR) ' + selected_year,
                                     'Corporate income tax (thousand EUR) ' + selected_year,
                                     'Net profit (thousand EUR) ' + selected_year,
                                     'Personnel expenses (thousand EUR) ' + selected_year,
                                     'Goods and materials consumption (thousand EUR) ' + selected_year,
                                     'Materials (thousand EUR) ' + selected_year,
                                     'Cash flow (thousand EUR) ' + selected_year,
                                     'EBIT (thousand EUR) ' + selected_year,
                                     'Total assets (thousand EUR) ' + selected_year,
                                     'Current assets (thousand EUR) ' + selected_year,
                                     'Receivables (thousand EUR) ' + selected_year,
                                     'Inventory (thousand EUR) ' + selected_year,
                                     'Fixed assets (thousand EUR) ' + selected_year,
                                     'Intangible assets (thousand EUR) ' + selected_year,
                                     'Tangible assets (thousand EUR) ' + selected_year,
                                     'Other fixed liabilities (thousand EUR) ' + selected_year,
                                     'Total liabilities and equity (thousand EUR) ' + selected_year,
                                     'Working capital (thousand EUR) ' + selected_year,
                                     'Number of employees ' + selected_year,
                                     'Financial debts (thousand EUR) ' + selected_year,
                                     'Fixed liabilities (thousand EUR) ' + selected_year,
                                     'Liquid liabilities (thousand EUR) ' + selected_year,
                                     'Return on Equity (%), ' + selected_year,
                                     'Return on Total Assets (%), ' + selected_year,
                                     'Profit Margin (%), ' + selected_year,
                                     'Solvency Ratio (%), ' + selected_year,
                                     'Liquidity Ratio (%), ' + selected_year,
                                     'Leverage (%), ' + selected_year,
                                     'Profit per Employee (thousands), ' + selected_year,
                                     'Average Employee Cost (thousands), ' + selected_year,
                                     'Total Assets per Employee (thousands), ' + selected_year,
                                     'Personnel Expenses (%), ' + selected_year,
                                     'Total Assets (%), ' + selected_year,
                                     'Equity (%), ' + selected_year,
                                     'Long-term Creditors (%), ' + selected_year,
                                     'Working Capital (%), ' + selected_year,
                                     'Treasury (%), ' + selected_year,
                                     'Equity (thousand EUR) ' + selected_year]]

        # Add the 'Year' column to filtered_data
        filtered_data['Year'] = selected_year


        # Get the column names for the selected year
        revenue_column = 'Operating Revenues (thousand EUR) ' + selected_year
        ebitda_column = 'EBITDA (thousand EUR) ' + selected_year
        gross_profit_column = 'Gross result (thousand EUR) ' + selected_year
        
        financial_income_column = 'Financial income (thousand EUR) ' + selected_year
        operating_result_column = 'Operating result (thousand EUR) ' + selected_year
        financial_expenses_column = 'Financial expenses (thousand EUR) ' + selected_year
        corporate_income_tax_column = 'Corporate income tax (thousand EUR) ' + selected_year
        net_profit_column = 'Net profit (thousand EUR) ' + selected_year
        personnel_expenses_column = 'Personnel expenses (thousand EUR) ' + selected_year
        goods_consumption_column = 'Goods and materials consumption (thousand EUR) ' + selected_year
        
        materials_column = 'Materials (thousand EUR) ' + selected_year
        cash_flow_column = 'Cash flow (thousand EUR) ' + selected_year
        ebit_column = 'EBIT (thousand EUR) ' + selected_year
        total_assets_column = 'Total assets (thousand EUR) ' + selected_year
        current_assets_column = 'Current assets (thousand EUR) ' + selected_year
        receivables_column = 'Receivables (thousand EUR) ' + selected_year
        inventory_column = 'Inventory (thousand EUR) ' + selected_year
        fixed_assets_column = 'Fixed assets (thousand EUR) ' + selected_year
        
        intangible_assets_column = 'Intangible assets (thousand EUR) ' + selected_year
        tangible_assets_column = 'Tangible assets (thousand EUR) ' + selected_year
        other_fixed_liabilities_column = 'Other fixed liabilities (thousand EUR) ' + selected_year
        total_liabilities_equity_column = 'Total liabilities and equity (thousand EUR) ' + selected_year
        working_capital_column = 'Working capital (thousand EUR) ' + selected_year
        number_employees_column = 'Number of employees ' + selected_year
        financial_debts_column = 'Financial debts (thousand EUR) ' + selected_year
        
        fixed_liabilities_column = 'Fixed liabilities (thousand EUR) ' + selected_year
        liquid_liabilities_column = 'Liquid liabilities (thousand EUR) ' + selected_year
        return_equity_column = 'Return on Equity (%), ' + selected_year
        return_assets_column = 'Return on Total Assets (%), ' + selected_year
        profit_margin_column = 'Profit Margin (%), ' + selected_year
        solvency_ratio_column = 'Solvency Ratio (%), ' + selected_year
        liquidity_ratio_column = 'Liquidity Ratio (%), ' + selected_year
        
        leverage_column = 'Leverage (%), ' + selected_year
        profit_per_employee_column = 'Profit per Employee (thousands), ' + selected_year
        average_employee_cost_column = 'Average Employee Cost (thousands), ' + selected_year
        total_assets_per_employee_column = 'Total Assets per Employee (thousands), ' + selected_year
        personnel_expenses_column = 'Personnel Expenses (%) ' + selected_year
        total_assets_column = 'Total Assets (%), ' + selected_year
        equity_column = 'Equity (%), ' + selected_year
        long_term_creditors_column = 'Long-term Creditors (%), ' + selected_year
        working_capital_ratio_column = 'Working Capital (%), ' + selected_year
        treasury_column = 'Treasury (%), ' + selected_year
        Equity_column = 'Equity (thousand EUR)' + selected_year


        

        # Check if the columns exist in the company_data DataFrame
        if revenue_column in company_data.columns:
            filtered_data[revenue_column] = company_data[revenue_column]
        if ebitda_column in company_data.columns:
            filtered_data[ebitda_column] = company_data[ebitda_column]
        if gross_profit_column in company_data.columns:
            filtered_data[gross_profit_column] = company_data[gross_profit_column]
        if financial_income_column in company_data.columns:
            filtered_data[financial_income_column] = company_data[financial_income_column]
        if operating_result_column in company_data.columns:
            filtered_data[operating_result_column] = company_data[operating_result_column]
        if financial_expenses_column in company_data.columns:
            filtered_data[financial_expenses_column] = company_data[financial_expenses_column]
        if corporate_income_tax_column in company_data.columns:
            filtered_data[corporate_income_tax_column] = company_data[corporate_income_tax_column]
        if net_profit_column in company_data.columns:
            filtered_data[net_profit_column] = company_data[net_profit_column]
        if personnel_expenses_column in company_data.columns:
            filtered_data[personnel_expenses_column] = company_data[personnel_expenses_column]
        if goods_consumption_column in company_data.columns:
            filtered_data[goods_consumption_column] = company_data[goods_consumption_column]
        if materials_column in company_data.columns:
            filtered_data[materials_column] = company_data[materials_column]
        if cash_flow_column in company_data.columns:
            filtered_data[cash_flow_column] = company_data[cash_flow_column]
        if ebit_column in company_data.columns:
            filtered_data[ebit_column] = company_data[ebit_column]
        if total_assets_column in company_data.columns:
            filtered_data[total_assets_column] = company_data[total_assets_column]
        if current_assets_column in company_data.columns:
            filtered_data[current_assets_column] = company_data[current_assets_column]
        if receivables_column in company_data.columns:
            filtered_data[receivables_column] = company_data[receivables_column]
        if inventory_column in company_data.columns:
            filtered_data[inventory_column] = company_data[inventory_column]
        if fixed_assets_column in company_data.columns:
            filtered_data[fixed_assets_column] = company_data[fixed_assets_column]          
        if intangible_assets_column in company_data.columns:
            filtered_data[intangible_assets_column] = company_data[intangible_assets_column]
        if tangible_assets_column in company_data.columns:
            filtered_data[tangible_assets_column] = company_data[tangible_assets_column]
        if other_fixed_liabilities_column in company_data.columns:
            filtered_data[other_fixed_liabilities_column] = company_data[other_fixed_liabilities_column]
        if total_liabilities_equity_column in company_data.columns:
            filtered_data[total_liabilities_equity_column] = company_data[total_liabilities_equity_column]
        if working_capital_column in company_data.columns:
            filtered_data[working_capital_column] = company_data[working_capital_column]
        if number_employees_column in company_data.columns:
            filtered_data[number_employees_column] = company_data[number_employees_column]
        if financial_debts_column in company_data.columns:
            filtered_data[financial_debts_column] = company_data[financial_debts_column]         
        if fixed_liabilities_column in company_data.columns:
            filtered_data[fixed_liabilities_column] = company_data[fixed_liabilities_column]
        if liquid_liabilities_column in company_data.columns:
            filtered_data[liquid_liabilities_column] = company_data[liquid_liabilities_column]
        if return_equity_column in company_data.columns:
            filtered_data[return_equity_column] = company_data[return_equity_column]
        if return_assets_column in company_data.columns:
            filtered_data[return_assets_column] = company_data[return_assets_column]
        if profit_margin_column in company_data.columns:
            filtered_data[profit_margin_column] = company_data[profit_margin_column]
        if solvency_ratio_column in company_data.columns:
            filtered_data[solvency_ratio_column] = company_data[solvency_ratio_column]
        if liquidity_ratio_column in company_data.columns:
            filtered_data[liquidity_ratio_column] = company_data[liquidity_ratio_column]           
        if leverage_column in company_data.columns:
            filtered_data[leverage_column] = company_data[leverage_column]
        if profit_per_employee_column in company_data.columns:
            filtered_data[profit_per_employee_column] = company_data[profit_per_employee_column]
        if average_employee_cost_column in company_data.columns:
            filtered_data[average_employee_cost_column] = company_data[average_employee_cost_column]
        if total_assets_per_employee_column in company_data.columns:
            filtered_data[total_assets_per_employee_column] = company_data[total_assets_per_employee_column]
        if personnel_expenses_column in company_data.columns:
            filtered_data[personnel_expenses_column] = company_data[personnel_expenses_column]
        if total_assets_column in company_data.columns:
            filtered_data[total_assets_column] = company_data[total_assets_column]
        if equity_column in company_data.columns:
            filtered_data[equity_column] = company_data[equity_column]
        if long_term_creditors_column in company_data.columns:
            filtered_data[long_term_creditors_column] = company_data[long_term_creditors_column]
        if working_capital_ratio_column in company_data.columns:
            filtered_data[working_capital_ratio_column] = company_data[working_capital_ratio_column]
        if treasury_column in company_data.columns:
            filtered_data[treasury_column] = company_data[treasury_column]
        if Equity_column in company_data.columns:
            filtered_data[Equity_column] = company_data[Equity_column]


        col1, col2 = st.columns(2)
        
        # Display All the key insights
        with col1:
            st.write(f"**Operating Revenue (in thousand EUR):** {format_number(company_data['Operating Revenues (thousand EUR) ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Gross Profit (in thousand EUR):** {format_number(company_data['Gross result (thousand EUR) ' + selected_year].values[0])}")
    
        with col1:
            st.write(f"**EBITDA (in thousand EUR):** {format_number(company_data['EBITDA (thousand EUR) ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Net Income (in thousand EUR):** {format_number(company_data['Net profit (thousand EUR) ' + selected_year].values[0])}")

        with col1:
            st.write(f"**Return on Equity (%):** {format_number(company_data['Return on Equity (%), ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Return on Total Assets (%):** {format_number(company_data['Return on Total Assets (%), ' + selected_year].values[0])}")

        with col1:
            st.write(f"**Profit Margin (%):** {format_number(company_data['Profit Margin (%), ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Solvency Ratio (%):** {format_number(company_data['Solvency Ratio (%), ' + selected_year].values[0])}")

        with col1:
            st.write(f"**Liquidity Ratio (%):** {format_number(company_data['Liquidity Ratio (%), ' + selected_year].values[0])}")
        with col2:
            st.write(f"**Leverage Ratio (%):** {format_number(company_data['Leverage (%), ' + selected_year].values[0])}")
            

        
           # Additional Statistical Info button
        if st.button("Additional Info"):
            st.subheader("Additional Info")
                    
            st.table(filtered_data)



 


        # Set a new list of variables
        variables = [
            'Operating Revenues (thousand EUR)',
            'EBITDA (thousand EUR)',
            'Gross result (thousand EUR)',
            'Financial income (thousand EUR)',
            'Operating result (thousand EUR)',
            'Financial expenses (thousand EUR)',
            'Corporate income tax (thousand EUR)',
            'Net profit (thousand EUR)',
            'Personnel expenses (thousand EUR)',
            'Goods and materials consumption (thousand EUR)',
            'Materials (thousand EUR)',
            'Cash flow (thousand EUR)',
            'EBIT (thousand EUR)',
            'Total assets (thousand EUR)',
            'Current assets (thousand EUR)',
            'Receivables (thousand EUR)',
            'Inventory (thousand EUR)',
            'Fixed assets (thousand EUR)',
            'Intangible assets (thousand EUR)',
            'Tangible assets (thousand EUR)',
            'Other fixed liabilities (thousand EUR)',
            'Total liabilities and equity (thousand EUR)',
            'Working capital (thousand EUR)',
            'Number of employees',
            'Financial debts (thousand EUR)',
            'Fixed liabilities (thousand EUR)',
            'Liquid liabilities (thousand EUR)',
            'Return on Equity (%)',
            'Return on Total Assets (%)',
            'Profit Margin (%)',
            'Solvency Ratio (%)',
            'Liquidity Ratio (%)',
            'Leverage (%)',
            'Profit per Employee (thousands)',
            'Average Employee Cost (thousands)',
            'Total Assets per Employee (thousands)',
            'Personnel Expenses (%)',
            'Total Assets (%)',
            'Equity (%)',
            'Long-term Creditors (%)',
            'Working Capital (%)',
            'Treasury (%)',
            'Equity (thousand EUR)'
        ]
        

        selected_variable = st.sidebar.selectbox("Select a Variable for Plotting the Hisogram:", variables)
        column_names = [column for column in df.columns if selected_variable in column]
        years = [column.split()[-1] for column in column_names]
        filtered_df = df[column_names]

        # Plotting
        data = [go.Bar(x=years, y=filtered_df.iloc[0].values)]
        layout = go.Layout(title=f"{selected_variable} - Evolution Over the Years")
        fig = go.Figure(data=data, layout=layout)
        
        st.title("Histogram Plot")

        #We want the filters below the histogram and not in the left side of the app
        selected_variable = st.selectbox("Select a Variable for Plotting:", variables)
        selected_companies = st.multiselect("Select Companies:", company_names)
        st.write("Variable Chosen:", selected_variable)

        # Here we plot the histogram
        histogram_data = []
        for company in selected_companies or []:
            company_data = df[df['Name'] == company]
            column_names = [column for column in company_data.columns if selected_variable in column]
            years = [column.split()[-1] for column in column_names]
            values = company_data[column_names].values.flatten().tolist()
            histogram_data.append(go.Bar(name=company, x=years, y=values))


        histogram_layout = go.Layout(title=f"{selected_variable} - Histogram Plot")
        histogram_fig = go.Figure(data=histogram_data, layout=histogram_layout)

        # Plot it
        st.plotly_chart(histogram_fig)

        # Additional visualizations - Line Chart
        st.subheader("Line Chart")

        # PLot the line chart / prepare the data
        line_data = []
        for company in selected_companies or []:
            company_data = df[df['Name'] == company]
            column_names = [column for column in company_data.columns if selected_variable in column]
            years = [column.split()[-1] for column in column_names]
            values = company_data[column_names].values.flatten().tolist()
            sorted_data = sorted(zip(years, values))
            sorted_years, sorted_values = zip(*sorted_data)
            line_data.append(go.Scatter(x=sorted_years, y=sorted_values, mode='lines', name=company))

        line_layout = go.Layout(title=f"{selected_variable} - Line Chart", xaxis_title="Year", yaxis_title=selected_variable)
        line_fig = go.Figure(data=line_data, layout=line_layout)
        st.plotly_chart(line_fig)

        

        # Additional Statistical Info button
        if st.button("Additional Statistical Info"):
            st.subheader("Summary Statistics")

            # Create a new dataframe to store all the values
            summary_stats = pd.DataFrame(columns=["Company", "Variable", "Mean", "Median", "Standard Deviation"])

            for company in selected_companies or []:
                company_data = df[df['Name'] == company]
                column_names = [column for column in company_data.columns if selected_variable in column]
                variable_data = company_data[column_names].values.flatten()

                mean = np.mean(variable_data)
                median = np.median(variable_data)
                std_dev = np.std(variable_data)

                summary_stats = summary_stats.append(
                    {"Company": company, "Variable": selected_variable, "Mean": mean, "Median": median,
                     "Standard Deviation": std_dev},
                    ignore_index=True
                )

                #We display de info
                st.write(f"**Company:** {company}")
                st.write(f"**Variable:** {selected_variable}")
                st.write(f"**Mean:** {mean:,.0f}")
                st.write(f"**Median:** {median:,.0f}")
                st.write(f"**Standard Deviation:** {std_dev:,.0f}")

                st.write("---")


            # Box Plot
            st.write("**Box Plot**")

            box_data = []
            for company in selected_companies or []:
                company_data = df[df['Name'] == company]
                column_names = [column for column in company_data.columns if selected_variable in column]
                values = company_data[column_names].values.flatten().tolist()
                box_data.append(go.Box(name=company, y=values))

            box_layout = go.Layout(title=f"{selected_variable} - Box Plot")
            box_fig = go.Figure(data=box_data, layout=box_layout)
            st.plotly_chart(box_fig)

            # Scatter Plot
            st.write("**Scatter Plot**")

            scatter_data = []
            for company in selected_companies or []:
                company_data = df[df['Name'] == company]
                column_names = [column for column in company_data.columns if selected_variable in column]
                years = [column.split()[-1] for column in column_names]
                values = company_data[column_names].values.flatten().tolist()
                scatter_data.append(go.Scatter(x=years, y=values, mode='markers', name=company))

            scatter_layout = go.Layout(title=f"{selected_variable} - Scatter Plot", xaxis_title="Year",
                                       yaxis_title=selected_variable)
            scatter_fig = go.Figure(data=scatter_data, layout=scatter_layout)
            st.plotly_chart(scatter_fig)

            # Display the summary statistics DataFrame
            st.subheader("Summary Statistics Table")
            st.dataframe(summary_stats)
         
                    
                   



# Company Financial Efficiency Ratios


elif choice == 'Company Financial Efficiency Ratios':
    st.title("Company Financial Efficiency Ratios")


    selected_companies = st.multiselect("Select Companies", df["Name"].unique())
    year_range = range(2010, 2023)  # Update to include 2022

    st.write("Metric Selected : ")

    # Calculate ratios for all years
    ratios_data = []
    for company_name in selected_companies:
        for year in year_range:
            year_column = str(year)

            filtered_df = df[df['Name'] == company_name]
            filtered_df = filtered_df.filter(regex=f'.*{year_column}$')

            if filtered_df.empty:
                continue

            # Convert columns to numeric values in order to standarize it and avoid the errors
            numeric_columns = [
                f'Operating Revenues (thousand EUR) {year_column}',
                f'Gross result (thousand EUR) {year_column}',
                f'Operating result (thousand EUR) {year_column}',
                f'Net profit (thousand EUR) {year_column}',
                f'Total assets (thousand EUR) {year_column}',
                f'Current assets (thousand EUR) {year_column}',
                f'Inventory (thousand EUR) {year_column}',
                f'Equity (thousand EUR) {year_column}',  
                f'Financial debts (thousand EUR) {year_column}'  
            ]
            filtered_df[numeric_columns] = filtered_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

            operating_revenues = filtered_df[f'Operating Revenues (thousand EUR) {year_column}']
            gross_result = filtered_df[f'Gross result (thousand EUR) {year_column}']
            operating_result = filtered_df[f'Operating result (thousand EUR) {year_column}']
            net_profit = filtered_df[f'Net profit (thousand EUR) {year_column}']
            total_assets = filtered_df[f'Total assets (thousand EUR) {year_column}']
            current_assets = filtered_df[f'Current assets (thousand EUR) {year_column}']
            inventory = filtered_df[f'Inventory (thousand EUR) {year_column}']
            equity = filtered_df[f'Equity (thousand EUR) {year_column}']  
            financial_debts = filtered_df[f'Financial debts (thousand EUR) {year_column}']  

            gross_margin = (gross_result / operating_revenues) * 100
            operating_margin = (operating_result / operating_revenues) * 100
            return_on_assets = (net_profit / total_assets) * 100
            net_profit_margin = (net_profit / operating_revenues) * 100
            current_ratio = current_assets / total_assets
            quick_ratio = (current_assets - inventory) / total_assets

            # New ratios
            debt_to_equity = (financial_debts / equity) * 100
            solvency = (equity / total_assets) * 100
            return_on_equity = (net_profit / equity) * 100

            ratios_data.append({
                "Company": company_name,
                "Year": year,
                "Gross Margin": gross_margin.values[0],
                "Operating Margin": operating_margin.values[0],
                "Return on Assets (ROA)": return_on_assets.values[0],
                "Net Profit Margin": net_profit_margin.values[0],
                "Current Ratio": current_ratio.values[0],
                "Quick Ratio": quick_ratio.values[0],
                "Debt to Equity (%)": debt_to_equity.values[0],
                "Solvency (%)": solvency.values[0],
                "Return on Equity (%)": return_on_equity.values[0]
            })


    # Create the dataframe for the ratios / margins and prepare the layout for display it / filter
    ratios_df = pd.DataFrame(ratios_data)


    selected_variables = st.sidebar.multiselect("Select Variables:", ratios_df.columns[2:])

    # Now we prepare the plot
    data = []
    for company in selected_companies:
        company_data = ratios_df[ratios_df["Company"] == company]
        for variable in selected_variables:
            data.append(go.Bar(x=company_data["Year"], y=company_data[variable], name=f"{company} - {variable}"))

    layout = go.Layout(
        title="Financial Efficiency Ratios - Evolution Over the Years",
        width=800
    )
    fig = go.Figure(data=data, layout=layout)

    # Bar chart
    st.plotly_chart(fig, use_container_width=False)

    # Trend Analysis
    st.subheader("Trend Analysis")

    # Once again we preapre the data as we have done before
    trend_data = []
    for company in selected_companies:
        company_data = ratios_df[ratios_df["Company"] == company]
        for variable in selected_variables:
            trend_data.append(go.Scatter(x=company_data["Year"], y=company_data[variable], mode="lines", name=f"{company} - {variable}"))

    # Create the layout
    trend_layout = go.Layout(
        title="Financial Efficiency Ratios - Trend Over the Years",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Ratio Value")
    )
    
    trend_fig = go.Figure(data=trend_data, layout=trend_layout)
    st.plotly_chart(trend_fig)

    # Calculate descriptive statistics for selected ratios
    if selected_variables:
        descriptive_stats = ratios_df[selected_variables].describe().T

        # Calculate additional insights
        descriptive_stats['Range'] = descriptive_stats['max'] - descriptive_stats['min']
        descriptive_stats['Variance'] = descriptive_stats['std'] ** 2
        descriptive_stats['Coefficient of Variation'] = (descriptive_stats['std'] / descriptive_stats['mean']) * 100

    # Display the info 
    st.subheader("Descriptive Statistics and Insights")

    if selected_variables:
        st.write(descriptive_stats[['mean', '50%', 'std', 'min', 'max', 'Range', 'Variance', 'Coefficient of Variation']].round(2))
    else:
        st.write("No variables selected.")

    #Some spaces for design 
    st.write("") 
    st.write("") 

    #We create the button for the correlation matrix 
    st.markdown("## Correlation Matrix")
    show_correlation_matrix = st.checkbox("Check to show correlation matrix")

    if show_correlation_matrix:
        st.subheader("Correlation Matrix")

        # Calculate the correlation matrix
        correlation_matrix = ratios_df.drop(columns=["Year"]).corr()
        available_ratios = correlation_matrix.columns.tolist()
        selected_ratios = st.multiselect("Select Ratios", available_ratios)
        selected_correlation_matrix = correlation_matrix.loc[selected_ratios, selected_ratios]
        selected_correlation_values = selected_correlation_matrix[selected_ratios].mean()

        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=selected_correlation_matrix.values,
            x=selected_ratios,
            y=selected_ratios,
            colorscale="Inferno",
            opacity=0.7,  # Set opacity to 0.7 for transparency
            zmin=-1,  # Set the minimum value for the color scale to -1
            zmax=1,  # Set the maximum value for the color scale to 1
            colorbar=dict(
                title="Correlation",
                titleside="right"
            )
        ))

        fig.update_layout(title="Correlation Heatmap")

        # Some hover effects
        fig.update_traces(hovertemplate="Variable A: %{y}<br>Variable B: %{x}<br>Correlation: %{z}<extra></extra>")

        # We plot it as always
        st.plotly_chart(fig)
        st.write("Correlation with Selected Ratios:")
        st.write(selected_correlation_values)

    #Now we create another button / checkbox to hide this section (another way of seeing the correlation between ratios / margins and the companies selcted
    st.markdown("## Quick analysis by Margin / Ratio by Year")
    show_global_inf = st.checkbox("Check to show correlation matrix", key="global_inf_checkbox")

    if show_global_inf:

        # Create a list of all available ratios again...
        ratios = [
            "Gross Margin",
            "Operating Margin",
            "Return on Assets (ROA)",
            "Net Profit Margin",
            "Current Ratio",
            "Quick Ratio",
            "Debt to Equity",
            "Solvency",
            "Return on Equity"
        ]

        # Here we add the year selection as the previous one was more general
        selected_companies = st.multiselect("Select Companies", df["Name"].unique(), key="companies_multiselect")
        year_range = range(2010, 2023)
        selected_year = st.selectbox("Select a Year", year_range)

        ratios_data = []
        for company_name in selected_companies:
            filtered_df = df[df['Name'] == company_name]
            filtered_df = filtered_df.filter(regex=f'.*{selected_year}$')

            if filtered_df.empty:
                continue

            operating_revenues = filtered_df[f'Operating Revenues (thousand EUR) {selected_year}']
            gross_result = filtered_df[f'Gross result (thousand EUR) {selected_year}']
            operating_result = filtered_df[f'Operating result (thousand EUR) {selected_year}']
            net_profit = filtered_df[f'Net profit (thousand EUR) {selected_year}']
            total_assets = filtered_df[f'Total assets (thousand EUR) {selected_year}']
            current_assets = filtered_df[f'Current assets (thousand EUR) {selected_year}']
            inventory = filtered_df[f'Inventory (thousand EUR) {selected_year}']
            financial_debts = filtered_df[f'Financial debts (thousand EUR) {selected_year}']
            equity = filtered_df[f'Equity (thousand EUR) {selected_year}']

            # Convert 'n.d.' values to NaN to avoid errors
            gross_result = gross_result.replace('n.d.', np.nan)
            operating_result = operating_result.replace('n.d.', np.nan)
            net_profit = net_profit.replace('n.d.', np.nan)
            total_assets = total_assets.replace('n.d.', np.nan)
            current_assets = current_assets.replace('n.d.', np.nan)
            inventory = inventory.replace('n.d.', np.nan)
            financial_debts = financial_debts.replace('n.d.', np.nan)
            equity = equity.replace('n.d.', np.nan)

            # Convert columns to float also to avoid errors as to standarize all the data outcomes
            gross_result = gross_result.astype(float)
            operating_result = operating_result.astype(float)
            net_profit = net_profit.astype(float)
            total_assets = total_assets.astype(float)
            current_assets = current_assets.astype(float)
            inventory = inventory.astype(float)
            financial_debts = financial_debts.astype(float)
            equity = equity.astype(float)

            # Calculate the ratios in order to add the into de df
            gross_margin = (gross_result / operating_revenues) * 100
            operating_margin = (operating_result / operating_revenues) * 100
            roa = (net_profit / total_assets) * 100
            net_profit_margin = (net_profit / operating_revenues) * 100
            current_ratio = current_assets / total_assets
            quick_ratio = (current_assets - inventory) / total_assets
            debt_to_equity = (financial_debts / equity) * 100
            solvency = (equity / total_assets) * 100
            return_on_equity = (net_profit / equity) * 100

            ratios_data.append({
                "Company": company_name,
                "Gross Margin": gross_margin.values[0],
                "Operating Margin": operating_margin.values[0],
                "Return on Assets (ROA)": roa.values[0],
                "Net Profit Margin": net_profit_margin.values[0],
                "Current Ratio": current_ratio.values[0],
                "Quick Ratio": quick_ratio.values[0],
                "Debt to Equity": debt_to_equity.values[0],
                "Solvency": solvency.values[0],
                "Return on Equity": return_on_equity.values[0]
            })

        ratios_df = pd.DataFrame(ratios_data)

        # Check if there are rows in the DataFrame for errors 
        if not ratios_df.empty:
            ratios_df.set_index("Company", inplace=True)

            # Sidebar for selecting the different variables
            x_ratio, y_ratio = st.columns(2)
            with x_ratio:
                x_axis_ratio = st.selectbox("Select a ratio/margin for the X axis", ratios)
            with y_ratio:
                y_axis_ratio = st.selectbox("Select a ratio/margin for the Y axis", ratios)

            # Plot all the data
            data = []
            for i, company in enumerate(ratios_df.index):
                x_values = [ratios_df.loc[company, x_axis_ratio]]
                y_values = [ratios_df.loc[company, y_axis_ratio]]
                text = [company]
                data.append(go.Scatter(x=x_values, y=y_values, mode='markers',
                                       text=text, marker=dict(size=10),
                                       hovertemplate="Company: %{text}<br>" + x_axis_ratio + ": %{x}<br>" +
                                       y_axis_ratio + ": %{y}", name=company))

            layout = go.Layout(title=f"{x_axis_ratio} vs {y_axis_ratio} - Global Information",
                               xaxis=dict(title=x_axis_ratio),
                               yaxis=dict(title=y_axis_ratio))
            fig = go.Figure(data=data, layout=layout)
            st.plotly_chart(fig, use_container_width=True)

            # Calculate correlation coefficient
            x_values = ratios_df[x_axis_ratio].values
            y_values = ratios_df[y_axis_ratio].values
            correlation_coefficient = np.corrcoef(x_values, y_values)[0, 1]

            # Display correlation analysis
            st.subheader("Correlation Analysis")
            st.write(f"The correlation coefficient between {x_axis_ratio} and {y_axis_ratio} is: {correlation_coefficient:.2f}")
        else:
            st.warning("No companies selected.")




# Market Analysis
elif choice == 'Market Analysis':
    st.title("Market Analysis & Growth(g) Forecast")


    
    st.write("Click the button below to execute calculations for Spain's individual growth rates projected over the next decade. These derived metrics can then be seamlessly integrated into the Valuation Calculator for enhanced financial analysis.")
    if st.button("Calculate growth rates"):
        import pandas as pd
        from pmdarima.arima import auto_arima

        # Sorting columns in ascending order to ensure the cash flow data is in chronological order
        df_cashflow = df_cashflow[df_cashflow.columns[::-1]]

        # We'll store all the predictions in this DataFrame
        predictions = pd.DataFrame()

        for i, row in df_cashflow.iterrows():
            # Ignore the company name column for ARIMA model
            cashflow_values = row.values

            # Ensure the data is numeric and handle any non-numeric values
            cashflow_values = pd.to_numeric(cashflow_values, errors='coerce')

            # Drop NaN values from the series
            cashflow_values = cashflow_values[~pd.isnull(cashflow_values)]

            if cashflow_values.size == 0:
                continue

            model = auto_arima(cashflow_values, start_p=1, start_q=1,
                            max_p=5, max_q=5, m=12,
                            start_P=0, seasonal=False,
                            d=1, D=1, trace=True,
                            error_action='ignore',   # we don't want to know if an order does not work
                            suppress_warnings=True,  # we don't want convergence warnings
                            stepwise=True)  # set to stepwise

            forecast, conf_int = model.predict(n_periods=11, return_conf_int=True)  # Forecasting for the next 10 years

            # Apply dampening factor
            dampening_factor = 1.0  # Adjust this as per requirement
            forecast = [value * (dampening_factor ** j) for j, value in enumerate(forecast)]

            predictions[i] = forecast

        # Transpose the predictions DataFrame and set appropriate column names
        predictions = predictions.T
        predictions.columns = range(2023, 2034)

        growth_rates = predictions.pct_change(axis=1)

        # Print out the result
        st.table(growth_rates.head(1))

    
    variables = [
            'Operating Revenues (thousand EUR)',
            'EBITDA (thousand EUR)',
            'Gross result (thousand EUR)',
            'Financial income (thousand EUR)',
            'Operating result (thousand EUR)',
            'Financial expenses (thousand EUR)',
            'Corporate income tax (thousand EUR)',
            'Net profit (thousand EUR)',
            'Personnel expenses (thousand EUR)',
            'Goods and materials consumption (thousand EUR)',
            'Materials (thousand EUR)',
            'Cash flow (thousand EUR)',
            'EBIT (thousand EUR)',
            'Total assets (thousand EUR)',
            'Current assets (thousand EUR)',
            'Receivables (thousand EUR)',
            'Inventory (thousand EUR)',
            'Fixed assets (thousand EUR)',
            'Intangible assets (thousand EUR)',
            'Tangible assets (thousand EUR)',
            'Other fixed liabilities (thousand EUR)',
            'Total liabilities and equity (thousand EUR)',
            'Working capital (thousand EUR)',
            'Number of employees',
            'Financial debts (thousand EUR)',
            'Fixed liabilities (thousand EUR)',
            'Liquid liabilities (thousand EUR)',
            'Return on Equity (%)',
            'Return on Total Assets (%)',
            'Profit Margin (%)',
            'Solvency Ratio (%)',
            'Liquidity Ratio (%)',
            'Leverage (%)',
            'Profit per Employee (thousands)',
            'Average Employee Cost (thousands)',
            'Total Assets per Employee (thousands)',
            'Personnel Expenses (%)',
            'Total Assets (%)',
            'Equity (%)',
            'Long-term Creditors (%)',
            'Working Capital (%)',
            'Treasury (%)',
            'Equity (thousand EUR)'
        ]

    plot_type = st.selectbox("Select Plot Type:", ["Histogram", "Line Plot"])

    selected_variable = st.selectbox("Select a Variable for Plotting:", variables)
    company_names = df['Name'].unique()
    selected_companies = st.multiselect("Select Companies:", company_names)

    st.write("Variable Chosen:", selected_variable)

    # Prepare the data for plotting
    plot_data = []
    for company in selected_companies or []:
        company_data = df[df['Name'] == company]
        column_names = [column for column in company_data.columns if selected_variable in column]
        years = [column.split()[-1] for column in column_names]
        values = company_data[column_names].values.flatten().tolist()
        if plot_type == "Histogram":
            plot_data.append(go.Bar(name=company, x=years, y=values))
        else:
            sorted_data = sorted(zip(years, values))
            sorted_years, sorted_values = zip(*sorted_data)
            plot_data.append(go.Scatter(x=sorted_years, y=sorted_values, mode='lines', name=company))

    # Calculate the market average for the selected variable
    market_data = df.copy()
    column_names = [column for column in market_data.columns if selected_variable in column]
    years = [column.split()[-1] for column in column_names]

    market_values = market_data[column_names].mean().tolist()
    lower_quartile_values = market_data[column_names].quantile(0.25).tolist()
    upper_quartile_values = market_data[column_names].quantile(0.75).tolist()

    sorted_market_values = sorted(zip(years, market_values))
    sorted_lower_values = sorted(zip(years, lower_quartile_values))
    sorted_upper_values = sorted(zip(years, upper_quartile_values))

    sorted_years, sorted_values = zip(*sorted_market_values)
    if plot_type == "Histogram":
        plot_data.append(go.Bar(name='Market Average', x=sorted_years, y=sorted_values))
    else:
        plot_data.append(go.Scatter(x=sorted_years, y=sorted_values, mode='lines', name='Market Average'))

    sorted_years, sorted_values = zip(*sorted_lower_values)
    if plot_type == "Histogram":
        plot_data.append(go.Bar(name='Lower Quartile', x=sorted_years, y=sorted_values))
    else:
        plot_data.append(go.Scatter(x=sorted_years, y=sorted_values, mode='lines', name='Lower Quartile'))

    sorted_years, sorted_values = zip(*sorted_upper_values)
    if plot_type == "Histogram":
        plot_data.append(go.Bar(name='Upper Quartile', x=sorted_years, y=sorted_values))
    else:
        plot_data.append(go.Scatter(x=sorted_years, y=sorted_values, mode='lines', name='Upper Quartile'))

    if plot_type == "Histogram":
        layout = go.Layout(title=f"{selected_variable} - Histogram Plot")
    else:
        layout = go.Layout(title=f"{selected_variable} - Line Chart", xaxis_title="Year", yaxis_title=selected_variable)

    fig = go.Figure(data=plot_data, layout=layout)

    st.plotly_chart(fig)


  


elif choice == "Valuation Calculator":
    st.title("Valuation Calculator")


    # Set the locale to the desired format
    locale.setlocale(locale.LC_ALL, 'en_US')


    st.subheader('DCF Valuation Calculator')
    company_name = st.selectbox('Select Company', df['Name'].unique())
    selected_company = df[df['Name'] == company_name]

    # Calculate projected free cash flows
    last_revenue = selected_company['Operating Revenues (thousand EUR) 2022'].sum()
    growth_rate = st.number_input('Growth Rate (%)', value=5.0)
    discount_rate = st.number_input('Discount Rate (%)', value=10.0)
    num_years = st.number_input('Number of Years', value=5, min_value=1)

    free_cash_flows = [last_revenue]
    for _ in range(num_years):
        last_revenue *= 1 + growth_rate / 100
        free_cash_flows.append(last_revenue)

    # Calculate present value of free cash flows
    present_value = 0
    discount_factors = []
    for year, cash_flow in enumerate(free_cash_flows, start=1):
        discount_factor = 1 / ((1 + discount_rate / 100) ** year)
        present_value += cash_flow * discount_factor
        discount_factors.append(discount_factor)

    # Calculate terminal value
    terminal_growth_rate = st.number_input('Terminal Growth Rate (%)', value=2.5)
    terminal_cash_flow = free_cash_flows[-1] * (1 + terminal_growth_rate / 100)
    terminal_discount_factor = 1 / ((discount_rate - terminal_growth_rate) / 100)
    terminal_value = terminal_cash_flow * terminal_discount_factor

    # Calculate enterprise value
    enterprise_value = present_value + terminal_value

    # Additional inputs

    shares_outstanding = st.number_input('Shares Outstanding (millions)', value=100)
    value_per_share = enterprise_value / (shares_outstanding * 1e6)

    # Format the numbers with thousands separator using commas for standarization purposes
    formatted_last_revenue = locale.format_string('%.0f', last_revenue, grouping=True)
    formatted_present_value = locale.format_string('%.0f', present_value, grouping=True)
    formatted_terminal_value = locale.format_string('%.0f', terminal_value, grouping=True)
    formatted_enterprise_value = locale.format_string('%.0f', enterprise_value, grouping=True)
    formatted_value_per_share = locale.format_string('%.2f', value_per_share)

    # Prepare data for the projected free cash flows table
    years = np.arange(1, num_years + 1)
    cash_flows_table = pd.DataFrame({'Year': years, 'Projected Free Cash Flows': free_cash_flows[:-1]})
    cash_flows_table['Projected Free Cash Flows'] = cash_flows_table['Projected Free Cash Flows'].apply(lambda x: locale.format_string('%.0f', x, grouping=True))

    # Calculate discount factors for each year
    discount_factors = [1 / ((1 + discount_rate / 100) ** year) for year in years]

    # Create a table to display the valuation results
    valuation_table = pd.DataFrame({
        'FCF': [formatted_last_revenue] + cash_flows_table['Projected Free Cash Flows'].tolist(),
        'Terminal Growth Rate': [f'{terminal_growth_rate}%'] + [''] * num_years,
        'WACC': [f'{discount_rate}%'] + [''] * num_years,
        'Terminal Value': [formatted_terminal_value] + [''] * num_years,
        'Discount Factor (WACC)': [''] + [f'{discount_factor:.2f}' for discount_factor in discount_factors],
        'PV of FCF': [formatted_present_value] + [''] * num_years,
        'PV of Terminal Value': [''] + [''] * num_years,
        'Total PV of Core Operation': [formatted_enterprise_value] + [''] * num_years,
        'Equity Value': [formatted_enterprise_value] + [''] * num_years,
        'Shares Outstanding (millions)': [shares_outstanding] + [''] * num_years,
        'Earnings Per Share outstanding': [formatted_value_per_share] + [''] * num_years
    })

    # Display the results
    st.subheader('Valuation Results')
    st.write(f"Company Name: {company_name}")
    st.write("Projected Free Cash Flows:")

    st.table(valuation_table)

    # Plotting the projected free cash flows
    fig = go.Figure()

    # Add a line plot for the projected free cash flows
    fig.add_trace(go.Scatter(
        x=years,
        y=free_cash_flows[:-1],
        mode='lines+markers',
        name='Projected Free Cash Flows',
        line=dict(color='blue')
    ))

    # Add labels to the data points on the plot
    annotations = [dict(
        x=year,
        y=cash_flow,
        text=locale.format_string('%.0f', cash_flow, grouping=True),
        xanchor='center',
        yanchor='bottom',
        showarrow=False,
        font=dict(color='white')
    ) for year, cash_flow in zip(years, free_cash_flows[:-1])]
    fig.update_layout(annotations=annotations)

    # Set the layout for the plot
    fig.update_layout(
        title='Projected Free Cash Flows',
        xaxis_title='Years',
        yaxis_title='Free Cash Flows (thousand EUR)',
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        hovermode='closest'
    )

    # Display the plot
    st.plotly_chart(fig)


































       



