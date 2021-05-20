from kakebo import app

@app.route('/')
def index():
    return 'FLASK RULANDO'