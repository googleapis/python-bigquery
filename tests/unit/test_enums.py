def test_compression_enums():
    from google.cloud.bigquery.enums import Compression

    expected_comps_sorted = ["DEFLATE", "GZIP", "NONE", "SNAPPY", "ZSTD"]

    result_comps_sorted = sorted(comp.value for comp in Compression)

    assert result_comps_sorted == expected_comps_sorted
