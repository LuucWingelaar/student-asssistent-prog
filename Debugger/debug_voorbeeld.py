# This is a faulty function that should convert Celcius to Fahrenheit, but uses the wrong formula
def faulty_fahrenheit(celcius):
    fahrenheit = celcius + 32 * 9 / 5 # This is the wrong formula!
    return fahrenheit

def test_faulty_fahrenheit():
    if faulty_fahrenheit(100) != 212:
        return False
    else:
        return True

if __name__ == '__main__':
    if not test_faulty_fahrenheit():
        print("Er ging iets mis!")
    else:
        print("Alles werkt!")

    