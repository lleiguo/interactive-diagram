# 2019.py
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

with Diagram("Hootsuite 2019", show=False, direction="TB", graph_attr=graph_attr, outformat=["svg"]):

    with Cluster(label="Edge"):
        dns = Route53("dns")

    with Cluster("Auth Facade"):
        authFacade = AutoScaling("Auth Facade")
        authFacadeALB = ALB("Auth Facade ALB")

    with Cluster("Aperture"):
        apertureNLB = NLB("Aperture NLB", id="apertureNLB")
        traefik = AutoScaling("Aperture Traefik",  id="traefik")

    ec2attributes = {
        "id": "ec2"
    }
    with Cluster("EC2 Services"):
        EC2Services = [EC2(label="Dashboard-Web", id="ec2-Dashboard-Web"),
                       EC2("Dashboard-Gear", id="ec2-Dashboard-Gear"),
                       EC2("Dashboard-Cron", id="ec2-Dashboard-Cron"),
                       EC2("Member", id="ec2-Member"),
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

    with Cluster("Skyline"):
        skylineLB = ALB("Skyline ALB", id="skylineLB")
        skylineBridge = EC2("Skyline Bridge", id="skylineBridge")

    with Cluster("Kubernetes Cluster"):
        with Cluster("Ingress Nodes"):
            k8sIngress = NLB("Ingress LB")
            traefikPods = Pod("Traefik Pods", id="traefikPods")
        with Cluster(label="Worker Nodes"):
            servicePod = Pod("More service pods... ", id="servicePods")
            servicePods = [Pod("Service POD"), Pod("Service POD"), Pod("Service POD"), Pod("Service POD")]

    with Cluster("Event Bus (Kafka)"):
        with Cluster("VPC"):
            vpcLocal = Kafka(id="VPC Local", label="VPC Local")
            vpcAgg = Kafka(id="VPC Aggregate", label="VPC Aggregate")
        with Cluster("EC2 Classic aka Limbo"):
            limboLocal = Kafka(id="Limbo Local", label="Limbo Local")
            limboAgg = Kafka(id="Limbo Aggregate", label="Limbo Aggregate")
        
        kafka = [vpcLocal, vpcAgg,limboLocal,limboAgg]
        vpcLocal >> limboAgg
        limboLocal >> vpcAgg

    with Cluster("Data Storage"):
        rds = RDS("RDS")
        aurora = Aurora("Aurora")
        memcached = ElasticacheForMemcached("Memcached")
        redis = ElasticacheForRedis("Redis")
        s3 = S3("S3")
        mongodb = EC2("Mongo")


# Path:
    EC2Services >> skylineLB >> skylineBridge >> k8sIngress
    dns >> apertureNLB >> traefik >> k8sIngress
    dns >> authFacadeALB >> authFacade >> k8sIngress
    k8sIngress >> traefikPods >> servicePod >> s3, rds, aurora, memcached, redis, kafka
    servicePod << Edge(color="red", style="dashed", node=servicePod, forward=True, reverse=True) << kafka

