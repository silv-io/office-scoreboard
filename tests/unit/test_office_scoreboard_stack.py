import aws_cdk as core
import aws_cdk.assertions as assertions

from office_scoreboard.office_scoreboard_stack import OfficeScoreboardStack

# example tests. To run these tests, uncomment this file along with the example
# resource in office_scoreboard/office_scoreboard_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OfficeScoreboardStack(app, "office-scoreboard")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
