*Note: This is llms-full.txt is not complete, please enter a Firecrawl API key to get the entire llms-full.txt at llmstxt.firecrawl.dev or you can access llms.txt via API with curl -X GET 'http://llmstxt.firecrawl.dev/https://lancedb.github.io/lancedb/python/python/?FIRECRAWL_API_KEY=fc-8b492ef4411549e894cd4b923a82e5fc' or llms-full.txt via API with curl -X GET 'http://llmstxt.firecrawl.dev/https://lancedb.github.io/lancedb/python/python//full?FIRECRAWL_API_KEY=fc-8b492ef4411549e894cd4b923a82e5fc'

# https://lancedb.github.io/lancedb/python/python/ llms-full.txt

# 404

**There isn't a GitHub Pages site here.**

If you're trying to publish one,
[read the full documentation](https://help.github.com/pages/)
to learn how to set up **GitHub Pages**
for your repository, organization, or user account.


[GitHub Status](https://githubstatus.com) —
[@githubstatus](https://twitter.com/githubstatus)

[![](<Base64-Image-Removed>)](/)[![](<Base64-Image-Removed>)](/)- [Creating datasets](notebooks/quickstart.html)
- [Versioning](notebooks/quickstart.html#versioning)
- [Vectors](notebooks/quickstart.html#vectors)
- [Read and Write Lance Dataset](read_and_write.html)
- [Lance Formats](format.html)
- [Arrays](arrays.html)
- [Integrations](integrations/integrations.html)
- [Performance Guide](performance.html)
- [API References](api/api.html)
- [Contributor Guide](contributing.html)
- [Examples](examples/examples.html)

[![_images/lance_logo.png](_images/lance_logo.png)](_images/lance_logo.png)

# Lance: modern columnar data format for ML [¶](\#lance-modern-columnar-data-format-for-ml "Permalink to this heading")

Lance is a columnar data format that is easy and fast to version, query and train on.
It’s designed to be used with images, videos, 3D point clouds, audio and of course tabular data.
It supports any POSIX file systems, and cloud storage like AWS S3 and Google Cloud Storage.
The key features of Lance include:

- **High-performance random access:** 100x faster than Parquet.

- **Vector search:** find nearest neighbors in under 1 millisecond and combine OLAP-queries with vector search.

- **Zero-copy, automatic versioning:** manage versions of your data automatically, and reduce redundancy with zero-copy logic built-in.

- **Ecosystem integrations:** Apache-Arrow, DuckDB and more on the way.


## Installation [¶](\#installation "Permalink to this heading")

You can install Lance via pip:

```
pip install pylance

```

For the latest features and bug fixes, you can install the preview version:

```
pip install --pre --extra-index-url https://pypi.fury.io/lancedb/ pylance

```

Preview releases receive the same level of testing as regular releases.

- [Creating datasets](notebooks/quickstart.html)
- [Versioning](notebooks/quickstart.html#versioning)
- [Vectors](notebooks/quickstart.html#vectors)
- [Read and Write Lance Dataset](read_and_write.html)
- [Lance Formats](format.html)
- [Arrays](arrays.html)
- [Integrations](integrations/integrations.html)
- [Performance Guide](performance.html)
- [API References](api/api.html)
- [Contributor Guide](contributing.html)
- [Examples](examples/examples.html)

# Indices and tables [¶](\#indices-and-tables "Permalink to this heading")

- [Index](genindex.html)

- [Module Index](py-modindex.html)

- [Search Page](search.html)


<Page contents

>Page contents:

- Lance: modern columnar data format for ML
  - [Installation](#installation)
- [Indices and tables](#indices-and-tables)

[Creating datasets>](notebooks/quickstart.html)

Styled using the [Piccolo Theme](https://github.com/piccolo-orm/piccolo_theme)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/cloud/index.md "Edit this page")

# About LanceDB Cloud [Permanent link](\#about-lancedb-cloud "Permanent link")

LanceDB Cloud is a SaaS (software-as-a-service) solution that runs serverless in the cloud, clearly separating storage from compute. It's designed to be highly scalable without breaking the bank. LanceDB Cloud is currently in private beta with general availability coming soon, but you can apply for early access with the private beta release by signing up below.

[Try out LanceDB Cloud](https://noteforms.com/forms/lancedb-mailing-list-cloud-kty1o5?notionforms=1&utm_source=notionforms)

## Architecture [Permanent link](\#architecture "Permanent link")

LanceDB Cloud provides the same underlying fast vector store that powers the OSS version, but without the need to maintain your own infrastructure. Because it's serverless, you only pay for the storage you use, and you can scale compute up and down as needed depending on the size of your data and its associated index.

![](../assets/lancedb_cloud.png)

## Transitioning from the OSS to the Cloud version [Permanent link](\#transitioning-from-the-oss-to-the-cloud-version "Permanent link")

The OSS version of LanceDB is designed to be embedded in your application, and it runs in-process. This makes it incredibly simple to self-host your own AI retrieval workflows for RAG and more and build and test out your concepts on your own infrastructure. The OSS version is forever free, and you can continue to build and integrate LanceDB into your existing backend applications without any added costs.

Should you decide that you need a managed deployment in production, it's possible to seamlessly transition from the OSS to the cloud version by changing the connection string to point to a remote database instead of a local one. With LanceDB Cloud, you can take your AI application from development to production without major code changes or infrastructure burden.

Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/sql.md "Edit this page")

# Filtering [Permanent link](\#filtering "Permanent link")

## Pre and post-filtering [Permanent link](\#pre-and-post-filtering "Permanent link")

LanceDB supports filtering of query results based on metadata fields. By default, post-filtering is
performed on the top-k results returned by the vector search. However, pre-filtering is also an
option that performs the filter prior to vector search. This can be useful to narrow down on
the search space on a very large dataset to reduce query latency.

Note that both pre-filtering and post-filtering can yield false positives. For pre-filtering, if the filter is too selective, it might eliminate relevant items that the vector search would have otherwise identified as a good match. In this case, increasing `nprobes` parameter will help reduce such false positives. It is recommended to set `use_index=false` if you know that the filter is highly selective.

Similarly, a highly selective post-filter can lead to false positives. Increasing both `nprobes` and `refine_factor` can mitigate this issue. When deciding between pre-filtering and post-filtering, pre-filtering is generally the safer choice if you're uncertain.

[Python](#__tabbed_1_1)[TypeScript](#__tabbed_1_2)

```
result = (
    tbl.search([0.5, 0.2])
    .where("id = 10", prefilter=True)
    .limit(1)
    .to_arrow()
)

```

[@lancedb/lancedb](#__tabbed_2_1)[vectordb (deprecated)](#__tabbed_2_2)

```
const _result = await tbl
  .search(Array(1536).fill(0.5))
  .limit(1)
  .where("id = 10")
  .toArray();

```

```
let result = await tbl
  .search(Array(1536).fill(0.5))
  .limit(1)
  .filter("id = 10")
  .prefilter(true)
  .execute();

```

Note

Creating a [scalar index](../guides/scalar_index/) accelerates filtering

## SQL filters [Permanent link](\#sql-filters "Permanent link")

Because it's built on top of [DataFusion](https://github.com/apache/arrow-datafusion), LanceDB
embraces the utilization of standard SQL expressions as predicates for filtering operations.
It can be used during vector search, update, and deletion operations.

Currently, Lance supports a growing list of SQL expressions.

- `>`, `>=`, `<`, `<=`, `=`
- `AND`, `OR`, `NOT`
- `IS NULL`, `IS NOT NULL`
- `IS TRUE`, `IS NOT TRUE`, `IS FALSE`, `IS NOT FALSE`
- `IN`
- `LIKE`, `NOT LIKE`
- `CAST`
- `regexp_match(column, pattern)`
- [DataFusion Functions](https://arrow.apache.org/datafusion/user-guide/sql/scalar_functions.html)

For example, the following filter string is acceptable:

[Python](#__tabbed_3_1)[TypeScript](#__tabbed_3_2)

```
tbl.search([100, 102]) \
   .where("(item IN ('item 0', 'item 2')) AND (id > 10)") \
   .to_arrow()

```

[@lancedb/lancedb](#__tabbed_4_1)[vectordb (deprecated)](#__tabbed_4_2)

```
const result = await (
  tbl.search(Array(1536).fill(0)) as lancedb.VectorQuery
)
  .where("(item IN ('item 0', 'item 2')) AND (id > 10)")
  .postfilter()
  .toArray();

```

```
await tbl
  .search(Array(1536).fill(0))
  .where("(item IN ('item 0', 'item 2')) AND (id > 10)")
  .execute();

```

If your column name contains special characters or is a [SQL Keyword](https://docs.rs/sqlparser/latest/sqlparser/keywords/index.html),
you can use backtick ( `` ` ``) to escape it. For nested fields, each segment of the
path must be wrapped in backticks.

[SQL](#__tabbed_5_1)

```
`CUBE` = 10 AND `column name with space` IS NOT NULL
  AND `nested with space`.`inner with space` < 2

```

Field names containing periods ( `.`) are not supported.

Literals for dates, timestamps, and decimals can be written by writing the string
value after the type name. For example

[SQL](#__tabbed_6_1)

```
date_col = date '2021-01-01'
and timestamp_col = timestamp '2021-01-01 00:00:00'
and decimal_col = decimal(8,3) '1.000'

```

For timestamp columns, the precision can be specified as a number in the type
parameter. Microsecond precision (6) is the default.

| SQL | Time unit |
| --- | --- |
| `timestamp(0)` | Seconds |
| `timestamp(3)` | Milliseconds |
| `timestamp(6)` | Microseconds |
| `timestamp(9)` | Nanoseconds |

LanceDB internally stores data in [Apache Arrow](https://arrow.apache.org/) format.
The mapping from SQL types to Arrow types is:

| SQL type | Arrow type |
| --- | --- |
| `boolean` | `Boolean` |
| `tinyint` / `tinyint unsigned` | `Int8` / `UInt8` |
| `smallint` / `smallint unsigned` | `Int16` / `UInt16` |
| `int` or `integer` / `int unsigned` or `integer unsigned` | `Int32` / `UInt32` |
| `bigint` / `bigint unsigned` | `Int64` / `UInt64` |
| `float` | `Float32` |
| `double` | `Float64` |
| `decimal(precision, scale)` | `Decimal128` |
| `date` | `Date32` |
| `timestamp` | `Timestamp` [1](#fn:1) |
| `string` | `Utf8` |
| `binary` | `Binary` |

## Filtering without Vector Search [Permanent link](\#filtering-without-vector-search "Permanent link")

You can also filter your data without search.

[Python](#__tabbed_7_1)[TypeScript](#__tabbed_7_2)

```
tbl.search().where("id = 10").limit(10).to_arrow()

```

[@lancedb/lancedb](#__tabbed_8_1)[vectordb (deprecated)](#__tabbed_8_2)

```
await tbl.query().where("id = 10").limit(10).toArray();

```

```
await tbl.filter("id = 10").limit(10).execute();

```

If your table is large, this could potentially return a very large amount of data. Please be sure to use a `limit` clause unless you're sure you want to return the whole result set.

* * *

1. See precision mapping in previous table. [↩](#fnref:1 "Jump back to footnote 1 in the text")


Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/reranking/index.md "Edit this page")

# Quickstart

Reranking is the process of reordering a list of items based on some criteria. In the context of search, reranking is used to reorder the search results returned by a search engine based on some criteria. This can be useful when the initial ranking of the search results is not satisfactory or when the user has provided additional information that can be used to improve the ranking of the search results.

LanceDB comes with some built-in rerankers. Some of the rerankers that are available in LanceDB are:

| Reranker | Description | Supported Query Types |
| --- | --- | --- |
| `LinearCombinationReranker` | Reranks search results based on a linear combination of FTS and vector search scores | Hybrid |
| `CohereReranker` | Uses cohere Reranker API to rerank results | Vector, FTS, Hybrid |
| `CrossEncoderReranker` | Uses a cross-encoder model to rerank search results | Vector, FTS, Hybrid |
| `ColbertReranker` | Uses a colbert model to rerank search results | Vector, FTS, Hybrid |
| `OpenaiReranker`(Experimental) | Uses OpenAI's chat model to rerank search results | Vector, FTS, Hybrid |
| `VoyageAIReranker` | Uses voyageai Reranker API to rerank results | Vector, FTS, Hybrid |

## Using a Reranker [Permanent link](\#using-a-reranker "Permanent link")

Using rerankers is optional for vector and FTS. However, for hybrid search, rerankers are required. To use a reranker, you need to create an instance of the reranker and pass it to the `rerank` method of the query builder.

```
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from lancedb.rerankers import CohereReranker

embedder = get_registry().get("sentence-transformers").create()
db = lancedb.connect("~/.lancedb")

class Schema(LanceModel):
    text: str = embedder.SourceField()
    vector: Vector(embedder.ndims()) = embedder.VectorField()

data = [\
    {"text": "hello world"},\
    {"text": "goodbye world"}\
    ]
tbl = db.create_table("test", data)
reranker = CohereReranker(api_key="your_api_key")

# Run vector search with a reranker
result = tbl.query("hello").rerank(reranker).to_list()

# Run FTS search with a reranker
result = tbl.query("hello", query_type="fts").rerank(reranker).to_list()

# Run hybrid search with a reranker
tbl.create_fts_index("text")
result = tbl.query("hello", query_type="hybrid").rerank(reranker).to_list()

```

### Multi-vector reranking [Permanent link](\#multi-vector-reranking "Permanent link")

Most rerankers support reranking based on multiple vectors. To rerank based on multiple vectors, you can pass a list of vectors to the `rerank` method. Here's an example of how to rerank based on multiple vector columns using the `CrossEncoderReranker`:

```
from lancedb.rerankers import CrossEncoderReranker

reranker = CrossEncoderReranker()

query = "hello"

res1 = table.search(query, vector_column_name="vector").limit(3)
res2 = table.search(query, vector_column_name="text_vector").limit(3)
res3 = table.search(query, vector_column_name="meta_vector").limit(3)

reranked = reranker.rerank_multivector([res1, res2, res3],  deduplicate=True)

```

## Available Rerankers [Permanent link](\#available-rerankers "Permanent link")

LanceDB comes with some built-in rerankers. Here are some of the rerankers that are available in LanceDB:

- [Cohere Reranker](cohere/)
- [Cross Encoder Reranker](cross_encoder/)
- [ColBERT Reranker](colbert/)
- [OpenAI Reranker](openai/)
- [Linear Combination Reranker](linear_combination/)
- [Jina Reranker](jina/)
- [AnswerDotAI Rerankers](answerdotai/)
- [Reciprocal Rank Fusion Reranker](rrf/)
- [VoyageAI Reranker](voyageai/)

## Creating Custom Rerankers [Permanent link](\#creating-custom-rerankers "Permanent link")

LanceDB also you to create custom rerankers by extending the base `Reranker` class. The custom reranker should implement the `rerank` method that takes a list of search results and returns a reranked list of search results. This is covered in more detail in the [Creating Custom Rerankers](custom_reranker/) section.

Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/faq.md "Edit this page")

# 💭 FAQs

This section covers some common questions and issues that you may encounter when using LanceDB.

### Is LanceDB open source? [Permanent link](\#is-lancedb-open-source "Permanent link")

Yes, LanceDB is an open source vector database available under an Apache 2.0 license. We also have a serverless SaaS solution, LanceDB Cloud, available under a commercial license.

### What is the difference between Lance and LanceDB? [Permanent link](\#what-is-the-difference-between-lance-and-lancedb "Permanent link")

[Lance](https://github.com/lancedb/lance) is a modern columnar data format for AI, written in Rust 🦀. It’s perfect for building search engines, feature stores and being the foundation of large-scale ML training jobs requiring high performance IO and shuffles. It also has native support for storing, querying, and inspecting deeply nested data for robotics or large blobs like images, point clouds, and more.

LanceDB is the vector database that’s built on top of Lance, and utilizes the underlying optimized storage format to build efficient disk-based indexes that power semantic search & retrieval applications, from RAGs to QA Bots to recommender systems.

### Why invent another data format instead of using Parquet? [Permanent link](\#why-invent-another-data-format-instead-of-using-parquet "Permanent link")

As we mention in our talk titled “ [Lance, a modern columnar data format](https://www.youtube.com/watch?v=ixpbVyrsuL8)”, Parquet and other tabular formats that derive from it are rather dated (Parquet is over 10 years old), especially when it comes to random access on vectors. We needed a format that’s able to handle the complex trade-offs involved in shuffling, scanning, OLAP and filtering large datasets involving vectors, and our extensive experiments with Parquet didn't yield sufficient levels of performance for modern ML. [Our benchmarks](https://blog.lancedb.com/benchmarking-random-access-in-lance-ed690757a826) show that Lance is up to 1000x faster than Parquet for random access, which we believe justifies our decision to create a new data format for AI.

### Why build in Rust? 🦀 [Permanent link](\#why-build-in-rust "Permanent link")

We believe that the Rust ecosystem has attained mainstream maturity and that Rust will form the underpinnings of large parts of the data and ML landscape in a few years. Performance, latency and reliability are paramount to a vector DB, and building in Rust allows us to iterate and release updates more rapidly due to Rust’s safety guarantees. Both Lance (the data format) and LanceDB (the database) are written entirely in Rust. We also provide Python, JavaScript, and Rust client libraries to interact with the database.

### What is the difference between LanceDB OSS and LanceDB Cloud? [Permanent link](\#what-is-the-difference-between-lancedb-oss-and-lancedb-cloud "Permanent link")

LanceDB OSS is an **embedded** (in-process) solution that can be used as the vector store of choice for your LLM and RAG applications. It can be embedded inside an existing application backend, or used in-process alongside existing ML and data engineering pipelines.

LanceDB Cloud is a **serverless** solution — the database and data sit on the cloud and we manage the scalability of the application side via a remote client, without the need to manage any infrastructure.

Both flavors of LanceDB benefit from the blazing fast Lance data format and are built on the same open source foundations.

### What makes LanceDB different? [Permanent link](\#what-makes-lancedb-different "Permanent link")

LanceDB is among the few embedded vector DBs out there that we believe can unlock a whole new class of LLM-powered applications in the browser or via edge functions. Lance’s multi-modal nature allows you to store the raw data, metadata and the embeddings all at once, unlike other solutions that typically store just the embeddings and metadata.

The Lance data format that powers our storage system also provides true zero-copy access and seamless interoperability with numerous other data formats (like Pandas, Polars, Pydantic) via Apache Arrow, as well as automatic data versioning and data management without needing extra infrastructure.

### How large of a dataset can LanceDB handle? [Permanent link](\#how-large-of-a-dataset-can-lancedb-handle "Permanent link")

LanceDB and its underlying data format, Lance, are built to scale to really large amounts of data (hundreds of terabytes). We are currently working with customers who regularly perform operations on 200M+ vectors, and we’re fast approaching billion scale and beyond, which are well-handled by our disk-based indexes, without you having to break the bank.

### Do I need to build an ANN index to run vector search? [Permanent link](\#do-i-need-to-build-an-ann-index-to-run-vector-search "Permanent link")

No. LanceDB is blazing fast (due to its disk-based index) for even brute force kNN search, within reason. In our benchmarks, computing 100K pairs of 1000-dimension vectors takes less than 20ms. For small datasets of ~100K records or applications that can accept ~100ms latency, an ANN index is usually not necessary.

For large-scale (>1M) or higher dimension vectors, it is beneficial to create an ANN index. See the [ANN indexes](../ann_indexes/) section for more details.

### Does LanceDB support full-text search? [Permanent link](\#does-lancedb-support-full-text-search "Permanent link")

Yes, LanceDB supports full-text search (FTS) via [Tantivy](https://github.com/quickwit-oss/tantivy). Our current FTS integration is Python-only, and our goal is to push it down to the Rust level in future versions to enable much more powerful search capabilities available to our Python, JavaScript and Rust clients. Follow along in the [Github issue](https://github.com/lancedb/lance/issues/1195)

### How can I speed up data inserts? [Permanent link](\#how-can-i-speed-up-data-inserts "Permanent link")

It's highly recommend to perform bulk inserts via batches (for e.g., Pandas DataFrames or lists of dicts in Python) to speed up inserts for large datasets. Inserting records one at a time is slow and can result in suboptimal performance because each insert creates a new data fragment on disk. Batching inserts allows LanceDB to create larger fragments (and their associated manifests), which are more efficient to read and write.

### Do I need to set a refine factor when using an index? [Permanent link](\#do-i-need-to-set-a-refine-factor-when-using-an-index "Permanent link")

Yes. LanceDB uses PQ, or Product Quantization, to compress vectors and speed up search when using an ANN index. However, because PQ is a lossy compression algorithm, it tends to reduce recall while also reducing the index size. To address this trade-off, we introduce a process called **refinement**. The normal process computes distances by operating on the compressed PQ vectors. The refinement factor ( _rf_) is a multiplier that takes the top-k similar PQ vectors to a given query, fetches `rf * k` _full_ vectors and computes the raw vector distances between them and the query vector, reordering the top-k results based on these scores instead.

For example, if you're retrieving the top 10 results and set `refine_factor` to 25, LanceDB will fetch the 250 most similar vectors (according to PQ), compute the distances again based on the full vectors for those 250 and then re-rank based on their scores. This can significantly improve recall, with a small added latency cost (typically a few milliseconds), so it's recommended you set a `refine_factor` of anywhere between 5-50 and measure its impact on latency prior to deploying your solution.

### How can I improve IVF-PQ recall while keeping latency low? [Permanent link](\#how-can-i-improve-ivf-pq-recall-while-keeping-latency-low "Permanent link")

When using an IVF-PQ index, there's a trade-off between recall and latency at query time. You can improve recall by increasing the number of probes and the `refine_factor`. In our benchmark on the GIST-1M dataset, we show that it's possible to achieve >0.95 recall with a latency of under 10 ms on most systems, using ~50 probes and a `refine_factor` of 50. This is, of course, subject to the dataset at hand and a quick sensitivity study can be performed on your own data. You can find more details on the benchmark in our [blog post](https://blog.lancedb.com/benchmarking-lancedb-92b01032874a).

![](../assets/recall-vs-latency.webp)

### How do I connect to MinIO? [Permanent link](\#how-do-i-connect-to-minio "Permanent link")

MinIO supports an S3 compatible API. In order to connect to a MinIO instance, you need to:

- Set the envvar `AWS_ENDPOINT` to the URL of your MinIO API
- Set the envvars `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with your MinIO credential
- Call `lancedb.connect("s3://minio_bucket_name")`

### Where can I find benchmarks for LanceDB? [Permanent link](\#where-can-i-find-benchmarks-for-lancedb "Permanent link")

Refer to this [post](https://blog.lancedb.com/benchmarking-lancedb-92b01032874a) for recent benchmarks.

### How much data can LanceDB practically manage without effecting performance? [Permanent link](\#how-much-data-can-lancedb-practically-manage-without-effecting-performance "Permanent link")

We target good performance on ~10-50 billion rows and ~10-30 TB of data.

### Does LanceDB support concurrent operations? [Permanent link](\#does-lancedb-support-concurrent-operations "Permanent link")

LanceDB can handle concurrent reads very well, and can scale horizontally. The main constraint is how well the [storage layer](https://lancedb.github.io/lancedb/concepts/storage/) you've chosen scales. For writes, we support concurrent writing, though too many concurrent writers can lead to failing writes as there is a limited number of times a writer retries a commit

Multiprocessing with LanceDB

For multiprocessing you should probably not use `fork` as lance is multi-threaded internally and `fork` and multi-thread do not work well. [Refer to this discussion](https://discuss.python.org/t/concerns-regarding-deprecation-of-fork-with-alive-threads/33555)

Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/embeddings/index.md "Edit this page")

# Get Started

Due to the nature of vector embeddings, they can be used to represent any kind of data, from text to images to audio.
This makes them a very powerful tool for machine learning practitioners.
However, there's no one-size-fits-all solution for generating embeddings - there are many different libraries and APIs
(both commercial and open source) that can be used to generate embeddings from structured/unstructured data.

LanceDB supports 3 methods of working with embeddings.

1. You can manually generate embeddings for the data and queries. This is done outside of LanceDB.
2. You can use the built-in [embedding functions](embedding_functions/) to embed the data and queries in the background.
3. You can define your own [custom embedding function](custom_embedding_function/)
    that extends the default embedding functions.

For python users, there is also a legacy [with\_embeddings API](legacy/).
It is retained for compatibility and will be removed in a future version.

## Quickstart [Permanent link](\#quickstart "Permanent link")

To get started with embeddings, you can use the built-in embedding functions.

### OpenAI Embedding function [Permanent link](\#openai-embedding-function "Permanent link")

LanceDB registers the OpenAI embeddings function in the registry as `openai`. You can pass any supported model name to the `create`. By default it uses `"text-embedding-ada-002"`.

[Python](#__tabbed_1_1)[TypeScript](#__tabbed_1_2)[Rust](#__tabbed_1_3)

```
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

db = lancedb.connect("/tmp/db")
func = get_registry().get("openai").create(name="text-embedding-ada-002")

class Words(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()

table = db.create_table("words", schema=Words, mode="overwrite")
table.add(
    [\
        {"text": "hello world"},\
        {"text": "goodbye world"}\
    ]
    )

query = "greetings"
actual = table.search(query).limit(1).to_pydantic(Words)[0]
print(actual.text)

```

```
import * as lancedb from "@lancedb/lancedb";
import "@lancedb/lancedb/embedding/openai";
import { LanceSchema, getRegistry, register } from "@lancedb/lancedb/embedding";
import { EmbeddingFunction } from "@lancedb/lancedb/embedding";
import { type Float, Float32, Utf8 } from "apache-arrow";
const db = await lancedb.connect(databaseDir);
const func = getRegistry()
  .get("openai")
  ?.create({ model: "text-embedding-ada-002" }) as EmbeddingFunction;

const wordsSchema = LanceSchema({
  text: func.sourceField(new Utf8()),
  vector: func.vectorField(),
});
const tbl = await db.createEmptyTable("words", wordsSchema, {
  mode: "overwrite",
});
await tbl.add([{ text: "hello world" }, { text: "goodbye world" }]);

const query = "greetings";
const actual = (await tbl.search(query).limit(1).toArray())[0];

```

```
use std::{iter::once, sync::Arc};

use arrow_array::{Float64Array, Int32Array, RecordBatch, RecordBatchIterator, StringArray};
use arrow_schema::{DataType, Field, Schema};
use futures::StreamExt;
use lancedb::{
    arrow::IntoArrow,
    connect,
    embeddings::{openai::OpenAIEmbeddingFunction, EmbeddingDefinition, EmbeddingFunction},
    query::{ExecutableQuery, QueryBase},
    Result,
};

#[tokio::main]
async fn main() -> Result<()> {
    let tempdir = tempfile::tempdir().unwrap();
    let tempdir = tempdir.path().to_str().unwrap();
    let api_key = std::env::var("OPENAI_API_KEY").expect("OPENAI_API_KEY is not set");
    let embedding = Arc::new(OpenAIEmbeddingFunction::new_with_model(
        api_key,
        "text-embedding-3-large",
    )?);

    let db = connect(tempdir).execute().await?;
    db.embedding_registry()
        .register("openai", embedding.clone())?;

    let table = db
        .create_table("vectors", make_data())
        .add_embedding(EmbeddingDefinition::new(
            "text",
            "openai",
            Some("embeddings"),
        ))?
        .execute()
        .await?;

    let query = Arc::new(StringArray::from_iter_values(once("something warm")));
    let query_vector = embedding.compute_query_embeddings(query)?;
    let mut results = table
        .vector_search(query_vector)?
        .limit(1)
        .execute()
        .await?;

    let rb = results.next().await.unwrap()?;
    let out = rb
        .column_by_name("text")
        .unwrap()
        .as_any()
        .downcast_ref::<StringArray>()
        .unwrap();
    let text = out.iter().next().unwrap().unwrap();
    println!("Closest match: {}", text);
    Ok(())
}

```

### Sentence Transformers Embedding function [Permanent link](\#sentence-transformers-embedding-function "Permanent link")

LanceDB registers the Sentence Transformers embeddings function in the registry as `sentence-transformers`. You can pass any supported model name to the `create`. By default it uses `"sentence-transformers/paraphrase-MiniLM-L6-v2"`.

[Python](#__tabbed_2_1)[TypeScript](#__tabbed_2_2)[Rust](#__tabbed_2_3)

```
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

db = lancedb.connect("/tmp/db")
model = get_registry().get("sentence-transformers").create(name="BAAI/bge-small-en-v1.5", device="cpu")

class Words(LanceModel):
    text: str = model.SourceField()
    vector: Vector(model.ndims()) = model.VectorField()

table = db.create_table("words", schema=Words)
table.add(
    [\
        {"text": "hello world"},\
        {"text": "goodbye world"}\
    ]
)

query = "greetings"
actual = table.search(query).limit(1).to_pydantic(Words)[0]
print(actual.text)

```

Coming Soon!

Coming Soon!

### Embedding function with LanceDB cloud [Permanent link](\#embedding-function-with-lancedb-cloud "Permanent link")

Embedding functions are now supported on LanceDB cloud. The embeddings will be generated on the source device and sent to the cloud. This means that the source device must have the necessary resources to generate the embeddings. Here's an example using the OpenAI embedding function:

```
import os
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
os.environ['OPENAI_API_KEY'] = "..."

db = lancedb.connect(
  uri="db://....",
  api_key="sk_...",
  region="us-east-1"
)
func = get_registry().get("openai").create()

class Words(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()

table = db.create_table("words", schema=Words)
table.add([\
    {"text": "hello world"},\
    {"text": "goodbye world"}\
])

query = "greetings"
actual = table.search(query).limit(1).to_pydantic(Words)[0]
print(actual.text)

```

Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/fts.md "Edit this page")

# Full-text search (Native FTS) [Permanent link](\#full-text-search-native-fts "Permanent link")

LanceDB provides support for full-text search via Lance, allowing you to incorporate keyword-based search (based on BM25) in your retrieval solutions.

Note

The Python SDK uses tantivy-based FTS by default, need to pass `use_tantivy=False` to use native FTS.

## Example [Permanent link](\#example "Permanent link")

Consider that we have a LanceDB table named `my_table`, whose string column `text` we want to index and query via keyword search, the FTS index must be created before you can search via keywords.

[Python](#__tabbed_1_1)[TypeScript](#__tabbed_1_2)[Rust](#__tabbed_1_3)

```
import lancedb

uri = "data/sample-lancedb"
db = lancedb.connect(uri)

table = db.create_table(
    "my_table",
    data=[\
        {"vector": [3.1, 4.1], "text": "Frodo was a happy puppy"},\
        {"vector": [5.9, 26.5], "text": "There are several kittens playing"},\
    ],
)

# passing `use_tantivy=False` to use lance FTS index
# `use_tantivy=True` by default
table.create_fts_index("text", use_tantivy=False)
table.search("puppy").limit(10).select(["text"]).to_list()
# [{'text': 'Frodo was a happy puppy', '_score': 0.6931471824645996}]
# ...

```

```
import * as lancedb from "@lancedb/lancedb";
const uri = "data/sample-lancedb"
const db = await lancedb.connect(uri);

const data = [\
{ vector: [3.1, 4.1], text: "Frodo was a happy puppy" },\
{ vector: [5.9, 26.5], text: "There are several kittens playing" },\
];
const tbl = await db.createTable("my_table", data, { mode: "overwrite" });
await tbl.createIndex("text", {
    config: lancedb.Index.fts(),
});

await tbl
    .search("puppy", queryType="fts")
    .select(["text"])
    .limit(10)
    .toArray();

```

```
let uri = "data/sample-lancedb";
let db = connect(uri).execute().await?;
let initial_data: Box<dyn RecordBatchReader + Send> = create_some_records()?;
let tbl = db
    .create_table("my_table", initial_data)
    .execute()
    .await?;
tbl
    .create_index(&["text"], Index::FTS(FtsIndexBuilder::default()))
    .execute()
    .await?;

tbl
    .query()
    .full_text_search(FullTextSearchQuery::new("puppy".to_owned()))
    .select(lancedb::query::Select::Columns(vec!["text".to_owned()]))
    .limit(10)
    .execute()
    .await?;

```

It would search on all indexed columns by default, so it's useful when there are multiple indexed columns.

Passing `fts_columns="text"` if you want to specify the columns to search.

Note

LanceDB automatically searches on the existing FTS index if the input to the search is of type `str`. If you provide a vector as input, LanceDB will search the ANN index instead.

## Tokenization [Permanent link](\#tokenization "Permanent link")

By default the text is tokenized by splitting on punctuation and whitespaces, and would filter out words that are with length greater than 40, and lowercase all words.

Stemming is useful for improving search results by reducing words to their root form, e.g. "running" to "run". LanceDB supports stemming for multiple languages, you can specify the tokenizer name to enable stemming by the pattern `tokenizer_name="{language_code}_stem"`, e.g. `en_stem` for English.

For example, to enable stemming for English:

```
table.create_fts_index("text", use_tantivy=True, tokenizer_name="en_stem")

```

the following [languages](https://docs.rs/tantivy/latest/tantivy/tokenizer/enum.Language.html) are currently supported.

The tokenizer is customizable, you can specify how the tokenizer splits the text, and how it filters out words, etc.

For example, for language with accents, you can specify the tokenizer to use `ascii_folding` to remove accents, e.g. 'é' to 'e':

```
table.create_fts_index("text",
                        use_tantivy=False,
                        language="French",
                        stem=True,
                        ascii_folding=True)

```

## Filtering [Permanent link](\#filtering "Permanent link")

LanceDB full text search supports to filter the search results by a condition, both pre-filtering and post-filtering are supported.

This can be invoked via the familiar `where` syntax.

With pre-filtering:

[Python](#__tabbed_2_1)[TypeScript](#__tabbed_2_2)[Rust](#__tabbed_2_3)

```
table.search("puppy").limit(10).where("meta='foo'", prefilte=True).to_list()

```

```
await tbl
.search("puppy")
.select(["id", "doc"])
.limit(10)
.where("meta='foo'")
.prefilter(true)
.toArray();

```

```
table
    .query()
    .full_text_search(FullTextSearchQuery::new("puppy".to_owned()))
    .select(lancedb::query::Select::Columns(vec!["doc".to_owned()]))
    .limit(10)
    .only_if("meta='foo'")
    .execute()
    .await?;

```

With post-filtering:

[Python](#__tabbed_3_1)[TypeScript](#__tabbed_3_2)[Rust](#__tabbed_3_3)

```
table.search("puppy").limit(10).where("meta='foo'", prefilte=False).to_list()

```

```
await tbl
.search("apple")
.select(["id", "doc"])
.limit(10)
.where("meta='foo'")
.prefilter(false)
.toArray();

```

```
table
    .query()
    .full_text_search(FullTextSearchQuery::new(words[0].to_owned()))
    .select(lancedb::query::Select::Columns(vec!["doc".to_owned()]))
    .postfilter()
    .limit(10)
    .only_if("meta='foo'")
    .execute()
    .await?;

```

## Phrase queries vs. terms queries [Permanent link](\#phrase-queries-vs-terms-queries "Permanent link")

Warn

Lance-based FTS doesn't support queries using boolean operators `OR`, `AND`.

For full-text search you can specify either a **phrase** query like `"the old man and the sea"`,
or a **terms** search query like `old man sea`. For more details on the terms
query syntax, see Tantivy's [query parser rules](https://docs.rs/tantivy/latest/tantivy/query/struct.QueryParser.html).

To search for a phrase, the index must be created with `with_position=True`:

```
table.create_fts_index("text", use_tantivy=False, with_position=True)

```

This will allow you to search for phrases, but it will also significantly increase the index size and indexing time.

## Incremental indexing [Permanent link](\#incremental-indexing "Permanent link")

LanceDB supports incremental indexing, which means you can add new records to the table without reindexing the entire table.

This can make the query more efficient, especially when the table is large and the new records are relatively small.

[Python](#__tabbed_4_1)[TypeScript](#__tabbed_4_2)[Rust](#__tabbed_4_3)

```
table.add([{"vector": [3.1, 4.1], "text": "Frodo was a happy puppy"}])
table.optimize()

```

```
await tbl.add([{ vector: [3.1, 4.1], text: "Frodo was a happy puppy" }]);
await tbl.optimize();

```

```
let more_data: Box<dyn RecordBatchReader + Send> = create_some_records()?;
tbl.add(more_data).execute().await?;
tbl.optimize(OptimizeAction::All).execute().await?;

```

Note

New data added after creating the FTS index will appear in search results while incremental index is still progress, but with increased latency due to a flat search on the unindexed portion. LanceDB Cloud automates this merging process, minimizing the impact on search speed.

Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/integrations/index.md "Edit this page")

# Integrations [Permanent link](\#integrations "Permanent link")

LanceDB supports ingesting from and exporting to your favorite data formats across the Python and JavaScript ecosystems.

![Illustration](../assets/ecosystem-illustration.png)

## Tools [Permanent link](\#tools "Permanent link")

LanceDB is integrated with a lot of popular AI tools, with more coming soon.
Get started using these examples and quick links.

| Integrations |  |
| --- | --- |
| ### LlamaIndex<br>LlamaIndex is a simple, flexible data framework for connecting custom data sources to large language models. Llama index integrates with LanceDB as the serverless VectorDB. <br>### [Lean More](https://gpt-index.readthedocs.io/en/latest/examples/vector_stores/LanceDBIndexDemo.html) | ![image](../assets/llama-index.jpg) |
| ### Langchain<br>Langchain allows building applications with LLMs through composability <br>### [Lean More](https://lancedb.github.io/lancedb/integrations/langchain/) | ![image](../assets/langchain.png) |
| ### Langchain TS<br> Javascript bindings for Langchain. It integrates with LanceDB's serverless vectordb allowing you to build powerful AI applications through composibility using only serverless functions. <br>### [Learn More](https://js.langchain.com/docs/modules/data_connection/vectorstores/integrations/lancedb) | ![image](../assets/langchain.png) |
| ### Voxel51<br> It is an open source toolkit that enables you to build better computer vision workflows by improving the quality of your datasets and delivering insights about your models.<br>### [Learn More](voxel51/) | ![image](../assets/voxel.gif) |
| ### PromptTools<br> Offers a set of free, open-source tools for testing and experimenting with models, prompts, and configurations. The core idea is to enable developers to evaluate prompts using familiar interfaces like code and notebooks. You can use it to experiment with different configurations of LanceDB, and test how LanceDB integrates with the LLM of your choice.<br>### [Learn More](prompttools/) | ![image](../assets/prompttools.jpeg) |

Back to top

[Ask AI](https://asklancedb.com)

[Edit this page](https://github.com/lancedb/lancedb/tree/main/docs/src/index.md "Edit this page")

# LanceDB [Permanent link](\#lancedb "Permanent link")

LanceDB is an open-source vector database for AI that's designed to store, manage, query and retrieve embeddings on large-scale multi-modal data. The core of LanceDB is written in Rust 🦀 and is built on top of [Lance](https://github.com/lancedb/lance), an open-source columnar data format designed for performant ML workloads and fast random access.

Both the database and the underlying data format are designed from the ground up to be **easy-to-use**, **scalable** and **cost-effective**.

![](assets/lancedb_and_lance.png)

## Truly multi-modal [Permanent link](\#truly-multi-modal "Permanent link")

Most existing vector databases that store and query just the embeddings and their metadata. The actual data is stored elsewhere, requiring you to manage their storage and versioning separately.

LanceDB supports storage of the _actual data itself_, alongside the embeddings and metadata. You can persist your images, videos, text documents, audio files and more in the Lance format, which provides automatic data versioning and blazing fast retrievals and filtering via LanceDB.

## Open-source and cloud solutions [Permanent link](\#open-source-and-cloud-solutions "Permanent link")

LanceDB is available in two flavors: **OSS** and **Cloud**.

LanceDB **OSS** is an **open-source**, batteries-included embedded vector database that you can run on your own infrastructure. "Embedded" means that it runs _in-process_, making it incredibly simple to self-host your own AI retrieval workflows for RAG and more. No servers, no hassle.

LanceDB **Cloud** is a SaaS (software-as-a-service) solution that runs serverless in the cloud, making the storage clearly separated from compute. It's designed to be cost-effective and highly scalable without breaking the bank. LanceDB Cloud is currently in private beta with general availability coming soon, but you can apply for early access with the private beta release by signing up below.

[Try out LanceDB Cloud](https://noteforms.com/forms/lancedb-mailing-list-cloud-kty1o5?notionforms=1&utm_source=notionforms)

## Why use LanceDB? [Permanent link](\#why-use-lancedb "Permanent link")

- Embedded (OSS) and serverless (Cloud) - no need to manage servers

- Fast production-scale vector similarity, full-text & hybrid search and a SQL query interface (via [DataFusion](https://github.com/apache/arrow-datafusion))

- Python, Javascript/Typescript, and Rust support

- Store, query & manage multi-modal data (text, images, videos, point clouds, etc.), not just the embeddings and metadata

- Tight integration with the [Arrow](https://arrow.apache.org/docs/format/Columnar.html) ecosystem, allowing true zero-copy access in shared memory with SIMD and GPU acceleration

- Automatic data versioning to manage versions of your data without needing extra infrastructure

- Disk-based index & storage, allowing for massive scalability without breaking the bank

- Ingest your favorite data formats directly, like pandas DataFrames, Pydantic objects, Polars (coming soon), and more


## Documentation guide [Permanent link](\#documentation-guide "Permanent link")

The following pages go deeper into the internal of LanceDB and how to use it.

- [Quick start](basic/): Get started with LanceDB and vector DB concepts
- [Vector search concepts](concepts/vector_search/): Understand the basics of vector search
- [Working with tables](guides/tables/): Learn how to work with tables and their associated functions
- [Indexing](ann_indexes/): Understand how to create indexes
- [Vector search](search/): Learn how to perform vector similarity search
- [Full-text search (native)](fts/): Learn how to perform full-text search
- [Full-text search (tantivy-based)](fts_tantivy/): Learn how to perform full-text search using Tantivy
- [Managing embeddings](embeddings/): Managing embeddings and the embedding functions API in LanceDB
- [Ecosystem Integrations](integrations/): Integrate LanceDB with other tools in the data ecosystem
- [Python API Reference](python/python/): Python OSS and Cloud API references
- [JavaScript API Reference](javascript/modules/): JavaScript OSS and Cloud API references
- [Rust API Reference](https://docs.rs/lancedb/latest/lancedb/index.html): Rust API reference

Back to top

[Ask AI](https://asklancedb.com)

# LanceDB MCP Server Documentation

## Overview
The LanceDB MCP (Model Control Protocol) Server provides a standardized interface for managing vector databases using LanceDB. It implements the MCP specification for vector database operations while leveraging LanceDB's efficient storage and retrieval capabilities.

## Key Features
- Embedded vector database server
- Efficient resource management
- Concurrent read support
- Automatic cleanup and garbage collection
- Error handling for common edge cases

## Server Operations

### Initialization
```python
from lancedb_mcp.server import LanceDBServer

# Initialize with default URI
server = LanceDBServer()

# Initialize with custom URI
server = LanceDBServer(uri="custom/data/path")
```

### Resource Management
The server implements efficient resource management:
- Tables are automatically cleaned up when no longer needed
- No explicit `close()` calls required
- Python's garbage collector handles resource cleanup
- References are cleared during server shutdown

### Error Handling
The server includes comprehensive error handling for:
- Non-existent tables
- Invalid vector dimensions
- Concurrent access issues
- Resource allocation failures

## Best Practices

### Server Usage
1. Initialize server with appropriate URI
2. Use batch operations for better performance
3. Handle errors appropriately
4. Allow proper cleanup during shutdown

### Performance Optimization
1. Use batch operations when possible
2. Clear unused references
3. Monitor memory usage
4. Handle cleanup properly

## Testing
The server includes comprehensive test coverage for:
- Server initialization
- Table operations
- Error handling
- Concurrent access
- Resource cleanup

For detailed test examples, see `tests/test_server.py` and `tests/test_initialization.py`.
