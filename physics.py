""" LEGACY CODE
# Check collisions between polygon and rectangle
def check_collisions_polygon_rectangle(poly, rect):
    for i in range(len(poly)):
        if i == 1 and len(poly) == 2:
            break
        if i + 1 == len(poly):
            line = (poly[0], poly[i])
        else:
            line = (poly[i], poly[i + 1])
        for j in range(len(rect)):
            if j == 1 and len(rect) == 2:
                break
            if j + 1 == len(rect):
                right_line = (rect[0], rect[j])
            else:
                right_line = (rect[j], rect[j + 1])
            if check_collision_line_right_line(line, right_line):
                return j
    return -1
"""


# Check collisions between polygon and rectangle
import math


def check_collisions_polygon_rectangle(poly, rect):
    for i in range(len(poly)):
        if i == 1 and len(poly) == 2:
            break

        if i + 1 == len(poly):
            line = (poly[0], poly[i])
        else:
            line = (poly[i], poly[i + 1])

        for j in range(len(rect)):
            if j == 1 and len(rect) == 2:
                break

            if j + 1 == len(rect):
                rect_line = (rect[0], rect[j])
            else:
                rect_line = (rect[j], rect[j + 1])
            if check_collisions_polygons(line, rect_line):
                return j
    return -1


# Check collisions between two polygons
def check_collisions_polygons(a, b):
    for i in range(len(a)):
        if i == 1 and len(a) == 2:
            break
        if i + 1 == len(a):
            line_a = (a[0], a[i])
        else:
            line_a = (a[i], a[i + 1])
        for j in range(len(b)):
            if j == 1 and len(b) == 2:
                break
            if j + 1 == len(b):
                line_b = (b[0], b[j])
            else:
                line_b = (b[j], b[j + 1])
            if check_collision_lines(line_a, line_b):
                # print("Collision between:", line_a, "and", line_b)
                return True
    # print("i:", i, "j:", j)
    return False


# Check if two lines intersect a=((ax1, ay1), (ax2, ay2)) and b=((bx1, by1), (bx2, by2))
def check_collision_lines(a, b) -> bool:
    # Check if two segment intersect (using wikipedia's line-line intersection, section "Given two points on each line segment").
    # This method works with any pair of segments that are not parallel (even vertical and perpendicular).
    # There is an intersection if 0 <= t <= 1 and 0 <= u <= 1.
    denominator = (a[0][0] - a[1][0]) * (b[0][1] - b[1][1]) - (a[0][1] - a[1][1]) * (b[0][0] - b[1][0])

    if denominator == 0:  # If the lines are parallel
        print("Oh no it's broken !")
        return False
    else:
        # Calculate t and u, and check if (0 <= u <= 1 and 0 <= t <= 1)
        if 0 <= ((a[0][0] - b[0][0]) * (b[0][1] - b[1][1]) - (a[0][1] - b[0][1]) * (b[0][0] - b[1][0])) / denominator <= 1 and 0 <= ((a[0][0] - b[0][0]) * (a[0][1] - a[1][1]) - (a[0][1] - b[0][1]) * (a[0][0] - a[1][0])) / denominator <= 1:
            return True

    return False

    # if a[0][0] == a[1][0] or b[0][0] == b[1][0]:  # One line is vertical
    #     if a[0][0] == a[1][0] and b[0][0] == b[1][0]:  # Lines are vertical
    #         # Check if the vertical lines intersect
    #         if a[0][0] == b[0][0] and \
    #                 (b[0][1] <= a[0][1] <= b[1][1] or b[0][1] <= a[1][1] <= b[1][1] or a[0][1] <= b[0][1] <= a[1][1]
    #                  or a[0][1] <= b[1][1] <= a[1][1] or b[0][1] >= a[0][1] >= b[1][1] or b[0][1] >= a[1][1] >= b[1][1]
    #                  or a[0][1] >= b[0][1] >= a[1][1] or a[0][1] >= b[1][1] >= a[1][1]):
    #             return True
    #         else:
    #             return False
    #     else:  # Only one line is parallel, check as if lines where random
    #         return (point_orientation(a[0], a[1], b[0]) != point_orientation(a[0], a[1], b[1]) and
    #                 point_orientation(b[0], b[1], a[0]) != point_orientation(b[0], b[1], a[1]))
    # elif (a[1][1] - a[0][1]) / (a[1][0] - a[0][0]) == (b[1][1] - b[0][1]) / (b[1][0] - b[0][0]):  # Lines are parallel
    #     # Check if lines have the same y-intersect
    #     a_slope = (a[1][1] - a[0][1]) / (a[1][0] - a[0][0])
    #     b_slope = (b[1][1] - b[0][1]) / (b[1][0] - b[0][0])
    #
    #     # p = y - mx
    #     if a[0][1] - a_slope * a[0][0] == b[0][1] - b_slope * b[0][0]:  # Lines are aligned
    #         if (b[0][1] <= a[0][1] <= b[1][1] or b[0][1] <= a[1][1] <= b[1][1] or a[0][1] <= b[0][1] <= a[1][1]
    #                 or a[0][1] <= b[1][1] <= a[1][1] or b[0][1] >= a[0][1] >= b[1][1] or b[0][1] >= a[1][1] >= b[1][1]
    #                 or a[0][1] >= b[0][1] >= a[1][1] or a[0][1] >= b[1][1] >= a[1][1]):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
    # else:  # Lines are not parallel
    #     # Use orientation of point to determine
    #     # return (point_orientation(a[0], b[0], a[1]) != point_orientation(a[0], b[0], b[1]) and
    #     #         point_orientation(a[1], b[1], a[0]) != point_orientation(a[1], b[1], b[0]))
    #     return (point_orientation(a[0], a[1], b[0]) != point_orientation(a[0], a[1], b[1]) and
    #             point_orientation(b[0], b[1], a[0]) != point_orientation(b[0], b[1], a[1]))


