from churchAPP import create_app

app = create_app()

if __name__ == '__main__':
    app.run(Debug=True)
    app.run(host="0.0.0.0", port=8080, threaded=True)
