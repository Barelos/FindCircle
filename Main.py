import sys
import re
import matplotlib.pyplot as plt

#####################Constants#####################
ALPHA = 0.01
EPSILON = 0.00001
DEFAULT_R = 1

###################################################
#####################Functions#####################
'''
function to calculate the cost of a guess
'''
def cost_function(x, y, r, x_values, y_values):
    sum = 0
    for i in range(len(x_values)):
        sum += ((x - x_values[i])**2 + (y - y_values[i])**2 - r**2)**2
    return sum

'''
derivative of the cost function with respect to x
'''
def derivative_x(x, y, r, x_values, y_values):
    sum = 0
    for i in range(len(x_values)):
        sum += 4*(x - x_values[i])*((x - x_values[i])**2 + (y - y_values[i])**2 - r**2)
    return sum

'''
derivative of the cost function with respect to y
'''
def derivative_y(x, y, r, x_values, y_values):
    sum = 0
    for i in range(len(x_values)):
        sum += 4*(y - y_values[i])*((x - x_values[i])**2 + (y - y_values[i])**2 - r**2)
    return sum


'''
derivative of the cost function with respect to r
'''
def derivative_r(x, y, r, x_values, y_values):
    sum = 0
    for i in range(len(x_values)):
        sum += -4*r*((x-x_values[i])**2 + (y - y_values[i])**2 - r**2)
    return sum

'''
one step of gradient descent
'''
def gradient_descent(x, y, r, x_values, y_values):
    temp_x = x
    temp_y = y
    temp_r = r

    x -= ALPHA * derivative_x(temp_x, temp_y, temp_r, x_values, y_values)
    y -= ALPHA * derivative_y(temp_x, temp_y, temp_r, x_values, y_values)
    r -= ALPHA * derivative_r(temp_x, temp_y, temp_r, x_values, y_values)
    return x, y, r

'''
function to initialize variables
'''
def initialize_x_y_r(x_values, y_values):
    # initialize x, y and r
    x = sum(x_values) / len(x_values)
    y = sum(y_values) / len(y_values)
    r = (max(x_values)-min(x_values))/2
    return x, y, r

###################################################

def main():

    # make a matcher
    x_and_y = re.compile('(.+),(.+)')
    try:
        # read the input file
        with open(sys.argv[1]) as f:
            lines = f.readlines()

        # make list of x and y values
        x_values = []
        y_values = []
        i = 0

        for line in lines:
            match = x_and_y.match(line)
            x_values.append(int(match.group(1)))
            y_values.append(int(match.group(2)))
            i += 1
        # initialize a guess
        x, y, r =initialize_x_y_r(x_values, y_values)

        #initialize variable for the difrrence between the costs
        dif = 1;
        while dif > EPSILON:
            current_cost = cost_function(x, y, r, x_values, y_values)
            x, y, r = gradient_descent(x, y, r, x_values, y_values)
            new_cost = cost_function(x, y, r, x_values, y_values)
            dif = current_cost - new_cost

            if dif < 0:
                global ALPHA
                ALPHA *= 1 / 10
                dif = 1
                x, y ,r = initialize_x_y_r(x_values, y_values)
        plt.scatter(x_values, y_values)
        circle = plt.Circle((x, y), r, fill=False)
        ax = plt.gca()
        ax.add_artist(circle)
        # val = max(max(x_values),max(y_values),min(x_values),min(y_values))*2
        plt.ylim([y-(r+10), y+r+10])
        plt.xlim([x-(r+10), x+r+10])
        plt.show()
    except:
        print("problem with arguments, enter a proper file path")

# call to start the process
main()