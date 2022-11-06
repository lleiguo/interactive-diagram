
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
        centerH
    };
  }

  var svgURL = "https://github.hootops.com/raw/lei-guo/interactive-diagram/master/diagrams/hootsuite_2019.svg"
  require([svgURL], function(data){
        const svg = d3.select(data.documentElement);
        const svgNode = svg.node();
        const svgBBox = getElementBBox(svgNode);
        
      const ec2 = svg.selectAll('[id^=ec2]').nodes();
      const servicePods = svg.select('#servicePods').node();
      const servicePodsPos = getElementBBox(servicePods);

      console.log(svgNode);

      const ec2Migration = (i) => {
        d3.select(ec2[i])
        .transition()
        .duration(150)
        .attrTween('transform', function() {
          const currentPos = getElementBBox(ec2[i]);
          const x = servicePodsPos.x - currentPos.x + (currentPos.w)* (i+1);
          const y = servicePodsPos.y - currentPos.y;
          return d3.interpolateString(`translate(0, 0)`, `translate(${x}, ${y})`);
        })
        .on('end', function() {
            d3.select(ec2[i])
            .select("image")
            .attr('xlink:href', 'https://raw.githubusercontent.com/mingrammer/diagrams/834899659ae2e4f9f0d0dd9d01a4d7f31513d726/resources/k8s/compute/pod.png')

            d3.select('[id=clust8]').size([400, 300]);
            d3.select('[id=clust8]').node().appendChild(ec2[i]);
            if(i < ec2.length - 1) {
              ec2Migration(i + 1);
            } 
          });
      }
    
      const removeSkyline = () => {
        const skylineCluster = svg.selectAll('[id^=skyline]').nodes();

        skylineCluster.forEach((child) => {
          console.log(child)
          d3.select(child)
          .style("opacity", 1)
          .transition()
          .duration(2000)
          .delay(1000)
          .style("opacity", 0)
          .on('end', function() {
            d3.select(child).remove();
          });
        });
      }

      svg.selectAll('[id=clust4]').on("click", function() {
        ec2Migration(0);
      });

      svg.selectAll('[id=skyline]').on("click", function() {
        removeSkyline();
      });
    });