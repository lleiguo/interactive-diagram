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
  "https://raw.githubusercontent.com/lleiguo/interactive-diagram/main/base.svg";
d3.xml(svgURL).then((data) => {
  d3.select("#svg-container").node().append(data.documentElement);

  const svg = d3.select("svg");

  //transform a set of nodes to new location with new style
  const transformPosAndStyle = (nodes, index, moveTo, tag, attr, value) => {
    const node = nodes[index];
    d3.select(node)
      .transition()
      .duration(5000)
      .attrTween("transform", function () {
        const nodeBox = getElementBBox(node);
        const x = 125;
        const y = moveTo.y - nodeBox.y;
        return d3.interpolateString(`translate(0, 0)`, `translate(${x}, ${y})`);
      })
      .on("end", () => {
        d3.select("[id=clust8]").node().appendChild(node);
        d3.select(node).select(tag).attr(attr, value);
      })
      .on("start", function () {
        if (index < nodes.length - 1) {
          transformPosAndStyle(nodes, index + 1, moveTo, tag, attr, value);
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
    path.lineTo(elementBox.x, elementBox.y + elementBox.h);
    path.closePath();

    element.attr("d", path);
  };

  //Remove the given nodes with animation
  const remove = (nodes) => {
    nodes.forEach((node) => {
      d3.select(node)
        .style("opacity", 1)
        .transition()
        .duration(2000)
        .delay(1000)
        .style("opacity", 0)
        .on("end", function () {
          d3.select(node).remove();
        });
    });
  };

  // EC2 migration animation
  d3.select("[id=cluster_ec2]").on("click", function () {
    const workerNode = d3.select("[id=cluster_k8s_worker]").select("path");
    const ec2 = svg.selectAll("[id^=ec2]").nodes();

    expand(workerNode, ec2.length + 6);

    const servicePods = d3.select("#servicePods").node();
    const servicePodsBox = getElementBBox(servicePods);
    const newImageLink =
      "https://raw.githubusercontent.com/mingrammer/diagrams/834899659ae2e4f9f0d0dd9d01a4d7f31513d726/resources/k8s/compute/pod.png";

    transformPosAndStyle(
      ec2,
      0,
      servicePodsBox,
      "image",
      "xlink:href",
      newImageLink
    );
  });

  // Skyline deprecation animation
  d3.select("[id=skyline]").on("click", function () {
    const skylineCluster = svg.selectAll("[id^=skyline]").nodes();
    remove(skylineCluster);
  });

  // Consolidate Aperture
  d3.select("[id=aperture]").on("click", function () {
    const apertureCluster = svg.selectAll("[id^=aperture]").nodes();
    remove(apertureCluster);
  });
});
