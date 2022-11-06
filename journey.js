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
  "https://raw.githubusercontent.com/lleiguo/interactive-diagram/main/diagrams/hootsuite_2019.svg";
d3.xml(svgURL).then((data) => {
  d3.select("#svg-container").node().append(data.documentElement);

  const svg = d3.select("svg");
  const ec2 = svg.selectAll("[id^=ec2]").nodes();
  const servicePods = d3.select("#servicePods").node();
  const servicePodsPos = getElementBBox(servicePods);
  const workerNode = d3.select("[id=clust8]").select("path");
  const workerNodePos = getElementBBox(workerNode.node());

  const ec2Migration = (i) => {
    d3.select(ec2[i])
      .transition()
      .duration(1000)
      .attrTween("transform", function () {
        const currentPos = getElementBBox(ec2[i]);
        const x = servicePodsPos.x - currentPos.x + currentPos.w * (i + 1);
        const y = servicePodsPos.y - currentPos.y;
        return d3.interpolateString(`translate(0, 0)`, `translate(${x}, ${y})`);
      })
      .on("end", function () {
        d3.select(ec2[i])
          .select("image")
          .attr(
            "xlink:href",
            "https://raw.githubusercontent.com/mingrammer/diagrams/834899659ae2e4f9f0d0dd9d01a4d7f31513d726/resources/k8s/compute/pod.png"
          );

        d3.select("[id=clust8]").node().appendChild(ec2[i]);

        const path = d3.path();
        path.moveTo(workerNodePos.x, workerNodePos.y);
        path.lineTo(
          workerNodePos.x + workerNodePos.w * (i + 1),
          workerNodePos.y
        );
        path.lineTo(
          workerNodePos.x + workerNodePos.w * (i + 1),
          workerNodePos.y + workerNodePos.h
        );
        path.lineTo(workerNodePos.x, workerNodePos.y + workerNodePos.h);
        path.closePath();
        console.log(path);

        workerNode.attr("d", path);

        if (i < ec2.length - 1) {
          ec2Migration(i + 1);
        }
      });
  };

  const removeSkyline = () => {
    const skylineCluster = svg.selectAll("[id^=skyline]").nodes();

    skylineCluster.forEach((child) => {
      console.log(child);
      d3.select(child)
        .style("opacity", 1)
        .transition()
        .duration(2000)
        .delay(1000)
        .style("opacity", 0)
        .on("end", function () {
          d3.select(child).remove();
        });
    });
  };

  d3.select("[id=clust4]").on("click", function () {
    ec2Migration(0);
  });

  d3.select("[id=skyline]").on("click", function () {
    removeSkyline();
  });
});
