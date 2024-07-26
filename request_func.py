
import requests

def Get_JWT_Token(URL, Username, Password):
    """_summary_: Get JWT Token from the API

    Args:
        URL (_type_): URL of the API
        Username (_type_): Username to login
        Password (_type_): Password to login

    Returns:
        _type_: JWT Token
    """
    
    params = {"username": Username,
              "password": Password}
    
    login_request = requests.post(URL, data=params)
    print(login_request)
    
    
    login_request_json = login_request.json()
    jwt_token = login_request_json['access_token']
    
    return jwt_token


### Yield Prediction ###
def Get_Yield_Prediction(URL, 
                         JWT_Token, 
                         Soil_Quality, 
                         Seed_Variety,
                         Fertilizer_Amount_kg_per_hectare,
                         Sunny_Days,
                         Rainfall_mm,
                         Irrigation_Schedule
                         ):
        
    headers = {"Authorization": f"Bearer {JWT_Token}" }
    
    params = {
        "Soil_Quality": Soil_Quality,
        "Seed_Variety": Seed_Variety,
        "Fertilizer_Amount_kg_per_hectare": Fertilizer_Amount_kg_per_hectare,
        "Sunny_Days": Sunny_Days,
        "Rainfall_mm": Rainfall_mm,
        "Irrigation_Schedule": Irrigation_Schedule
    }

    yield_prediction_request = requests.post(URL, headers=headers, json=params)
    
    
    yield_prediction = yield_prediction_request.json()
    
    return yield_prediction



### Crop Recommendation ###
def Get_Crop_Recommendation(URL, 
                            JWT_Token,
                            N,
                            P,
                            K,
                            temperature,
                            humidity,
                            ph,
                            rainfall):
    
    headers = {"Authorization": f"Bearer {JWT_Token}" }
    
    params = {
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }    
    
    get_crop_recommendation_request = requests.post(URL, headers=headers, json=params)
    
    crop_recommendation = get_crop_recommendation_request.json()
    
    return crop_recommendation
    


### Fertilizer Recommendation ###
def Get_Fertilizer_Recommendation(URL, 
                                  JWT_Token,
                                  Soil_color,
                                  Nitrogen,
                                  Phosphorus,
                                  Potassium,
                                  pH,
                                  Rainfall,
                                  Temperature,
                                  Crop):
    
    headers = {"Authorization": f"Bearer {JWT_Token}" }
    
    params = {
        "Soil_color": Soil_color,
        "Nitrogen": Nitrogen,
        "Phosphorus": Phosphorus,
        "Potassium": Potassium,
        "pH": pH,
        "Rainfall": Rainfall,
        "Temperature": Temperature,
        "Crop": Crop
    }    
    
    get_fertilizer_recommendation_request = requests.post(URL, headers=headers, json=params)
    
    fertilizer_recommendation = get_fertilizer_recommendation_request.json()
    
    return fertilizer_recommendation




