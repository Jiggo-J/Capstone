pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
from sklearn.ensemble import IsolationForest
import base64
import folium
from branca.colormap import linear
from streamlit_folium import folium_static


st.set_option('deprecation.showPyplotGlobalUse', False)





df = pd.read_excel('/Users/antoniocucala/Desktop/Def2.xls')

# Create a dictionary to map the original column names to their English translations
column_name_mapping = {
    'Nombre': 'Name',
    'Código NIF': 'Tax Identification Number',
    'Número BvD': 'Bureau van Dijk Number',
    'Localidad': 'City',
    'Comunidad autónoma': 'Autonomous Community',
    'Código postal': 'Postal Code',
    'Dirección web': 'Website URL',
    'Provincia': 'Province',
    'País': 'Country',
    'Ultimo número empleados': 'Number of Employees',
    'Capital social\nmil EUR': 'Share Capital (in thousand EUR)',
    'Cotización Bolsa': 'Stock Exchange Listing',
    'Ingresos de explotación\nmil EUR\n2022': 'Operating Revenue (in thousand EUR)',
    'Resultado bruto\nmil EUR\n2022': 'Gross Profit (in thousand EUR)',
    'EBITDA\nmil EUR\n2022': 'EBITDA (in thousand EUR)',
    'Resultado Explotación\nmil EUR\n2022': 'Operating Income (in thousand EUR)',
    'Ingresos financieros\nmil EUR\n2022': 'Financial Income (in thousand EUR)',
    'Gastos financieros\nmil EUR\n2022': 'Financial Expenses (in thousand EUR)',
    'Impuestos sobre sociedades\nmil EUR\n2022': 'Corporate Taxes (in thousand EUR)',
    'Resultado del Ejercicio\nmil EUR\n2022': 'Net Income (in thousand EUR)',
    'Gastos de personal\nmil EUR\n2022': 'Personnel Expenses (in thousand EUR)',
    'Consumo de mercaderías y de materias\nmil EUR\n2022': 'Cost of Goods Sold (in thousand EUR)',
    'Materiales\nmil EUR\n2022': 'Raw Materials (in thousand EUR)',
    'Cash flow\nmil EUR\n2022': 'Cash Flow (in thousand EUR)',
    'EBIT\nmil EUR\n2022': 'EBIT (in thousand EUR)',
    'Total activo\nmil EUR\n2022': 'Total Assets (in thousand EUR)',
    'Activo circulante\nmil EUR\n2022': 'Current Assets (in thousand EUR)',
    'Deudores\nmil EUR\n2022': 'Accounts Receivable (in thousand EUR)',
    'Existencias\nmil EUR\n2022': 'Inventory (in thousand EUR)',
    'Inmovilizado\nmil EUR\n2022': 'Fixed Assets (in thousand EUR)',
    'Inmovilizado inmaterial\nmil EUR\n2022': 'Intangible Fixed Assets (in thousand EUR)',
    'Inmovilizado material\nmil EUR\n2022': 'Tangible Fixed Assets (in thousand EUR)',
    'Otros pasivos fijos\nmil EUR\n2022': 'Other Long-term Liabilities (in thousand EUR)',
    'Total pasivo y capital propio\nmil EUR\n2022': 'Total Liabilities and Equity (in thousand EUR)',
    'Fondo de maniobra\nmil EUR\n2022': 'Working Capital (in thousand EUR)',
    'Número empleados\n2022': 'Number of Employees',
    'Deudas financieras\nmil EUR\n2022': 'Financial Debt (in thousand EUR)',
    'Pasivo fijo\nmil EUR\n2022': 'Long-term Liabilities (in thousand EUR)',
    'Pasivo líquido\nmil EUR\n2022': 'Short-term Liabilities (in thousand EUR)',
    'Rentabilidad sobre recursos propios (%)\n%\n2022': 'Return on Equity (%)',
    'Rentabilidad sobre el activo total (%)\n%\n2022': 'Return on Total Assets (%)',
    'Margen de beneficio (%)\n%\n2022': 'Profit Margin (%)',
    'Ratio de solvencia\n%\n2022': 'Solvency Ratio (%)',
    'Ratio de liquidez\n%\n2022': 'Liquidity Ratio (%)',
    'Apalancamiento (%)\n%\n2022': 'Leverage Ratio (%)',
    'Beneficio por empleado\nmil\n2022': 'Profit per Employee (in thousand)',
    'Coste medio de los empleados\nmil\n2022': 'Average Employee Cost (in thousand)',
    'Total activos por empleado\nmil\n2022': 'Total Assets per Employee (in thousand)',
    'Tesorería\n%\n2022': 'Cash and Cash Equivalents (%)',
    'Fondo maniobra\n%\n2022': 'Working Capital (%)',
    'Total activo\n%\n2022': 'Total Assets (%)',
    'Fondos propios\n%\n2022': 'Shareholders Equity (%)',
    'Acreedores a largo plazo\n%\n2022': 'Long-term Creditors (%)',
    'Resultados antes de impuestos\n%\n2022': 'Earnings Before Taxes (%)',
    'Gastos de personal (%) 2022': 'Personnel Expenses (%)',
    'Coordenada - Y' : 'Coordinate Y', 'Coordenada - X' : 'Coordinate X'}


# Rename columns using the dictionary
df.rename(columns=column_name_mapping, inplace=True)


df = df.loc[:,~df.columns.duplicated()]

def format_number(value):
            if isinstance(value, str):
                try:
                    value = float(value.replace(",", ""))
                except ValueError:
                    return value
            return "{:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")

        
