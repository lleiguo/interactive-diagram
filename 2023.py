# 2019.py
from diagrams import Diagram, Cluster

from diagrams.aws.database import RDS, Aurora, ElasticacheForRedis, ElasticacheForMemcached
from diagrams.aws.network import Route53, CloudFront, NLB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ManagedStreamingForKafka

from diagrams.k8s.compute import Pod

graph_attr = {
    "fontsize": "60",
    "bgcolor": "transparent"
}

with Diagram("Hootsuite 2023", show=True, direction="TB", graph_attr=graph_attr, outformat=["png", "dot"]):

    # Major components
    with Cluster("Edge"):
        dns = Route53("dns")
        cdn = CloudFront("CDN/WAF")

    with Cluster("Kubernetes Cluster"):
        with Cluster("Ingress Nodes"):
            k8sIngress = NLB("Ingress LB")
            traefikPods = Pod("Traefik")
        with Cluster("Worker Nodes"):
            servicePods = [Pod("200+ Microservices")] 

    with Cluster("Data Storage"):
       rds = RDS("RDS")
       aurora = Aurora("Aurora")
       memcached =  ElasticacheForMemcached("Memcached")
       redis =  ElasticacheForRedis("Redis")
       s3 = S3("S3")

    with Cluster("Event Bus (MSK)"):
        kafka = ManagedStreamingForKafka("MSK")

# Path: 
    dns >> cdn >> k8sIngress >> traefikPods >> servicePods >> [rds, aurora, memcached, redis, s3, kafka]
    servicePods >> kafka