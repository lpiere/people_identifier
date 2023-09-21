from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def train_network():
    classificador = Sequential()
    classificador.add(
        Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    classificador.add(BatchNormalization())
    classificador.add(MaxPooling2D(pool_size=(2, 2)))

    classificador.add(
        Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    classificador.add(BatchNormalization())
    classificador.add(MaxPooling2D(pool_size=(2, 2)))

    classificador.add(Flatten())

    classificador.add(Dense(units=128, activation='relu'))
    classificador.add(Dropout(0.2))
    classificador.add(Dense(units=128, activation='relu'))
    classificador.add(Dropout(0.2))

    classificador.add(Dense(units=3, activation='softmax'))

    # classificador.load_weights('try_to_know_who_is/people_reconizer.h5')

    classificador.compile(optimizer='adam', loss='categorical_crossentropy',
                        metrics=['accuracy'])


    gerador_treinamento = ImageDataGenerator(rescale=1./255,
                                            rotation_range=7,
                                            horizontal_flip=True,
                                            shear_range=0.2,
                                            height_shift_range=0.07,
                                            zoom_range=0.2)


    base_treinamento = gerador_treinamento.flow_from_directory('try_to_know_who_is/data',
                                                            target_size=(
                                                                64, 64),
                                                            batch_size=32,
                                                            class_mode='categorical')

    classificador.fit(base_treinamento, steps_per_epoch=6432 / 32,
                    epochs=10)


    classifier_json = classificador.to_json()
    with open('try_to_know_who_is/people_reconizer.json', 'w') as json_file:
        json_file.write(classifier_json)
    classificador.save_weights('try_to_know_who_is/people_reconizer.h5')
