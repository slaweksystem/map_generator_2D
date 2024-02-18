class MapPiece:

    def __init__(self, pieceData: dict):

        valid, output = MapPiece.validate_pieceData_(pieceData)
        if not valid:
            raise Exception("Bad piece:", output)
        
        self.id = pieceData["ID"]
        self.name = pieceData["name"]
        self.size = tuple(pieceData["size"])
        # Convert lists to tuples
        self.connections = tuple(tuple(tuple(el) for el in par) for par in pieceData["connections"])
        self.fields = pieceData["fields"]
        self.image = pieceData["image"]

    def validate_pieceData_(pieceData: dict) -> "list[bool, str]":

        # Check for ID
        if not pieceData["ID"]:
            return False, "missing ID"
        
        # Add validation

        return True, "Piece Ok"

    #def parseJson(pieceList: "list[dict]") -> "list[MapPiece]":
    #
    #    while pieceList:
    #        piece = pieceList.pop(0)
    #        MapPiece._validate_pieceData_(piece)