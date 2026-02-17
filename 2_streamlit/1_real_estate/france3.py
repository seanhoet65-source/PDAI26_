import pandas as pd
import streamlit as st


@st.cache_data
def load_data(url):
    """Load and cache data from URL."""
    return pd.read_csv(url, compression="gzip", low_memory=False)


def display_property_info(df):
    """Display info about a selected individual property."""
    st.header("Individual Property Search")

    # Unique label combining number + street + date
    df['display_name'] = (
        df['adresse_numero'].astype(str) + " " +
        df['adresse_nom_voie'] + " (" +
        df['date_mutation'] + ")"
    )

    selected_label = st.selectbox(
        "Select a property to view details:",
        df['display_name'].unique()
    )

    property_details = df[df['display_name'] == selected_label].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Price", f"{property_details['valeur_fonciere']} €")
        st.write(f"**Address:** {property_details['adresse_numero']} {property_details['adresse_nom_voie']}")
        st.write(f"**City:** {property_details['nom_commune']}")
    with col2:
        st.write(f"**Surface area:** {property_details['surface_reelle_bati']} m²")
        st.write(f"**Rooms:** {property_details['nombre_pieces_principales']}")
        st.write(f"**Type:** {property_details['type_local']}")

    st.divider()


def display_table(df, year):
    """Display the raw data table."""
    st.header("Browse All Data")
    st.write(f"Showing {df.shape[0]} transactions for {year}")
    st.dataframe(df)


def get_sidebar_and_data():
    """Get sidebar filters and load data."""
    with st.sidebar:
        st.header("Filters")
        year = st.selectbox("Year:", [2020, 2021, 2022, 2023, 2024])
        department = st.selectbox("Department:", [75, 92, 93, 94])
        only_sales = st.checkbox("Exclude non-sale transactions", value=True)

    file = (
        f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
        f"departements/{department}.csv.gz"
    )
    df = load_data(file)

    if only_sales:
        df = df[df["nature_mutation"] == "Vente"]

    median_price = df["valeur_fonciere"].median()
    st.sidebar.write(f"Median price: {median_price:.0f} €")

    return df, year


def main():
    st.title("Real estate prices in France")

    df, year = get_sidebar_and_data()

    display_property_info(df)
    display_table(df, year)


if __name__ == "__main__":
    main()