from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/stats')
def stats():
    # Placeholder: Replace with real analytics
    return jsonify({
        'vehicle_counts': {'lane_1': 12, 'lane_2': 19, 'lane_3': 7},
        'average_speeds': {'lane_1': 45, 'lane_2': 38, 'lane_3': 52},
        'heatmap': [[0,1,2],[2,3,1],[1,0,4]]
    })
