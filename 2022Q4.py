# 2019.py
from xml.sax.xmlreader import AttributesImpl
from diagrams import Diagram, Cluster, Edge

from diagrams.aws.compute import EC2, AutoScaling, EC2ElasticIpAddress
from diagrams.aws.database import RDS, Aurora, ElasticacheForRedis
from diagrams.aws.network import Route53, ALB, NLB, CloudFront
from diagrams.aws.storage import S3

from diagrams.k8s.compute import Pod
from diagrams.onprem.queue import Kafka 
from diagrams.onprem.network import Zookeeper


graph_attr = {
    "fontsize": "250",
    "bgcolor": "transparent"
}

with Diagram(filename="2022Q4", show=False, direction="TB", graph_attr=graph_attr, outformat=["svg"]):

    with Cluster(label="Production/Staging", direction="TB", graph_attr={"id": "cluster_production"}):

        with Cluster("Aperture", graph_attr={"id": "cluster_edge_aperture"}):
            traefik = AutoScaling("Traefik Aperture",
                                id="ec2_aperture_traefik")
            authFacade = AutoScaling("Auth Facade", id="ec2_aperture_authfacade")

        with Cluster("EC2 Services", graph_attr={"id": "cluster_ec2"}):
                EC2Services = [EC2("Auth Facade", id="ec2-AuthFacade"),
                            EC2("Webhook Egress Proxy", id="ec2-WebhookEgressProxy"),
                            EC2("External API", id="ec2-ExternalAPI"),
                            EC2("Data Deletion", id="ec2-DataDeletion")]

        with Cluster("Vault"):
            vault = EC2("Vault", id="ec2-vault")

        with Cluster("Event Bus (Kafka)", direction="LR", graph_attr={"id": "cluster_kafka"}):
            kafka = Kafka("Kafka")
            zookeeper = Zookeeper("Zookeeper")

        with Cluster("Stateful Services", graph_attr={"id": "cluster_data_storage"}):
            rds = RDS("Aurora 5.6")
            cache = ElasticacheForRedis("Redis")
            datastore = [rds, cache]

    with Cluster("Kubernetes Cluster", direction="TB", graph_attr={"id": "cluster_k8s"}):
            k8sIngress = NLB("Traefik Ingress")
            servicePods = [Pod("Dashboard PHP", id="dashboard"), Pod("Amplify", id="amplify")]
            servicePod = Pod("Other Microservices Pods... ", id="servicePods")

    with Cluster("US-West-1 - Owly", graph_attr={"id": "cluster_owly"}):
        haproxy = NLB("HAProxy", id="haproxy")
        owlyweb = EC2("Owly Web", id="owlyweb")
        owlydb = EC2("Owly Analytics", id="owly-analytics")

# Path:
    traefik >> k8sIngress
    authFacade >> k8sIngress
    traefik >> Edge(reverse=True, id="edge_ec2_traefik") >> EC2Services
    servicePod >> Edge(reverse=True) << kafka
    vault >> Edge(reverse=True) << servicePods
    k8sIngress >> Edge(reverse=True) << servicePod, servicePods
    servicePod >> Edge(reverse=True, id="edge_datastore") << datastore