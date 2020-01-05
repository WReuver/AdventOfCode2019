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
        self.buildImage(layers)
                

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

        lowest = counts[0][index]
        lowestIndex = None

        for i, c in enumerate(counts):
            if c[0] < lowest:
                lowest = c[0]
                lowestIndex = i

        return lowestIndex

    def buildImage(self, layers):
        image = layers[0]
        for x, layer in enumerate(layers):
            for i, pixel in enumerate(layer):
                # print(f"Image[{i}] = {image[i]} and pixel = {pixel}")
                if image[i] == 2 and pixel != 2:
                    image[i] = pixel

        chop = []
        index = 0
        for _ in range(6):
            chop.append(image[index: index + 25])
            index += 25

        chop = [i.replace('2', '-') for i in chop]
        [print(i) for i in chop]
            

if __name__ == "__main__":    
    decoder = SpaceImageFormatDecoder('biosimage.sif')
    decoder.decode(25, 6)
