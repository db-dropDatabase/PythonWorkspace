# SLP File Spec

## Introduction

SLP files are the image asset storage method for the Genie Engine, used in games such as Age of Empires 2. This file seeks to collect my notes on the SLP file format, and hopefully serve as a resource to developers looking to accomplish something with the SLP files.

Here are some places I have pulled my resources:
* https://web.archive.org/web/20160801213608/http://www.boekabart.net/aoe2wide/hg/slp.txt
* https://web.archive.org/web/20131127014051/http://www.digitization.org:80/wiki/index.php/SLP (kinda sparse)
* https://github.com/fredreichbier/genie
* https://github.com/genie-js/genie-slp
* And, of course, looking at raw SLP files.

For consistency and clarity, here are some standards which I will maintain throughout this paper:
* All strings in code examples will **not** be automatically null terminated. Because the developers did not always null terminate strings, `'2.0N'` should not be confused with `'2.0N\0'`.
* All data types in SLP are little endian (e.g. `[0x01, 0x00]` becomes 1, not 256). All data structures are stored in sequential order, C style.
* All structure examples are written in C. I also use [GNU C datatypes](https://os.mbed.com/handbook/C-Data-Types) from `stdint.h`, with a small variation: `(u?)int8_t` means I was unable to find whether or not the number is signed. For most of these numbers the signing doesn't seem to make much of a difference.
* If an element in a structure has an assignment statement to a constant such as `uint8_t thing = 7;` this means that I have not observed this value changing across SLP files, and as a result it is probably safe to ignore. If the assignment statement is to a calculated value such as `uint8_t thing = 7 * WIDTH` the value may change but can be derived by means other than reading it.

## Structure

SLP files are encoded as raw binary, using little-endian and a varying word size depending on the section. There are three compon

## Header

```C
typedef struct Header
{
    char         Version[4]               = "2.0N";
    (u?)int32_t  Num_Frames;
    char         Comment[24]              = "ArtDesk1.00 SLP Writer\0";
    Frame_Info   Frame_Data[Num_Frames];
} Header;
```

## `Frame_Data` Array

```C
typedef struct Frame_Info
{
    uint32_t     Shape_Data_Offset;    
    uint32_t     Shape_Outline_Offset;
    uint32_t     Palette_Offset          = 0;
    uint32_t     Properties              = 1;
    (u?)int32_t  Width;
    (u?)int32_t  Height;
    int32_t      Hotspot_X;
    int32_t      Hotspot_Y;
} Frame_Info;
```

## Outline Data

One for each row, store the distance from the left edge to start and the distance from the right edge to finish, exclusive (only store skip count not index)

```C
struct rowedge
{
    uint16_t left; // exclusive
    uint16_t right; // exclusive 
};

rowedge rows[Frame_Info.Height];
```

## Command Offset Data

An array of longs of size `height`, which stores offsets to the first command of each row.

```C
uint32_t offsets[Frame_Info.Height];
```

## Frames

Colors are stored bytes.

TODO: Color palette, document outline array/frame arrays

player color = requested color | player num << 4

```C
typedef struct Frame
```