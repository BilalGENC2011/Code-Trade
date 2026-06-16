from flask import Flask, render_template

app = Flask(__name__)

# Bu kısım sitenin ana sayfası (kapısı)
@app.route('/')
def ana_sayfa():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()