Python Client for Google BigQuery
=================================

|GA| |pypi| |versions|

Querying massive datasets can be time consuming and expensive without the
right hardware and infrastructure. Google `BigQuery`_ solves this problem by
enabling super-fast, SQL queries against append-mostly tables, using the
processing power of Google's infrastructure.

-  `Client Library Documentation`_
-  `Product Documentation`_

.. |GA| image:: https://img.shields.io/badge/support-GA-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#general-availability
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-bigquery.svg
   :target: https://pypi.org/project/google-cloud-bigquery/
.. _BigQuery: https://cloud.google.com/bigquery/what-is-bigquery
.. _Client Library Documentation: https://googleapis.dev/python/bigquery/latest
.. _Product Documentation: https://cloud.google.com/bigquery/docs/reference/v2/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud BigQuery API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud BigQuery API.:  https://cloud.google.com/bigquery
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.7

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7, Python == 3.5, Python == 3.6.

The last version of this library compatible with Python 2.7 and 3.5 is
`google-cloud-bigquery==1.28.0`.


Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-bigquery


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-bigquery

Example Usage
-------------

Perform a query
~~~~~~~~~~~~~~~

.. code:: python

    from google.cloud import bigquery

    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row.name)

Instrumenting With OpenTelemetry
--------------------------------

This application uses `OpenTelemetry`_ to output tracing data from
API calls to BigQuery. To enable OpenTelemetry tracing in
the BigQuery client the following PyPI packages need to be installed:

.. _OpenTelemetry: https://opentelemetry.io

.. code-block:: console

    pip install google-cloud-bigquery[opentelemetry] opentelemetry-exporter-gcp-trace

After installation, OpenTelemetry can be used in the BigQuery
client and in BigQuery jobs. First, however, an exporter must be
specified for where the trace data will be outputted to. An
example of this can be found here:

.. code-block:: python

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
    tracer_provider = TracerProvider()
    tracer_provider = BatchSpanProcessor(CloudTraceSpanExporter())
    trace.set_tracer_provider(TracerProvider())

In this example all tracing data will be published to the Google
`Cloud Trace`_ console. For more information on OpenTelemetry, please consult the `OpenTelemetry documentation`_.

.. _OpenTelemetry documentation: https://opentelemetry-python.readthedocs.io
.. _Cloud Trace: https://cloud.google.com/trace

Logging
-------

This library uses the standard Python :code:`logging` functionality to log some RPC events that could be of interest for debugging and monitoring purposes.
Note the following:

#. Logs may contain sensitive information. Take care to **restrict access to the logs** if they are saved, whether it be on local storage or on Google Cloud Logging.
#. Google may refine the occurrence, level, and content of various log messages in this library without flagging such changes as breaking. **Do not depend on immutability of the logging events**.
#. By default, the logging events from this library are not handled. You must **explicitly configure log handling** using one of the mechanisms below.

Simple, environment-based configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable logging for this library without any changes in your code, set the :code:`GOOGLE_SDK_PYTHON_LOGGING_SCOPE` environment variable to a valid Google
logging scope. This configures handling of logging events (at level :code:`logging.DEBUG` or higher) from this library in a default manner, emitting the logged
messages in a structured format. It does not currently allow customizing the logging levels captured nor the handlers, formatters, etc. used for any logging
event.

A logging scope is a period-separated namespace that begins with :code:`google`, identifying the Python module or package to log.

- Valid logging scopes: :code:`google`, :code:`google.cloud.asset.v1`, :code:`google.api`, :code:`google.auth`, etc.
- Invalid logging scopes: :code:`foo`, :code:`123`, etc.

**NOTE**: If the logging scope is invalid, the library does not set up any logging handlers.

Examples
^^^^^^^^

- Enabling the default handler for all Google-based loggers

.. code-block:: console

    export GOOGLE_SDK_PYTHON_LOGGING_SCOPE=google

- Enabling the default handler for a specific Google module (for a client library called :code:`google.cloud.bigquery_v2`):

.. code-block:: console

    export GOOGLE_SDK_PYTHON_LOGGING_SCOPE=google.cloud.bigquery_v2


Advanced, code-based configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also configure a valid logging scope using Python's standard `logging` mechanism.

Examples
^^^^^^^^

- Configuring a handler for all Google-based loggers

.. code-block:: python

    import logging
    
    from google.cloud.translate_v3 import translate
    
    base_logger = logging.getLogger("google")
    base_logger.addHandler(logging.StreamHandler())
    base_logger.setLevel(logging.DEBUG)

- Configuring a handler for a specific Google module (for a client library called :code:`google.cloud.bigquery_v2`):

.. code-block:: python

    import logging
    
    from google.cloud.translate_v3 import translate
    
    base_logger = logging.getLogger("google.cloud.bigquery_v2")
    base_logger.addHandler(logging.StreamHandler())
    base_logger.setLevel(logging.DEBUG)

Logging details
~~~~~~~~~~~~~~~

#. Regardless of which of the mechanisms above you use to configure logging for this library, by default logging events are not propagated up to the root
   logger from the `google`-level logger. If you need the events to be propagated to the root logger, you must explicitly set
   :code:`logging.getLogger("google").propagate = True` in your code.
#. You can mix the different logging configurations above for different Google modules. For example, you may want use a code-based logging configuration for
   one library, but decide you need to also set up environment-based logging configuration for another library.

   #. If you attempt to use both code-based and environment-based configuration for the same module, the environment-based configuration will be ineffectual
      if the code -based configuration gets applied first.

#. The Google-specific logging configurations (default handlers for environment-based configuration; not propagating logging events to the root logger) get
   executed the first time *any* client library is instantiated in your application, and only if the affected loggers have not been previously configured.
   (This is the reason for 2.i. above.)
