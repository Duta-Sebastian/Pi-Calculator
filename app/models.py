"""
API Models for Swagger Documentation
"""
from flask_restx import fields, Api


def create_api_models(api: Api):
    return {
        'calculation_request': api.model('CalculationRequest', {
            'n': fields.Integer(
                required=True,
                min=1,
                max=200,
                description='Number of decimal places for π calculation',
                example=5
            )
        }),

        'calculation_response': api.model('CalculationResponse', {
            'task_id': fields.String(
                required=True,
                description='Unique task identifier for tracking progress',
                example='12345678-1234-1234-1234-123456789abc'
            ),
        }),

        'progress_response': api.model('ProgressResponse', {
            'state': fields.String(
                required=True,
                description='Current task state',
                enum=['PROGRESS', 'FINISHED'],
                example='PROGRESS'
            ),
            'progress': fields.String(
                required=True,
                description='Completion progress (0.0 to 1.0)',
                example='0.75'
            ),
            'result': fields.String(
                allow_null=True,
                description='Calculated π value (null if not finished)',
                example=3.14159
            ),
        }),

        'error_response_calculate': api.model('ErrorResponse', {
            'message': fields.String(
                required=True,
                description='Error description',
                example='Parameter n (number of decimals) is required'
            ),
            'errors': fields.Raw(
                description='Detailed error information',
                example={}
            )
        }),

        'error_response_progress': api.model('ErrorResponseProgress', {
            'message': fields.String(
                required=True,
                description='Error description',
                example='Invalid task id parameter'
            ),
            'errors': fields.Raw(
                description='Detailed error information',
                example={}
            )
        }),

        'error_response_internal_server_error': api.model('ErrorResponseInternalServerError', {
            'message': fields.String(
                required=True,
                description='Error description',
                example='Request could not be processed, internal server error encountered'
            ),
            'errors': fields.Raw(
                description='Detailed error information',
                example={}
            )
        })
    }

def create_health_response(api: Api):
    return {
        'health_response': api.model('HealthResponse', {
            'status': fields.String(
                required=True,
                description='Service health status',
                example='healthy'
            ),
            'service': fields.String(
                description='Service name',
                example='π Calculator API'
            ),
            'message': fields.String(
                description='Status message',
                example='Ready to calculate π using Monte Carlo magic!'
            )
        })
    }
