
# ده كده فنش و ده صفحه ال Recomendation

# from flask import Flask, request, jsonify
# import joblib
# import numpy as np
# import requests
# import logging
# from datetime import datetime
# from collections import defaultdict
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# logging.basicConfig(level=logging.INFO)

# model = joblib.load('random_forest_model.joblib')

# # الترميزات المطلوبة
# crop_type_encoding = {'BANANA': 0, 'SOYABEAN': 1, 'CABBAGE': 2, 'POTATO': 3, 'RICE': 4,
#                       'MELON': 5, 'MAIZE': 6, 'CITRUS': 7, 'BEAN': 8, 'WHEAT': 9,
#                       'MUSTARD': 10, 'COTTON': 11, 'SUGARCANE': 12, 'TOMATO': 13, 'ONION': 14}

# soil_type_encoding = {'DRY': 0, 'WET': 1, 'MOIST': 2}
# region_encoding = {'DESERT': 0, 'SEMI ARID': 1, 'SEMI HUMID': 2, 'HUMID': 3}
# weather_condition_mapping = {
#     'THUNDERSTORM': 'RAINY',
#     'DRIZZLE': 'RAINY',
#     'RAIN': 'RAINY',
#     'SNOW': 'NORMAL',
#     'CLEAR': 'SUNNY',
#     'CLOUDS': 'WINDY',
#     'MIST': 'NORMAL',
#     'SMOKE': 'NORMAL',
#     'HAZE': 'NORMAL',
#     'DUST': 'NORMAL',
#     'FOG': 'NORMAL',
#     'SAND': 'NORMAL',
#     'ASH': 'NORMAL',
#     'SQUALL': 'WINDY',
#     'TORNADO': 'WINDY'
# }

# weather_condition_encoding = {
#     'NORMAL': 0,
#     'SUNNY': 1,
#     'WINDY': 2,
#     'RAINY': 3
# }

# WEATHER_API_KEY = "5e0150a5613f6434ab77f2bfb7d461e0"


# def get_coordinates(city_name):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={WEATHER_API_KEY}"
#         response = requests.get(url)
#         data = response.json()

#         # تحويل كود الاستجابة لسلسلة نصية للتحقق
#         response_code = str(data.get('cod', '200'))

#         if response_code != '200':
#             error_msg = data.get('message', 'City not found').lower()
#             return None, None, error_msg

#         lat = data['city']['coord']['lat']
#         lon = data['city']['coord']['lon']
#         return lat, lon, None

#     except requests.exceptions.RequestException as e:
#         return None, None, f"Connection error: {str(e)}"
#     except Exception as e:
#         return None, None, f"Unexpected error: {str(e)}"


# def get_4day_forecast(lat, lon):
#     try:
#         url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()

#         daily_data = defaultdict(lambda: {'temps': [], 'weather_conditions': []})

#         for entry in data['list']:
#             date_str = entry['dt_txt'].split()[0]
#             weather_main = entry['weather'][0]['main'].upper()
#             daily_data[date_str]['temps'].append(entry['main']['temp'])
#             daily_data[date_str]['weather_conditions'].append(
#                 weather_condition_mapping.get(weather_main, 'NORMAL')
#             )

#         processed = []
#         for date_str in sorted(daily_data.keys())[:4]:
#             day = daily_data[date_str]
#             temp_min = round(min(day['temps']), 1)
#             temp_max = round(max(day['temps']), 1)

#             # تحديد المنطقة المناخية
#             temp_diff = temp_max - temp_min
#             if temp_diff > 15:
#                 region = "DESERT"
#             elif temp_diff > 10:
#                 region = "SEMI ARID"
#             elif temp_diff > 5:
#                 region = "SEMI HUMID"
#             else:
#                 region = "HUMID"

#             # تحديد الحالة الجوية السائدة
#             weather_count = defaultdict(int)
#             for w in day['weather_conditions']:
#                 weather_count[w] += 1
#             main_weather = max(weather_count, key=weather_count.get)

#             processed.append({
#                 'date': datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y"),
#                 'temp_min': temp_min,
#                 'temp_max': temp_max,
#                 'region': region,
#                 'weather_condition': main_weather
#             })

#         return processed
#     except Exception as e:
#         app.logger.error(f"Weather API Error: {str(e)}")
#         raise Exception("فشل في الحصول على توقعات الطقس")


# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()
#         app.logger.info(f"Request received: {data}")

#         # التحقق من البيانات المدخلة
#         required_fields = ['crop_type', 'soil_type']
#         if not data or any(field not in data for field in required_fields):
#             return jsonify({"error": "بيانات الإدخال غير مكتملة"}), 400

#         # معالجة الإحداثيات
#         lat, lon = None, None
#         if data.get('city'):
#             lat, lon, error = get_coordinates(data['city'])
#             if error:
#                 return jsonify({"error": error}), 400
#         else:
#             lat = data.get('latitude')
#             lon = data.get('longitude')

#         if not all([lat, lon]):
#             return jsonify({"error": "خطأ في تحديد الموقع"}), 400

#         # الحصول على توقعات الطقس
#         forecast_data = get_4day_forecast(lat, lon)

