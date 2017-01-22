import getopt

# ----------------- User Input ----------------- #

def get_distances(argv):

	# Default camera positions
	position_0 = (0.0, 0.0)
	position_1 = (0.0, 0.0)

	# Gets user input
    opts, args = getopt.getopt(argv,"h:a:b:",["Help","CameraA=","CameraB="])
    for opt, arg in opts:
	    if opt in ('-h', "--Help"):
            print 'driver.py'
            print ' -a camera_0_x_coordinate, camera_1_0_coordinate'
            print ' -b camera_1_x_coordinate, camera_1_y_coordinate'
        elif opt in ("-a", "--CameraA"):
	        a_x, a_y = tuple(arg)
	        position_0 = double(a_x), double(a_y)
	    elif opt in ("-b", "--CameraB"):
	       	b_x, b_y = tuple(arg)
	        position_0 = double(b_x), double(b_y)