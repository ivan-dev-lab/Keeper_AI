import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras import Sequential, Model, layers
from keras.optimizers import Adam

## \brief Функция для создания модели
## \authors ivan-dev-lab
## \version 1.0.0
## \date 16.08.2023
## \param[in] input_shape Размерность входных данных. Необходима для входного слоя модели
## \details Ниже представлен исходный код архитектуры модели
## \code
# model = Sequential()
# model.add(layers.Dense(units=256, activation="relu", input_shape=(input_shape,)))
# model.add(layers.Dropout(0.4))
# model.add(layers.Dense(units=128, activation="relu"))
# model.add(layers.Dropout(0.3))
# model.add(layers.Dense(units=64, activation="relu"))
# model.add(layers.Dense(units=32, activation="relu"))
# model.add(layers.Dense(units=1, activation="relu"))
## \endcode
## \details Модель скомпилирована с использованием таких функций, как:
## <ol>
## <li>Функция-оптимизатор: <b>Adam</b> с фактором обучения: <b>0.001</b></li>
## <li>Функция потерь: <b>RMSprop</b> с фактором обучения: <b>0.01</b></li>
## <li>Метрики: <b>[ MeanSquaredError() ]</b></li>
## </ol>
## \details Ниже представлен исходный код компиляции модели
## \code
# model.compile(optimizer=RMSprop(learning_rate= 0.01), loss="mse", metrics=[MeanSquaredError()])
## \endcode
## \return keras.Model - скомпилированная, но не обученная модель
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