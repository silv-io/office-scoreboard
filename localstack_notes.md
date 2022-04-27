# Notes

This document contains notes about things that should be noted in [the documentation of LocalStack](docs.localstack.cloud) or features that might be useful.
Those things would have helped during the creation of this project.

## Specific issues with this example
- For `cdklocal` to work you need to remove the ipv4 part of the port mappings in the docker-compose file.
- Newer versions of cdk have a client-side validation of bucket construct creation.
  - Therefore we can't use `__local__` as the hot-reloading bucket name anymore.
  - We should reserve a bucket name like maybe `hot-code`
- `BUCKET_MARKER_LOCAL` doesn't seem to work or the hot reloading in general doesn't work?
  - At least the example in the docs needs updating because AWS changed their sample file
- Got this error: 
  - ```Unable to deploy resource type "CDK::Metadata": {"Type": "AWS::CDK::Metadata", "Metadata": {"aws:cdk:path": "OfficeScoreboard/CDKMetadata/Default"}, "Condition": "CDKMetadataAvailable", "LogicalResourceId": "CDKMetadata", "Properties": {"Analytics": "v2:deflate64:H4sIAAAAAAAA/1WQQW8CIRCFf4t3lkY9eVSb3hqN7d3MwtROd4HNAhqy4b93WDTR03zzgPdeWMnVUi4XcPON0l3TUyunrwCqEyydJ7+Wu6g6DDvwKHSyYJzmK9/Q9ij2P3aGLGCgCwS8QZLTCX3YDlROn3CrlIs2iHccepcMMrL6tHHqZbaswE9dHBXOwY/l7ln5E8Ov00WqlAWB4XhXm83z6HpSqayVsujBtBrkVCQcDXlPzoqPaFUowPKDs8ArF/NsGe+WPHN+aXOIYYjhpRfz3llN1eOYuJt9W8uN3Cz+PFEz8jeQQXmq8x9y/cp9ggEAAA==", "PhysicalResourceId": "cdk-meta-f237966c"}, "_state_": {"type": "AWS::CDK::Metadata"}}```
## General feature ideas
- some kind of "reset" functionality which wipes all the user state of the current running instance to avoid relaunching localstack everytime you want a blank slate
  - Next Hackathon? :)