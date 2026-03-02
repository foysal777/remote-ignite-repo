import os
from project_root.aws_secrets import load_aws_secrets

print("Loading AWS Secrets...")

secrets = load_aws_secrets(
    secret_name="prod/senses",
    region_name="us-east-2"
)

for key, value in secrets.items():
    if value:
        os.environ[key] = str(value)

print("AWS secrets loaded successfully.")