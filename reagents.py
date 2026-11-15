from flask import Blueprint

reagents_bp = Blueprint("reagents", __name__, url_prefix="/admin/reagents")


@reagents_bp.route("/import", methods=["GET", "POST"])
def import_csv():
    return "CSV 업로드 준비 중입니다."
