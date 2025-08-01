from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API key from exchangerate-api.com (you can get a free one)
API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])
        
        # Get exchange rates
        response = requests.get(f'{BASE_URL}{from_currency}')
        data = response.json()
        
        if data['result'] == 'success':
            rate = data['conversion_rates'][to_currency]
            converted_amount = round(amount * rate, 2)
            return jsonify({
                'success': True,
                'result': f'{amount} {from_currency} = {converted_amount} {to_currency}',
                'rate': f'1 {from_currency} = {rate} {to_currency}'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch exchange rates'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)