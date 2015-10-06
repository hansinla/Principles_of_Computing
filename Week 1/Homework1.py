"""
HOMEWORK 1
"""

def resources_vs_time(upgrade_cost_increment, num_upgrade):
    """
    Build function that performs unit upgrades with specified cost increments
    """
    cost = 1.0 + upgrade_cost_increment
    rate = 2.0
    total_resources_generated = 1.0
    time = 1.0
    time_slice = 0.0000001

    upgrade_list = [[time, total_resources_generated]]

    for i in range(1, num_upgrade):
        time_needed = cost/rate
        total_resources_generated += cost
        time += time_needed
        upgrade_list.append([time, total_resources_generated])
        rate += 1.0
        cost += upgrade_cost_increment

    return upgrade_list

def test():
    """
    Testing code for resources_vs_time
    """
    data1 = resources_vs_time(0.5, 20)
##    data2 = resources_vs_time(1.5, 10)
    data3 = resources_vs_time(0, 10)
    data4 = resources_vs_time(1, 10)
##
    print(data1)
##    print()
##    print(data2)
##    print()
##    print(data3[9])
##    print(data4[9])

test()


# Sample output from the print statements for data1 and data2
#[[1.0, 1], [1.75, 2.5], [2.41666666667, 4.5], [3.04166666667, 7.0], [3.64166666667, 10.0], [4.225, 13.5], [4.79642857143, 17.5], [5.35892857143, 22.0], [5.91448412698, 27.0], [6.46448412698, 32.5], [7.00993867244, 38.5], [7.55160533911, 45.0], [8.09006687757, 52.0], [8.62578116328, 59.5], [9.15911449661, 67.5], [9.69036449661, 76.0], [10.2197762613, 85.0], [10.7475540391, 94.5], [11.2738698286, 104.5], [11.7988698286, 115.0]]
#[[1.0, 1], [2.25, 3.5], [3.58333333333, 7.5], [4.95833333333, 13.0], [6.35833333333, 20.0], [7.775, 28.5], [9.20357142857, 38.5], [10.6410714286, 50.0], [12.085515873, 63.0], [13.535515873, 77.5]]

