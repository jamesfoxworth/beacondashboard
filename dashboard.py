import streamlit as st
import pandas as pd
from datetime import datetime
import regex as re
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Beacon Dashboard",
                   layout="wide", page_icon=":b:")

# Global variables
blue = "#004397"
yellow = "#FFC03B"

# Width and height standards
w = 750
l = 550

# Init datasets
beacon_law = None
brigids_hope = None
ca = None
essential_services = None
navigation = None
volunteer_data_day_center = None
beacon_law_counts_t = None
beacon_law_savings_t = None
essential_services_t = None
year = None
top_law_cases = None


def init_year(text):
    global year
    pattern = r'\b\d{4}\b'
    match = re.search(pattern, text)
    if match:
        year = match.group()
    else:
        year = datetime.now().year


def read_sheets(uploaded_file):
    global beacon_law, brigids_hope, ca, essential_services, navigation, volunteer_data_day_center, year

    beacon_law = pd.read_excel(
        uploaded_file, sheet_name="Beacon Law")
    brigids_hope = pd.read_excel(
        uploaded_file, sheet_name="Brigids Hope")
    ca = pd.read_excel(uploaded_file, sheet_name="CA")
    essential_services = pd.read_excel(
        uploaded_file, sheet_name="Essential Services")
    navigation = pd.read_excel(
        uploaded_file, sheet_name="Navigation")
    volunteer_data_day_center = pd.read_excel(
        uploaded_file, sheet_name="Volunteer Data (Day Center)")
    init_year(uploaded_file.name)


def clean(df):
    df_counts = df.drop(columns=['Count (YTD)'])
    df_counts = df_counts.dropna()
    df_t = df_counts.T.reset_index()
    df_t.columns = df_t.iloc[0]
    df_t = df_t.drop(0)
    df_t = df_t.rename(columns={"Service Type": "Month"})
    for index, value in enumerate(df_t["Month"]):
        df_t.at[index+1,
                "Month"] = value.replace('Count (', '').replace(')', '')
    return df_t


law_case_titles = {
    "Consumer": f"Beacon Law: Consumer Cases Throughout ",
    "Family Law": f"Beacon Law: Family Law Cases Throughout ",
    "Housing": f"Beacon Law: Housing-Related Cases Throughout ",
    "ID Restoration": f"Beacon Law: ID Restoration Cases Throughout ",
    "Individual Rights/Immigration": f"Beacon Law: Immigration and Individual Rights Cases Throughout ",
    "Expunction/Nondisclosure": f"Beacon Law: Record Clearing Cases Throughout ",
    "Public Benefits": f"Beacon Law: Public Benefits Cases Throughout ",
    "Other": f"Beacon Law: Other Cases Throughout ",
    "Wills/Estates": f"Beacon Law: Wills and Estates Cases Throughout ",
    "Closed Cases - Total # (BL)": f"Beacon Law: Total Closed Cases Throughout ",
    "Total Applications (BL)": f"Beacon Law: Total Applications Throughout "
}

savings_titles = {
    "Consumer": f"Beacon Law: Consumer Savings Throughout ",
    "Family Law": f"Beacon Law: Family Law Savings Throughout ",
    "Housing": f"Beacon Law: Housing-Related Savings Throughout ",
    "ID Restoration": f"Beacon Law: ID Restoration Savings Throughout ",
    "Individual Rights/Immigration": f"Beacon Law: Immigration and Individual Rights Savings Throughout ",
    "Expunction/Nondisclosure": f"Beacon Law: Record Clearing Savings Throughout ",
    "Public Benefits": f"Beacon Law: Public Benefits Savings Throughout ",
    "Other": f"Beacon Law: Other Savings Throughout ",
    "Wills/Estates": f"Beacon Law: Wills and Estates Savings Throughout ",
    "Total Savings": f"Beacon Law: Total Savings Throughout "
}

ca_titles = {
    "Total Assessments Completed (System)": f"Total Assessments Completed Throughout ",
    "Housing Assessments (Internal)": f"Housing Assessments Throughout ",
    "CA Contact": f"CA Contact Throughout ",
    "Pre-Navigation": f"Pre-Navigation Participation Throughout "
}

service_titles = {
    "Breakfast": f"Breakfast Service Use Throughout ",
    "Building Entry": f"Building Entry Throughout ",
    "Laundry": f"Laundry Service Use Throughout ",
    "Lunch": f"Lunch Service Use Throughout ",
    "Showers": f"Shower Service Use Throughout ",
    "Total Meals": f"Total Meals (Breakfast and Lunch) Throughout ",
    "Unduplicated clients served": f"Unique Clients Served Throughout ",
    "Clients in Program": f"Clients in Program Throughout ",
    "New Enrollments": f"New Enrollments Throughout ",
    "Service Days in the Month": f"Service Days Throughout Each Month ()",
    "Resource and Referral - AD": f"Resource and Referral (AD) Throughout ",
    "Resource and Referral - CG": f"Resource and Referral (CG) Throughout ",
    "Mail Check": f"Mail Check Service Use Throughout "
}

