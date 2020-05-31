import pandas as pd
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.mllib.recommendation import MatrixFactorizationModel
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col
from pyspark.sql.functions import udf

from Misc import generate_columns, concat_data_from_list, apply_hash, apply_abs

spark = SparkSession.builder \
        .master("local") \
        .appName("ExtremeBlueBT") \
        .config('spark.executor.heartbeatInterval', '3600')\
        .config('spark.executor.memory', '6g')\
        .getOrCreate()

location_path = '/Users/vladdragoi/Documents/ecommerce-data/'
data_path = location_path + 'data.csv'
cleaned_data_path = location_path + 'clean_data.csv'
results_data_path = location_path + 'results.csv'
model_path = location_path + 'model.data'

model_df = spark.read.csv(cleaned_data_path, header=True, inferSchema=True)

'''
StockCode - product id
Quantity - number of products purchased
CustomerID - user id
'''


(training, test) = model_df.randomSplit([0.8, 0.2])

#make stock code be a number
#would like to concatenate fields which are the same
#abs the quanity of -



# Build the recommendation model using ALS on the training data
# Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
als = ALS(maxIter=10, regParam=0.01, implicitPrefs=True, userCol="CustomerID", itemCol="StockCode", ratingCol='Quantity_Scaled',
          coldStartStrategy="drop")

model = als.fit(training)
model.save(model_path)


# Evaluate the model by computing the RMSE on the test data
predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="Quantity_Scaled",
                                predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = " + str(rmse))


userRecs = model.recommendForAllUsers(5)

df = userRecs.toPandas()
aggregated_df = generate_columns()
df = pd.concat([df, aggregated_df], axis=1)
for i in range(0, len(df.index)):
    result_list = df['recommendations'].values[i]
    df = concat_data_from_list(result_list, df, i)

df = df.drop(columns=['recommendations'])
df.to_csv(results_data_path, index=False)