from flask import Flask, request, render_template
import pickle

# Create flask app
app = Flask(__name__, template_folder='',static_folder='')
model = pickle.load(open("lr_model.pickle", "rb"))


def get_predicted_salary(exp, level, company_size, company_type):
    yrs_exp = exp
    level_Head, level_Middle, level_Senior = 0, 0, 0
    company_size_100_1000, company_size_50_100, company_size_more_than_1000 = 0, 0, 0
    company_type_Agency, company_type_Product, company_type_Startup = 0, 0, 0
    if level == "Head":
        level_Head = 1
    elif level == "Middle":
        level_Middle = 1
    elif level == "Senior":
        level_Senior = 1

    if company_size == "100-1000":
        company_size_100_1000 = 1
    elif company_size == "50-100":
        company_size_50_100 = 1
    elif company_size == "more_than_1000":
        company_size_more_than_1000 = 1

    if company_type == "Agency":
        company_type_Agency = 1
    elif company_type == "Product":
        company_type_Product = 1
    elif company_type == "Startup":
        company_type_Startup = 1

    x = [yrs_exp, level_Head, level_Middle, level_Senior, company_size_100_1000, company_size_50_100, company_size_more_than_1000, company_type_Agency, company_type_Product, company_type_Startup]
    value = str(int(model.predict([x])[0]))[:-3] + "000"  # converting 123456.556767 to 123000
    return int(value)


@app.route("/")
def Home():
    return render_template("app.html")


@app.route("/predict", methods=['POST'])
def predict_price():
    exp = request.form.get("exp")
    level = request.form.get("level")
    company_size = request.form.get("company_size")
    company_type = request.form.get("company_type")
    sal = get_predicted_salary(exp, level, company_size, company_type)
    return render_template("app.html", salary=sal)


if __name__ == "__main__":
    app.run(debug=True)
