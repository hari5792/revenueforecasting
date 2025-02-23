import streamlit as st
import pandas as pd
import bcrypt
import os
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from pmdarima import auto_arima
import joblib

plt.style.use("ggplot")
st.title("📈 5-Year Revenue Forecasting App")
st.write("#### Predict revenue trends for the next five years using ARIMA modeling.")

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to validate user credentials
def validate_user(username, password, users_df):
    user = users_df[users_df['username'] == username]
    if not user.empty:
        stored_hash = user.iloc[0]['password_hash']
        return bcrypt.checkpw(password.encode(), stored_hash.encode())
    return False

# Load the CSV file with user credentials
credentials_file = "users.csv"
if not os.path.exists(credentials_file):
    st.error("User credentials file not found. Please create 'users.csv' with hashed login credentials.")
    st.stop()

users_df = pd.read_csv(credentials_file)

# Session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login Page
if not st.session_state.authenticated:
    st.subheader("🔐 Login")

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    login_button = st.button("Login")

    if login_button:
        if validate_user(username, password, users_df):
            st.session_state.authenticated = True
            st.success("Login successful! Welcome to the Revenue Forecasting App.")
        else:
            st.error("Invalid username or password. Please try again.")

    st.stop()

# Sidebar navigation with icons and customized appearance
with st.sidebar:
    selected_page = option_menu(
        menu_title="Navigation",
        options=["Welcome", "Predicted Data", "Forecast Table"],
        icons=["house", "graph-up-arrow", "table"],
        menu_icon="menu-app",
        default_index=0,
    )

# Load and prepare the data
data = pd.read_csv("dataset.csv")

# Validate and clean the dataset
if "Month" not in data.columns:
    for col in data.columns:
        if col.strip().lower() == "month":
            data = data.rename(columns={col: "Month"})
            break
    else:
        st.error("No 'Month' column found in the dataset. Please check the CSV file.")
        st.stop()

# Convert 'Month' to datetime format and set as index
data["Month"] = pd.to_datetime(data["Month"])
data.set_index("Month", inplace=True)

# Clean the 'Revenue' column
data[" Revenue "] = (
    data[" Revenue "].replace({"\$": "", ",": ""}, regex=True).astype(float)
)

# Preprocess data
data.index = data.index + pd.offsets.MonthEnd(-1)  # Adjust to month-end
data = data[~data.index.duplicated(keep="first")]  # Remove duplicates
data[" Revenue "] = data[" Revenue "].fillna(method="ffill")  # Fill missing values

# Forecast parameters
n_periods = 60  # 5 years = 60 months
model_filename = "arima_model.pkl"

# Load or train the model
if "model" not in st.session_state:
    if os.path.exists(model_filename):
        with st.spinner("Loading ARIMA model..."):
            try:
                st.session_state.model = joblib.load(model_filename)
                st.success("Model loaded successfully!")
            except EOFError:
                st.error("Model file is corrupted. Please delete the file and retrain the model.")
                os.remove(model_filename)
    else:
        with st.spinner("Training ARIMA model..."):
            st.session_state.model = auto_arima(
                data[" Revenue "],
                seasonal=True,
                m=12,
                trace=False,
                stepwise=True,
            )
            joblib.dump(st.session_state.model, model_filename)
        st.success("Model trained and saved successfully!")

# Forecasting
model = st.session_state.model
forecast = model.predict(n_periods=n_periods)
forecast_index = pd.date_range(start=data.index[-1], periods=n_periods + 1, freq="M")[1:]
forecast_series = pd.Series(forecast, index=forecast_index)

# Initialize slider state if not set
if "selected_end_year" not in st.session_state:
    st.session_state.selected_end_year = 1976

# Initialize selected_years globally
selected_years = (1972, st.session_state.selected_end_year)

# Page content based on selected menu option
if selected_page == "Welcome":
    st.write("## Welcome to the Revenue Forecasting App!")
    st.info(
        "Navigate to 'Predicted Data' to view the forecast graph or 'Forecast Table' for the data table and download option."
    )

elif selected_page == "Predicted Data":
    st.write("### 5-Year Revenue Forecast")

    # Slider for selecting the end year with a start of 1972
    st.session_state.selected_end_year = st.slider(
        "Select End Year for Forecast Plot",
        min_value=1972,
        max_value=1976,
        value=st.session_state.selected_end_year,
        step=1,
    )
    selected_years = (1972, st.session_state.selected_end_year)

    # Combined forecast plot
    st.write("#### Combined Forecast for Selected Years")
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(data, label="Historical Revenue", color="black", linewidth=2)
    ax.plot(
        forecast_series[
            (forecast_series.index.year >= selected_years[0])
            & (forecast_series.index.year <= selected_years[1])
        ],
        label="Forecasted Revenue (Selected Years)",
        color="red",
        linestyle="--",
        linewidth=2,
    )
    ax.set_title(f"Combined Forecast (1972 - {selected_years[1]})", fontsize=16)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Revenue ($M)", fontsize=14)
    ax.legend()
    st.pyplot(fig)

    # Individual forecast plots by year
    for year in range(selected_years[0], selected_years[1] + 1):
        year_forecast = forecast_series[forecast_series.index.year == year]
        st.write(f"#### Forecast for {year}")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(year_forecast, label=f"Forecasted Revenue for {year}", color="blue")
        ax.set_title(f"Forecasted Revenue - {year}", fontsize=14)
        ax.set_xlabel("Year-Month", fontsize=12)
        ax.set_ylabel("Revenue ($M)", fontsize=12)
        ax.legend()
        st.pyplot(fig)

elif selected_page == "Forecast Table":
    st.write("### Forecasted Revenue Data")

    # Creating the forecasted data frame
    forecast_df = forecast_series.reset_index()
    forecast_df.columns = ["Date", "Forecasted Revenue"]

    # Filter for selected years
    filtered_df = forecast_df[
        forecast_df["Date"].dt.year.isin(
            range(selected_years[0], selected_years[1] + 1)
        )
    ]

    # Style the DataFrame
    styled_df = filtered_df.style.format({"Forecasted Revenue": "${:,.2f}"})

    # Display the styled DataFrame with download option
    st.dataframe(styled_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Download Forecast Data as CSV",
        data=csv,
        file_name="forecast_data.csv",
        mime="text/csv",
    )

    ### Updated to run Jenkins

    # Use This command to run the app streamlit run streamlit.py --server.port 8501 --server.headless true
