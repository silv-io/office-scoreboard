from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_events as events,
)
from constructs import Construct

from .serverless import Serverless

STR = dynamodb.AttributeType.STRING
NUM = dynamodb.AttributeType.NUMBER

GAME = 'toplist_pk'
PLAYER = 'toplist_sk'
SCORE = 'score'
FROM_SCORE = 'from_score'


class OfficeScoreboardStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        serverless = Serverless(self)

        serverless.create_application(
            app_id=construct_id,
            resource_handlers=[
                {
                    'path': '/game/{game}/scoreboard',
                    'methods': ['GET'],
                    'handler': 'handler.get_scoreboard',
                    'size': 1024,
                },
                {
                    'path': '/game/{game}/tiers',
                    'methods': ['DELETE'],
                    'handler': 'handler.delete_tier_aggregates',
                    'size': 1024,
                },
                {
                    'path': '/game/{game}/player/{player}/score',
                    'methods': ['PUT', 'POST'],
                    'handler': 'handler.add_player_score',
                    'size': 1024,
                },
                {
                    'path': '/game/{game}/player/{player}/score',
                    'methods': ['GET'],
                    'handler': 'handler.get_player_score',
                    'size': 1024,
                },
                {
                    'schedule': events.Schedule.rate(
                        duration=Duration.minutes(1)
                    ),
                    'handler': 'handler.calculate_nr_players_per_tier',
                    'size': 1024,
                },
                {
                    'handler': 'handler.generate_test_data',
                    'size': 1024
                },
            ],
            dynamo_table={
                'table_name': '{}-table'.format(construct_id),
                'partition_key': {'name': GAME, 'type': STR},
                'sort_key': {'name': PLAYER, 'type': STR},
                'indexes': [
                    {
                        'index_name': 'game-score-index',
                        'partition_key': {'name': GAME, 'type': STR},
                        'sort_key': {'name': SCORE, 'type': NUM},
                    },
                    {
                        'index_name': 'game-tier-index',
                        'partition_key': {'name': GAME, 'type': STR},
                        'sort_key': {'name': FROM_SCORE, 'type': NUM},
                    },
                ],
            },
        )
