import os
from flask import Flask
from personality_insights_wrapper import PersonalityInsightCaller

app = Flask(__name__)

@app.route('/')
def Hello():
    return 'This is mere test. Try the /pitest route'

@app.route('/piroute')
def PIroute():
    username = os.getenv('PIUsername', 'MOCK')
    password = os.getenv('PIPassword','MOCK')
    url = os.getenv('PIUrl','MOCK')
    creds = {'username':username,'password':password,'url':url}
    PIDemo = PersonalityInsightCaller(creds)
    PIDemo.insert_text('Random text for the mock code.')
    insights = PIDemo.get_personality()    
    return insights

@app.route('/pitest')
def PItest():
    username = 'MOCK'
    password = 'MOCK'
    url = 'MOCK'
    creds = {'username':username,'password':password,'url':url}
    PIDemo = PersonalityInsightCaller(creds)
    PIDemo.insert_text('Random text for the mock code.')
    insights = PIDemo.get_personality()
    return insights

#port = os.getenv('PORT', '8080')
port = int(os.getenv('VCAP_APP_PORT', '5000'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)
