# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

from google.cloud.bigquery_v2.types import encryption_config
from google.cloud.bigquery_v2.types import model_reference as gcb_model_reference
from google.cloud.bigquery_v2.types import standard_sql
from google.cloud.bigquery_v2.types import table_reference
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.v2",
    manifest={
        "RemoteModelInfo",
        "TransformColumn",
        "Model",
        "GetModelRequest",
        "PatchModelRequest",
        "DeleteModelRequest",
        "ListModelsRequest",
        "ListModelsResponse",
    },
)


class RemoteModelInfo(proto.Message):
    r"""Remote Model Info

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        endpoint (str):
            Output only. The endpoint for remote model.

            This field is a member of `oneof`_ ``remote_service``.
        remote_service_type (google.cloud.bigquery_v2.types.RemoteModelInfo.RemoteServiceType):
            Output only. The remote service type for
            remote model.

            This field is a member of `oneof`_ ``remote_service``.
        connection (str):
            Output only. Fully qualified name of the user-provided
            connection object of the remote model. Format:
            ``"projects/{project_id}/locations/{location_id}/connections/{connection_id}"``
        max_batching_rows (int):
            Output only. Max number of rows in each batch
            sent to the remote service. If unset, the number
            of rows in each batch is set dynamically.
        remote_model_version (str):
            Output only. The model version for LLM.
        speech_recognizer (str):
            Output only. The name of the speech recognizer to use for
            speech recognition. The expected format is
            ``projects/{project}/locations/{location}/recognizers/{recognizer}``.
            Customers can specify this field at model creation. If not
            specified, a default recognizer
            ``projects/{model project}/locations/global/recognizers/_``
            will be used. See more details at
            `recognizers <https://cloud.google.com/speech-to-text/v2/docs/reference/rest/v2/projects.locations.recognizers>`__
    """

    class RemoteServiceType(proto.Enum):
        r"""Supported service type for remote model.

        Values:
            REMOTE_SERVICE_TYPE_UNSPECIFIED (0):
                Unspecified remote service type.
            CLOUD_AI_TRANSLATE_V3 (1):
                V3 Cloud AI Translation API. See more details at [Cloud
                Translation API]
                (https://cloud.google.com/translate/docs/reference/rest).
            CLOUD_AI_VISION_V1 (2):
                V1 Cloud AI Vision API See more details at [Cloud Vision
                API] (https://cloud.google.com/vision/docs/reference/rest).
            CLOUD_AI_NATURAL_LANGUAGE_V1 (3):
                V1 Cloud AI Natural Language API. See more details at `REST
                Resource:
                documents <https://cloud.google.com/natural-language/docs/reference/rest/v1/documents>`__.
            CLOUD_AI_SPEECH_TO_TEXT_V2 (7):
                V2 Speech-to-Text API. See more details at `Google Cloud
                Speech-to-Text V2
                API <https://cloud.google.com/speech-to-text/v2/docs>`__
        """
        REMOTE_SERVICE_TYPE_UNSPECIFIED = 0
        CLOUD_AI_TRANSLATE_V3 = 1
        CLOUD_AI_VISION_V1 = 2
        CLOUD_AI_NATURAL_LANGUAGE_V1 = 3
        CLOUD_AI_SPEECH_TO_TEXT_V2 = 7

    endpoint: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="remote_service",
    )
    remote_service_type: RemoteServiceType = proto.Field(
        proto.ENUM,
        number=2,
        oneof="remote_service",
        enum=RemoteServiceType,
    )
    connection: str = proto.Field(
        proto.STRING,
        number=3,
    )
    max_batching_rows: int = proto.Field(
        proto.INT64,
        number=4,
    )
    remote_model_version: str = proto.Field(
        proto.STRING,
        number=5,
    )
    speech_recognizer: str = proto.Field(
        proto.STRING,
        number=7,
    )


