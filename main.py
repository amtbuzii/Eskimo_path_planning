import main_GUI
import logging

logging.basicConfig(
    filename="../test.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


if __name__ == "__main__":
    main_GUI.main()
    # main_no_GUI.main()