# Returns whether three points are in counter-clockwise order or not
# def point_orientation(p1, p2, p3):
#     return (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p3[1] - p2[1]) * (p2[0] - p1[0]) < 0


# def vector_angle():
#     pass  # TODO


"""
# Check collisions between two random lines
def check_collision_lines(a, b):
    # Find the simplified equation of each line
    # y = ratio_a * x + intercept_a
    # y = ratio_b * x + intercept_b

    if a[0][0] == a[1][0]:  # Vertical line_a
        if b[0][0] == b[1][0]:  # Vertical line_b
            if a[0][0] == b[0][0] and ((b[0][1] <= a[0][1] <= b[1][1]) or (b[0][1] <= a[1][1] <= b[1][1]) or (a[0][1] <= b[0][1] <= a[1][1]) or (a[0][1] <= b[1][1] <= a[1][1])):
                return True
        elif b[0][1] == b[1][1]:  # Horizontal line_b
            if ((b[0][0] <= a[0][0] <= b[1][0]) or (b[1][0] <= a[0][0] <= b[0][0])) and ((a[0][1] <= b[0][1] <= a[1][1]) or (a[1][1] <= b[0][1] <= a[0][1])):
                return True
        else:  # Random line_b
            ratio_b = (b[1][1] - b[0][1]) / (b[1][0] - b[0][0])
            intercept_b = b[0][1] - (ratio_b * b[0][0])
            x = a[0][0]
            y = ratio_b * x + intercept_b
            if ((b[0][0] <= x <= b[1][0]) or (b[1][0] <= x <= b[0][0])) and ((a[0][1] <= y <= a[1][1]) or (a[1][1] <= y <= a[0][1])) and ((b[0][1] <= y <= b[1][1]) or (b[1][1] <= y <= b[0][1])):
                return True
    elif a[0][1] == a[1][1]:  # Horizontal line_a
        if b[0][0] == b[1][0]:  # Vertical line_b
            if ((a[0][0] <= b[0][0] <= a[1][0]) or (a[1][0] <= b[0][0] <= a[0][0])) and ((b[0][1] <= a[0][1] <= b[1][1]) or (b[1][1] <= a[0][1] <= b[0][1])):
                return True
        elif b[0][1] == b[1][1]:  # Horizontal line_b
            if a[0][1] == b[0][1] and ((b[0][0] <= a[0][0] <= b[1][0]) or (b[0][0] <= a[1][0] <= b[1][0]) or (a[0][0] <= b[0][0] <= a[1][0]) or (a[0][0] <= b[1][0] <= a[1][0])):
                return True
        else:  # Random line_b
            ratio_b = (b[1][1] - b[0][1]) / (b[1][0] - b[0][0])
            intercept_b = b[0][1] - (ratio_b * b[0][0])
            y = a[0][1]
            x = (y - intercept_b) / ratio_b
            if ((b[0][1] <= y <= b[1][1]) or (b[1][1] <= y <= b[0][1])) and ((a[0][0] <= x <= a[1][0]) or (a[1][0] <= x <= a[0][0])) and ((b[0][0] <= x <= b[1][0]) or (b[1][0] <= x <= b[0][0])):
                return True
    else:
        ratio_a = (a[1][1] - a[0][1]) / (a[1][0] - a[0][0])
        intercept_a = a[0][1] - (ratio_a * a[0][0])
        if b[0][0] == b[1][0]:  # Vertical line_b
            x = b[0][0]
            y = ratio_a * x + intercept_a
            if ((a[0][0] <= x <= a[1][0]) or (a[1][0] <= x <= a[0][0])) and ((a[0][1] <= y <= a[1][1]) or (a[1][1] <= y <= a[0][1])) and ((b[0][1] <= y <= b[1][1]) or (b[1][1] <= y <= b[0][1])):
                return True
        elif b[0][1] == b[1][1]:  # Horizontal line_b
            y = b[0][1]
            x = (y - intercept_a) / ratio_a
            if ((a[0][1] <= y <= a[1][1]) or (a[1][1] <= y <= a[0][1])) and ((a[0][0] <= x <= a[1][0]) or (a[1][0] <= x <= a[0][0])) and ((b[0][0] <= x <= b[1][0]) or (b[1][0] <= x <= b[0][0])):
                return True
        else:  # Random line_b
            ratio_b = (b[1][1] - b[0][1]) / (b[1][0] - b[0][0])
            intercept_b = b[0][1] - (ratio_b * b[0][0])
            if ratio_a == ratio_b:  # Parallel lines
                if intercept_a == intercept_b:
                    return True
            else:
                x = (intercept_b - intercept_a) / (ratio_a - ratio_b)
                y = ratio_a * x + intercept_a
                if ((a[0][0] <= x <= a[1][0]) or (a[1][0] <= x <= a[0][0])) and ((b[0][0] <= x <= b[1][0]) or (b[1][0] <= x <= b[0][0])) and ((a[0][1] <= y <= a[1][1]) or (a[1][1] <= y <= a[0][1])) and ((b[0][1] <= y <= b[1][1]) or (b[1][1] <= y <= b[0][1])):
                    return True

    # print("No collision: lines touch but not on segments x:", x, "y:", y)
    return False


# Check collisions between a random line and a right line
def check_collision_line_right_line(line, right_line):
    # Line is not vertical nor horizontal
    if line[0][0] == line[1][0]:  # Vertical line
        # Vertical obstacle line and Vertical line
        if right_line[0][0] == right_line[1][0]:
            if right_line[0][0] == line[0][0] and ((line[0][1] <= right_line[0][1] <= line[1][1]) or (
                    line[0][1] <= right_line[1][1] <= line[1][1]) or (
                                                           right_line[0][1] <= line[0][1] <= right_line[1][1]) or (
                                                           right_line[0][1] <= line[1][1] <= right_line[1][1])):
                return True
        # Horizontal obstacle line and Vertical line
        elif right_line[0][1] == right_line[1][1]:
            if ((right_line[0][0] >= line[0][0] >= right_line[1][0]) or (
                    right_line[1][0] >= line[0][0] >= right_line[0][0])) and ((line[0][1] >= right_line[0][1] >= line[1][1]) or (
                    line[1][1] >= right_line[0][1] >= line[0][1])):
                return True
    elif line[0][1] == line[1][1]:  # Horizontal line
        # Vertical obstacle line and Horizontal line
        if right_line[0][0] == right_line[1][0]:
            if ((line[0][0] <= right_line[0][0] <= line[1][0]) or (line[1][0] <= right_line[0][0] <= line[0][0])) and ((right_line[0][1] <= line[0][1] <= right_line[1][1]) or (right_line[1][1] <= line[0][1] <= right_line[0][1])):
                return True
        # Horizontal obstacle line and Horizontal line
        elif right_line[0][1] == right_line[1][1]:
            if right_line[0][1] == line[0][1] and ((line[0][0] <= right_line[0][0] <= line[1][0]) or (
                    line[0][0] <= right_line[1][0] <= line[1][0]) or (
                                                           right_line[0][0] <= line[0][0] <= right_line[1][0]) or (
                                                           right_line[0][1] <= line[1][0] <= right_line[1][0])):
                return True
    elif line[0][0] != line[1][0] and line[0][1] != line[1][1]:
        ratio = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
        intercept = line[0][1] - (ratio * line[0][0])
        if right_line[0][0] == right_line[1][0]:  # Vertical obstacle line
            x = right_line[0][0]
            y = ratio * x + intercept

            if ((line[0][0] >= x >= line[1][0]) or (line[1][0] >= x >= line[0][0])) and ((right_line[0][1] >= y >= right_line[1][1]) or (right_line[1][1] >= y >= right_line[0][1])):
                return True
        elif right_line[0][1] == right_line[1][1]:  # Horizontal obstacle line
            y = right_line[0][1]
            x = (y - intercept) / ratio

            if ((line[0][1] <= y <= line[1][1]) or (line[1][1] <= y <= line[0][1])) and ((right_line[0][0] <= x <= right_line[1][0]) or (right_line[1][0] <= x <= right_line[0][0])):
                return True
    return False
"""


# Get the angle between two lines
def get_lines_angle(a: tuple, b: tuple):
    a_len = math.sqrt((a[1][0] - a[0][0]) ** 2 + (a[1][1] - a[0][1]) ** 2)
    b_len = math.sqrt((b[1][0] - b[0][0]) ** 2 + (b[1][1] - b[0][1]) ** 2)
    dot_prod = (a[1][0] - a[0][0]) * (b[1][0] - b[0][0]) + (a[1][1] - a[0][1]) * (b[1][1] - b[0][1])
    return math.degrees(math.acos(dot_prod / (a_len * b_len)))


# Get the coordinates of the vertices of a rectangle
def get_rectangle_vertices(rect):
    return (rect[0], rect[1]), (rect[0] + rect[2], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), \
           (rect[0], rect[1] + rect[3])
