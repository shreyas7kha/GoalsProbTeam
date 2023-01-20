import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker
import matplotlib as mpl
import matplotlib.patheffects as PathEffects
import seaborn as sns
from highlight_text import fig_text
from functions import suffix_def

def change_spine_col(ax, col):
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_color(col)

def add_legend(ax, xg_pshot_for, xg_pshot_rank, xg_pshot_against, xg_pshot_a_rank, xg_for_p90, xg_for_rank,
            xg_against_p90, xg_a_rank, col, text_col):
    # ADD INFOMRATION HEXAGONS
    ax.axis('off')
    ax.set_xlim(0.1, 0.9)
    ax.set_ylim(0,1)
    y_pt, y_lab_pt, y_rank_pt = 0.5, 0.2, 0.36
    ax.scatter([0.2,0.4,0.6,0.8], [y_pt]*4, s=2000, ec=text_col, marker='h', c='None', ls='--')

    # ADD LABELS
    ax.text(0.2,y_pt,'{:.2f}'.format(xg_pshot_for), c=col, ha='center', va='center',
           size=15)
    ax.text(0.2,y_lab_pt,'NpxG\nper Shot', c='#ad993c', ha='center', va='top',size=10)
    ax.text(0.2,y_rank_pt,f'{xg_pshot_rank}{suffix_def(xg_pshot_rank)}', c='#878787', ha='center', va='center',size=8)
    
    ax.text(0.4,y_pt,'{:.2f}'.format(xg_pshot_against), c=col, ha='center', va='center',
           size=15)
    ax.text(0.4,y_lab_pt,'NpxG\nAgainst\nper Shot', c='#ad993c', ha='center', va='top',size=10)
    ax.text(0.4,y_rank_pt,f'{xg_pshot_a_rank}{suffix_def(xg_pshot_a_rank)}', c='#878787', 
            ha='center', va='center',size=8)
    
    ax.text(0.6,y_pt,'{:.2f}'.format(xg_for_p90), c=col, ha='center', va='center',
           size=15)
    ax.text(0.6,y_lab_pt,'NpxG\nper 90', c='#ad993c', ha='center', va='top',size=10)
    ax.text(0.6,y_rank_pt,f'{xg_for_rank}{suffix_def(xg_for_rank)}', c='#878787', ha='center', va='center',size=8)
    
    ax.text(0.8,y_pt,'{:.2f}'.format(xg_against_p90), c=col, ha='center', va='center',
           size=15)
    ax.text(0.8,y_lab_pt,'NpxG\nAgainst\nper 90', c='#ad993c', ha='center', va='top',size=10)
    ax.text(0.8,y_rank_pt,f'{xg_a_rank}{suffix_def(xg_a_rank)}', c='#878787', ha='center', va='center',size=8)

def prob_hist(ax, col_bar, max_goals, least_goals, most_goals, tot_goals, dic, no_simulations, background, col):
    ax.patch.set_facecolor(background)
    ax.bar(np.arange(least_goals,max_goals+1), np.array(list(dic.values()))*100/no_simulations,
                ec=col_bar, fc='none', hatch='/')
    for s in ['top','right']:
        ax.spines[s].set_visible(False)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax.set_xticks(np.arange(least_goals, max_goals+1))
    
    # TEXT IN AXES 1
    for i,v in enumerate(ax.patches):
        if i+least_goals==tot_goals:
            ax.text(v.get_x()+v.get_width()/2, v.get_height(),
                str(round(v.get_height(),2))+'%', c=col, ha='center', va='bottom',
                fontsize = 9, weight='bold', family='Calibri')
        if i+least_goals==most_goals:
            if most_goals == tot_goals: break
            ax.text(v.get_x()+v.get_width()/2, v.get_height(),
                str(round(v.get_height(),2))+'%', ha='center', va='bottom',
                fontsize = 9, weight='bold', family='Calibri')