df = df.replace('n.d.', 0)
        
        
# Load your dataset here

# Define app layout
st.title('M&A App')

# Add sidebar for navigation
menu = ['Home', 'Information Overview', 'Company Financial Efficiency Ratios','Market Analysis', 'Machine Learning Insights', 'Valuation Calculator']
choice = st.sidebar.selectbox('Select an option', menu)


if choice == 'Home':
    st.title("Home")
    st.write("""
    The M&A Financial App is a tool for analyzing investment opportunities in various sectors, industries, and locations. It uses unsupervised machine learning algorithms to cluster companies based on their financial metrics and ratios, allowing users to quickly identify potential targets for M&A activity.
    """)
    st.write("""
    Key features of the app include:
    - Access to a large database of companies with financial data
    - Calculation of financial ratios and metrics for each company
    - Clustering of companies based on their financial metrics and ratios
    - News and insights related to companies in the database
    """)
    st.write("""
    Use the navigation menu on the left to explore the different sections of the app, including:
    - Information Overview: Get a high-level overview of the companies in the database
    - Company Financial Efficiency Ratios: Analyze the financial ratios and efficiency of individual companies
    - Market Analysis: Explore trends and insights related to the market and industry
    - M&A Insights: Stay up-to-date on mergers, acquisitions, and divestitures in the industry
    - Machine Learning Insights: View insights and predictions generated by our machine learning models
    """)
    

    
    
    # Add call to action section
    st.subheader("Get Started")
    st.write("Ready to start exploring investment opportunities? Use the navigation menu on the left to get started!")
    
  



elif choice == 'Information Overview':
        st.title("Information Overview")

    # Load data
        

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

        st.write(f"**Selected Company:** {selected_company}")

        # Display company information
        st.subheader(f"Selected Company: {selected_company}")
        st.write(company_data)

        # Display key financial ratios and insights for the selected company
      
        st.subheader("Key Financial Insights")

        col1, col2 = st.columns(2)

        # Display operating revenue and gross profit
        with col1:
            st.write(f"**Operating Revenue (in thousand EUR):** {format_number(company_data['Operating Revenue (in thousand EUR)'].values[0])}")
        with col2:
            st.write(f"**Gross Profit (in thousand EUR):** {format_number(company_data['Gross Profit (in thousand EUR)'].values[0])}")

        # Display EBITDA and net income
        with col1:
            st.write(f"**EBITDA (in thousand EUR):** {format_number(company_data['EBITDA (in thousand EUR)'].values[0])}")
        with col2:
            st.write(f"**Net Income (in thousand EUR):** {format_number(company_data['Net Income (in thousand EUR)'].values[0])}")

        # Display return on equity and return on total assets
        with col1:
            st.write(f"**Return on Equity (%):** {format_number(company_data['Return on Equity (%)'].values[0])}")
        with col2:
            st.write(f"**Return on Total Assets (%):** {format_number(company_data['Return on Total Assets (%)'].values[0])}")

        # Display profit margin and solvency ratio
        with col1:
            st.write(f"**Profit Margin (%):** {format_number(company_data['Profit Margin (%)'].values[0])}")
        with col2:
            st.write(f"**Solvency Ratio (%):** {format_number(company_data['Solvency Ratio (%)'].values[0])}")

        # Display liquidity ratio and leverage ratio
        with col1:
            st.write(f"**Liquidity Ratio (%):** {format_number(company_data['Liquidity Ratio (%)'].values[0])}")
        with col2:
            st.write(f"**Leverage Ratio (%):** {format_number(company_data['Leverage Ratio (%)'].values[0])}")
            
            
        st.write('\n')
        st.write('\n')


            
        # Create a checkbox to display column information

        if st.checkbox('Show Column Information (What columns are being used)'):
            st.subheader('Column Information')
            # Define the column groups
            company_info_cols = ['Name', 'Bureau van Dijk Number','Tax Identification Number', 'City', 'Autonomous Community', 'Postal Code', 'Website URL', 'Province', 'Country', 'Coordinate Y','Coordinate X']
            financial_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)','Cash Flow', 'Cost of Goods Sold (in thousand EUR)','Stock Exchange Listing']
            asset_cols = ['Total Assets (in thousand EUR)', 'Current Assets (in thousand EUR)','Raw Materials', 'Accounts Receivable (in thousand EUR)', 'Inventory (in thousand EUR)', 'Fixed Assets (in thousand EUR)', 'Intangible Fixed Assets (in thousand EUR)', 'Tangible Fixed Assets (in thousand EUR)', 'Other Long-term Liabilities (in thousand EUR)']
            liability_cols = ['Total Liabilities and Equity (in thousand EUR)', 'Financial Debt (in thousand EUR)', 'Long-term Liabilities (in thousand EUR)', 'Short-term Liabilities (in thousand EUR)','Total Liabilities and Equity (in thousand EUR) for financial statements ']
            ratio_cols = ['Return on Equity (%)', 'Return on Total Assets (%)', 'Profit Margin (%)', 'Solvency Ratio (%)', 'Liquidity Ratio (%)', 'Leverage Ratio (%)', 'Profit per Employee (in thousand)', 'Average Employee Cost (in thousand)', 'Total Assets per Employee (in thousand)', 'Cash and Cash Equivalents (%)', 'Working Capital (%)', 'Total Assets (%)', 'Shareholders Equity (%)', 'Long-term Creditors (%)', 'Earnings Before Taxes (%)', 'Personnel Expenses (%)']
            # Display the column groups and their respective columns
            st.write('**Company Info:**')
            st.write(company_info_cols)
            st.write('**Financial Metrics:**')
            st.write(financial_cols)
            st.write('**Asset Metrics:**')
            st.write(asset_cols)
            st.write('**Liability Metrics:**')
            st.write(liability_cols)
            st.write('**Ratio Metrics:**')
            st.write(ratio_cols)







