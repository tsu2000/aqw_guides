import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import math


def main():
    st.title('AQWorlds Reputation Guide')
    st.markdown('### Reputation Statistics in AQWorlds')
    
    st.markdown('This web app aims to be a resource for understanding how reputation works in the MMORPG, AdventureQuest Worlds. Users can input their rank, current amount of reputation, as well as any rep-boosting items to determine the required amount of quest repetition to reach the in-game maximum reputation rank.')
    st.markdown('Players may also view an in-depth visualisation of the reputation system in AQWorlds by selecting the other box from the banner below.')
    
    topics = ['Reputation Progress & Quest Requirement Calculator', 
              'Reputation in AQWorlds: A Comprehensive Visualisation']

    topic = st.selectbox('Select a topic: ', topics)

    if topic == topics[0]:
        calc()
    elif topic == topics[1]:
        desc()
    
    
def calc():
    st.markdown('---')
    st.markdown('## Reputation Progress Calculator')
     
    st.markdown('Select the rank and the current amount of reputation you currently have for that rank: ')
    
    # Dictionaries for each rep rank for rep required to reach next rank
    rep_rank = {1: 900,
                2: 2700, 
                3: 6400,
                4: 12500,
                5: 21600,
                6: 34300,
                7: 51200,
                8: 72900,
                9: 100000}

    # Calculates the reputation up to previous rank confirmed to have been earned
    def rank_rec(num):
        if num == 1:
            return 0
        else:
            return rep_rank[num - 1] + rank_rec(num - 1)
    
    # User input
    rank = st.number_input('Input current rank: ', min_value = 1, max_value = 9, value = 6, step = 1)
    rep = st.number_input('Input current rep: ', min_value = 0, max_value = rep_rank[rank] - 1, value = 100, step = 1)
    
    # Calculating percentage completion
    total_rep = rank_rec(rank) + rep
    
    rep_left = sum(rep_rank.values()) - total_rep

    rep_percent = total_rep / sum(rep_rank.values())*100
    
    quest_series = pd.Series(index = ['Percent completed', 'Percent left'], data = [rep_percent, 100 - rep_percent])
    
    def progress_bar():
        plt.style.use('default')
        fig, ax = plt.subplots(figsize = (12, 1), dpi = 300)

        # Plotting (1st argument is y-value, so any value can be used as long as they are both the same) 
        b1 = plt.barh(1, quest_series[0], color = 'green', alpha = 0.7, height = 0.3)
        b2 = plt.barh(1, quest_series[1], left = quest_series[0], color = 'red', alpha = 0.7, height = 0.3)

        plt.legend([b1, b2], 
                   quest_series.index,
                   ncol = 2,
                   loc = 'lower left', 
                   bbox_to_anchor = (0.33, -1.1))

        plt.xlim(0, 100)
        plt.xticks(np.arange(0, 101, 10))
        
        # Formatting text in horizontal bar
        fmt = '%.2f%%'
        fontweight = 'bold'
        remove_percent = 2.5
        
        # Formatting bar labels and percentages
        if quest_series[0] < remove_percent:
            ax.bar_label(b2, label_type = 'center', fmt = fmt, fontweight = fontweight)

        elif quest_series[1] < remove_percent:
            ax.bar_label(b1, label_type = 'center', fmt = fmt, fontweight = fontweight)

        else:
            ax.bar_label(b1, label_type = 'center', fmt = fmt, fontweight = fontweight)
            ax.bar_label(b2, label_type = 'center', fmt = fmt, fontweight = fontweight)

        # Removing x-axis
        frame1 = plt.gca()
        frame1.axes.get_yaxis().set_visible(False)

        return st.pyplot(fig)
    
    st.subheader('Rate of Completion')
    progress_bar()
    
    st.markdown(f'You are **{round(rep_percent, 2)}%** of the way to reaching the maximum rep rank.')
    st.markdown(f'There is still **{round(100 - rep_percent, 2)}%** to go before reaching the maximum rep rank.')
    
    # Creating table of results
    def progress_table():
        rep_dict = {'Reputation Points': [round(total_rep, 0), round(rep_left, 0)],
                    'Percentage (%)': list(quest_series)}
        rep_df = pd.DataFrame(index = ['Rep amount completed', 'Rep amount left'], data = rep_dict)

        # Adjust formatting of cells
        rep_df['Reputation Points'] = rep_df['Reputation Points'].astype(int)
        bold_headers = [f'<b>{item}<b>' for item in (['Total Rep Amount'] + list(rep_df.columns))]
        
        # Create figure
        fig = go.Figure(data = [go.Table(columnwidth = [1, 1, 1],
                                         
                                         header = dict(values = bold_headers,
                                                       fill_color = 'paleturquoise',
                                                       line_color = 'darkslategray',
                                                       align = 'center',
                                                       font = dict(color = 'black', 
                                                                   size = 14, 
                                                                   family = 'Georgia')),
                           
                                         cells = dict(values = [rep_df.index,
                                                                rep_df['Reputation Points'],
                                                                rep_df['Percentage (%)']], 
                                                      fill_color = 'lavender',
                                                      line_color = 'darkslategray',
                                                      align = ['left', 'center'],
                                                      font = dict(color = ['black'], 
                                                                  size = [14, 14], 
                                                                  family = 'Georgia'),
                                                      height = 25,
                                                      format = ['', ',', ',.2f']))])
        
        fig.update_layout(height = 95, width = 700, margin = dict(l = 5, r = 5, t = 5, b = 5))
        return st.plotly_chart(fig, use_container_width = True)
    
    st.subheader('Table of Results')
    progress_table()
    
    st.markdown(f'You are currently at **Rank {int(rank)}** out of 10.')
    st.markdown('You have earned **{:,}** reputation point(s) so far.'.format(int(total_rep)))
    st.markdown('There are **{:,}** reputation point(s) left to reach the maximum rank.'.format(int(rep_left)))
    
    # Quest Section
    st.markdown('---')
    st.markdown('## Quest Requirement Calculator')
    
    st.markdown('This is a continuation of the first section where you can see how many times you would have to repeat the same quest(s) in order to reach a particular rank in a reputation faction, using data that was entered in the previous reputation progress section.')
    
    # User input
    st.subheader('Quest Reputation')
    quest_rep = st.number_input('Input reputation points provided by quest(s) you plan to repeat: ', 
                           min_value = 1, max_value = 50000, value = 400, step = 1)
    
    st.subheader('Rep-boosting inputs')   
    item_boost = st.number_input('Input the reputation percentage increase from rep-boosting items (in %): ', 
                          min_value = 0, max_value = 100, value = 0, step = 1)
    
    rep_boost = st.selectbox('Are you using a reputation boost right now?', ['No', 'Yes'])
    
    server_boost = st.selectbox('Is there a server boost going on right now?', ['No', 'Yes (2x)', 'Yes (3x)'])
    
    # Boolean checking for rep boost and server boost
    if rep_boost == 'Yes':
        rep_boost = True
    else:
        rep_boost = False
        
    if server_boost == 'Yes (2x)':
        server_boost = 2
    elif server_boost == 'Yes (3x)':
        server_boost = 3
    else:
        server_boost = 1

    quest_rep = quest_rep * (1 + item_boost / 100)
    quest_rep = quest_rep * (1 + rep_boost)
    quest_rep = quest_rep * (server_boost)

    total_quests = math.ceil(rep_left / quest_rep)
    
    if st.button('Calculate'):    
        def quest_table():
            
            # Create table to see amount of quests to reach particular rank
            rq_dict = {}
            for i in range(2, 11):
                if rank_rec(i) > total_rep:
                    rq_dict.update({f'Rank {i}': rank_rec(i) - total_rep})
                else:
                    continue
                    
            q_klist = list(rq_dict.keys())       
            q_vlist = list(rq_dict.values())
            quest_array = np.ceil(np.array(list(rq_dict.values())) / quest_rep)

            fig = go.Figure(data = [go.Table(columnwidth = [1, 1, 1],

                                                     header = dict(values = ['To reach:', 
                                                                             'Rep required',
                                                                             'No. of Quests required'],
                                                                   fill_color = 'lightcoral',
                                                                   line_color = 'darkslategray',
                                                                   align = 'center',
                                                                   font = dict(color = 'black', 
                                                                               size = 14, 
                                                                               family = 'Georgia')),

                                                     cells = dict(values = [q_klist, q_vlist, quest_array], 
                                                                  fill_color = 'wheat',
                                                                  line_color = 'darkslategray',
                                                                  align = ['left', 'center'],
                                                                  font = dict(color = ['black'], 
                                                                              size = [14, 14], 
                                                                              family = 'Georgia'),
                                                                  height = 25,
                                                                  format = ['', ',', ',']))]) 
            fig.update_layout(height = 300, width = 700, margin = dict(l = 5, r = 5, t = 5, b = 5))
            return st.plotly_chart(fig, use_container_width = True)
        
        st.subheader('Results')
        quest_table()
        
        st.subheader('Result Summary')
        st.markdown(f'One quest completion gives **{int(quest_rep)}** rep after accounting for all possible boosts.')
        st.markdown(f'You need to complete the same quest **{total_quests}** time(s) to reach Rank 10.')
        
    st.markdown('---')

        
