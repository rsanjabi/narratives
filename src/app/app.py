
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
from lightfm import LightFM

app = Flask(__name__)
model = pickle.load(open('../../data/models/test.pkl', 'rb'))



def sample_fanworks_rec(model, dataset, users):

    n_users, n_items = dataset.interactions_shape()
    
    for user_name in users:
        #known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]
        user_id = dataset.mapping()[0][user_name]
        
        scores2 = model.predict(user_id, np.arange(n_items))
        #top_items = data['work_id'][np.argsort(-scores)]
        top_indices = np.argsort(-scores2)
        #top_items = dataset.mapping()[2][np.argsort(-scores)]

        print(f"User {user_id} {user_name}")
        print("     Known positives:")
        

        #for x in known_positives[:3]:
        #    print("        %s" % x)

        print("     Recommended:")

        for x in top_indices[:10]:

            y = dict(map(reversed, dataset.mapping()[2].items()))[x]
            print(f"http://www.archiveofourown.org/works/{y}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    fanwork_id = [int(x) for x in request.form.values()][0]
    scores2 = model.predict(fanwork_id, np.arange(4224))
    top_indices = np.argsort(-scores2)
    return render_template('index.html', prediction_text='Getting predictions for {}'.format(top_indices[0]))


@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)