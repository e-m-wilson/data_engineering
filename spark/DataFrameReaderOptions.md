# Reading Files in PySpark

PySpark provides several ways to configure reader options. All of the following are valid approaches.

---

## 1. Chaining `.option()`

This is probably the most common style.

```python
people = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("./fakefriends-header.csv")
)
```

---

## 2. Using `.options()` for Multiple Options

This is cleaner when you have several options.

```python
people = (
    spark.read
    .options(header=True, inferSchema=True)
    .csv("./fakefriends-header.csv")
)
```

---

## 3. Passing Options Directly to the data source, i.e. `csv()`

The `csv()` reader accepts keyword arguments for many common options.

Many developers prefer this approach because everything is in one place.

```python
people = spark.read.csv(
    "./fakefriends-header.csv",
    header=True,
    inferSchema=True
)
```

---

## 4. Providing an Explicit Schema (Recommended for Production)

Instead of inferring the schema, define it explicitly.

```python
from pyspark.sql.types import *

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("friends", IntegerType(), True)
])

people = spark.read.csv(
    "./fakefriends-header.csv",
    header=True,
    schema=schema
)
```

### Why use an explicit schema?

- Faster than schema inference
- Avoids incorrect data type detection
- Produces more predictable and maintainable code
- Recommended for production workloads

---

# `inferSchema` vs `inferschema`

Spark option names are **case-insensitive**, so all of the following are equivalent:

```python
.option("inferSchema", True)
.option("inferschema", True)
.option("INFERSCHEMA", True)
```

The same applies to `header`:

```python
.option("header", True)
.option("HEADER", True)
.option("Header", True)
```

> **Convention:** Most PySpark documentation uses:
>
> - `inferSchema` (camelCase)
> - `header` (lowercase)

---

# Which Style Is Preferred?

For modern PySpark code, a concise and readable style is:

```python
people = spark.read.csv(
    "./fakefriends-header.csv",
    header=True,
    schema=schema
)
```

If you have several configuration options, using `.options()` keeps the code organized:

```python
people = (
    spark.read
    .options(
        header=True,
        schema=schema,
        sep=",",
        mode="PERMISSIVE"
    )
    .csv("./fakefriends-header.csv")
)
```

These are the styles you'll most commonly encounter in modern PySpark codebases.