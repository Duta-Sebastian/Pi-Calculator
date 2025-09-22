"""
Pi calculation namespace and routes
"""
import logging

from flask import request
from flask_restx import Resource

from app.app import api
from app.models import create_api_models
from celery_worker.tasks import calculate_pi_task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ns_pi = api.namespace('pi', description='π Calculation Operations')

api_models = create_api_models(api)

calculation_request = api_models['calculation_request']
calculation_response = api_models['calculation_response']
progress_response = api_models['progress_response']
error_response_calculate = api_models['error_response_calculate']
error_response_progress = api_models['error_response_progress']
error_response_internal_server_error = api_models['error_response_internal_server_error']


@ns_pi.route('/calculate')
class CalculatePi(Resource):
    """Start π calculation using Monte Carlo method"""

    @ns_pi.doc(
        'calculate_pi',
        description='Start calculating π to specified decimal places using Monte Carlo simulation',
        params={
            'n': 'Number of decimal places (1-200).'
        }
    )
    @ns_pi.response(400, 'Invalid decimal places parameter', model=error_response_calculate)
    @ns_pi.response(500, 'Internal server error', model=error_response_internal_server_error)
    @ns_pi.marshal_with(calculation_response, code=200, description='Calculation started successfully')
    def get(self):
        """Start π calculation task"""
        try:
            n = request.args.get('n', type=int)
            if n is None:
                api.abort(400, 'Parameter n (number of decimals) is required')

            if n < 1 or n > 200:
                api.abort(400, 'n must be between 1 and 200')

            task = calculate_pi_task.delay(n)
            logger.info(f"Started π calculation task {task.id} for {n} decimals")

            return {"task_id": str(task.id)}

        except Exception as e:
            logger.error(f"Error starting π calculation: {e}")
            api.abort(500, 'Internal server error')


@ns_pi.route('/progress')
class CheckProgress(Resource):
    """Check the progress of a π calculation task"""

    @ns_pi.doc(
        'check_progress',
        description='Check the progress and result of a π calculation task',
        params={
            'task_id': 'Task ID returned from /pi/calculate endpoint'
        }
    )
    @ns_pi.response(400, 'Invalid task ID parameter', model=error_response_progress)
    @ns_pi.response(500, 'Internal server error', model=error_response_internal_server_error)
    @ns_pi.marshal_with(progress_response, code=200, description='Progress information')
    def get(self):
        """Check task progress"""
        try:
            task_id = request.args.get('task_id')
            if not task_id:
                api.abort(400, 'Parameter task_id is required')

            task = calculate_pi_task.AsyncResult(task_id)
            logger.info(f"Current state of calculation task {task.id} is {task.state}, {task.info}, {task.result}")
            if task.state == 'PENDING':
                response = {
                    'state': 'PROGRESS',
                    'progress': 0.0,
                    'result': None
                }
            elif task.state == 'PROGRESS':
                info = task.info or {}
                response = {
                    'state': 'PROGRESS',
                    'progress': info.get('progress', 0),
                    'result': None
                }
            elif task.state == 'SUCCESS':
                response = {
                    'state': 'FINISHED',
                    'progress': 1.0,
                    'result': task.result
                }
            else:
                response = {
                    'state': 'FAILED',
                    'progress': 0.0,
                    'result': None
                }

            return response

        except Exception as e:
            logger.error(f"Error checking progress: {e}")
            api.abort(500, 'Internal server error')
