"""
Health check namespace and route
"""
from flask_restx import Resource

from app.app import api
from app.models import create_health_response

ns_health = api.namespace('health', description='Health Check')

health_response = create_health_response(api)['health_response']

@ns_health.route('/health')
class HealthCheck(Resource):
    """System health check"""

    @ns_health.doc('health_check', description='Check if the API is running properly')
    @ns_health.marshal_with(health_response, code=200, description='Service is healthy')
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'π Calculator API',
            'message': 'Ready to calculate π using Monte Carlo magic!'
        }
