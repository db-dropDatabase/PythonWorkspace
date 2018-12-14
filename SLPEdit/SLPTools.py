"""
SLP Encoding, manipulation, and decoding library for AoE2:HD SLP Files

For more information, check out the Spec.md.
"""

from struct import *
from enum import Enum

HEADER_t = "<4sI24s"
FRAME_DATA_t = "<8I"
OUTLINE_t = "<2H"

class PixelState(Enum):
    TRANSPARENT = 0,
    COLOR = 1,
    TEAM_COLOR = -1

    @staticmethod
    def getState(num):
        if num > 0:
            return PixelState.COLOR
        if num < 0:
            return PixelState.TEAM_COLOR
        return PixelState.TRANSPARENT

"""
Decode the header of an SLP file into python-understandable types.
"""
def decodeSLPHeader(slpData):
    data = unpack(HEADER_t, slpData[:32])
    return {
        "version": data[0].decode('ascii'),
        "num_frames": data[1],
        "comment": data[2].decode('ascii'),
    }


def encodeSimpleSLP(frame, framecount):
    width = len(frame[0])
    height = len(frame)
    # generate and pack header
    outstr = bytearray(pack(HEADER_t, b'2.0N', framecount, b"Noah and Sam!\0"))
    # generate a single template frame
    # assume no outlines or team colors for now
    frameCommand = bytearray([])
    # we also need to store the relative offsets so we can make them absolute later
    frameOffsets = []
    for y in range(height):
        frameOffsets.append(len(frameCommand))
        # block copy command, with length of the image
        frameCommand.append(width << 2)
        for x in range(width):
            # append each pixel color code
            frameCommand.append(frame[y][x])
        # end row
        frameCommand.append(0x0F)
    # generate a single template for the outlines, which is just a bunch of zeros
    outlines = bytearray([0 for x in range(4 * height)])
    # outlines + the commad offset data
    frameDataRelOffset = len(outlines)
    # add that do the data itself and we got ouselves frame size
    frameDataSize = frameDataRelOffset + height * 4 + len(frameCommand)
    # header + frame_data array
    frameDataOff = 32 * framecount + 32
    # generate and start appending the frame_data array
    for i in range(framecount):
        outstr.extend(pack(FRAME_DATA_t, 
            frameDataOff + frameDataRelOffset + frameDataSize*i, 
            frameDataOff + frameDataSize*i, 
            0, 
            24, 
            width,
            height,
            width // 2,
            height // 2
        ))
    # finish generating and append the frames themselves
    for i in range(framecount):
        # append outlines
        outstr.extend(outlines)
        # append command offset data
        startlen = len(outstr) + height * 4
        for i in range(height):
            # binary length + the length of the offsets themselves plus the relative offset
            outstr.extend(pack("<I", startlen + frameOffsets[i]))
        # append the frame itself
        outstr.extend(frameCommand)
    return outstr;

"""
Encode a series of bitmap images (row major 2d arrays) into an SLP, or a asset format used
by Age of Empires 2

Parameters:
    frames - An array of images (2d row-major arrays). Uses the in-game color pallete,
    except in the case of negative numbers, which are replaced with team colors (-1 to -8
    are valid team colors). All images must be the same width and height, and for best
    results less than 64x64.
Returns: A bytearray of the raw generated SLP file

"""
def encodeSLP(frames):
    width = len(frames[0][0])
    height = len(frames[0])
    # generate and pack header
    header = bytearray(pack(HEADER_t, b'2.0N', len(frames), b"Noah's SLP tool!\0"))
    # generate the frame command strings, with offsets
    frameCommands = []
    for singleFrame in frames:
        # store the frame data in a bytearray
        # we also need to store the relative offsets so we can make them absolute later
        frameData = {
            "off": [],
            "data": bytearray([]),
        }
        for y, row in enumerate(singleFrame):
            # get current relative offset
            frameData["off"].append(len(frameData["data"]))
            # iterate through the array, pushing a command on condition change or row end
            tempPixels = []
            for x, pix in enumerate(row, 0):
                tempPixels.append(pix)
                state = PixelState.getState(pix)
                # if the state is going to change or we're on the last pixel, write command
                if x == width - 1 or state != PixelState.getState(row[x + 1]):
                    if state == PixelState.COLOR:
                        # write block command command
                        frameData["data"].append(len(tempPixels) << 2)
                        # and the data
                        frameData["data"].extend(tempPixels)
                    elif state == PixelState.TRANSPARENT:
                        # write a transparent command (skip pixels)
                        frameData["data"].append((len(tempPixels) << 2) | 1)
                    elif state == PixelState.TEAM_COLOR:
                        # write a team color block
                        if len(tempPixels) < 16:
                            # short block
                            frameData["data"].append((len(tempPixels) << 4) | 0b0110)
                        # else long block
                        else:
                            frameData["data"].append(0b00000110)
                            frameData["data"].append(len(tempPixels))
                        # write pixel data, but not negative
                        frameData["data"].extend([abs(pix) for pix in tempPixels])
                    else:
                        print("aaaaAAA?")
                        return None
                    # clear pixels
                    tempPixels = []
            # end row
            frameData["data"].append(0x0F)
        # append the frame to the generated framecommands
        frameCommands.append(frameData)
    # generate and start appending the frame_data array, based on the sizes of our frames
    frameMeta = bytearray([])
    # calculate the data offset by adding the header, size of the frame data array
    offset = 32 + 32*len(frameCommands)
    for i, frame in enumerate(frameCommands):
        # create our frame metadata
        frameMeta.extend(pack(FRAME_DATA_t,
            # add outline size to get data offset
            offset + 4*height,
            offset,
            0, 
            24, 
            width,
            height,
            width // 2, # centerX at closest to center
            height // 2
        ))
        # keep a running total of the offset, adding the outlines, offsets, and data (the size of the frame)
        offset = offset + 8*height + len(frame["data"])
    # start generating the file itself
    outFile = header + frameMeta
    # generate a single template for the outlines, which is just a bunch of zeros
    outlines = bytearray([0 for x in range(4 * height)])
    # finish generating and append the frames themselves
    for i, frame in enumerate(frameCommands):
        # append outlines
        outFile.extend(outlines)
        # append command offset data
        startlen = len(outFile) + height*4
        for h in range(height):
            # binary length + the length of the offsets themselves plus the relative offset
            outFile.extend(pack("<I", startlen + frame["off"][h]))
        # append the frame itself
        outFile.extend(frame["data"])
    return outFile;