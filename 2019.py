# 2019.py
from xml.sax.xmlreader import AttributesImpl
from diagrams import Diagram, Cluster, Edge

from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS, Aurora, ElasticacheForRedis, ElasticacheForMemcached
from diagrams.aws.network import ELB, Route53, ALB, NLB
from diagrams.aws.storage import S3

from diagrams.k8s.compute import Pod
from diagrams.generic.virtualization import Vmware
from diagrams.onprem.network import Zookeeper
from diagrams.onprem.queue import Kafka

graph_attr = {
    "fontsize": "60",
    "bgcolor": "transparent"
}

with Diagram(filename="base", show=False, direction="TB", graph_attr=graph_attr, outformat=["svg"]):

    with Cluster(label="Edge", direction="TB", graph_attr={"id": "cluster_edge"}):
        dns = Route53("dns", id="cluster_edge_dns")

        with Cluster("Auth Facade", graph_attr={"id": "cluster_edge_auth_facade"}):
            authFacade = AutoScaling("Auth Facade", id="cluster_edge_aperture")
            authFacadeALB = ALB("Auth Facade ALB", id="cluster_edge_apertureALB")

        with Cluster("Aperture", graph_attr={"id": "cluster_edge_aperture"}):
            apertureNLB = NLB("Aperture NLB", id="cluster_edge_apertureNLB")
            traefik = AutoScaling("Aperture Traefik",  id="cluster_edge_traefik")

    with Cluster("Kubernetes Cluster", graph_attr={"id": "cluster_k8s"}):
        with Cluster("Ingress Nodes", graph_attr={"id": "cluster_k8s_ingress"}):
            k8sIngress = NLB("Ingress LB")
            traefikPods = Pod("Traefik Pods", id="traefikPods")
        with Cluster(label="Worker Nodes", graph_attr={"id": "cluster_k8s_worker"}):
            servicePod = Pod("More service pods... ", id="servicePods")
            servicePods = [Pod("Service POD", id="service_pod"), Pod(
                "Service POD", id="service_pod"), Pod("Service POD", id="service_pod"), Pod("Service POD", id="service_pod")]

    with Cluster("EC2 Services", direction="LR", graph_attr={"id": "cluster_ec2"}):
        EC2Services = [EC2("Member", id="ec2-Member"),
                       EC2("SCUM", id="ec2-SCUM"),
                       EC2("Billing", id="ec2-Billing"),
                       EC2("Message Achieve", id="ec2-Message Achieve"),
                       EC2("Message Review", id="ec2-Message Review"),
                       EC2("Scheduled Data", id="ec2-Scheduled Data"),
                       EC2("Core", id="ec2-Core"),
                       EC2("TOPS", id="ec2-TOPS"),
                       EC2("GSS", id="ec2-GSS"),
                       EC2("HootSupport", id="ec2-HootSupport"),
                       EC2("Push Notifications", id="ec2-Push Notifications"),
                       EC2("Crypto", id="ec2-Crypto"),
                       EC2("Aperture Authz", id="ec2-Aperture Authz"),
                       EC2("Amplify", id="ec2-Amplify")]

    with Cluster("EC2 Dashboard", direction="LR", graph_attr={"id": "cluster_ec2_dashboard"}):
        EC2Dashboard = [EC2(label="Dashboard-Web", id="ec2-Dashboard-Web"),
                       EC2("Dashboard-Gear", id="ec2-Dashboard-Gear"),
                       EC2("Dashboard-Cron", id="ec2-Dashboard-Cron")]

    with Cluster("Skyline", direction="LR", graph_attr={"id": "cluster_skyline"}):
        skylineLB = ALB("Skyline ALB", id="skylineLB")
        skylineBridge = EC2("Skyline Bridge", id="skylineBridge")

    with Cluster("Event Bus (Kafka)", direction="LR", graph_attr={"id": "cluster_kafka"}):
        with Cluster("VPC", graph_attr={"id": "cluster_kafka_vpc"}):
            vpcLocal = Kafka(id="VPC Local", label="VPC Local")
            vpcAgg = Kafka(id="VPC Aggregate", label="VPC Aggregate")
        with Cluster("EC2 Classic aka Limbo", graph_attr={"id": "cluster_kafka_limbo"}):
            limboLocal = Kafka(id="Limbo Local", label="Limbo Local")
            limboAgg = Kafka(id="Limbo Aggregate", label="Limbo Aggregate")

        kafka = [vpcLocal, vpcAgg, limboLocal, limboAgg]
        vpcLocal >> limboAgg
        limboLocal >> vpcAgg

    with Cluster("Data Storage", graph_attr={"id": "cluster_data_storage"}):
        rds = RDS("RDS")
        aurora = Aurora("Aurora")
        memcached = ElasticacheForMemcached("Memcached")
        redis = ElasticacheForRedis("Redis")
        s3 = S3("S3")
        mongodb = EC2("Mongo")
        datastore = [rds, aurora, memcached, redis, s3, mongodb]


# Path:
    EC2Dashboard, EC2Services >> Edge(color="black", style="dashed",
                       node=servicePod, forward=True, reverse=True, id="edge_ec2_skyline") >> skylineLB >> Edge(color="black", style="dashed",
                       node=servicePod, forward=True, reverse=True, id="edge_skyline") >>  skylineBridge >> Edge(color="black", style="dashed",
                       node=servicePod, forward=True, reverse=True, id="edge_skyline") >> k8sIngress
    dns >> apertureNLB >> traefik >> k8sIngress
    traefik >> Edge(color="black", style="dashed",
                       node=servicePod, forward=True, reverse=True, id="edge_ec2_traefik") >> EC2Services, EC2Dashboard
    dns >> authFacadeALB >> authFacade >> k8sIngress
    servicePod >> Edge(color="black", style="dashed",
                       node=vpcLocal, forward=True, reverse=True) << kafka
    k8sIngress >> traefikPods >> Edge(
        color="black", style="dashed", node=servicePod, forward=True, reverse=True) << servicePods
    servicePod >> Edge(color="black", style="dashed",
                       node=servicePod, forward=True, reverse=True, id="edge_datastore") << datastore