navigation_titles = {
    "Clients in Programs": f"Clients in Programs Throughout ",
    "Community Covid Housing Referrals": f"Community COVID Housing Referrals Throughout ",
    "Move-Ins": f"Move-Ins Throughout ",
    "Unable to Locate/Contact": f"Number of People Unable to Locate or Contact Throughout ",
    "Jail/Hospitalization": f"Jail/Hospitalizations Throughout ",
    "Refused": f"Number of Refusals Throughout ",
    "Other": f"Other - ",
    "Total Number Exited": f"Total Number Exited Throughout "
}


def strip_column_names(df):
    for column in df.columns:
        new_column_name = column.strip()
        df.rename(columns={column: new_column_name}, inplace=True)


def clean_law_counts():
    global beacon_law_counts_t
    beacon_law_counts = beacon_law.drop(
        columns=[col for col in beacon_law.columns if col.startswith("Savings")])
    beacon_law_counts = beacon_law_counts.drop(
        columns=["YTD Savings", "Unnamed: 14", 'Count (YTD)'])
    beacon_law_counts = beacon_law_counts.dropna()
    beacon_law_counts_t = beacon_law_counts.T.reset_index()
    beacon_law_counts_t.columns = beacon_law_counts_t.iloc[0]
    beacon_law_counts_t = beacon_law_counts_t.drop(0)
    beacon_law_counts_t = beacon_law_counts_t.rename(
        columns={"Service Type": "Month"})
    for index, value in enumerate(beacon_law_counts_t["Month"]):
        beacon_law_counts_t.at[index+1,
                               "Month"] = value.replace('Count (', '').replace(')', '')
    strip_column_names(beacon_law_counts_t)


def clean_law_savings():
    global beacon_law_savings_t
    beacon_law_savings = beacon_law.drop(
        columns=[col for col in beacon_law.columns if col.startswith("Count")])
    beacon_law_savings = beacon_law_savings.drop(
        columns=["YTD Savings", "Unnamed: 14"])
    beacon_law_savings = beacon_law_savings.dropna()
    beacon_law_savings_t = beacon_law_savings.T.reset_index()
    beacon_law_savings_t.columns = beacon_law_savings_t.iloc[0]
    beacon_law_savings_t = beacon_law_savings_t.drop(0)
    beacon_law_savings_t = beacon_law_savings_t.rename(
        columns={"Service Type": "Month"})
    for index, value in enumerate(beacon_law_savings_t["Month"]):
        beacon_law_savings_t.at[index+1, "Month"] = value.replace(
            'Savings (Month -', '').replace(')', '')
    strip_column_names(beacon_law_savings_t)


def clean_services():
    global essential_services_t, essential_services
    essential_services = essential_services.dropna()
    essential_services_t = essential_services.T.reset_index()
    essential_services_t.columns = essential_services_t.iloc[0]
    essential_services_t = essential_services_t.drop(0)
    essential_services_t = essential_services_t.rename(
        columns={"Service Type": "Month"})
    for index, value in enumerate(essential_services_t["Month"]):
        essential_services_t.at[index+1,
                                "Month"] = value.replace('Count (', '').replace(')', '')
    essential_services_t = essential_services_t.drop(13)


def plot_law_savings_bars():
    global top_law_cases
    law_count_filter = beacon_law[beacon_law['Service Type']
                                  != 'Closed Cases - Total # (BL)']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Applications (BL)']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Number of Unduplicated Clients']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Number of PB Volunteers']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Number of PB Volunteer Hours']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Savings']
    top5_count = law_count_filter.sort_values(
        by='YTD Savings', ascending=False).head(5)

    fig = px.bar(top5_count, x='Service Type', y='YTD Savings',
                 title="Beacon Law - Savings " + year,
                 labels={'Service Type': 'Legal Service',
                         'YTD Savings': 'Savings (YTD)'},
                 text='YTD Savings')
    fig.update_traces(marker_color=blue)
    fig.update_layout(width=w, height=l)
    st.plotly_chart(fig)


def plot_law_cases_bars():
    global top_law_cases
    law_count_filter = beacon_law[beacon_law['Service Type']
                                  != 'Closed Cases - Total # (BL)']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Applications (BL)']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Number of Unduplicated Clients']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Number of PB Volunteers']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Number of PB Volunteer Hours']
    law_count_filter = law_count_filter[law_count_filter['Service Type']
                                        != 'Total Savings']
    top5_count = law_count_filter.sort_values(
        by='Count (YTD)', ascending=False).head(5)

    fig = px.bar(top5_count, x='Service Type', y='Count (YTD)',
                 title="Beacon Law - Cases " + year,
                 labels={'Service Type': 'Legal Service',
                         'YTD Savings': 'Savings (YTD)'},
                 text='Count (YTD)')
    fig.update_traces(marker_color=blue)
    fig.update_layout(width=w, height=l)
    st.plotly_chart(fig)


