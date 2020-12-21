"""
Load data from opendota
"""
import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt

#### settings
logger = logging.getLogger(__name__)
plt.style.use("ggplot")
pd.set_option("display.max_rows", 150)
pd.set_option("display.max_columns", 50)

#### constants
BASE_URL = "https://api.opendota.com/api"

#### functions
def get_pro_players():
    """
    Load list of all pro players from opendota
    """
    r = requests.get(f"{BASE_URL}/proPlayers")
    if r.status_code == 200:
        players_dict = r.json()
        players_df = pd.DataFrame.from_dict(players_dict)
        return players_df
    else:
        logger.info(f"Requesting pro players failed with error code: {r.status_code}")
        return pd.DataFrame()


def get_players_per_country(players):
    """
    Group by country code and return all players where country is present
    """
    players_grouped = (
        players.loc[players["country_code"] != ""]
        .groupby("country_code")
        .size()
        .sort_values(ascending=False)
    )
    return players_grouped


def plot_players_per_country(players_country):
    """
    Plot players per country using a bar chart
    """
    fig, ax = plt.subplots(1, 1)
    players_country.head(20).plot.bar(ax=ax)
    ax.tick_params(axis="x", rotation=60)
    ax.set_title('Number of Pro Players per Country (Top 20)')
    ax.set_ylabel('Number of Players')
    ax.set_xlabel('Country Code')
    plt.show()


if __name__ == "__main__":
    players_df = get_pro_players()
    players_country = get_players_per_country(players_df)
    plot_players_per_country(players_country)