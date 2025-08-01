from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# API configuration
API_KEY = 'a8ec91453e1f88bbfec2a156' # Replace with your actual API key
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'
CURRENCIES = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'JPY': 'Japanese Yen',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'INR': 'Indian Rupee',
    'CNY': 'Chinese Yuan',
    'SGD': 'Singapore Dollar',
    'CHF': 'Swiss Franc',
    'MXN': 'Mexican Peso',
    'BRL': 'Brazilian Real',
    'ZAR': 'South African Rand'
}

@app.route('/')
def index():
    return render_template('index.html', currencies=CURRENCIES)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])
        
        if from_currency == to_currency:
            return jsonify({
                'success': True,
                'result': f'{amount} {from_currency} = {amount} {to_currency}',
                'rate': f'1 {from_currency} = 1 {to_currency}',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        response = requests.get(f'{BASE_URL}{from_currency}')
        data = response.json()
        
        if data['result'] == 'success':
            rate = data['conversion_rates'][to_currency]
            converted_amount = round(amount * rate, 2)
            return jsonify({
                'success': True,
                'result': f'{amount} {from_currency} = {converted_amount} {to_currency}',
                'rate': f'1 {from_currency} = {rate} {to_currency}',
                'time': data['time_last_update_utc'][:-9]  # Format the timestamp
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch exchange rates'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)