from enum import Enum


class PixelValue(Enum):
    Zero = 1
    One = 2
    Two = 3


class SpaceImageFormatDecoder:
    def __init__(self, imageFile):
        imageData = open(imageFile).readlines()
        self.imageData = imageData[0].strip('\n')
        self.decodedImage = []

    def decode(self, width, height):
        layers = self.splitLayers(width, height)
        image = self.buildImage(layers, width, height)
                

    def checksum(self, width, height):
        layers = self.splitLayers(width, height)
        counts = self.layerCounts(layers)
        lowestIndex = self.lowestCount(counts, PixelValue.Zero)

        return counts[lowestIndex][1] * counts[lowestIndex][2]

    def splitLayers(self, width, height):
        layerSize = (width*height) 
        layers = []
        layerStart = 0

        for _ in range(int(len(self.imageData)/layerSize)):
            layer = self.imageData[layerStart: layerStart+layerSize]
            layers.append(layer)
            layerStart += layerSize

        return layers

    def layerCounts(self, layers):
        counts = []

        for layer in layers:
            zero = layer.count('0')
            one = layer.count('1')
            two = layer.count('2')            
            counts.append([zero, one, two])

        return counts

    def lowestCount(self, counts, pixelValue):
        if pixelValue is PixelValue.Zero:
            index = 0
        elif pixelValue is PixelValue.One:
            index = 1
        elif pixelValue is PixelValue.Two:
            index = 2

        # Set the first pixel as supposed lowest
        lowestIndex = 0

        for i, c in enumerate(counts):
            if c[index] < counts[lowestIndex][index]:
                lowestIndex = i

        return lowestIndex

    def buildImage(self, layers, width, height):
        layers = [list(layer) for layer in layers]
        # Let the first layer be the base image
        imageData = layers[0]

        for x, layer in enumerate(layers):
            for i, pixel in enumerate(layer):
                # Replace transparent pixel with non-transparent pixel if the layer contains one
                if imageData[i] == '2' and pixel != '2':
                    imageData[i] = pixel

        self.printImage(imageData, width, height, True)

    def printImage(self, imageData, width, height, ascii=False):
        image = []
        index = 0
        for _ in range(height):
            # Split the image into a 2D list corresponding its width and height
            image.append(imageData[index: index + width])
            index += width

        # Rejoin each layer into a continuous string
        image = [''.join(layer) for layer in image]
        # Replace numbers with characters for legibility
        if ascii:
            image = [i.replace('0', '-') for i in image]
            image = [i.replace('1', 'Z') for i in image]
            image = [i.replace('2', '-') for i in image]
        
        [print('\t' + i) for i in image]
            

if __name__ == "__main__":    
    decoder = SpaceImageFormatDecoder('biosimage.sif')
    decoder.decode(25, 6)
