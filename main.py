from cdktf import App, TerraformStack, TerraformAsset, AssetType
from constructs import Construct
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.sqs_queue import SqsQueue
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.lambda_event_source_mapping import LambdaEventSourceMapping

class GradedLabStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region="us-east-1")

        # Création des files SQS
        input_queue = SqsQueue(self, "InputQueue", name="graded_lab_input_queue", visibility_timeout_seconds=60)
        output_queue = SqsQueue(self, "OutputQueue", name="graded_lab_output_queue", visibility_timeout_seconds=60)

        # Packagage du code
        code = TerraformAsset(
            self, "code",
            path="./lambda", # dossier du code
            type= AssetType.ARCHIVE
        )

        # Create Lambda function
        lambda_function = LambdaFunction(self,
                "lambda",
                function_name="first_lambda",
                runtime="python3.8",
                memory_size=128,
                timeout=60,
                role="arn:aws:iam::868291412192:role/LabRole",
                filename= code.path,
                handler="lambda_function.lambda_handler",
                environment={"variables":{"foo":"bar"}}
            )

        # Lier la Lambda à la file SQS d'entrée
        LambdaEventSourceMapping(
            self, "EventSourceMapping",
            event_source_arn=input_queue.arn,
            function_name=lambda_function.arn
        )

app = App()
GradedLabStack(app, "graded_lab")
app.synth()
