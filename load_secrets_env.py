import json
import boto3

client = boto3.client("secretsmanager", region_name="us-east-2")

response = client.get_secret_value(
    SecretId="prod/senses"
)

secrets = json.loads(response["SecretString"])

for k, v in secrets.items():
    print(f'export {k}="{v}"')