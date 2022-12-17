import streamlit as st
import io
import requests

from streamlit_extras.badges import badge
from PIL import Image

def main():
    col1, col2, col3 = st.columns([0.0675, 0.27, 0.035])
    
    with col1:
        url = 'https://github.com/tsu2000/aqw_guides/raw/main/images/aqw.png'
        response = requests.get(url)
        img = Image.open(io.BytesIO(response.content))
        st.image(img, output_format = 'png')

    with col2:
        st.title('AQWorlds Stats Guides')

    with col3:
        badge(type = 'github', name = 'tsu2000/aqw_guides', url = 'https://github.com/tsu2000/aqw_guides')

    st.markdown('### Statistics-Based Web Apps for AdventureQuest Worlds')
    st.markdown('Welcome to the new homepage for all Streamlit-based web applications centered around statistics in AdventureQuest Worlds! To start using a feature, navigate to the sidebar on the left.')

    st.markdown('---')

    st.markdown('#### Current Web Apps:')

    st.markdown('These are the guides the application currently offers:')
    st.markdown('- **Drop Rate Guide**: Allows users to visualise in-game drop rate mechanics and the probabiity distribution of drops in AQWorlds.')
    st.markdown('- **Reputation Guide**: Allows users to view their in-game reputation statistics and track their reputation progress.')
    st.markdown('- **Void Aura Guide**: Allows users to estimate the total time required to reach 7,500 Void Auras.')

    st.markdown('---')

    st.markdown('***Disclaimer**: This application is not affiliated with AdventureQuest Worlds or Artix Entertainment in any way, shape or form. Information in this app may be subject to change and inaccurate. Please visit the [**AQWorlds Wiki**](http://aqwwiki.wikidot.com) for the latest in-game information on AdventureQuest Worlds.*')

if __name__ == "__main__":
    st.set_page_config(page_title = 'AQWorlds Stats Guides', page_icon = '📊')
    main()