def plot_service_bars():
    bar_services = essential_services.drop(0)
    bar_services.iloc[4, bar_services.columns.get_loc(
        'Service Type')] = "Meals (Breakfast + Lunch)"
    for i in range(1, 14):
        if i == 10 or i == 5 or i == 2 or i == 4 or i == 15:
            continue
        bar_services = bar_services.drop(i)

    top5_serv = bar_services.sort_values(by='Count (YTD)', ascending=False)
    fig = px.bar(
        top5_serv,
        x='Service Type',
        y='Count (YTD)',
        text='Count (YTD)',
        color='Count (YTD)',
        color_continuous_scale='blues'
    )

    fig.update_traces(textposition='auto', marker_color=blue)

    fig.update_layout(
        title="Top Essential Services",
        xaxis_title="Service",
        yaxis_title="Count (YTD)"
    )
    fig.update_layout(width=w, height=l)
    st.plotly_chart(fig)


def show_line_df(option, df, titles):
    if option in df.columns and option != "Month":
        fig = px.line(df, x="Month", y=option, title=titles[option] + year)
        fig.update_layout(yaxis=dict(range=[0, df[option].max()]))
        fig.update_layout(width=w, height=l)
        fig.update_traces(mode='markers+lines')
        st.plotly_chart(fig)


def main():
    st.title("Beacon Dashboard")
    st.markdown(
        '<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    if file is not None:
        read_sheets(file)
        clean_law_counts()
        clean_law_savings()
        clean_services()

    st.header("Essential Services")
    service_col1, service_col2 = st.columns(2)

    with service_col1:
        default = "Clients in Program"
        idx = list(service_titles.keys()).index(
            default) if default in list(service_titles.keys()) else 0
        selected_option = st.selectbox(
            "Essential Services", list(service_titles.keys()))
        show_line_df(selected_option, essential_services_t, service_titles)

    with service_col2:
        plot_service_bars()

    st.header("Brigid's Hope")
    hope_col1, hope_col2 = st.columns(2)

    with hope_col1:
        keys = ['Increased Education/Income Post-Graduation', 'Did Not Increase']
        col = "Count (YTD)"
        data = [brigids_hope.iloc[13][col], 1-brigids_hope.iloc[13][col]]
        fig = px.pie(names=keys, values=data, title='Percentage of Individuals Based on Post-Graduation Income/Education Increase',
                     color_discrete_sequence=[blue, yellow])

        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(width=w, height=l)
        st.plotly_chart(fig)

    with hope_col2:
        keys = ['Moved into Stable Housing',
                'Did Not Move Into Stable Housing']
        col = "Count (YTD)"
        data = [brigids_hope.iloc[12][col], 1-brigids_hope.iloc[12][col]]
        fig = px.pie(names=keys, values=data, title='Percentage of Individuals who Moved Into Stable Housing at the End of the Program',
                     color_discrete_sequence=[blue, yellow])

        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(width=w, height=l)
        st.plotly_chart(fig)

    st.header("Beacon Law (Cases)")
    law_col1, law_col2 = st.columns(2)

    with law_col1:
        default = "Closed Cases - Total # (BL)"
        idx = list(law_case_titles.keys()).index(
            default) if default in list(law_case_titles.keys()) else 0
        selected_option = st.selectbox(
            "Beacon Law (Cases):", list(law_case_titles.keys()), index=idx)
        show_line_df(selected_option,
                     beacon_law_counts_t, law_case_titles)

    with law_col2:
        plot_law_cases_bars()

    st.header("Beacon Law (Savings)")
    savings_col1, savings_col2 = st.columns(2)

    with savings_col1:
        default = "Total Savings"
        idx = list(savings_titles.keys()).index(
            default) if default in list(savings_titles.keys()) else 0
        selected_option = st.selectbox(
            "Beacon Law (Savings):", list(savings_titles.keys()), index=idx)
        show_line_df(selected_option, beacon_law_savings_t, savings_titles)

    with savings_col2:
        plot_law_savings_bars()
        st.empty()

    keys = ['Back Awards and Ongoing Benefits (Social Security & Consumer)',
            'Cost Savings/Costs Avoided (ID Restoration, Record Clearing, and Landlord/Tenant)']
    col = 'YTD Savings'
    total = beacon_law.iloc[9][col]
    benefits = beacon_law.iloc[6][col] + beacon_law.iloc[0][col]
    data = [benefits, total-benefits]
    fig = px.pie(names=keys, values=data, title='Beacon Law: Dollar Outcomes',
                 color_discrete_sequence=[blue, yellow])

    fig.update_traces(textposition='outside', textinfo='percent+label')
    fig.update_layout(width=w, height=l)
    st.plotly_chart(fig, use_container_width=True)

    st.header("Housing (Coordinated Access / Navigation)")
    housing_col1, housing_col2 = st.columns(2)

    with housing_col1:
        show_line_df("Housing Assessments (Internal)", clean(ca), ca_titles)

    with housing_col2:
        keys = ['Move-ins', 'Unable to Contact<br>Or Locate',
                'Jail/Hospitalization', 'Refused', 'Other']
        col = "Count (YTD)"
        data = [navigation.iloc[2][col], navigation.iloc[3][col],
                navigation.iloc[4][col], navigation.iloc[5][col], navigation.iloc[6][col]]
        fig = px.pie(names=keys, values=data, title='Navigation Move-ins')

        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(width=w, height=l)
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()
