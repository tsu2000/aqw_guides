import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import seaborn as sns


def main():
    st.title('AQWorlds Void Aura Guide')
    st.markdown('### Void Aura Statistics in AQWorlds')

    st.markdown("This web app shows the data visualisation for the **approximate** number of days required to obtain **7,500** Void Auras for the Necrotic Sword of Doom in AdventureQuest Worlds, using the quests **_'Retrieve Void Auras'_**, **_'Gathering Unstable Essences'_**, or **_'Commanding Shadow Essences'_**, and based on the user's following inputs:")
    st.markdown('- Current number of Void Auras')
    st.markdown('- Number of Quests to be completed per day')
    st.markdown("- Whether the Daily Quest **_'The Encroaching Shadows (Daily)'_**,  **_'Glimpse Into The Dark (Daily)'_** or both quests are completed every day")

    topics = ['Void Aura Days Estimator', 
              'FAQ']

    topic = st.selectbox('Select a topic: ', topics)

    st.markdown('---')

    if topic == topics[0]:
        analysis()
    elif topic == topics[1]:
        faq()


def analysis():
    st.markdown('### User Inputs:')
    st.markdown('\n')
    # Code to read user's inputs
    current = st.number_input('Choose the amount of Void Auras you currently have:', min_value = 0, max_value = 7499, 
                        value = 500, step = 1)

    quests_per_day = st.number_input("Enter the number of times you aim to complete the quest 'Retrieve Void Auras', 'Gathering Unstable Essences', or 'Commanding Shadow Essences' per day:", min_value = 1, max_value = 500, value = 5, step = 1)

    dq_options = ['The Encroaching Shadows (Daily) - [Non-Member]', 'Glimpse Into The Dark (Daily) - [Member Only]', 'Both Daily Quests', 'None']
    dq_choice = st.selectbox('Which Daily Quest do you plan to do every day?', dq_options)

    # Define a function to return the mean number of Void Auras from a sample of n, depending on whether there is a Void Aura boost
    def mean_aura(n, boost_status):

        aura_list = []
        if boost_status == True:
            for i in range(0, n):
                x = np.random.choice(np.array([5, 10, 20]), p = [1/3, 1/3, 1/3])
                aura_list.append(x)

        elif boost_status == False:
            for i in range(0, n):
                x = np.random.choice(np.array([5, 6, 7]), p = [1/3, 1/3, 1/3])
                aura_list.append(x)

        return np.mean(aura_list)

    amt_req = 7500
    amt_farm = amt_req - current

    st.markdown('There are **{}** Void Auras left to obtain before reaching the target of **7500** Void Auras.'.format(int(amt_farm)))

    plot_graph = st.button('View Plot')
    st.markdown('---')

    # Simulation of the mean number of auras among 10 quest turn-ins with a sample size of n = 100
    x_ord = np.array([mean_aura(10, False) for i in range(0, 100)])
    y_ord = np.ceil(amt_farm / x_ord)

    x_boost = np.array([mean_aura(10, True) for i in range(0, 100)])
    y_boost = np.ceil(amt_farm / x_boost)

    # Obtaining values used for the KDE Plots
    if dq_choice == dq_options[0]:
        exp_days_ord = amt_farm / ((quests_per_day *  x_ord) + 50)
        exp_days_boost = amt_farm / ((quests_per_day * x_boost) + 50)
        
    elif dq_choice == dq_options[1]:
        exp_days_ord = amt_farm / ((quests_per_day *  x_ord) + 100)
        exp_days_boost = amt_farm / ((quests_per_day * x_boost) + 100)

    elif dq_choice == dq_options[2]:
        exp_days_ord = amt_farm / ((quests_per_day *  x_ord) + 150)
        exp_days_boost = amt_farm / ((quests_per_day * x_boost) + 150)

    elif dq_choice == dq_options[3]:
        exp_days_ord = amt_farm / (quests_per_day *  x_ord)
        exp_days_boost = amt_farm / (quests_per_day * x_boost)
        
    st.markdown('### Data Visualisation')

    # Plotting the 2 graphs: With and without Void Aura Boosts
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize = (12, 10), dpi = 300)

    ax = sns.kdeplot(data = exp_days_ord, label = 'Without Void Aura Boost', color = 'red')
    ax2 = sns.kdeplot(data = exp_days_boost, label = 'With Void Aura Boost', color = 'blue')

    plt.title(f'Expected number of days to reach 7500 Void Auras from {current} Void Auras', fontsize = 18)
    plt.xlabel('Estimated number of days to reach goal', fontsize = 15, labelpad = 10)
    plt.ylabel('Probability Density Function (PDF)', fontsize = 15, labelpad = 10) 

    # Obtain x and y values of maximum points to plot the expected number of days
    data_x, data_y = ax.lines[0].get_data()
    xi = np.median(exp_days_ord)
    yi = np.interp(xi, data_x, data_y)
    plt.plot(xi, yi, marker = 'o', color = 'black')

    data_x2, data_y2 = ax2.lines[1].get_data()
    xi2 = np.median(exp_days_boost)
    yi2 = np.interp(xi2, data_x2, data_y2)
    plt.plot(xi2, yi2, marker = 'o', color = 'black')

    # Labelling maximum points
    plt.text(xi, yi, '~ {} day(s)'.format(int(np.ceil(xi))), fontsize = 15, color = 'r', ha = 'left', va = 'bottom')
    plt.text(xi2, yi2, '~ {} day(s)'.format(int(np.ceil(xi2))), fontsize = 15, color = 'b', ha = 'left', va = 'bottom')

    # Adjusting Plot Legend
    legend = plt.legend(loc = 'upper left', frameon = 1, framealpha = 1, fontsize = 15)
    frame = legend.get_frame()
    frame.set_facecolor('lightcyan')
    frame.set_edgecolor('black')

    if plot_graph:
        st.pyplot(fig)
    else:
        st.markdown('Click the *View Plot* button to view the visualisation for the approximate number of days to reach 7,500 Void Auras.')

    # Statistical Summary
    st.markdown('---')
    st.markdown('### Statistical Summary')

    st.markdown('#### Without Void Aura Boost')
    st.markdown('Expected Number of Days: **{}**'.format(int(np.ceil(xi))))
    st.markdown('Standard Deviation: **{}**'.format(round(np.std(exp_days_ord), 3)))
    st.markdown(f'Range of possible days to complete all quests: **[{round(np.min(exp_days_ord), 2)}, {round(np.max(exp_days_ord), 2)}]**')

    st.markdown('#### With Void Aura Boost')
    st.markdown('Expected Number of Days: **{}**'.format(int(np.ceil(xi2))))
    st.markdown('Standard Deviation: **{}**'.format(round(np.std(exp_days_boost), 3)))
    st.markdown(f'Range of possible days to complete all quests: **[{round(np.min(exp_days_boost), 2)}, {round(np.max(exp_days_boost), 2)}]**')

    dif = int(np.ceil(xi)) - int(np.ceil(xi2))

    st.markdown('#### Time saved by obtaining Void Auras during a boost')
    st.markdown('Number of days saved: {}'.format(dif))
    st.markdown('Time spent farming reduced by **{}%**'.format(round(dif/int(np.ceil(xi))*100, 2)))
    st.markdown('---')

def faq():                                                                                                     
    st.markdown('## Frequently Asked Questions (FAQ):')

    st.markdown('**What does the vertical axis measure?**')
    st.markdown('- It measures the probability of obtaining all the necessary resources within a certain amount of days. A higher y-value means that there is a greater probability of reaching 7,500 Void Auras on the number of expected days.')

    st.markdown('**What does the horizontal axis measure?**')
    st.markdown('- It measures the days it will take to obtain all the necessary resources. A graph with a wider range indicates that there is a greater possible range of days that it may take to obtain all the necessary resources.') 
            
    st.markdown('**How did you create this simulation?**')
    st.markdown('- I simulated the completion of the basic quest (which gave 5/6/7 Void Auras each time) 10 times and took the mean. Then I repeated this until I had a sample size of 100, and then I found the average number of days for each of those 100 instances before grouping the data into kernel density estimate **(KDE)** plots to visualise the distribution of observations in my dataset. I repeat this twice, once for normal rates and once during a Void Aura Boost (5/10/20).')
                                                                                                        
    st.markdown('---')

if __name__ == "__main__":
    main()