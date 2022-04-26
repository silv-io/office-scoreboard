from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb
)
from constructs import Construct

from serverless import Serverless

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
