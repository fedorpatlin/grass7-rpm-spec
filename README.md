# grass7-rpm-spec
SPEC file that builds GRASS GIS 7.0.3 rpm package for Centos 6

[GRASS GIS](https://grass.osgeo.org/), commonly referred to as GRASS (Geographic Resources Analysis Support System), is a free and open source Geographic Information System (GIS) software suite used for geospatial data management and analysis.

## Requirements
Building and installing GRASS GIS requires enabled EPEL-repository

  yum install -y epel-release

Also required gdal-1.11 package not available on centos6. You may take in from [github](https://github.com/fedorpatlin/gdal-rpm)
