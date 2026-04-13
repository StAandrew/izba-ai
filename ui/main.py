import requests
import streamlit as st
import babel.numbers
import decimal

URL = "http://127.0.0.1:8080/"

st.title("Izba AI")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("You: ","")

if st.button("Send"):
    if user_input:
        # Append user input to chat history
        st.session_state['chat_history'].append({"role": "user", "content": user_input, "type": "user"})

        orchestrator_response = requests.get(URL+f"/orchestrator/{user_input}").json()["llm_response"]
        if orchestrator_response == "out-of-scope":
            st.session_state['chat_history'].append({"role": "assistant", "content": "Unfortunately, I'm not currently capable of answering this question. Do you have any other questions about UK properties?"})    
        elif orchestrator_response.split("/")[0] == "current_listings":
            current_listings_data_response = requests.get(URL+f"current_listings/{user_input}").json()
            images = []
            properties = current_listings_data_response["return_data"]
            for property in properties:
                images.append(property['image1_url'])
            st.session_state['chat_history'].append({"role": "assistant", "content": current_listings_data_response["return_str"], "type": "current_listings", "properties": properties, "images": images})
        else:
            llm_response = requests.get(URL+f"/llama_index_agent/{user_input}").json()["llm_response"]
            st.session_state['chat_history'].append({"role": "assistant", "content": llm_response, "type": "llm_agent"})

# Display chat history
for chat in st.session_state['chat_history']:
    if chat['role'] == 'user':
        st.markdown(f"<span style='color:green'>You</span>: {chat['content']}", unsafe_allow_html=True)
    else:
        if chat["type"] == "llm_agent":
            st.markdown(f"<span style='color:red'>Domovenok</span>: {chat['content']}", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red'>Domovenok</span>:", unsafe_allow_html=True)
            properties = chat["properties"]
            for property in properties:
                with st.container():
                    cols = st.columns(2)
                    with cols[0]:
                        # Display property image
                        st.image(property['image1_url'], width=350)
                    with cols[1]:
                        # Display property details
                        st.subheader(f"{property['title']}")
                        st.write(f"**Price**: {babel.numbers.format_currency(decimal.Decimal(property['price']), 'GBP')}")
                        st.write(f"**Bedrooms**: {property['number_of_bedrooms']} | **Bathrooms**: {property['number_of_bathrooms']}")
                        st.write(f"**Address**: {property['address']}")
                        st.write(f"**Postcode**: {property['postcode']}")

            # st.image(chat["images"][-1], width=350)