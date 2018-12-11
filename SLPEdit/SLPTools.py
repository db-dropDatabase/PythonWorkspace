"""
SLP Encoding, manipulation, and decoding library for AoE2:HD SLP Files

For more information, check out the Spec.md.
"""

from struct import *



HEADER_t = "<4sI24s"
FRAME_DATA_t = "<8I"
OUTLINE_t = "<2H"


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

