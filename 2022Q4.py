# 2019.py
from xml.sax.xmlreader import AttributesImpl
from diagrams import Diagram, Cluster, Edge

from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import Aurora, Dynamodb
from diagrams.aws.network import NLB

from diagrams.k8s.compute import Pod
from diagrams.onprem.queue import Kafka 
from diagrams.onprem.network import Zookeeper


graph_attr = {
    "fontsize": "50",
    "bgcolor": "transparent"
}

with Diagram("2022 Q4", filename="2022Q4", show=False, direction="TB", graph_attr=graph_attr, outformat=["png"]):

    with Cluster(label="Production/Staging", direction="TB", graph_attr={"id": "cluster_production","bgcolor": "white", "fontsize": "20"}):

        with Cluster("Aperture", graph_attr={"id": "cluster_aperture", "fontsize": "20"}):
            traefik = AutoScaling("Traefik Aperture",
                                id="ec2_aperture_traefik")

        with Cluster("EC2 Services", graph_attr={"id": "cluster_ec2","fontsize": "20"}):
            authfacade = EC2("Auth Facade", id="ec2-AuthFacade")
            EC2Services = [EC2("Webhook Egress Proxy", id="ec2-WebhookEgressProxy"),
                        EC2("External API", id="ec2-ExternalAPI")]

        with Cluster("Vault", graph_attr={"id": "cluster_vault", "fontsize": "20"}):
            vault = EC2("Vault", id="ec2-vault")

        with Cluster("Event Bus (Kafka)", direction="LR", graph_attr={"id": "cluster_kafka", "fontsize": "20"}):
            kafka = Kafka("Kafka")
            zookeeper = Zookeeper("Zookeeper")

        with Cluster("Stateful Services", graph_attr={"id": "cluster_data_storage","fontsize": "20"}):
            rds = Aurora("Aurora 5.6")
            dynamo = Dynamodb("DynamoDB")
            datastore = [rds, dynamo]

    with Cluster("US-West-1 - Owly", graph_attr={"id": "cluster_owly","bgcolor": "white", "fontsize": "20"}):
        haproxy = NLB("HAProxy", id="haproxy")
        owlyweb = EC2("Owly Web", id="owlyweb")
        owlydb = EC2("Owly DB", id="owly-analytics")
        owlyAnalytics = EC2("Owly Analytics DB", id="owly-analytics")
        owly = [owlyAnalytics, owlydb]

    with Cluster("Kubernetes Cluster", direction="TB", graph_attr={"id": "cluster_k8s","fontsize": "20"}):
            k8sIngress = AutoScaling("Traefik K8s Ingress")
            servicePods = [Pod("Dashboard PHP", id="dashboard"), Pod("Amplify", id="amplify")]
            servicePod = Pod("200+ Microservices", id="servicePods")


# Path:
    traefik >> k8sIngress
    traefik >> Edge(reverse=True, id="edge_ec2_traefik") >> EC2Services
    servicePod >> Edge(reverse=True) << kafka
    vault >> Edge(reverse=True) << servicePods
    k8sIngress >> Edge(reverse=True) << servicePods
    k8sIngress >> Edge(reverse=True) << servicePod
    servicePod >> Edge(reverse=True, id="edge_datastore") << datastore
    authfacade >> Edge(reverse=True, id="edge_ec2other") << datastore 
    authfacade >> Edge(reverse=True, id="edge_ec2other") << kafka 
    haproxy >> Edge(reverse=True, id="edge_kafka") << owlyweb >> owly