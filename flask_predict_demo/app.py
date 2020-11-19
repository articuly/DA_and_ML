from flask import Flask, request, render_template
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


def create_app():
    iris = load_iris()
    model = LogisticRegression()
    model.fit(iris.data, iris.target)
    print('completed fitting')

    app = Flask(__name__)

    @app.route('/predict', methods=['POST', 'GET'])
    def predict():
        if request.method == 'POST':
            try:
                sample = [
                    float(request.form['sl']),
                    float(request.form['sw']),
                    float(request.form['pl']),
                    float(request.form['pw']),
                ]
                pred = model.predict(np.array(sample).reshape(1, -1))[0]
                return "h2>The predictor say it's a <b>{}</b></h2>".format(iris['target_names'][pred])
            except Exception as e:
                print(e)
                return '<h2>Error, value should be all numbers.</h2>'
        return render_template('predict.html')

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

'''
参考数据
5.1, 3.5, 1.4, 0.2 setosa
7.0, 3.2, 4.7, 1.4 versicolor
6.3, 3.3, 6.0, 2.5 virginica
'''