#         # توليد التنبؤات
#         predictions = []
#         for day in forecast_data:
#             features = [
#                 crop_type_encoding[data['crop_type']],
#                 soil_type_encoding[data['soil_type']],
#                 region_encoding[day['region']],
#                 weather_condition_encoding.get(day['weather_condition'], 0),
#                 day['temp_max'] - day['temp_min'],
#                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
#             ]

#             water_required = model.predict([features])[0]

#             predictions.append({
#                 'date': day['date'],
#                 'temp_min': day['temp_min'],
#                 'temp_max': day['temp_max'],
#                 'water_required': round(water_required, 1)
#             })

#         return jsonify({'predictions': predictions})

#     except Exception as e:
#         app.logger.error(f"Prediction Error: {str(e)}")
#         return jsonify({"error": "خطأ في معالجة الطلب"}), 500


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


# //////////////////////////////////////////////////////////////////



# ده كده فنش صفحه Water
from flask import Flask, request, jsonify
import joblib
import numpy as np
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load('random_forest_model.joblib')

crop_type_encoding = {
    'BANANA': 0, 'SOYABEAN': 1, 'CABBAGE': 2, 'POTATO': 3, 'RICE': 4,
    'MELON': 5, 'MAIZE': 6, 'CITRUS': 7, 'BEAN': 8, 'WHEAT': 9,
    'MUSTARD': 10, 'COTTON': 11, 'SUGARCANE': 12, 'TOMATO': 13, 'ONION': 14
}
soil_type_encoding = {'DRY': 0, 'WET': 1, 'MOIST': 2}
region_encoding = {'DESERT': 0, 'SEMI ARID': 1, 'SEMI HUMID': 2, 'HUMID': 3}
weather_condition_encoding = {'NORMAL': 0, 'SUNNY': 1, 'WINDY': 2, 'RAINY': 3}

WEATHER_API_KEY = "5e0150a5613f6434ab77f2bfb7d461e0"

def get_location_name(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('name', 'Unknown location')
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

def get_weather_and_region(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        weather_main = data['weather'][0]['main'].upper()
        weather_condition = weather_condition_encoding.get(weather_main, 0)
        
        humidity = data['main']['humidity']
        region = (
            "DESERT" if humidity < 30 else
            "SEMI ARID" if humidity < 50 else
            "SEMI HUMID" if humidity < 70 else
            "HUMID"
        )
        return temp_min, temp_max, weather_condition, region_encoding[region]
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None, None, None, None

def get_coordinates_from_city(city_name):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # تحويل كود الاستجابة لسلسلة نصية للتحقق
        response_code = str(data.get('cod', '200'))
        
        if response_code != '200':
            error_message = data.get('message', 'City not found').lower()
            # ترجمة رسائل الخطأ الشائعة
            error_translations = {
                'city not found': 'المدينة غير موجودة',
                'invalid api key': 'مفتاح API غير صالح',
                'nothing to geocode': 'اسم المدينة فارغ'
            }
            translated_error = error_translations.get(error_message, 'خطأ في اسم المدينة')
            return None, None, {"error": translated_error}
        
        coord = data.get('coord', {})
        lat = coord.get('lat')
        lon = coord.get('lon')
        
        if lat is None or lon is None:
            return None, None, {"error": "بيانات المدينة غير صحيحة"}
        
        return lat, lon, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None, {"error": "فشل في الاتصال بالخادم"}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "لم يتم إرسال أي بيانات"}), 400
            
        city = data.get('city')
        lat = data.get('latitude')
        lon = data.get('longitude')
        crop_type = data.get('crop_type')
        soil_type = data.get('soil_type')
        
        if not crop_type or not soil_type:
            return jsonify({"error": "يجب اختيار نوع المحصول والتربة"}), 400
        
        error_msg = None
        if city:
            lat, lon, error_msg = get_coordinates_from_city(city)
            if error_msg:
                return jsonify(error_msg), 400
            location_name = city
        else:
            if not lat or not lon:
                return jsonify({"error": "الإحداثيات مفقودة"}), 400
            location_name = get_location_name(lat, lon) or "موقع غير معروف"
        
        temp_min, temp_max, weather_condition, region_encoded = get_weather_and_region(lat, lon)
        if None in (temp_min, temp_max, weather_condition, region_encoded):
            return jsonify({"error": "فشل في جلب بيانات الطقس"}), 500
        
        try:
            crop_type_encoded = crop_type_encoding[crop_type.upper()]
            soil_type_encoded = soil_type_encoding[soil_type.upper()]
        except KeyError as e:
            return jsonify({"error": f"اختيار غير صالح: {str(e)}"}), 400
        
        input_features = np.array([[crop_type_encoded, soil_type_encoded, region_encoded, 
                                  weather_condition, temp_min, temp_max, 0, 0, 0, 0, 0, 0, 0]])
        
        prediction = model.predict(input_features)[0]
        
        return jsonify({
            "location": location_name,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "weather_condition": weather_condition,
            "region": region_encoded,
            "water_required": prediction
        })
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "خطأ داخلي في الخادم"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
#  /////////////////////////////////////////////////////////////////////////////