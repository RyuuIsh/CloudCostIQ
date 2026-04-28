def generate_recommendations(service_costs):
    recommendations = []

    for service in service_costs:
        name = service["service"]
        cost = service["cost"]

        # EC2
        if "EC2" in name or "Elastic Compute Cloud" in name:
            if cost >= 20:
                recommendations.append({
                    "severity": "High",
                    "category": "Compute Optimization",
                    "message": "High EC2 cost detected. Review running instances, stop unused instances, and consider right-sizing."
                })
            elif cost >= 5:
                recommendations.append({
                    "severity": "Medium",
                    "category": "Compute Optimization",
                    "message": "Moderate EC2 cost detected. Check if all running instances are required."
                })

        # EBS
        elif "EBS" in name or "Elastic Block Store" in name:
            if cost >= 10:
                recommendations.append({
                    "severity": "High",
                    "category": "Storage Optimization",
                    "message": "High EBS cost detected. Check for unattached volumes and oversized storage."
                })
            elif cost >= 3:
                recommendations.append({
                    "severity": "Medium",
                    "category": "Storage Optimization",
                    "message": "EBS usage detected. Review unattached volumes and old snapshots."
                })

        # Load Balancer
        elif "Load Balancer" in name or "Elastic Load Balancing" in name:
            recommendations.append({
                "severity": "Medium",
                "category": "Network Optimization",
                "message": "Load Balancer cost detected. Review idle or unused ALBs/NLBs."
            })

        # NAT Gateway
        elif "NAT Gateway" in name or "NAT" in name:
            recommendations.append({
                "severity": "High",
                "category": "Network Optimization",
                "message": "NAT Gateway cost detected. Review private subnet traffic and consider VPC endpoints where possible."
            })

        # Data Transfer
        elif "Data Transfer" in name:
            recommendations.append({
                "severity": "Medium",
                "category": "Data Transfer Optimization",
                "message": "Data transfer cost detected. Use caching, CloudFront, and region-aware architecture to reduce transfer charges."
            })

        # S3
        elif "S3" in name or "Simple Storage Service" in name:
            if cost >= 5:
                recommendations.append({
                    "severity": "Medium",
                    "category": "Storage Optimization",
                    "message": "S3 cost detected. Review storage classes, lifecycle policies, and unused objects."
                })
            elif cost > 0:
                recommendations.append({
                    "severity": "Low",
                    "category": "Storage Optimization",
                    "message": "S3 usage detected. Consider lifecycle rules for long-term storage optimization."
                })

        # CloudFront
        elif "CloudFront" in name:
            recommendations.append({
                "severity": "Low",
                "category": "CDN Optimization",
                "message": "CloudFront usage detected. Review cache hit ratio and compression settings."
            })

        # Route 53
        elif "Route 53" in name:
            recommendations.append({
                "severity": "Low",
                "category": "DNS Optimization",
                "message": "Route 53 cost detected. Review hosted zones and unused DNS records."
            })

    if not recommendations:
        recommendations.append({
            "severity": "Info",
            "category": "Cost Health",
            "message": "No major optimization opportunities detected based on current service costs."
        })

    return recommendations