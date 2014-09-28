__author__ = 'tmwsiy'
import socket, time

UDP_IP = "192.168.5.12"
#UDP_IP = "192.168.5.17"

UDP_PORT = 4239

def send_command(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command, (UDP_IP, UDP_PORT))
    time.sleep(.025)

def set_block(x, y, z, block):
    send_command(' '.join(['/setblock', str(x) ,str(y)  , str(z) , block,'\r\n']))

def draw_cube(origin, size, block):
    for i in range(size):
        for j in range(size):
            for k in range(size):
                set_block(origin[0]+i , origin[1]+j, origin[2]+k, block)


def draw_flat_plane(origin, length, width,  block):
    for i in range(width):
        for j in range(length):
                set_block(origin[0]+i , origin[1], origin[2]+j, block)

#along x-axis
def draw_vertical_plane(origin, height, width,  block):
    for i in range(width):
        for j in range(height):
                set_block(origin[0]+i , origin[1]+j, origin[2], block)

#along z-axis
def draw_vertical_plane_90deg(origin, height, width,  block):
    for i in range(width):
        for j in range(height):
                set_block(origin[0] , origin[1]+j, origin[2]+i, block)

# size should be odd
def draw_pyramid( origin, size, block, step_size=2):
    if size <= 0:
        return
    draw_flat_plane(origin, size,  size, block)
    origin[1]+=1
    origin[2]+=1
    origin[0]+=1
    draw_pyramid(origin,size-step_size, block, step_size)

def draw_box(origin, length, height, width,  block):
    #draw left wall
    draw_vertical_plane(origin, height + 1, length, block)
    # draw bottom
    draw_flat_plane(origin,width + 1, length,  block)
    # increase reference point by height
    origin[1] += height
    # draw top
    draw_flat_plane(origin,width  + 1, length,  block)
    # decrease reference point by height to reset
    origin[1] -= height
    # increase reference point horizontally to right corner
    origin[2] += width
    # draw right side
    draw_vertical_plane(origin, height, length, block)
    # decrease reference point horizontally to reset
    origin[2] -= width
    draw_vertical_plane_90deg(origin, height +1, length, block)
    # increase reference point (other) horizontally to back left corner
    origin[0] += (length -1)
    draw_vertical_plane_90deg(origin, height +1, length, block)
    origin[0] -= length

origin=[-99, 115, -464,]

draw_flat_plane(origin, 50, 50,  'air')

#draw_box(origin, 10, 10, 10, 'cobblestone')
