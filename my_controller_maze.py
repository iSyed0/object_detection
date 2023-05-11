"""my_controller_maze controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Camera

if __name__ == "__main__":

    # create the Robot instance.
    robot = Robot()
    
    # get the time step of the current world.
    TIME_STEP = 64
    max_speed = 6.28


    # creating motor instances and setting position and velocity
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setPosition(float('inf'))    
    right_motor.setPosition(float('inf'))
    
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
        
    def set_speed(left, right):
        left_motor.setVelocity(left)
        right_motor.setVelocity(right)
    
    # creating camera and distance sensor instance 
    camera = robot.getDevice('camera')
    camera.enable(TIME_STEP)

    # Initialize a flag for stopping at blue
    stopped_at_blue = False

    # Main loop:
    while robot.step(TIME_STEP) != -1:
        if not stopped_at_blue:
        
            speed = [0.5 * max_speed, 0.5 * max_speed]  # [left, right]
            
            # Process camera image
            image = camera.getImage()
            width = camera.getWidth()
            height = camera.getHeight()
            green = False
            red = False
            blue = False
            
            # color detection
            for x in range(0, width, 10):  # step size 10 to speed up
                for y in range(0, height, 10):
                    r = camera.imageGetRed(image, width, x, y)
                    g = camera.imageGetGreen(image, width, x, y)
                    b = camera.imageGetBlue(image, width, x, y)
                    
                    # Define color ranges
                    green_range = g > 2.5*r and g > 2.5*b
                    red_range = r > 2.5*g and r > 2.5*b
                    blue_range = b > 2.5*r and b > 2.5*g
                    
                    if green_range:
                        green = True
                        print("Detected green") 
                    elif red_range:
                        red = True
                        print("Detected red")  
                    elif blue_range:
                        blue = True
                        print("Detected blue")  
                    
                    
            # Define behaviors based on detected colors
            if green:
                speed = [0.1 * max_speed, -0.1 * max_speed] # turn left
                print("Detected green box, turning left") 
                robot.step(1900)
            elif red:
                speed = [-0.1 * max_speed, 0.1 * max_speed] # turn right
                print("Detected red box, turning right")
                robot.step(1900)
            elif blue:
                speed = [0.0, 0.0] # stop
                print("Detected blue ball, stopping")
                stopped_at_blue = True
    
            else:
                speed = [0.5 * max_speed, 0.5 * max_speed] # drive forward
            
            left_motor.setVelocity(speed[0])
            right_motor.setVelocity(speed[1])
    
            # Enter here exit cleanup code.
        