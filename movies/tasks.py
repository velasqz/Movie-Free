from celery._state import get_current_app

app = get_current_app()

@app.task()
def add(x,y):
    print(x+y)
