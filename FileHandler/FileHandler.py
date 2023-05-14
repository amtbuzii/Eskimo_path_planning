import matplotlib.pyplot as plt
from FieldManager.Field import Field
from Point.Point import Point
import constant
import logging


def create_file(field: Field) -> None:
    header = create_header_text(field)
    polygons = create_polygons_text(field.polygons)
    write_to_file(constant.FILE_PATH, header + polygons)


def create_header_text(field: Field) -> str:
    _ice_number = len(field.polygons)

    # create the header text
    header_text = (
        f"{field.size}\n{field.size}\n{field.start}\n{field.end}\n{_ice_number}"
    )

    return header_text


def create_polygons_text(polygons: list) -> str:
    polygons_text = ""

    for pol in range(len(polygons)):
        polygon_dots_number = len(polygons[pol])
        # add to polygons text
        points = "\n".join([str(point) for point in polygons[pol]])
        polygons_text += f"\n{pol + 1}\n{polygon_dots_number}\n{points}"

    return polygons_text


def write_to_file(file_name: str, lines: str = "") -> None:
    """
    write the data to file.
    """

    try:
        with open(file_name, "w") as file:
            file.writelines(lines)
    except FileNotFoundError:
        logging.info("Error: The file was not found.")
    except PermissionError:
        logging.info("Error: You don't have the required permissions to access the file.")
    except OSError as e:
        logging.info("Error: An operating system error occurred -", e)
    except ValueError:
        logging.info("Error: Invalid value or format.")
    except TypeError:
        logging.info("Error: Invalid data type.")
    except Exception as e:
        logging.info("Error: An unexpected error occurred -", e)
    else:
        logging.info("The data was successfully written to the file.")


def read_field(file_name: str) -> Field:
    """
    read txt file and returns - start, end, polygons
    """
    file = open(file_name, "r")
    size_x = float(file.readline())
    size_y = float(file.readline())
    start = Point(tuple(map(float, file.readline().split(" "))))
    end = Point(tuple(map(float, file.readline().split(" "))))
    ice_num = int(file.readline())
    polygons = [[] for _ in range(ice_num)]

    # read polygons
    for polygon in range(ice_num):
        iceberg_num = int(file.readline())
        ice_dots = int(file.readline())
        for dot in range(ice_dots):
            point = tuple(map(float, file.readline().split(" ")))
            polygons[polygon].append(Point(point[0], point[1]))

    file.close()
    logging.info("The data was successfully read from file.")

    return Field(size_x, start, end, polygons)


def show_field(field_data: Field, convex: bool) -> None:
    """
    Show field with start, end points and all polygons.
    """

    # figure title
    # plt.figure(1, figsize=(5, 5))
    # plt.suptitle("Eskimo field", fontsize=15)

    # plot START + END point
    plt.scatter(
        field_data.start.x,
        field_data.start.y,
        color="blue",
        marker="p",
        s=50,
        label="Start",
    )
    plt.scatter(
        field_data.end.x,
        field_data.end.y,
        color="red",
        marker="*",
        s=50,
        label="End",
    )

    # Plot polygons:
    for polygon in field_data.polygons:
        points_x = [pt.x for pt in polygon]
        points_y = [pt.y for pt in polygon]
        plt.scatter(points_x, points_y, s=8)

        if convex:
            points_x.append(points_x[0])
            points_y.append(points_y[0])
            plt.plot(points_x, points_y, linewidth=1)

    # plt.xlim(-5,field_data.size)
    # plt.ylim(-5,field_data.size)

    # grid configurations
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=5)
    plt.show()
