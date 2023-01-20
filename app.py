import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from info import *
from functions import (complementaryColor, scrap_main_func, process_data, league_team_data, process_league_data)
from plot import make_plot

# APP TITLE
st.title("xG Distribution of Teams\n")

st.text("An app to evaluate shooting of various teams and see the probability of goals"+
        "they scored\nand conceded in comparison to the quality of chances they got and conceded")
st.caption("Made by Shreyas Khatri. Twitter: @khatri_shreyas\n\n", unsafe_allow_html=False)

# WIDGETS
col1, col2 = st.columns(2)
team_name = col1.selectbox("Select Team:", team_names, index=0)
season = col2.number_input("Select Season:", min_value=2014, max_value=2022, value=2022)

# COLOR WIDGETS SIDEBAR
team_col = st.sidebar.color_picker('Pick A Color:', '#EA2304')
comp_col = complementaryColor(team_col)
theme = st.sidebar.radio(
     "Visualisation Theme:",
     ('light', 'dark')
)

if theme == 'light':
    background = '#F2F2F2' 
    text_col = 'black'
elif theme == 'dark':
    background = complementaryColor('#F2F2F2')
    text_col = 'white' 

@st.cache
def full_data_fetching(team_name, season):
    league, df = scrap_main_func(team_name, season)
    df = df[df['situation']!='Penalty']
    (tot_goals_scored, tot_goals_conceded, matches, dic_team, dic_opp, total_prob_scored, total_prob_conceded, most_goals_scored,
    most_goals_conceded, least_goals_scored, least_goals_conceded, max_goals_scored, max_goals_conceded, max_prob_scored, 
    max_prob_conceded, shots_team_p90, shots_opp_p90, xg_pshot_for, xg_pshot_against, xg_for_p90, 
    xg_against_p90, no_simulations, shots_team, shots_opp) = process_data(df, team_name)
                
    df_leagues = league_team_data(league, season)
    shots_for_rank, xg_for_rank, xg_pshot_rank, shots_a_rank, xg_a_rank, xg_pshot_a_rank = tuple(process_league_data(df_leagues, team_name))

    return (df, league, tot_goals_scored, tot_goals_conceded, matches, dic_team, dic_opp, total_prob_scored, total_prob_conceded, 
        most_goals_scored, most_goals_conceded, least_goals_scored, least_goals_conceded, max_goals_scored, max_goals_conceded, 
        max_prob_scored, max_prob_conceded, shots_team_p90, shots_opp_p90, xg_pshot_for, xg_pshot_against, xg_for_p90, xg_against_p90,
        no_simulations, shots_team, shots_opp, shots_for_rank, xg_for_rank, xg_pshot_rank, shots_a_rank, xg_a_rank, xg_pshot_a_rank)

if st.button("Make visualisation"):
    with st.spinner('Wait for data to download and process...'):
        (df, league, tot_goals_scored, tot_goals_conceded, matches, dic_team, dic_opp, total_prob_scored, total_prob_conceded, 
        most_goals_scored, most_goals_conceded, least_goals_scored, least_goals_conceded, max_goals_scored, max_goals_conceded, 
        max_prob_scored, max_prob_conceded, shots_team_p90, shots_opp_p90, xg_pshot_for, xg_pshot_against, xg_for_p90, xg_against_p90,
        no_simulations, shots_team, shots_opp, shots_for_rank, xg_for_rank, xg_pshot_rank, shots_a_rank, xg_a_rank, 
        xg_pshot_a_rank) = full_data_fetching(team_name, season)

    # BAR AXES COLORS // DO NOT TOUCH
    col_bar_1 = [text_col]*(max_goals_scored - least_goals_scored+1)
    col_bar_1[tot_goals_scored-least_goals_scored] = team_col
    col_bar_2 = [text_col]*(max_goals_conceded - least_goals_conceded+1)
    col_bar_2[tot_goals_conceded-least_goals_conceded] = team_col

    fig, ax = make_plot(team_name, season, tot_goals_scored, tot_goals_conceded, matches, dic_team, dic_opp, total_prob_scored, 
        total_prob_conceded, most_goals_scored, most_goals_conceded, least_goals_scored, least_goals_conceded, max_goals_scored, 
        max_goals_conceded, max_prob_scored, max_prob_conceded, xg_pshot_for, xg_pshot_against, xg_for_p90, xg_against_p90,
        no_simulations, shots_team, shots_opp, shots_for_rank, xg_for_rank, xg_pshot_rank, shots_a_rank, xg_a_rank, xg_pshot_a_rank, 
        background, text_col, team_col, comp_col, col_bar_1, col_bar_2)
    plt.savefig('static/GoalsProb.png', dpi=300, facecolor=background)
    st.balloons()
    st.pyplot(fig)
    with open("static/GoalsProb.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="GoalsProb.png",
            mime="image/png"
           )

# SHOW EXAMPLES OF THEMES
st.subheader("Examples of charts:")
col1, col2 = st.columns(2)

image = Image.open('static/White.png')
col1.image(image, caption='Light theme')

image = Image.open('static/Black.png')
col2.image(image, caption='Dark theme')