def make_plot(team_name, season, tot_goals_scored, tot_goals_conceded, matches, dic_team, dic_opp, total_prob_scored, total_prob_conceded, 
        most_goals_scored, most_goals_conceded, least_goals_scored, least_goals_conceded, max_goals_scored, max_goals_conceded, 
        max_prob_scored, max_prob_conceded, xg_pshot_for, xg_pshot_against, xg_for_p90, xg_against_p90,
        no_simulations, shots_team, shots_opp, shots_for_rank, xg_for_rank, xg_pshot_rank, shots_a_rank, xg_a_rank, xg_pshot_a_rank, 
        background, text_col, team_col, comp_col, col_bar_1, col_bar_2):

    mpl.rcParams['font.family']= 'Monospace'
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['font.weight'] = 'bold'
    mpl.rcParams['text.color'] = text_col
    mpl.rcParams['xtick.color'] = text_col
    mpl.rcParams['ytick.color'] = text_col
    mpl.rcParams['legend.title_fontsize'] = 20
    mpl.rcParams['legend.fontsize'] = 17

    fig, ax = plt.subplots(figsize=(10,10))
    fig.set_facecolor(background)
    ax.axis('off')

    # Team Goals Bar
    ax1 = fig.add_axes([0.1,0.42,0.87,0.26])
    change_spine_col(ax1, text_col)
    prob_hist(ax1, col_bar_1, max_goals_scored, least_goals_scored, most_goals_scored, tot_goals_scored, dic_team,
            no_simulations, background, team_col)
    ax1.set_xlabel('Number of Goals Scored', size=13, weight='bold')
    ax1.set_ylabel('Probability', size=13, weight='bold')
    ax1.set_title('Probability of Goals Scored Based on Shot Simulation ({:.2f} xG For)'.format(sum(shots_team)), 
                size=16, weight='bold', 
                loc='left', c='#878787')
    x_pt1 = ax1.get_xlim()[0] + 0.875*(ax1.get_xlim()[1]-ax1.get_xlim()[0])
    x_pt2 = ax1.get_xlim()[0] + 0.125*(ax1.get_xlim()[1]-ax1.get_xlim()[0])
    y_pt = 0.8*(ax1.get_ylim()[1]-ax1.get_ylim()[0])

    # TEXT IN AXES 1
    for i,v in enumerate(ax1.patches):
        if i+least_goals_scored==tot_goals_scored:
            if v.get_height()/max_prob_scored < 0.45:
                ax1.text(v.get_x()+v.get_width()/2, 0.1*y_pt + v.get_height(), 
                        'Actual goals scored', rotation = 90, ha='center', va='bottom', c='#ad993c', size=8)
            else:
                ax1.text(v.get_x()+v.get_width()/2, v.get_height()/2, 
                        'Actual goals scored', rotation = 90, ha='center', va='center', c='#ad993c', size=8,
                        bbox={'facecolor': background,'pad': 0.5, 'edgecolor':background})
            
    # HEXAGONS
    ax1.scatter(x_pt1, y_pt, s=2750, marker='h', c='none', ec=text_col, ls='--')
    txt1 = ax1.text(x_pt1, y_pt, '{:.2f}%'.format(total_prob_scored), c=team_col, ha='center', va='center',
                size=12)
    txt1.set_path_effects([PathEffects.withStroke(linewidth=1, foreground=text_col)])
    ax1.text(x_pt1, 0.7*y_pt, f'Probability of\nscoring greater or\nequal to {tot_goals_scored} goals', 
            c='#ad993c', ha='center', va='center', size=9)
    ax1.scatter(x_pt2, y_pt, s=2750, marker='h', c='none', ec=text_col, ls='--')
    txt2 = ax1.text(x_pt2, y_pt, '{:.2f}'.format(len(shots_team)/matches), c=team_col, ha='center', va='center',
                size=14)
    txt2.set_path_effects([PathEffects.withStroke(linewidth=1, foreground=text_col)])
    ax1.text(x_pt2, 0.7*y_pt, f'Shots\ntaken\nper 90', 
            c='#ad993c', ha='center', va='center', size=9)
    ax1.text(x_pt2, 0.9*y_pt, f'{shots_for_rank}{suffix_def(shots_for_rank)}', 
            c='#878787', ha='center', va='center', size=8.5)

    # Opposition Goals Bar
    ax3 = fig.add_axes([0.1,0.08,0.87,0.26])
    change_spine_col(ax3, text_col)
    prob_hist(ax3, col_bar_2, max_goals_conceded, least_goals_conceded, most_goals_conceded, tot_goals_conceded, dic_opp,
            no_simulations, background, team_col)
    ax3.set_xlabel('Number of Goals Conceded', size=13, weight='bold')
    ax3.set_ylabel('Probability', size=13, weight='bold')
    ax3.set_title('Probability of Goals Conceded Based on Shot Simulation ({:.2f} xGA)'.format(sum(shots_opp)), 
                size=16, weight='bold', loc='left', c='#878787')
    x_pt1 = ax3.get_xlim()[0] + 0.875*(ax3.get_xlim()[1]-ax3.get_xlim()[0])
    x_pt2 = ax3.get_xlim()[0] + 0.125*(ax3.get_xlim()[1]-ax3.get_xlim()[0])
    y_pt = 0.8*(ax3.get_ylim()[1]-ax3.get_ylim()[0])

    # TEXT IN AXES 3
    for i,v in enumerate(ax3.patches):
        if i+least_goals_conceded==tot_goals_conceded:
            if v.get_height()/max_prob_conceded < 0.5:
                ax3.text(v.get_x()+v.get_width()/2, 0.1*y_pt + v.get_height(), 
                        'Actual goals conceded', rotation = 90, ha='center', va='bottom', c='#ad993c', size=8)
            else:
                ax3.text(v.get_x()+v.get_width()/2, v.get_height()/2, 
                        'Actual goals conceded', rotation = 90, ha='center', va='center', c='#ad993c', size=8,
                        bbox={'facecolor': background,'pad': 0.5, 'edgecolor':background})
            
    # HEXAGONS
    ax3.scatter(x_pt1, y_pt, s=2750, marker='h', c='none', ec=text_col, ls='--')
    txt1 = ax3.text(x_pt1, y_pt, '{:.2f}%'.format(total_prob_conceded), c=team_col, ha='center', va='center',
                size=12)
    txt1.set_path_effects([PathEffects.withStroke(linewidth=0.75, foreground=text_col)])
    ax3.text(x_pt1, 0.7*y_pt, f'Probability of\nconceding lesser or\nequal to {tot_goals_conceded} goals', 
            c='#ad993c', ha='center', va='center', size=9)
    ax3.scatter(x_pt2, y_pt, s=2750, marker='h', c='none', ec=text_col, ls='--')
    txt2 = ax3.text(x_pt2, y_pt, '{:.2f}'.format(len(shots_opp)/matches), c=team_col, ha='center', va='center',
                size=14)
    txt2.set_path_effects([PathEffects.withStroke(linewidth=0.75, foreground=text_col)])
    ax3.text(x_pt2, 0.7*y_pt, f'Shots\nconceded\nper 90', 
            c='#ad993c', ha='center', va='center', size=9)
    ax3.text(x_pt2, 0.9*y_pt, f'{shots_a_rank}{suffix_def(shots_a_rank)}', 
            c='#878787', ha='center', va='center', size=8.5)

    # CHANCE VARIATION HIST
    bins = np.arange(0,1.01,0.1)
    ax2 = fig.add_axes([0.6,0.76,0.37,0.2])
    change_spine_col(ax2, text_col)
    ax2.patch.set_facecolor(background)
    sns.distplot(np.array(shots_team), ax=ax2, bins=bins, hist=False, 
                    kde_kws={"color": team_col, "lw": 1})
    sns.distplot(np.array(shots_opp), ax=ax2, bins=bins, hist=False, 
                kde_kws={"color": comp_col, "ls":'--', "lw": 0.5})

    ax2.hist(np.array(shots_opp), density=True, bins=bins, ec=comp_col, fc='none', alpha=0.5)
    ax2.hist(np.array(shots_team), density=True, bins=bins, ec=team_col, fc='none', alpha=0.75)
    for s in ['top','right']:
        ax2.spines[s].set_visible(False)
    ax2.set_xlim(0,1)
    ax2.set_title('xG Distribution of Shots', size=14, weight='bold', loc='left', c='#878787')
    ax2.set_ylabel('Density', size=12, weight='bold')
    ax2.set_xlabel('xG Value of Shot', size=12, weight='bold')
    ax2.set_yticklabels([y/10 for y in ax2.get_yticks()])
    ax2.text(0.175, 0.7*ax2.get_ylim()[1], 'Solid line represents density distribution of\nvalue of'+
            f' shots taken by {team_name}\nin {season%2000}/{season%2000+1}.', size=9, c=team_col)
    ax2.text(0.175, 0.4*ax2.get_ylim()[1], 'Dashed line represents density distribution of\nvalue'+
            f' of shots conceded by {team_name}\nin {season%2000}/{season%2000+1}.', size=9, c=comp_col)

    # LABELS
    fig.text(0.03,0.95,'TEAM xG DISTRIBUTION', size=30, c='#878787')
    fig.text(0.03, 0.91, f'{team_name} | {season}/{season%2000+1}'.upper(), size=23, c='#ad993c')
    fig_text(0.05, 0.89, 'Number of Goals Scored: <{}>'.format(tot_goals_scored),
            size=13, highlight_textprops=[{'color':team_col}])
    fig_text(0.05, 0.865, 'Number of Goals Conceded: <{}>'.format(tot_goals_conceded),
            size=13, highlight_textprops=[{'color':team_col}])

    fig.text(0.01,0.01, f'Made by Shreyas Khatri/@khatri_shreyas. Data from Understat.com. *Only non-penalty considered.',
            size=10, weight='bold')

    # ADD LEGEND
    ax_leg = fig.add_axes([0.135,0.735,0.33,0.13])
    add_legend(ax_leg, xg_pshot_for, xg_pshot_rank, xg_pshot_against, xg_pshot_a_rank, xg_for_p90, xg_for_rank,
            xg_against_p90, xg_a_rank, team_col, text_col)

    return fig, ax