# Company Financial Efficiency Ratios
elif choice == 'Company Financial Efficiency Ratios':
    st.title("Company Financial Efficiency Ratios")

    # Sidebar for selecting a country
    country_names = df['Country'].unique()
    selected_country = st.sidebar.selectbox("Select a Country:", country_names)

    # Filter dataframe for the selected country
    country_data = df[df['Country'] == selected_country]

    # Sidebar for selecting a company
    company_names = country_data['Name'].unique()
    selected_company = st.sidebar.selectbox("Select a Company:", company_names)

    # Filter dataframe for the selected company
    company_data = country_data[country_data['Name'] == selected_company]

    st.write(f"**Selected Company:** {selected_company}")

    # Gross Margin
    
    menu = ['Individual Information', 'Global Information']
    choice = st.sidebar.selectbox("Select a Section:", menu)
    
    if choice == 'Individual Information':

        st.markdown('---')
        st.markdown('## Individual Information')
        st.write('Here are some key financial ratios that can help you gain insights into the company’s financial performance.')

        # Define format_number function with one argument
        def format_number(num):
            return format(num, ".2f")

        # Gross Margin
        st.markdown('---')
        st.markdown('### Gross Margin')
        try:
            if 'Gross Profit (in thousand EUR)' not in company_data.columns:
                raise KeyError("Gross Profit (in thousand EUR) column is missing")
            if 'Operating Revenue (in thousand EUR)' not in company_data.columns:
                raise KeyError("Operating Revenue (in thousand EUR) column is missing")

            # Replace 'n.d.' values with NaN
            company_data = company_data.replace('n.d.', np.nan)

            gross_profit = company_data['Gross Profit (in thousand EUR)'].astype(float).mean()
            operating_revenue = company_data['Operating Revenue (in thousand EUR)'].astype(float).mean()

            if np.isnan(gross_profit) or np.isnan(operating_revenue):
                raise ValueError("Data is missing or in the wrong format")

            gross_margin = 100 * gross_profit / operating_revenue
            st.write(f"Gross Margin: {format_number(gross_margin)}%")
            if st.checkbox("Extra Information", key="gross_margin"):
                st.write("Gross margin measures the percentage of each euro of revenue that remains after the cost of goods sold has been deducted. A higher gross margin indicates that a company is generating more profit from each euro of revenue, while a lower gross margin could indicate pricing pressures or higher costs.")
        except (KeyError, ValueError) as e:
            st.warning(f"Cannot calculate Gross Margin: {str(e)}")

        # Operating Margin
        st.markdown('---')
        st.markdown('### Operating Margin')
        try:
            operating_income = float(company_data['Operating Income (in thousand EUR)'].values[0])
            operating_revenue = float(company_data['Operating Revenue (in thousand EUR)'].values[0])
            operating_margin = 100 * operating_income / operating_revenue
            st.write(f"Operating Margin: {format_number(operating_margin)}%")
            if st.checkbox("Extra Information", key="Operating_margin"):
                st.write("Operating margin is a profitability ratio that measures how much profit a company makes on each dollar of revenue after accounting for all of its operating expenses. A high operating margin is generally seen as a positive sign, as it indicates that the company is able to effectively manage its costs.")
        except ValueError:
            st.warning("Cannot calculate Operating Margin as data is missing or in the wrong format.")

        # Return on Assets
        st.markdown('---')
        st.markdown('### Return on Assets (ROA)')
        try:
            net_income = float(company_data['Net Income (in thousand EUR)'].values[0])
            total_assets = float(company_data['Total Assets (in thousand EUR)'].values[0])
            roa = 100 * net_income / total_assets
            st.write(f"Return on Assets (ROA): {format_number(roa)}%")
            if st.checkbox("Extra Information", key="ROA"):
                st.write("ROA measures how efficiently a company is using its assets to generate profit. A higher ROA is generally seen as better, as it indicates that the company is using its assets more efficiently to generate profits.")
        except ValueError:
            st.warning("Cannot calculate Return on Assets (ROA) as data is missing or in the wrong format.")

        # Net Profit Margin
        st.markdown('---')
        st.markdown('### Net Profit Margin')
        try:
            net_income = float(company_data['Net Income (in thousand EUR)'].values[0])
            operating_revenue = float(company_data['Operating Revenue (in thousand EUR)'].values[0])
            net_profit_margin = 100 * net_income / operating_revenue
            st.write(f"Net Profit Margin: {format_number(net_profit_margin)}%")
            if st.checkbox("Extra Information", key="Net_Profit_Margin"):
                st.write("Net profit margin measures how much profit a company makes on each dollar of revenue after accounting for all of its expenses, including taxes and interest. A higher net profit margin is generally seen as a positive sign, as it indicates that the company is able to effectively manage its costs and generate profits.")
        except ValueError:
            st.warning("Cannot calculate Net Profit Margin as data is missing or in the wrong format.")

        # Current Ratio
        st.markdown('---')
        st.markdown('### Current Ratio')
        try:
            current_assets = float(company_data['Current Assets (in thousand EUR)'].values[0])
            current_liabilities = float(company_data['Short-term Liabilities (in thousand EUR)'].values[0])
            current_ratio = current_assets / current_liabilities
            st.write(f"Current Ratio: {format_number(current_ratio)}")
            if st.checkbox("Extra Information", key="Current_Ratio"):
                st.write("Current ratio is a liquidity ratio that measures a company's ability to pay its short-term debts with its current assets. A ratio above 1 indicates that the company has enough current assets to cover its current liabilities, while a ratio below 1 indicates that the company may have difficulty paying its short-term debts.")
        except ValueError:
            st.warning("Cannot calculate Current Ratio as data is missing or in the wrong format.")

        # Quick Ratio
        st.markdown('---')
        st.subheader("Quick Ratio")
        try:
            current_assets = float(company_data['Current Assets (in thousand EUR)'].values[0])
            inventory = float(company_data['Inventory (in thousand EUR)'].values[0])
            current_liabilities = float(company_data['Short-term Liabilities (in thousand EUR)'].values[0])
            quick_ratio = (current_assets - inventory) / current_liabilities

            # Update function call to pass one argument
            st.write(f"Quick Ratio: {format_number(quick_ratio)}")
            if st.checkbox("Extra Information", key="Quick_Ratio"):
                st.write("The quick ratio, also known as the acid-test ratio, is a liquidity ratio that measures a company's ability to pay its short-term debts with its most liquid assets. This ratio is more stringent than the current ratio, as it excludes inventory from current assets. A ratio above 1 indicates that the company has enough liquid assets to cover its short-term debts, while a ratio below 1 indicates that the company may have difficulty paying its short-term debts.")

        except ValueError:
            st.warning("Cannot calculate Quick Ratio as data is missing or in the wrong format.")

        # Define format_number function with one argument
        def format_number(num):
            return format(num, ".2f")
        
        
        st.write('\n' * 3)


        # Filter the data to only include the selected company
        company_df = company_data[company_data["Name"] == selected_company]

        # Create a balance sheet
        balance_sheet_cols = ["Total Assets (in thousand EUR)", "Current Assets (in thousand EUR)", "Accounts Receivable (in thousand EUR)", 
                              "Inventory (in thousand EUR)", "Fixed Assets (in thousand EUR)", "Intangible Fixed Assets (in thousand EUR)", 
                              "Tangible Fixed Assets (in thousand EUR)", "Other Long-term Liabilities (in thousand EUR)", "Total Liabilities and Equity (in thousand EUR)", 
                              "Working Capital (in thousand EUR)", "Financial Debt (in thousand EUR)", "Long-term Liabilities (in thousand EUR)", 
                              "Short-term Liabilities (in thousand EUR)", "Shareholders Equity (%)"]
        balance_sheet_data = company_df[balance_sheet_cols].transpose()
        balance_sheet_data.columns = [selected_company]
        st.subheader("Balance Sheet")
        st.dataframe(balance_sheet_data)

        # Create a profit and loss statement
        p_and_l_cols = ["Operating Revenue (in thousand EUR)", "Cost of Goods Sold (in thousand EUR)", "Gross Profit (in thousand EUR)", 
                        "Personnel Expenses (in thousand EUR)", "EBIT (in thousand EUR)", "EBITDA (in thousand EUR)", "Operating Income (in thousand EUR)", 
                        "Financial Income (in thousand EUR)", "Financial Expenses (in thousand EUR)", "Corporate Taxes (in thousand EUR)", 
                        "Net Income (in thousand EUR)", "Profit Margin (%)"]
        p_and_l_data = company_df[p_and_l_cols].transpose()
        p_and_l_data.columns = [selected_company]
        st.subheader("Profit and Loss Statement")
        st.dataframe(p_and_l_data)

        import pandas as pd

      # create a dataframe with financial information
 
       # create a dataframe with financial information
        financial_info = pd.concat([balance_sheet_data, p_and_l_data], axis=1)

        # add company name as a column
        financial_info["Company"] = selected_company

        # add index as a column for the variable names
        financial_info.reset_index(inplace=True)

        # rename columns
        financial_info.rename(columns={"index": "Variable Name", selected_company: "Value"}, inplace=True)

        # download button
        if st.button("Download financial information"):
            csv = financial_info.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings
            link = f'<a href="data:file/csv;base64,{b64}" download="{selected_company}_financial_info.csv">Download financial information</a>'
            st.markdown(link, unsafe_allow_html=True)


    if choice == 'Global Information':
        st.header("Global Information")
      

        # Create a list of all available ratios
        ratios = [
            "Gross Margin",
            "Operating Margin",
            "Return on Assets (ROA)",
            "Net Profit Margin",
            "Current Ratio",
            "Quick Ratio"
        ]

        # Create a multiselect dropdown to select which ratios to plot on the X and Y axis
        x_ratio, y_ratio = st.columns(2)
        with x_ratio:
            x_axis_ratio = st.selectbox("Select a ratio for the X axis", ratios)
        with y_ratio:
            y_axis_ratio = st.selectbox("Select a ratio for the Y axis", ratios)

        # Create a multiselect dropdown to select which companies to plot
        selected_companies = st.multiselect("Select companies to plot", df["Name"].unique())

        # Filter the dataframe to only include selected companies
        df_selected = df[df["Name"].isin(selected_companies)]

        # Calculate selected ratios for each company
        df_selected["Gross Margin"] = 100 * df_selected["Gross Profit (in thousand EUR)"].astype(float) / df_selected["Operating Revenue (in thousand EUR)"].astype(float)
        df_selected["Operating Margin"] = 100 * df_selected["Operating Income (in thousand EUR)"].astype(float) / df_selected["Operating Revenue (in thousand EUR)"].astype(float)
        df_selected["Return on Assets (ROA)"] = 100 * df_selected["Net Income (in thousand EUR)"].astype(float) / df_selected["Total Assets (in thousand EUR)"].astype(float)
        df_selected["Net Profit Margin"] = 100 * df_selected["Net Income (in thousand EUR)"].astype(float) / df_selected["Operating Revenue (in thousand EUR)"].astype(float)
        df_selected["Current Ratio"] = df_selected["Current Assets (in thousand EUR)"].astype(float) / df_selected["Short-term Liabilities (in thousand EUR)"].astype(float)
        df_selected["Quick Ratio"] = (df_selected["Current Assets (in thousand EUR)"].astype(float) - df_selected["Inventory (in thousand EUR)"].astype(float)) / df_selected["Short-term Liabilities (in thousand EUR)"].astype(float)

        # Create the scatter plot
        fig = px.scatter(
            df_selected,
            x=x_axis_ratio,
            y=y_axis_ratio,
            color="Name",
            hover_data=["Name"]
        )

        # Set axis labels
        fig.update_xaxes(title=x_axis_ratio)
        fig.update_yaxes(title=y_axis_ratio)

        # Show the plot
        st.plotly_chart(fig)
        
                 # Select numerical columns for correlation matrix
        numerical_cols = [    'Operating Revenue (in thousand EUR)',    'Gross Profit (in thousand EUR)',    'EBITDA (in thousand EUR)',    'Operating Income (in thousand EUR)',    'Net Income (in thousand EUR)',    'Cost of Goods Sold (in thousand EUR)',    'Total Assets (in thousand EUR)',    'Current Assets (in thousand EUR)',    'Accounts Receivable (in thousand EUR)',    'Inventory (in thousand EUR)',    'Fixed Assets (in thousand EUR)',    'Intangible Fixed Assets (in thousand EUR)',    'Tangible Fixed Assets (in thousand EUR)',    'Other Long-term Liabilities (in thousand EUR)',    'Total Liabilities and Equity (in thousand EUR)',    'Working Capital (in thousand EUR)',    'Financial Debt (in thousand EUR)',    'Long-term Liabilities (in thousand EUR)',    'Short-term Liabilities (in thousand EUR)',    'Return on Equity (%)',    'Return on Total Assets (%)',    'Profit Margin (%)',    'Solvency Ratio (%)',    'Liquidity Ratio (%)',    'Leverage Ratio (%)',    'Profit per Employee (in thousand)',    'Average Employee Cost (in thousand)',    'Total Assets per Employee (in thousand)',    'Cash and Cash Equivalents (%)',    'Working Capital (%)',    'Total Assets (%)',    'Shareholders Equity (%)',    'Long-term Creditors (%)',    'Earnings Before Taxes (%)',    'Personnel Expenses (%)']

        # Create a dropdown to select columns to display
        selected_cols = st.multiselect('Select columns to display', numerical_cols)

        # Select only numerical columns
        numerical_df = df[selected_cols]

        # Calculate correlation matrix
        corr_matrix = numerical_df.corr()

        # Create heatmap using plotly
        fig = px.imshow(corr_matrix)

        # Add annotations to heatmap
        for i in range(len(selected_cols)):
            for j in range(len(selected_cols)):
                fig.add_annotation(x=i, y=j, 
                                   text=str(round(corr_matrix.iloc[i, j], 2)), 
                                   showarrow=False, 
                                   font=dict(color='white', size=12),
                                   xref='x', yref='y')

        fig.update_xaxes(side="top")
        fig.update_layout(
            title={
                'text': "",
                'y':0.2,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        st.plotly_chart(fig)

        
        st.write(
    "<div style='text-align: center;'>"
    "<h3>Correlation Matrix of Financial Metrics</h3>"
    "</div>", unsafe_allow_html=True
)

           
                # Select only numeric columns
        df_numeric = df.select_dtypes(include=[np.number])

        # Filter for selecting column for marker size
        size_column = st.selectbox("Select Column for Marker Size", df_numeric.columns)

        # Create color map for marker size
        color_scale = linear.YlOrRd_04.scale(df_numeric[size_column].min(), df_numeric[size_column].max())


       # Filter for selecting column for marker size
        value_columns = [col for col in df.columns if df[col].dtype in [float, int] and col != "Coordenada - X" and col != "Coordenada - Y"]
        size_column = st.selectbox("Select Column for Marker Size.", value_columns)

        # Create color map for marker size
        color_scale = linear.YlOrRd_04.scale(df[size_column].min(), df[size_column].max())

        # Create map centered on Spain
        map_center = [40.4168, -3.7038]
        m = folium.Map(location=map_center, zoom_start=6)

        # Restrict map to show only Spain
        spain_bounds = [[35.0, -10.0], [44.0, 5.0]]
        m.fit_bounds(spain_bounds)
        
        # Define new radius_scale function to increase marker size
        radius_scale = lambda x: 1 + 5 * np.log10(x)

        # Add markers for each company using new radius_scale function
        for index, row in df.iterrows():
            popup_text = f"<strong>{row['Name']}</strong><br>{size_column}: {row[size_column]}"
            folium.CircleMarker(location=[row['Coordinate X'], row['Coordinate Y']],
                                radius=radius_scale(row[size_column]),
                                color=color_scale(row[size_column]),
                                fill=True,
                                fill_opacity=0.7,
                                popup=popup_text).add_to(m)


        # Add color map legend
        color_scale.caption = size_column
        color_scale.add_to(m)

        # Display map
        folium_static(m)




# Market Analysis
elif choice == 'Market Analysis':
    st.title("Market Analysis")

    # Sidebar for selecting a country
    country_names = df['Country'].unique()
    selected_country = st.sidebar.selectbox("Select a Country:", country_names)

    # Filter dataframe for the selected country
    country_data = df[df['Country'] == selected_country]

    # Sidebar for selecting a company
    company_names = country_data['Name'].unique()
    selected_company = st.sidebar.selectbox("Select a Company:", company_names)

    # Filter dataframe for the selected company
    company_data = country_data[country_data['Name'] == selected_company]

    st.write(f"**Selected Company:** {selected_company}")

    # Market Size
    st.subheader("Market Size")
    try:
        if 'Operating Revenue (in thousand EUR)' not in company_data.columns:
            raise KeyError("Operating Revenue (in thousand EUR) column is missing")

        # Replace 'n.d.' values with NaN
        company_data = company_data.replace('n.d.', np.nan)

        # Calculate total operating revenue for the country
        country_revenue = country_data['Operating Revenue (in thousand EUR)'].astype(float).sum()

        # Calculate market share for the selected company
        company_revenue = company_data['Operating Revenue (in thousand EUR)'].astype(float).sum()
        market_share = 100 * company_revenue / country_revenue

        market_size = company_revenue / market_share
        st.write(f"Market Size: {f'{market_size:,.2f}'} million EUR")
    except (KeyError, ValueError) as e:
        st.warning(f"Cannot calculate Market Size: {str(e)}")

    # Growth Potential
    st.subheader("Growth Potential")
    try:
        if 'Operating Revenue (in thousand EUR)' not in company_data.columns:
            raise KeyError("Operating Revenue (in thousand EUR) column is missing")

        # Replace 'n.d.' values with NaN
        company_data = company_data.replace('n.d.', np.nan)

        # Calculate revenue growth rate for the last 3 years
        revenue_data = company_data[['Operating Revenue (in thousand EUR)', 'Country']].sort_values(by='Country')
        revenue_data['Operating Revenue (in thousand EUR)'] = revenue_data['Operating Revenue (in thousand EUR)'].astype(float)
        revenue_data = revenue_data.groupby('Country').apply(lambda x: (x['Operating Revenue (in thousand EUR)'].iloc[-1] / x['Operating Revenue (in thousand EUR)'].iloc[0])**(1/3) - 1)
        revenue_growth_rate = revenue_data.mean() * 100

        st.write(f"Revenue Growth Rate (3-year average): {format(revenue_growth_rate, '.2f')}%")

    except (KeyError, ValueError) as e:
        st.warning(f"Cannot calculate Growth Potential: {str(e)}")

        # Competitive Landscape
    # Competitive Landscape
    try:
        st.subheader("Competitive Landscape")

        if 'Operating Revenue (in thousand EUR)' not in df.columns:
            raise KeyError("Operating Revenue (in thousand EUR) column is missing")

        # Replace 'n.d.' values with NaN
        df = df.replace('n.d.', np.nan)

        # Filter dataframe for the selected country
        country_data = df[df['Country'] == selected_country]

        # Calculate total operating revenue for the country
        country_revenue = country_data['Operating Revenue (in thousand EUR)'].sum()

        # Calculate market share for all companies in the country
        total_revenue = country_data['Operating Revenue (in thousand EUR)'].sum()
        country_data['Market Share'] = country_data['Operating Revenue (in thousand EUR)'] / total_revenue

        # Display top 10 companies by market share
        top_10_companies = country_data.sort_values('Market Share', ascending=False).head(10)
        st.subheader("Top 10 Companies by Market Share")
        st.dataframe(top_10_companies[['Name', 'Market Share']].reset_index(drop=True))

        # Calculate market concentration
        market_concentration = 100 * top_10_companies['Market Share'].sum()
        st.write(f"Market Concentration: {format(market_concentration, '.2f')}%")

    except (KeyError, ValueError) as e:
        st.warning(f"Cannot calculate Competitive Landscape: {str(e)}")




                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
                                                          
        
elif choice == "Machine Learning Insights":
    st.title("Machine Learning Insights")
    st.write("Select a machine learning algorithm to explore insights:")
    ml_algorithm = st.selectbox("", ["Clustering Analysis",'Random Forest Classifier', 'PCA', 'Support Vector Machine (SVM)', 'Isolation Forest - Anomaly Detection'])

    if ml_algorithm == "Clustering Analysis":
        st.title("Clustering Analysis")
        st.write("Use unsupervised machine learning algorithms such as K-Means or DBSCAN to group companies based on their financial metrics and ratios. This can help you identify clusters of companies that share similar financial characteristics and may be good M&A targets.")

        # Select the columns to use for clustering
        cluster_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Net Income (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Normalize the data
        scaler = StandardScaler()
        X = df[cluster_cols].values
        X = scaler.fit_transform(X)

        # Set the number of clusters
        n_clusters = 5

        # Fit the K-Means model
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(X)

        # Add the cluster labels to the DataFrame
        df['Cluster'] = kmeans.labels_

        # Display the number of companies in each cluster
        cluster_counts = df['Cluster'].value_counts()
        st.write(f"There are {len(cluster_counts)} clusters:")
        for i, count in cluster_counts.iteritems():
            st.write(f"- Cluster {i}: {count} companies")

        # Display a scatter plot of the clusters
        fig = px.scatter(df, x='Operating Revenue (in thousand EUR)', y='Net Income (in thousand EUR)', color='Cluster', hover_data=['Name'])
        st.plotly_chart(fig)

    elif ml_algorithm == "Random Forest Classifier":
        st.title("Random Forest Classifier")
        st.write("Use a supervised machine learning algorithm such as Random Forest to classify companies as good or bad M&A targets based on their financial metrics and ratios.")

        # Create a new column called 'M&A Target' and set the values based on net income
        df['M&A Target'] = np.where(df['Net Income (in thousand EUR)'] > 0, 'Good', 'Bad')

        # Set the columns to use for classification
        classifier_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Define the input and output variables
        X = df[classifier_cols].values
        y = df['M&A Target'].values

        # Create a Random Forest Classifier with 100 trees
        rfc = RandomForestClassifier(n_estimators=100, random_state=0)

        # Fit the classifier to the data
        rfc.fit(X, y)

        # Get the feature importances
        importances = rfc.feature_importances_

        # Create a DataFrame with the feature names and their importances
        feature_importances = pd.DataFrame({'feature': classifier_cols, 'importance': importances})

        # Sort the DataFrame by the importance in descending order
        feature_importances = feature_importances.sort_values('importance', ascending=False)

        # Display the feature importances
        st.write("Feature Importances:")
        st.write(feature_importances)

        # Create a dropdown menu to select a company
        selected_company = st.selectbox("Select a company:", df['Name'])

        # Get the financial metrics for the selected company
        company_metrics = df[df['Name'] == selected_company][classifier_cols].values

        # Predict the M&A target for the selected company
        target = rfc.predict(company_metrics)[0]

        # Display whether the selected company is a good or bad M&A target
        st.write(f"{selected_company} is a {target} M&A target.")

        # Add an "Explanation" dropdown
        if st.checkbox("Explanation"):
            st.write("The Random Forest Classifier predicts whether a company is a good or bad M&A target based on its financial metrics and ratios. The classifier was trained on a dataset of companies that were labeled as either 'Good' or 'Bad' M&A targets based on whether they had positive or negative net income. The classifier uses the input financial metrics and ratios to make a prediction on whether a given company is a 'Good' or 'Bad' M&A target, based on how similar its financials are to the companies in the training set.")

        # Calculate the precision, recall, and F1-score
        y_pred = rfc.predict(X)
        report = classification_report(y, y_pred, output_dict=True)
        df_report = pd.DataFrame(report).transpose()
        st.write("Classification Report:")
        st.write(df_report)
        
        
    elif ml_algorithm == "PCA":
        st.title("Principal Component Analysis (PCA)")
        st.write("Use PCA to identify patterns and relationships in high-dimensional data and reduce the number of variables in your dataset.")

        # Set the columns to use for PCA
        pca_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Define the input variables
        X = df[pca_cols].values

        # Perform PCA on the input data
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(X)

        # Create a DataFrame with the principal components
        principal_df = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2'])

        # Concatenate the principal components with the company names
        final_df = pd.concat([principal_df, df[['Name']]], axis = 1)

        # Plot the principal components
        fig = px.scatter(final_df, x='principal component 1', y='principal component 2', hover_name='Name')
        st.plotly_chart(fig)
        
        # Add an "Explanation" dropdown
        if st.checkbox("Explanation"):
            st.write("Principal Component Analysis (PCA) is a dimensionality reduction technique that can be used to identify patterns and relationships in high-dimensional data. It works by finding new dimensions, called principal components, that capture as much of the variability in the data as possible. The first principal component captures the most variability in the data, the second principal component captures the second most variability, and so on. By reducing the number of dimensions, PCA can help simplify your analysis and improve the accuracy of your predictions, while still capturing as much of the variability in the data as possible.")
            
            
            
            
    elif ml_algorithm == "Support Vector Machine (SVM)":
        st.title("Support Vector Machine (SVM)")
        st.write("Use a supervised machine learning algorithm such as SVM to classify companies as good or bad M&A targets based on their financial metrics and ratios.")

        # Create a new column called 'M&A Target' and set the values based on net income
        df['M&A Target'] = np.where(df['Net Income (in thousand EUR)'] > 0, 'Good', 'Bad')

        from sklearn.model_selection import train_test_split

        # Set the columns to use for classification
        classifier_cols = ['Operating Revenue (in thousand EUR)', 'Gross Profit (in thousand EUR)', 'EBITDA (in thousand EUR)', 'Operating Income (in thousand EUR)', 'Financial Income (in thousand EUR)', 'Financial Expenses (in thousand EUR)', 'Corporate Taxes (in thousand EUR)', 'Personnel Expenses (in thousand EUR)', 'Cost of Goods Sold (in thousand EUR)']

        # Define the input and output variables
        X = df[classifier_cols].values
        y = df['M&A Target'].values

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Encode the labels
        le = LabelEncoder()
        y_train_encoded = le.fit_transform(y_train)

        # Fit the PCA to the training data
        pca = PCA(n_components=2)
        X_train_reduced = pca.fit_transform(X_train)

        # Create a Support Vector Machine with a linear kernel
        svm = SVC(kernel='linear', C=1, random_state=0)

        # Fit the SVM to the training data
        svm.fit(X_train_reduced, y_train_encoded)

        # Create a dropdown menu to select a company
        selected_company = st.selectbox("Select a company:", df['Name'])

        # Get the financial metrics for the selected company
        company_metrics = df[df['Name'] == selected_company][classifier_cols].values

        # Predict the M&A target for the selected company
        target = svm.predict(pca.transform(company_metrics))[0]
        target = le.inverse_transform([target])[0]

        # Display whether the selected company is a good or bad M&A target
        st.write(f"{selected_company} is a {target} M&A target.")

        # Generate a meshgrid of points for plotting the decision boundary
        h = 0.0001  # step size in the mesh
        x_min, x_max = X_train_reduced[:, 0].min() - 1, X_train_reduced[:, 0].max() + 1
        y_min, y_max = X_train_reduced[:, 1].min() - 1, X_train_reduced[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        X_mesh = np.c_[xx.ravel(), yy.ravel()]

        # Predict the M&A targets for the meshgrid points
        Z = svm.predict(X_mesh)

        # Reshape the predicted targets into a meshgrid
        Z = Z.reshape(xx.shape)

        # Plot the decision boundary and the data points
        fig, ax = plt.subplots()
        scatter = ax.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y_encoded, cmap='bwr')
        ax.contour(xx, yy, Z, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
        ax.set_xlabel('Principal Component 1')
        ax.set_ylabel('Principal Component 2')
        ax.set_title('Support Vector Machine')
        st.write(fig)



    elif ml_algorithm == "Isolation Forest - Anomaly Detection":
        st.title("Isolation Forest - Anomaly Detection")

        # Select the numerical columns for analysis
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        selected_columns = st.multiselect("Select the numerical columns to analyze:", numerical_cols)
        if not selected_columns:
            st.warning("Please select at least one column for analysis.")
            st.stop()

        # Filter the data to only include selected columns
        filtered_data = df[selected_columns]

        # Replace 'n.d.' values with NaN
        filtered_data = filtered_data.replace('n.d.', np.nan)

        # Remove rows with missing data
        filtered_data = filtered_data.dropna()

        # Create isolation forest model and fit to data
        iso_forest = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
        iso_forest.fit(filtered_data)

        # Predict outliers using isolation forest model
        outlier_preds = iso_forest.predict(filtered_data)

        # Create dataframe of outliers
        outliers = filtered_data[outlier_preds == -1]

        # Merge outliers with company_data to show company name
        company_names = df['Name']
        outlier_names = company_names[outlier_preds == -1]
        outliers = pd.concat([outliers, outlier_names], axis=1)

        # Display number of outliers found
        st.write(f"Number of outliers found: {len(outliers)}")

        # Display table of outlier data
        st.write(outliers)
        
        if st.button("Extra Information"):
            st.write("Isolation Forest is an unsupervised learning algorithm used for anomaly detection. It works by isolating observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature. The number of splits required to isolate the observation is counted, and the anomaly score is given by the average of the number of splits over all trees. The algorithm is efficient and can work well even in high-dimensional spaces.")


if choice == "Valuation Calculator":
    st.title("Valuation Calculator")
    
    
    menu = ["Discounted Cash Flow (DCF)" , "Price-to-Earnings (P/E) Ratio"]
    valuation_choice = st.sidebar.selectbox("Select Valuation Method:", menu)
    
    # Filter for selecting a company
    selected_company = st.selectbox("Select a Company", df["Name"].unique())

    # Get the selected company's data
    company_data = df.loc[df["Name"] == selected_company].iloc[0]

    # Display company information
    st.subheader(f"Selected Company: {selected_company}")
    st.write(company_data)

    #valuation_choice = st.selectbox("Select Valuation Method", ["Discounted Cash Flow (DCF)", "Price-to-Earnings (P/E) Ratio"])
    
    
    if valuation_choice == "Discounted Cash Flow (DCF)":
        # Inputs for the DCF Valuation Calculator
        free_cash_flow = st.number_input("Free Cash Flow (in thousand EUR)", min_value=0, step=1)
        growth_rate = st.number_input("Growth Rate (%)", min_value=0.0, step=0.1)
        discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, step=0.1)
        number_of_years = st.number_input("Number of Years", min_value=1, step=1)

        # Calculate the DCF valuation
        if st.button("Calculate DCF Valuation"):
            valuation = 0
            for i in range(1, number_of_years + 1):
                valuation += free_cash_flow * (1 + growth_rate / 100)**i / (1 + discount_rate / 100)**i

            st.write(f"DCF Valuation: {valuation:,.2f} thousand EUR")
            
        if st.checkbox("Explanation"):
            st.write("Discounted Cash Flow (DCF) is a valuation method used to estimate the value of an investment based on its expected future cash flows. DCF takes into account the time value of money by discounting projected cash flows back to their present value using a discount rate. This method is commonly used in corporate finance and investment analysis to determine the intrinsic value of a company or asset.")

    elif valuation_choice == "Price-to-Earnings (P/E) Ratio":
        # Inputs for the P/E Valuation Calculator
        net_income = st.number_input("Net Income (in thousand EUR)", min_value=0, step=1)
        number_of_shares = st.number_input("Number of Shares (in thousand)", min_value=0, step=1)
        pe_ratio = st.number_input("Price-to-Earnings (P/E) Ratio", min_value=0.0, step=0.1)

        # Calculate the P/E valuation
        if st.button("Calculate P/E Valuation"):
            if number_of_shares == 0:
                st.error("Number of Shares must be greater than 0.")
            else:
                earnings_per_share = net_income / number_of_shares
                valuation = earnings_per_share * pe_ratio

                st.write(f"Earnings per Share: {earnings_per_share:,.2f} thousand EUR")
                st.write(f"Valuation: {valuation:,.2f} thousand EUR")


        if st.checkbox("Explanation"):
            st.write("Price-to-Earnings (P/E) Ratio is a financial ratio that compares a company's current stock price to its earnings per share (EPS). The P/E ratio is a popular metric used by investors to evaluate a company's current market value and potential for growth. A high P/E ratio may indicate that the market has high expectations for the company's future earnings growth, while a low P/E ratio may suggest that the market has lower expectations or that the company is undervalued. However, it's important to consider other factors such as the company's industry, growth prospects, and financial health before making investment decisions based solely on the P/E ratio.")





































       



