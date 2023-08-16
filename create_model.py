from keras import Sequential, Model, layers
from keras.optimizers import Adam

def create_model (input_shape: int) -> Model:
    model = Sequential()
    model.add(layers.Dense(units=256, activation="relu", input_shape=(input_shape,)))
    model.add(layers.Dropout(0.4))
    model.add(layers.Dense(units=128, activation="relu"))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(units=64, activation="relu"))
    model.add(layers.Dense(units=32, activation="relu"))
    model.add(layers.Dense(units=1, activation="relu"))

    model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mse"])

    return model