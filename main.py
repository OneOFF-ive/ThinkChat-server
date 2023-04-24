from flask import Flask, url_for, make_response, session

app = Flask(__name__)
app.secret_key = 'my_secret_key'


@app.route('/projects')
def projects():
    resp = make_response()
    resp.set_data(value="The project page")
    return resp


@app.route('/about')
def about():
    resp = make_response()
    test = session.get('test')
    if test is not None:
        print(test)
    else:
        session['test'] = "test"
    resp.set_data(value="about")
    return resp


@app.errorhandler(404)
def page_not_found(error):
    return "404"


if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('projects', test=123))
    app.run(port=2023)
