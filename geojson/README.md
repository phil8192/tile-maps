`counties.geojson` contains the 48 [ceremonial counties](https://en.wikipedia.org/wiki/Ceremonial_counties_of_England) of England.
after reform, many of these counties no longer have any administrative function and as such can not be found on the #
[ONS Geography portal]([http://geoportal.statistics.gov.uk/) for example. Instead, the exist in current form usually as operating
regions for emergency services and previously as Royal mail postal counnties (which were later abandoned in favour of postcodes).

This data was obtained from [doogal.co.uk](https://www.doogal.co.uk/Counties.php). in KML format and later converted to GeoJSON. 


```
cat counties.geojson |json_pp |grep Name |wc -l
48
```
