from flask import Flask, request, render_template
import pickle
from markupsafe import Markup
from narratives.db.ao3_db import AO3DB  # type: ignore

app = Flask(__name__)
NUM_TO_RETURN = 12


def get_meta(work_id):

    # Lookup matrix index for fanwork ID
    # print(f"DEBUG 1: {indices['work_id']['24670738']}")
    work_indice = indices["work_id"][str(work_id)]
    # print(f"DEBUG: {work_indice}")

    # Find similar items
    related_BPR = model.similar_items(work_indice, NUM_TO_RETURN)

    for work in related_BPR:
        # Find fanwork ID from matrix indices
        suggested_id = inverted_indices["work_id"][work[0]]
        meta = ao3_db.fanwork_select(suggested_id)
        title = meta[1]
        author = meta[2]
        yield suggested_id, title, author


def validate(request):
    try:
        fanwork_id = [int(x) for x in request.form.values()][0]
        fanwork_id = str(fanwork_id)
    except ValueError:
        raise ValueError("Enter a number as fanwork ID")
        return

    if ao3_db.fanwork_exists(fanwork_id):
        return fanwork_id
    else:
        raise ValueError("FanWork ID not in current recommendation system")


@app.before_first_request
def load__model():
    global model
    global indices
    global inverted_indices
    global ao3_db

    try:
        ao3_db = AO3DB("inference_log", "models/implicit.log")
    except Exception as e:
        print(f"ERROR in app.py: {e}")

    model = pickle.load(open("models/implicit.pkl", "rb"))
    indices = pickle.load(open("models/indices.pkl", "rb"))
    inverted_indices = {"work_id": {}, "user": {}}
    inverted_indices["work_id"] = {v: k for k, v in indices["work_id"].items()}
    inverted_indices["user"] = {v: k for k, v in indices["user"].items()}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            fanwork_id = validate(request)
        except Exception as e:
            errormsg = f"{str(e)}"
            return render_template("index.html", prediction_text=errormsg)

        suggestions = get_meta(fanwork_id)
        response = (
            f"Suggested works for <a href='http://ao3.org/works/{fanwork_id}'"
            f" target='_blank'> {next(suggestions)[1]}</a>:<br><br>"
        )
        next(suggestions)
        count = 1
        for suggested_id, title, author in suggestions:
            if count > NUM_TO_RETURN:
                print(f"breaking out at count value: {count}")
                break
            link = (
                f"{count}. "
                f"<a href ='http://ao3.org/works/{suggested_id}'"
                f" target='_blank'> {title}</a> .... by {','.join(author)}"
                f"<br>"
            )
            response = response + link
            count += 1
        return render_template("index.html", prediction_text=Markup(response))


@app.route("/<work_id>", methods=["POST"])
def predict_again(work_id):
    # make generator pickup where it left off at
    # temp = return_template('index.html', work_id=work_id)
    # # forgot what return_template should be
    temp = 0
    return temp


if __name__ == "__main__":
    app.run(debug=True)
