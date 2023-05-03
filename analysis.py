import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_path = "../Eskimo_path_planning/anaysis_data.txt"
p = np.loadtxt(file_path)

"""
mean_naive = np.mean(p[:,0])*np.ones(len(p))
mean_opt = np.mean(p[:,1])*np.ones(len(p))
mean_rnd = np.mean(p[:,2])*np.ones(len(p))

plt.title("Path calculation analysis")
plt.plot(mean_naive,label = "Naive" ,color = "blue")
plt.plot(mean_opt,label = "Optimal" , color = "orange")
plt.plot(mean_rnd,label = "Random" ,color = "green")

plt.plot(p[:,0], alpha=0.3, color = "blue")
plt.plot(p[:,1],alpha=0.3, color = "orange")
plt.plot(p[:,2],alpha=0.3, color = "green")
plt.ylabel("Score")
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3)
plt.show()

"""

polygons_number = [int(i) for i in np.linspace(10, 100, 10)]

plt.title("Run-time analysis")
plt.plot(polygons_number, p[:,0],label = "Naive" )
plt.plot(polygons_number, p[:,1],label = "Optimal" )
plt.plot(polygons_number, p[:,2],label = "Random" )
plt.xlabel("Number of polygons")
plt.ylabel("Run-time [s]")
plt.legend(loc="best", ncol=1)
plt.show()


plt.title("Run-time analysis")
plt.plot(polygons_number, p[:,1],label = "Optimal" )
plt.plot(polygons_number, p[:,2],label = "Random" )
plt.xlabel("Number of polygons")
plt.ylabel("Run-time [s]")
plt.legend(loc="best", ncol=1)
plt.show()



"""
N = 5


ind = np.arange(N)  # the x locations for the groups
width = 0.135       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(ind, p[:,0], width, color='royalblue')

rects2 = ax.bar(ind+width, p[:,1], width, color='seagreen')

rects3 = ax.bar(ind+2*width, p[:,2], width, color='orange')

# add some
ax.set_ylabel('Scores')
ax.set_title("Path calculation analysis")

ax.legend( (rects1[0], rects2[0], rects3[0]), ('Naive', 'Optimal', 'Random') )

plt.show()

"""
def main():
    test_num = 10

    polygons_numbers = [int(i) for i in np.linspace(10,100,test_num)]

    runtime_result = np.zeros([test_num, 3])
    length_result = np.zeros([test_num, 3])

    for idx in range(test_num):
        constant.MAX_ICEBERGS = polygons_numbers[idx]
        constant.MIN_ICEBERGS = polygons_numbers[idx]
        # Step 1: Field parameters
        field_size = 300
        start_point = Point(5, 5)
        end_point = Point(field_size - 10, field_size - 10)
        rand_seed = random.randint(0, 600)
        rand_seed = random.randint(rand_seed, 6000)

        print(idx)

        # Step 2: Start the program - create the field and write to file
        field_m = FieldManager(
            size=field_size, start=start_point, end=end_point, seed=rand_seed
        )
        logging.info("Field FieldManager success")
        logging.info("Field seed: {}".format(rand_seed))
        logging.info("Field size: {}".format(field_size))

        # Step 3: Read from file and show the field
        test_field = fh.read_field(constant.FILE_PATH)
        #fh.show_field(test_field, convex=False)

        # Step 4 - Convex Hull
        test_field.polygons = field_m.get_convexhull_polygons()
        #fh.show_field(test_field, convex=True)

        gc = GraphCreator(test_field)


        # Step 5 - Create naive Graph and find the Shortest Path
        start_time = time.time()
        gc.create_graph(graph_type="naive")
        naive_length = gc.shortest_path()
        naive_runtime = time.time() - start_time
        logging.info("naive length: {}".format(naive_length))
        logging.info("naive time: {}".format(naive_runtime))
        #gc.draw_graph()
        runtime_result[idx, 0] = naive_runtime
        length_result[idx, 0] = naive_length

        # Step 6 - Create optimal Graph and find the Shortest Path
        start_time = time.time()
        gc.create_graph(graph_type="optimal")
        optimal_length = gc.shortest_path()
        optimal_runtime = time.time() - start_time
        logging.info("naive length: {}".format(optimal_length))
        logging.info("naive time: {}".format(optimal_runtime))
        #gc.draw_graph()
        runtime_result[idx, 1] = optimal_runtime
        length_result[idx, 1] = optimal_length

        # Step 7 - Create RRT Graph and find the Shortest Path
        start_time = time.time()
        gc.create_graph(graph_type="RRT")
        random_length = gc.shortest_path()
        random_runtime = time.time() - start_time
        logging.info("naive length: {}".format(random_length))
        logging.info("naive time: {}".format(random_runtime))
        #gc.draw_graph()
        runtime_result[idx, 2] = random_runtime
        length_result[idx, 2] = random_length

    file_path = "../Eskimo_path_planning/anaysis_data.txt"
    with open(file_path, 'a') as file:
        file.write(str(runtime_result))
        file.write("\n")
        file.write(str(length_result))
        file.write("\n")

    # Step 8 - Dubins extension
    # gc.dubins_graph(vel=8, phi=6)


if __name__ == "__main__":
    main()