import sensor


def test_sensor_data_contains_temperature():
    data = sensor.generate_sensor_data()

    assert "temperature" in data


def test_sensor_data_contains_humidity():
    data = sensor.generate_sensor_data()

    assert "humidity" in data


def test_sensor_data_contains_light():
    data = sensor.generate_sensor_data()

    assert "light" in data


def test_sensor_data_values_are_valid():
    data = sensor.generate_sensor_data()

    assert 18 <= data["temperature"] <= 28
    assert 40 <= data["humidity"] <= 80
    assert 100 <= data["light"] <= 900
