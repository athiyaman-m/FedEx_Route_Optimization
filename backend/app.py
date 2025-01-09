from flask import Flask, request, jsonify
from utils import get_traffic_data, get_weather_data, get_route
from models import db, Route

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/routes.db'
db.init_app(app)

@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    start = data['start']
    end = data['end']
    vehicle = data['vehicle']

    # Fetch data
    route = get_route(start, end)
    traffic = get_traffic_data(start, end)
    weather = get_weather_data(route['geometry']['coordinates'][0])

    # Emissions calculation
    distance_km = route['distance'] / 1000
    emission_factor = vehicle['emission_factor']
    emissions = distance_km * emission_factor

    # Store in DB
    new_route = Route(
        start=start, end=end, distance_km=distance_km,
        emissions=emissions, traffic=traffic, weather=weather
    )
    db.session.add(new_route)
    db.session.commit()

    return jsonify({
        "route": route,
        "traffic": traffic,
        "weather": weather,
        "emissions": emissions
    })

if __name__ == '__main__':
    app.run(debug=True)
