# 2019.py
from diagrams import Diagram, Cluster

from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS, Aurora,  ElasticacheForRedis, ElasticacheForMemcached
from diagrams.aws.network import  Route53, CloudFront, ALB, NLB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.onprem.network import Zookeeper
from diagrams.onprem.queue import Kafka

from diagrams.k8s.compute import Pod

graph_attr = {
    "fontsize": "60",
    "bgcolor": "transparent"
}

with Diagram("Hootsuite 2022", show=True, direction="TB", graph_attr=graph_attr, outformat=["png", "svg"]):

    # Major components
    with Cluster("Edge"):
        dns = Route53("dns")

    with Cluster("Aperture"):
        apertureNLB = NLB("Aperture NLB")
        apertureCDN = CloudFront("Aperture CDN")
        traefik = [AutoScaling("Aperture Traefik"), AutoScaling("Dashboard Traefik"),AutoScaling("Webhook Traefik")]

    with Cluster("Auth Facade"):
        authFacade = AutoScaling("Auth Facade")
        authFacadeALB = ALB("Auth Facade ALB")

    with Cluster("EC2 Services"):
       EC2Services = [EC2("Dashboard-Geard")]

    with Cluster("Kubernetes Cluster"):
        with Cluster("Ingress Nodes"):
            k8sIngress = NLB("Ingress LB")
            traefikPods = Pod("Traefik")
        with Cluster("Worker Nodes"):
            servicePods = [Pod("100+ Microservices"),
                    Pod("Dashboard-Web"),
                    Pod("Dashboard-Gear"),
                    Pod("Dashboard-Cron"),
                    Pod("Member"),
                    Pod("SCUM"),
                    Pod("Billing"),
                    Pod("Message Achieve"),
                    Pod("Message Review"),
                    Pod("Scheduled Data"),
                    Pod("Core"),
                    Pod("TOPS"),
                    Pod("GSS"),
                    Pod("HootSupport"),
                    Pod("Push Notifications"),
                    Pod("Crypto"),
                    Pod("Amplify")] 
            apertureAuthz = Pod("Aperture Authz") 

    with Cluster("Data Storage"):
       rds = RDS("RDS")
       aurora = Aurora("Aurora")
       memcached =  ElasticacheForMemcached("Memcached")
       redis =  ElasticacheForRedis("Redis")
       s3 = S3("S3")

    with Cluster("Event Bus (Kafka)"):
        kafka = Kafka("Kafka")

# Path: 
    dns >> apertureCDN >> apertureNLB >> traefik >> k8sIngress
    dns >> authFacadeALB >> authFacade >> k8sIngress
    traefikPods >> servicePods >> rds, aurora, memcached, redis, s3, kafka
