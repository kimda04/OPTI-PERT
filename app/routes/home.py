from app.services.graph_plot_service import generate_graph
from app.services.gantt_service import generate_gantt
from flask import send_file
from app.services.excel_service import generate_excel
from app.services.pdf_service import generate_pdf
from app.services.graph_plot_service import export_graph_png
from app.services.gantt_service import export_gantt_png

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app.models.activity import Activity

from app.services.project_service import (
    get_project,
    add_activity,
    remove_activity
)

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return render_template(
        "index.html",
        project=get_project(),
        graph_html=generate_graph(),
        gantt_html=generate_gantt()
    )

@home_bp.route("/activity/add", methods=["POST"])
def activity_add():

    activity = Activity(

        name=request.form["name"],

        description=request.form["description"],

        optimistic=float(request.form["optimistic"]),

        most_likely=float(request.form["most_likely"]),

        pessimistic=float(request.form["pessimistic"]),

        predecessors=[
            predecessor.strip()
            for predecessor in request.form["predecessors"].split(",")
            if predecessor.strip()
        ]
    )

    add_activity(activity)

    return redirect(url_for("home.home"))


@home_bp.route("/activity/delete/<name>")
def activity_delete(name):

    remove_activity(name)

    return redirect(url_for("home.home"))

@home_bp.route("/export/excel")
def export_excel():
    return send_file(
        generate_excel(),
        as_attachment=True,
        download_name="OPTI-PERT.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
@home_bp.route("/export/pdf")
def export_pdf():
    return send_file(
        generate_pdf(),
        as_attachment=True,
        download_name="OPTI-PERT.pdf",
        mimetype="application/pdf"
    )
    
@home_bp.route("/export/png/pert")
def export_pert_png():
    return send_file(
        export_graph_png(),
        mimetype="image/png",
        as_attachment=True,
        download_name="PERT.png"
    )


@home_bp.route("/export/png/gantt")
def export_gantt_png_route():
    return send_file(
        export_gantt_png(),
        mimetype="image/png",
        as_attachment=True,
        download_name="Gantt.png"
    )