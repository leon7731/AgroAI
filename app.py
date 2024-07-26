
import os
import streamlit as st

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


from Config.Config import settings
from request_func import Get_JWT_Token, Get_Yield_Prediction, Get_Crop_Recommendation, Get_Fertilizer_Recommendation
# Set Local environment variables
os.environ["OPENAI_API_KEY"] = settings.openai_api_key
os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"


# Streamlit app title
st.set_page_config(page_title="Agro AI Dashboard", page_icon="🌾", layout="centered")

# Constants
LOGIN_URL = "http://3.90.230.130/auth/login"
YIELD_PREDICTION_URL = "http://3.90.230.130/yield_prediction/predict"
CROP_RECOMMENDATION_URL = "http://3.90.230.130/crop_recommendation/recommend"
FERTILIZER_RECOMMENDATION_URL = "http://3.90.230.130/fertilizer_recommendation/recommend"


# Initialize session state variables
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = ""
    
    
# Soil color and crop mappings
soil_color_mapping = {
    'Black': 0, 'Red ': 1, 'Medium Brown': 2, 'Dark Brown': 3,
    'Red': 4, 'Light Brown': 5, 'Reddish Brown': 6
}
crop_mapping = {
    'Sugarcane': 0, 'Jowar': 1, 'Cotton': 2, 'Rice': 3, 'Wheat': 4,
    'Groundnut': 5, 'Maize': 6, 'Tur': 7, 'Urad': 8, 'Moong': 9,
    'Gram': 10, 'Masoor': 11, 'Soybean': 12, 'Ginger': 13,
    'Turmeric': 14, 'Grapes': 15
}
# Streamlit login function with dialog
@st.dialog("Login to Agro AI Dashboard")
def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
     
    if st.button("Login"):
        token = Get_JWT_Token(LOGIN_URL, username, password)
        if token:
            st.session_state.current_user = username
            st.session_state.jwt_token = token
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid username or password")
# Main function
def main():
    
    if not (st.session_state.current_user and st.session_state.jwt_token):
        login()
        st.stop()
        
    else:
        st.title("Agro AI Dashboard")
        st.sidebar.title("Options")
        
        option = st.sidebar.radio("Choose an option", ["Yield Prediction", "Crop Recommendation", "Fertilizer Recommendation", "Chat with AgroBot"])
        
        if option == "Yield Prediction":
            st.subheader("Yield Prediction")
            Soil_Quality = st.number_input("Soil Quality", value=93.30)
            Seed_Variety = st.number_input("Seed Variety", min_value=0, max_value=1, value=0)
            Fertilizer_Amount_kg_per_hectare = st.number_input("Fertilizer Amount (kg/ha)", min_value=0.0, value=132.52)
            Sunny_Days = st.number_input("Sunny Days", min_value=0.0, value=96.67)
            Rainfall_mm = st.number_input("Rainfall (mm)", min_value=0.0, value=602.38)
            Irrigation_Schedule = st.number_input("Irrigation Schedule", min_value=0, value=3)
            
            if st.button("Predict Yield"):
                result = Get_Yield_Prediction(YIELD_PREDICTION_URL, st.session_state.jwt_token, Soil_Quality, Seed_Variety, Fertilizer_Amount_kg_per_hectare, Sunny_Days, Rainfall_mm, Irrigation_Schedule)
                st.write(result)
                
        elif option == "Crop Recommendation":
            st.subheader("Crop Recommendation")
            N = st.number_input("Nitrogen (N)", min_value=0.0, value=90.0)
            P = st.number_input("Phosphorus (P)", min_value=0.0, value=42.0)
            K = st.number_input("Potassium (K)", min_value=0.0, value=43.0)
            temperature = st.number_input("Temperature", min_value=0.0, value=20.87)
            humidity = st.number_input("Humidity", min_value=0.0, value=82.00)
            ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5)
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=202.93)
            
            if st.button("Recommend Crop"):
                result = Get_Crop_Recommendation(CROP_RECOMMENDATION_URL, st.session_state.jwt_token, N, P, K, temperature, humidity, ph, rainfall)
                st.write(result)
                
        elif option == "Fertilizer Recommendation":
            st.subheader("Fertilizer Recommendation")
            soil_color_name = st.selectbox("Soil Color", list(soil_color_mapping.keys()))
            Soil_color = soil_color_mapping[soil_color_name]
            Nitrogen = st.number_input("Nitrogen", min_value=0.0, value=75.0)
            Phosphorus = st.number_input("Phosphorus", min_value=0.0, value=50.0)
            Potassium = st.number_input("Potassium", min_value=0.0, value=100.0)
            pH = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5)
            Rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=1000.0)
            Temperature = st.number_input("Temperature", min_value=0.0, value=20.0)
            crop_name = st.selectbox("Crop", list(crop_mapping.keys()))
            Crop = crop_mapping[crop_name]
            
            if st.button("Recommend Fertilizer"):
                result = Get_Fertilizer_Recommendation(FERTILIZER_RECOMMENDATION_URL, st.session_state.jwt_token, Soil_color, Nitrogen, Phosphorus, Potassium, pH, Rainfall, Temperature, Crop)
                st.write(result)
                
        elif option == "Chat with AgroBot":
            st.subheader("Chat with AgroBot")
            
            # Initialize the vector store and retrieval chain
            db = Chroma(
                embedding_function=OpenAIEmbeddings(),
                persist_directory="./farming_knowledge_vector_db"
            )
            
            llm = ChatOpenAI(model="gpt-4o", temperature=0)
            
            prompt = ChatPromptTemplate.from_template("""
            Persona:
            An experienced agricultural advisor who specializes in integrating advanced technology into farming practices.
            
            Context:
            The user is a farmer seeking to enhance crop yield and sustainability through modern agricultural technologies. 
            They need advice on using data analytics and smart farming techniques to optimize their operations. 
            The advisor should provide comprehensive guidance, explaining the benefits of these technologies, how to implement them, 
            and the long-term advantages. The advice should be detailed, covering the use of IoT devices, precision farming, satellite imagery, drones, and relevant software platforms. 
            The goal is to help the farmer transition to technology-driven practices, improving productivity and sustainability.
            
            Voice:
            Authoritative and knowledgeable
            
            Tone:
            Supportive and encouraging
            
            Style:
            Detailed and informative
            
            As an agricultural advisor specializing in modern farming technologies, your goal is to provide comprehensive guidance to farmers seeking to 
            improve their crop yield and sustainability. This includes integrating advanced tools and methods such as data analytics, IoT devices, and precision farming techniques.
            Begin by understanding the farmer's current practices and the specific crops they are cultivating. Gather information about their soil conditions,
            climate, and existing equipment. This context will help tailor your advice to their unique situation.
            Explain the benefits of adopting smart farming technologies. Discuss how IoT devices can monitor soil moisture, temperature, and humidity in real-time, 
            providing valuable data for making informed decisions. Highlight the importance of data analytics in predicting crop diseases, optimizing irrigation schedules, and improving overall crop health.
            Provide detailed steps for implementing these technologies. Start with the basics of setting up sensors in the field, connecting them to a centralized 
            data platform, and interpreting the collected data. Emphasize the importance of regular monitoring and maintenance of these devices to ensure accurate data collection.
            Illustrate the concept of precision farming, where inputs like water, fertilizers, and pesticides are applied in precise amounts based on the specific needs 
            of each crop section. Describe how satellite imagery and drones can assist in monitoring crop health and identifying areas that require attention.
            Offer recommendations on software platforms that can aggregate and analyze farm data, providing actionable insights. Suggest training or workshops for the 
            farmer and their team to get acquainted with these new technologies.
            Finally, emphasize the long-term benefits of adopting these advanced farming techniques, such as increased yield, reduced costs, and improved sustainability. 
            Encourage the farmer to start small, experiment with different technologies, and gradually scale up their operations as they become more comfortable with the new methods.
            By providing a comprehensive and tailored approach, you can help the farmer successfully transition to modern, technology-driven agricultural practices, leading to enhanced 
            productivity and sustainability.      
            
            <context>
            {context}
            </context>
            Question: {input}
            """)
            
            from langchain_core.runnables import RunnablePassthrough
            chain = (
                {"context": db.as_retriever(), "input": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            # Display chat messages from history on app rerun
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Enter your question:"):
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)

                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Get response
                response_content = chain.invoke(prompt)

                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response_content)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()
