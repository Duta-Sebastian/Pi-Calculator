"""
Flask API Server for π Calculator with Swagger Documentation
"""
from flask import Flask
from flask_restx import Api
from celery import Celery
import logging
from shared_config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

api = Api(
    app,
    title='π Calculator API',
    version='1.0',
    description='''
    Calculate π using the Monte Carlo method with asynchronous processing!
    
    ## How it works
    We use the Monte Carlo method - imagine throwing darts at a square with a circle inscribed inside.
    The ratio of darts landing inside the circle vs total darts approximates π/4!
    
    ## Usage Flow
    1. **Start Calculation**: Call `/pi/calculate` with desired decimal precision
    2. **Monitor Progress**: Use `/pi/progress` with the returned task_id
    3. **Get Result**: When state is "FINISHED", the result contains your π value!
    
    ## Monte Carlo Magic
    - More decimal places = more "dart throws" = higher accuracy
    - Progress updates in real-time
    - Fun to watch π emerge from randomness!
    ''',
    doc='/swagger/',
    contact='Duta Andrei-Sebastian',
    license='MIT'
)

celery = Celery(
    app.import_name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)

from app.routes import pi_calculation_route
from app.routes import health_route

