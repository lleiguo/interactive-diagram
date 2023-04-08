const getElementBBox = (element) => {
  if (!element) {
    return;
  }
  const w = element.getBBox().width;
  const h = element.getBBox().height;

  const x = element.getBBox().x;
  const y = element.getBBox().y;

  const centerW = x + w / 2;
  const centerH = y + h / 2;

  return {
    h,
    w,
    x,
    y,
    centerW,
    centerH,
  };
};

var svgURL =
  "https://raw.githubusercontent.com/lleiguo/interactive-diagram/main/2022Q4.svg";
d3.xml(svgURL).then((data) => {
  d3.select("#svg-container").node().append(data.documentElement);

  const svg = d3.select("svg");

  //transform a set of nodes to new location with new style
  const transformPosAndStyle = (
    nodes,
    index,
    moveToX,
    moveToY,
    tag,
    attr,
    value
  ) => {
    const node = nodes[index];
    d3.select(node)
      .transition()
      .duration(5000)
      .attrTween("transform", function () {
        const nodeBox = getElementBBox(node);
        return d3.interpolateString(
          `translate(0, 0)`,
          `translate(${moveToX}, ${moveToY - nodeBox.y})`
        );
      })
      .on("end", () => {
        d3.select(node).select(tag).attr(attr, value);
      })
      .on("start", function () {
        if (index < nodes.length - 1) {
          transformPosAndStyle(
            nodes,
            index + 1,
            moveToX,
            moveToY,
            tag,
            attr,
            value
          );
        }
      });
  };

  //Expand the given element size by times
  const expand = (element, times) => {
    const elementBox = getElementBBox(element.node());

    const path = d3.path();
    path.moveTo(elementBox.x, elementBox.y);
    path.lineTo(elementBox.x + elementBox.w * (times - 1), elementBox.y);
    path.lineTo(
      elementBox.x + elementBox.w * (times - 1),
      elementBox.y + elementBox.h
    );
    path.lineTo(elementBox.x - elementBox.w * 1.2, elementBox.y + elementBox.h);
    path.lineTo(elementBox.x - elementBox.w * 1.2, elementBox.y);
    path.closePath();

    element.attr("d", path);
  };

  //Remove the given nodes with animation
  const remove = (nodes) => {
    nodes.forEach((node) => {
      d3.select(node)
        .style("opacity", 1)
        .transition()
        .duration(4000)
        .delay(2000)
        .style("opacity", 0)
        .on("end", function () {
          d3.select(node).remove();
        });
    });
  };

  // EC2 migration animation
  d3.select("[id=ccluster_owly]").on("click", function () {
    const workerCluster = d3.select("[id=cluster_k8s]");
    const ec2 = svg.selectAll("[id^=ec2]").nodes();

    const moveTo = getElementBBox(d3.select("[id=servicePods]").node());
    const newImageLink =
      "https://raw.githubusercontent.com/mingrammer/diagrams/834899659ae2e4f9f0d0dd9d01a4d7f31513d726/resources/k8s/compute/pod.png";

    const currentParentBox = getElementBBox(
      d3.select("[id=cluster_ec2_other]").node()
    );
    const newParentBox = getElementBBox(workerCluster.node());
    const x = moveTo.x - currentParentBox.x - newParentBox.x;
    const y = moveTo.y;

    transformPosAndStyle(
      ec2,
      0,
      x + 150,
      y,
      "image",
      "xlink:href",
      newImageLink
    );

    expand(d3.select("[id=cluster_k8s]").select("path"), ec2.length);
    expand(workerCluster.select("path"), ec2.length);
    remove(d3.selectAll("[id*=edge_ec2_]").nodes());
    remove(d3.selectAll("[id=service_pod]").nodes());
    d3.select("[id=servicePods]").remove();
    d3.select("[id=cluster_ec2]").remove();
    d3.select("[id=cluster_ec2_other]").remove();
  });

  // Skyline deprecation animation
  d3.select("[id=cluster_skyline]").on("click", function () {
    const skylineCluster = svg.selectAll("[id*=skyline]").nodes();
    remove(skylineCluster);
    move(d3.selectAll("[id*=cluster_edge]").nodes(), 0, 400);
    move(d3.selectAll("[id*=dashboard_ec2]").nodes(), 0, 300);
  });

  const move = (element, x, y) => {
    element.forEach((node) => {
      d3.select(node)
        .transition()
        .duration(5000)
        .attrTween("transform", function () {
          const nodeBox = getElementBBox(node);
          return d3.interpolateString(
            `translate(0, 0)`,
            `translate(${x}, ${y})`
          );
        });
    });
  };

  // Consolidate Aperture
  d3.select("[id=cluster_aperture]").on("click", function () {
    const apertureCluster = svg.selectAll("[id*=aperture]").nodes();
    remove(apertureCluster);
  });

  d3.select("[id=cluster_dashboard_ec2]").on("click", function () {
    const currentParentBox = getElementBBox(
      d3.select("[id=cluster_dashboard_ec2]").node()
    );
    const moveTo = getElementBBox(d3.select("[id=ec2-Billing]").node());
    const newParentBox = getElementBBox(d3.select("[id=cluster_k8s_worker]").node());
    const x = moveTo.x - currentParentBox.x - newParentBox.x;
    const y = moveTo.y;

    transformPosAndStyle(
      svg.selectAll("[id^=dashboard_ec2]").nodes(),
      0,
      x,
      y+800,
      "image",
      "xlink:href",
      "https://raw.githubusercontent.com/mingrammer/diagrams/834899659ae2e4f9f0d0dd9d01a4d7f31513d726/resources/k8s/compute/pod.png"
    );

    remove(d3.selectAll("[id*=cluster_edge_dashboard]").nodes());
  });
});
