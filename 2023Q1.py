# 2019.py
from xml.sax.xmlreader import AttributesImpl
from diagrams import Diagram, Cluster, Edge

from diagrams.aws.compute import EC2, AutoScaling, ECS, EC2ElasticIpAddress
from diagrams.aws.database import RDS, Aurora, ElasticacheForRedis, ElasticacheForMemcached
from diagrams.aws.network import Route53, ALB, NLB, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ManagedStreamingForKafka


from diagrams.k8s.compute import Pod
from diagrams.onprem.queue import Kafka 
from diagrams.onprem.network import Zookeeper


graph_attr = {
    "fontsize": "60",
    "bgcolor": "transparent"
}

with Diagram(filename="2023Q1", show=False, direction="TB", graph_attr=graph_attr, outformat=["png"]):

    with Cluster(label="Production/Staging", direction="TB", graph_attr={"id": "cluster_production"}):

        with Cluster("Stateful Services", graph_attr={"id": "cluster_data_storage"}):
            rds = RDS("Aurora 5.7")
            cache = ElasticacheForRedis("Redis")
            msk = ManagedStreamingForKafka("MSK")
            datastore = [rds, cache]

        with Cluster("EC2 Services", graph_attr={"id": "cluster_ec2"}):
                EC2Services = [EC2("External API", id="ec2-ExternalAPI"),
                            EC2("Data Deletion", id="ec2-DataDeletion")]

        with Cluster("Vault"):
            vault = ECS("Vault", id="ec2-vault")

    with Cluster("Kubernetes Cluster", graph_attr={"id": "cluster_k8s"}):
        with Cluster("Ingress", graph_attr={"id": "cluster_edge_aperture"}):
            apertureNLB = NLB("Aperture NLB", id="cluster_edge_apertureNLB")
            traefik = AutoScaling("Aperture Traefik",
                                id="cluster_edge_traefik")
            k8sIngress = NLB("Traefik Ingress")

        servicePods = [Pod("Dashboard PHP", id="dashboard"), Pod("Amplify", id="amplify"), Pod("Owly", id="owlyPod"), Pod("Auth Facade", id="authfacade"), Pod("Webhook Egress Proxy", id="webhookEgressProxy")]
        servicePod = Pod("Other Microservices Pods... ", id="servicePods")

# Path:
    apertureNLB >> Edge(reverse=True, id="cluster_edge") >> traefik >> k8sIngress
    traefik >> Edge(reverse=True, id="edge_ec2_traefik") >> EC2Services
    servicePod >> Edge(reverse=True) << msk
    vault >> Edge(reverse=True) << servicePods
    k8sIngress >> Edge(reverse=True) << servicePods, servicePod
    servicePod >> Edge(reverse=True, id="edge_datastore") << datastore