#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.office_scoreboard_stack import OfficeScoreboardStack

if __name__ == '__main__':
    app = cdk.App()
    OfficeScoreboardStack(app, "OfficeScoreboard")
    app.synth()
