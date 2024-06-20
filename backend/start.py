from src.app import create_app, socketio

if __name__ == '__main__':
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    print(response)
    socketio.run(app, debug=True, port=7890)  # Use socketio.run instead of app.run
    