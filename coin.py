from flask import Flask,render_template, redirect,url_for
import requests
from bs4 import BeautifulSoup
from wtforms import StringField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm 
from bs4.element import ProcessingInstruction


# ----------------- FLASK APP-----------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = 'THISISMYSECRETKEY'

class InputForm(FlaskForm):
    coin = StringField(validators=[InputRequired(), Length(min=4,max=20)], render_kw={"placeholder": "Coin name: "})
    sumbit = SubmitField("Search")


@app.route('/',methods={'GET','POST'})
def home():
    form = InputForm()
    coin = form.coin.data

    if form.validate_on_submit():
        # ---------------------- PARSING --------------------------
        # coin = 'bitcoin'
        URL = f"https://news.bitcoin.com/?s={coin}"
        HEADERS = {"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36",
                        "accept" : "*/*"}
            

        html = requests.get(URL,headers = HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div',class_='td_module_16 td_module_wrap td-animation-stack')
        coins = []
        for item in items:
            coins.append({
                'title': item.find('h3', class_='entry-title td-module-title').get_text(strip=True),    
                'url': item.find('a').get('href')
                }) 
        
        return render_template('home.html', form=form, results=coins)

    return render_template('home.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

