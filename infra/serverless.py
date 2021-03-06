"""
Copied from https://github.com/aws-samples/serverless-scoreboard-example/blob/master/infrastructure/serverless.py
"""
from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    Duration,
    RemovalPolicy
)
from constructs import Construct

STR = dynamodb.AttributeType.STRING
NUM = dynamodb.AttributeType.NUMBER

GAME = 'toplist_pk'
PLAYER = 'toplist_sk'
SCORE = 'score'
FROM_SCORE = 'from_score'


class Serverless:
    def __init__(self, scope: Construct) -> None:
        self.scope = scope

    def create_application(self, app_id, resource_handlers, dynamo_table):
        bucket = s3.Bucket.from_bucket_name(self.scope, "HotReloadingBucket", "hot-code")
        code = _lambda.Code.from_bucket(bucket=bucket,
                                        key="/tmp/lambda")

        if bool(dynamo_table):
            ddb_table = self.create_ddb_table(dynamo_table)
        else:
            ddb_table = {}

        if len(resource_handlers) > 0:
            restapi = apigateway.RestApi(
                self.scope, '{}-api'.format(app_id), rest_api_name='{}-api'.format(app_id)
            )

            for resource_handler in resource_handlers:

                handler = resource_handler['handler']
                readonly = resource_handler.get('readonly', False) or False
                memory_size = resource_handler.get('memory_size', 512) or 512

                if resource_handler.get('path'):
                    path = resource_handler['path']
                    methods = resource_handler['methods']
                    if ['GET'] == methods:
                        readonly = True

                    self.create_resource_handler(
                        name=self.create_name(app_id, handler),
                        handler=handler,
                        memory_size=memory_size,
                        code=code,
                        api=restapi,
                        path=path,
                        methods=methods,
                        table=ddb_table,
                        readonly=readonly,
                    )

                elif resource_handler.get('schedule'):
                    function = self.create_function(
                        name=self.create_name(app_id, handler),
                        handler=handler,
                        memory_size=memory_size,
                        code=code,
                        table=ddb_table,
                        readonly=readonly,
                    )

                    rule_name = '{}-rule'.format(self.create_name(app_id, handler))

                    scheduled_rule = events.Rule(
                        self.scope,
                        rule_name,
                        rule_name=rule_name,
                        schedule=events.Schedule.rate(
                            duration=Duration.minutes(1)
                        ),
                    )
                    scheduled_rule.add_target(events_targets.LambdaFunction(function))
                else:
                    self.create_function(
                        name=self.create_name(app_id, handler),
                        handler=handler,
                        code=code,
                        table=ddb_table,
                        readonly=readonly,
                    )

    @staticmethod
    def create_name(app_id, handler):
        return '{}-{}-function'.format(
            app_id, handler.split('.')[1].replace('.', '').replace('_', '-')
        ).lower()

    def create_ddb_table(self, dynamo_table):
        table_name = dynamo_table['table_name']
        partition_key = dynamo_table['partition_key']
        sort_key = dynamo_table.get('sort_key')
        if sort_key:
            ddb_table = dynamodb.Table(
                self.scope,
                table_name,
                table_name=table_name,
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                partition_key=dynamodb.Attribute(
                    name=partition_key['name'], type=partition_key['type']
                ),
                sort_key=dynamodb.Attribute(
                    name=sort_key['name'], type=sort_key['type']
                ),
                removal_policy=RemovalPolicy.DESTROY,
            )
        else:
            ddb_table = dynamodb.Table(
                self.scope,
                table_name,
                table_name=table_name,
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                partition_key=dynamodb.Attribute(name=GAME, type=STR),
                removal_policy=RemovalPolicy.DESTROY,
            )

        indexes = dynamo_table.get('indexes', [])
        for index in indexes:
            gsi_partition_key = index['partition_key']
            gsi_sort_key = index['sort_key']
            ddb_table.add_global_secondary_index(
                index_name=index['index_name'],
                partition_key=dynamodb.Attribute(
                    name=gsi_partition_key['name'], type=gsi_partition_key['type']
                ),
                sort_key=dynamodb.Attribute(
                    name=gsi_sort_key['name'], type=gsi_sort_key['type']
                ),
            )
        return ddb_table

    def create_resource_handler(
            self,
            name,
            handler,
            api,
            path,
            methods,
            code,
            table,
            memory_size=512,
            readonly=True,
    ):

        function = self.create_function(
            name=name,
            handler=handler,
            memory_size=memory_size,
            code=code,
            table=table,
            readonly=readonly,
        )

        api_resource = api.root.resource_for_path(path)

        for method in methods:
            api_resource.add_method(method, apigateway.LambdaIntegration(function))

    def create_function(
            self, name, handler, code, table, memory_size=512, readonly=True
    ):
        has_table = bool(table)

        if has_table:
            envs = {'TABLE_NAME': table.table_name}
        else:
            envs = {}

        function = _lambda.Function(
            self.scope,
            name,
            function_name=name,
            runtime=_lambda.Runtime.PYTHON_3_9,
            memory_size=memory_size,
            code=code,
            handler=handler,
            tracing=_lambda.Tracing.ACTIVE,
            environment=envs,
        )

        if has_table and readonly:
            table.grant_read_data(function)
        elif has_table and not readonly:
            table.grant_read_write_data(function)

        return function
