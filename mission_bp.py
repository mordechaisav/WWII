from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from models.model import Mission  # נניח שהמודל מיובא ממקום מתאים
from ייייי import result

# יצירת הבלופרינט עבור המשימות
missions_bp = Blueprint('missions_bp', __name__)

@missions_bp.route('/missions', methods=['GET'])
def get_mission():
    result = Mission.query.limit(100).all()
    if len(result) == 0:
        return jsonify({"result": f"Target table is empty"}), 200
    return jsonify({"result": [target.to_dict() for target in result]}), 200


@missions_bp.route('/missions/<int:id>', methods=['GET'])
def get_mission_by_id(id):
    result = Mission.query.get(id)
    if not result:
        return jsonify({"result": f"No mission found with ID: {id}"}), 404
    return jsonify({"result": result.to_dict()}), 200


