from views import app

if __name__ == "__main__":
    app.run()

# Use webpy module to create a wsgi function
application = app.wsgifunc()
