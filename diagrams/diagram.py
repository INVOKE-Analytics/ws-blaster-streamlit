from cgitb import handler
from diagrams import Cluster, Diagram

from diagrams.aws.network import APIGateway
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import EFS

with Diagram("Whats App Blasting API", show=False):
    source = APIGateway("Request")

    with Cluster("Event Flows"):
        with Cluster("Web Servers"):
            handlers = [Lambda("Fast API Server"),
                        Lambda("Fast API Server"),
                        Lambda("Fast API Server")]

        queue = SQS("Whatsapp Blasting queue")

        with Cluster("Blasting Service"):
            workers = [Lambda("Selenium Worker"),
                       Lambda("Selenium Worker"),
                       Lambda("Selenium Worker")]

    store = EFS("Whats APP Account store")
    source >> handlers >> queue >> workers
    handlers - store
    workers - store
