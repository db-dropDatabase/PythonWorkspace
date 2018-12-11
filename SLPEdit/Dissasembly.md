# Disassembly of ArcherMoving.slp

## Header

```C
typedef struct Header
{
    char         Version[4]               = "2.0N";
    (u?)int64_t  Num_Frames;              = 50 0x32
    char         Comment[24]              = "ArtDesk1.00 SLP Writer\0";
    Frame_Info   Frame_Data[Num_Frames];
} Header;
```

## First Frame `Frame_Data` Array

```C
typedef struct Frame_Info
{
    uint32_t     Shape_Data_Offset       = 1824 0x720;    
    uint32_t     Shape_Outline_Offset    = 1632 0x660;
    uint32_t     Palette_Offset          = 0;
    uint32_t     Properties              = 24 0x16;
    (u?)int32_t  Width                   = 20 0x14;
    (u?)int32_t  Height                  = 48 0x30;
    int32_t      Hotspot_X               = 10 0x0A;
    int32_t      Hotspot_Y               = 38 0x26;
} Frame_Info;
```

## First Outline Data

```C
struct rowedge
{
	short left = 9, right = 10;
};
```

## First Frame

Draw 56 pixels, bitmap encoded