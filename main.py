from FieldManager.FieldManager import FieldManager



if __name__ == '__main__':
    field = FieldManager(300, (10.0, 10.0), (250.0, 250.0), seed = 0)

    # present the all field
    field.show_field()