def desc():
    st.markdown('---')
    st.markdown('## Reputation in AQWorlds: A Comprehensive Visualisation')
    st.markdown('Reputation in AdventureQuest Worlds consitutes a total of 10 ranks, with each rank requiring an increasing amount of reputation to reach the next rank. This aims to be a visual guide to the reputation required to reach rank 10 for anyone interested.')
    
    # Required calculations
    rep_rank = {1: 900,
                2: 2700, 
                3: 6400,
                4: 12500,
                5: 21600,
                6: 34300,
                7: 51200,
                8: 72900,
                9: 100000}
    
    rep_comp = {i: rep_rank[i] / sum(rep_rank.values()) * 100 for i in rep_rank.keys()}
    
    def rank_cum_percent(num):
        if num == 1:
            return rep_comp[num]
        else:
            return rep_comp[num] + rank_cum_percent(num - 1)
        
    rep_cum_comp = {'Rank 1': 0.0}
    rep_cum_comp.update({f'Rank {i + 1}': rank_cum_percent(i) for i in rep_comp})
    rep_cum_comp.update({'Rank 10': 100.0})    
    
    # Obtain plots
    def original_plot():
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)

        plt.bar(rep_rank.keys(), rep_rank.values(), color = 'g', alpha = 0.65)
        ax.bar_label(ax.containers[0])

        plt.xticks(ticks = list(rep_rank.keys()), 
                   labels = [f'Rank {num} - {num + 1}' for num in list(rep_rank.keys())])

        plt.title('Amount of Reputation to get from each rep rank to the next', fontsize = 15)
        plt.ylabel('Reputation Points', fontsize = 15, labelpad = 10)
        plt.xlabel('Rank Increments', fontsize = 15, labelpad = 10)
        return st.pyplot(fig)

    def percent_plot():
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)

        plt.bar(rep_comp.keys(), rep_comp.values(), color = 'b', alpha = 0.5)
        ax.bar_label(ax.containers[0], fmt = '%.2f%%')

        plt.xticks(ticks = list(rep_comp.keys()), 
                   labels = [f'Rank {num} - {num + 1}' for num in list(rep_comp.keys())])

        plt.title('Percentage of total rep contained in each rank increment', fontsize = 15)
        plt.ylabel('Percentage', fontsize = 15, labelpad = 10)
        plt.xlabel('Rank Increments', fontsize = 15, labelpad = 10)
        return st.pyplot(fig)
    
    def cumulative_plot():
        plt.style.use('seaborn-whitegrid')
        fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)

        plt.plot(rep_cum_comp.keys(), rep_cum_comp.values(), color = 'orange', alpha = 0.75, marker = 'X')

        plt.xticks(ticks = list(rep_cum_comp.keys()))

        for x, y in zip(rep_cum_comp.keys(), rep_cum_comp.values()):
            label = f'{round(y, 2)}%'
            plt.annotate(label, (x, y), xycoords = 'data', textcoords = 'offset points', 
                         xytext = (0, 5), ha = 'center', fontsize = 10)

        plt.title('Cumulative Percentage of total rep earned at end of each rank', fontsize = 15)
        plt.ylabel('Cumulative Percentage', fontsize = 15, labelpad = 10)
        plt.xlabel('% of total rep earned at start of:', fontsize = 15, labelpad = 10)
        return st.pyplot(fig)
    
    # User view
    st.markdown('### Quick View: Basic graph')
    st.markdown('This graph shows the raw amount of reputation required to reach the next rank, based on in-game data. From the graph it is clear that the bulk of the reputation required increases at an increasing rate.')
    original_plot()
    
    st.markdown('### Quick View: Basic graph with percentages')
    st.markdown('This shows a more comprehsive view of the reputation required to reach Rank 10 in a reputation as it shows the percentage that the transition between each rank up takes up compared to the total amount of reputation required. From the graph we can observe that the reputation gained from Ranks 1 to 7 is less than half of the total reputation required to reach rank 10, with the reputation gained from Ranks 8 to 10 having the bulk of the reputation required to reach the maximum rank.')
    percent_plot()
    
    st.markdown('### Cumulative percentage of reputation')
    st.markdown('Finally, this shows the cumulative percentage of rep earned at the start of each rank. For example, the point for Rank 4 on this graph will include the reputations earned from only Ranks 1 to 3 as a percentage of the total reputation required to reach Rank 10. This graph really puts the grind for reputation into perspective, as it shows the median (or 50%) of all total reputation required to reach Rank 10 in between Ranks 8 and 9. We can hence conclude that farming reputation to Rank 10 in AQWorlds gets exponentially more time-consuming as the reputation rank increases.')
    cumulative_plot()
        
    st.markdown('*All reputation information, calculations are graphs may be subject to future changes. This website may have not been updated to the latest information about reputation in-game.*')
    
    st.markdown('For a more in-depth and comprehensive guide to farming different reputation factions in AQWorlds efficiently, see the following source below (May contain outdated information):')
    st.markdown('- [**Battleon Forums - Reputation Farming Guide for AdventureQuest Worlds**](https://forums2.battleon.com/f/tm.asp?m=22078977)')

    st.markdown('---')
    

if __name__ == "__main__":
    main()