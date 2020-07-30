import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from client.ais_tar2tf import AisDataset, default_record_parser
from client.ais_tar2tf.ops import Select, Decode, Convert, Resize


def path_generator():
    i = 1
    while True:
        yield "train.record-{}".format(i)
        i += 1


EPOCHS = 10
BATCH_SIZE = 20

# ADJUST AisDataset PARAMETERS BELOW

BUCKET_NAME = "tar-bucket"
PROXY_URL = "http://localhost:8080"

# Create AisDataset.
# Values will be extracted from tar-records according to Resize(Convert(Decode("jpg"), tf.float32), (224, 224)) operation,
# meaning that bytes under "jpg" in tar-record will be decoded as an image, converted to tf.float32 type and then Resized to (224, 224)
# Labels will be extracted from tar-records according to Select("cls") operation, meaning that bytes under "cls" will be treated as label.
ais = AisDataset(BUCKET_NAME, PROXY_URL, [Decode("jpg"), Convert("jpg", tf.float32), Resize("jpg", (224, 224))], [Select("jpg"), Select("cls")])

# prepare your bucket, for example from `gsutil ls gs://lpr-gtc2020`
# save multiple TFRecord files with max size 2MB to paths generated by path_generator
train_records_files = ais.load("train-{0..3}.tar", path=path_generator, max_shard_size="2MB", num_workers=4)
# save TFRecord file to test.record path
ais.load("train-{4..7}.tar", path="test.record", num_workers=4)

train_dataset = tf.data.TFRecordDataset(filenames=train_records_files)
train_dataset = train_dataset.map(default_record_parser)
train_dataset = train_dataset.shuffle(buffer_size=1024).batch(BATCH_SIZE)

test_dataset = tf.data.TFRecordDataset(filenames=["test.record"])
test_dataset = test_dataset.map(default_record_parser).batch(BATCH_SIZE)

# TRAINING PART BELOW

inputs = keras.Input(shape=(224, 224, 3), name="images")
x = layers.Flatten()(inputs)
x = layers.Dense(64, activation="relu", name="dense_1")(x)
x = layers.Dense(64, activation="relu", name="dense_2")(x)
outputs = layers.Dense(10, name="predictions")(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer=keras.optimizers.Adam(1e-4), loss=keras.losses.mean_squared_error, metrics=["acc"])

model.summary()

model.fit(train_dataset, epochs=EPOCHS)
result = model.evaluate(test_dataset)
print(dict(zip(model.metrics_names, result)))
ais.stop()
