"""
Celery Tasks for π Calculator
"""
import random
from decimal import getcontext, Decimal

from celery import Celery
from celery.utils.log import get_task_logger
from shared_config import Config

celery = Celery(
    'tasks',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery.conf.update(
    worker_send_task_events=True,
    task_send_sent_event=True,
    result_expires=3600,
    timezone='UTC',
    enable_utc=True,
)

logger = get_task_logger(__name__)


@celery.task(bind=True)
def calculate_pi_task(self, decimals):
    """
    Calculate π using Monte Carlo method with progress updates.

    The Monte Carlo method works by:
    1. Generating random points in a unit square [0,1] x [0,1]
    2. Checking if they fall inside an inscribed unit circle (radius = 1)
    3. Using the ratio (points inside circle)/(total points) ≈ π/4
    4. Multiplying by 4 to get π


    Args:
        self:
        decimals (int): Number of decimal places for π precision

    Returns:
        float: Calculated π value rounded to specified decimals
    """
    logger.info(f" Starting Monte Carlo π calculation for {decimals} decimal places")
    getcontext().prec = decimals + 5

    iterations = int(10 ** (2 * decimals))

    logger.info(f"Will perform {iterations:,} Monte Carlo iterations (dart throws)")

    inside_circle = 0
    total_points = 0

    report_interval = max(1, iterations // 10000)

    try:
        self.update_state(
            state='PROGRESS',
            meta={
                'progress': 0
            }
        )
        for i in range(iterations):
            x = random.random()
            y = random.random()

            if x*x + y*y <= 1:
                inside_circle += 1

            total_points += 1

            if i % report_interval == 0 and i > 0:
                current_pi = Decimal(4) * Decimal(inside_circle) / Decimal(total_points)
                progress = (i + 1) / iterations

                self.update_state(
                    state='PROGRESS',
                    meta={
                        'progress': progress
                    }
                )

                logger.info(
                    f"Progress: {progress:.1%} | "
                    f"Current π: {current_pi:.{min(decimals+2, 10)}f} | "
                    f"Darts inside circle: {inside_circle:,}/{total_points:,}"
                )

    except Exception as e:
        logger.error(f"Error during π calculation: {e}")
        raise

    pi_estimate = Decimal(4) * Decimal(inside_circle) / Decimal(total_points)
    pi_string = str(pi_estimate.quantize(Decimal(10) ** -decimals))

    return pi_string