class TransformColumn(proto.Message):
    r"""Information about a single transform column.

    Attributes:
        name (str):
            Output only. Name of the column.
        type_ (google.cloud.bigquery_v2.types.StandardSqlDataType):
            Output only. Data type of the column after
            the transform.
        transform_sql (str):
            Output only. The SQL expression used in the
            column transform.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: standard_sql.StandardSqlDataType = proto.Field(
        proto.MESSAGE,
        number=2,
        message=standard_sql.StandardSqlDataType,
    )
    transform_sql: str = proto.Field(
        proto.STRING,
        number=3,
    )


class Model(proto.Message):
    r"""

    Attributes:
        etag (str):
            Output only. A hash of this resource.
        model_reference (google.cloud.bigquery_v2.types.ModelReference):
            Required. Unique identifier for this model.
        creation_time (int):
            Output only. The time when this model was
            created, in millisecs since the epoch.
        last_modified_time (int):
            Output only. The time when this model was
            last modified, in millisecs since the epoch.
        description (str):
            Optional. A user-friendly description of this
            model.
        friendly_name (str):
            Optional. A descriptive name for this model.
        labels (MutableMapping[str, str]):
            The labels associated with this model. You
            can use these to organize and group your models.
            Label keys and values can be no longer than 63
            characters, can only contain lowercase letters,
            numeric characters, underscores and dashes.
            International characters are allowed. Label
            values are optional. Label keys must start with
            a letter and each label in the list must have a
            different key.
        expiration_time (int):
            Optional. The time when this model expires,
            in milliseconds since the epoch. If not present,
            the model will persist indefinitely. Expired
            models will be deleted and their storage
            reclaimed.  The defaultTableExpirationMs
            property of the encapsulating dataset can be
            used to set a default expirationTime on newly
            created models.
        location (str):
            Output only. The geographic location where
            the model resides. This value is inherited from
            the dataset.
        encryption_configuration (google.cloud.bigquery_v2.types.EncryptionConfiguration):
            Custom encryption configuration (e.g., Cloud
            KMS keys). This shows the encryption
            configuration of the model data while stored in
            BigQuery storage. This field can be used with
            PatchModel to update encryption key for an
            already encrypted model.
        model_type (google.cloud.bigquery_v2.types.Model.ModelType):
            Output only. Type of the model resource.
        training_runs (MutableSequence[google.cloud.bigquery_v2.types.Model.TrainingRun]):
            Information for all training runs in increasing order of
            start_time.
        feature_columns (MutableSequence[google.cloud.bigquery_v2.types.StandardSqlField]):
            Output only. Input feature columns for the
            model inference. If the model is trained with
            TRANSFORM clause, these are the input of the
            TRANSFORM clause.
        label_columns (MutableSequence[google.cloud.bigquery_v2.types.StandardSqlField]):
            Output only. Label columns that were used to train this
            model. The output of the model will have a "predicted_"
            prefix to these columns.
        transform_columns (MutableSequence[google.cloud.bigquery_v2.types.TransformColumn]):
            Output only. This field will be populated if a TRANSFORM
            clause was used to train a model. TRANSFORM clause (if used)
            takes feature_columns as input and outputs
            transform_columns. transform_columns then are used to train
            the model.
        hparam_search_spaces (google.cloud.bigquery_v2.types.Model.HparamSearchSpaces):
            Output only. All hyperparameter search spaces
            in this model.
        default_trial_id (int):
            Output only. The default trial_id to use in TVFs when the
            trial_id is not passed in. For single-objective
            `hyperparameter
            tuning <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
            models, this is the best trial ID. For multi-objective
            `hyperparameter
            tuning <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
            models, this is the smallest trial ID among all Pareto
            optimal trials.
        hparam_trials (MutableSequence[google.cloud.bigquery_v2.types.Model.HparamTuningTrial]):
            Output only. Trials of a `hyperparameter
            tuning <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
            model sorted by trial_id.
        optimal_trial_ids (MutableSequence[int]):
            Output only. For single-objective `hyperparameter
            tuning <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
            models, it only contains the best trial. For multi-objective
            `hyperparameter
            tuning <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
            models, it contains all Pareto optimal trials sorted by
            trial_id.
        remote_model_info (google.cloud.bigquery_v2.types.RemoteModelInfo):
            Output only. Remote model info
    """

    class ModelType(proto.Enum):
        r"""Indicates the type of the Model.

        Values:
            MODEL_TYPE_UNSPECIFIED (0):
                Default value.
            LINEAR_REGRESSION (1):
                Linear regression model.
            LOGISTIC_REGRESSION (2):
                Logistic regression based classification
                model.
            KMEANS (3):
                K-means clustering model.
            MATRIX_FACTORIZATION (4):
                Matrix factorization model.
            DNN_CLASSIFIER (5):
                DNN classifier model.
            TENSORFLOW (6):
                An imported TensorFlow model.
            DNN_REGRESSOR (7):
                DNN regressor model.
            XGBOOST (8):
                An imported XGBoost model.
            BOOSTED_TREE_REGRESSOR (9):
                Boosted tree regressor model.
            BOOSTED_TREE_CLASSIFIER (10):
                Boosted tree classifier model.
            ARIMA (11):
                ARIMA model.
            AUTOML_REGRESSOR (12):
                AutoML Tables regression model.
            AUTOML_CLASSIFIER (13):
                AutoML Tables classification model.
            PCA (14):
                Prinpical Component Analysis model.
            DNN_LINEAR_COMBINED_CLASSIFIER (16):
                Wide-and-deep classifier model.
            DNN_LINEAR_COMBINED_REGRESSOR (17):
                Wide-and-deep regressor model.
            AUTOENCODER (18):
                Autoencoder model.
            ARIMA_PLUS (19):
                New name for the ARIMA model.
            ARIMA_PLUS_XREG (23):
                ARIMA with external regressors.
            RANDOM_FOREST_REGRESSOR (24):
                Random forest regressor model.
            RANDOM_FOREST_CLASSIFIER (25):
                Random forest classifier model.
            TENSORFLOW_LITE (26):
                An imported TensorFlow Lite model.
            ONNX (28):
                An imported ONNX model.
            TRANSFORM_ONLY (29):
                Model to capture the columns and logic in the
                TRANSFORM clause along with statistics useful
                for ML analytic functions.
            CONTRIBUTION_ANALYSIS (37):
                The contribution analysis model.
        """
        MODEL_TYPE_UNSPECIFIED = 0
        LINEAR_REGRESSION = 1
        LOGISTIC_REGRESSION = 2
        KMEANS = 3
        MATRIX_FACTORIZATION = 4
        DNN_CLASSIFIER = 5
        TENSORFLOW = 6
        DNN_REGRESSOR = 7
        XGBOOST = 8
        BOOSTED_TREE_REGRESSOR = 9
        BOOSTED_TREE_CLASSIFIER = 10
        ARIMA = 11
        AUTOML_REGRESSOR = 12
        AUTOML_CLASSIFIER = 13
        PCA = 14
        DNN_LINEAR_COMBINED_CLASSIFIER = 16
        DNN_LINEAR_COMBINED_REGRESSOR = 17
        AUTOENCODER = 18
        ARIMA_PLUS = 19
        ARIMA_PLUS_XREG = 23
        RANDOM_FOREST_REGRESSOR = 24
        RANDOM_FOREST_CLASSIFIER = 25
        TENSORFLOW_LITE = 26
        ONNX = 28
        TRANSFORM_ONLY = 29
        CONTRIBUTION_ANALYSIS = 37

    class LossType(proto.Enum):
        r"""Loss metric to evaluate model training performance.

        Values:
            LOSS_TYPE_UNSPECIFIED (0):
                Default value.
            MEAN_SQUARED_LOSS (1):
                Mean squared loss, used for linear
                regression.
            MEAN_LOG_LOSS (2):
                Mean log loss, used for logistic regression.
        """
        LOSS_TYPE_UNSPECIFIED = 0
        MEAN_SQUARED_LOSS = 1
        MEAN_LOG_LOSS = 2

    class DistanceType(proto.Enum):
        r"""Distance metric used to compute the distance between two
        points.

        Values:
            DISTANCE_TYPE_UNSPECIFIED (0):
                Default value.
            EUCLIDEAN (1):
                Eculidean distance.
            COSINE (2):
                Cosine distance.
        """
        DISTANCE_TYPE_UNSPECIFIED = 0
        EUCLIDEAN = 1
        COSINE = 2

    class DataSplitMethod(proto.Enum):
        r"""Indicates the method to split input data into multiple
        tables.

        Values:
            DATA_SPLIT_METHOD_UNSPECIFIED (0):
                Default value.
            RANDOM (1):
                Splits data randomly.
            CUSTOM (2):
                Splits data with the user provided tags.
            SEQUENTIAL (3):
                Splits data sequentially.
            NO_SPLIT (4):
                Data split will be skipped.
            AUTO_SPLIT (5):
                Splits data automatically: Uses NO_SPLIT if the data size is
                small. Otherwise uses RANDOM.
        """
        DATA_SPLIT_METHOD_UNSPECIFIED = 0
        RANDOM = 1
        CUSTOM = 2
        SEQUENTIAL = 3
        NO_SPLIT = 4
        AUTO_SPLIT = 5

    class DataFrequency(proto.Enum):
        r"""Type of supported data frequency for time series forecasting
        models.

        Values:
            DATA_FREQUENCY_UNSPECIFIED (0):
                Default value.
            AUTO_FREQUENCY (1):
                Automatically inferred from timestamps.
            YEARLY (2):
                Yearly data.
            QUARTERLY (3):
                Quarterly data.
            MONTHLY (4):
                Monthly data.
            WEEKLY (5):
                Weekly data.
            DAILY (6):
                Daily data.
            HOURLY (7):
                Hourly data.
            PER_MINUTE (8):
                Per-minute data.
        """
        DATA_FREQUENCY_UNSPECIFIED = 0
        AUTO_FREQUENCY = 1
        YEARLY = 2
        QUARTERLY = 3
        MONTHLY = 4
        WEEKLY = 5
        DAILY = 6
        HOURLY = 7
        PER_MINUTE = 8

    class HolidayRegion(proto.Enum):
        r"""Type of supported holiday regions for time series forecasting
        models.

        Values:
            HOLIDAY_REGION_UNSPECIFIED (0):
                Holiday region unspecified.
            GLOBAL (1):
                Global.
            NA (2):
                North America.
            JAPAC (3):
                Japan and Asia Pacific: Korea, Greater China,
                India, Australia, and New Zealand.
            EMEA (4):
                Europe, the Middle East and Africa.
            LAC (5):
                Latin America and the Caribbean.
            AE (6):
                United Arab Emirates
            AR (7):
                Argentina
            AT (8):
                Austria
            AU (9):
                Australia
            BE (10):
                Belgium
            BR (11):
                Brazil
            CA (12):
                Canada
            CH (13):
                Switzerland
            CL (14):
                Chile
            CN (15):
                China
            CO (16):
                Colombia
            CS (17):
                Czechoslovakia
            CZ (18):
                Czech Republic
            DE (19):
                Germany
            DK (20):
                Denmark
            DZ (21):
                Algeria
            EC (22):
                Ecuador
            EE (23):
                Estonia
            EG (24):
                Egypt
            ES (25):
                Spain
            FI (26):
                Finland
            FR (27):
                France
            GB (28):
                Great Britain (United Kingdom)
            GR (29):
                Greece
            HK (30):
                Hong Kong
            HU (31):
                Hungary
            ID (32):
                Indonesia
            IE (33):
                Ireland
            IL (34):
                Israel
            IN (35):
                India
            IR (36):
                Iran
            IT (37):
                Italy
            JP (38):
                Japan
            KR (39):
                Korea (South)
            LV (40):
                Latvia
            MA (41):
                Morocco
            MX (42):
                Mexico
            MY (43):
                Malaysia
            NG (44):
                Nigeria
            NL (45):
                Netherlands
            NO (46):
                Norway
            NZ (47):
                New Zealand
            PE (48):
                Peru
            PH (49):
                Philippines
            PK (50):
                Pakistan
            PL (51):
                Poland
            PT (52):
                Portugal
            RO (53):
                Romania
            RS (54):
                Serbia
            RU (55):
                Russian Federation
            SA (56):
                Saudi Arabia
            SE (57):
                Sweden
            SG (58):
                Singapore
            SI (59):
                Slovenia
            SK (60):
                Slovakia
            TH (61):
                Thailand
            TR (62):
                Turkey
            TW (63):
                Taiwan
            UA (64):
                Ukraine
            US (65):
                United States
            VE (66):
                Venezuela
            VN (67):
                Vietnam
            ZA (68):
                South Africa
        """
        HOLIDAY_REGION_UNSPECIFIED = 0
        GLOBAL = 1
        NA = 2
        JAPAC = 3
        EMEA = 4
        LAC = 5
        AE = 6
        AR = 7
        AT = 8
        AU = 9
        BE = 10
        BR = 11
        CA = 12
        CH = 13
        CL = 14
        CN = 15
        CO = 16
        CS = 17
        CZ = 18
        DE = 19
        DK = 20
        DZ = 21
        EC = 22
        EE = 23
        EG = 24
        ES = 25
        FI = 26
        FR = 27
        GB = 28
        GR = 29
        HK = 30
        HU = 31
        ID = 32
        IE = 33
        IL = 34
        IN = 35
        IR = 36
        IT = 37
        JP = 38
        KR = 39
        LV = 40
        MA = 41
        MX = 42
        MY = 43
        NG = 44
        NL = 45
        NO = 46
        NZ = 47
        PE = 48
        PH = 49
        PK = 50
        PL = 51
        PT = 52
        RO = 53
        RS = 54
        RU = 55
        SA = 56
        SE = 57
        SG = 58
        SI = 59
        SK = 60
        TH = 61
        TR = 62
        TW = 63
        UA = 64
        US = 65
        VE = 66
        VN = 67
        ZA = 68

    class ColorSpace(proto.Enum):
        r"""Enums for color space, used for processing images in Object
        Table. See more details at
        https://www.tensorflow.org/io/tutorials/colorspace.

        Values:
            COLOR_SPACE_UNSPECIFIED (0):
                Unspecified color space
            RGB (1):
                RGB
            HSV (2):
                HSV
            YIQ (3):
                YIQ
            YUV (4):
                YUV
            GRAYSCALE (5):
                GRAYSCALE
        """
        COLOR_SPACE_UNSPECIFIED = 0
        RGB = 1
        HSV = 2
        YIQ = 3
        YUV = 4
        GRAYSCALE = 5

    class LearnRateStrategy(proto.Enum):
        r"""Indicates the learning rate optimization strategy to use.

        Values:
            LEARN_RATE_STRATEGY_UNSPECIFIED (0):
                Default value.
            LINE_SEARCH (1):
                Use line search to determine learning rate.
            CONSTANT (2):
                Use a constant learning rate.
        """
        LEARN_RATE_STRATEGY_UNSPECIFIED = 0
        LINE_SEARCH = 1
        CONSTANT = 2

    class OptimizationStrategy(proto.Enum):
        r"""Indicates the optimization strategy used for training.

        Values:
            OPTIMIZATION_STRATEGY_UNSPECIFIED (0):
                Default value.
            BATCH_GRADIENT_DESCENT (1):
                Uses an iterative batch gradient descent
                algorithm.
            NORMAL_EQUATION (2):
                Uses a normal equation to solve linear
                regression problem.
        """
        OPTIMIZATION_STRATEGY_UNSPECIFIED = 0
        BATCH_GRADIENT_DESCENT = 1
        NORMAL_EQUATION = 2

    class FeedbackType(proto.Enum):
        r"""Indicates the training algorithm to use for matrix
        factorization models.

        Values:
            FEEDBACK_TYPE_UNSPECIFIED (0):
                Default value.
            IMPLICIT (1):
                Use weighted-als for implicit feedback
                problems.
            EXPLICIT (2):
                Use nonweighted-als for explicit feedback
                problems.
        """
        FEEDBACK_TYPE_UNSPECIFIED = 0
        IMPLICIT = 1
        EXPLICIT = 2

    class SeasonalPeriod(proto.Message):
        r"""Enums for seasonal period."""

        class SeasonalPeriodType(proto.Enum):
            r"""Seasonal period type.

            Values:
                SEASONAL_PERIOD_TYPE_UNSPECIFIED (0):
                    Unspecified seasonal period.
                NO_SEASONALITY (1):
                    No seasonality
                DAILY (2):
                    Daily period, 24 hours.
                WEEKLY (3):
                    Weekly period, 7 days.
                MONTHLY (4):
                    Monthly period, 30 days or irregular.
                QUARTERLY (5):
                    Quarterly period, 90 days or irregular.
                YEARLY (6):
                    Yearly period, 365 days or irregular.
            """
            SEASONAL_PERIOD_TYPE_UNSPECIFIED = 0
            NO_SEASONALITY = 1
            DAILY = 2
            WEEKLY = 3
            MONTHLY = 4
            QUARTERLY = 5
            YEARLY = 6

    class KmeansEnums(proto.Message):
        r"""Enums for kmeans model type."""

        class KmeansInitializationMethod(proto.Enum):
            r"""Indicates the method used to initialize the centroids for
            KMeans clustering algorithm.

            Values:
                KMEANS_INITIALIZATION_METHOD_UNSPECIFIED (0):
                    Unspecified initialization method.
                RANDOM (1):
                    Initializes the centroids randomly.
                CUSTOM (2):
                    Initializes the centroids using data specified in
                    kmeans_initialization_column.
                KMEANS_PLUS_PLUS (3):
                    Initializes with kmeans++.
            """
            KMEANS_INITIALIZATION_METHOD_UNSPECIFIED = 0
            RANDOM = 1
            CUSTOM = 2
            KMEANS_PLUS_PLUS = 3

    class BoostedTreeOptionEnums(proto.Message):
        r"""Enums for XGBoost model type."""

        class BoosterType(proto.Enum):
            r"""Booster types supported. Refer to booster parameter in
            XGBoost.

            Values:
                BOOSTER_TYPE_UNSPECIFIED (0):
                    Unspecified booster type.
                GBTREE (1):
                    Gbtree booster.
                DART (2):
                    Dart booster.
            """
            BOOSTER_TYPE_UNSPECIFIED = 0
            GBTREE = 1
            DART = 2

        class DartNormalizeType(proto.Enum):
            r"""Type of normalization algorithm for boosted tree models using dart
            booster. Refer to normalize_type in XGBoost.

            Values:
                DART_NORMALIZE_TYPE_UNSPECIFIED (0):
                    Unspecified dart normalize type.
                TREE (1):
                    New trees have the same weight of each of
                    dropped trees.
                FOREST (2):
                    New trees have the same weight of sum of
                    dropped trees.
            """
            DART_NORMALIZE_TYPE_UNSPECIFIED = 0
            TREE = 1
            FOREST = 2

        class TreeMethod(proto.Enum):
            r"""Tree construction algorithm used in boosted tree models. Refer to
            tree_method in XGBoost.

            Values:
                TREE_METHOD_UNSPECIFIED (0):
                    Unspecified tree method.
                AUTO (1):
                    Use heuristic to choose the fastest method.
                EXACT (2):
                    Exact greedy algorithm.
                APPROX (3):
                    Approximate greedy algorithm using quantile
                    sketch and gradient histogram.
                HIST (4):
                    Fast histogram optimized approximate greedy
                    algorithm.
            """
            TREE_METHOD_UNSPECIFIED = 0
            AUTO = 1
            EXACT = 2
            APPROX = 3
            HIST = 4

    class HparamTuningEnums(proto.Message):
        r"""Enums for hyperparameter tuning."""

        class HparamTuningObjective(proto.Enum):
            r"""Available evaluation metrics used as hyperparameter tuning
            objectives.

            Values:
                HPARAM_TUNING_OBJECTIVE_UNSPECIFIED (0):
                    Unspecified evaluation metric.
                MEAN_ABSOLUTE_ERROR (1):
                    Mean absolute error. mean_absolute_error = AVG(ABS(label -
                    predicted))
                MEAN_SQUARED_ERROR (2):
                    Mean squared error. mean_squared_error = AVG(POW(label -
                    predicted, 2))
                MEAN_SQUARED_LOG_ERROR (3):
                    Mean squared log error. mean_squared_log_error =
                    AVG(POW(LN(1 + label) - LN(1 + predicted), 2))
                MEDIAN_ABSOLUTE_ERROR (4):
                    Mean absolute error. median_absolute_error =
                    APPROX_QUANTILES(absolute_error, 2)[OFFSET(1)]
                R_SQUARED (5):
                    R^2 score. This corresponds to r2_score in ML.EVALUATE.
                    r_squared = 1 -
                    SUM(squared_error)/(COUNT(label)*VAR_POP(label))
                EXPLAINED_VARIANCE (6):
                    Explained variance. explained_variance = 1 -
                    VAR_POP(label_error)/VAR_POP(label)
                PRECISION (7):
                    Precision is the fraction of actual positive
                    predictions that had positive actual labels. For
                    multiclass this is a macro-averaged metric
                    treating each class as a binary classifier.
                RECALL (8):
                    Recall is the fraction of actual positive
                    labels that were given a positive prediction.
                    For multiclass this is a macro-averaged metric.
                ACCURACY (9):
                    Accuracy is the fraction of predictions given
                    the correct label. For multiclass this is a
                    globally micro-averaged metric.
                F1_SCORE (10):
                    The F1 score is an average of recall and
                    precision. For multiclass this is a
                    macro-averaged metric.
                LOG_LOSS (11):
                    Logarithmic Loss. For multiclass this is a
                    macro-averaged metric.
                ROC_AUC (12):
                    Area Under an ROC Curve. For multiclass this
                    is a macro-averaged metric.
                DAVIES_BOULDIN_INDEX (13):
                    Davies-Bouldin Index.
                MEAN_AVERAGE_PRECISION (14):
                    Mean Average Precision.
                NORMALIZED_DISCOUNTED_CUMULATIVE_GAIN (15):
                    Normalized Discounted Cumulative Gain.
                AVERAGE_RANK (16):
                    Average Rank.
            """
            HPARAM_TUNING_OBJECTIVE_UNSPECIFIED = 0
            MEAN_ABSOLUTE_ERROR = 1
            MEAN_SQUARED_ERROR = 2
            MEAN_SQUARED_LOG_ERROR = 3
            MEDIAN_ABSOLUTE_ERROR = 4
            R_SQUARED = 5
            EXPLAINED_VARIANCE = 6
            PRECISION = 7
            RECALL = 8
            ACCURACY = 9
            F1_SCORE = 10
            LOG_LOSS = 11
            ROC_AUC = 12
            DAVIES_BOULDIN_INDEX = 13
            MEAN_AVERAGE_PRECISION = 14
            NORMALIZED_DISCOUNTED_CUMULATIVE_GAIN = 15
            AVERAGE_RANK = 16

    class RegressionMetrics(proto.Message):
        r"""Evaluation metrics for regression and explicit feedback type
        matrix factorization models.

        Attributes:
            mean_absolute_error (google.protobuf.wrappers_pb2.DoubleValue):
                Mean absolute error.
            mean_squared_error (google.protobuf.wrappers_pb2.DoubleValue):
                Mean squared error.
            mean_squared_log_error (google.protobuf.wrappers_pb2.DoubleValue):
                Mean squared log error.
            median_absolute_error (google.protobuf.wrappers_pb2.DoubleValue):
                Median absolute error.
            r_squared (google.protobuf.wrappers_pb2.DoubleValue):
                R^2 score. This corresponds to r2_score in ML.EVALUATE.
        """

        mean_absolute_error: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.DoubleValue,
        )
        mean_squared_error: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.DoubleValue,
        )
        mean_squared_log_error: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=3,
            message=wrappers_pb2.DoubleValue,
        )
        median_absolute_error: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=4,
            message=wrappers_pb2.DoubleValue,
        )
        r_squared: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=5,
            message=wrappers_pb2.DoubleValue,
        )

    class AggregateClassificationMetrics(proto.Message):
        r"""Aggregate metrics for classification/classifier models. For
        multi-class models, the metrics are either macro-averaged or
        micro-averaged. When macro-averaged, the metrics are calculated
        for each label and then an unweighted average is taken of those
        values. When micro-averaged, the metric is calculated globally
        by counting the total number of correctly predicted rows.

        Attributes:
            precision (google.protobuf.wrappers_pb2.DoubleValue):
                Precision is the fraction of actual positive
                predictions that had positive actual labels. For
                multiclass this is a macro-averaged metric
                treating each class as a binary classifier.
            recall (google.protobuf.wrappers_pb2.DoubleValue):
                Recall is the fraction of actual positive
                labels that were given a positive prediction.
                For multiclass this is a macro-averaged metric.
            accuracy (google.protobuf.wrappers_pb2.DoubleValue):
                Accuracy is the fraction of predictions given
                the correct label. For multiclass this is a
                micro-averaged metric.
            threshold (google.protobuf.wrappers_pb2.DoubleValue):
                Threshold at which the metrics are computed.
                For binary classification models this is the
                positive class threshold. For multi-class
                classification models this is the confidence
                threshold.
            f1_score (google.protobuf.wrappers_pb2.DoubleValue):
                The F1 score is an average of recall and
                precision. For multiclass this is a
                macro-averaged metric.
            log_loss (google.protobuf.wrappers_pb2.DoubleValue):
                Logarithmic Loss. For multiclass this is a
                macro-averaged metric.
            roc_auc (google.protobuf.wrappers_pb2.DoubleValue):
                Area Under a ROC Curve. For multiclass this
                is a macro-averaged metric.
        """

        precision: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.DoubleValue,
        )
        recall: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.DoubleValue,
        )
        accuracy: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=3,
            message=wrappers_pb2.DoubleValue,
        )
        threshold: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=4,
            message=wrappers_pb2.DoubleValue,
        )
        f1_score: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=5,
            message=wrappers_pb2.DoubleValue,
        )
        log_loss: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=6,
            message=wrappers_pb2.DoubleValue,
        )
        roc_auc: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=7,
            message=wrappers_pb2.DoubleValue,
        )

    class BinaryClassificationMetrics(proto.Message):
        r"""Evaluation metrics for binary classification/classifier
        models.

        Attributes:
            aggregate_classification_metrics (google.cloud.bigquery_v2.types.Model.AggregateClassificationMetrics):
                Aggregate classification metrics.
            binary_confusion_matrix_list (MutableSequence[google.cloud.bigquery_v2.types.Model.BinaryClassificationMetrics.BinaryConfusionMatrix]):
                Binary confusion matrix at multiple
                thresholds.
            positive_label (str):
                Label representing the positive class.
            negative_label (str):
                Label representing the negative class.
        """

        class BinaryConfusionMatrix(proto.Message):
            r"""Confusion matrix for binary classification models.

            Attributes:
                positive_class_threshold (google.protobuf.wrappers_pb2.DoubleValue):
                    Threshold value used when computing each of
                    the following metric.
                true_positives (google.protobuf.wrappers_pb2.Int64Value):
                    Number of true samples predicted as true.
                false_positives (google.protobuf.wrappers_pb2.Int64Value):
                    Number of false samples predicted as true.
                true_negatives (google.protobuf.wrappers_pb2.Int64Value):
                    Number of true samples predicted as false.
                false_negatives (google.protobuf.wrappers_pb2.Int64Value):
                    Number of false samples predicted as false.
                precision (google.protobuf.wrappers_pb2.DoubleValue):
                    The fraction of actual positive predictions
                    that had positive actual labels.
                recall (google.protobuf.wrappers_pb2.DoubleValue):
                    The fraction of actual positive labels that
                    were given a positive prediction.
                f1_score (google.protobuf.wrappers_pb2.DoubleValue):
                    The equally weighted average of recall and
                    precision.
                accuracy (google.protobuf.wrappers_pb2.DoubleValue):
                    The fraction of predictions given the correct
                    label.
            """

            positive_class_threshold: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.DoubleValue,
            )
            true_positives: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=2,
                message=wrappers_pb2.Int64Value,
            )
            false_positives: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=3,
                message=wrappers_pb2.Int64Value,
            )
            true_negatives: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=4,
                message=wrappers_pb2.Int64Value,
            )
            false_negatives: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=5,
                message=wrappers_pb2.Int64Value,
            )
            precision: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=6,
                message=wrappers_pb2.DoubleValue,
            )
            recall: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=7,
                message=wrappers_pb2.DoubleValue,
            )
            f1_score: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=8,
                message=wrappers_pb2.DoubleValue,
            )
            accuracy: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=9,
                message=wrappers_pb2.DoubleValue,
            )

        aggregate_classification_metrics: "Model.AggregateClassificationMetrics" = (
            proto.Field(
                proto.MESSAGE,
                number=1,
                message="Model.AggregateClassificationMetrics",
            )
        )
        binary_confusion_matrix_list: MutableSequence[
            "Model.BinaryClassificationMetrics.BinaryConfusionMatrix"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Model.BinaryClassificationMetrics.BinaryConfusionMatrix",
        )
        positive_label: str = proto.Field(
            proto.STRING,
            number=3,
        )
        negative_label: str = proto.Field(
            proto.STRING,
            number=4,
        )

    class MultiClassClassificationMetrics(proto.Message):
        r"""Evaluation metrics for multi-class classification/classifier
        models.

        Attributes:
            aggregate_classification_metrics (google.cloud.bigquery_v2.types.Model.AggregateClassificationMetrics):
                Aggregate classification metrics.
            confusion_matrix_list (MutableSequence[google.cloud.bigquery_v2.types.Model.MultiClassClassificationMetrics.ConfusionMatrix]):
                Confusion matrix at different thresholds.
        """

        class ConfusionMatrix(proto.Message):
            r"""Confusion matrix for multi-class classification models.

            Attributes:
                confidence_threshold (google.protobuf.wrappers_pb2.DoubleValue):
                    Confidence threshold used when computing the
                    entries of the confusion matrix.
                rows (MutableSequence[google.cloud.bigquery_v2.types.Model.MultiClassClassificationMetrics.ConfusionMatrix.Row]):
                    One row per actual label.
            """

            class Entry(proto.Message):
                r"""A single entry in the confusion matrix.

                Attributes:
                    predicted_label (str):
                        The predicted label. For confidence_threshold > 0, we will
                        also add an entry indicating the number of items under the
                        confidence threshold.
                    item_count (google.protobuf.wrappers_pb2.Int64Value):
                        Number of items being predicted as this
                        label.
                """

                predicted_label: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                item_count: wrappers_pb2.Int64Value = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    message=wrappers_pb2.Int64Value,
                )

            class Row(proto.Message):
                r"""A single row in the confusion matrix.

                Attributes:
                    actual_label (str):
                        The original label of this row.
                    entries (MutableSequence[google.cloud.bigquery_v2.types.Model.MultiClassClassificationMetrics.ConfusionMatrix.Entry]):
                        Info describing predicted label distribution.
                """

                actual_label: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                entries: MutableSequence[
                    "Model.MultiClassClassificationMetrics.ConfusionMatrix.Entry"
                ] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=2,
                    message="Model.MultiClassClassificationMetrics.ConfusionMatrix.Entry",
                )

            confidence_threshold: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.DoubleValue,
            )
            rows: MutableSequence[
                "Model.MultiClassClassificationMetrics.ConfusionMatrix.Row"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Model.MultiClassClassificationMetrics.ConfusionMatrix.Row",
            )

        aggregate_classification_metrics: "Model.AggregateClassificationMetrics" = (
            proto.Field(
                proto.MESSAGE,
                number=1,
                message="Model.AggregateClassificationMetrics",
            )
        )
        confusion_matrix_list: MutableSequence[
            "Model.MultiClassClassificationMetrics.ConfusionMatrix"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Model.MultiClassClassificationMetrics.ConfusionMatrix",
        )

    class ClusteringMetrics(proto.Message):
        r"""Evaluation metrics for clustering models.

        Attributes:
            davies_bouldin_index (google.protobuf.wrappers_pb2.DoubleValue):
                Davies-Bouldin index.
            mean_squared_distance (google.protobuf.wrappers_pb2.DoubleValue):
                Mean of squared distances between each sample
                to its cluster centroid.
            clusters (MutableSequence[google.cloud.bigquery_v2.types.Model.ClusteringMetrics.Cluster]):
                Information for all clusters.
        """

        class Cluster(proto.Message):
            r"""Message containing the information about one cluster.

            Attributes:
                centroid_id (int):
                    Centroid id.
                feature_values (MutableSequence[google.cloud.bigquery_v2.types.Model.ClusteringMetrics.Cluster.FeatureValue]):
                    Values of highly variant features for this
                    cluster.
                count (google.protobuf.wrappers_pb2.Int64Value):
                    Count of training data rows that were
                    assigned to this cluster.
            """

            class FeatureValue(proto.Message):
                r"""Representative value of a single feature within the cluster.

                This message has `oneof`_ fields (mutually exclusive fields).
                For each oneof, at most one member field can be set at the same time.
                Setting any member of the oneof automatically clears all other
                members.

                .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

                Attributes:
                    feature_column (str):
                        The feature column name.
                    numerical_value (google.protobuf.wrappers_pb2.DoubleValue):
                        The numerical feature value. This is the
                        centroid value for this feature.

                        This field is a member of `oneof`_ ``value``.
                    categorical_value (google.cloud.bigquery_v2.types.Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue):
                        The categorical feature value.

                        This field is a member of `oneof`_ ``value``.
                """

                class CategoricalValue(proto.Message):
                    r"""Representative value of a categorical feature.

                    Attributes:
                        category_counts (MutableSequence[google.cloud.bigquery_v2.types.Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue.CategoryCount]):
                            Counts of all categories for the categorical feature. If
                            there are more than ten categories, we return top ten (by
                            count) and return one more CategoryCount with category
                            "*OTHER*" and count as aggregate counts of remaining
                            categories.
                    """

                    class CategoryCount(proto.Message):
                        r"""Represents the count of a single category within the cluster.

                        Attributes:
                            category (str):
                                The name of category.
                            count (google.protobuf.wrappers_pb2.Int64Value):
                                The count of training samples matching the
                                category within the cluster.
                        """

                        category: str = proto.Field(
                            proto.STRING,
                            number=1,
                        )
                        count: wrappers_pb2.Int64Value = proto.Field(
                            proto.MESSAGE,
                            number=2,
                            message=wrappers_pb2.Int64Value,
                        )

                    category_counts: MutableSequence[
                        "Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue.CategoryCount"
                    ] = proto.RepeatedField(
                        proto.MESSAGE,
                        number=1,
                        message="Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue.CategoryCount",
                    )

                feature_column: str = proto.Field(
                    proto.STRING,
                    number=1,
                )
                numerical_value: wrappers_pb2.DoubleValue = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    oneof="value",
                    message=wrappers_pb2.DoubleValue,
                )
                categorical_value: "Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue" = proto.Field(
                    proto.MESSAGE,
                    number=3,
                    oneof="value",
                    message="Model.ClusteringMetrics.Cluster.FeatureValue.CategoricalValue",
                )

            centroid_id: int = proto.Field(
                proto.INT64,
                number=1,
            )
            feature_values: MutableSequence[
                "Model.ClusteringMetrics.Cluster.FeatureValue"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Model.ClusteringMetrics.Cluster.FeatureValue",
            )
            count: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=3,
                message=wrappers_pb2.Int64Value,
            )

        davies_bouldin_index: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.DoubleValue,
        )
        mean_squared_distance: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.DoubleValue,
        )
        clusters: MutableSequence[
            "Model.ClusteringMetrics.Cluster"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="Model.ClusteringMetrics.Cluster",
        )

    class RankingMetrics(proto.Message):
        r"""Evaluation metrics used by weighted-ALS models specified by
        feedback_type=implicit.

        Attributes:
            mean_average_precision (google.protobuf.wrappers_pb2.DoubleValue):
                Calculates a precision per user for all the
                items by ranking them and then averages all the
                precisions across all the users.
            mean_squared_error (google.protobuf.wrappers_pb2.DoubleValue):
                Similar to the mean squared error computed in
                regression and explicit recommendation models
                except instead of computing the rating directly,
                the output from evaluate is computed against a
                preference which is 1 or 0 depending on if the
                rating exists or not.
            normalized_discounted_cumulative_gain (google.protobuf.wrappers_pb2.DoubleValue):
                A metric to determine the goodness of a
                ranking calculated from the predicted confidence
                by comparing it to an ideal rank measured by the
                original ratings.
            average_rank (google.protobuf.wrappers_pb2.DoubleValue):
                Determines the goodness of a ranking by
                computing the percentile rank from the predicted
                confidence and dividing it by the original rank.
        """

        mean_average_precision: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.DoubleValue,
        )
        mean_squared_error: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.DoubleValue,
        )
        normalized_discounted_cumulative_gain: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=3,
            message=wrappers_pb2.DoubleValue,
        )
        average_rank: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=4,
            message=wrappers_pb2.DoubleValue,
        )

    class ArimaForecastingMetrics(proto.Message):
        r"""Model evaluation metrics for ARIMA forecasting models.

        Attributes:
            arima_single_model_forecasting_metrics (MutableSequence[google.cloud.bigquery_v2.types.Model.ArimaForecastingMetrics.ArimaSingleModelForecastingMetrics]):
                Repeated as there can be many metric sets
                (one for each model) in auto-arima and the
                large-scale case.
        """

        class ArimaSingleModelForecastingMetrics(proto.Message):
            r"""Model evaluation metrics for a single ARIMA forecasting
            model.

            Attributes:
                non_seasonal_order (google.cloud.bigquery_v2.types.Model.ArimaOrder):
                    Non-seasonal order.
                arima_fitting_metrics (google.cloud.bigquery_v2.types.Model.ArimaFittingMetrics):
                    Arima fitting metrics.
                has_drift (google.protobuf.wrappers_pb2.BoolValue):
                    Is arima model fitted with drift or not. It
                    is always false when d is not 1.
                time_series_id (str):
                    The time_series_id value for this time series. It will be
                    one of the unique values from the time_series_id_column
                    specified during ARIMA model training. Only present when
                    time_series_id_column training option was used.
                time_series_ids (MutableSequence[str]):
                    The tuple of time_series_ids identifying this time series.
                    It will be one of the unique tuples of values present in the
                    time_series_id_columns specified during ARIMA model
                    training. Only present when time_series_id_columns training
                    option was used and the order of values here are same as the
                    order of time_series_id_columns.
                seasonal_periods (MutableSequence[google.cloud.bigquery_v2.types.Model.SeasonalPeriod.SeasonalPeriodType]):
                    Seasonal periods. Repeated because multiple
                    periods are supported for one time series.
                has_holiday_effect (google.protobuf.wrappers_pb2.BoolValue):
                    If true, holiday_effect is a part of time series
                    decomposition result.
                has_spikes_and_dips (google.protobuf.wrappers_pb2.BoolValue):
                    If true, spikes_and_dips is a part of time series
                    decomposition result.
                has_step_changes (google.protobuf.wrappers_pb2.BoolValue):
                    If true, step_changes is a part of time series decomposition
                    result.
            """

            non_seasonal_order: "Model.ArimaOrder" = proto.Field(
                proto.MESSAGE,
                number=1,
                message="Model.ArimaOrder",
            )
            arima_fitting_metrics: "Model.ArimaFittingMetrics" = proto.Field(
                proto.MESSAGE,
                number=2,
                message="Model.ArimaFittingMetrics",
            )
            has_drift: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=3,
                message=wrappers_pb2.BoolValue,
            )
            time_series_id: str = proto.Field(
                proto.STRING,
                number=4,
            )
            time_series_ids: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=9,
            )
            seasonal_periods: MutableSequence[
                "Model.SeasonalPeriod.SeasonalPeriodType"
            ] = proto.RepeatedField(
                proto.ENUM,
                number=5,
                enum="Model.SeasonalPeriod.SeasonalPeriodType",
            )
            has_holiday_effect: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=6,
                message=wrappers_pb2.BoolValue,
            )
            has_spikes_and_dips: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=7,
                message=wrappers_pb2.BoolValue,
            )
            has_step_changes: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=8,
                message=wrappers_pb2.BoolValue,
            )

        arima_single_model_forecasting_metrics: MutableSequence[
            "Model.ArimaForecastingMetrics.ArimaSingleModelForecastingMetrics"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=6,
            message="Model.ArimaForecastingMetrics.ArimaSingleModelForecastingMetrics",
        )

    class DimensionalityReductionMetrics(proto.Message):
        r"""Model evaluation metrics for dimensionality reduction models.

        Attributes:
            total_explained_variance_ratio (google.protobuf.wrappers_pb2.DoubleValue):
                Total percentage of variance explained by the
                selected principal components.
        """

        total_explained_variance_ratio: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.DoubleValue,
        )

    class EvaluationMetrics(proto.Message):
        r"""Evaluation metrics of a model. These are either computed on
        all training data or just the eval data based on whether eval
        data was used during training. These are not present for
        imported models.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            regression_metrics (google.cloud.bigquery_v2.types.Model.RegressionMetrics):
                Populated for regression models and explicit
                feedback type matrix factorization models.

                This field is a member of `oneof`_ ``metrics``.
            binary_classification_metrics (google.cloud.bigquery_v2.types.Model.BinaryClassificationMetrics):
                Populated for binary
                classification/classifier models.

                This field is a member of `oneof`_ ``metrics``.
            multi_class_classification_metrics (google.cloud.bigquery_v2.types.Model.MultiClassClassificationMetrics):
                Populated for multi-class
                classification/classifier models.

                This field is a member of `oneof`_ ``metrics``.
            clustering_metrics (google.cloud.bigquery_v2.types.Model.ClusteringMetrics):
                Populated for clustering models.

                This field is a member of `oneof`_ ``metrics``.
            ranking_metrics (google.cloud.bigquery_v2.types.Model.RankingMetrics):
                Populated for implicit feedback type matrix
                factorization models.

                This field is a member of `oneof`_ ``metrics``.
            arima_forecasting_metrics (google.cloud.bigquery_v2.types.Model.ArimaForecastingMetrics):
                Populated for ARIMA models.

                This field is a member of `oneof`_ ``metrics``.
            dimensionality_reduction_metrics (google.cloud.bigquery_v2.types.Model.DimensionalityReductionMetrics):
                Evaluation metrics when the model is a
                dimensionality reduction model, which currently
                includes PCA.

                This field is a member of `oneof`_ ``metrics``.
        """

        regression_metrics: "Model.RegressionMetrics" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="metrics",
            message="Model.RegressionMetrics",
        )
        binary_classification_metrics: "Model.BinaryClassificationMetrics" = (
            proto.Field(
                proto.MESSAGE,
                number=2,
                oneof="metrics",
                message="Model.BinaryClassificationMetrics",
            )
        )
        multi_class_classification_metrics: "Model.MultiClassClassificationMetrics" = (
            proto.Field(
                proto.MESSAGE,
                number=3,
                oneof="metrics",
                message="Model.MultiClassClassificationMetrics",
            )
        )
        clustering_metrics: "Model.ClusteringMetrics" = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="metrics",
            message="Model.ClusteringMetrics",
        )
        ranking_metrics: "Model.RankingMetrics" = proto.Field(
            proto.MESSAGE,
            number=5,
            oneof="metrics",
            message="Model.RankingMetrics",
        )
        arima_forecasting_metrics: "Model.ArimaForecastingMetrics" = proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="metrics",
            message="Model.ArimaForecastingMetrics",
        )
        dimensionality_reduction_metrics: "Model.DimensionalityReductionMetrics" = (
            proto.Field(
                proto.MESSAGE,
                number=7,
                oneof="metrics",
                message="Model.DimensionalityReductionMetrics",
            )
        )

    class DataSplitResult(proto.Message):
        r"""Data split result. This contains references to the training
        and evaluation data tables that were used to train the model.

        Attributes:
            training_table (google.cloud.bigquery_v2.types.TableReference):
                Table reference of the training data after
                split.
            evaluation_table (google.cloud.bigquery_v2.types.TableReference):
                Table reference of the evaluation data after
                split.
            test_table (google.cloud.bigquery_v2.types.TableReference):
                Table reference of the test data after split.
        """

        training_table: table_reference.TableReference = proto.Field(
            proto.MESSAGE,
            number=1,
            message=table_reference.TableReference,
        )
        evaluation_table: table_reference.TableReference = proto.Field(
            proto.MESSAGE,
            number=2,
            message=table_reference.TableReference,
        )
        test_table: table_reference.TableReference = proto.Field(
            proto.MESSAGE,
            number=3,
            message=table_reference.TableReference,
        )

    class ArimaOrder(proto.Message):
        r"""Arima order, can be used for both non-seasonal and seasonal
        parts.

        Attributes:
            p (google.protobuf.wrappers_pb2.Int64Value):
                Order of the autoregressive part.
            d (google.protobuf.wrappers_pb2.Int64Value):
                Order of the differencing part.
            q (google.protobuf.wrappers_pb2.Int64Value):
                Order of the moving-average part.
        """

        p: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.Int64Value,
        )
        d: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.Int64Value,
        )
        q: wrappers_pb2.Int64Value = proto.Field(
            proto.MESSAGE,
            number=3,
            message=wrappers_pb2.Int64Value,
        )

    class ArimaFittingMetrics(proto.Message):
        r"""ARIMA model fitting metrics.

        Attributes:
            log_likelihood (google.protobuf.wrappers_pb2.DoubleValue):
                Log-likelihood.
            aic (google.protobuf.wrappers_pb2.DoubleValue):
                AIC.
            variance (google.protobuf.wrappers_pb2.DoubleValue):
                Variance.
        """

        log_likelihood: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=1,
            message=wrappers_pb2.DoubleValue,
        )
        aic: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=2,
            message=wrappers_pb2.DoubleValue,
        )
        variance: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=3,
            message=wrappers_pb2.DoubleValue,
        )

    class GlobalExplanation(proto.Message):
        r"""Global explanations containing the top most important
        features after training.

        Attributes:
            explanations (MutableSequence[google.cloud.bigquery_v2.types.Model.GlobalExplanation.Explanation]):
                A list of the top global explanations. Sorted
                by absolute value of attribution in descending
                order.
            class_label (str):
                Class label for this set of global
                explanations. Will be empty/null for binary
                logistic and linear regression models. Sorted
                alphabetically in descending order.
        """

        class Explanation(proto.Message):
            r"""Explanation for a single feature.

            Attributes:
                feature_name (str):
                    The full feature name. For non-numerical features, will be
                    formatted like ``<column_name>.<encoded_feature_name>``.
                    Overall size of feature name will always be truncated to
                    first 120 characters.
                attribution (google.protobuf.wrappers_pb2.DoubleValue):
                    Attribution of feature.
            """

            feature_name: str = proto.Field(
                proto.STRING,
                number=1,
            )
            attribution: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=2,
                message=wrappers_pb2.DoubleValue,
            )

        explanations: MutableSequence[
            "Model.GlobalExplanation.Explanation"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Model.GlobalExplanation.Explanation",
        )
        class_label: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class CategoryEncodingMethod(proto.Message):
        r"""Encoding methods for categorical features."""

        class EncodingMethod(proto.Enum):
            r"""Supported encoding methods for categorical features.

            Values:
                ENCODING_METHOD_UNSPECIFIED (0):
                    Unspecified encoding method.
                ONE_HOT_ENCODING (1):
                    Applies one-hot encoding.
                LABEL_ENCODING (2):
                    Applies label encoding.
                DUMMY_ENCODING (3):
                    Applies dummy encoding.
            """
            ENCODING_METHOD_UNSPECIFIED = 0
            ONE_HOT_ENCODING = 1
            LABEL_ENCODING = 2
            DUMMY_ENCODING = 3

    class PcaSolverOptionEnums(proto.Message):
        r"""PCA solver options."""

        class PcaSolver(proto.Enum):
            r"""Enums for supported PCA solvers.

            Values:
                UNSPECIFIED (0):
                    Default value.
                FULL (1):
                    Full eigen-decoposition.
                RANDOMIZED (2):
                    Randomized SVD.
                AUTO (3):
                    Auto.
            """
            UNSPECIFIED = 0
            FULL = 1
            RANDOMIZED = 2
            AUTO = 3

    class ModelRegistryOptionEnums(proto.Message):
        r"""Model registry options."""

        class ModelRegistry(proto.Enum):
            r"""Enums for supported model registries.

            Values:
                MODEL_REGISTRY_UNSPECIFIED (0):
                    Default value.
                VERTEX_AI (1):
                    Vertex AI.
            """
            MODEL_REGISTRY_UNSPECIFIED = 0
            VERTEX_AI = 1

    class TrainingRun(proto.Message):
        r"""Information about a single training query run for the model.

        Attributes:
            training_options (google.cloud.bigquery_v2.types.Model.TrainingRun.TrainingOptions):
                Output only. Options that were used for this
                training run, includes user specified and
                default options that were used.
            start_time (google.protobuf.timestamp_pb2.Timestamp):
                Output only. The start time of this training
                run.
            results (MutableSequence[google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult]):
                Output only. Output of each iteration run, results.size() <=
                max_iterations.
            evaluation_metrics (google.cloud.bigquery_v2.types.Model.EvaluationMetrics):
                Output only. The evaluation metrics over
                training/eval data that were computed at the end
                of training.
            data_split_result (google.cloud.bigquery_v2.types.Model.DataSplitResult):
                Output only. Data split result of the
                training run. Only set when the input data is
                actually split.
            model_level_global_explanation (google.cloud.bigquery_v2.types.Model.GlobalExplanation):
                Output only. Global explanation contains the
                explanation of top features on the model level.
                Applies to both regression and classification
                models.
            class_level_global_explanations (MutableSequence[google.cloud.bigquery_v2.types.Model.GlobalExplanation]):
                Output only. Global explanation contains the
                explanation of top features on the class level.
                Applies to classification models only.
            vertex_ai_model_id (str):
                The model id in the `Vertex AI Model
                Registry <https://cloud.google.com/vertex-ai/docs/model-registry/introduction>`__
                for this training run.
            vertex_ai_model_version (str):
                Output only. The model version in the `Vertex AI Model
                Registry <https://cloud.google.com/vertex-ai/docs/model-registry/introduction>`__
                for this training run.
        """

        class TrainingOptions(proto.Message):
            r"""Options used in model training.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                max_iterations (int):
                    The maximum number of iterations in training.
                    Used only for iterative training algorithms.
                loss_type (google.cloud.bigquery_v2.types.Model.LossType):
                    Type of loss function used during training
                    run.
                learn_rate (float):
                    Learning rate in training. Used only for
                    iterative training algorithms.
                l1_regularization (google.protobuf.wrappers_pb2.DoubleValue):
                    L1 regularization coefficient.
                l2_regularization (google.protobuf.wrappers_pb2.DoubleValue):
                    L2 regularization coefficient.
                min_relative_progress (google.protobuf.wrappers_pb2.DoubleValue):
                    When early_stop is true, stops training when accuracy
                    improvement is less than 'min_relative_progress'. Used only
                    for iterative training algorithms.
                warm_start (google.protobuf.wrappers_pb2.BoolValue):
                    Whether to train a model from the last
                    checkpoint.
                early_stop (google.protobuf.wrappers_pb2.BoolValue):
                    Whether to stop early when the loss doesn't improve
                    significantly any more (compared to min_relative_progress).
                    Used only for iterative training algorithms.
                input_label_columns (MutableSequence[str]):
                    Name of input label columns in training data.
                data_split_method (google.cloud.bigquery_v2.types.Model.DataSplitMethod):
                    The data split type for training and
                    evaluation, e.g. RANDOM.
                data_split_eval_fraction (float):
                    The fraction of evaluation data over the
                    whole input data. The rest of data will be used
                    as training data. The format should be double.
                    Accurate to two decimal places.
                    Default value is 0.2.
                data_split_column (str):
                    The column to split data with. This column won't be used as
                    a feature.

                    1. When data_split_method is CUSTOM, the corresponding
                       column should be boolean. The rows with true value tag
                       are eval data, and the false are training data.
                    2. When data_split_method is SEQ, the first
                       DATA_SPLIT_EVAL_FRACTION rows (from smallest to largest)
                       in the corresponding column are used as training data,
                       and the rest are eval data. It respects the order in
                       Orderable data types:
                       https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_properties
                learn_rate_strategy (google.cloud.bigquery_v2.types.Model.LearnRateStrategy):
                    The strategy to determine learn rate for the
                    current iteration.
                initial_learn_rate (float):
                    Specifies the initial learning rate for the
                    line search learn rate strategy.
                label_class_weights (MutableMapping[str, float]):
                    Weights associated with each label class, for
                    rebalancing the training data. Only applicable
                    for classification models.
                user_column (str):
                    User column specified for matrix
                    factorization models.
                item_column (str):
                    Item column specified for matrix
                    factorization models.
                distance_type (google.cloud.bigquery_v2.types.Model.DistanceType):
                    Distance type for clustering models.
                num_clusters (int):
                    Number of clusters for clustering models.
                model_uri (str):
                    Google Cloud Storage URI from which the model
                    was imported. Only applicable for imported
                    models.
                optimization_strategy (google.cloud.bigquery_v2.types.Model.OptimizationStrategy):
                    Optimization strategy for training linear
                    regression models.
                hidden_units (MutableSequence[int]):
                    Hidden units for dnn models.
                batch_size (int):
                    Batch size for dnn models.
                dropout (google.protobuf.wrappers_pb2.DoubleValue):
                    Dropout probability for dnn models.
                max_tree_depth (int):
                    Maximum depth of a tree for boosted tree
                    models.
                subsample (float):
                    Subsample fraction of the training data to
                    grow tree to prevent overfitting for boosted
                    tree models.
                min_split_loss (google.protobuf.wrappers_pb2.DoubleValue):
                    Minimum split loss for boosted tree models.
                booster_type (google.cloud.bigquery_v2.types.Model.BoostedTreeOptionEnums.BoosterType):
                    Booster type for boosted tree models.
                num_parallel_tree (google.protobuf.wrappers_pb2.Int64Value):
                    Number of parallel trees constructed during
                    each iteration for boosted tree models.
                dart_normalize_type (google.cloud.bigquery_v2.types.Model.BoostedTreeOptionEnums.DartNormalizeType):
                    Type of normalization algorithm for boosted
                    tree models using dart booster.
                tree_method (google.cloud.bigquery_v2.types.Model.BoostedTreeOptionEnums.TreeMethod):
                    Tree construction algorithm for boosted tree
                    models.
                min_tree_child_weight (google.protobuf.wrappers_pb2.Int64Value):
                    Minimum sum of instance weight needed in a
                    child for boosted tree models.
                colsample_bytree (google.protobuf.wrappers_pb2.DoubleValue):
                    Subsample ratio of columns when constructing
                    each tree for boosted tree models.
                colsample_bylevel (google.protobuf.wrappers_pb2.DoubleValue):
                    Subsample ratio of columns for each level for
                    boosted tree models.
                colsample_bynode (google.protobuf.wrappers_pb2.DoubleValue):
                    Subsample ratio of columns for each
                    node(split) for boosted tree models.
                num_factors (int):
                    Num factors specified for matrix
                    factorization models.
                feedback_type (google.cloud.bigquery_v2.types.Model.FeedbackType):
                    Feedback type that specifies which algorithm
                    to run for matrix factorization.
                wals_alpha (google.protobuf.wrappers_pb2.DoubleValue):
                    Hyperparameter for matrix factoration when
                    implicit feedback type is specified.
                kmeans_initialization_method (google.cloud.bigquery_v2.types.Model.KmeansEnums.KmeansInitializationMethod):
                    The method used to initialize the centroids
                    for kmeans algorithm.
                kmeans_initialization_column (str):
                    The column used to provide the initial centroids for kmeans
                    algorithm when kmeans_initialization_method is CUSTOM.
                time_series_timestamp_column (str):
                    Column to be designated as time series
                    timestamp for ARIMA model.
                time_series_data_column (str):
                    Column to be designated as time series data
                    for ARIMA model.
                auto_arima (google.protobuf.wrappers_pb2.BoolValue):
                    Whether to enable auto ARIMA or not.
                non_seasonal_order (google.cloud.bigquery_v2.types.Model.ArimaOrder):
                    A specification of the non-seasonal part of
                    the ARIMA model: the three components (p, d, q)
                    are the AR order, the degree of differencing,
                    and the MA order.
                data_frequency (google.cloud.bigquery_v2.types.Model.DataFrequency):
                    The data frequency of a time series.
                calculate_p_values (google.protobuf.wrappers_pb2.BoolValue):
                    Whether or not p-value test should be
                    computed for this model. Only available for
                    linear and logistic regression models.
                include_drift (google.protobuf.wrappers_pb2.BoolValue):
                    Include drift when fitting an ARIMA model.
                holiday_region (google.cloud.bigquery_v2.types.Model.HolidayRegion):
                    The geographical region based on which the
                    holidays are considered in time series modeling.
                    If a valid value is specified, then holiday
                    effects modeling is enabled.
                holiday_regions (MutableSequence[google.cloud.bigquery_v2.types.Model.HolidayRegion]):
                    A list of geographical regions that are used
                    for time series modeling.
                time_series_id_column (str):
                    The time series id column that was used
                    during ARIMA model training.
                time_series_id_columns (MutableSequence[str]):
                    The time series id columns that were used
                    during ARIMA model training.
                forecast_limit_lower_bound (float):
                    The forecast limit lower bound that was used
                    during ARIMA model training with limits. To see
                    more details of the algorithm:

                    https://otexts.com/fpp2/limits.html
                forecast_limit_upper_bound (float):
                    The forecast limit upper bound that was used
                    during ARIMA model training with limits.
                horizon (int):
                    The number of periods ahead that need to be
                    forecasted.
                auto_arima_max_order (int):
                    The max value of the sum of non-seasonal p
                    and q.
                auto_arima_min_order (int):
                    The min value of the sum of non-seasonal p
                    and q.
                num_trials (int):
                    Number of trials to run this hyperparameter
                    tuning job.
                max_parallel_trials (int):
                    Maximum number of trials to run in parallel.
                hparam_tuning_objectives (MutableSequence[google.cloud.bigquery_v2.types.Model.HparamTuningEnums.HparamTuningObjective]):
                    The target evaluation metrics to optimize the
                    hyperparameters for.
                decompose_time_series (google.protobuf.wrappers_pb2.BoolValue):
                    If true, perform decompose time series and
                    save the results.
                clean_spikes_and_dips (google.protobuf.wrappers_pb2.BoolValue):
                    If true, clean spikes and dips in the input
                    time series.
                adjust_step_changes (google.protobuf.wrappers_pb2.BoolValue):
                    If true, detect step changes and make data
                    adjustment in the input time series.
                enable_global_explain (google.protobuf.wrappers_pb2.BoolValue):
                    If true, enable global explanation during
                    training.
                sampled_shapley_num_paths (int):
                    Number of paths for the sampled Shapley
                    explain method.
                integrated_gradients_num_steps (int):
                    Number of integral steps for the integrated
                    gradients explain method.
                category_encoding_method (google.cloud.bigquery_v2.types.Model.CategoryEncodingMethod.EncodingMethod):
                    Categorical feature encoding method.
                tf_version (str):
                    Based on the selected TF version, the
                    corresponding docker image is used to train
                    external models.
                color_space (google.cloud.bigquery_v2.types.Model.ColorSpace):
                    Enums for color space, used for processing
                    images in Object Table. See more details at
                    https://www.tensorflow.org/io/tutorials/colorspace.
                instance_weight_column (str):
                    Name of the instance weight column for
                    training data. This column isn't be used as a
                    feature.
                trend_smoothing_window_size (int):
                    Smoothing window size for the trend
                    component. When a positive value is specified, a
                    center moving average smoothing is applied on
                    the history trend. When the smoothing window is
                    out of the boundary at the beginning or the end
                    of the trend, the first element or the last
                    element is padded to fill the smoothing window
                    before the average is applied.
                time_series_length_fraction (float):
                    The fraction of the interpolated length of the time series
                    that's used to model the time series trend component. All of
                    the time points of the time series are used to model the
                    non-trend component. This training option accelerates
                    modeling training without sacrificing much forecasting
                    accuracy. You can use this option with
                    ``minTimeSeriesLength`` but not with
                    ``maxTimeSeriesLength``.
                min_time_series_length (int):
                    The minimum number of time points in a time series that are
                    used in modeling the trend component of the time series. If
                    you use this option you must also set the
                    ``timeSeriesLengthFraction`` option. This training option
                    ensures that enough time points are available when you use
                    ``timeSeriesLengthFraction`` in trend modeling. This is
                    particularly important when forecasting multiple time series
                    in a single query using ``timeSeriesIdColumn``. If the total
                    number of time points is less than the
                    ``minTimeSeriesLength`` value, then the query uses all
                    available time points.
                max_time_series_length (int):
                    The maximum number of time points in a time series that can
                    be used in modeling the trend component of the time series.
                    Don't use this option with the ``timeSeriesLengthFraction``
                    or ``minTimeSeriesLength`` options.
                xgboost_version (str):
                    User-selected XGBoost versions for training
                    of XGBoost models.
                approx_global_feature_contrib (google.protobuf.wrappers_pb2.BoolValue):
                    Whether to use approximate feature
                    contribution method in XGBoost model explanation
                    for global explain.
                fit_intercept (google.protobuf.wrappers_pb2.BoolValue):
                    Whether the model should include intercept
                    during model training.
                num_principal_components (int):
                    Number of principal components to keep in the
                    PCA model. Must be <= the number of features.
                pca_explained_variance_ratio (float):
                    The minimum ratio of cumulative explained
                    variance that needs to be given by the PCA
                    model.
                scale_features (google.protobuf.wrappers_pb2.BoolValue):
                    If true, scale the feature values by dividing
                    the feature standard deviation. Currently only
                    apply to PCA.
                pca_solver (google.cloud.bigquery_v2.types.Model.PcaSolverOptionEnums.PcaSolver):
                    The solver for PCA.
                auto_class_weights (google.protobuf.wrappers_pb2.BoolValue):
                    Whether to calculate class weights
                    automatically based on the popularity of each
                    label.
                activation_fn (str):
                    Activation function of the neural nets.
                optimizer (str):
                    Optimizer used for training the neural nets.
                budget_hours (float):
                    Budget in hours for AutoML training.
                standardize_features (google.protobuf.wrappers_pb2.BoolValue):
                    Whether to standardize numerical features.
                    Default to true.
                l1_reg_activation (float):
                    L1 regularization coefficient to activations.
                model_registry (google.cloud.bigquery_v2.types.Model.ModelRegistryOptionEnums.ModelRegistry):
                    The model registry.
                vertex_ai_model_version_aliases (MutableSequence[str]):
                    The version aliases to apply in Vertex AI
                    model registry. Always overwrite if the version
                    aliases exists in a existing model.
                dimension_id_columns (MutableSequence[str]):
                    Optional. Names of the columns to slice on.
                    Applies to contribution analysis models.
                contribution_metric (str):
                    The contribution metric. Applies to contribution analysis
                    models. Allowed formats supported are for summable and
                    summable ratio contribution metrics. These include
                    expressions such as ``SUM(x)`` or ``SUM(x)/SUM(y)``, where x
                    and y are column names from the base table.

                    This field is a member of `oneof`_ ``_contribution_metric``.
                is_test_column (str):
                    Name of the column used to determine the rows
                    corresponding to control and test. Applies to
                    contribution analysis models.

                    This field is a member of `oneof`_ ``_is_test_column``.
                min_apriori_support (float):
                    The apriori support minimum. Applies to
                    contribution analysis models.

                    This field is a member of `oneof`_ ``_min_apriori_support``.
            """

            max_iterations: int = proto.Field(
                proto.INT64,
                number=1,
            )
            loss_type: "Model.LossType" = proto.Field(
                proto.ENUM,
                number=2,
                enum="Model.LossType",
            )
            learn_rate: float = proto.Field(
                proto.DOUBLE,
                number=3,
            )
            l1_regularization: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=4,
                message=wrappers_pb2.DoubleValue,
            )
            l2_regularization: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=5,
                message=wrappers_pb2.DoubleValue,
            )
            min_relative_progress: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=6,
                message=wrappers_pb2.DoubleValue,
            )
            warm_start: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=7,
                message=wrappers_pb2.BoolValue,
            )
            early_stop: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=8,
                message=wrappers_pb2.BoolValue,
            )
            input_label_columns: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=9,
            )
            data_split_method: "Model.DataSplitMethod" = proto.Field(
                proto.ENUM,
                number=10,
                enum="Model.DataSplitMethod",
            )
            data_split_eval_fraction: float = proto.Field(
                proto.DOUBLE,
                number=11,
            )
            data_split_column: str = proto.Field(
                proto.STRING,
                number=12,
            )
            learn_rate_strategy: "Model.LearnRateStrategy" = proto.Field(
                proto.ENUM,
                number=13,
                enum="Model.LearnRateStrategy",
            )
            initial_learn_rate: float = proto.Field(
                proto.DOUBLE,
                number=16,
            )
            label_class_weights: MutableMapping[str, float] = proto.MapField(
                proto.STRING,
                proto.DOUBLE,
                number=17,
            )
            user_column: str = proto.Field(
                proto.STRING,
                number=18,
            )
            item_column: str = proto.Field(
                proto.STRING,
                number=19,
            )
            distance_type: "Model.DistanceType" = proto.Field(
                proto.ENUM,
                number=20,
                enum="Model.DistanceType",
            )
            num_clusters: int = proto.Field(
                proto.INT64,
                number=21,
            )
            model_uri: str = proto.Field(
                proto.STRING,
                number=22,
            )
            optimization_strategy: "Model.OptimizationStrategy" = proto.Field(
                proto.ENUM,
                number=23,
                enum="Model.OptimizationStrategy",
            )
            hidden_units: MutableSequence[int] = proto.RepeatedField(
                proto.INT64,
                number=24,
            )
            batch_size: int = proto.Field(
                proto.INT64,
                number=25,
            )
            dropout: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=26,
                message=wrappers_pb2.DoubleValue,
            )
            max_tree_depth: int = proto.Field(
                proto.INT64,
                number=27,
            )
            subsample: float = proto.Field(
                proto.DOUBLE,
                number=28,
            )
            min_split_loss: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=29,
                message=wrappers_pb2.DoubleValue,
            )
            booster_type: "Model.BoostedTreeOptionEnums.BoosterType" = proto.Field(
                proto.ENUM,
                number=60,
                enum="Model.BoostedTreeOptionEnums.BoosterType",
            )
            num_parallel_tree: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=61,
                message=wrappers_pb2.Int64Value,
            )
            dart_normalize_type: "Model.BoostedTreeOptionEnums.DartNormalizeType" = (
                proto.Field(
                    proto.ENUM,
                    number=62,
                    enum="Model.BoostedTreeOptionEnums.DartNormalizeType",
                )
            )
            tree_method: "Model.BoostedTreeOptionEnums.TreeMethod" = proto.Field(
                proto.ENUM,
                number=63,
                enum="Model.BoostedTreeOptionEnums.TreeMethod",
            )
            min_tree_child_weight: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=64,
                message=wrappers_pb2.Int64Value,
            )
            colsample_bytree: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=65,
                message=wrappers_pb2.DoubleValue,
            )
            colsample_bylevel: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=66,
                message=wrappers_pb2.DoubleValue,
            )
            colsample_bynode: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=67,
                message=wrappers_pb2.DoubleValue,
            )
            num_factors: int = proto.Field(
                proto.INT64,
                number=30,
            )
            feedback_type: "Model.FeedbackType" = proto.Field(
                proto.ENUM,
                number=31,
                enum="Model.FeedbackType",
            )
            wals_alpha: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=32,
                message=wrappers_pb2.DoubleValue,
            )
            kmeans_initialization_method: "Model.KmeansEnums.KmeansInitializationMethod" = proto.Field(
                proto.ENUM,
                number=33,
                enum="Model.KmeansEnums.KmeansInitializationMethod",
            )
            kmeans_initialization_column: str = proto.Field(
                proto.STRING,
                number=34,
            )
            time_series_timestamp_column: str = proto.Field(
                proto.STRING,
                number=35,
            )
            time_series_data_column: str = proto.Field(
                proto.STRING,
                number=36,
            )
            auto_arima: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=37,
                message=wrappers_pb2.BoolValue,
            )
            non_seasonal_order: "Model.ArimaOrder" = proto.Field(
                proto.MESSAGE,
                number=38,
                message="Model.ArimaOrder",
            )
            data_frequency: "Model.DataFrequency" = proto.Field(
                proto.ENUM,
                number=39,
                enum="Model.DataFrequency",
            )
            calculate_p_values: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=40,
                message=wrappers_pb2.BoolValue,
            )
            include_drift: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=41,
                message=wrappers_pb2.BoolValue,
            )
            holiday_region: "Model.HolidayRegion" = proto.Field(
                proto.ENUM,
                number=42,
                enum="Model.HolidayRegion",
            )
            holiday_regions: MutableSequence[
                "Model.HolidayRegion"
            ] = proto.RepeatedField(
                proto.ENUM,
                number=71,
                enum="Model.HolidayRegion",
            )
            time_series_id_column: str = proto.Field(
                proto.STRING,
                number=43,
            )
            time_series_id_columns: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=51,
            )
            forecast_limit_lower_bound: float = proto.Field(
                proto.DOUBLE,
                number=99,
            )
            forecast_limit_upper_bound: float = proto.Field(
                proto.DOUBLE,
                number=100,
            )
            horizon: int = proto.Field(
                proto.INT64,
                number=44,
            )
            auto_arima_max_order: int = proto.Field(
                proto.INT64,
                number=46,
            )
            auto_arima_min_order: int = proto.Field(
                proto.INT64,
                number=83,
            )
            num_trials: int = proto.Field(
                proto.INT64,
                number=47,
            )
            max_parallel_trials: int = proto.Field(
                proto.INT64,
                number=48,
            )
            hparam_tuning_objectives: MutableSequence[
                "Model.HparamTuningEnums.HparamTuningObjective"
            ] = proto.RepeatedField(
                proto.ENUM,
                number=54,
                enum="Model.HparamTuningEnums.HparamTuningObjective",
            )
            decompose_time_series: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=50,
                message=wrappers_pb2.BoolValue,
            )
            clean_spikes_and_dips: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=52,
                message=wrappers_pb2.BoolValue,
            )
            adjust_step_changes: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=53,
                message=wrappers_pb2.BoolValue,
            )
            enable_global_explain: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=55,
                message=wrappers_pb2.BoolValue,
            )
            sampled_shapley_num_paths: int = proto.Field(
                proto.INT64,
                number=56,
            )
            integrated_gradients_num_steps: int = proto.Field(
                proto.INT64,
                number=57,
            )
            category_encoding_method: "Model.CategoryEncodingMethod.EncodingMethod" = (
                proto.Field(
                    proto.ENUM,
                    number=58,
                    enum="Model.CategoryEncodingMethod.EncodingMethod",
                )
            )
            tf_version: str = proto.Field(
                proto.STRING,
                number=70,
            )
            color_space: "Model.ColorSpace" = proto.Field(
                proto.ENUM,
                number=72,
                enum="Model.ColorSpace",
            )
            instance_weight_column: str = proto.Field(
                proto.STRING,
                number=73,
            )
            trend_smoothing_window_size: int = proto.Field(
                proto.INT64,
                number=74,
            )
            time_series_length_fraction: float = proto.Field(
                proto.DOUBLE,
                number=75,
            )
            min_time_series_length: int = proto.Field(
                proto.INT64,
                number=76,
            )
            max_time_series_length: int = proto.Field(
                proto.INT64,
                number=77,
            )
            xgboost_version: str = proto.Field(
                proto.STRING,
                number=78,
            )
            approx_global_feature_contrib: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=84,
                message=wrappers_pb2.BoolValue,
            )
            fit_intercept: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=85,
                message=wrappers_pb2.BoolValue,
            )
            num_principal_components: int = proto.Field(
                proto.INT64,
                number=86,
            )
            pca_explained_variance_ratio: float = proto.Field(
                proto.DOUBLE,
                number=87,
            )
            scale_features: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=88,
                message=wrappers_pb2.BoolValue,
            )
            pca_solver: "Model.PcaSolverOptionEnums.PcaSolver" = proto.Field(
                proto.ENUM,
                number=89,
                enum="Model.PcaSolverOptionEnums.PcaSolver",
            )
            auto_class_weights: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=90,
                message=wrappers_pb2.BoolValue,
            )
            activation_fn: str = proto.Field(
                proto.STRING,
                number=91,
            )
            optimizer: str = proto.Field(
                proto.STRING,
                number=92,
            )
            budget_hours: float = proto.Field(
                proto.DOUBLE,
                number=93,
            )
            standardize_features: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=94,
                message=wrappers_pb2.BoolValue,
            )
            l1_reg_activation: float = proto.Field(
                proto.DOUBLE,
                number=95,
            )
            model_registry: "Model.ModelRegistryOptionEnums.ModelRegistry" = (
                proto.Field(
                    proto.ENUM,
                    number=96,
                    enum="Model.ModelRegistryOptionEnums.ModelRegistry",
                )
            )
            vertex_ai_model_version_aliases: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=97,
            )
            dimension_id_columns: MutableSequence[str] = proto.RepeatedField(
                proto.STRING,
                number=104,
            )
            contribution_metric: str = proto.Field(
                proto.STRING,
                number=105,
                optional=True,
            )
            is_test_column: str = proto.Field(
                proto.STRING,
                number=106,
                optional=True,
            )
            min_apriori_support: float = proto.Field(
                proto.DOUBLE,
                number=107,
                optional=True,
            )

        class IterationResult(proto.Message):
            r"""Information about a single iteration of the training run.

            Attributes:
                index (google.protobuf.wrappers_pb2.Int32Value):
                    Index of the iteration, 0 based.
                duration_ms (google.protobuf.wrappers_pb2.Int64Value):
                    Time taken to run the iteration in
                    milliseconds.
                training_loss (google.protobuf.wrappers_pb2.DoubleValue):
                    Loss computed on the training data at the end
                    of iteration.
                eval_loss (google.protobuf.wrappers_pb2.DoubleValue):
                    Loss computed on the eval data at the end of
                    iteration.
                learn_rate (float):
                    Learn rate used for this iteration.
                cluster_infos (MutableSequence[google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult.ClusterInfo]):
                    Information about top clusters for clustering
                    models.
                arima_result (google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult.ArimaResult):
                    Arima result.
                principal_component_infos (MutableSequence[google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult.PrincipalComponentInfo]):
                    The information of the principal components.
            """

            class ClusterInfo(proto.Message):
                r"""Information about a single cluster for clustering model.

                Attributes:
                    centroid_id (int):
                        Centroid id.
                    cluster_radius (google.protobuf.wrappers_pb2.DoubleValue):
                        Cluster radius, the average distance from
                        centroid to each point assigned to the cluster.
                    cluster_size (google.protobuf.wrappers_pb2.Int64Value):
                        Cluster size, the total number of points
                        assigned to the cluster.
                """

                centroid_id: int = proto.Field(
                    proto.INT64,
                    number=1,
                )
                cluster_radius: wrappers_pb2.DoubleValue = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    message=wrappers_pb2.DoubleValue,
                )
                cluster_size: wrappers_pb2.Int64Value = proto.Field(
                    proto.MESSAGE,
                    number=3,
                    message=wrappers_pb2.Int64Value,
                )

            class ArimaResult(proto.Message):
                r"""(Auto-)arima fitting result. Wrap everything in ArimaResult
                for easier refactoring if we want to use model-specific
                iteration results.

                Attributes:
                    arima_model_info (MutableSequence[google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult.ArimaResult.ArimaModelInfo]):
                        This message is repeated because there are
                        multiple arima models fitted in auto-arima. For
                        non-auto-arima model, its size is one.
                    seasonal_periods (MutableSequence[google.cloud.bigquery_v2.types.Model.SeasonalPeriod.SeasonalPeriodType]):
                        Seasonal periods. Repeated because multiple
                        periods are supported for one time series.
                """

                class ArimaCoefficients(proto.Message):
                    r"""Arima coefficients.

                    Attributes:
                        auto_regressive_coefficients (MutableSequence[float]):
                            Auto-regressive coefficients, an array of
                            double.
                        moving_average_coefficients (MutableSequence[float]):
                            Moving-average coefficients, an array of
                            double.
                        intercept_coefficient (google.protobuf.wrappers_pb2.DoubleValue):
                            Intercept coefficient, just a double not an
                            array.
                    """

                    auto_regressive_coefficients: MutableSequence[
                        float
                    ] = proto.RepeatedField(
                        proto.DOUBLE,
                        number=1,
                    )
                    moving_average_coefficients: MutableSequence[
                        float
                    ] = proto.RepeatedField(
                        proto.DOUBLE,
                        number=2,
                    )
                    intercept_coefficient: wrappers_pb2.DoubleValue = proto.Field(
                        proto.MESSAGE,
                        number=3,
                        message=wrappers_pb2.DoubleValue,
                    )

                class ArimaModelInfo(proto.Message):
                    r"""Arima model information.

                    Attributes:
                        non_seasonal_order (google.cloud.bigquery_v2.types.Model.ArimaOrder):
                            Non-seasonal order.
                        arima_coefficients (google.cloud.bigquery_v2.types.Model.TrainingRun.IterationResult.ArimaResult.ArimaCoefficients):
                            Arima coefficients.
                        arima_fitting_metrics (google.cloud.bigquery_v2.types.Model.ArimaFittingMetrics):
                            Arima fitting metrics.
                        has_drift (google.protobuf.wrappers_pb2.BoolValue):
                            Whether Arima model fitted with drift or not.
                            It is always false when d is not 1.
                        time_series_id (str):
                            The time_series_id value for this time series. It will be
                            one of the unique values from the time_series_id_column
                            specified during ARIMA model training. Only present when
                            time_series_id_column training option was used.
                        time_series_ids (MutableSequence[str]):
                            The tuple of time_series_ids identifying this time series.
                            It will be one of the unique tuples of values present in the
                            time_series_id_columns specified during ARIMA model
                            training. Only present when time_series_id_columns training
                            option was used and the order of values here are same as the
                            order of time_series_id_columns.
                        seasonal_periods (MutableSequence[google.cloud.bigquery_v2.types.Model.SeasonalPeriod.SeasonalPeriodType]):
                            Seasonal periods. Repeated because multiple
                            periods are supported for one time series.
                        has_holiday_effect (google.protobuf.wrappers_pb2.BoolValue):
                            If true, holiday_effect is a part of time series
                            decomposition result.
                        has_spikes_and_dips (google.protobuf.wrappers_pb2.BoolValue):
                            If true, spikes_and_dips is a part of time series
                            decomposition result.
                        has_step_changes (google.protobuf.wrappers_pb2.BoolValue):
                            If true, step_changes is a part of time series decomposition
                            result.
                    """

                    non_seasonal_order: "Model.ArimaOrder" = proto.Field(
                        proto.MESSAGE,
                        number=1,
                        message="Model.ArimaOrder",
                    )
                    arima_coefficients: "Model.TrainingRun.IterationResult.ArimaResult.ArimaCoefficients" = proto.Field(
                        proto.MESSAGE,
                        number=2,
                        message="Model.TrainingRun.IterationResult.ArimaResult.ArimaCoefficients",
                    )
                    arima_fitting_metrics: "Model.ArimaFittingMetrics" = proto.Field(
                        proto.MESSAGE,
                        number=3,
                        message="Model.ArimaFittingMetrics",
                    )
                    has_drift: wrappers_pb2.BoolValue = proto.Field(
                        proto.MESSAGE,
                        number=4,
                        message=wrappers_pb2.BoolValue,
                    )
                    time_series_id: str = proto.Field(
                        proto.STRING,
                        number=5,
                    )
                    time_series_ids: MutableSequence[str] = proto.RepeatedField(
                        proto.STRING,
                        number=10,
                    )
                    seasonal_periods: MutableSequence[
                        "Model.SeasonalPeriod.SeasonalPeriodType"
                    ] = proto.RepeatedField(
                        proto.ENUM,
                        number=6,
                        enum="Model.SeasonalPeriod.SeasonalPeriodType",
                    )
                    has_holiday_effect: wrappers_pb2.BoolValue = proto.Field(
                        proto.MESSAGE,
                        number=7,
                        message=wrappers_pb2.BoolValue,
                    )
                    has_spikes_and_dips: wrappers_pb2.BoolValue = proto.Field(
                        proto.MESSAGE,
                        number=8,
                        message=wrappers_pb2.BoolValue,
                    )
                    has_step_changes: wrappers_pb2.BoolValue = proto.Field(
                        proto.MESSAGE,
                        number=9,
                        message=wrappers_pb2.BoolValue,
                    )

                arima_model_info: MutableSequence[
                    "Model.TrainingRun.IterationResult.ArimaResult.ArimaModelInfo"
                ] = proto.RepeatedField(
                    proto.MESSAGE,
                    number=1,
                    message="Model.TrainingRun.IterationResult.ArimaResult.ArimaModelInfo",
                )
                seasonal_periods: MutableSequence[
                    "Model.SeasonalPeriod.SeasonalPeriodType"
                ] = proto.RepeatedField(
                    proto.ENUM,
                    number=2,
                    enum="Model.SeasonalPeriod.SeasonalPeriodType",
                )

            class PrincipalComponentInfo(proto.Message):
                r"""Principal component infos, used only for eigen decomposition based
                models, e.g., PCA. Ordered by explained_variance in the descending
                order.

                Attributes:
                    principal_component_id (google.protobuf.wrappers_pb2.Int64Value):
                        Id of the principal component.
                    explained_variance (google.protobuf.wrappers_pb2.DoubleValue):
                        Explained variance by this principal
                        component, which is simply the eigenvalue.
                    explained_variance_ratio (google.protobuf.wrappers_pb2.DoubleValue):
                        Explained_variance over the total explained variance.
                    cumulative_explained_variance_ratio (google.protobuf.wrappers_pb2.DoubleValue):
                        The explained_variance is pre-ordered in the descending
                        order to compute the cumulative explained variance ratio.
                """

                principal_component_id: wrappers_pb2.Int64Value = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    message=wrappers_pb2.Int64Value,
                )
                explained_variance: wrappers_pb2.DoubleValue = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    message=wrappers_pb2.DoubleValue,
                )
                explained_variance_ratio: wrappers_pb2.DoubleValue = proto.Field(
                    proto.MESSAGE,
                    number=3,
                    message=wrappers_pb2.DoubleValue,
                )
                cumulative_explained_variance_ratio: wrappers_pb2.DoubleValue = (
                    proto.Field(
                        proto.MESSAGE,
                        number=4,
                        message=wrappers_pb2.DoubleValue,
                    )
                )

            index: wrappers_pb2.Int32Value = proto.Field(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.Int32Value,
            )
            duration_ms: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=4,
                message=wrappers_pb2.Int64Value,
            )
            training_loss: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=5,
                message=wrappers_pb2.DoubleValue,
            )
            eval_loss: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=6,
                message=wrappers_pb2.DoubleValue,
            )
            learn_rate: float = proto.Field(
                proto.DOUBLE,
                number=7,
            )
            cluster_infos: MutableSequence[
                "Model.TrainingRun.IterationResult.ClusterInfo"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=8,
                message="Model.TrainingRun.IterationResult.ClusterInfo",
            )
            arima_result: "Model.TrainingRun.IterationResult.ArimaResult" = proto.Field(
                proto.MESSAGE,
                number=9,
                message="Model.TrainingRun.IterationResult.ArimaResult",
            )
            principal_component_infos: MutableSequence[
                "Model.TrainingRun.IterationResult.PrincipalComponentInfo"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=10,
                message="Model.TrainingRun.IterationResult.PrincipalComponentInfo",
            )

        training_options: "Model.TrainingRun.TrainingOptions" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Model.TrainingRun.TrainingOptions",
        )
        start_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=8,
            message=timestamp_pb2.Timestamp,
        )
        results: MutableSequence[
            "Model.TrainingRun.IterationResult"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=6,
            message="Model.TrainingRun.IterationResult",
        )
        evaluation_metrics: "Model.EvaluationMetrics" = proto.Field(
            proto.MESSAGE,
            number=7,
            message="Model.EvaluationMetrics",
        )
        data_split_result: "Model.DataSplitResult" = proto.Field(
            proto.MESSAGE,
            number=9,
            message="Model.DataSplitResult",
        )
        model_level_global_explanation: "Model.GlobalExplanation" = proto.Field(
            proto.MESSAGE,
            number=11,
            message="Model.GlobalExplanation",
        )
        class_level_global_explanations: MutableSequence[
            "Model.GlobalExplanation"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=12,
            message="Model.GlobalExplanation",
        )
        vertex_ai_model_id: str = proto.Field(
            proto.STRING,
            number=14,
        )
        vertex_ai_model_version: str = proto.Field(
            proto.STRING,
            number=15,
        )

    class DoubleHparamSearchSpace(proto.Message):
        r"""Search space for a double hyperparameter.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            range_ (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace.DoubleRange):
                Range of the double hyperparameter.

                This field is a member of `oneof`_ ``search_space``.
            candidates (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace.DoubleCandidates):
                Candidates of the double hyperparameter.

                This field is a member of `oneof`_ ``search_space``.
        """

        class DoubleRange(proto.Message):
            r"""Range of a double hyperparameter.

            Attributes:
                min_ (google.protobuf.wrappers_pb2.DoubleValue):
                    Min value of the double parameter.
                max_ (google.protobuf.wrappers_pb2.DoubleValue):
                    Max value of the double parameter.
            """

            min_: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.DoubleValue,
            )
            max_: wrappers_pb2.DoubleValue = proto.Field(
                proto.MESSAGE,
                number=2,
                message=wrappers_pb2.DoubleValue,
            )

        class DoubleCandidates(proto.Message):
            r"""Discrete candidates of a double hyperparameter.

            Attributes:
                candidates (MutableSequence[google.protobuf.wrappers_pb2.DoubleValue]):
                    Candidates for the double parameter in
                    increasing order.
            """

            candidates: MutableSequence[wrappers_pb2.DoubleValue] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.DoubleValue,
            )

        range_: "Model.DoubleHparamSearchSpace.DoubleRange" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="search_space",
            message="Model.DoubleHparamSearchSpace.DoubleRange",
        )
        candidates: "Model.DoubleHparamSearchSpace.DoubleCandidates" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="search_space",
            message="Model.DoubleHparamSearchSpace.DoubleCandidates",
        )

    class IntHparamSearchSpace(proto.Message):
        r"""Search space for an int hyperparameter.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            range_ (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace.IntRange):
                Range of the int hyperparameter.

                This field is a member of `oneof`_ ``search_space``.
            candidates (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace.IntCandidates):
                Candidates of the int hyperparameter.

                This field is a member of `oneof`_ ``search_space``.
        """

        class IntRange(proto.Message):
            r"""Range of an int hyperparameter.

            Attributes:
                min_ (google.protobuf.wrappers_pb2.Int64Value):
                    Min value of the int parameter.
                max_ (google.protobuf.wrappers_pb2.Int64Value):
                    Max value of the int parameter.
            """

            min_: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.Int64Value,
            )
            max_: wrappers_pb2.Int64Value = proto.Field(
                proto.MESSAGE,
                number=2,
                message=wrappers_pb2.Int64Value,
            )

        class IntCandidates(proto.Message):
            r"""Discrete candidates of an int hyperparameter.

            Attributes:
                candidates (MutableSequence[google.protobuf.wrappers_pb2.Int64Value]):
                    Candidates for the int parameter in
                    increasing order.
            """

            candidates: MutableSequence[wrappers_pb2.Int64Value] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.Int64Value,
            )

        range_: "Model.IntHparamSearchSpace.IntRange" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="search_space",
            message="Model.IntHparamSearchSpace.IntRange",
        )
        candidates: "Model.IntHparamSearchSpace.IntCandidates" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="search_space",
            message="Model.IntHparamSearchSpace.IntCandidates",
        )

    class StringHparamSearchSpace(proto.Message):
        r"""Search space for string and enum.

        Attributes:
            candidates (MutableSequence[str]):
                Canididates for the string or enum parameter
                in lower case.
        """

        candidates: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class IntArrayHparamSearchSpace(proto.Message):
        r"""Search space for int array.

        Attributes:
            candidates (MutableSequence[google.cloud.bigquery_v2.types.Model.IntArrayHparamSearchSpace.IntArray]):
                Candidates for the int array parameter.
        """

        class IntArray(proto.Message):
            r"""An array of int.

            Attributes:
                elements (MutableSequence[int]):
                    Elements in the int array.
            """

            elements: MutableSequence[int] = proto.RepeatedField(
                proto.INT64,
                number=1,
            )

        candidates: MutableSequence[
            "Model.IntArrayHparamSearchSpace.IntArray"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Model.IntArrayHparamSearchSpace.IntArray",
        )

    class HparamSearchSpaces(proto.Message):
        r"""Hyperparameter search spaces. These should be a subset of
        training_options.

        Attributes:
            learn_rate (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Learning rate of training jobs.
            l1_reg (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                L1 regularization coefficient.
            l2_reg (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                L2 regularization coefficient.
            num_clusters (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace):
                Number of clusters for k-means.
            num_factors (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace):
                Number of latent factors to train on.
            hidden_units (google.cloud.bigquery_v2.types.Model.IntArrayHparamSearchSpace):
                Hidden units for neural network models.
            batch_size (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace):
                Mini batch sample size.
            dropout (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Dropout probability for dnn model training
                and boosted tree models using dart booster.
            max_tree_depth (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace):
                Maximum depth of a tree for boosted tree
                models.
            subsample (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Subsample the training data to grow tree to
                prevent overfitting for boosted tree models.
            min_split_loss (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Minimum split loss for boosted tree models.
            wals_alpha (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Hyperparameter for matrix factoration when
                implicit feedback type is specified.
            booster_type (google.cloud.bigquery_v2.types.Model.StringHparamSearchSpace):
                Booster type for boosted tree models.
            num_parallel_tree (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace):
                Number of parallel trees for boosted tree
                models.
            dart_normalize_type (google.cloud.bigquery_v2.types.Model.StringHparamSearchSpace):
                Dart normalization type for boosted tree
                models.
            tree_method (google.cloud.bigquery_v2.types.Model.StringHparamSearchSpace):
                Tree construction algorithm for boosted tree
                models.
            min_tree_child_weight (google.cloud.bigquery_v2.types.Model.IntHparamSearchSpace):
                Minimum sum of instance weight needed in a
                child for boosted tree models.
            colsample_bytree (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Subsample ratio of columns when constructing
                each tree for boosted tree models.
            colsample_bylevel (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Subsample ratio of columns for each level for
                boosted tree models.
            colsample_bynode (google.cloud.bigquery_v2.types.Model.DoubleHparamSearchSpace):
                Subsample ratio of columns for each
                node(split) for boosted tree models.
            activation_fn (google.cloud.bigquery_v2.types.Model.StringHparamSearchSpace):
                Activation functions of neural network
                models.
            optimizer (google.cloud.bigquery_v2.types.Model.StringHparamSearchSpace):
                Optimizer of TF models.
        """

        learn_rate: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Model.DoubleHparamSearchSpace",
        )
        l1_reg: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Model.DoubleHparamSearchSpace",
        )
        l2_reg: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=4,
            message="Model.DoubleHparamSearchSpace",
        )
        num_clusters: "Model.IntHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=26,
            message="Model.IntHparamSearchSpace",
        )
        num_factors: "Model.IntHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=31,
            message="Model.IntHparamSearchSpace",
        )
        hidden_units: "Model.IntArrayHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=34,
            message="Model.IntArrayHparamSearchSpace",
        )
        batch_size: "Model.IntHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=37,
            message="Model.IntHparamSearchSpace",
        )
        dropout: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=38,
            message="Model.DoubleHparamSearchSpace",
        )
        max_tree_depth: "Model.IntHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=41,
            message="Model.IntHparamSearchSpace",
        )
        subsample: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=42,
            message="Model.DoubleHparamSearchSpace",
        )
        min_split_loss: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=43,
            message="Model.DoubleHparamSearchSpace",
        )
        wals_alpha: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=49,
            message="Model.DoubleHparamSearchSpace",
        )
        booster_type: "Model.StringHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=56,
            message="Model.StringHparamSearchSpace",
        )
        num_parallel_tree: "Model.IntHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=57,
            message="Model.IntHparamSearchSpace",
        )
        dart_normalize_type: "Model.StringHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=58,
            message="Model.StringHparamSearchSpace",
        )
        tree_method: "Model.StringHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=59,
            message="Model.StringHparamSearchSpace",
        )
        min_tree_child_weight: "Model.IntHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=60,
            message="Model.IntHparamSearchSpace",
        )
        colsample_bytree: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=61,
            message="Model.DoubleHparamSearchSpace",
        )
        colsample_bylevel: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=62,
            message="Model.DoubleHparamSearchSpace",
        )
        colsample_bynode: "Model.DoubleHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=63,
            message="Model.DoubleHparamSearchSpace",
        )
        activation_fn: "Model.StringHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=67,
            message="Model.StringHparamSearchSpace",
        )
        optimizer: "Model.StringHparamSearchSpace" = proto.Field(
            proto.MESSAGE,
            number=68,
            message="Model.StringHparamSearchSpace",
        )

    class HparamTuningTrial(proto.Message):
        r"""Training info of a trial in `hyperparameter
        tuning <https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-hp-tuning-overview>`__
        models.

        Attributes:
            trial_id (int):
                1-based index of the trial.
            start_time_ms (int):
                Starting time of the trial.
            end_time_ms (int):
                Ending time of the trial.
            hparams (google.cloud.bigquery_v2.types.Model.TrainingRun.TrainingOptions):
                The hyperprameters selected for this trial.
            evaluation_metrics (google.cloud.bigquery_v2.types.Model.EvaluationMetrics):
                Evaluation metrics of this trial calculated
                on the test data. Empty in Job API.
            status (google.cloud.bigquery_v2.types.Model.HparamTuningTrial.TrialStatus):
                The status of the trial.
            error_message (str):
                Error message for FAILED and INFEASIBLE
                trial.
            training_loss (google.protobuf.wrappers_pb2.DoubleValue):
                Loss computed on the training data at the end
                of trial.
            eval_loss (google.protobuf.wrappers_pb2.DoubleValue):
                Loss computed on the eval data at the end of
                trial.
            hparam_tuning_evaluation_metrics (google.cloud.bigquery_v2.types.Model.EvaluationMetrics):
                Hyperparameter tuning evaluation metrics of this trial
                calculated on the eval data. Unlike evaluation_metrics, only
                the fields corresponding to the hparam_tuning_objectives are
                set.
        """

        class TrialStatus(proto.Enum):
            r"""Current status of the trial.

            Values:
                TRIAL_STATUS_UNSPECIFIED (0):
                    Default value.
                NOT_STARTED (1):
                    Scheduled but not started.
                RUNNING (2):
                    Running state.
                SUCCEEDED (3):
                    The trial succeeded.
                FAILED (4):
                    The trial failed.
                INFEASIBLE (5):
                    The trial is infeasible due to the invalid
                    params.
                STOPPED_EARLY (6):
                    Trial stopped early because it's not
                    promising.
            """
            TRIAL_STATUS_UNSPECIFIED = 0
            NOT_STARTED = 1
            RUNNING = 2
            SUCCEEDED = 3
            FAILED = 4
            INFEASIBLE = 5
            STOPPED_EARLY = 6

        trial_id: int = proto.Field(
            proto.INT64,
            number=1,
        )
        start_time_ms: int = proto.Field(
            proto.INT64,
            number=2,
        )
        end_time_ms: int = proto.Field(
            proto.INT64,
            number=3,
        )
        hparams: "Model.TrainingRun.TrainingOptions" = proto.Field(
            proto.MESSAGE,
            number=4,
            message="Model.TrainingRun.TrainingOptions",
        )
        evaluation_metrics: "Model.EvaluationMetrics" = proto.Field(
            proto.MESSAGE,
            number=5,
            message="Model.EvaluationMetrics",
        )
        status: "Model.HparamTuningTrial.TrialStatus" = proto.Field(
            proto.ENUM,
            number=6,
            enum="Model.HparamTuningTrial.TrialStatus",
        )
        error_message: str = proto.Field(
            proto.STRING,
            number=7,
        )
        training_loss: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=8,
            message=wrappers_pb2.DoubleValue,
        )
        eval_loss: wrappers_pb2.DoubleValue = proto.Field(
            proto.MESSAGE,
            number=9,
            message=wrappers_pb2.DoubleValue,
        )
        hparam_tuning_evaluation_metrics: "Model.EvaluationMetrics" = proto.Field(
            proto.MESSAGE,
            number=10,
            message="Model.EvaluationMetrics",
        )

    etag: str = proto.Field(
        proto.STRING,
        number=1,
    )
    model_reference: gcb_model_reference.ModelReference = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcb_model_reference.ModelReference,
    )
    creation_time: int = proto.Field(
        proto.INT64,
        number=5,
    )
    last_modified_time: int = proto.Field(
        proto.INT64,
        number=6,
    )
    description: str = proto.Field(
        proto.STRING,
        number=12,
    )
    friendly_name: str = proto.Field(
        proto.STRING,
        number=14,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=15,
    )
    expiration_time: int = proto.Field(
        proto.INT64,
        number=16,
    )
    location: str = proto.Field(
        proto.STRING,
        number=13,
    )
    encryption_configuration: encryption_config.EncryptionConfiguration = proto.Field(
        proto.MESSAGE,
        number=17,
        message=encryption_config.EncryptionConfiguration,
    )
    model_type: ModelType = proto.Field(
        proto.ENUM,
        number=7,
        enum=ModelType,
    )
    training_runs: MutableSequence[TrainingRun] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message=TrainingRun,
    )
    feature_columns: MutableSequence[
        standard_sql.StandardSqlField
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=standard_sql.StandardSqlField,
    )
    label_columns: MutableSequence[standard_sql.StandardSqlField] = proto.RepeatedField(
        proto.MESSAGE,
        number=11,
        message=standard_sql.StandardSqlField,
    )
    transform_columns: MutableSequence["TransformColumn"] = proto.RepeatedField(
        proto.MESSAGE,
        number=26,
        message="TransformColumn",
    )
    hparam_search_spaces: HparamSearchSpaces = proto.Field(
        proto.MESSAGE,
        number=18,
        message=HparamSearchSpaces,
    )
    default_trial_id: int = proto.Field(
        proto.INT64,
        number=21,
    )
    hparam_trials: MutableSequence[HparamTuningTrial] = proto.RepeatedField(
        proto.MESSAGE,
        number=20,
        message=HparamTuningTrial,
    )
    optimal_trial_ids: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=22,
    )
    remote_model_info: "RemoteModelInfo" = proto.Field(
        proto.MESSAGE,
        number=25,
        message="RemoteModelInfo",
    )


class GetModelRequest(proto.Message):
    r"""Request format for getting information about a BigQuery ML
    model.

    Attributes:
        project_id (str):
            Required. Project ID of the requested model.
        dataset_id (str):
            Required. Dataset ID of the requested model.
        model_id (str):
            Required. Model ID of the requested model.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class PatchModelRequest(proto.Message):
    r"""

    Attributes:
        project_id (str):
            Required. Project ID of the model to patch.
        dataset_id (str):
            Required. Dataset ID of the model to patch.
        model_id (str):
            Required. Model ID of the model to patch.
        model (google.cloud.bigquery_v2.types.Model):
            Required. Patched model.
            Follows RFC5789 patch semantics. Missing fields
            are not updated. To clear a field, explicitly
            set to default value.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    model: "Model" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Model",
    )


class DeleteModelRequest(proto.Message):
    r"""Request format for deleting BigQuery ML models.

    Attributes:
        project_id (str):
            Required. Project ID of the model to delete.
        dataset_id (str):
            Required. Dataset ID of the model to delete.
        model_id (str):
            Required. Model ID of the model to delete.
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    model_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListModelsRequest(proto.Message):
    r"""Request format for listing BigQuery ML models.

    Attributes:
        project_id (str):
            Required. Project ID of the models to list.
        dataset_id (str):
            Required. Dataset ID of the models to list.
        max_results (google.protobuf.wrappers_pb2.UInt32Value):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call to
            request the next page of results
    """

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    max_results: wrappers_pb2.UInt32Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.UInt32Value,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListModelsResponse(proto.Message):
    r"""Response format for a single page when listing BigQuery ML
    models.

    Attributes:
        models (MutableSequence[google.cloud.bigquery_v2.types.Model]):
            Models in the requested dataset. Only the following fields
            are populated: model_reference, model_type, creation_time,
            last_modified_time and labels.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    models: MutableSequence["Model"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Model",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
