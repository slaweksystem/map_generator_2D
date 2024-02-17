import numpy as np

from src.Map.MapPiece import MapPiece

class MapGrid:
    pieces: "dict[int, MapPiece]"

    def __init__(self, PieceData: "dict"):
        print("Initilizing Map")
        print(f"Process Data for set: {PieceData['Name']}")

        self.pieceSize = PieceData["PieceSize"]
        
        self.pieces = {}
        self._load_pieces(PieceData["Pieces"].copy())
        
        # Init Some Variables
        self.mapElements = []
        
    def _load_pieces(self, pieces: list):
        while pieces:
            candidate = pieces.pop(0)
            try:
                self.pieces[candidate["ID"]] = MapPiece(candidate)
            except Exception as e: 
                print(f'Unable to add Piece: {candidate["name"]} - {e}')
                continue

    def addItem(self, pieceID: int, rotation: int, coords: "tuple[int, int]"):
    
        # Check, if ID is valid
        if not pieceID in self.pieces:
            raise Exception(f"Invalid piece ID: {pieceID}")

        # Check collision
        
        ## Account for element rotation
        sizeCoordX = rotation%2
        sizeCoordY = int(not rotation%2)
        sizeX = self.pieces[pieceID].size[sizeCoordX]
        sizeY = self.pieces[pieceID].size[sizeCoordY]

        if not self.checkCoords(coords, (sizeX, sizeY)):
            raise Exception(f"Area occupied: {coords}")

        # Check if connection points match

        self.mapElements.append({
            "ID": pieceID,
            "rotation": rotation,
            "coords": coords})
            
    def delItem(self, coords: "tuple[int, int]"):
        '''
        
        '''
        print("Deletion not implemented yet")

        for item in self.mapElements:
            if item["coords"] == coords:
                print(f"Found")

    def checkCoords(self, coords: "tuple[int, int]", size:"tuple[int, int]" = (1, 1)) -> bool:
        '''
        Check if coords are free - return True if yes, False if not
        '''

        endCoords = (coords[0] + size[0] - 1, coords[1] + size[1] - 1)

        # Check coords
        for element in self.mapElements:
            # Account for element rotation
            sizeCoordX = element["rotation"]%2
            sizeCoordY = int(not element["rotation"]%2)

            itemEndCoords = (element['coords'][0] + self.pieces[element['ID']].size[sizeCoordX] - 1, element['coords'][1] + self.pieces[element['ID']].size[sizeCoordY] - 1)
    
            # check if item occupies space
            if coords[0] <= itemEndCoords[0] and endCoords[0] >= element['coords'][0] and \
               coords[1] <= itemEndCoords[1] and endCoords[1] >= element['coords'][1]:
                return False
            
        return True

    def getDimensions(self) -> "list[tuple[int, int],tuple[int, int],tuple[int, int]]":

        if not self.mapElements:
            return (1,1), (0,0), (0,0)
        
        startCoords, endCoords = self.getBorderCoords()

        size = (endCoords[0] - startCoords[0] + 1 , endCoords[1] - startCoords[1] + 1)

        return size, startCoords, endCoords
    
    def getBorderCoords(self) -> "list[tuple[int, int], tuple[int, int]]":
        startCoords = []
        endCoords = []
        # In case The map is still empty:
        if not self.mapElements:
            startCoords = [0,0]
            endCoords = [0,0]
        else:
            # Need to start somewhere
            startCoords = list(self.mapElements[0]["coords"])
            endCoords   = list(self.mapElements[0]["coords"])

        for element in self.mapElements:
            # Start coords
            startCoords[0] = min(startCoords[0], element["coords"][0])
            startCoords[1] = min(startCoords[1], element["coords"][1])

            # End coords
            # Account for rotation
            sizeCoordX = element["rotation"]%2
            sizeCoordY = int(not element["rotation"]%2)

            endReachCoordX = element["coords"][0] + self.pieces[element["ID"]].size[sizeCoordX] - 1
            endReachCoordY = element["coords"][1] + self.pieces[element["ID"]].size[sizeCoordY] - 1

            endCoords[0] = max(endCoords[0], endReachCoordX)
            endCoords[1] = max(endCoords[1], endReachCoordY)

        return tuple(startCoords), tuple(endCoords)
    

    def getItemsFromCoords(self, coords: "tuple[int, int]", size:"tuple[int, int]" = (1, 1)) -> list:

        endCoords = (coords[0] + size[0] - 1, coords[1] + size[1] - 1)
        elementsInCoords = []
        # Check coords
        for element in self.mapElements:
            # Account for element rotation
            sizeCoordX = element["rotation"]%2
            sizeCoordY = int(not element["rotation"]%2)

            itemEndCoords = (element['coords'][0] + self.pieces[element['ID']].size[sizeCoordX] - 1, element['coords'][1] + self.pieces[element['ID']].size[sizeCoordY] - 1)
    
            # check if item occupies space
            if coords[0] <= itemEndCoords[0] and endCoords[0] >= element['coords'][0] and \
               coords[1] <= itemEndCoords[1] and endCoords[1] >= element['coords'][1]:
                elementsInCoords.append(element)
            
        return elementsInCoords
    
    def renderMap(self):

        map_size, startCoords, _ = self.getDimensions()

        map_width  = self.pieceSize * map_size[0]
        map_height = self.pieceSize * map_size[1]

        rendered_map = np.zeros([map_height, map_width, 3], np.uint8)
        rendered_map[:] = 125 # Grey color

        # Grid paint - vertical
        for i in range (1, map_size[0]):
            rendered_map[:,i*self.pieceSize] = 255

        # Grid paint - Horizontal
        for i in range (1, map_size[1]):
            rendered_map[i*self.pieceSize] = 255

        print("Start coords:", startCoords)

        # Add Pieces to the map
        for element in self.mapElements:
            # print("Adding Item:", element)
            # print("Name:", self.pieces[element['ID']].name)

            size = self.pieces[element['ID']].size
            # print(f"Element Size: {size[0]}x{size[1]}")

            # Account for rotation
            sizeCoordX = element["rotation"]%2
            sizeCoordY = int(not element["rotation"]%2)

            # Calculate position on the picture:
            element_start_w = self.pieceSize * (element["coords"][0] - startCoords[0])
            element_start_h = self.pieceSize * (map_size[1] - (element["coords"][1] - startCoords[1]) - size[sizeCoordY])
            
            # print(f"Picture element start coords - {element_start_w},{element_start_h}")

            element_end_w = element_start_w + self.pieceSize * size[sizeCoordX]
            element_end_h = element_start_h + self.pieceSize * size[sizeCoordY]

            # print(f"Picture element end coords -   {element_end_w},{element_end_h}")

            rendered_map[element_start_h:element_end_h,element_start_w:element_end_w] = np.rot90(self.pieces[element['ID']].image, k=-element["rotation"], axes=(0,1))     

        return rendered_map
    
