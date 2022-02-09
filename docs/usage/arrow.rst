Using BigQuery with PyArrow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: add column re: NUMERIC/BIGNUMERIC with note regarding extreme BIGNUMERIC values.

.. list-table:: ArrowData Type Mapping
   :header-rows: 1

   * - BigQuery
     - PyArrow
     - Notes
   * - BOOL
     - boolean
     -
   * - DATETIME
     - datetime64[ns], object
     - The object dtype is used when there are values not representable in a
       pandas nanosecond-precision timestamp.
   * - DATE
     - dbdate, object
     - The object dtype is used when there are values not representable in a
       pandas nanosecond-precision timestamp.

       Requires the ``db-dtypes`` package. See the `db-dtypes usage guide
       <https://googleapis.dev/python/db-dtypes/latest/usage.html>`_
   * - FLOAT64
     - float64
     -
   * - INT64
     - Int64
     -
   * - TIME
     - dbtime
     - Requires the ``db-dtypes`` package. See the `db-dtypes usage guide
       <https://googleapis.dev/python/db-dtypes/latest/usage.html>`_
