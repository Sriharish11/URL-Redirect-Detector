from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        session = requests.Session()
        chain = []
        resp = session.get(url, timeout=10, allow_redirects=False)
        while resp.is_redirect or resp.is_permanent_redirect:
            location = resp.headers.get('location')
            chain.append({'status_code': resp.status_code, 'url': resp.url, 'location': location})
            resp = session.get(location, timeout=10, allow_redirects=False)
        chain.append({'status_code': resp.status_code, 'url': resp.url, 'location': None})
        return jsonify({'result': {'redirect_chain': chain}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)