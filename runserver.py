from news import app,config
if __name__ == '__main__':
    if config.DEBUG:
        app.run(host='0.0.0.0',debug=True)
    else:
        app.run(host='0.0.0.0',port=80,debug=False)

application=app
