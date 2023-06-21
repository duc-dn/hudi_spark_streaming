## Hudi with spark-streaming
---
- Copy spark lib vào spark container
```
docker cp ./docker-config/spark/lib/. master:/opt/spark/jars

docker cp ./docker-config/spark/lib/. worker-a:/opt/spark/jars
```
---
- Test với trino
```
docker exec -it trino bash

trino

use minio.default;

show tables;
```
- Example with ux_data_click 
```
select events[1].segmentation from ux_click1;

select distinct events[1].segmentation.parent from ux_click1;

select events[1].segmentation.parent from ux_click1;
```
---
- Test với spark
```
df = spark.read.format("delta").load("s3a://datalake/hudi-table-name")

df.createOrReplaceTempView("hudi-table-name")

spark.sql("select count(*) as num_record from hudi-table-name").show()
```
