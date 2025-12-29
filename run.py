from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable for cloud deployment
    port = int(os.environ.get('PORT', 5000))
    # Use 0.0.0.0 for cloud hosting
    app.run(debug=False, host='0.0.0.0', port=port)