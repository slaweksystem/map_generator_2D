def get_rotated(coords, rotation):

    newCordX = coords[0]
    newCordY = coords[1]

    oldCordX = newCordX
    oldCordY = newCordY

    for _ in range (rotation):
        newCordX = oldCordY
        newCordY = -oldCordX

        oldCordX = newCordX
        oldCordY = newCordY

    return (newCordX, newCordY)

def rotate_coords(coords, size, rotation):
    # Rotate Coords
    newCoords = get_rotated(coords, rotation)

    # Rotate Size
    newSizeAdjustment = get_rotated(size, rotation)

    # Coords adjustment (rotation along the left botttom corner):
    newSizeAdjustmentX = -1 * min(0, newSizeAdjustment[0] + 1) # Had to add one due to the fact, that we operate on coordinats
    newSizeAdjustmentY = -1 * min(0, newSizeAdjustment[1] + 1)

    newCoords = (newCoords[0] + newSizeAdjustmentX, newCoords[1] + newSizeAdjustmentY)

    return newCoords

def rotate_connection(connection, rotation):

    return get_rotated(connection, rotation)