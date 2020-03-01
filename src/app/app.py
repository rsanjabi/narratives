
from flask import Flask, request, jsonify, render_template
import pickle
import implicit
from markupsafe import Markup

app = Flask(__name__)

NUM_TO_RETURN = 5

@app.before_first_request
def load__model():
    global model
    global indices
    global inverted_indices

    model = pickle.load(open('../../models/bpr270220.pkl', 'rb'))
    indices = pickle.load(open('../../models/indices270220.pkl', 'rb'))
    inverted_indices = {'work_id':{}, 'user':{}}
    inverted_indices['work_id'] = {v: k for k, v in indices['work_id'].items()}
    inverted_indices['user'] = {v: k for k, v in indices['user'].items()}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        results = ""
        prefix = "<a href='http://www.archiveofourown.org/works/"
        postfix = "'>"
        postpostfix = "</a>\n"
        fanwork_id = [int(x) for x in request.form.values()][0]
        work_indice = indices['work_id'][str(fanwork_id)]
        related_BPR = model.similar_items(work_indice, NUM_TO_RETURN)
        for suggestion in related_BPR:
            work_id = inverted_indices['work_id'][suggestion[0]]
            results = results + prefix + work_id + postfix + work_id + postpostfix
        return render_template('index.html', prediction_text = Markup(results))
        #return render_template('index.html', results
    #return render_template('index.html', prediction_text=results)

if __name__ == "__main__":
    app.run(debug=True)