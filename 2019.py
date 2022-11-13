# 2019.py
from xml.sax.xmlreader import AttributesImpl
from diagrams import Diagram, Cluster, Edge

from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS, Aurora, ElasticacheForRedis, ElasticacheForMemcached
from diagrams.aws.network import ELB, Route53, ALB, NLB, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.security import WAF

from diagrams.k8s.compute import Pod
from diagrams.onprem.queue import Kafka

graph_attr = {
    "fontsize": "60",
    "bgcolor": "transparent"
}

with Diagram(filename="base", show=False, direction="TB", graph_attr=graph_attr, outformat=["svg"]):

    with Cluster(label="Edge", direction="LR", graph_attr={"id": "cluster_edge"}):
        dns = Route53("dns", id="cluster_edge_dns")
        cdn = CloudFront("cdn", id="cluster_edge_cdn")
        waf = WAF("waf", id="cluster_edge_waf")

        with Cluster("Auth Facade", graph_attr={"id": "cluster_edge_auth_facade"}):
            authFacade = AutoScaling("Auth Facade", id="cluster_edge_aperture")
            authFacadeALB = ALB("Auth Facade ALB",
                                id="cluster_edge_apertureALB")

        with Cluster("Aperture", graph_attr={"id": "cluster_edge_aperture"}):
            apertureNLB = NLB("Aperture NLB", id="cluster_edge_apertureNLB")
            traefik = AutoScaling("Aperture Traefik",
                                  id="cluster_edge_traefik")

        with Cluster("Dashboard", graph_attr={"id": "cluster_edge_dashboard"}):
            dashboardENLB = NLB("Dashboard External NLB",
                                id="cluster_edge_dashboardENLB")
            dashboardINLB = NLB("Dashboard Internal NLB",
                                id="cluster_edge_dashboardENLB")
            dashboardELB = NLB("Dashboard ELB", id="cluster_edge_dashboardELB")

    with Cluster("Kubernetes Cluster", graph_attr={"id": "cluster_k8s"}):
        with Cluster("Ingress Auto Scaling Group", graph_attr={"id": "cluster_k8s_ingress"}):
            k8sIngress = NLB("Ingress LB")
            traefikPods = Pod("Traefik Pods", id="traefikPods")
        with Cluster(label="Managed Worker Nodes Auto Scaling Group", graph_attr={"id": "cluster_k8s_worker"}):
            servicePod = Pod("Service Pods... ", id="servicePods")
            servicePods = [Pod("Service POD", id="service_pod"), Pod(
                "Service POD", id="service_pod"), Pod("Service POD", id="service_pod"), Pod("Service POD", id="service_pod")]

    with Cluster("EC2 Services", direction="LR", graph_attr={"id": "cluster_ec2"}):
        with Cluster("Dashboard", direction="LR", graph_attr={"id": "cluster_dashboard_ec2"}):
            dashboardWeb = EC2("Dashboard-Web", id="dashboard-Web")
            EC2Dashboard = [dashboardWeb,
                            EC2("Dashboard-Gear", id="dashboard-Gear"),
                            EC2("Dashboard-Cron", id="dashboard-Cron")]

        with Cluster("Other Services", direction="LR", graph_attr={"id": "cluster_ec2_other"}):
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
    dns >> Edge(id="cluster_edge") >> cdn >> Edge(id="cluster_edge") >> waf >> Edge(id="cluster_edge") >> [
        dashboardENLB, authFacadeALB, apertureNLB]
    [dashboardENLB, dashboardINLB] >> dashboardELB >> dashboardWeb
    dashboardWeb, EC2Services >> Edge(reverse=True, id="edge_ec2_skyline") >> skylineLB >> Edge(
        reverse=True, id="edge_skyline") >> skylineBridge >> Edge(reverse=True, id="edge_skyline") >> k8sIngress
    apertureNLB >> Edge(reverse=True, id="cluster_edge_dns") >> traefik >> k8sIngress
    traefik >> Edge(reverse=True, id="edge_ec2_traefik") >> EC2Services, EC2Dashboard
    authFacadeALB >> Edge(reverse=True, id="cluster_edge_dns") >> authFacade >> Edge(reverse=True, id="cluster_edge_dns") >> k8sIngress
    servicePod >> Edge(reverse=True) << kafka
    k8sIngress >> traefikPods >> Edge(reverse=True) << servicePods
    servicePod >> Edge(reverse=True, id="edge_datastore") << mongodb
