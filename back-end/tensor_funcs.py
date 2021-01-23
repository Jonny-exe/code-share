import pandas as pd
import tensorflow as tf
import numpy as np


def get_classifier():
    my_feature_columns = []
    NUMERIC_COLUMNS = ["message_length", "likes"]
    # CATEGORICAL_COLUMNS = []

    for feature_name in NUMERIC_COLUMNS:
        my_feature_columns.append(
            tf.feature_column.numeric_column(key=feature_name, dtype=tf.int8)
        )

    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        hidden_units=[30, 10],
        n_classes=2,
        model_dir="./classifier",
    )
    return classifier


def predict_message(predict):
    RESULTS = ["terrible", "bad", "good"]

    classifier = get_classifier()

    for key in predict.keys():
        predict[key] = [predict[key]]

    def input_fn(features):
        # Convert the inputs to a Dataset without labels.
        return tf.data.Dataset.from_tensor_slices(dict(features)).batch(256)

    predictions = classifier.predict(input_fn=lambda: input_fn(predict))

    for pred_dict in predictions:
        class_id = pred_dict["class_ids"][0]
        probability = pred_dict["probabilities"][class_id]
        print(
            'Prediction is "{}" \
            ({:.1f}%)'.format(RESULTS[class_id], 100 * probability)
        )
        print("Result: ", RESULTS[class_id])
        result = class_id.item()
        return result


def train_messages():
    file_path = "/home/a/Documents/GitHub/code-share/back-end/test1.csv"
    train = pd.read_csv(file_path)
    test = pd.read_csv(file_path)

    train_y = train.pop("group")
    test_y = test.pop("group")

    classifier = get_classifier()

    def input_fn(features, labels, training=True, batch_size=256):
        # Convert the inputs to a Dataset.
        dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

        # Shuffle and repeat if you are in training mode.
        if training:
            dataset = dataset.shuffle(1000).repeat()

        return dataset.batch(batch_size)

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
