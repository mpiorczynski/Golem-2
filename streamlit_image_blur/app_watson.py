import streamlit as st
import watson_utils  

    
def app():
    st.markdown('## Watson')
    st.write('\n')

    uploaded_file = st.file_uploader("Choose a file", type=['mp3'])

    if uploaded_file is not None:
        with st.spinner('Wait for it...'):
            # filename = 'recording.mp3'
            # with open(filename, 'wb') as f:
            #     f.write(uploaded_file.getbuffer())
            prediction = watson_utils.get_prediction('p13.mp3')
            st.write(prediction)
