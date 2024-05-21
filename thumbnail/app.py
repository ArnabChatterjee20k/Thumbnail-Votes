from thumnbail import create_app
app = create_app()
from dotenv import load_dotenv
load_dotenv(".env")
app.app_context().push()
app.run("0.0.0.0",port=5400,debug=True)