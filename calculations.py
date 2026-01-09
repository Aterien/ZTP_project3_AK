import pandas as pd

'''
Moduł do obliczeń
'''

def calculate_station_monthly_averages(df):
    """
    Oblicza miesięczne średnie wartości PM2.5 dla każdej stacji w każdym roku
    
    Args:
        df (pd.DataFrame): DataFrame z danymi PM2.5, gdzie kolumny to kody stacji, a indeks to daty.
        
    Returns:
        pd.DataFrame: DataFrame z miesięcznymi średnimi wartościami PM2.5.
    """
    df_result = df.copy()
    df_result["Rok"] = df["Data"].dt.year
    df_result["Miesiąc"] = df["Data"].dt.month
    df_result = df_result.sort_index(axis=1)

    month_means = df_result.groupby(["Rok", "Miesiąc"]).mean(numeric_only=True)
    
    return month_means

def calculate_city_monthly_averages(df):
    """
    Oblicza miesięczne średnie wartości PM2.5 dla każdego miasta w każdym roku
    
    Args:
        df (pd.DataFrame): DataFrame ze średnimi dla każdej stacji.
        
    Returns:
        pd.DataFrame: DataFrame z miesięcznymi średnimi wartościami PM2.5 dla miejscowości.
    """
    df_result = df.copy()
    city_month_means = df_result.T.groupby(level=0).mean().T

    return city_month_means

def calculate_days_exceeding_limit(df):
    """
    Oblicza liczbę dni w miesiącu, kiedy średnia dzienna wartość PM2.5 przekracza określony limit.
    
    Args:
        df (pd.DataFrame): DataFrame z danymi PM2.5, gdzie kolumny to kody stacji, a indeks to daty.
        limit (float): Limit wartości PM2.5 do sprawdzenia przekroczeń.
        df (pd.DataFrame): DataFrame z danymi PM2.5, gdzie kolumny to kody stacji, a indeks to daty.
        limit (float): Limit wartości PM2.5 do sprawdzenia przekroczeń.
    """
    # Przygotowanie dataframe'u z datami bez czasu
    df_c = df.copy()
    df_c['Dzień'] = df_c['Data'].dt.date #dzień, czyli data w formacie rok-miesiąc-dzień
    df_c = df_c.drop(columns=['Data', 'Rok', 'Miesiąc'], errors='ignore')

    # Obliczanie średnich dziennych stężeń na stacje
    day_means = df_c.groupby('Dzień').mean(numeric_only=True).reset_index()

    # Sprawdzanie ile dni w każdym roku przekroczono 15 µg/m^3 dla każdej stacji
    day_means = day_means.set_index('Dzień')
    mask = day_means > 15
    day_means['Rok'] = pd.to_datetime(day_means.index).year

    exceeded_results = mask.groupby(day_means['Rok']).sum()

    return exceeded_results

def get_3_lowest_highest(df, year):
    """
    Znajduje 3 najniższych i 3 najwyższych miesięcznych średnich wartości PM2.5 dla każdej stacji.
    
    Args:
        df (pd.DataFrame): DataFrame z miesięcznymi średnimi wartościami PM2.5.
        year (int): Rok, dla którego obliczamy wartości.

    Returns:
        df (pd.DataFrame): DataFrame z 3 najniższymi i 3 najwyższymi wartościami PM2.5 dla każdej stacji.
    """
    exceed = df.loc[year].copy()
    smallest3 = exceed.nsmallest(3)
    largest3 = exceed.nlargest(3)

    top_bottom = list(smallest3.index) + list(largest3.index)
    df_results = df[top_bottom]

    return df_results