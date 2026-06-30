"""
=========================================================
项目名称：电商用户行为数据平台
文件名称：etl_sparksql.py

功能说明：
1. 读取阿里天池用户行为数据
2. 中文字段统一转换为英文
3. 数据清洗（去重、去空值）
4. Unix 时间戳转换为标准时间
5. 商品价格分层
6. 导出清洗后的数据（写入 Hive）

=========================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_unixtime, when, lit, to_timestamp,
    count as spark_count, sum as spark_sum
)
import logging

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =====================================================
# 0. 创建 SparkSession
# =====================================================

def create_spark_session():
    """创建 SparkSession，启用 Hive 支持"""
    return SparkSession.builder \
        .appName("EcommerceETL") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("hive.metastore.uris", "thrift://localhost:9083") \
        .enableHiveSupport() \
        .getOrCreate()


# =====================================================
# 1. Extract —— 读取原始数据
# =====================================================

def extract_data(spark):
    """读取原始 CSV 数据"""
    input_path = "UserBehavior_2025.csv"
    logger.info(f"正在读取数据：{input_path}")

    df = spark.read.csv(
        input_path,
        header=True,
        inferSchema=True,
        sep=","
    )

    logger.info(f"原始数据量：{df.count()} 条")
    return df


# =====================================================
# 2. Transform —— 数据清洗与转换
# =====================================================

def transform_data(df):
    """数据清洗与转换"""

    # =====================================================
    # 2.1 字段重命名（中文 → 英文）
    # =====================================================
    logger.info("字段重命名（中文 → 英文）...")
    df = df.select(
        col("用户ID").alias("user_id"),
        col("商品ID").alias("item_id"),
        col("品牌").alias("brand"),
        col("品牌ID").alias("brand_id"),
        col("商品名称").alias("item_name"),
        col("商品类别").alias("category"),
        col("商品类目ID").alias("category_id"),
        col("行为类型").alias("behavior"),
        col("时间戳").alias("timestamp"),
        col("售价").alias("price")
    )

    # =====================================================
    # 2.2 数据清洗（去重、去空值）
    # =====================================================
    logger.info("开始数据清洗...")

    # 去重
    before_dedup = df.count()
    df = df.dropDuplicates()
    after_dedup = df.count()
    logger.info(f"去重前：{before_dedup} 条，去重后：{after_dedup} 条，去除：{before_dedup - after_dedup} 条")

    # 去空值
    before_null = df.count()
    df = df.filter(
        col("user_id").isNotNull() &
        col("item_id").isNotNull() &
        col("brand_id").isNotNull() &
        col("category_id").isNotNull() &
        col("price").isNotNull() &
        (col("price") > 0)
    )
    after_null = df.count()
    logger.info(f"去空前：{before_null} 条，去空后：{after_null} 条，去除：{before_null - after_null} 条")

    # =====================================================
    # 2.3 时间格式转换
    # =====================================================
    logger.info("Unix 时间戳转换为标准时间...")
    df = df.withColumn(
        "datetime",
        from_unixtime(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
    )

    # =====================================================
    # 2.4 商品价格分层（Business Rule）
    # =====================================================
    logger.info("商品价格分层...")
    df = df.withColumn(
        "price_level",
        when(col("price") < 500, "低价")
        .when((col("price") >= 500) & (col("price") < 2000), "中价")
        .when((col("price") >= 2000) & (col("price") < 5000), "高价")
        .otherwise("奢侈")
    )

    return df


# =====================================================
# 3. Load —— 导出清洗后的数据
# =====================================================

def load_data(df):
    """导出清洗后的数据"""

    # 写入 Hive（方式一：直接写入 Hive 表）
    output_table = "ecommerce_dw.ods_user_behavior"
    logger.info(f"正在写入 Hive 表：{output_table}")

    # 创建数据库（如果不存在）
    df._jdf.sparkSession().sql("CREATE DATABASE IF NOT EXISTS ecommerce_dw")

    df.write.mode("overwrite").saveAsTable(output_table)
    logger.info(f"写入成功！数据量：{df.count()} 条")

    # 同时导出 CSV 备份（方式二）
    output_csv_path = "clean_user_behavior.csv"
    logger.info(f"正在导出 CSV：{output_csv_path}")

    df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .option("encoding", "utf-8") \
        .csv(output_csv_path)

    logger.info(f"CSV 导出成功！")


# =====================================================
# 4. 主流程
# =====================================================

def main():
    """ETL 主流程"""

    logger.info("=" * 60)
    logger.info("========== ETL 开始 ==========")
    logger.info("=" * 60)

    # 创建 SparkSession
    spark = create_spark_session()

    try:
        # 1. Extract —— 读取原始数据
        df = extract_data(spark)

        # 2. Transform —— 数据清洗与转换
        df = transform_data(df)

        # 3. Load —— 导出清洗后的数据
        load_data(df)

        # =====================================================
        # 打印结果预览
        # =====================================================
        logger.info("\n" + "=" * 60)
        logger.info("最终结果前5条：")
        df.show(5, truncate=False)

        logger.info("=" * 60)
        logger.info(f"最终数据量：{df.count()} 条")
        logger.info("========== ETL 完成 ==========")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"ETL 执行失败：{e}")
        raise
    finally:
        spark.stop()


# =====================================================
# 程序入口
# =====================================================

if __name__ == "__main__":
    main()