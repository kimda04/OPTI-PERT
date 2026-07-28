from email.mime import text

from app.services.graph_plot_service import generate_graph
from app.services.gantt_service import generate_gantt
from flask import send_file
from app.services.excel_service import generate_excel
from app.services.pdf_service import generate_pdf
from app.services.graph_plot_service import export_graph_png
from app.services.gantt_service import export_gantt_png
from app.ai.speech_service import SpeechService
from app.ai.vision_service import VisionService
from app.services.pert_context_service import PertContextService
from app.ai.pert_parser import PertParser
from app.services.project_service import add_activity
from werkzeug.utils import secure_filename
from app.services.calendar_service import generate_calendar

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

import os
import uuid
from flask import request, jsonify
from app.ai.vision_service import VisionService
from app.ai.pert_parser import PertParser
from flask import render_template
from app.ai.openai_service import OpenAIService

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():

    return render_template(
        "index.html",
        project=get_project(),
        graph_html=generate_graph(),
        gantt_html=generate_gantt(),
        calendar_events=generate_calendar()
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
    
@home_bp.route("/speech/test")
def speech_test():

    text = SpeechService.transcribe_audio(
        "audio.wav"
    )

    return {
        "text": text
    }


@home_bp.route("/speech")
def speech_page():

    return render_template(
        "speech.html"
    )



@home_bp.route("/speech/upload", methods=["POST"])
def speech_upload():

    audio = request.files.get(
        "audio"
    )


    if not audio:

        return redirect(
            url_for("home.speech_page")
        )


    filename = secure_filename(
        audio.filename
    )


    filepath = os.path.join(
        "app",
        "exports",
        filename
    )


    audio.save(filepath)


    text = SpeechService.transcribe_audio(
        filepath
    )


    os.remove(filepath)


    return render_template(
        "speech.html",
        text=text
    )
    
@home_bp.route("/vision/test")
def vision_test():

    text = VisionService.extract_text(
        "tabla.jpg"
    )

    return {
        "text": text
    }
    
    
@home_bp.route("/vision/upload", methods=["POST"])
def vision_upload():

    image = request.files.get(
        "image"
    )


    if not image:

        return jsonify(
            {
                "error":
                "No se recibió imagen"
            }
        ), 400


    filename = (
        str(uuid.uuid4())
        + ".jpg"
    )


    filepath = os.path.join(
        "app",
        "exports",
        filename
    )


    image.save(filepath)


    text = VisionService.extract_text(
        filepath
    )


    activities = PertParser.parse_ocr_text(
        text
    )


    os.remove(filepath)


    return render_template(
        "ocr_test.html",
        ocr_text=text,
        activities=activities
    )
    
@home_bp.route("/ocr")
def ocr_page():

    return render_template(
        "ocr_test.html"
    )
    
    
@home_bp.route("/ai/test")
def ai_test():

    project_context = PertContextService.generate_context()

    question = """
    Analiza el proyecto actual.

    Explica:
    - posibles problemas
    - actividades importantes
    - recomendaciones
    """

    response = OpenAIService.ask(
        question,
        project_context
    )

    return {
        "respuesta": response
    }
    
@home_bp.route("/ai", methods=["GET","POST"])
def ai_page():

    response=None

    if request.method=="POST":

        question=request.form["question"]

        project_context=str(get_project())


        response=OpenAIService.ask(
            question,
            project_context
        )


    return render_template(
        "ai.html",
        response=response
    )
    
@home_bp.route("/activity/edit/<name>", methods=["GET","POST"])
def activity_edit(name):

    project = get_project()

    activity = next(
        (
            a for a in project.activities
            if a.name == name
        ),
        None
    )

    if not activity:
        return redirect(url_for("home.home"))


    if request.method == "POST":

        activity.description = request.form["description"]

        activity.optimistic = float(
            request.form["optimistic"]
        )

        activity.most_likely = float(
            request.form["most_likely"]
        )

        activity.pessimistic = float(
            request.form["pessimistic"]
        )

        activity.predecessors = [
            x.strip()
            for x in request.form["predecessors"].split(",")
            if x.strip()
        ]

        return redirect(
            url_for("home.home")
        )


    return render_template(
        "edit_activity.html",
        activity=activity
    )
    

@home_bp.route("/calendar")
def calendar():

    return render_template(
        "calendar.html"
    )



@home_bp.route("/gantt")
def gantt_page():

    return render_template(
        "gantt.html",
        gantt_html=generate_gantt()
    )



@home_bp.route("/critical-path")
def critical_path():

    project = get_project()

    return render_template(
        "critical_path.html",
        project=project
    )