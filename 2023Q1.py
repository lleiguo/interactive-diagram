# 2019.py
from xml.sax.xmlreader import AttributesImpl
from diagrams import Diagram, Cluster, Edge

from diagrams.aws.compute import ECS
from diagrams.aws.database import Aurora, Dynamodb
from diagrams.aws.analytics import ManagedStreamingForKafka


from diagrams.k8s.compute import Pod

graph_attr = {
    "fontsize": "60",
    "bgcolor": "transparent"
}

with Diagram("2023 Q1", filename="2023Q1", show=False, direction="TB", graph_attr=graph_attr, outformat=["png"]):


    with Cluster(label="Production/Staging", direction="TB", graph_attr={"id": "cluster_production","bgcolor": "white", "fontsize": "20"}):

        with Cluster("Vault"):
            vault = ECS("Vault", id="ec2-vault")

        with Cluster("Stateful Services", graph_attr={"id": "cluster_data_storage", "fontsize": "20"}):
            rds = Aurora("Aurora 5.7")
            dynamo = Dynamodb("DynamoDB")
            msk = ManagedStreamingForKafka("MSK")
            datastore = [rds, msk, dynamo]

    with Cluster("Kubernetes Cluster", graph_attr={"id": "cluster_k8s", "fontsize": "20"}):
        with Cluster("Ingress", graph_attr={"id": "cluster_edge_aperture"}):
            traefik = Pod("Traefik Aperture",
                                id="cluster_edge_traefik")
            k8sIngress = Pod("Traefik K8s Ingress")

        servicePods = [Pod("Dashboard PHP", id="dashboard"), Pod("Amplify", id="amplify"), Pod("Owly Web", id="owlyPod"), Pod("Auth Facade", id="authfacade"), Pod("Webhook Egress Proxy", id="webhookEgressProxy")]
        servicePod = Pod("200+ Microservices", id="servicePods")



# Path:
    vault >> Edge(reverse=True) << servicePods
    servicePod >> Edge(reverse=True, id="edge_datastore") << datastore
    k8sIngress >> Edge(reverse=True) << servicePods
    k8sIngress >> Edge(reverse=True) << servicePod
    traefik >> Edge(reverse=True) << servicePods
    traefik >> Edge(reverse=True) << servicePod
    servicePod >> Edge(reverse=True, id="edge_datastore") << datastore
