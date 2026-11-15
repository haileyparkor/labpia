from flask import Blueprint

qr_bp = Blueprint("qr", __name__, url_prefix="/admin/qr")
qr_public_bp = Blueprint("qr_public", __name__)


@qr_bp.route("/label/<int:supply_id>")
def label(supply_id):
    return f"QR 라벨 준비 중입니다: {supply_id}"


@qr_bp.route("/tags/link", methods=["GET", "POST"])
def link_tag():
    return "태그 연결 준비 중입니다."


@qr_public_bp.route("/scan")
def scan():
    return "스캔 준비 중입니다."


@qr_public_bp.route("/q/<token>")
def resolve(token):
    return f"QR 조회 준비 중입니다: {token}"
