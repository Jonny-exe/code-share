from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
import tensorflow as tf

def predict_message(predict):
    RESULTS = ["notDead", "dead"]

    classifier = train_messages()

    def input_fn(features, batch_size=256):
        # Convert the inputs to a Dataset without labels.
        return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

    predictions = classifier.predict(input_fn=lambda: input_fn(predict))

    for pred_dict in predictions:
        class_id = pred_dict["class_ids"][0]
        probability = pred_dict["probabilities"][class_id]
        print(
            'Prediction is "{}" ({:.1f}%)'.format(RESULTS[class_id], 100 * probability)
        )
        return RESULTS[class_id]


def train_messages():
    my_feature_columns = []

    train = pd.read_csv("test1.csv")
    test = pd.read_csv("test1.csv")
    print(train.head())

    train_y = train.pop("dead")
    test_y = test.pop("dead")
    print(train_y.head())

    NUMERIC_COLUMNS = ["status", "type"]
    CATEGORICAL_COLUMNS = ["color"]

    for feature_name in NUMERIC_COLUMNS:
        my_feature_columns.append(
            tf.feature_column.numeric_column(key=feature_name, dtype=tf.int8)
        )

    for feature_name in CATEGORICAL_COLUMNS:
        vocabulary = train[feature_name].unique()
        print("Vocabulary: ", vocabulary)
        categorical_column = tf.feature_column.categorical_column_with_vocabulary_list(
            key=feature_name,
            vocabulary_list=vocabulary,
            dtype=tf.string,
            default_value=-1,
            num_oov_buckets=0,
        )
        # These must be wrapped https://stackoverflow.com/questions/48614819/items-of-feature-columns-must-be-a-featurecolumn-given-vocabularylistcategori
        my_feature_columns.append(
            tf.feature_column.indicator_column(categorical_column)
        )


    def input_fn(features, labels, training=True, batch_size=256):
        # Convert the inputs to a Dataset.
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

        # Shuffle and repeat if you are in training mode.
        if training:
            dataset = dataset.shuffle(1000).repeat()

        return dataset.batch(batch_size)

    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        hidden_units=[30, 10],
        n_classes=2,
        model_dir='./classifier'
    )

    def evaluate():
        eval_result = classifier.evaluate(
            input_fn=lambda: input_fn(test, test_y, training=False)
        )
        print("\nTest set accuracy: {accuracy:0.3f}\n".format(**eval_result))

    classifier.train(
        input_fn=lambda: input_fn(train, train_y, training=True), steps=5000
    )

    evaluate()
    return classifier


predict_message({"status": [1], "type":[0], "color":["blue"]})